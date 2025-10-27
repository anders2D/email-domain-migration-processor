import logging
import base64
from typing import Dict, Any
from src.features.email_processing.domain.email_service import EmailProcessingService
from src.shared.validation_adapter import RegexEmailValidator
from src.shared.logging_adapter import PythonLogger

logger = logging.getLogger(__name__)


class EmailProcessingLambda:
    """
    Lambda adapter for email processing.
    Handles AWS Lambda events and responses following hexagonal architecture.
    """
    
    def __init__(self):
        # Dependency Injection
        self.validator = RegexEmailValidator()
        self.logger = PythonLogger("lambda")
        self.service = EmailProcessingService(self.validator, self.logger)
    
    def extract(self, data: Dict[str, Any]) -> list:
        """Extract emails from different input types."""
        input_type = data.get('input_type', 'list')
        input_data = data.get('input', data.get('emails', []))
        
        logger.info(f"Extracting emails from {input_type}")
        
        if input_type == 'file':
            file_content = data.get('file_content')
            if not file_content:
                raise ValueError('file_content required for input_type=file')
            decoded = base64.b64decode(file_content).decode('utf-8')
            emails = [e.strip() for e in decoded.split('\n') if e.strip()]
        elif input_type == 'list':
            emails = input_data if isinstance(input_data, list) else [input_data]
        elif input_type == 'text':
            emails = [e.strip() for e in input_data.split('\n') if e.strip()]
        else:
            raise ValueError('Invalid input_type. Use: file, list, or text')
        
        logger.info(f"Extracted {len(emails)} emails")
        return emails
    
    def transform(self, emails: list, new_domain: str) -> Dict[str, Any]:
        """Transform emails using domain service."""
        logger.info(f"Transforming {len(emails)} emails to domain {new_domain}")
        result = self.service.transform_emails(emails, new_domain)
        logger.info(f"Transformed {result['processed']}/{result['total']} emails successfully")
        return result
    
    def generate(self, result: Dict[str, Any], output_type: str = 'json') -> Dict[str, Any]:
        """Generate output in specified format."""
        results = []
        for email in result['emails']:
            results.append({
                'nombre': email.nombre,
                'apellido': email.apellido,
                'correo_original': email.correo_original,
                'correo_nuevo': str(email)
            })
        
        response_data = {
            'success': True,
            'processed': result['processed'],
            'total': result['total'],
            'results': results
        }
        
        if output_type == 'csv':
            csv_lines = ['Nombre,Apellido,Correo Original,Correo Nuevo']
            for r in results:
                csv_lines.append(f"{r['nombre']},{r['apellido']},{r['correo_original']},{r['correo_nuevo']}")
            response_data['csv'] = '\n'.join(csv_lines)
        
        return response_data
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process complete pipeline: extract -> transform -> generate."""
        new_domain = data.get('new_domain')
        if not new_domain:
            raise ValueError('Missing required field: new_domain')
        
        output_type = data.get('output_type', 'json')
        
        # Extract
        emails = self.extract(data)
        
        # Transform
        result = self.transform(emails, new_domain)
        
        # Generate
        return self.generate(result, output_type)
