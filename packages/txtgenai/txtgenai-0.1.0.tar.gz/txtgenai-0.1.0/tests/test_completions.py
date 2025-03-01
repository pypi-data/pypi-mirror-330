# textgen/tests/test_completions.py
import unittest
from unittest.mock import patch, MagicMock

from textgen.client import TextGenClient
from textgen.endpoints.completions import CompletionsEndpoint

class TestCompletionsEndpoint(unittest.TestCase):
    """
    Tests for the CompletionsEndpoint class.
    """
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TextGenClient()
        self.completions_endpoint = CompletionsEndpoint(self.client)
    
    @patch.object(TextGenClient, 'post')
    def test_create(self, mock_post):
        """Test text completion creation"""
        # Setup mock response
        mock_response = {
            "id": "cmpl-123",
            "object": "text_completion",
            "created": 1677652288,
            "model": "test-model",
            "choices": [{
                "text": "This is a test completion response.",
                "index": 0,
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 8,
                "total_tokens": 13
            }
        }
        mock_post.return_value = mock_response
        
        # Execute create
        result = self.completions_endpoint.create(
            prompt="Complete this sentence:"
        )
        
        # Verify results
        self.assertEqual(result['text'], "This is a test completion response.")
        self.assertEqual(result['model_used'], "test-model")
        self.assertEqual(result['full_response'], mock_response)
        
        # Verify post call
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['endpoint'], "completions")
        self.assertEqual(kwargs['json_data']['prompt'], "Complete this sentence:")
    
    @patch.object(TextGenClient, 'post')
    def test_create_with_parameters(self, mock_post):
        """Test text completion creation with parameters"""
        # Setup mock response
        mock_post.return_value = {
            "choices": [{
                "text": "Test completion"
            }],
            "model": "test-model"
        }
        
        # Execute create with parameters
        result = self.completions_endpoint.create(
            prompt="Generate text:",
            model="specific-model",
            temperature=0.5,
            max_tokens=50,
            top_p=0.8,
            stop=["\n"]
        )
        
        # Verify post call parameters
        args, kwargs = mock_post.call_args
        json_data = kwargs['json_data']
        
        self.assertEqual(json_data['prompt'], "Generate text:")
        self.assertEqual(json_data['model'], "specific-model")
        self.assertEqual(json_data['temperature'], 0.5)
        self.assertEqual(json_data['max_tokens'], 50)
        self.assertEqual(json_data['top_p'], 0.8)
        self.assertEqual(json_data['stop'], ["\n"])
    
    @patch.object(CompletionsEndpoint, 'create')
    def test_stream_completion(self, mock_create):
        """Test stream completion functionality"""
        # Setup mock response
        mock_create.return_value = "streaming_response"
        
        # Execute stream_completion
        result = self.completions_endpoint.stream_completion(
            prompt="Stream text:", 
            model="test-model"
        )
        
        # Verify results
        self.assertEqual(result, "streaming_response")
        
        # Verify create call
        mock_create.assert_called_with(
            "Stream text:", 
            "test-model", 
            stream=True
        )

if __name__ == '__main__':
    unittest.main()