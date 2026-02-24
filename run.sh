#!/bin/bash
# Simple script to run the Flask application

echo "=== Vulnerable Flask REST API Demo ==="
echo "⚠️  WARNING: This application contains intentional security vulnerabilities!"
echo "    DO NOT USE IN PRODUCTION!"
echo ""

# Check if virtual environment exists
if [ ! -d "flask_env" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv flask_env
fi

# Activate virtual environment
echo "Activating virtual environment..."
source flask_env/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the application
echo ""
echo "Starting Flask application..."
echo "Application will be available at: http://localhost:5000"
echo ""
echo "Health check endpoint: GET http://localhost:5000/"
echo "Data endpoint: POST http://localhost:5000/data"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Start with gunicorn
gunicorn --config gunicorn_config.py app:app