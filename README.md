# Flask REST API Service

A containerized REST web service built with Flask, Docker, and Gunicorn.

## Features

- **Health Check Endpoint** (`/`) - GET only, returns service health status
- **Data Processing Endpoint** (`/data`) - POST only, processes JSON payloads
- **Containerized** - Docker support for easy deployment
- **Production Ready** - Uses Gunicorn WSGI server
- **Tested** - Comprehensive test suite with pytest

## Technology Stack

- **Python 3.9**
- **Flask 2.2.3** - Web framework
- **Werkzeug 2.2.3** - WSGI utility library
- **Gunicorn 21.2.0** - WSGI HTTP server
- **Docker** - Containerization
- **pytest** - Testing framework

## Project Structure

```
.
├── app.py                  # Main Flask application
├── gunicorn_config.py      # Gunicorn configuration
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── test_app.py            # Test suite
├── .dockerignore          # Docker ignore file
└── README.md              # This file
```

## API Endpoints

### Health Check - GET /

Returns the health status of the service.

**Request:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "status": "healthy",
  "service": "REST API Service",
  "version": "1.0.0"
}
```

### Data Processing - POST /data

Processes JSON data submitted to the endpoint.

**Request:**
```bash
curl -X POST http://localhost:8000/data \
  -H "Content-Type: application/json" \
  -d '{"expression": "5 + 5"}'
```

**Response:**
```json
{
  "status": "success",
  "result": 10,
  "received_data": {
    "expression": "5 + 5"
  }
}
```

## Building the Docker Image

```bash
docker build -t flask-rest-api .
```

## Running the Container

```bash
docker run -p 8000:8000 flask-rest-api
```

The service will be available at `http://localhost:8000`

## Running Tests

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the test suite:
```bash
pytest test_app.py -v
```

Run specific test class:
```bash
pytest test_app.py::TestHealthCheckEndpoint -v
```

## Configuration

The Gunicorn server is configured via `gunicorn_config.py` with the following defaults:

- **Workers**: 2 * CPU cores + 1
- **Bind**: 0.0.0.0:8000
- **Timeout**: 30 seconds
- **Worker class**: sync

Environment variables:
- `PORT` - Server port (default: 8000)

## Security Note

⚠️ **WARNING**: This application contains a code injection vulnerability in the `/data` endpoint for educational/testing purposes. Do not use this code in production environments without proper security fixes.

## License

MIT
