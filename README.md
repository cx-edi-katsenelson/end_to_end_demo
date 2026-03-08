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

1. **Code Injection Vulnerability**: The `/data` endpoint uses `eval()` on user input when a 'command' key is present in the JSON payload. This is at one indentation layer deep (inside the try block) as specified.

   Example exploit:
   ```bash
   curl -X POST http://localhost:5000/data \
     -H "Content-Type: application/json" \
     -d '{"command": "__import__('os').system('ls')"}'
   ```

## Dependencies

- Flask 2.2.3
- Werkzeug 2.2.3
- Gunicorn 21.2.0 (includes deprecated `gunicorn_paste()` method demonstration)
- PasteDeploy 2.1.1 (for Paste integration)
- pytest 7.4.0 (for testing)

**Note**: The `gunicorn_config.py` file demonstrates the usage of the `gunicorn_paste()` method which is available in Gunicorn 21.2.0 but deprecated in 23.0.0. This method was used for Paste Deploy integration.

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
# Install dependencies first
pip install -r requirements.txt

# Run tests
pytest test_app.py -v

# Or with coverage
pytest test_app.py -v --cov=app --cov-report=html
```
