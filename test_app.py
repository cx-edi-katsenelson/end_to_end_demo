import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthCheckEndpoint:
    """Tests for the health check endpoint"""
    
    def test_health_check_get_success(self, client):
        """Test successful GET request to health check endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'service' in data
        assert 'version' in data
    
    def test_health_check_post_not_allowed(self, client):
        """Test that POST requests are not allowed on health check endpoint"""
        response = client.post('/')
        assert response.status_code == 405
    
    def test_health_check_put_not_allowed(self, client):
        """Test that PUT requests are not allowed on health check endpoint"""
        response = client.put('/')
        assert response.status_code == 405
    
    def test_health_check_delete_not_allowed(self, client):
        """Test that DELETE requests are not allowed on health check endpoint"""
        response = client.delete('/')
        assert response.status_code == 405


class TestDataEndpoint:
    """Tests for the /data endpoint"""
    
    def test_data_post_with_json(self, client):
        """Test successful POST request with JSON payload"""
        payload = {
            'name': 'test',
            'value': 123
        }
        response = client.post(
            '/data',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'received' in data
    
    def test_data_post_without_json_content_type(self, client):
        """Test POST request without JSON content type"""
        response = client.post('/data', data='not json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_data_post_with_expression(self, client):
        """Test POST request with expression field (vulnerable code path)"""
        payload = {
            'expression': '2 + 2'
        }
        response = client.post(
            '/data',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['result'] == 4
    
    def test_data_get_not_allowed(self, client):
        """Test that GET requests are not allowed on /data endpoint"""
        response = client.get('/data')
        assert response.status_code == 405
    
    def test_data_put_not_allowed(self, client):
        """Test that PUT requests are not allowed on /data endpoint"""
        response = client.put('/data')
        assert response.status_code == 405
    
    def test_data_delete_not_allowed(self, client):
        """Test that DELETE requests are not allowed on /data endpoint"""
        response = client.delete('/data')
        assert response.status_code == 405
    
    def test_data_post_empty_json(self, client):
        """Test POST request with empty JSON payload"""
        response = client.post(
            '/data',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
    
    def test_data_post_complex_json(self, client):
        """Test POST request with complex JSON payload"""
        payload = {
            'user': {
                'name': 'John Doe',
                'age': 30
            },
            'items': [1, 2, 3, 4, 5],
            'metadata': {
                'timestamp': '2026-03-16',
                'source': 'test'
            }
        }
        response = client.post(
            '/data',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['received'] == payload


class TestVulnerability:
    """Tests to demonstrate the code injection vulnerability"""
    
    def test_code_injection_vulnerability(self, client):
        """
        WARNING: This test demonstrates the code injection vulnerability
        The eval() function in the /data endpoint is vulnerable to code injection
        """
        # This would execute arbitrary Python code on the server
        payload = {
            'expression': '__import__("os").getcwd()'
        }
        response = client.post(
            '/data',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200
        # This test passes, demonstrating the vulnerability exists
