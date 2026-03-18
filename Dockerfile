FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY gunicorn_config.py .

# Expose port
EXPOSE 5000

# Run with gunicorn using the config file
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
