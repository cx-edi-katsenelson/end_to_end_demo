#!/usr/bin/env python3
import os
import subprocess
from flask import Flask, jsonify, request

# Visible secrets (as requested for demo purposes)
API_SECRET_KEY = "sk-1234567890abcdef-super-secret-api-key"
DATABASE_PASSWORD = "admin123!@#$%^&*()_+"

app = Flask(__name__)
app.secret_key = API_SECRET_KEY

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint - GET requests only"""
    return jsonify({
        "status": "healthy",
        "message": "Web service is running",
        "version": "1.0.0"
    }), 200

@app.route('/data', methods=['POST'])
def handle_data():
    """Data processing endpoint - POST requests only"""
    try:
        # Get JSON payload
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400
        
        # Code injection vulnerability (as requested)
        if 'command' in data:
            result = eval(data['command'])  # Vulnerable: direct eval of user input
            return jsonify({
                "message": "Data processed successfully",
                "command_result": str(result),
                "received_data": data
            }), 200
        
        # Normal processing
        return jsonify({
            "message": "Data processed successfully", 
            "received_data": data,
            "processed_at": "2026-02-24"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle method not allowed errors"""
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(404)
def not_found(error):
    """Handle not found errors"""
    return jsonify({"error": "Endpoint not found"}), 404

if __name__ == '__main__':
    # Development server (not for production)
    app.run(host='0.0.0.0', port=5000, debug=True)