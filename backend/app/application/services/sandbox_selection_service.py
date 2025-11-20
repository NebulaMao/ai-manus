"""
Sandbox Selection Service

This service manages the selection between legacy and AIO sandbox types.
It can be configured globally or per-session based on user preferences.
"""

import logging
from typing import Optional
from app.core.config import get_settings
from app.domain.external.sandbox import Sandbox
from app.infrastructure.external.sandbox.sandbox_factory import SandboxFactory
from app.infrastructure.external.sandbox.docker_sandbox import DockerSandbox
from app.infrastructure.external.sandbox.aio_docker_sandbox import AioDockerSandbox

logger = logging.getLogger(__name__)

class SandboxSelectionService:
    """
    Service for managing sandbox type selection
    """

    def __init__(self):
        self._settings = get_settings()
        logger.info(f"SandboxSelectionService initialized with AIO enabled: {self._settings.aio_sandbox_enabled}")

    def get_sandbox_class(self, sandbox_type: Optional[str] = None) -> type:
        """
        Get the appropriate sandbox class based on configuration or explicit type

        Args:
            sandbox_type: Explicit sandbox type ("legacy" or "aio"). If None, uses default.

        Returns:
            Sandbox class to use
        """
        if sandbox_type is None:
            sandbox_type = self.get_default_sandbox_type()

        if sandbox_type == "aio":
            logger.debug("Selected AIO Docker sandbox")
            return AioDockerSandbox
        else:
            logger.debug("Selected legacy Docker sandbox")
            return DockerSandbox

    def get_default_sandbox_type(self) -> str:
        """
        Get the default sandbox type based on configuration

        Returns:
            Default sandbox type ("legacy" or "aio")
        """
        return "aio" if self._settings.aio_sandbox_enabled else "legacy"

    def is_aio_sandbox_enabled(self) -> bool:
        """
        Check if AIO sandbox is enabled in configuration

        Returns:
            True if AIO sandbox is enabled
        """
        return self._settings.aio_sandbox_enabled

    async def create_sandbox(self, sandbox_type: Optional[str] = None, **kwargs) -> Sandbox:
        """
        Create a sandbox instance of the specified type

        Args:
            sandbox_type: Type of sandbox to create. If None, uses default.
            **kwargs: Additional arguments for sandbox creation

        Returns:
            Sandbox instance
        """
        if sandbox_type is None:
            sandbox_type = self.get_default_sandbox_type()

        return await SandboxFactory.create_sandbox(sandbox_type=sandbox_type, **kwargs)

    async def get_sandbox(self, sandbox_id: str, sandbox_type: Optional[str] = None) -> Sandbox:
        """
        Get an existing sandbox instance

        Args:
            sandbox_id: Container ID of the sandbox
            sandbox_type: Type of sandbox. If None, uses default.

        Returns:
            Sandbox instance
        """
        if sandbox_type is None:
            sandbox_type = self.get_default_sandbox_type()

        return await SandboxFactory.get_sandbox(sandbox_id, sandbox_type)


# Global instance for dependency injection
_sandbox_selection_service: Optional[SandboxSelectionService] = None

def get_sandbox_selection_service() -> SandboxSelectionService:
    """
    Get singleton instance of SandboxSelectionService

    Returns:
        SandboxSelectionService instance
    """
    global _sandbox_selection_service
    if _sandbox_selection_service is None:
        _sandbox_selection_service = SandboxSelectionService()
    return _sandbox_selection_service

def get_default_sandbox_class() -> type:
    """
    Get the default sandbox class for dependency injection

    Returns:
        Default sandbox class
    """
    service = get_sandbox_selection_service()
    return service.get_sandbox_class()