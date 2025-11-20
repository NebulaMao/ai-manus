from typing import Dict, Any, Optional, List, BinaryIO
import uuid
import httpx
import docker
import socket
import logging
import asyncio
import io
from async_lru import alru_cache
from app.core.config import get_settings
from app.domain.models.tool_result import ToolResult
from app.domain.external.sandbox import Sandbox
from app.infrastructure.external.browser.playwright_browser import PlaywrightBrowser
from app.domain.external.browser import Browser
from app.domain.external.llm import LLM

logger = logging.getLogger(__name__)

class AioDockerSandbox(Sandbox):
    """AIO Sandbox implementation using ghcr.io/agent-infra/sandbox image"""

    def __init__(self, ip: str = None, container_name: str = None):
        """Initialize AIO Docker sandbox and API interaction client"""
        self.client = httpx.AsyncClient(timeout=600)
        self.ip = ip
        self.base_url = f"http://{self.ip}:8080"
        self._vnc_url = f"ws://{self.ip}:5900"  # AIO Sandbox uses standard VNC port
        self._cdp_url = f"http://{self.ip}:9222"
        self._container_name = container_name

    @property
    def id(self) -> str:
        """Sandbox ID"""
        if not self._container_name:
            return "aio-sandbox-dev"
        return self._container_name

    @property
    def cdp_url(self) -> str:
        return self._cdp_url

    @property
    def vnc_url(self) -> str:
        return self._vnc_url

    @staticmethod
    def _get_container_ip(container) -> str:
        """Get container IP address from network settings

        Args:
            container: Docker container instance

        Returns:
            Container IP address
        """
        # Get container network settings
        network_settings = container.attrs['NetworkSettings']
        ip_address = network_settings['IPAddress']

        # If default network has no IP, try to get IP from other networks
        if not ip_address and 'Networks' in network_settings:
            networks = network_settings['Networks']
            # Try to get IP from first available network
            for network_name, network_config in networks.items():
                if 'IPAddress' in network_config and network_config['IPAddress']:
                    ip_address = network_config['IPAddress']
                    break

        return ip_address

    @staticmethod
    def _create_task() -> 'AioDockerSandbox':
        """Create a new AIO Docker sandbox (static method)

        Returns:
            AioDockerSandbox instance
        """
        # Use configured default values
        settings = get_settings()

        # AIO Sandbox specific configuration
        image = settings.aio_sandbox_image
        name_prefix = "aio-sandbox"
        container_name = f"{name_prefix}-{str(uuid.uuid4())[:8]}"

        try:
            # Create Docker client
            docker_client = docker.from_env()

            # Prepare AIO Sandbox container configuration
            container_config = {
                "image": image,
                "name": container_name,
                "detach": True,
                "remove": True,
                "ports": {
                    "8080/tcp": None,  # Let Docker assign random host port
                    "5900/tcp": None,  # VNC port
                    "9222/tcp": None   # CDP port
                },
                "volumes": {
                    f"aio-{container_name}-workspace": {"bind": "/home/gem/workspace", "mode": "rw"},
                    f"aio-{container_name}-shared": {"bind": "/home/gem/shared", "mode": "rw"}
                },
                "security_opt": ["seccomp:unconfined"],
                "extra_hosts": {"host.docker.internal": "host-gateway"},
                "shm_size": "2gb",
                "environment": {
                    "WORKSPACE": "/home/gem",
                    "TZ": "UTC",
                    "PROXY_SERVER": "",
                    "JWT_PUBLIC_KEY": "",
                    "DNS_OVER_HTTPS_TEMPLATES": "",
                    "HOMEPAGE": "https://example.com",
                    "BROWSER_EXTRA_ARGS": "--disable-gpu",
                    "WAIT_PORTS": "3000,5000"
                },
                "healthcheck": {
                    "test": ["CMD", "curl", "-f", "http://localhost:8080/health"],
                    "interval": 30000000000,  # 30 seconds in nanoseconds
                    "timeout": 10000000000,   # 10 seconds in nanoseconds
                    "retries": 3
                }
            }

            # Add network to container config if configured
            if settings.sandbox_network:
                container_config["network"] = settings.sandbox_network

            # Create container
            container = docker_client.containers.run(**container_config)

            # Get container IP address
            container.reload()  # Refresh container info
            ip_address = AioDockerSandbox._get_container_ip(container)

            # Create and return AioDockerSandbox instance
            return AioDockerSandbox(
                ip=ip_address,
                container_name=container_name
            )

        except Exception as e:
            raise Exception(f"Failed to create AIO Docker sandbox: {str(e)}")

    async def ensure_sandbox(self) -> None:
        """Ensure AIO sandbox is ready by checking health endpoint"""
        max_retries = 30  # Maximum number of retries
        retry_interval = 2  # Seconds between retries

        for attempt in range(max_retries):
            try:
                # AIO Sandbox uses /health endpoint instead of supervisor status
                response = await self.client.get(f"{self.base_url}/health")
                response.raise_for_status()

                health_data = response.json()
                if health_data.get("status") == "healthy":
                    logger.info(f"AIO Sandbox is healthy and ready (attempt {attempt + 1}/{max_retries})")
                    return  # Success - sandbox is ready
                else:
                    logger.warning(f"AIO Sandbox not ready yet: {health_data} (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(retry_interval)

            except Exception as e:
                logger.warning(f"Failed to check AIO Sandbox health (attempt {attempt + 1}/{max_retries}): {str(e)}")
                await asyncio.sleep(retry_interval)

        # If we reach here, we've exhausted all retries
        error_message = f"AIO Sandbox failed to become healthy after {max_retries} attempts ({max_retries * retry_interval} seconds)"
        logger.error(error_message)
        # TODO: find a way to handle this
        #raise Exception(error_message)

    # AIO Sandbox uses different API endpoints, so we need to adapt the calls
    async def exec_command(self, session_id: str, exec_dir: str, command: str) -> ToolResult:
        """Execute command in AIO Sandbox"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/shell/exec",
                json={
                    "id": session_id,
                    "exec_dir": exec_dir,
                    "command": command
                }
            )
            return ToolResult(**response.json())
        except Exception as e:
            # Fallback: try to use AIO Sandbox's native API format
            try:
                response = await self.client.post(
                    f"{self.base_url}/v1/sandbox/shell",
                    json={
                        "session_id": session_id,
                        "command": command,
                        "cwd": exec_dir
                    }
                )
                result = response.json()
                return ToolResult(
                    success=True,
                    data=result.get("output", ""),
                    message=result.get("error", "")
                )
            except Exception as fallback_error:
                logger.error(f"Both API formats failed for exec_command: {str(e)}, fallback: {str(fallback_error)}")
                return ToolResult(success=False, message=f"Command execution failed: {str(e)}")

    async def view_shell(self, session_id: str, console: bool = False) -> ToolResult:
        """View shell status in AIO Sandbox"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/shell/view",
                json={
                    "id": session_id,
                    "console": console
                }
            )
            return ToolResult(**response.json())
        except Exception as e:
            # Fallback for AIO Sandbox
            return ToolResult(success=False, message=f"Shell view not implemented in AIO Sandbox: {str(e)}")

    async def wait_for_process(self, session_id: str, seconds: Optional[int] = None) -> ToolResult:
        """Wait for process in AIO Sandbox"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/shell/wait",
                json={
                    "id": session_id,
                    "seconds": seconds
                }
            )
            return ToolResult(**response.json())
        except Exception as e:
            # Fallback for AIO Sandbox
            return ToolResult(success=False, message=f"Process wait not implemented in AIO Sandbox: {str(e)}")

    async def write_to_process(self, session_id: str, input_text: str, press_enter: bool = True) -> ToolResult:
        """Write input to process in AIO Sandbox"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/shell/write",
                json={
                    "id": session_id,
                    "input": input_text,
                    "press_enter": press_enter
                }
            )
            return ToolResult(**response.json())
        except Exception as e:
            # Fallback for AIO Sandbox
            return ToolResult(success=False, message=f"Process write not implemented in AIO Sandbox: {str(e)}")

    async def kill_process(self, session_id: str) -> ToolResult:
        """Terminate process in AIO Sandbox"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/shell/kill",
                json={"id": session_id}
            )
            return ToolResult(**response.json())
        except Exception as e:
            # Fallback for AIO Sandbox
            return ToolResult(success=False, message=f"Process kill not implemented in AIO Sandbox: {str(e)}")

    async def file_write(self, file: str, content: str, append: bool = False,
                        leading_newline: bool = False, trailing_newline: bool = False,
                        sudo: bool = False) -> ToolResult:
        """Write content to file in AIO Sandbox"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/file/write",
                json={
                    "file": file,
                    "content": content,
                    "append": append,
                    "leading_newline": leading_newline,
                    "trailing_newline": trailing_newline,
                    "sudo": sudo
                }
            )
            return ToolResult(**response.json())
        except Exception as e:
            # Fallback for AIO Sandbox
            return ToolResult(success=False, message=f"File write not implemented in AIO Sandbox: {str(e)}")

    async def file_read(self, file: str, start_line: int = None,
                        end_line: int = None, sudo: bool = False) -> ToolResult:
        """Read file content in AIO Sandbox"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/file/read",
                json={
                    "file": file,
                    "start_line": start_line,
                    "end_line": end_line,
                    "sudo": sudo
                }
            )
            return ToolResult(**response.json())
        except Exception as e:
            # Fallback for AIO Sandbox
            return ToolResult(success=False, message=f"File read not implemented in AIO Sandbox: {str(e)}")

    async def file_exists(self, path: str) -> ToolResult:
        """Check if file exists in AIO Sandbox"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/file/exists",
                json={"path": path}
            )
            return ToolResult(**response.json())
        except Exception as e:
            # Fallback for AIO Sandbox
            return ToolResult(success=False, message=f"File exists check not implemented in AIO Sandbox: {str(e)}")

    async def file_delete(self, path: str) -> ToolResult:
        """Delete file in AIO Sandbox"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/file/delete",
                json={"path": path}
            )
            return ToolResult(**response.json())
        except Exception as e:
            # Fallback for AIO Sandbox
            return ToolResult(success=False, message=f"File delete not implemented in AIO Sandbox: {str(e)}")

    async def file_list(self, path: str) -> ToolResult:
        """List directory contents in AIO Sandbox"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/file/list",
                json={"path": path}
            )
            return ToolResult(**response.json())
        except Exception as e:
            # Fallback for AIO Sandbox
            return ToolResult(success=False, message=f"File list not implemented in AIO Sandbox: {str(e)}")

    async def file_replace(self, file: str, old_str: str, new_str: str, sudo: bool = False) -> ToolResult:
        """Replace string in file in AIO Sandbox"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/file/replace",
                json={
                    "file": file,
                    "old_str": old_str,
                    "new_str": new_str,
                    "sudo": sudo
                }
            )
            return ToolResult(**response.json())
        except Exception as e:
            # Fallback for AIO Sandbox
            return ToolResult(success=False, message=f"File replace not implemented in AIO Sandbox: {str(e)}")

    async def file_search(self, file: str, regex: str, sudo: bool = False) -> ToolResult:
        """Search in file content in AIO Sandbox"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/file/search",
                json={
                    "file": file,
                    "regex": regex,
                    "sudo": sudo
                }
            )
            return ToolResult(**response.json())
        except Exception as e:
            # Fallback for AIO Sandbox
            return ToolResult(success=False, message=f"File search not implemented in AIO Sandbox: {str(e)}")

    async def file_find(self, path: str, glob_pattern: str) -> ToolResult:
        """Find files by name pattern in AIO Sandbox"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/file/find",
                json={
                    "path": path,
                    "glob": glob_pattern
                }
            )
            return ToolResult(**response.json())
        except Exception as e:
            # Fallback for AIO Sandbox
            return ToolResult(success=False, message=f"File find not implemented in AIO Sandbox: {str(e)}")

    async def file_upload(self, file_data: BinaryIO, path: str, filename: str = None) -> ToolResult:
        """Upload file to AIO Sandbox"""
        try:
            # Prepare form data for upload
            files = {"file": (filename or "upload", file_data, "application/octet-stream")}
            data = {"path": path}

            response = await self.client.post(
                f"{self.base_url}/api/v1/file/upload",
                files=files,
                data=data
            )
            return ToolResult(**response.json())
        except Exception as e:
            # Fallback for AIO Sandbox
            return ToolResult(success=False, message=f"File upload not implemented in AIO Sandbox: {str(e)}")

    async def file_download(self, path: str) -> BinaryIO:
        """Download file from AIO Sandbox"""
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/file/download",
                params={"path": path}
            )
            response.raise_for_status()

            # Return the response content as a BinaryIO stream
            # TODO: change to real stream
            return io.BytesIO(response.content)
        except Exception as e:
            # Fallback for AIO Sandbox
            raise Exception(f"File download not implemented in AIO Sandbox: {str(e)}")

    @staticmethod
    @alru_cache(maxsize=128, typed=True)
    async def _resolve_hostname_to_ip(hostname: str) -> str:
        """Resolve hostname to IP address

        Args:
            hostname: Hostname to resolve

        Returns:
            Resolved IP address, or None if resolution fails

        Note:
            This method is cached using LRU cache with a maximum size of 128 entries.
            The cache helps reduce repeated DNS lookups for the same hostname.
        """
        try:
            # First check if hostname is already in IP address format
            try:
                socket.inet_pton(socket.AF_INET, hostname)
                # If successfully parsed, it's an IPv4 address format, return directly
                return hostname
            except OSError:
                # Not a valid IP address format, proceed with DNS resolution
                pass

            # Use socket.getaddrinfo for DNS resolution
            addr_info = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
            # Return the first IPv4 address found
            if addr_info and len(addr_info) > 0:
                return addr_info[0][4][0]  # Return sockaddr[0] from (family, type, proto, canonname, sockaddr), which is the IP address
            return None
        except Exception as e:
            # Log error and return None on failure
            logger.error(f"Failed to resolve hostname {hostname}: {str(e)}")
            return None

    async def destroy(self) -> bool:
        """Destroy AIO Docker sandbox"""
        try:
            if self.client:
                await self.client.aclose()
            if self._container_name:
                docker_client = docker.from_env()
                docker_client.containers.get(self._container_name).remove(force=True)
            return True
        except Exception as e:
            logger.error(f"Failed to destroy AIO Docker sandbox: {str(e)}")
            return False

    async def get_browser(self) -> Browser:
        """Get browser instance from AIO Sandbox

        Returns:
            Browser: Returns a configured PlaywrightBrowser instance
                    connected using the sandbox's CDP URL
        """
        return PlaywrightBrowser(self.cdp_url)

    @classmethod
    async def create(cls) -> Sandbox:
        """Create a new AIO sandbox instance

        Returns:
            New sandbox instance
        """
        settings = get_settings()

        if settings.sandbox_address:
            # Chrome CDP needs IP address
            ip = await cls._resolve_hostname_to_ip(settings.sandbox_address)
            return AioDockerSandbox(ip=ip)

        return await asyncio.to_thread(AioDockerSandbox._create_task)

    @classmethod
    @alru_cache(maxsize=128, typed=True)
    async def get(cls, id: str) -> Sandbox:
        """Get AIO sandbox by ID

        Args:
            id: Sandbox ID

        Returns:
            Sandbox instance
        """
        settings = get_settings()
        if settings.sandbox_address:
            ip = await cls._resolve_hostname_to_ip(settings.sandbox_address)
            return AioDockerSandbox(ip=ip, container_name=id)

        docker_client = docker.from_env()
        container = docker_client.containers.get(id)
        container.reload()

        ip_address = cls._get_container_ip(container)
        logger.info(f"AIO Sandbox IP address: {ip_address}")
        return AioDockerSandbox(ip=ip_address, container_name=id)