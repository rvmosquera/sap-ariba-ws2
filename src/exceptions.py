"""
Custom exceptions for the Ariba API.
"""

from fastapi import HTTPException, status


class AribaConfigError(HTTPException):
    """Raised when configuration is invalid or missing."""
    def __init__(self, detail: str = "Configuration error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class AribaAuthenticationError(HTTPException):
    """Raised when authentication fails."""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )


class AribaServiceError(HTTPException):
    """Raised when Ariba service call fails."""
    def __init__(self, detail: str = "Ariba service error", status_code: int = 502):
        super().__init__(
            status_code=status_code,
            detail=detail
        ) 