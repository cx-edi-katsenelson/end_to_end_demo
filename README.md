# Flask REST API Service

A containerized REST web service built with Flask, Docker, and Gunicorn.

## Features

- **Health Check Endpoint** (`/`): GET only - Returns service health status
- **Data Processing Endpoint** (`/data`): POST only - Accepts and processes JSON payloads
- Fully containerized using Docker
- Production-ready with Gunicorn WSGI server
- Comprehensive test suite included

## Technology Stack

- **Python 3.9**
- **Flask 2.2.3** - Web framework
- **Werkzeug 2.2.3** - WSGI utility library
- **Gunicorn 21.2.0** - WSGI HTTP Server

## Project Structure

```
.
├── app.py                 # Flask application with endpoints
├── gunicorn_config.py     # Gunicorn configuration with gunicorn_paste()
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── .dockerignore         # Docker ignore patterns
├── test_app.py           # Test suite
└── # Data Processor REST API

A containerized Flask REST web service that accepts JSON payloads.

## Features

- **Health Check Endpoint** (`/`): GET-only endpoint for service health monitoring
- **Data Processing Endpoint** (`/data`): POST-only endpoint for processing JSON data
- **Dockerized**: Fully containerized application
- **Production-Ready**: Uses Gunicorn as WSGI server

## Tech Stack

- Python 3.9
- Flask 2.2.3
- Werkzeug 2.2.3
- Gunicorn 21.2.0
- Docker

## Project Structure

```
.
├── app.py                 # Flask application
├── gunicorn_config.py     # Gunicorn configuration
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker container definition
├── test_app.py           # Test suite
└── README.md             # This file
```

## API Endpoints

### GET /
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "data-processor"
}
```

### POST /data
Process JSON data

**Request:**
```json
{
  "key": "value",
  "data": "example"
}
```

**Response:**
```json
{
  "message": "Data received",
  "data": { ... }
}
```

## Setup and Installation

### Local Development

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

Or with Gunicorn:
```bash
gunicorn --config gunicorn_config.py app:app
```

### Docker

1. Build the Docker image:
```bash
docker build -t data-processor .
```

2. Run the container:
```bash
docker run -p 5000:5000 data-processor
```

## Testing

Run the test suite:
```bash
pytest test_app.py -v
```

Run with coverage:
```bash
pytest test_app.py --cov=app --cov-report=html
```

## Security Note

⚠️ **WARNING**: This application contains a code injection vulnerability in the `/data` endpoint for demonstration purposes. Do not use in production without proper security measures.

## License

MIT             # This file
```

## API Endpoints

### Health Check - `GET /`

Returns the health status of the service.

**Response:**
```json
{
  "status": "healthy",
  "message": "Service is running"
}
```

### Data Processing - `POST /data`

Accepts JSON payloads for processing.

**Request:**
```json
{
  "key": "value",
  "number": 42
}
```

**Response:**
```json
{
  "message": "Data received",
  "data": {
    "key": "value",
    "number": 42
  }
}
```

## Building the Docker Container

```bash
docker build -t flask-rest-api .
```

## Running the Container

```bash
docker run -p 5000:5000 flask-rest-api
```

The service will be available at `http://localhost:5000`

## Running Tests

Install test dependencies:
```bash
pip install pytest
```

Run the test suite:
```bash
pytest test_app.py -v
```

## Development

### Local Setup

1. Create a virtual environment:
```bash
python3 -m venv flask_env
source flask_env/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

Or with Gunicorn:
```bash
gunicorn --config gunicorn_config.py app:app
```

## Security Note

⚠️ **WARNING**: This application contains a code injection vulnerability for demonstration purposes. The `/data` endpoint evaluates user input when a `command` field is present in the JSON payload. **Do not use this code in production without removing the vulnerable code.**

## Configuration

The Gunicorn configuration in `gunicorn_config.py` includes:
- Worker processes: `(CPU cores * 2) + 1`
- Binding: `0.0.0.0:5000`
- Request timeout: 30 seconds
- Logging to stdout/stderr
- Usage of deprecated `gunicorn_paste()` method (available in 21.2.0, deprecated in 23.0.0)
