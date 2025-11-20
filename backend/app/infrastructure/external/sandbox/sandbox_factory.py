import logging
from typing import Optional
from app.core.config import get_settings
from app.domain.external.sandbox import Sandbox
from .docker_sandbox import DockerSandbox
from .aio_docker_sandbox import AioDockerSandbox

logger = logging.getLogger(__name__)

class SandboxFactory:
    """Factory class for creating different types of sandbox instances"""

    @staticmethod
    async def create_sandbox(sandbox_type: str = "legacy", **kwargs) -> Sandbox:
        """
        Create a sandbox instance based on the specified type

        Args:
            sandbox_type: Type of sandbox to create ("legacy" or "aio")
            **kwargs: Additional keyword arguments for sandbox creation

        Returns:
            Sandbox instance

        Raises:
            ValueError: If sandbox_type is not supported
        """
        settings = get_settings()

        if sandbox_type == "legacy":
            logger.info("Creating legacy Docker sandbox")
            return await DockerSandbox.create(**kwargs)
        elif sandbox_type == "aio":
            logger.info("Creating AIO Docker sandbox")
            return await AioDockerSandbox.create(**kwargs)
        else:
            raise ValueError(f"Unsupported sandbox type: {sandbox_type}")

    @staticmethod
    async def get_sandbox(sandbox_id: str, sandbox_type: str = "legacy") -> Sandbox:
        """
        Get an existing sandbox instance by ID

        Args:
            sandbox_id: Container ID of the sandbox
            sandbox_type: Type of sandbox ("legacy" or "aio")

        Returns:
            Sandbox instance

        Raises:
            ValueError: If sandbox_type is not supported
        """
        if sandbox_type == "legacy":
            logger.info(f"Getting legacy Docker sandbox: {sandbox_id}")
            return await DockerSandbox.get(sandbox_id)
        elif sandbox_type == "aio":
            logger.info(f"Getting AIO Docker sandbox: {sandbox_id}")
            return await AioDockerSandbox.get(sandbox_id)
        else:
            raise ValueError(f"Unsupported sandbox type: {sandbox_type}")

    @staticmethod
    def get_default_sandbox_type() -> str:
        """
        Get the default sandbox type based on configuration

        Returns:
            Default sandbox type ("legacy" or "aio")
        """
        settings = get_settings()
        return "aio" if settings.aio_sandbox_enabled else "legacy"

    @staticmethod
    def is_aio_sandbox_enabled() -> bool:
        """
        Check if AIO Sandbox is enabled in configuration

        Returns:
            True if AIO Sandbox is enabled, False otherwise
        """
        settings = get_settings()
        return settings.aio_sandbox_enabled

    @staticmethod
    async def create_default_sandbox(**kwargs) -> Sandbox:
        """
        Create a sandbox instance using the default type

        Args:
            **kwargs: Additional keyword arguments for sandbox creation

        Returns:
            Sandbox instance
        """
        default_type = SandboxFactory.get_default_sandbox_type()
        return await SandboxFactory.create_sandbox(sandbox_type=default_type, **kwargs)

    @staticmethod
    async def get_default_sandbox(sandbox_id: str) -> Sandbox:
        """
        Get an existing sandbox instance using the default type

        Args:
            sandbox_id: Container ID of the sandbox

        Returns:
            Sandbox instance
        """
        default_type = SandboxFactory.get_default_sandbox_type()
        return await SandboxFactory.get_sandbox(sandbox_id, default_type)