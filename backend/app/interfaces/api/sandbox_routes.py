"""
Sandbox management API routes

These routes provide endpoints for managing sandbox types,
preferences, and monitoring sandbox status.
"""

import time
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.interfaces.dependencies import get_current_user
from app.interfaces.schemas.base import APIResponse
from app.interfaces.schemas.sandbox import (
    SandboxTypeRequest,
    SandboxTypeResponse,
    SandboxStatusResponse,
    SandboxPreferenceResponse,
    HealthCheckResponse
)
from app.domain.models.user import User
from app.application.services.sandbox_selection_service import get_sandbox_selection_service
from app.infrastructure.external.sandbox.sandbox_factory import SandboxFactory

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sandbox", tags=["sandbox"])


@router.get("/type", response_model=APIResponse[SandboxTypeResponse])
async def get_sandbox_type(
    current_user: User = Depends(get_current_user)
) -> APIResponse[SandboxTypeResponse]:
    """
    Get the current sandbox type configuration

    Returns the current default sandbox type and whether AIO sandbox is enabled.
    """
    try:
        sandbox_service = get_sandbox_selection_service()

        response = SandboxTypeResponse(
            sandbox_type=sandbox_service.get_default_sandbox_type(),
            available_types=["legacy", "aio"],
            aio_enabled=sandbox_service.is_aio_sandbox_enabled()
        )

        logger.info(f"User {current_user.id} requested sandbox type info")
        return APIResponse.success(response)

    except Exception as e:
        logger.error(f"Failed to get sandbox type: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get sandbox type: {str(e)}"
        )


@router.post("/type", response_model=APIResponse[SandboxTypeResponse])
async def set_sandbox_type(
    request: SandboxTypeRequest,
    current_user: User = Depends(get_current_user)
) -> APIResponse[SandboxTypeResponse]:
    """
    Set the sandbox type preference (placeholder for future user preference storage)

    Currently this endpoint validates the sandbox type but doesn't persist user preferences.
    In a future implementation, this would store user preferences in the database.
    """
    try:
        sandbox_service = get_sandbox_selection_service()

        # Validate that the requested sandbox type is available
        if request.sandbox_type == "aio" and not sandbox_service.is_aio_sandbox_enabled():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="AIO sandbox is not enabled in configuration"
            )

        # TODO: Store user preference in database
        # For now, just validate and return current configuration

        response = SandboxTypeResponse(
            sandbox_type=sandbox_service.get_default_sandbox_type(),
            available_types=["legacy", "aio"],
            aio_enabled=sandbox_service.is_aio_sandbox_enabled()
        )

        logger.info(f"User {current_user.id} requested sandbox type: {request.sandbox_type}")
        return APIResponse.success(response)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to set sandbox type: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set sandbox type: {str(e)}"
        )


@router.get("/status/{sandbox_id}", response_model=APIResponse[SandboxStatusResponse])
async def get_sandbox_status(
    sandbox_id: str,
    sandbox_type: Optional[str] = None,
    current_user: User = Depends(get_current_user)
) -> APIResponse[SandboxStatusResponse]:
    """
    Get status information for a specific sandbox

    Returns detailed status information about the specified sandbox container.
    """
    try:
        sandbox_service = get_sandbox_selection_service()

        if sandbox_type is None:
            sandbox_type = sandbox_service.get_default_sandbox_type()

        # Get sandbox instance
        sandbox = await sandbox_service.get_sandbox(sandbox_id, sandbox_type)

        response = SandboxStatusResponse(
            sandbox_id=sandbox.id,
            sandbox_type=sandbox_type,
            status="running",  # TODO: Implement actual status checking
            base_url=sandbox.base_url,
            vnc_url=sandbox.vnc_url,
            cdp_url=sandbox.cdp_url
        )

        logger.info(f"User {current_user.id} requested status for sandbox {sandbox_id}")
        return APIResponse.success(response)

    except Exception as e:
        logger.error(f"Failed to get sandbox status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get sandbox status: {str(e)}"
        )


@router.get("/health", response_model=APIResponse[HealthCheckResponse])
async def check_sandbox_health(
    sandbox_type: Optional[str] = None,
    current_user: User = Depends(get_current_user)
) -> APIResponse[HealthCheckResponse]:
    """
    Check health of the default sandbox type

    Creates a temporary sandbox to verify that the sandbox system is working correctly.
    """
    try:
        sandbox_service = get_sandbox_selection_service()

        if sandbox_type is None:
            sandbox_type = sandbox_service.get_default_sandbox_type()

        start_time = time.time()

        # Create a test sandbox
        test_sandbox = await sandbox_service.create_sandbox(sandbox_type)

        try:
            # Try to ensure it's ready
            await test_sandbox.ensure_sandbox()

            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds

            response = HealthCheckResponse(
                is_healthy=True,
                response_time_ms=response_time
            )

            logger.info(f"Sandbox health check passed for {sandbox_type} in {response_time:.2f}ms")

        finally:
            # Clean up the test sandbox
            await test_sandbox.destroy()

        return APIResponse.success(response)

    except Exception as e:
        response_time = (time.time() - start_time) * 1000
        logger.error(f"Sandbox health check failed for {sandbox_type}: {str(e)}")

        response = HealthCheckResponse(
            is_healthy=False,
            response_time_ms=response_time,
            error_message=str(e)
        )

        return APIResponse.success(response)


@router.get("/compare", response_model=APIResponse[dict])
async def compare_sandbox_types(
    current_user: User = Depends(get_current_user)
) -> APIResponse[dict]:
    """
    Compare features and capabilities of different sandbox types

    Returns a comparison matrix showing the differences between legacy and AIO sandboxes.
    """
    try:
        sandbox_service = get_sandbox_selection_service()

        comparison = {
            "legacy": {
                "name": "Legacy Docker Sandbox",
                "description": "Original AI Manus sandbox implementation",
                "features": [
                    "File system operations",
                    "Shell command execution",
                    "Browser automation (Playwright)",
                    "VNC remote desktop",
                    "Process management"
                ],
                "advantages": [
                    "Stable and tested",
                    "Full compatibility",
                    "Lower resource usage"
                ],
                "limitations": [
                    "Limited tool ecosystem",
                    "No built-in development tools",
                    "Older technology stack"
                ]
            },
            "aio": {
                "name": "AIO Sandbox",
                "description": "Enhanced sandbox with MCP protocol support",
                "features": [
                    "All legacy features",
                    "MCP (Model Context Protocol) support",
                    "Chrome DevTools Protocol",
                    "Built-in Jupyter notebook",
                    "VSCode Server integration",
                    "Enhanced development tools",
                    "Modern container environment"
                ],
                "advantages": [
                    "Rich tool ecosystem",
                    "Standard protocols (MCP, CDP)",
                    "Better development experience",
                    "Active development"
                ],
                "limitations": [
                    "Higher resource usage",
                    "Newer technology (less tested)",
                    "Larger container image"
                ]
            }
        }

        # Add availability information
        comparison["current_default"] = sandbox_service.get_default_sandbox_type()
        comparison["aio_available"] = sandbox_service.is_aio_sandbox_enabled()

        logger.info(f"User {current_user.id} requested sandbox comparison")
        return APIResponse.success(comparison)

    except Exception as e:
        logger.error(f"Failed to get sandbox comparison: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get sandbox comparison: {str(e)}"
        )