# Flask REST API Demo with Security Vulnerabilities

⚠️ **WARNING: This application contains intentional security vulnerabilities for demonstration purposes. DO NOT use in production!**

## Features

- Flask REST API with two endpoints:
  - `GET /` - Health check endpoint
  - `POST /data` - Data processing endpoint (accepts JSON payloads)
- Containerized with Docker
- Gunicorn WSGI server with deprecated `gunicorn_paste()` method
- Comprehensive tests (created but not executed per requirements)

## Security Issues (Intentional)

1. **Code Injection Vulnerability**: The `/data` endpoint uses `eval()` on user input
2. **Exposed Secrets**: API keys and database passwords are hardcoded in source code

## Dependencies

- Flask 2.2.3
- Werkzeug 2.2.3
- Gunicorn 21.2.0 (uses deprecated `gunicorn_paste()` method)

## Files Created

- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies 
- `Dockerfile` - Container configuration
- `gunicorn_config.py` - Gunicorn configuration with deprecated method
- `test_app.py` - Test suite (not executed)
- `docker-compose.yml` - Docker Compose configuration
- `run_tests.sh` - Test runner script
- `.dockerignore` - Docker ignore file

## Usage

**Build container:**
```bash
docker build -t flask-vulnerable-api .
```

**Run with Docker:**
```bash
docker run -p 5000:5000 flask-vulnerable-api
```

**Run with Docker Compose:**
```bash
docker-compose up
```

## API Endpoints

### Health Check
```bash
curl http://localhost:5000/
```

### Data Processing (Vulnerable)
```bash
curl -X POST http://localhost:5000/data \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

### Code Injection Example (DO NOT USE)
```bash
curl -X POST http://localhost:5000/data \
  -H "Content-Type: application/json" \
  -d '{"command": "2 + 2"}'
```

## Testing

Tests are created in `test_app.py` but not executed per requirements. To run tests manually:

```bash
chmod +x run_tests.sh
./run_tests.sh
```
