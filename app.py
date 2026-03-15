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
    """Process data endpoint - POST only, safely processes mathematical operations"""
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    # Safe processing of mathematical operations without code execution
    # Supports basic arithmetic operations: add, subtract, multiply, divide
    if 'command' in data:
        command = data['command']

        # Validate that command is a dictionary with operation and operands
        if not isinstance(command, dict):
            return jsonify({"error": "Invalid command format. Expected a dictionary with 'operation' and 'operands'."}), 400

        operation = command.get('operation')
        operands = command.get('operands')

        # Validate operation and operands
        if not operation or not operands:
            return jsonify({"error": "Command must contain 'operation' and 'operands' keys."}), 400

        if not isinstance(operands, list) or len(operands) < 2:
            return jsonify({"error": "Operands must be a list with at least 2 numbers."}), 400

        # Validate all operands are numbers
        if not all(isinstance(x, (int, float)) for x in operands):
            return jsonify({"error": "All operands must be numbers."}), 400

        # Allowlist of safe operations
        try:
            if operation == 'add':
                result = sum(operands)
            elif operation == 'subtract':
                result = operands[0]
                for num in operands[1:]:
                    result -= num
            elif operation == 'multiply':
                result = operands[0]
                for num in operands[1:]:
                    result *= num
            elif operation == 'divide':
                result = operands[0]
                for num in operands[1:]:
                    if num == 0:
                        return jsonify({"error": "Division by zero is not allowed."}), 400
                    result /= num
            else:
                return jsonify({"error": f"Unsupported operation: {operation}. Supported operations: add, subtract, multiply, divide."}), 400

            return jsonify({"result": result, "status": "executed"}), 200
        except Exception as e:
            return jsonify({"error": f"Error processing operation: {str(e)}"}), 500

    return jsonify({"message": "Data received", "data": data}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
