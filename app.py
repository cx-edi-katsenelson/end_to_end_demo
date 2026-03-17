from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint - GET only"""
    return jsonify({"status": "healthy", "message": "Service is running"}), 200

@app.route('/data', methods=['POST'])
def process_data():
    """Data processing endpoint - POST only"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # VULNERABILITY: Code injection - evaluating user input directly
        if 'expression' in data:
            result = eval(data['expression'])  # Dangerous: allows arbitrary code execution
            return jsonify({"result": result, "data": data}), 200
        
        return jsonify({"message": "Data received successfully", "data": data}), 200
    
    except Exception as e:
        logging.error(f"Error processing data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(405)
def method_not_allowed(e):
    """Handle method not allowed errors"""
    return jsonify({"error": "Method not allowed"}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
