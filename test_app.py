"""
Test suite for the Flask REST API
Tests for health check endpoint and data processing endpoint
"""

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
    """Tests for the / health check endpoint"""
    
    def test_health_check_get_success(self, client):
        """Test that GET request to / returns healthy status"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'message' in data
    
    def test_health_check_post_not_allowed(self, client):
        """Test that POST request to / is not allowed"""
        response = client.post('/')
        assert response.status_code == 405
    
    def test_health_check_put_not_allowed(self, client):
        """Test that PUT request to / is not allowed"""
        response = client.put('/')
        assert response.status_code == 405
    
    def test_health_check_delete_not_allowed(self, client):
        """Test that DELETE request to / is not allowed"""
        response = client.delete('/')
        assert response.status_code == 405


class TestDataEndpoint:
    """Tests for the /data endpoint"""
    
    def test_data_post_success_normal_data(self, client):
        """Test that POST request to /data with normal data succeeds"""
        payload = {"key": "value", "number": 42}
        response = client.post('/data',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert data['data'] == payload
    
    def test_data_post_no_json(self, client):
        """Test that POST request without JSON returns error"""
        response = client.post('/data')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_data_post_with_command_injection(self, client):
        """Test the code injection vulnerability (for security testing)"""
        payload = {"command": "1 + 1"}
        response = client.post('/data',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'result' in data
        assert data['result'] == '2'
    
    def test_data_post_with_dangerous_command(self, client):
        """Test dangerous code injection (for security testing)"""
        payload = {"command": "__import__('os').getcwd()"}
        response = client.post('/data',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'result' in data
    
    def test_data_get_not_allowed(self, client):
        """Test that GET request to /data is not allowed"""
        response = client.get('/data')
        assert response.status_code == 405
    
    def test_data_put_not_allowed(self, client):
        """Test that PUT request to /data is not allowed"""
        response = client.put('/data')
        assert response.status_code == 405
    
    def test_data_delete_not_allowed(self, client):
        """Test that DELETE request to /data is not allowed"""
        response = client.delete('/data')
        assert response.status_code == 405
    
    def test_data_post_with_invalid_json(self, client):
        """Test that POST with invalid JSON format handles errors"""
        response = client.post('/data',
                              data='invalid json',
                              content_type='application/json')
        assert response.status_code in [400, 500]
    
    def test_data_post_with_complex_data(self, client):
        """Test POST with complex nested JSON data"""
        payload = {
            "user": {
                "name": "Test User",
                "id": 123
            },
            "items": [1, 2, 3, 4, 5],
            "metadata": {
                "timestamp": "2026-03-11",
                "version": "1.0"
            }
        }
        response = client.post('/data',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data'] == payload
