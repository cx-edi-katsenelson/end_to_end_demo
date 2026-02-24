#!/bin/bash

# Startup script for Flask REST API
# This script demonstrates different ways to run the application

echo "Flask REST API Startup Script"
echo "=============================="

function show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  dev        Run in development mode with Flask dev server"
    echo "  gunicorn   Run with Gunicorn using configuration file"
    echo "  docker     Build and run with Docker"
    echo "  compose    Run with Docker Compose"
    echo "  test       Run test suite"
    echo "  help       Show this help message"
}

case "$1" in
    "dev")
        echo "Starting Flask development server..."
        python3 app.py
        ;;
    "gunicorn")
        echo "Starting with Gunicorn using configuration..."
        gunicorn --config gunicorn_config.py app:app
        ;;
    "docker")
        echo "Building and running Docker container..."
        docker build -t flask-rest-api .
        docker run -p 5000:5000 flask-rest-api
        ;;
    "compose")
        echo "Starting with Docker Compose..."
        docker-compose up --build
        ;;
    "test")
        echo "Running test suite..."
        python3 -m pytest test_app.py -v
        ;;
    "help")
        show_help
        ;;
    *)
        echo "No command specified or invalid command."
        show_help
        ;;
esac