"""
FastAPI application for Ariba Web Service Client.
Provides REST API endpoints for interacting with Ariba's Polling Service.
"""

import time
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from src.config import Config
from src.ariba_client import AribaClient
from src.models import (
    PollingRequest, 
    PollingResponse, 
    HealthResponse, 
    ConfigResponse
)
from src.exceptions import AribaConfigError, AribaServiceError, AribaAuthenticationError

# Global variables for app state
config: Config = None
client: AribaClient = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    global config, client
    
    print("Starting AribaWS3 API...")
    
    # Initialize configuration
    config = Config()
    if not config.load_environment_variables():
        raise AribaConfigError("Failed to load environment variables")
    
    if not config.validate_credentials():
        raise AribaConfigError("Invalid credentials configuration")
    
    # Initialize Ariba client
    client = AribaClient(config)
    
    print("AribaWS3 API started successfully!")
    
    yield
    
    # Shutdown
    if client:
        client.close()
    print("AribaWS3 API shutdown complete.")


# Create FastAPI app
app = FastAPI(
    title="AribaWS3 API",
    description="FastAPI-based client for Ariba Web Services",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_client() -> AribaClient:
    """Dependency to get the Ariba client."""
    if client is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return client


def get_config() -> Config:
    """Dependency to get the configuration."""
    if config is None:
        raise HTTPException(status_code=503, detail="Configuration not loaded")
    return config


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "AribaWS3 API",
        "version": "0.1.0",
        "description": "FastAPI-based client for Ariba Web Services"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
    )


@app.get("/config", response_model=ConfigResponse)
async def get_config_status(config_obj: Config = Depends(get_config)):
    """Get configuration status."""
    try:
        # Debug: Print the actual values to see what we're getting
        print(f"Debug - is_configured: {config_obj.is_configured} (type: {type(config_obj.is_configured)})")
        print(f"Debug - username: {config_obj.username} (type: {type(config_obj.username)})")
        print(f"Debug - password: {config_obj.password} (type: {type(config_obj.password)})")
        
        # Ensure we have proper boolean values with explicit conversion
        is_configured = bool(config_obj.is_configured) if config_obj.is_configured is not None else False
        has_creds = bool(config_obj.username and config_obj.password)
        
        print(f"Debug - final is_configured: {is_configured} (type: {type(is_configured)})")
        print(f"Debug - final has_creds: {has_creds} (type: {type(has_creds)})")
        
        return ConfigResponse(
            configured=is_configured,
            has_credentials=has_creds,
            base_url=config_obj.base_url
        )
    except Exception as e:
        print(f"Error in /config endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}")


@app.post("/poll", response_model=PollingResponse)
async def call_polling_service(
    request: PollingRequest,
    ariba_client: AribaClient = Depends(get_client)
):
    """
    Call Ariba's Polling Service.
    
    This endpoint sends a SOAP request to Ariba's Polling Service
    to check for business partner data replication requests.
    """
    try:
        result = ariba_client.call_polling_service(request.service_name)
        
        return PollingResponse(
            success=result["success"],
            status_code=result["status_code"],
            message=result["message"],
            data=result["data"],
            error=result["error"]
        )
        
    except AribaAuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except AribaServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/poll", response_model=PollingResponse)
async def call_polling_service_get(
    service_name: str = "BusinessPartnerSUITEBulkReplicateRequest_In",
    ariba_client: AribaClient = Depends(get_client)
):
    """
    Call Ariba's Polling Service (GET method).
    
    This endpoint sends a SOAP request to Ariba's Polling Service
    using the default service name.
    """
    try:
        result = ariba_client.call_polling_service(service_name)
        
        return PollingResponse(
            success=result["success"],
            status_code=result["status_code"],
            message=result["message"],
            data=result["data"],
            error=result["error"]
        )
        
    except AribaAuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except AribaServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)