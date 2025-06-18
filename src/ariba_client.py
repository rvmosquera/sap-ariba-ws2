"""
Ariba web service client.
Handles SOAP requests to Ariba's Polling Service.
"""

import base64
import time
from typing import Optional
import requests
from .config import Config


class AribaClient:
    """Client for interacting with Ariba web services."""
    
    def __init__(self, config: Config):
        """
        Initialize the Ariba client.
        
        Args:
            config: Configuration object containing credentials and settings
        """
        self.config = config
        self.session = requests.Session()
    
    def _create_auth_header(self) -> str:
        """
        Create Basic Authentication header.
        
        Returns:
            str: Base64 encoded authentication string
        """
        auth_string = f"{self.config.username}:{self.config.password}"
        auth_bytes = auth_string.encode('ascii')
        return base64.b64encode(auth_bytes).decode('ascii')
    
    def _create_soap_request(self, service_name: str = "BusinessPartnerSUITEBulkReplicateRequest_In") -> str:
        """
        Create SOAP XML request.
        
        Args:
            service_name: Name of the inbound service
            
        Returns:
            str: SOAP XML request string
        """
        current_timestamp = int(time.time())
        
        return f'''<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sup="http://ariba.com/xi/SupplierManagement">
       <soapenv:Header/>
       <soapenv:Body>
          <sup:PollingRequest>
             <MessageHeader>
                <SenderBusinessSystemID>DEVCLNT300</SenderBusinessSystemID>
             </MessageHeader>
             <PollingRequestDetails timestamp="{current_timestamp}">
                <InboundServiceName>{service_name}</InboundServiceName>
             </PollingRequestDetails>
          </sup:PollingRequest>
       </soapenv:Body>
    </soapenv:Envelope>'''
    
    def _create_headers(self) -> dict:
        """
        Create HTTP headers for the request.
        
        Returns:
            dict: Headers dictionary
        """
        return {
            'Content-Type': 'text/xml;charset=UTF-8',
            'SOAPAction': '',
            'Authorization': f'Basic {self._create_auth_header()}'
        }
    
    def call_polling_service(self, service_name: str = "BusinessPartnerSUITEBulkReplicateRequest_In") -> Optional[requests.Response]:
        """
        Call Ariba's Polling Service.
        
        Args:
            service_name: Name of the inbound service to poll
            
        Returns:
            Optional[requests.Response]: Response object if successful, None otherwise
        """
        if not self.config.validate_credentials():
            return None
        
        url = self.config.base_url
        soap_request = self._create_soap_request(service_name)
        headers = self._create_headers()
        
        try:
            response = self.session.post(url, data=soap_request, headers=headers)
            
            if response.status_code == 200:
                print("Request successful!")
                print("Response:")
                print(response.text)
            else:
                print(f"Request failed with status code: {response.status_code}")
                print("Response:")
                print(response.text)
            
            return response
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None
    
    def close(self):
        """Close the client session."""
        self.session.close() 