"""
Pydantic models for API request and response handling.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class PollingRequest(BaseModel):
    """Request model for polling service calls."""
    service_name: str = Field(
        default="BusinessPartnerSUITEBulkReplicateRequest_In",
        description="Name of the inbound service to poll"
    )


class PollingResponse(BaseModel):
    """Response model for polling service calls."""
    success: bool = Field(description="Whether the request was successful")
    status_code: Optional[int] = Field(description="HTTP status code")
    message: str = Field(description="Response message")
    data: Optional[Dict[str, Any]] = Field(description="Response data")
    error: Optional[str] = Field(description="Error message if any")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(description="Service status")
    version: str = Field(description="API version")
    timestamp: str = Field(description="Current timestamp")


class ConfigResponse(BaseModel):
    """Configuration status response model."""
    configured: bool = Field(description="Whether configuration is loaded")
    has_credentials: bool = Field(description="Whether credentials are available")
    base_url: str = Field(description="Ariba base URL") 