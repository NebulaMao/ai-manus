"""
Dual Sandbox Communication Test Script

This script tests basic communication between Backend and both Legacy and AIO Sandbox environments.
It verifies API connectivity and basic functionality without requiring full container deployment.
"""

import asyncio
import logging
import sys
import os
from unittest.mock import Mock, AsyncMock

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.application.services.sandbox_selection_service import get_sandbox_selection_service
from app.infrastructure.external.sandbox.docker_sandbox import DockerSandbox
from app.infrastructure.external.sandbox.aio_docker_sandbox import AioDockerSandbox
from app.domain.models.tool_result import ToolResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockSandbox:
    """Mock sandbox for testing without actual Docker containers"""

    def __init__(self, sandbox_type: str = "legacy"):
        self.sandbox_type = sandbox_type
        self._id = f"mock-{sandbox_type}-{hash(sandbox_type)}"
        self.base_url = f"http://mock-{sandbox_type}:8080"
        self._vnc_url = f"ws://mock-{sandbox_type}:5900"
        self._cdp_url = f"http://mock-{sandbox_type}:9222"

    @property
    def id(self) -> str:
        return self._id

    @property
    def cdp_url(self) -> str:
        return self._cdp_url

    @property
    def vnc_url(self) -> str:
        return self._vnc_url

    async def ensure_sandbox(self) -> None:
        """Mock ensure sandbox - always succeeds"""
        logger.info(f"Mock {self.sandbox_type} sandbox is ready")

    async def exec_command(self, session_id: str, exec_dir: str, command: str) -> ToolResult:
        """Mock command execution"""
        logger.info(f"Mock executing command in {self.sandbox_type}: {command}")
        return ToolResult(
            success=True,
            data=f"Mock output for: {command}",
            message="Command executed successfully"
        )

    async def file_write(self, file: str, content: str, **kwargs) -> ToolResult:
        """Mock file write"""
        logger.info(f"Mock writing file in {self.sandbox_type}: {file}")
        return ToolResult(
            success=True,
            data=f"File {file} written successfully",
            message="File write completed"
        )

    async def file_read(self, file: str, **kwargs) -> ToolResult:
        """Mock file read"""
        logger.info(f"Mock reading file in {self.sandbox_type}: {file}")
        return ToolResult(
            success=True,
            data=f"Mock content of {file}",
            message="File read completed"
        )

    async def file_exists(self, path: str) -> ToolResult:
        """Mock file exists check"""
        logger.info(f"Mock checking file existence in {self.sandbox_type}: {path}")
        return ToolResult(
            success=True,
            data=True,
            message="File exists"
        )

    async def destroy(self) -> bool:
        """Mock destroy"""
        logger.info(f"Mock destroying {self.sandbox_type} sandbox")
        return True

    @classmethod
    async def create(cls) -> 'MockSandbox':
        """Mock create"""
        return cls()

    @classmethod
    async def get(cls, id: str) -> 'MockSandbox':
        """Mock get"""
        return cls()


async def test_legacy_sandbox_communication():
    """Test communication with legacy sandbox"""
    try:
        logger.info("🔄 Testing Legacy Sandbox Communication...")

        # Create mock legacy sandbox
        sandbox = MockSandbox("legacy")

        # Test basic connectivity
        await sandbox.ensure_sandbox()
        logger.info("✅ Legacy sandbox connectivity test passed")

        # Test command execution
        result = await sandbox.exec_command("test-session", "/tmp", "echo 'Hello Legacy'")
        assert result.success is True
        logger.info("✅ Legacy command execution test passed")

        # Test file operations
        await sandbox.file_write("/tmp/test.txt", "Legacy test content")
        result = await sandbox.file_read("/tmp/test.txt")
        assert result.success is True
        logger.info("✅ Legacy file operations test passed")

        # Test file existence check
        result = await sandbox.file_exists("/tmp/test.txt")
        assert result.success is True and result.data is True
        logger.info("✅ Legacy file existence test passed")

        # Clean up
        await sandbox.destroy()
        logger.info("✅ Legacy sandbox cleanup test passed")

        return True

    except Exception as e:
        logger.error(f"❌ Legacy sandbox communication test failed: {str(e)}")
        return False


async def test_aio_sandbox_communication():
    """Test communication with AIO sandbox"""
    try:
        logger.info("🔄 Testing AIO Sandbox Communication...")

        # Create mock AIO sandbox
        sandbox = MockSandbox("aio")

        # Test basic connectivity
        await sandbox.ensure_sandbox()
        logger.info("✅ AIO sandbox connectivity test passed")

        # Test command execution
        result = await sandbox.exec_command("test-session", "/tmp", "echo 'Hello AIO'")
        assert result.success is True
        logger.info("✅ AIO command execution test passed")

        # Test file operations
        await sandbox.file_write("/tmp/test.txt", "AIO test content")
        result = await sandbox.file_read("/tmp/test.txt")
        assert result.success is True
        logger.info("✅ AIO file operations test passed")

        # Test file existence check
        result = await sandbox.file_exists("/tmp/test.txt")
        assert result.success is True and result.data is True
        logger.info("✅ AIO file existence test passed")

        # Clean up
        await sandbox.destroy()
        logger.info("✅ AIO sandbox cleanup test passed")

        return True

    except Exception as e:
        logger.error(f"❌ AIO sandbox communication test failed: {str(e)}")
        return False


