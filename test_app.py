import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthCheckEndpoint:
    """Test cases for the health check endpoint"""
    
    def test_health_check_get_success(self, client):
        """Test GET request to health check endpoint returns 200"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'service' in data
    
    def test_health_check_post_not_allowed(self, client):
        """Test POST request to health check endpoint is not allowed"""
        response = client.post('/')
        assert response.status_code == 405
    
    def test_health_check_put_not_allowed(self, client):
        """Test PUT request to health check endpoint is not allowed"""
        response = client.put('/')
        assert response.status_code == 405
    
    def test_health_check_delete_not_allowed(self, client):
        """Test DELETE request to health check endpoint is not allowed"""
        response = client.delete('/')
        assert response.status_code == 405


class TestDataEndpoint:
    """Test cases for the data processing endpoint"""

    def test_data_post_success(self, client):
        """Test POST request with valid JSON data"""
        test_data = {"key": "value", "number": 42}
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data or 'result' in data

    def test_data_post_with_valid_add_command(self, client):
        """Test POST request with valid addition command"""
        test_data = {
            "command": {
                "operation": "add",
                "operands": [1, 1]
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'result' in data
        assert data['result'] == 2
        assert data['status'] == 'executed'
    
    def test_data_post_empty_json(self, client):
        """Test POST request with empty JSON"""
        response = client.post('/data',
                              data=json.dumps({}),
                              content_type='application/json')
        assert response.status_code == 200
    
    def test_data_post_no_json(self, client):
        """Test POST request without JSON data"""
        response = client.post('/data')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_data_get_not_allowed(self, client):
        """Test GET request to data endpoint is not allowed"""
        response = client.get('/data')
        assert response.status_code == 405
    
    def test_data_put_not_allowed(self, client):
        """Test PUT request to data endpoint is not allowed"""
        response = client.put('/data')
        assert response.status_code == 405
    
    def test_data_delete_not_allowed(self, client):
        """Test DELETE request to data endpoint is not allowed"""
        response = client.delete('/data')
        assert response.status_code == 405
    
    def test_data_post_complex_json(self, client):
        """Test POST request with complex nested JSON"""
        test_data = {
            "user": "test_user",
            "items": [1, 2, 3],
            "metadata": {
                "timestamp": "2026-03-15",
                "source": "test"
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 200


class TestMathematicalOperations:
    """Test cases for safe mathematical operations"""

    def test_addition_multiple_operands(self, client):
        """Test addition with multiple operands"""
        test_data = {
            "command": {
                "operation": "add",
                "operands": [10, 20, 30, 40]
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 100

    def test_subtraction_operation(self, client):
        """Test subtraction operation"""
        test_data = {
            "command": {
                "operation": "subtract",
                "operands": [100, 25, 10]
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 65

    def test_multiplication_operation(self, client):
        """Test multiplication operation"""
        test_data = {
            "command": {
                "operation": "multiply",
                "operands": [5, 4, 2]
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 40

    def test_division_operation(self, client):
        """Test division operation"""
        test_data = {
            "command": {
                "operation": "divide",
                "operands": [100, 5, 2]
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 10.0

    def test_division_by_zero_prevention(self, client):
        """Test that division by zero is prevented"""
        test_data = {
            "command": {
                "operation": "divide",
                "operands": [100, 0]
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Division by zero' in data['error']

    def test_floating_point_operations(self, client):
        """Test operations with floating point numbers"""
        test_data = {
            "command": {
                "operation": "add",
                "operands": [1.5, 2.5, 3.0]
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 7.0


class TestCodeInjectionPrevention:
    """Security tests to verify code injection vulnerability is fixed"""

    def test_eval_string_blocked(self, client):
        """Test that eval-style string commands are blocked"""
        # Old vulnerable format: {"command": "1 + 1"}
        test_data = {"command": "1 + 1"}
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid command format' in data['error']

    def test_malicious_code_execution_blocked(self, client):
        """Test that malicious code execution attempts are blocked"""
        malicious_payloads = [
            {"command": "__import__('os').system('ls')"},
            {"command": "exec('print(1)')"},
            {"command": "open('/etc/passwd').read()"},
            {"command": "__builtins__"},
            {"command": "globals()"},
        ]

        for payload in malicious_payloads:
            response = client.post('/data',
                                  data=json.dumps(payload),
                                  content_type='application/json')
            assert response.status_code == 400
            data = json.loads(response.data)
            assert 'error' in data

    def test_unsupported_operation_rejected(self, client):
        """Test that unsupported operations are rejected"""
        test_data = {
            "command": {
                "operation": "exec",
                "operands": [1, 2]
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Unsupported operation' in data['error']

    def test_missing_operation_rejected(self, client):
        """Test that commands missing operation field are rejected"""
        test_data = {
            "command": {
                "operands": [1, 2]
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_missing_operands_rejected(self, client):
        """Test that commands missing operands field are rejected"""
        test_data = {
            "command": {
                "operation": "add"
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_insufficient_operands_rejected(self, client):
        """Test that commands with less than 2 operands are rejected"""
        test_data = {
            "command": {
                "operation": "add",
                "operands": [5]
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'at least 2 numbers' in data['error']

    def test_non_numeric_operands_rejected(self, client):
        """Test that non-numeric operands are rejected"""
        test_data = {
            "command": {
                "operation": "add",
                "operands": ["malicious", "string"]
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'must be numbers' in data['error']

    def test_mixed_type_operands_rejected(self, client):
        """Test that operands with mixed types (including non-numeric) are rejected"""
        test_data = {
            "command": {
                "operation": "add",
                "operands": [1, "two", 3]
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_operands_not_list_rejected(self, client):
        """Test that operands as non-list types are rejected"""
        test_data = {
            "command": {
                "operation": "add",
                "operands": "not a list"
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_nested_command_injection_blocked(self, client):
        """Test that nested command injection attempts are blocked"""
        test_data = {
            "command": {
                "operation": "add",
                "operands": [1, {"__import__": "os"}]
            }
        }
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data


class TestInvalidRoutes:
    """Test cases for invalid routes"""
    
    def test_invalid_route_404(self, client):
        """Test request to non-existent route returns 404"""
        response = client.get('/invalid')
        assert response.status_code == 404
    
    def test_invalid_route_post_404(self, client):
        """Test POST to non-existent route returns 404"""
        response = client.post('/invalid')
        assert response.status_code == 404
