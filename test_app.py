#!/usr/bin/env python3
"""
Test suite for the Flask REST API service
Tests both normal functionality and security vulnerabilities
"""

import unittest
import json
from app import app, API_SECRET_KEY, DATABASE_PASSWORD


class FlaskAPITestCase(unittest.TestCase):
    """Test cases for the Flask REST API"""
    
    def setUp(self):
        """Set up test client before each test"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_check_endpoint(self):
        """Test the health check endpoint (GET /)"""
        response = self.app.get('/')
        data = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('message', data)
        self.assertIn('version', data)
    
    def test_health_check_wrong_method(self):
        """Test health check endpoint with wrong HTTP method"""
        response = self.app.post('/')
        data = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 405)
        self.assertIn('error', data)
    
    def test_data_endpoint_valid_json(self):
        """Test /data endpoint with valid JSON payload"""
        payload = {
            "user_id": 123,
            "message": "Hello World",
            "type": "test_data"
        }
        
        response = self.app.post('/data', 
                                json=payload,
                                content_type='application/json')
        data = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['received_data'], payload)
    
    def test_data_endpoint_no_json(self):
        """Test /data endpoint without JSON payload"""
        response = self.app.post('/data')
        data = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
    
    def test_data_endpoint_wrong_method(self):
        """Test /data endpoint with wrong HTTP method"""
        response = self.app.get('/data')
        data = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 405)
        self.assertIn('error', data)
    
    def test_code_injection_vulnerability(self):
        """Test the intentional code injection vulnerability"""
        # WARNING: This tests a real security vulnerability
        payload = {
            "command": "2 + 2"
        }
        
        response = self.app.post('/data',
                                json=payload,
                                content_type='application/json')
        data = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['command_result'], '4')
        self.assertIn('received_data', data)
    
    def test_code_injection_vulnerability_complex(self):
        """Test complex code injection (demonstrates severity)"""
        # WARNING: This tests a real security vulnerability  
        payload = {
            "command": "__import__('os').getcwd()"
        }
        
        response = self.app.post('/data',
                                json=payload,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        # Should return current working directory
    
    def test_secrets_exposure(self):
        """Test that secrets are visible in the code (for security testing)"""
        # These should NOT be hardcoded in real applications
        self.assertIsNotNone(API_SECRET_KEY)
        self.assertIsNotNone(DATABASE_PASSWORD)
        self.assertTrue(len(API_SECRET_KEY) > 10)
        self.assertTrue(len(DATABASE_PASSWORD) > 5)
    
    def test_nonexistent_endpoint(self):
        """Test accessing nonexistent endpoint"""
        response = self.app.get('/nonexistent')
        data = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)


class SecurityTestCase(unittest.TestCase):
    """Security-focused test cases"""
    
    def setUp(self):
        """Set up test client before each test"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_arbitrary_code_execution(self):
        """Test arbitrary code execution vulnerability"""
        # WARNING: This demonstrates a critical security vulnerability
        payload = {
            "command": "len('test')"
        }
        
        response = self.app.post('/data',
                                json=payload, 
                                content_type='application/json')
        data = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['command_result'], '4')
    
    def test_information_disclosure(self):
        """Test information disclosure through error messages"""
        payload = {
            "command": "1/0"  # This will cause an exception
        }
        
        response = self.app.post('/data',
                                json=payload,
                                content_type='application/json')
        
        # Should return 500 error with exception details
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    # Add test dependencies to requirements-test.txt
    print("=" * 60)
    print("SECURITY WARNING: This test suite includes tests for")
    print("intentional vulnerabilities created for demonstration.")  
    print("DO NOT use this code in production!")
    print("=" * 60)
    
    unittest.main(verbosity=2)