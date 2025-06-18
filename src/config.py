"""
Configuration management for AribaWS2.
Handles environment variables and application settings.
"""

import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration class for AribaWS2 application."""
    
    def __init__(self):
        self._loaded = False
        self._username: Optional[str] = None
        self._password: Optional[str] = None
        self._base_url: str = "https://s1.ariba.com/SM/soap/PollingService"
    
    def load_environment_variables(self) -> bool:
        """
        Load environment variables from .env file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            load_dotenv()
            self._username = os.environ.get('ARIBA_USERNAME')
            self._password = os.environ.get('ARIBA_PASSWORD')
            self._loaded = True
            return True
        except Exception as e:
            print(f"Error loading environment variables: {str(e)}")
            return False
    
    @property
    def username(self) -> Optional[str]:
        """Get the Ariba username."""
        return self._username
    
    @property
    def password(self) -> Optional[str]:
        """Get the Ariba password."""
        return self._password
    
    @property
    def base_url(self) -> str:
        """Get the Ariba base URL."""
        return self._base_url
    
    @property
    def is_configured(self) -> bool:
        """Check if configuration is properly loaded."""
        return self._loaded and self._username and self._password
    
    def validate_credentials(self) -> bool:
        """
        Validate that required credentials are available.
        
        Returns:
            bool: True if credentials are valid, False otherwise
        """
        if not self.is_configured:
            print("Error: ARIBA_USERNAME or ARIBA_PASSWORD environment variables not set")
            return False
        return True 