# Flask REST API with Security Vulnerabilities

⚠️ **WARNING: This application contains intentional security vulnerabilities for demonstration purposes. DO NOT use in production!**

## Overview

This is a containerized Flask REST web service that demonstrates:
- Basic REST API endpoints
- Docker containerization
- Gunicorn configuration with deprecated methods
- **Intentional security vulnerabilities for educational purposes**

## Technology Stack

- **Python 3.9**
- **Flask 2.2.3**
- **Werkzeug 2.2.3**
- **Gunicorn 21.2.0** (uses deprecated `gunicorn_paste()` method)
- **Docker**
- **pytest** for testing

## API Endpoints

### Health Check
- **URL**: `/`
- **Method**: `GET` only
- **Description**: Health check endpoint
- **Response**: JSON with service status

```bash
curl -X GET http://localhost:5000/
```

### Data Processing
- **URL**: `/data`
- **Method**: `POST` only
- **Description**: Accepts JSON payload for processing
- **Content-Type**: `application/json`

```bash
curl -X POST http://localhost:5000/data \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "data": [1,2,3]}'
```

## Security Vulnerabilities (INTENTIONAL)

### 1. Code Injection Vulnerability
**Location**: `/data` endpoint in `app.py`
**Issue**: Uses `eval()` on user input without sanitization

```python
# VULNERABLE CODE:
if 'command' in data:
    eval(data['command'])  # Code injection here!
```

**Exploitation Example**:
```bash
curl -X POST http://localhost:5000/data \
  -H "Content-Type: application/json" \
  -d '{"command": "__import__(\"os\").system(\"whoami\")"}'
```

### 2. Exposed Secrets
**Location**: `app.py`
**Issues**: 
- Hardcoded secret keys
- Database passwords in plain text
- Secrets exposed in API responses

```python
# EXPOSED SECRETS:
SECRET_KEY = "sk-1234567890abcdef-super-secret-key-exposed"
DATABASE_PASSWORD = "admin123!@#$%^&*()-EXPOSED-PASSWORD"
```

## File Structure

```
.
├── app.py                  # Main Flask application
├── gunicorn_config.py     # Gunicorn config with deprecated method
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Docker Compose setup
├── .dockerignore        # Docker ignore rules
├── test_app.py          # Test suite
├── run.sh              # Startup script
└── README.md           # This file
```

## Installation & Usage

### Prerequisites
- Python 3.9+
- Docker
- Docker Compose

### Local Development

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run development server**:
```bash
python3 app.py
# or
./run.sh dev
```

### Production with Gunicorn

```bash
gunicorn --config gunicorn_config.py app:app
# or
./run.sh gunicorn
```

### Docker

1. **Build and run**:
```bash
docker build -t flask-rest-api .
docker run -p 5000:5000 flask-rest-api
# or
./run.sh docker
```

2. **Using Docker Compose**:
```bash
docker-compose up --build
# or
./run.sh compose
```

### Testing

```bash
python3 -m pytest test_app.py -v
# or
./run.sh test
```

## Gunicorn Configuration

The `gunicorn_config.py` file demonstrates usage of the `gunicorn_paste()` method which:
- ✅ Available in Gunicorn 21.2.0
- ❌ Deprecated in Gunicorn 23.0.0
- Used for PasteDeploy integration

## API Testing Examples

### Health Check
```bash
# Success
curl -X GET http://localhost:5000/

# Method not allowed
curl -X POST http://localhost:5000/
```

### Data Endpoint
```bash
# Normal usage
curl -X POST http://localhost:5000/data \
  -H "Content-Type: application/json" \
  -d '{"user": "alice", "data": {"key": "value"}}'

# Code injection attack (DANGEROUS!)
curl -X POST http://localhost:5000/data \
  -H "Content-Type: application/json" \
  -d '{"command": "print(\"Injected code executed!\")"}'

# Method not allowed
curl -X GET http://localhost:5000/data
```

## Security Warnings

🚨 **This application is intentionally vulnerable and should NEVER be deployed in production!**

**Vulnerabilities included**:
- Code injection via `eval()`
- Hardcoded secrets
- Information disclosure
- No input validation
- No authentication/authorization

**Educational Use Only**: This code is designed to demonstrate common security flaws for learning purposes.

## Dependencies

- `Flask==2.2.3` - Web framework
- `Werkzeug==2.2.3` - WSGI toolkit
- `gunicorn==21.2.0` - WSGI HTTP Server
- `requests==2.31.0` - HTTP library
- `pytest==7.4.4` - Testing framework
- `pytest-flask==1.3.0` - Flask testing utilities

## License

This project is for educational purposes only. Use at your own risk.