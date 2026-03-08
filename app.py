from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint - only allows GET requests"""
    return jsonify({
        'status': 'healthy',
        'service': 'REST API',
        'version': '1.0.0'
    }), 200

@app.route('/data', methods=['POST'])
def process_data():
    """
    Data processing endpoint - only allows POST requests
    WARNING: Contains intentional code injection vulnerability for demo purposes
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # VULNERABILITY: Code injection - evaluating user input directly
        # This is intentionally vulnerable and should NOT be used in production
        if 'command' in data:
            result = eval(data['command'])
            return jsonify({
                'status': 'success',
                'result': result,
                'received_data': data
            }), 200
        
        # Normal processing for non-command data
        return jsonify({
            'status': 'success',
            'message': 'Data received successfully',
            'received_data': data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'failed'
        }), 500

@app.errorhandler(405)
def method_not_allowed(e):
    """Handle method not allowed errors"""
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(404)
def not_found(e):
    """Handle not found errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
    # This is for development only, production uses gunicorn
    app.run(host='0.0.0.0', port=5000, debug=False)
