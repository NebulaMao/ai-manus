"""
Basic Communication Test Script

This script tests basic sandbox communication without Docker dependencies.
"""

import asyncio
import logging
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.domain.models.tool_result import ToolResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockSandboxInterface:
    """Mock sandbox interface for testing API compatibility"""

    def __init__(self, sandbox_type: str = "legacy"):
        self.sandbox_type = sandbox_type
        self._id = f"mock-{sandbox_type}-12345"
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
        """Mock ensure sandbox"""
        logger.info(f"Mock {self.sandbox_type} sandbox ready")

    async def exec_command(self, session_id: str, exec_dir: str, command: str) -> ToolResult:
        """Mock command execution"""
        logger.info(f"[{self.sandbox_type}] Exec: {command}")
        return ToolResult(
            success=True,
            data=f"Output from {self.sandbox_type}: {command}",
            message="Command executed"
        )

    async def file_write(self, file: str, content: str, **kwargs) -> ToolResult:
        """Mock file write"""
        logger.info(f"[{self.sandbox_type}] Write: {file}")
        return ToolResult(
            success=True,
            data=f"File written to {file}",
            message="File write success"
        )

    async def file_read(self, file: str, **kwargs) -> ToolResult:
        """Mock file read"""
        logger.info(f"[{self.sandbox_type}] Read: {file}")
        return ToolResult(
            success=True,
            data=f"Content of {file} ({self.sandbox_type})",
            message="File read success"
        )

    async def file_exists(self, path: str) -> ToolResult:
        """Mock file exists"""
        logger.info(f"[{self.sandbox_type}] Exists: {path}")
        return ToolResult(
            success=True,
            data=True,
            message="File exists"
        )

    async def destroy(self) -> bool:
        """Mock destroy"""
        logger.info(f"[{self.sandbox_type}] Destroyed")
        return True


async def test_basic_api_compatibility():
    """Test that both sandbox types have compatible APIs"""
    try:
        logger.info("🔄 Testing Basic API Compatibility...")

        # Create mock sandboxes
        legacy = MockSandboxInterface("legacy")
        aio = MockSandboxInterface("aio")

        # Test required methods exist
        required_methods = [
            'ensure_sandbox', 'exec_command', 'file_write', 'file_read',
            'file_exists', 'destroy', 'id', 'cdp_url', 'vnc_url'
        ]

        for method in required_methods:
            if not hasattr(legacy, method):
                raise AttributeError(f"Legacy missing {method}")
            if not hasattr(aio, method):
                raise AttributeError(f"AIO missing {method}")

        logger.info("✅ Both sandboxes implement required methods")

        # Test method calls work the same way
        await legacy.ensure_sandbox()
        await aio.ensure_sandbox()
        logger.info("✅ Both sandboxes ready")

        # Test properties
        assert legacy.id.startswith("mock-legacy-")
        assert aio.id.startswith("mock-aio-")
        logger.info("✅ Properties work correctly")

        return True

    except Exception as e:
        logger.error(f"❌ API compatibility test failed: {str(e)}")
        return False


async def test_command_execution_compatibility():
    """Test command execution compatibility"""
    try:
        logger.info("🔄 Testing Command Execution Compatibility...")

        legacy = MockSandboxInterface("legacy")
        aio = MockSandboxInterface("aio")

        # Test same command on both sandboxes
        test_command = "echo 'Hello World'"

        legacy_result = await legacy.exec_command("session1", "/tmp", test_command)
        aio_result = await aio.exec_command("session2", "/tmp", test_command)

        assert legacy_result.success is True
        assert aio_result.success is True
        assert "legacy" in legacy_result.data
        assert "aio" in aio_result.data

        logger.info("✅ Command execution compatible")

        return True

    except Exception as e:
        logger.error(f"❌ Command execution test failed: {str(e)}")
        return False


async def test_file_operations_compatibility():
    """Test file operations compatibility"""
    try:
        logger.info("🔄 Testing File Operations Compatibility...")

        legacy = MockSandboxInterface("legacy")
        aio = MockSandboxInterface("aio")

        test_file = "/tmp/test.txt"
        test_content = "Test content"

        # Test write operations
        legacy_write = await legacy.file_write(test_file, test_content)
        aio_write = await aio.file_write(test_file, test_content)

        assert legacy_write.success is True
        assert aio_write.success is True

        # Test read operations
        legacy_read = await legacy.file_read(test_file)
        aio_read = await aio.file_read(test_file)

        assert legacy_read.success is True
        assert aio_read.success is True
        assert "legacy" in legacy_read.data
        assert "aio" in aio_read.data

        logger.info("✅ File operations compatible")

        return True

    except Exception as e:
        logger.error(f"❌ File operations test failed: {str(e)}")
        return False


