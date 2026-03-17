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
