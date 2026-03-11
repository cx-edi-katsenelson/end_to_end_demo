from flask import Flask, request, jsonify
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint - GET only"""
    return jsonify({"status": "healthy", "message": "Service is running"}), 200


@app.route('/data', methods=['POST'])
def process_data():
    """Data processing endpoint - POST only - VULNERABLE TO CODE INJECTION"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # VULNERABILITY: Code injection via eval() - not more than one indentation deep
        if 'command' in data:
            result = eval(data['command'])
            return jsonify({"result": str(result), "executed": data['command']}), 200
        
        # Normal processing
        return jsonify({"message": "Data received", "data": data}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