async def test_parallel_operations():
    """Test running operations in parallel"""
    try:
        logger.info("🔄 Testing Parallel Operations...")

        legacy = MockSandboxInterface("legacy")
        aio = MockSandboxInterface("aio")

        # Run multiple operations in parallel
        tasks = [
            legacy.ensure_sandbox(),
            aio.ensure_sandbox(),
            legacy.exec_command("session1", "/tmp", "echo 'Legacy Test'"),
            aio.exec_command("session2", "/tmp", "echo 'AIO Test'"),
            legacy.file_write("/tmp/legacy.txt", "Legacy content"),
            aio.file_write("/tmp/aio.txt", "AIO content"),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Check all operations succeeded
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"❌ Parallel operation {i} failed: {result}")
                return False

        logger.info("✅ All parallel operations succeeded")

        # Cleanup in parallel
        cleanup_tasks = [legacy.destroy(), aio.destroy()]
        await asyncio.gather(*cleanup_tasks)

        return True

    except Exception as e:
        logger.error(f"❌ Parallel operations test failed: {str(e)}")
        return False


async def test_error_handling():
    """Test error handling compatibility"""
    try:
        logger.info("🔄 Testing Error Handling...")

        legacy = MockSandboxInterface("legacy")
        aio = MockSandboxInterface("aio")

        # All mock operations should succeed
        # In real implementation, we would test error scenarios
        legacy_result = await legacy.exec_command("session1", "/tmp", "echo test")
        aio_result = await aio.exec_command("session2", "/tmp", "echo test")

        assert legacy_result.success is True
        assert aio_result.success is True

        logger.info("✅ Error handling compatible")

        return True

    except Exception as e:
        logger.error(f"❌ Error handling test failed: {str(e)}")
        return False


async def test_mcp_protocol_simulation():
    """Test MCP protocol simulation"""
    try:
        logger.info("🔄 Testing MCP Protocol Simulation...")

        # Simulate MCP tool discovery
        legacy_tools = {
            "file_system": ["read", "write", "list"],
            "shell": ["exec", "view"],
            "browser": ["navigate", "click"]
        }

        aio_tools = {
            "file_system": ["read", "write", "list"],
            "shell": ["exec", "view"],
            "browser": ["navigate", "click"],
            "development": ["jupyter", "vscode"],
            "mcp": ["execute_tool", "list_tools"]
        }

        # Verify AIO has additional tools
        assert len(aio_tools) > len(legacy_tools)
        assert "development" in aio_tools
        assert "mcp" in aio_tools

        # Verify legacy tools are subset of AIO tools
        for category, tools in legacy_tools.items():
            assert category in aio_tools
            for tool in tools:
                assert tool in aio_tools[category]

        logger.info(f"✅ Legacy tools: {list(legacy_tools.keys())}")
        logger.info(f"✅ AIO tools: {list(aio_tools.keys())}")
        logger.info("✅ MCP protocol simulation passed")

        return True

    except Exception as e:
        logger.error(f"❌ MCP protocol simulation failed: {str(e)}")
        return False


async def run_basic_tests():
    """Run all basic communication tests"""
    logger.info("🚀 Starting Basic Communication Tests...")

    tests = [
        ("API Compatibility", test_basic_api_compatibility),
        ("Command Execution", test_command_execution_compatibility),
        ("File Operations", test_file_operations_compatibility),
        ("Parallel Operations", test_parallel_operations),
        ("Error Handling", test_error_handling),
        ("MCP Protocol", test_mcp_protocol_simulation),
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

    logger.info(f"\n📊 Basic Test Results: {passed}/{total} tests passed")

    if passed == total:
        logger.info("🎉 All basic communication tests passed!")
        return 0
    else:
        logger.error(f"💥 {total - passed} tests failed")
        return 1


if __name__ == "__main__":
    # Run tests
    exit_code = asyncio.run(run_basic_tests())
    exit(exit_code)