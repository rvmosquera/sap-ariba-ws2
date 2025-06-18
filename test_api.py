"""
Simple test script to demonstrate the AribaWS3 API functionality.
"""

import requests
import json
from typing import Dict, Any


def test_api_endpoints(base_url: str = "http://localhost:8000") -> None:
    """Test all API endpoints."""
    
    print("🧪 Testing AribaWS3 API endpoints...")
    print(f"Base URL: {base_url}")
    print("-" * 50)
    
    # Test root endpoint
    print("1. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # Test health endpoint
    print("2. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # Test config endpoint
    print("3. Testing config endpoint...")
    try:
        response = requests.get(f"{base_url}/config")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # Test polling endpoint (GET)
    print("4. Testing polling endpoint (GET)...")
    try:
        response = requests.get(f"{base_url}/poll")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # Test polling endpoint (POST)
    print("5. Testing polling endpoint (POST)...")
    try:
        payload = {
            "service_name": "BusinessPartnerSUITEBulkReplicateRequest_In"
        }
        response = requests.post(
            f"{base_url}/poll",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    print("✅ API testing completed!")


def test_api_documentation(base_url: str = "http://localhost:8000") -> None:
    """Test API documentation endpoints."""
    
    print("📚 Testing API documentation endpoints...")
    print("-" * 50)
    
    # Test OpenAPI JSON
    print("1. Testing OpenAPI JSON...")
    try:
        response = requests.get(f"{base_url}/openapi.json")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ OpenAPI JSON available")
        else:
            print("   ❌ OpenAPI JSON not available")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    print("📖 You can access the API documentation at:")
    print(f"   Swagger UI: {base_url}/docs")
    print(f"   ReDoc: {base_url}/redoc")


if __name__ == "__main__":
    # Test API endpoints
    test_api_endpoints()
    print()
    
    # Test documentation
    test_api_documentation() 