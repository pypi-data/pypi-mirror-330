from mistralai import Mistral
from .base import BaseService

class MistralService(BaseService):
    """Service implementation for Mistral API."""
    
    def __init__(self, model: str, api_key: str):
        """
        Initialize the Mistral service.
        
        Args:
            model: The model to use (e.g., "mistral-large-latest")
            api_key: Mistral API key
        """
        super().__init__(model, api_key)
        self.client = Mistral(api_key=api_key)
        
    def call(self, prompt: str) -> str:
        """
        Send a prompt to Mistral and get the response.
        
        Args:
            prompt: The input text to send to the model
            
        Returns:
            The model's response as a string
        """
        response = self.client.chat.complete(
            model=self.model,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.choices[0].message.content
