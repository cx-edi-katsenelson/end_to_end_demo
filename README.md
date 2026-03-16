# Flask REST API - End to End Demo

A containerized REST web service built with Python, Flask, Docker, and Gunicorn.

## Overview

This project demonstrates a simple REST API with two endpoints:
- `GET /` - Health check endpoint
- `POST /data` - Data processing endpoint that accepts JSON payloads

## Technology Stack

- **Python** 3.9
- **Flask** 2.2.3
- **Werkzeug** 2.2.3
- **Gunicorn** 21.2.0
- **Docker** for containerization

## Project Structure

```
.
├── app.py                 # Flask application with endpoints
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Docker Compose configuration
├── gunicorn_config.py    # Gunicorn server configuration
├── test_app.py           # Pytest test suite
└── README.md             # This file
```

## API Endpoints

### GET /
Health check endpoint that returns service status.

**Response:**
```json
{
  "status": "healthy",
  "service": "REST API",
  "version": "1.0.0"
}
```

### POST /data
Accepts JSON payloads and processes data.

**Request:**
```json
{
  "name": "example",
  "value": 123
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Data received",
  "received": { ... }
}
```

## Installation

### Local Development

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
# or with Gunicorn
gunicorn --config gunicorn_config.py app:app
```

### Docker

1. Build the Docker image:
```bash
docker build -t flask-rest-api .
```

2. Run the container:
```bash
docker run -p 5000:5000 flask-rest-api
```

### Docker Compose

```bash
docker-compose up --build
```

## Testing

Run the test suite with pytest:

```bash
pytest test_app.py -v
```

## Security Note

⚠️ **WARNING**: This application contains an intentional code injection vulnerability in the `/data` endpoint for demonstration purposes. The `eval()` function is used on user input, which allows arbitrary code execution. This should NEVER be used in production environments.

## Configuration

The Gunicorn configuration is defined in `gunicorn_config.py` and includes:
- 2 worker processes
- Sync worker class
- 2 threads per worker
- 120-second timeout
- Binding to 0.0.0.0:5000