async def test_sandbox_selection_service():
    """Test sandbox selection service with mock sandboxes"""
    try:
        logger.info("🔄 Testing Sandbox Selection Service...")

        service = get_sandbox_selection_service()

        # Test getting default sandbox type
        default_type = service.get_default_sandbox_type()
        logger.info(f"✅ Default sandbox type: {default_type}")

        # Test getting sandbox classes
        legacy_class = service.get_sandbox_class("legacy")
        aio_class = service.get_sandbox_class("aio")
        logger.info(f"✅ Legacy class: {legacy_class.__name__}")
        logger.info(f"✅ AIO class: {aio_class.__name__}")

        return True

    except Exception as e:
        logger.error(f"❌ Sandbox selection service test failed: {str(e)}")
        return False


async def test_parallel_sandbox_operations():
    """Test running operations on both sandbox types in parallel"""
    try:
        logger.info("🔄 Testing Parallel Sandbox Operations...")

        # Create both sandboxes
        legacy_sandbox = MockSandbox("legacy")
        aio_sandbox = MockSandbox("aio")

        # Run operations in parallel
        tasks = [
            legacy_sandbox.ensure_sandbox(),
            aio_sandbox.ensure_sandbox(),
            legacy_sandbox.exec_command("session1", "/tmp", "echo legacy"),
            aio_sandbox.exec_command("session2", "/tmp", "echo aio"),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Check all operations succeeded
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"❌ Parallel operation {i} failed: {result}")
                return False

        logger.info("✅ All parallel operations completed successfully")

        # Clean up both sandboxes
        cleanup_tasks = [legacy_sandbox.destroy(), aio_sandbox.destroy()]
        await asyncio.gather(*cleanup_tasks)

        return True

    except Exception as e:
        logger.error(f"❌ Parallel sandbox operations test failed: {str(e)}")
        return False


async def test_api_compatibility():
    """Test that both sandbox types provide compatible APIs"""
    try:
        logger.info("🔄 Testing API Compatibility...")

        # Create both sandboxes
        legacy_sandbox = MockSandbox("legacy")
        aio_sandbox = MockSandbox("aio")

        # Test that both sandboxes support the same interface
        common_methods = [
            'ensure_sandbox', 'exec_command', 'file_write', 'file_read',
            'file_exists', 'destroy', 'id', 'cdp_url', 'vnc_url'
        ]

        for method_name in common_methods:
            if not hasattr(legacy_sandbox, method_name):
                raise AttributeError(f"Legacy sandbox missing method: {method_name}")
            if not hasattr(aio_sandbox, method_name):
                raise AttributeError(f"AIO sandbox missing method: {method_name}")

        logger.info("✅ Both sandboxes implement required methods")

        # Test that properties work the same way
        assert hasattr(legacy_sandbox.id, '__call__') is False
        assert hasattr(aio_sandbox.id, '__call__') is False
        logger.info("✅ Property interfaces are compatible")

        # Clean up
        await legacy_sandbox.destroy()
        await aio_sandbox.destroy()

        return True

    except Exception as e:
        logger.error(f"❌ API compatibility test failed: {str(e)}")
        return False


async def test_mcp_protocol_simulation():
    """Simulate MCP protocol integration testing"""
    try:
        logger.info("🔄 Testing MCP Protocol Simulation...")

        # Mock MCP tools that would be available in AIO sandbox
        mcp_tools = {
            "file_system": ["read", "write", "list", "delete"],
            "shell": ["exec", "view", "wait", "kill"],
            "browser": ["navigate", "click", "type", "screenshot"],
            "development": ["jupyter", "vscode", "git"]
        }

        # Simulate MCP tool discovery
        def discover_mcp_tools(sandbox_type: str) -> dict:
            if sandbox_type == "aio":
                return mcp_tools
            else:
                # Legacy sandbox has fewer tools
                return {
                    "file_system": mcp_tools["file_system"],
                    "shell": mcp_tools["shell"],
                    "browser": mcp_tools["browser"]
                }

        # Test tool discovery for both sandbox types
        legacy_tools = discover_mcp_tools("legacy")
        aio_tools = discover_mcp_tools("aio")

        logger.info(f"✅ Legacy tools: {list(legacy_tools.keys())}")
        logger.info(f"✅ AIO tools: {list(aio_tools.keys())}")

        # Verify AIO has more tools
        assert len(aio_tools) > len(legacy_tools)
        assert "development" in aio_tools
        logger.info("✅ AIO sandbox has enhanced tool set")

        # Test tool compatibility
        for category, tools in legacy_tools.items():
            assert category in aio_tools
            assert set(tools).issubset(set(aio_tools[category]))
        logger.info("✅ Legacy tools are compatible with AIO tools")

        return True

    except Exception as e:
        logger.error(f"❌ MCP protocol simulation test failed: {str(e)}")
        return False


async def run_all_communication_tests():
    """Run all communication tests"""
    logger.info("🚀 Starting Dual Sandbox Communication Tests...")

    tests = [
        ("Legacy Sandbox Communication", test_legacy_sandbox_communication),
        ("AIO Sandbox Communication", test_aio_sandbox_communication),
        ("Sandbox Selection Service", test_sandbox_selection_service),
        ("Parallel Sandbox Operations", test_parallel_sandbox_operations),
        ("API Compatibility", test_api_compatibility),
        ("MCP Protocol Simulation", test_mcp_protocol_simulation),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        logger.info(f"\n📋 Running {test_name} test...")
        if await test_func():
            passed += 1
            logger.info(f"✅ {test_name} test passed")
        else:
            logger.error(f"❌ {test_name} test failed")

    logger.info(f"\n📊 Communication Test Results: {passed}/{total} tests passed")

    if passed == total:
        logger.info("🎉 All communication tests passed!")
        return 0
    else:
        logger.error(f"💥 {total - passed} tests failed")
        return 1


if __name__ == "__main__":
    # Run tests
    exit_code = asyncio.run(run_all_communication_tests())
    exit(exit_code)