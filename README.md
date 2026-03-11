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
└── README.md             # This file
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
