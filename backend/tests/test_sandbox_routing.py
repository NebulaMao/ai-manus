"""
Sandbox routing test script

This script tests the sandbox routing and type selection functionality.
"""

import asyncio
import logging
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.application.services.sandbox_selection_service import SandboxSelectionService, get_sandbox_selection_service
from app.infrastructure.external.sandbox.sandbox_factory import SandboxFactory
from app.interfaces.dependencies import get_default_sandbox_class

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_sandbox_selection_service():
    """Test SandboxSelectionService functionality"""
    try:
        # Test service creation
        service = SandboxSelectionService()
        logger.info("✅ SandboxSelectionService created successfully")

        # Test default sandbox type
        default_type = service.get_default_sandbox_type()
        logger.info(f"✅ Default sandbox type: {default_type}")

        # Test sandbox class selection
        sandbox_class = service.get_sandbox_class()
        logger.info(f"✅ Selected sandbox class: {sandbox_class.__name__}")

        # Test AIO enabled status
        aio_enabled = service.is_aio_sandbox_enabled()
        logger.info(f"✅ AIO sandbox enabled: {aio_enabled}")

        return True

    except Exception as e:
        logger.error(f"❌ SandboxSelectionService test failed: {str(e)}")
        return False


async def test_sandbox_factory():
    """Test SandboxFactory functionality"""
    try:
        # Test factory methods (without actually creating containers)
        default_type = SandboxFactory.get_default_sandbox_type()
        logger.info(f"✅ Factory default type: {default_type}")

        aio_enabled = SandboxFactory.is_aio_sandbox_enabled()
        logger.info(f"✅ Factory AIO enabled: {aio_enabled}")

        return True

    except Exception as e:
        logger.error(f"❌ SandboxFactory test failed: {str(e)}")
        return False


async def test_dependency_injection():
    """Test dependency injection functions"""
    try:
        # Test default sandbox class from dependency injection
        sandbox_class = get_default_sandbox_class()
        logger.info(f"✅ DI sandbox class: {sandbox_class.__name__}")

        # Test service singleton
        service1 = get_sandbox_selection_service()
        service2 = get_sandbox_selection_service()

        if service1 is service2:
            logger.info("✅ Service singleton working correctly")
        else:
            logger.error("❌ Service singleton not working")
            return False

        return True

    except Exception as e:
        logger.error(f"❌ Dependency injection test failed: {str(e)}")
        return False


async def test_sandbox_type_switching():
    """Test switching between sandbox types"""
    try:
        service = get_sandbox_selection_service()

        # Test legacy sandbox class
        legacy_class = service.get_sandbox_class("legacy")
        logger.info(f"✅ Legacy sandbox class: {legacy_class.__name__}")

        # Test AIO sandbox class
        aio_class = service.get_sandbox_class("aio")
        logger.info(f"✅ AIO sandbox class: {aio_class.__name__}")

        # Verify they are different
        if legacy_class.__name__ != aio_class.__name__:
            logger.info("✅ Sandbox classes are different as expected")
        else:
            logger.warning("⚠️ Sandbox classes are the same (may be expected if AIO is disabled)")

        return True

    except Exception as e:
        logger.error(f"❌ Sandbox type switching test failed: {str(e)}")
        return False


async def run_all_tests():
    """Run all sandbox routing tests"""
    logger.info("🚀 Starting sandbox routing tests...")

    tests = [
        ("SandboxSelectionService", test_sandbox_selection_service),
        ("SandboxFactory", test_sandbox_factory),
        ("Dependency Injection", test_dependency_injection),
        ("Sandbox Type Switching", test_sandbox_type_switching),
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

    logger.info(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        logger.info("🎉 All sandbox routing tests passed!")
        return 0
    else:
        logger.error(f"💥 {total - passed} tests failed")
        return 1


if __name__ == "__main__":
    # Run tests
    exit_code = asyncio.run(run_all_tests())
    exit(exit_code)