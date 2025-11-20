"""
AIO Sandbox deployment test script

This script tests the basic deployment and connectivity of AIO Sandbox containers.
"""

import asyncio
import logging
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.infrastructure.external.sandbox.sandbox_factory import SandboxFactory
from app.infrastructure.external.sandbox.aio_docker_sandbox import AioDockerSandbox

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_aio_sandbox_factory():
    """Test AIO Sandbox factory creation"""
    try:
        # Test creating an AIO sandbox
        sandbox = await SandboxFactory.create_sandbox(sandbox_type="aio")

        # Verify it's the correct type
        assert isinstance(sandbox, AioDockerSandbox)

        # Test basic properties
        assert sandbox.id is not None
        assert sandbox.base_url is not None

        logger.info(f"Created AIO Sandbox with ID: {sandbox.id}")
        logger.info(f"Sandbox base URL: {sandbox.base_url}")

        # Clean up
        destroyed = await sandbox.destroy()
        assert destroyed is True

        logger.info("AIO Sandbox test completed successfully")

    except Exception as e:
        logger.error(f"AIO Sandbox factory test failed: {str(e)}")
        raise

async def test_aio_sandbox_health_check():
    """Test AIO Sandbox health check functionality"""
    try:
        # Create AIO sandbox
        sandbox = await SandboxFactory.create_sandbox(sandbox_type="aio")

        # Wait for sandbox to be ready
        await sandbox.ensure_sandbox()

        logger.info(f"AIO Sandbox {sandbox.id} is ready and healthy")

        # Clean up
        await sandbox.destroy()

        logger.info("AIO Sandbox health check test completed successfully")

    except Exception as e:
        logger.error(f"AIO Sandbox health check test failed: {str(e)}")
        # Try to clean up even if test fails
        try:
            await sandbox.destroy()
        except:
            pass
        raise

async def test_legacy_vs_aio_sandbox():
    """Test that both legacy and AIO sandboxes can be created"""
    try:
        # Create legacy sandbox
        legacy_sandbox = await SandboxFactory.create_sandbox(sandbox_type="legacy")
        logger.info(f"Created legacy sandbox: {legacy_sandbox.id}")

        # Create AIO sandbox
        aio_sandbox = await SandboxFactory.create_sandbox(sandbox_type="aio")
        logger.info(f"Created AIO sandbox: {aio_sandbox.id}")

        # Verify they are different types
        assert type(legacy_sandbox).__name__ == "DockerSandbox"
        assert type(aio_sandbox).__name__ == "AioDockerSandbox"

        # Clean up both
        await legacy_sandbox.destroy()
        await aio_sandbox.destroy()

        logger.info("Legacy vs AIO sandbox test completed successfully")

    except Exception as e:
        logger.error(f"Legacy vs AIO sandbox test failed: {str(e)}")
        # Try to clean up even if test fails
        try:
            await legacy_sandbox.destroy()
        except:
            pass
        try:
            await aio_sandbox.destroy()
        except:
            pass
        raise

if __name__ == "__main__":
    """
    Manual test runner for quick verification
    """
    async def run_manual_tests():
        """Run tests manually without pytest"""
        print("Starting manual AIO Sandbox deployment tests...")

        try:
            await test_aio_sandbox_factory()
            print("✅ Factory test passed")

            await test_aio_sandbox_health_check()
            print("✅ Health check test passed")

            await test_legacy_vs_aio_sandbox()
            print("✅ Comparison test passed")

            print("🎉 All manual tests passed!")

        except Exception as e:
            print(f"❌ Manual test failed: {str(e)}")
            return 1

        return 0

    # Run manual tests
    exit_code = asyncio.run(run_manual_tests())
    exit(exit_code)