from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class BaseService(ABC):
    """Base class for LLM service implementations."""
    
    def __init__(self, model: str, api_key: str):
        """
        Initialize the service.
        
        Args:
            model: The model identifier to use
            api_key: API key for authentication
        """
        self.model = model
        self.api_key = api_key
        
    @abstractmethod
    def call(self, prompt: str) -> str:
        """
        Send a prompt to the LLM service and get the response.
        
        Args:
            prompt: The input text to send to the model
            
        Returns:
            The model's response as a string
        """
        pass
