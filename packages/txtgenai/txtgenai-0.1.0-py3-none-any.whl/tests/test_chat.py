# textgen/tests/test_chat.py
import unittest
from unittest.mock import patch, MagicMock

from textgen.client import TextGenClient
from textgen.endpoints.chat import ChatEndpoint

class TestChatEndpoint(unittest.TestCase):
    """
    Tests for the ChatEndpoint class.
    """
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TextGenClient()
        self.chat_endpoint = ChatEndpoint(self.client)
    
    @patch.object(TextGenClient, 'post')
    def test_generate(self, mock_post):
        """Test chat generation"""
        # Setup mock response
        mock_response = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1677652288,
            "model": "test-model",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello, how can I help you today?"
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 8,
                "total_tokens": 18
            }
        }
        mock_post.return_value = mock_response
        
        # Test messages
        messages = [
            {"role": "user", "content": "Hello"}
        ]
        
        # Execute generate
        result = self.chat_endpoint.generate(messages)
        
        # Verify results
        self.assertEqual(result['content'], "Hello, how can I help you today?")
        self.assertEqual(result['model_used'], "test-model")
        self.assertEqual(result['full_response'], mock_response)
        
        # Verify post call
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['endpoint'], "chat/completions")
        self.assertEqual(kwargs['json_data']['messages'], messages)
    
    @patch.object(TextGenClient, 'post')
    def test_generate_with_parameters(self, mock_post):
        """Test chat generation with parameters"""
        # Setup mock response
        mock_post.return_value = {
            "choices": [{
                "message": {
                    "content": "Test response"
                }
            }],
            "model": "test-model"
        }
        
        # Test messages and parameters
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Tell me a joke."}
        ]
        
        # Execute generate with parameters
        result = self.chat_endpoint.generate(
            messages,
            model="specific-model",
            temperature=0.7,
            max_tokens=100,
            top_p=0.9,
            stop=["User:"]
        )
        
        # Verify post call parameters
        args, kwargs = mock_post.call_args
        json_data = kwargs['json_data']
        
        self.assertEqual(json_data['messages'], messages)
        self.assertEqual(json_data['model'], "specific-model")
        self.assertEqual(json_data['temperature'], 0.7)
        self.assertEqual(json_data['max_tokens'], 100)
        self.assertEqual(json_data['top_p'], 0.9)
        self.assertEqual(json_data['stop'], ["User:"])
    
    @patch.object(ChatEndpoint, 'generate')
    def test_stream_chat(self, mock_generate):
        """Test stream chat functionality"""
        # Setup mock response
        mock_generate.return_value = "streaming_response"
        
        # Test messages
        messages = [
            {"role": "user", "content": "Tell me a story."}
        ]
        
        # Execute stream_chat
        result = self.chat_endpoint.stream_chat(messages, model="test-model")
        
        # Verify results
        self.assertEqual(result, "streaming_response")
        
        # Verify generate call
        mock_generate.assert_called_with(
            messages, 
            "test-model", 
            stream=True
        )

if __name__ == '__main__':
    unittest.main()