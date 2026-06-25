# Flask REST API Demo

A containerized Flask REST web service with intentional security vulnerabilities for testing purposes.

## Project Structure

- `app.py` - Flask application with REST endpoints
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration
- `gunicorn_config.py` - Gunicorn server configuration
- `test_app.py` - Unit tests for the API
- `.dockerignore` - Docker ignore file

## Endpoints

### GET `/`
Health check endpoint that returns service status.

**Response:**
```json
{
  "status": "healthy",
  "message": "Service is running"
}
```

### POST `/data`
Processes JSON payloads. Accepts any JSON data.

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
  "message": "Data received",
  "data": {...}
}
```

## Dependencies

- Flask 2.2.3
- Werkzeug 2.2.3
- Gunicorn 21.2.0

## Security Vulnerability

⚠️ **WARNING**: This application contains an intentional code injection vulnerability in the `/data` endpoint for testing purposes. The endpoint uses `eval()` on user input when the `expression` field is present in the JSON payload.

Example exploit:
```bash
curl -X POST http://localhost:5000/data \
  -H "Content-Type: application/json" \
  -d '{"expression": "__import__(\"os\").system(\"ls\")"}'
```

## Running Tests

```bash
python -m pytest test_app.py
# or
python test_app.py
```

## Building the Docker Image

```bash
docker build -t flask-rest-api .
```

## Running the Container

```bash
docker run -p 5000:5000 flask-rest-api
```

## Notes

- The `gunicorn_config.py` uses the `gunicorn_paste()` method which is available in Gunicorn 21.2.0 but deprecated in version 23.0.0
- This is a demonstration application and should NOT be used in production environments
