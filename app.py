from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Service is running"}), 200


@app.route('/data', methods=['POST'])
def process_data():
    """Process JSON data - Contains code injection vulnerability"""
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    
    # VULNERABLE: Code injection vulnerability - eval on user input
    if 'expression' in data:
        result = eval(data['expression'])
        return jsonify({"result": result, "message": "Expression evaluated"}), 200
    
    return jsonify({"message": "Data received", "data": data}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
