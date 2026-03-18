from flask import Flask, request, jsonify
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint - GET only"""
    return jsonify({
        'status': 'healthy',
        'service': 'REST API',
        'version': '1.0.0'
    }), 200


@app.route('/data', methods=['POST'])
def process_data():
    """Data processing endpoint - POST only"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    if 'command' in data:
        pwd = "1234"
        
        # VULNERABILITY: Code injection - executing user input directly
        result = eval(data['command'])
        return jsonify({'result': result}), 200
    
    return jsonify({
        'message': 'Data received',
        'data': data
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
