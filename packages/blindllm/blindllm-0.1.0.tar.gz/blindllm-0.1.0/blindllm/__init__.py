"""
BlindLLM - A library for making anonymized calls to LLM APIs
"""

from .core import BlindLLM
from .services import ServiceType

__version__ = "0.1.0"
__all__ = ["BlindLLM", "ServiceType"]
