from typing import Literal
from .base import BaseService
from .openai_service import OpenAIService
from .mistral_service import MistralService
from .claude_service import ClaudeService

ServiceType = Literal["openai", "mistral", "claude"]

def create_service(service_type: ServiceType, model: str, api_key: str) -> BaseService:
    """
    Factory function to create the appropriate service instance.
    
    Args:
        service_type: Type of service ("openai", "mistral", or "claude")
        model: Model identifier for the service
        api_key: API key for authentication
        
    Returns:
        An instance of the appropriate service class
        
    Raises:
        ValueError: If an invalid service type is provided
    """
    services = {
        "openai": OpenAIService,
        "mistral": MistralService,
        "claude": ClaudeService
    }
    
    if service_type not in services:
        raise ValueError(f"Invalid service type: {service_type}. Must be one of: {', '.join(services.keys())}")
    
    service_class = services[service_type]
    return service_class(model=model, api_key=api_key)
