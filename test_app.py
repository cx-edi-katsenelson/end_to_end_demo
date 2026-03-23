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
    
    def test_health_check_delete_not_allowed(self, client):
        """Test that DELETE is not allowed on health check endpoint"""
        response = client.delete('/')
        assert response.status_code == 405


class TestDataEndpoint:
    """Tests for the data processing endpoint"""
    
    def test_data_post_valid_json(self, client):
        """Test POST request with valid JSON payload"""
        payload = {'name': 'test', 'value': 123}
        response = client.post(
            '/data',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data'] == payload
    
    def test_data_post_empty_json(self, client):
        """Test POST request with empty JSON"""
        response = client.post(
            '/data',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
    
    def test_data_post_no_json(self, client):
        """Test POST request without JSON payload"""
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
    
    def test_data_post_with_expression(self, client):
        """Test POST request with expression field (vulnerable code path)"""
        payload = {'expression': '2 + 2'}
        response = client.post(
            '/data',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['result'] == 4
    
    def test_data_post_complex_payload(self, client):
        """Test POST request with complex nested JSON"""
        payload = {
            'user': {
                'name': 'John Doe',
                'email': 'john@example.com'
            },
            'items': [1, 2, 3, 4, 5],
            'metadata': {
                'timestamp': '2026-03-23T00:00:00Z',
                'version': '1.0'
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
        assert data['data'] == payload


class TestInvalidRoutes:
    """Tests for invalid routes"""
    
    def test_invalid_route(self, client):
        """Test request to non-existent route"""
        response = client.get('/invalid')
        assert response.status_code == 404
    
    def test_invalid_route_post(self, client):
        """Test POST request to non-existent route"""
        response = client.post('/invalid')
        assert response.status_code == 404


class TestContentType:
    """Tests for content type handling"""
    
    def test_data_post_invalid_content_type(self, client):
        """Test POST with invalid content type"""
        response = client.post(
            '/data',
            data='not json',
            content_type='text/plain'
        )
        # Flask will return 400 or 500 depending on how it handles the invalid JSON
        assert response.status_code in [400, 500]
    
    def test_data_post_form_data(self, client):
        """Test POST with form data instead of JSON"""
        response = client.post(
            '/data',
            data={'key': 'value'},
            content_type='application/x-www-form-urlencoded'
        )
        # Should fail as we expect JSON
        assert response.status_code in [400, 500]
