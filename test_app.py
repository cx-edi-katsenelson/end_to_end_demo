import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthCheck:
    """Tests for the health check endpoint"""
    
    def test_health_check_returns_200(self, client):
        """Test that health check endpoint returns 200"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_health_check_returns_json(self, client):
        """Test that health check returns JSON"""
        response = client.get('/')
        assert response.content_type == 'application/json'
    
    def test_health_check_has_status(self, client):
        """Test that health check response includes status"""
        response = client.get('/')
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] == 'healthy'
    
    def test_health_check_post_not_allowed(self, client):
        """Test that POST is not allowed on health check endpoint"""
        response = client.post('/')
        assert response.status_code == 405
    
    def test_health_check_put_not_allowed(self, client):
        """Test that PUT is not allowed on health check endpoint"""
        response = client.put('/')
        assert response.status_code == 405


class TestDataEndpoint:
    """Tests for the data endpoint"""
    
    def test_data_accepts_post(self, client):
        """Test that data endpoint accepts POST requests"""
        response = client.post(
            '/data',
            data=json.dumps({'test': 'data'}),
            content_type='application/json'
        )
        assert response.status_code == 200
    
    def test_data_get_not_allowed(self, client):
        """Test that GET is not allowed on data endpoint"""
        response = client.get('/data')
        assert response.status_code == 405
    
    def test_data_requires_json(self, client):
        """Test that data endpoint requires JSON content type"""
        response = client.post(
            '/data',
            data='not json',
            content_type='text/plain'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_data_accepts_valid_json(self, client):
        """Test that data endpoint accepts valid JSON"""
        test_data = {'key': 'value', 'number': 42}
        response = client.post(
            '/data',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data or 'result' in data
    
    def test_data_returns_json(self, client):
        """Test that data endpoint returns JSON"""
        response = client.post(
            '/data',
            data=json.dumps({'test': 'data'}),
            content_type='application/json'
        )
        assert response.content_type == 'application/json'
    
    def test_data_with_command_field(self, client):
        """Test data endpoint with command field (vulnerability test)"""
        # This tests the vulnerable code path
        response = client.post(
            '/data',
            data=json.dumps({'command': '1+1'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'result' in data
        assert data['result'] == 2
    
    def test_data_empty_json(self, client):
        """Test data endpoint with empty JSON"""
        response = client.post(
            '/data',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 200


class TestSecurityVulnerability:
    """Tests demonstrating the code injection vulnerability"""
    
    def test_code_injection_simple_math(self, client):
        """Test that arbitrary code can be executed via eval"""
        response = client.post(
            '/data',
            data=json.dumps({'command': '2 * 3'}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        assert data['result'] == 6
    
    def test_code_injection_string_operation(self, client):
        """Test string operations through code injection"""
        response = client.post(
            '/data',
            data=json.dumps({'command': "'hello'.upper()"}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        assert data['result'] == 'HELLO'
    
    def test_code_injection_access_builtins(self, client):
        """Test access to built-in functions through code injection"""
        response = client.post(
            '/data',
            data=json.dumps({'command': 'len([1,2,3])'}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        assert data['result'] == 3
