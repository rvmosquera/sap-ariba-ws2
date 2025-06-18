"""
Main entry point for AribaWS2 application.
"""

from src.config import Config
from src.ariba_client import AribaClient

def main():
    """Main application entry point."""
    print("AribaWS2 - Starting application...")
    
    # Initialize configuration
    config = Config()
    
    # Load environment variables
    if not config.load_environment_variables():
        print("Failed to load environment variables. Exiting.")
        return
    
    # Validate credentials
    if not config.validate_credentials():
        print("Invalid credentials. Exiting.")
        return
    
    # Initialize Ariba client
    client = AribaClient(config)
    
    try:
        # Call the polling service
        response = client.call_polling_service()
        
        if response is None:
            print("Failed to call Ariba polling service.")
        else:
            print("Ariba polling service call completed.")
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    
    finally:
        # Clean up
        client.close()
        print("Application finished.")


if __name__ == "__main__":
    main()