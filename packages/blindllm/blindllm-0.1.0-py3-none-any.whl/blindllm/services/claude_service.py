import anthropic
from .base import BaseService

class ClaudeService(BaseService):
    """Service implementation for Anthropic's Claude API."""
    
    def __init__(self, model: str, api_key: str):
        """
        Initialize the Claude service.
        
        Args:
            model: The model to use (e.g., "claude-3-5-sonnet-20241022")
            api_key: Anthropic API key
        """
        super().__init__(model, api_key)
        self.client = anthropic.Anthropic(api_key=api_key)
        
    def call(self, prompt: str) -> str:
        """
        Send a prompt to Claude and get the response.
        
        Args:
            prompt: The input text to send to the model
            
        Returns:
            The model's response as a string
        """
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }]
        )
        return message.content[0].text
