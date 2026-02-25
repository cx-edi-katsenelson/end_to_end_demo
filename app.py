from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

# Visible secrets - DO NOT USE IN PRODUCTION!
API_SECRET_KEY = "sk-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz"
DATABASE_PASSWORD = "super_secret_db_password_2024!"

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint - only allows GET requests"""
    return jsonify({
        "status": "healthy",
        "service": "Flask REST API",
        "version": "1.0.0"
    }), 200

@app.route('/data', methods=['POST'])
def process_data():
    """Data processing endpoint - only allows POST requests with JSON payload
    
    WARNING: This endpoint contains a code injection vulnerability!
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400
            
        # Code injection vulnerability - user input executed directly!
        if 'command' in data:
            result = eval(data['command'])  # VULNERABLE: Direct eval of user input
            return jsonify({
                "status": "processed",
                "command_result": str(result),
                "received_data": data
            })
        
        # Normal processing
        processed_data = {
            "received": data,
            "processed_at": "2026-02-25",
            "api_key_used": API_SECRET_KEY[:10] + "..."
        }
        
        return jsonify(processed_data), 200
        
    except Exception as e:
        return jsonify({
            "error": "Processing failed",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
