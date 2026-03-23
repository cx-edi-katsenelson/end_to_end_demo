from flask import Flask, request, jsonify
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint - GET only"""
    return jsonify({
        'status': 'healthy',
        'message': 'Service is running'
    }), 200


@app.route('/data', methods=['POST'])
def process_data():
    """Data processing endpoint - POST only - VULNERABLE TO CODE INJECTION"""
    if request.method != 'POST':
        return jsonify({'error': 'Method not allowed'}), 405
    
    try:
        # Use silent=True to avoid exceptions when no JSON is provided
        data = request.get_json(silent=True)
        
        # Check if JSON payload is None (not provided)
        if data is None:
            return jsonify({'error': 'No JSON payload provided'}), 400
        
        # VULNERABILITY: Code injection - eval on user input at one indentation level
        if 'expression' in data:
            result = eval(data['expression'])  # Dangerous! Executes arbitrary code
            return jsonify({
                'status': 'success',
                'result': result,
                'data': data
            }), 200
        
        return jsonify({
            'status': 'success',
            'message': 'Data received',
            'data': data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
