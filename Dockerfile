FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY gunicorn_config.py .

# Expose port
EXPOSE 5000

# Run the application with gunicorn
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
