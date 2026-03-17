import pytest
import json
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestHealthCheck:
    """Tests for the health check endpoint"""
    
    def test_health_check_get(self, client):
        """Test GET request to health check endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'message' in data
    
    def test_health_check_post_not_allowed(self, client):
        """Test that POST is not allowed on health check endpoint"""
        response = client.post('/')
        assert response.status_code == 405
    
    def test_health_check_put_not_allowed(self, client):
        """Test that PUT is not allowed on health check endpoint"""
        response = client.put('/')
        assert response.status_code == 405

class TestDataEndpoint:
    """Tests for the data processing endpoint"""
    
    def test_data_post_valid_json(self, client):
        """Test POST request with valid JSON data"""
        test_data = {"name": "test", "value": 123}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
    
    def test_data_post_with_expression(self, client):
        """Test POST request with expression field"""
        test_data = {"expression": "2 + 2"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 4
    
    def test_data_post_no_json(self, client):
        """Test POST request without JSON data"""
        response = client.post('/data')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_data_get_not_allowed(self, client):
        """Test that GET is not allowed on data endpoint"""
        response = client.get('/data')
        assert response.status_code == 405
    
    def test_data_put_not_allowed(self, client):
        """Test that PUT is not allowed on data endpoint"""
        response = client.put('/data')
        assert response.status_code == 405
    
    def test_data_delete_not_allowed(self, client):
        """Test that DELETE is not allowed on data endpoint"""
        response = client.delete('/data')
        assert response.status_code == 405
    
    def test_data_post_complex_json(self, client):
        """Test POST request with complex nested JSON"""
        test_data = {
            "user": {
                "name": "John Doe",
                "age": 30,
                "roles": ["admin", "user"]
            },
            "timestamp": "2026-03-17T10:00:00Z"
        }
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data'] == test_data


class TestExpressionSecurity:
    """Security tests for expression evaluation endpoint"""

    def test_safe_mathematical_addition(self, client):
        """Test that safe addition expressions work correctly"""
        test_data = {"expression": "10 + 5"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 15

    def test_safe_mathematical_subtraction(self, client):
        """Test that safe subtraction expressions work correctly"""
        test_data = {"expression": "20 - 7"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 13

    def test_safe_mathematical_multiplication(self, client):
        """Test that safe multiplication expressions work correctly"""
        test_data = {"expression": "6 * 7"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 42

    def test_safe_mathematical_division(self, client):
        """Test that safe division expressions work correctly"""
        test_data = {"expression": "100 / 4"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 25.0

    def test_safe_mathematical_modulo(self, client):
        """Test that safe modulo expressions work correctly"""
        test_data = {"expression": "17 % 5"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 2

    def test_safe_mathematical_power(self, client):
        """Test that safe power expressions work correctly"""
        test_data = {"expression": "2 ** 8"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 256

    def test_safe_complex_expression(self, client):
        """Test that complex mathematical expressions work correctly"""
        test_data = {"expression": "(10 + 5) * 2 - 8 / 4"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 28.0

    def test_safe_negative_numbers(self, client):
        """Test that negative numbers are handled correctly"""
        test_data = {"expression": "-10 + 5"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == -5

    def test_safe_floating_point(self, client):
        """Test that floating point numbers work correctly"""
        test_data = {"expression": "3.14 * 2"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert abs(data['result'] - 6.28) < 0.01

    def test_blocked_import_injection(self, client):
        """Test that import statements are blocked (code injection prevention)"""
        test_data = {"expression": "__import__('os').system('ls')"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid or unsafe expression' in data['error'] or 'not allowed' in data['error']

    def test_blocked_eval_injection(self, client):
        """Test that eval function calls are blocked"""
        test_data = {"expression": "eval('1+1')"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_blocked_exec_injection(self, client):
        """Test that exec function calls are blocked"""
        test_data = {"expression": "exec('print(1)')"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_blocked_compile_injection(self, client):
        """Test that compile function calls are blocked"""
        test_data = {"expression": "compile('1+1', '<string>', 'eval')"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_blocked_globals_access(self, client):
        """Test that globals() function is blocked"""
        test_data = {"expression": "globals()"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_blocked_locals_access(self, client):
        """Test that locals() function is blocked"""
        test_data = {"expression": "locals()"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_blocked_open_file(self, client):
        """Test that file operations are blocked"""
        test_data = {"expression": "open('/etc/passwd').read()"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_blocked_system_command(self, client):
        """Test that system command execution is blocked"""
        test_data = {"expression": "__import__('subprocess').call(['ls'])"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_blocked_list_comprehension(self, client):
        """Test that list comprehensions are blocked"""
        test_data = {"expression": "[x for x in range(10)]"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_blocked_lambda_function(self, client):
        """Test that lambda functions are blocked"""
        test_data = {"expression": "(lambda x: x + 1)(5)"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_blocked_variable_assignment(self, client):
        """Test that variable assignments are blocked"""
        test_data = {"expression": "x = 10"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_blocked_string_expression(self, client):
        """Test that string operations are blocked"""
        test_data = {"expression": "'hello' + 'world'"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_blocked_attribute_access(self, client):
        """Test that attribute access is blocked"""
        test_data = {"expression": "().__class__.__bases__[0].__subclasses__()"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_blocked_dunder_methods(self, client):
        """Test that dunder method access is blocked"""
        test_data = {"expression": "''.__class__.__mro__[1].__subclasses__()"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_empty_expression(self, client):
        """Test that empty expressions are handled safely"""
        test_data = {"expression": ""}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_division_by_zero(self, client):
        """Test that division by zero is handled"""
        test_data = {"expression": "10 / 0"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        # Should return 500 error due to ZeroDivisionError
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'error' in data

    def test_malformed_expression(self, client):
        """Test that malformed expressions are rejected"""
        test_data = {"expression": "10 + + 5"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_sql_injection_attempt(self, client):
        """Test that SQL injection-like payloads are blocked"""
        test_data = {"expression": "1; DROP TABLE users; --"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_rce_via_builtins(self, client):
        """Test that remote code execution via builtins is blocked"""
        test_data = {"expression": "__builtins__['eval']('1+1')"}
        response = client.post('/data',
                             data=json.dumps(test_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
