"""
Sandbox-related schemas for API requests and responses
"""

from typing import Optional
from pydantic import BaseModel, Field


class SandboxTypeRequest(BaseModel):
    """Request model for setting sandbox type preference"""
    sandbox_type: str = Field(..., description="Sandbox type: 'legacy' or 'aio'", regex="^(legacy|aio)$")


class SandboxTypeResponse(BaseModel):
    """Response model for getting current sandbox type"""
    sandbox_type: str = Field(..., description="Current sandbox type")
    available_types: list[str] = Field(default=["legacy", "aio"], description="Available sandbox types")
    aio_enabled: bool = Field(..., description="Whether AIO sandbox is enabled in configuration")


class SandboxStatusResponse(BaseModel):
    """Response model for sandbox status information"""
    sandbox_id: str = Field(..., description="Sandbox container ID")
    sandbox_type: str = Field(..., description="Sandbox type")
    status: str = Field(..., description="Sandbox status")
    base_url: str = Field(..., description="Sandbox API base URL")
    vnc_url: Optional[str] = Field(None, description="VNC connection URL")
    cdp_url: Optional[str] = Field(None, description="Chrome DevTools Protocol URL")


class SandboxPreferenceResponse(BaseModel):
    """Response model for user sandbox preferences"""
    user_id: str = Field(..., description="User ID")
    preferred_sandbox_type: str = Field(..., description="User's preferred sandbox type")
    is_default: bool = Field(..., description="Whether using system default")


class HealthCheckResponse(BaseModel):
    """Response model for sandbox health check"""
    is_healthy: bool = Field(..., description="Whether the sandbox is healthy")
    response_time_ms: Optional[float] = Field(None, description="Health check response time in milliseconds")
    error_message: Optional[str] = Field(None, description="Error message if health check failed")