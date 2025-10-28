"""
Library Usage Adapter - Modular & Stateless
"""
from typing import Union, List
from src.features.email_processing.domain.email_service import EmailProcessingService
from src.features.email_processing.adapters.output.file_adapter import FileEmailRepository

from src.shared.validation_adapter import RegexEmailValidator
from src.shared.logging_adapter import PythonLogger


class EmailProcessingLibrary:
    """
    Stateless library for email processing.
    Each method is independent and can be used separately.
    """
    
    # Shared service instance
    _validator = RegexEmailValidator()
    _logger = PythonLogger("library")
    _service = EmailProcessingService(_validator, _logger)
    
    @staticmethod
    def extract(input_data: Union[str, List[str]], input_type: str = 'file') -> List[str]:
        """
        Extract emails from different sources.
        
        Args:
            input_data: File path, list of emails, or text with emails
            input_type: 'file', 'list', or 'text'
        
        Returns:
            List of email strings
        """
        if input_type == 'file':
            return FileEmailRepository().read(input_data)
        elif input_type == 'list':
            return input_data if isinstance(input_data, list) else input_data.split(',')
        elif input_type == 'text':
            return [e.strip() for e in input_data.split('\n') if e.strip()]
        else:
            raise ValueError(f"Invalid input_type: {input_type}")
    
    @classmethod
    def transform(cls, emails: List[str], new_domain: str) -> List[dict]:
        """
        Transform emails to new domain.
        
        Args:
            emails: List of email strings
            new_domain: New domain to apply
        
        Returns:
            List of dicts with 'original', 'transformed', 'valid' keys
        """
        # Use domain service
        result = cls._service.transform_emails(emails, new_domain)
        
        transformed = []
        for email in result['emails']:
            transformed.append({
                'original': email.correo_original,
                'transformed': str(email),
                'valid': True
            })
        
        for error in result['error_details']:
            transformed.append({
                'original': error['email'],
                'valid': False,
                'error': error['error']
            })
        
        return transformed
    
    @staticmethod
    def generate(transformed: List[dict], output_type: str = 'inline', output_file: str = None):
        """
        Generate output in different formats.
        
        Args:
            transformed: List of transformed email dicts
            output_type: 'csv', 'json', 'inline', or 'silent'
            output_file: Output file path (required for csv/json)
        
        Returns:
            Count of processed emails or list of emails (for inline)
        """
        if output_type == 'csv':
            if not output_file:
                raise ValueError("output_file required for csv")
            # Convert to Email objects
            from src.features.email_processing.domain.email import Email
            email_objects = []
            for item in transformed:
                if item.get('valid'):
                    parts = item['transformed'].split('@')
                    if len(parts) == 2:
                        name_parts = parts[0].split('.')
                        if len(name_parts) == 2:
                            email_obj = Email.create(
                                nombre=name_parts[0],
                                apellido=name_parts[1],
                                correo_original=item['original'],
                                nuevo_dominio=parts[1]
                            )
                            email_objects.append(email_obj)
            from src.features.email_processing.adapters.output.csv_adapter import CsvEmailWriter
            CsvEmailWriter().save_emails(email_objects, output_file)
            return len(email_objects)
        
        elif output_type == 'json':
            if not output_file:
                raise ValueError("output_file required for json")
            # Convert to Email objects
            from src.features.email_processing.domain.email import Email
            from src.features.email_processing.adapters.output.json_adapter import JsonEmailWriter
            email_objects = []
            for item in transformed:
                if item.get('valid'):
                    parts = item['transformed'].split('@')
                    if len(parts) == 2:
                        name_parts = parts[0].split('.')
                        if len(name_parts) == 2:
                            email_obj = Email.create(
                                nombre=name_parts[0],
                                apellido=name_parts[1],
                                correo_original=item['original'],
                                nuevo_dominio=parts[1]
                            )
                            email_objects.append(email_obj)
            JsonEmailWriter().save_emails(email_objects, output_file)
            return len(email_objects)
        
        elif output_type == 'inline':
            emails = [item['transformed'] for item in transformed if item.get('valid')]
            return emails
        
        elif output_type == 'silent':
            emails = [item['transformed'] for item in transformed if item.get('valid')]
            return len(emails)
        
        else:
            raise ValueError(f"Invalid output_type: {output_type}")
    
    @classmethod
    def validate(cls, email: str) -> bool:
        """
        Validate a single email.
        
        Args:
            email: Email string to validate
        
        Returns:
            True if valid, False otherwise
        """
        try:
            cls._validator.validate_and_parse(email)
            return True
        except:
            return False
