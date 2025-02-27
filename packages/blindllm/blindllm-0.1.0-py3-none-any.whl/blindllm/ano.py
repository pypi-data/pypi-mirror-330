# Ajout de l'importation de la bibliothèque text-anonymizer
import text_anonymizer
from typing import Dict, Tuple

class TextAnonymizer:
    def __init__(self):
        pass  # Suppression des patterns et des compteurs

    def anonymize(self, text: str) -> tuple[str, dict]:
        """
        Anonymise le texte donné.
        
        Args:
            text: Le texte à anonymiser
            
        Returns:
            Un tuple (texte_anonymisé, dictionnaire_correspondance)
        """
        # Utiliser la fonction anonymize importée
        return text_anonymizer.anonymize(text)  # Appel à la fonction importée

    def deanonymize(self, text: str, anonymization_map: Dict[str, str]) -> str:
        """
        Restore original values in anonymized text.
        
        Args:
            text: The anonymized text.
            anonymization_map: Dictionary mapping tokens to original values.
            
        Returns:
            The original text with sensitive information restored.
        """
        # Utiliser la fonction deanonymize importée
        return text_anonymizer.deanonymize(text, anonymization_map)  # Appel à la fonction importée

# Create singleton instance
_anonymizer = TextAnonymizer()

def anonymize(text: str) -> tuple[str, dict]:
    """
    Fonction utilitaire pour anonymiser du texte.
    
    Args:
        text: Le texte à anonymiser
        
    Returns:
        Un tuple (texte_anonymisé, dictionnaire_correspondance)
    """
    return _anonymizer.anonymize(text)

def deanonymize(text: str, anonymization_map: Dict[str, str]) -> str:
    """Convenience function to deanonymize text using the singleton instance."""
    return _anonymizer.deanonymize(text, anonymization_map)