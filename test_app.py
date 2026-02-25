import pytest
import json
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check_get(client):
    """Test GET request to health check endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['service'] == 'Flask REST API'
    assert data['version'] == '1.0.0'

def test_health_check_post_not_allowed(client):
    """Test that POST requests are not allowed on health check endpoint"""
    response = client.post('/')
    assert response.status_code == 405  # Method Not Allowed

def test_data_endpoint_post_valid_json(client):
    """Test POST request to data endpoint with valid JSON"""
    test_data = {'key': 'value', 'number': 42}
    response = client.post('/data',
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'received' in data
    assert data['received'] == test_data

def test_data_endpoint_post_no_json(client):
    """Test POST request to data endpoint without JSON payload"""
    response = client.post('/data')
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert 'error' in data
    assert 'No JSON payload provided' in data['error']

def test_data_endpoint_get_not_allowed(client):
    """Test that GET requests are not allowed on data endpoint"""
    response = client.get('/data')
    assert response.status_code == 405  # Method Not Allowed

def test_code_injection_vulnerability(client):
    """Test the code injection vulnerability (DO NOT USE IN PRODUCTION!)
    
    WARNING: This test demonstrates the security vulnerability!
    """
    # Test basic math expression injection
    malicious_payload = {'command': '2 + 2'}
    response = client.post('/data',
                          data=json.dumps(malicious_payload),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['command_result'] == '4'
    
    # Test string injection
    malicious_payload = {'command': '"hello" + " world"'}
    response = client.post('/data',
                          data=json.dumps(malicious_payload),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['command_result'] == 'hello world'

def test_secrets_exposure(client):
    """Test that secrets are exposed in API response (security issue!)"""
    test_data = {'test': 'data'}
    response = client.post('/data',
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'api_key_used' in data
    assert data['api_key_used'].startswith('sk-abc123d')

def test_invalid_json_handling(client):
    """Test handling of malformed JSON"""
    response = client.post('/data',
                          data='invalid json{',
                          content_type='application/json')
    
    assert response.status_code == 400
