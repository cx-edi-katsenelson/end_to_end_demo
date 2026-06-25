import unittest
import json
from app import app


class TestFlaskApp(unittest.TestCase):
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.client = self.app.test_client()
        self.app.testing = True
    
    def test_health_check_get(self):
        """Test GET request to health check endpoint"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('message', data)
    
    def test_health_check_post_not_allowed(self):
        """Test that POST is not allowed on health check endpoint"""
        response = self.client.post('/')
        self.assertEqual(response.status_code, 405)
    
    def test_data_endpoint_post_valid_json(self):
        """Test POST request to /data with valid JSON"""
        payload = {"name": "test", "value": 123}
        response = self.client.post(
            '/data',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
    
    def test_data_endpoint_post_with_expression(self):
        """Test POST request to /data with expression field"""
        payload = {"expression": "2 + 2"}
        response = self.client.post(
            '/data',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], 4)
    
    def test_data_endpoint_post_invalid_content_type(self):
        """Test POST request to /data with invalid content type"""
        response = self.client.post(
            '/data',
            data="not json",
            content_type='text/plain'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_data_endpoint_get_not_allowed(self):
        """Test that GET is not allowed on /data endpoint"""
        response = self.client.get('/data')
        self.assertEqual(response.status_code, 405)
    
    def test_data_endpoint_put_not_allowed(self):
        """Test that PUT is not allowed on /data endpoint"""
        response = self.client.put('/data')
        self.assertEqual(response.status_code, 405)
    
    def test_data_endpoint_delete_not_allowed(self):
        """Test that DELETE is not allowed on /data endpoint"""
        response = self.client.delete('/data')
        self.assertEqual(response.status_code, 405)


if __name__ == '__main__':
    unittest.main()
