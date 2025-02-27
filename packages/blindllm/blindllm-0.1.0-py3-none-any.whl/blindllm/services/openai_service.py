from typing import Optional
from openai import OpenAI
from .base import BaseService

class OpenAIService(BaseService):
    """Service implementation for OpenAI API."""
    
    def __init__(self, model: str, api_key: str):
        """
        Initialize the OpenAI service.
        
        Args:
            model: The model to use (e.g., "gpt-4", "gpt-3.5-turbo")
            api_key: OpenAI API key
        """
        super().__init__(model, api_key)
        self.client = OpenAI(api_key=api_key)
        
    def call(self, prompt: str) -> str:
        """
        Send a prompt to OpenAI and get the response.
        
        Args:
            prompt: The input text to send to the model
            
        Returns:
            The model's response as a string
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extraire le contenu du message de la réponse
        response_message = response.choices[0].message
        return response_message.content if hasattr(response_message, 'content') else str(response_message)
