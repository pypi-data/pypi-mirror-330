# textgen/endpoints/models.py
from typing import Dict, List, Optional

class ModelsEndpoint:
    """
    Handler for models API.
    """
    
    def __init__(self, client):
        """
        Initialize the models endpoint handler.
        
        Args:
            client: The TextGenClient instance
        """
        self.client = client
        
    def list(self) -> List[Dict]:
        """
        List all available models.
        
        Returns:
            List of model information dictionaries
        """
        response = self.client.get("models")
        
        # Simplify the response for easier consumption
        if 'data' in response:
            models = response['data']
            # Extract and transform the relevant information
            simplified_models = [
                {
                    'id': model.get('id'),
                    'name': model.get('name', model.get('id')),
                    'context_length': model.get('context_length'),
                    'capabilities': model.get('capabilities', [])
                }
                for model in models
            ]
            return simplified_models
        return response
    
    def retrieve(self, model_id: str) -> Dict:
        """
        Get information about a specific model.
        
        Args:
            model_id: The ID of the model to retrieve
            
        Returns:
            Model information dictionary
        """
        return self.client.get(f"models/{model_id}")