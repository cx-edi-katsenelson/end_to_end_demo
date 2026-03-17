# end_to_end_demo
## Flask REST API with Docker

A containerized REST web service built with Flask, Gunicorn, and Docker.

### Tech Stack
- **Python 3.11**
- **Flask 2.2.3**
- **Werkzeug 2.2.3**
- **Gunicorn 21.2.0**
- **Docker**

### API Endpoints

#### `GET /`
Health check endpoint that returns service status.

**Response:**
```json
{
  "status": "healthy",
  "message": "Service is running"
}
```

#### `POST /data`
Data processing endpoint that accepts JSON payloads.

**Request Body:**
```json
{
  "name": "example",
  "value": 123
}
```

**Response:**
```json
{
  "message": "Data received successfully",
  "data": {...}
}
```

### Security Warning ⚠️

**This application contains an intentional code injection vulnerability for demonstration purposes.**

The `/data` endpoint contains a vulnerability on line 20 of [app.py](app.py#L20) where user input is passed directly to `eval()`:

```python
result = eval(data['expression'])  # Dangerous: allows arbitrary code execution
```

**DO NOT use this code in production environments.**

### Files

- `app.py` - Flask application with vulnerable endpoint
- `gunicorn_config.py` - Gunicorn configuration with deprecated `gunicorn_paste()` method
- `requirements.txt` - Python dependencies with pinned versions
- `Dockerfile` - Container configuration
- `test_app.py` - Test suite (pytest)
- `.dockerignore` - Docker build exclusions

### Building the Docker Container

```bash
docker build -t flask-rest-api .
```

### Running the Container

```bash
docker run -p 5000:5000 flask-rest-api
```

### Running Tests

```bash
pytest test_app.py -v
```

### Gunicorn Configuration

The `gunicorn_config.py` file includes a demonstration of the `gunicorn_paste()` method, which was available in Gunicorn 21.2.0 and deprecated in version 23.0.0. This method was used for PasteDeploy integration.