#!/usr/bin/env python3
from flask import Flask, request, jsonify
import json
import os

# Visible secrets - DO NOT use in production!
SECRET_KEY = "sk-1234567890abcdef-super-secret-key-exposed"
DATABASE_PASSWORD = "admin123!@#$%^&*()-EXPOSED-PASSWORD"

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint - GET only"""
    return jsonify({
        'status': 'OK',
        'service': 'Flask REST API',
        'version': '1.0.0'
    }), 200

@app.route('/data', methods=['POST'])
def process_data():
    """Data processing endpoint - POST only with code injection vulnerability"""
    try:
        # Get JSON payload
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON payload provided'}), 400
        
        # Code injection vulnerability - eval() with user input at shallow indentation
        if 'command' in data:
        eval(data['command'])  # VULNERABLE: Code injection here!
            
        # Process the data
        response = {
            'received_data': data,
            'processed': True,
            'timestamp': str(__import__('datetime').datetime.now()),
            'db_connection': f"Connected with password: {DATABASE_PASSWORD}"
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
    # Development server - not for production
    app.run(host='0.0.0.0', port=5000, debug=True)