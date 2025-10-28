"""
Output Service - Domain Layer
Handles output generation in different formats (hexagonal architecture).
"""
from typing import List, Dict, Any, Optional
from src.features.email_processing.domain.email import Email


class OutputService:
    """Service for generating output in different formats."""
    
    @staticmethod
    def generate_inline(emails: List[Email]) -> List[str]:
        """Generate inline output (list of email strings)."""
        return [str(email) for email in emails]
    
    @staticmethod
    def generate_silent(emails: List[Email]) -> int:
        """Generate silent output (just count)."""
        return len(emails)
    
    @staticmethod
    def to_dict_list(emails: List[Email]) -> List[Dict[str, str]]:
        """Convert emails to list of dictionaries."""
        return [
            {
                'nombre': email.nombre,
                'apellido': email.apellido,
                'correo_original': email.correo_original,
                'correo_nuevo': email.correo_nuevo
            }
            for email in emails
        ]
