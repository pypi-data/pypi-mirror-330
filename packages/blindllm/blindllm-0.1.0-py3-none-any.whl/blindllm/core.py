from typing import Optional
from .ano import anonymize, deanonymize
from .services import create_service, ServiceType

class BlindLLM:
    """
    Main class for anonymized LLM interactions.
    Handles anonymization of prompts and de-anonymization of responses.
    """
    
    def __init__(self, service: ServiceType, model: str, api_key: str):
        """
        Initialize BlindLLM with a specific service configuration.
        
        Args:
            service: Service type ("openai", "mistral", or "claude")
            model: Model identifier for the chosen service
            api_key: API key for authentication
        """
        self.service = create_service(service, model, api_key)
    
    def call(self, prompt: str) -> dict:
        """
        Send a prompt to the LLM service with automatic anonymization and de-anonymization.
        
        Args:
            prompt: The input text to send to the model
            
        Returns:
            A dictionary containing:
            - anonymized_prompt: The anonymized version of the input prompt
            - anonymized_response: The raw response from the LLM
            - response: The de-anonymized final response
            - anonymization_map: The mapping of anonymized tokens to original values
            
        Example:
            llm = BlindLLM(service="openai", model="gpt-4", api_key="your-api-key")
            result = llm.call("John Smith from Acme Corp sent an email about project X")
            print(result['anonymized_prompt'])  # Anonymized input
            print(result['anonymized_response'])  # Raw LLM response
            print(result['response'])  # De-anonymized response
            print(result['anonymization_map'])  # Anonymization mapping
        """
        # Step 1: Anonymize the prompt
        anonymized_prompt, anonymization_map = anonymize(prompt)
        
        # Step 2: Send to LLM service
        anonymized_response = self.service.call(anonymized_prompt)
        
        # Step 3: De-anonymize the response
        original_response = deanonymize(anonymized_response, anonymization_map)
        
        return {
            'anonymized_prompt': anonymized_prompt,
            'anonymized_response': anonymized_response,
            'response': original_response,
            'anonymization_map': anonymization_map
        }
