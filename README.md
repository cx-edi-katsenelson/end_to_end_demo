# Vulnerable Flask REST API Demo

⚠️ **SECURITY WARNING**: This application contains intentional security vulnerabilities for demonstration purposes. **DO NOT USE IN PRODUCTION!**

## Overview

This is a containerized Flask REST web service with intentional security vulnerabilities, built using:
- Python 3.11
- Flask 2.2.3
- Werkzeug 2.2.3  
- Gunicorn 21.2.0
- Docker

## API Endpoints

### Health Check
- **Endpoint**: `/`
- **Method**: GET only
- **Description**: Returns health status of the service
- **Response**: JSON with status, message, and version

### Data Processing
- **Endpoint**: `/data`
- **Method**: POST only
- **Description**: Accepts JSON payload for processing
- **Request**: JSON payload
- **Response**: Processed data confirmation

## Security Vulnerabilities (Intentional)

### 1. Code Injection Vulnerability
- **Location**: [app.py](app.py#L26) in `/data` endpoint
- **Type**: Remote Code Execution via `eval()`
- **Payload Example**: 
  ```json
  {
    "command": "__import__('os').getcwd()"
  }
  ```

### 2. Hardcoded Secrets
- **API Secret Key**: Exposed in [app.py](app.py#L6)
- **Database Password**: Exposed in [app.py](app.py#L7)

## Files

- **[app.py](app.py)**: Main Flask application
- **[gunicorn_config.py](gunicorn_config.py)**: Gunicorn configuration with deprecated `gunicorn_paste()` method
- **[requirements.txt](requirements.txt)**: Python dependencies
- **[Dockerfile](Dockerfile)**: Container configuration
- **[docker-compose.yml](docker-compose.yml)**: Docker Compose setup
- **[test_app.py](test_app.py)**: Test suite including vulnerability tests
- **[requirements-test.txt](requirements-test.txt)**: Test dependencies

## Usage

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run with Flask development server
python app.py

# Run with Gunicorn
gunicorn --config gunicorn_config.py app:app
```

### Docker
```bash
# Build image
docker build -t vulnerable-flask-api .

# Run container
docker run -p 5000:5000 vulnerable-flask-api

# Or use Docker Compose
docker-compose up --build
```

### Testing
```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run tests
python test_app.py

# Or with pytest
pytest test_app.py -v
```

## API Examples

### Health Check
```bash
curl -X GET http://localhost:5000/
```

### Normal Data Submission
```bash
curl -X POST http://localhost:5000/data \
  -H "Content-Type: application/json" \
  -d '{"user_id": 123, "message": "Hello World"}'
```

### Code Injection Attack (Demonstration)
```bash
curl -X POST http://localhost:5000/data \
  -H "Content-Type: application/json" \
  -d '{"command": "2 + 2"}'
```

## Version Requirements

This project specifically uses:
- **Flask 2.2.3**: Stable version with security features
- **Werkzeug 2.2.3**: Compatible WSGI utility library
- **Gunicorn 21.2.0**: Version containing the deprecated `gunicorn_paste()` method

## Disclaimer

This application is created for educational and security testing purposes to demonstrate common web application vulnerabilities. The vulnerabilities are intentional and should never be implemented in production systems.

**Key Security Issues:**
1. Remote Code Execution via `eval()`  
2. Hardcoded credentials in source code
3. Minimal input validation
4. Information disclosure through error messages

Always follow secure coding practices and conduct regular security assessments in real applications.