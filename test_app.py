#!/usr/bin/env python3
"""
Test suite for Flask REST API
Tests both endpoints and various scenarios including the vulnerability
"""

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
    """Tests for the / health check endpoint"""
    
    def test_health_check_get_success(self, client):
        """Test successful GET request to health check endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'OK'
        assert data['service'] == 'Flask REST API'
        assert data['version'] == '1.0.0'
    
    def test_health_check_post_not_allowed(self, client):
        """Test that POST requests to health check are not allowed"""
        response = client.post('/')
        assert response.status_code == 405
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Method not allowed' in data['error']
    
    def test_health_check_put_not_allowed(self, client):
        """Test that PUT requests to health check are not allowed"""
        response = client.put('/')
        assert response.status_code == 405
    
    def test_health_check_delete_not_allowed(self, client):
        """Test that DELETE requests to health check are not allowed"""
        response = client.delete('/')
        assert response.status_code == 405

class TestDataEndpoint:
    """Tests for the /data endpoint"""
    
    def test_data_post_success(self, client):
        """Test successful POST request to data endpoint"""
        payload = {
            'name': 'test_user',
            'data': [1, 2, 3, 4, 5],
            'metadata': {'type': 'test'}
        }
        
        response = client.post('/data', 
                              json=payload,
                              content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['processed'] is True
        assert data['received_data'] == payload
        assert 'timestamp' in data
        assert 'db_connection' in data
    
    def test_data_post_empty_payload(self, client):
        """Test POST request with empty JSON payload"""
        response = client.post('/data', 
                              json={},
                              content_type='application/json')
        assert response.status_code == 200  # Empty JSON is still valid
    
    def test_data_post_no_json(self, client):
        """Test POST request without JSON payload"""
        response = client.post('/data')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'No JSON payload provided' in data['error']
    
    def test_data_get_not_allowed(self, client):
        """Test that GET requests to data endpoint are not allowed"""
        response = client.get('/data')
        assert response.status_code == 405
    
    def test_data_put_not_allowed(self, client):
        """Test that PUT requests to data endpoint are not allowed"""
        response = client.put('/data')
        assert response.status_code == 405
    
    def test_data_post_with_command_vulnerability(self, client):
        """
        Test the code injection vulnerability in /data endpoint
        WARNING: This tests a security vulnerability - DO NOT use in production!
        """
        # Test basic mathematical expression
        payload = {'command': '2 + 2'}
        response = client.post('/data', 
                              json=payload,
                              content_type='application/json')
        assert response.status_code == 200
        
        # Test variable assignment (this will execute due to eval vulnerability)
        payload = {'command': 'test_var = "injected"'}
        response = client.post('/data', 
                              json=payload,
                              content_type='application/json')
        assert response.status_code == 200
    
    def test_data_post_malformed_json(self, client):
        """Test POST request with malformed JSON"""
        response = client.post('/data', 
                              data='{"invalid": json}',
                              content_type='application/json')
        assert response.status_code == 400

class TestErrorHandling:
    """Tests for error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 error for non-existent endpoint"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Endpoint not found' in data['error']
    
    def test_405_method_not_allowed_data_endpoint(self, client):
        """Test 405 error for wrong HTTP method on data endpoint"""
        response = client.get('/data')
        assert response.status_code == 405
    
    def test_405_method_not_allowed_health_endpoint(self, client):
        """Test 405 error for wrong HTTP method on health endpoint"""  
        response = client.post('/')
        assert response.status_code == 405

class TestSecurityVulnerabilities:
    """Tests to demonstrate security vulnerabilities (for educational purposes)"""
    
    def test_secrets_exposure(self, client):
        """Test that secrets are exposed in responses"""
        payload = {'test': 'data'}
        response = client.post('/data', 
                              json=payload,
                              content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        # Verify that the database password is exposed in response
        assert 'admin123' in data['db_connection']
    
    def test_code_injection_vulnerability(self, client):
        """
        Test the eval() code injection vulnerability
        WARNING: This is a deliberate security flaw for demonstration
        """
        # Test that we can execute arbitrary Python code
        payload = {'command': '__import__("os").getcwd()'}
        response = client.post('/data', 
                              json=payload,
                              content_type='application/json')
        # The request should succeed (which means the vulnerability exists)
        assert response.status_code == 200

if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v'])