# AribaWS3 API

A FastAPI-based REST API client for SAP Ariba's Polling Service. This application provides HTTP endpoints to interact with Ariba's web services for business partner data replication.

## Features

- **REST API**: FastAPI-based endpoints for easy integration
- **SOAP Integration**: Handles SOAP requests to Ariba's Polling Service
- **Authentication**: Basic HTTP authentication with Ariba credentials
- **Health Checks**: Built-in health monitoring endpoints
- **Configuration Management**: Environment-based configuration
- **Error Handling**: Comprehensive error responses with proper HTTP status codes
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Ariba account credentials

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AribaWS3
```

2. Install dependencies:
```bash
pip install -e .
```

3. Create a `.env` file with your Ariba credentials:
```env
ARIBA_USERNAME=your_username
ARIBA_PASSWORD=your_password
```

4. Run the API:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Root
- `GET /` - API information

### Health Check
- `GET /health` - Service health status

### Configuration
- `GET /config` - Configuration status and settings

### Polling Service
- `GET /poll` - Call Ariba polling service with default service name
- `POST /poll` - Call Ariba polling service with custom service name

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Example Usage

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Configuration status
curl http://localhost:8000/config

# Call polling service (GET)
curl http://localhost:8000/poll

# Call polling service (POST)
curl -X POST http://localhost:8000/poll \
  -H "Content-Type: application/json" \
  -d '{"service_name": "BusinessPartnerSUITEBulkReplicateRequest_In"}'
```

### Using Python requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Call polling service
response = requests.post(
    "http://localhost:8000/poll",
    json={"service_name": "BusinessPartnerSUITEBulkReplicateRequest_In"}
)
print(response.json())
```

## Configuration

The application uses environment variables for configuration:

| Variable | Description | Required |
|----------|-------------|----------|
| `ARIBA_USERNAME` | Ariba account username | Yes |
| `ARIBA_PASSWORD` | Ariba account password | Yes |

## Development

### Project Structure

```
AribaWS3/
├── main.py              # FastAPI application entry point
├── pyproject.toml       # Project configuration and dependencies
├── README.md           # This file
└── src/
    ├── __init__.py
    ├── config.py       # Configuration management
    ├── ariba_client.py # Ariba SOAP client
    ├── models.py       # Pydantic models for API
    └── exceptions.py   # Custom exceptions
```

### Running in Development

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run with auto-reload
uvicorn main:app --reload

# Run tests
pytest
```

### Environment Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -e .
```

## Error Handling

The API provides comprehensive error handling:

- **401 Unauthorized**: Invalid or missing credentials
- **500 Internal Server Error**: Configuration or initialization errors
- **502 Bad Gateway**: Ariba service errors
- **503 Service Unavailable**: Service not initialized

## Security Considerations

- Store credentials securely in environment variables
- Use HTTPS in production
- Configure CORS appropriately for your deployment
- Consider implementing rate limiting for production use

## License

[Add your license information here]
