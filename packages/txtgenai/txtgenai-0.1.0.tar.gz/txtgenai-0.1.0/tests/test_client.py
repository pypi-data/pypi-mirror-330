# textgen/tests/test_client.py
import unittest
from unittest.mock import patch, MagicMock
import json

from textgen.client import TextGenClient
from textgen.exceptions import TextGenError, APIError

class TestTextGenClient(unittest.TestCase):
    """
    Tests for the TextGenClient class.
    """
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TextGenClient()
    
    @patch('textgen.client.requests.request')
    def test_request_success(self, mock_request):
        """Test successful API request"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": "test_data"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        # Execute request
        result = self.client.request("GET", "test/endpoint")
        
        # Verify results
        self.assertEqual(result, {"success": True, "data": "test_data"})
        mock_request.assert_called_once()
    
    @patch('textgen.client.requests.request')
    def test_request_http_error(self, mock_request):
        """Test HTTP error handling"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": {"message": "Bad request"}}
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        mock_request.return_value = mock_response
        
        # Execute request and verify exception
        with self.assertRaises(APIError):
            self.client.request("GET", "test/endpoint")
    
    @patch('textgen.client.requests.request')
    def test_request_connection_error(self, mock_request):
        """Test connection error handling"""
        # Setup mock response
        mock_request.side_effect = Exception("Connection failed")
        
        # Execute request and verify exception
        with self.assertRaises(TextGenError):
            self.client.request("GET", "test/endpoint")
    
    def test_get_method(self):
        """Test get method"""
        with patch.object(self.client, 'request') as mock_request:
            mock_request.return_value = {"success": True}
            
            result = self.client.get("test/endpoint", params={"param": "value"})
            
            mock_request.assert_called_with(
                "GET", 
                "test/endpoint", 
                params={"param": "value"}, 
                headers=None
            )
            self.assertEqual(result, {"success": True})
    
    def test_post_method(self):
        """Test post method"""
        with patch.object(self.client, 'request') as mock_request:
            mock_request.return_value = {"success": True}
            
            result = self.client.post(
                "test/endpoint", 
                json_data={"data": "value"}
            )
            
            mock_request.assert_called_with(
                "POST", 
                "test/endpoint", 
                json_data={"data": "value"}, 
                headers=None
            )
            self.assertEqual(result, {"success": True})

if __name__ == '__main__':
    unittest.main()