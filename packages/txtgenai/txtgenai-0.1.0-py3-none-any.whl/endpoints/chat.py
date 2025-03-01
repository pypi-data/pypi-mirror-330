# textgen/endpoints/chat.py
from typing import Dict, List, Optional, Union, Any

class ChatEndpoint:
    """
    Handler for chat completions API.
    """
    
    def __init__(self, client):
        """
        Initialize the chat endpoint handler.
        
        Args:
            client: The TextGenClient instance
        """
        self.client = client
        
    def generate(self, 
               messages: List[Dict[str, str]], 
               model: Optional[str] = None,
               temperature: Optional[float] = None,
               max_tokens: Optional[int] = None,
               top_p: Optional[float] = None,
               stream: bool = False,
               stop: Optional[Union[str, List[str]]] = None,
               **kwargs) -> Dict:
        """
        Generate a chat completion response.
        
        Args:
            messages: A list of message dictionaries with 'role' and 'content'
            model: The model to use (optional, will use default if not specified)
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter
            stream: Whether to stream the response
            stop: Sequences where the API will stop generating further tokens
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            The generated response
        """
        json_data = {
            "messages": messages,
        }
        
        # Add model if provided, otherwise will use default from backend
        if model:
            json_data["model"] = model
            
        # Add optional parameters if provided
        if temperature is not None:
            json_data["temperature"] = temperature
            
        if max_tokens is not None:
            json_data["max_tokens"] = max_tokens
            
        if top_p is not None:
            json_data["top_p"] = top_p
            
        if stream:
            json_data["stream"] = stream
            
        if stop:
            json_data["stop"] = stop
            
        # Add any additional parameters
        for key, value in kwargs.items():
            json_data[key] = value
            
        response = self.client.post(
            endpoint="chat/completions",
            json_data=json_data
        )
        
        # Process the response to make it simpler for users
        if 'choices' in response and len(response['choices']) > 0:
            # Extract just the content for simplicity
            simple_response = {
                'content': response['choices'][0]['message']['content'],
                'model_used': response.get('model', 'unknown'),
                'full_response': response  # Include full response for users who need it
            }
            return simple_response
        
        return response
        
    def stream_chat(self, 
                    messages: List[Dict[str, str]],
                    model: Optional[str] = None,
                    **kwargs) -> Any:
        """
        Stream a chat completion response.
        
        Args:
            messages: A list of message dictionaries with 'role' and 'content'
            model: The model to use (optional)
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            A generator yielding response chunks
        """
        kwargs["stream"] = True
        return self.generate(messages, model, **kwargs)