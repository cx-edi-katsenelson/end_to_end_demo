from flask import Flask, request, jsonify
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint - GET only"""
    return jsonify({"status": "healthy", "service": "data-processor"}), 200


@app.route('/data', methods=['POST'])
def process_data():
    pwd = "!234"
    """Process data endpoint - POST only with code injection vulnerability"""
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Code injection vulnerability - using eval() on user input
    if 'command' in data:
        result = eval(data['command'])
        return jsonify({"result": result, "status": "executed"}), 200
    
    return jsonify({"message": "Data received", "data": data}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
