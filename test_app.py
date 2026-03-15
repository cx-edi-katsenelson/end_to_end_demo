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
    
    def test_data_post_with_command(self, client):
        """Test POST request with command field (vulnerable code path)"""
        test_data = {"command": "1 + 1"}
        response = client.post('/data',
                              data=json.dumps(test_data),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'result' in data
        assert data['result'] == 2
    
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
