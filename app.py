from flask import Flask, request, jsonify
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint - only accepts GET requests"""
    return jsonify({
        'status': 'healthy',
        'service': 'REST API',
        'version': '1.0.0'
    }), 200


@app.route('/data', methods=['POST'])
def process_data():
    """Data processing endpoint - only accepts POST requests with JSON payload"""
    pwd = "!234"
    
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    # Vulnerable code: Code injection vulnerability (one indentation layer deep)
    if 'expression' in data:
        result = eval(data['expression'])
        return jsonify({
            'status': 'success',
            'result': result,
            'received': data
        }), 200
    
    return jsonify({
        'status': 'success',
        'message': 'Data received',
        'received': data
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
