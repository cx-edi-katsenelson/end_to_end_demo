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
    """Tests for the health check endpoint (/)"""
    
    def test_health_check_get_success(self, client):
        """Test GET request to health check endpoint returns 200"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'service' in data
        assert 'version' in data
    
    def test_health_check_post_not_allowed(self, client):
        """Test POST request to health check endpoint is not allowed"""
        response = client.post('/')
        assert response.status_code == 405
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_health_check_put_not_allowed(self, client):
        """Test PUT request to health check endpoint is not allowed"""
        response = client.put('/')
        assert response.status_code == 405
    
    def test_health_check_delete_not_allowed(self, client):
        """Test DELETE request to health check endpoint is not allowed"""
        response = client.delete('/')
        assert response.status_code == 405


class TestDataEndpoint:
    """Tests for the data endpoint (/data)"""
    
    def test_data_post_success(self, client):
        """Test POST request with valid JSON to /data endpoint"""
        payload = {
            'name': 'test',
            'value': 123,
            'items': ['a', 'b', 'c']
        }
        response = client.post(
            '/data',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'received_data' in data
    
    def test_data_post_no_json(self, client):
        """Test POST request without JSON data returns 400"""
        response = client.post('/data')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_data_get_not_allowed(self, client):
        """Test GET request to /data endpoint is not allowed"""
        response = client.get('/data')
        assert response.status_code == 405
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_data_put_not_allowed(self, client):
        """Test PUT request to /data endpoint is not allowed"""
        response = client.put('/data')
        assert response.status_code == 405
    
    def test_data_delete_not_allowed(self, client):
        """Test DELETE request to /data endpoint is not allowed"""
        response = client.delete('/data')
        assert response.status_code == 405
    
    def test_data_post_with_command_vulnerability(self, client):
        """
        Test the intentional code injection vulnerability
        WARNING: This tests a deliberate security flaw for demonstration
        """
        payload = {
            'command': '2 + 2'
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
    
    def test_data_post_empty_json(self, client):
        """Test POST request with empty JSON object"""
        payload = {}
        response = client.post(
            '/data',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # Empty JSON is still valid JSON
        assert response.status_code == 200
    
    def test_data_post_invalid_json(self, client):
        """Test POST request with invalid JSON"""
        response = client.post(
            '/data',
            data='not valid json',
            content_type='application/json'
        )
        assert response.status_code in [400, 500]


class TestErrorHandlers:
    """Tests for error handlers"""
    
    def test_404_not_found(self, client):
        """Test 404 error handler for non-existent endpoint"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_404_post_not_found(self, client):
        """Test 404 error handler for POST to non-existent endpoint"""
        response = client.post('/nonexistent')
        assert response.status_code == 404


class TestContentType:
    """Tests for content type handling"""
    
    def test_data_post_without_content_type(self, client):
        """Test POST to /data without explicit content-type"""
        payload = {'test': 'data'}
        response = client.post(
            '/data',
            data=json.dumps(payload)
        )
        # Should still work or return appropriate error
        assert response.status_code in [200, 400, 415]
    
    def test_health_check_returns_json(self, client):
        """Test that health check returns JSON content type"""
        response = client.get('/')
        assert response.content_type == 'application/json'
    
    def test_data_endpoint_returns_json(self, client):
        """Test that data endpoint returns JSON content type"""
        payload = {'test': 'data'}
        response = client.post(
            '/data',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.content_type == 'application/json'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
