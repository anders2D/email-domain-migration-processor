from typing import List, Dict
from src.features.email_processing.domain.email import Email
from src.features.email_processing.domain.ports import EmailValidator, Logger


class EmailProcessingService:
    """Core business logic - Stateless service."""
    
    def __init__(self, validator: EmailValidator, logger: Logger):
        self._validator = validator
        self._logger = logger
    
    def transform_emails(self, raw_emails: List[str], new_domain: str) -> Dict:
        """Transform emails applying BR-001 to BR-005 and TR-001 to TR-005."""
        self._logger.info(f"Transforming {len(raw_emails)} emails to domain {new_domain}")
        
        # Validar dominio destino
        if not self._validator.validate_domain(new_domain):
            raise ValueError(f"Invalid target domain: {new_domain}")
        
        processed = []
        errors = []
        seen = set()
        
        for i, raw_email in enumerate(raw_emails, 1):
            raw_email = raw_email.strip()
            
            # Detectar duplicados
            if raw_email in seen:
                self._logger.warning(f"Duplicate email: {raw_email}")
                errors.append({'email': raw_email, 'error': 'Duplicate'})
                continue
            seen.add(raw_email)
            
            # Validar y transformar
            try:
                nombre, apellido = self._validator.validate_and_parse(raw_email)
                email = Email.create(nombre, apellido, raw_email, new_domain)
                processed.append(email)
                
                if i % 10 == 0:
                    self._logger.info(f"Processed {i}/{len(raw_emails)} emails")
            except ValueError as e:
                self._logger.warning(f"Validation failed for {raw_email}: {e}")
                errors.append({'email': raw_email, 'error': str(e)})
        
        stats = {
            'total': len(raw_emails),
            'processed': len(processed),
            'errors': len(errors),
            'success_rate': (len(processed) / len(raw_emails)) * 100 if raw_emails else 0,
            'emails': processed,
            'error_details': errors
        }
        
        self._logger.info(f"Transformation completed: {stats['processed']}/{stats['total']} ({stats['success_rate']:.1f}%)")
        return stats