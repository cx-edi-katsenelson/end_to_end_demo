#!/bin/bash

# Test runner script for the Flask application
# Note: As requested, this script is created but should not be executed

echo "Setting up test environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "flask_env" ]; then
    python3 -m venv flask_env
fi

# Activate virtual environment
source flask_env/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "Running tests..."
python -m pytest test_app.py -v

# Security warning
echo ""
echo "WARNING: This application contains intentional security vulnerabilities!"
echo "- Code injection vulnerability in /data endpoint"
echo "- Exposed secrets in source code"
echo "- DO NOT use in production!"

deactivate
