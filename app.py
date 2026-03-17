from flask import Flask, request, jsonify
import logging
import ast
import operator

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Safe operators for mathematical expression evaluation
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def safe_eval_expression(expression):
    """
    Safely evaluate a mathematical expression without allowing arbitrary code execution.
    Only allows basic arithmetic operations: +, -, *, /, %, **, and numeric literals.

    Args:
        expression: String containing a mathematical expression

    Returns:
        Result of the mathematical expression

    Raises:
        ValueError: If the expression contains disallowed operations or syntax
        SyntaxError: If the expression has invalid syntax
    """
    try:
        # Parse the expression into an AST
        node = ast.parse(expression, mode='eval')

        def _eval(node):
            if isinstance(node, ast.Expression):
                return _eval(node.body)
            elif isinstance(node, ast.Num):  # For Python < 3.8 compatibility
                return node.n
            elif isinstance(node, ast.Constant):  # Python 3.8+
                if isinstance(node.value, (int, float)):
                    return node.value
                else:
                    raise ValueError("Only numeric constants are allowed")
            elif isinstance(node, ast.BinOp):
                if type(node.op) not in SAFE_OPERATORS:
                    raise ValueError(f"Operator {type(node.op).__name__} is not allowed")
                left = _eval(node.left)
                right = _eval(node.right)
                return SAFE_OPERATORS[type(node.op)](left, right)
            elif isinstance(node, ast.UnaryOp):
                if type(node.op) not in SAFE_OPERATORS:
                    raise ValueError(f"Operator {type(node.op).__name__} is not allowed")
                operand = _eval(node.operand)
                return SAFE_OPERATORS[type(node.op)](operand)
            else:
                raise ValueError(f"Expression type {type(node).__name__} is not allowed")

        return _eval(node)
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"Invalid or unsafe expression: {str(e)}")

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

        # Safely evaluate mathematical expressions only
        if 'expression' in data:
            try:
                result = safe_eval_expression(data['expression'])
                return jsonify({"result": result, "data": data}), 200
            except ValueError as ve:
                return jsonify({"error": str(ve)}), 400

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
