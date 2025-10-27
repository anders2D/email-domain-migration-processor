import logging
import time
from typing import Union, List
from src.features.email_processing.domain.email_service import EmailProcessingService
from src.features.email_processing.adapters.output.file_adapter import FileEmailRepository
from src.features.email_processing.adapters.output.csv_adapter import CsvEmailWriter
from src.shared.validation_adapter import RegexEmailValidator
from src.shared.logging_adapter import PythonLogger
from src.shared.error_logger import ErrorLogger
from src.shared.summary_generator import SummaryGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EmailProcessingCLI:
    """
    CLI for email processing.
    
    Usage:
        python main.py --input-type file --input emails.txt --new-domain company.com --output-type csv --output result.csv
        python main.py --input-type list --input "email1,email2" --new-domain company.com --output-type inline
        python main.py --input-type text --input "email1\nemail2" --new-domain company.com --output-type silent
    
    Input types: file, list, text
    Output types: csv, json, inline, silent
    """
    
    def __init__(self):
        # Dependency Injection
        self.validator = RegexEmailValidator()
        self.logger = PythonLogger("cli")
        self.service = EmailProcessingService(self.validator, self.logger)
    
    @staticmethod
    def show_usage():
        print("""
╔══════════════════════════════════════════════════════════════╗
║           EMAIL PROCESSOR - HEXAGONAL ARCHITECTURE           ║
╚══════════════════════════════════════════════════════════════╝

USAGE:
  python main.py [OPTIONS]

INPUT OPTIONS:
  --input-type    Type: file, list, text (default: file)
  --input         Input data (file path, list, or text)

TRANSFORM OPTIONS:
  --new-domain    New domain for emails (required)

OUTPUT OPTIONS:
  --output-type   Type: csv, json, inline, silent (default: csv)
  --output        Output file path (required for csv/json)

EXAMPLES:
  # From file to CSV
  python main.py --input-type file --input emails.txt --new-domain company.com --output-type csv --output result.csv
  
  # From list to inline
  python main.py --input-type list --input "a@x.com,b@y.com" --new-domain new.com --output-type inline
  
  # Silent mode (no output)
  python main.py --input-type text --input "a@x.com\\nb@y.com" --new-domain new.com --output-type silent
        """)
    
    @staticmethod
    def extract(input_data: Union[str, List[str]], input_type: str = 'file') -> List[str]:
        logger.info(f"Extracting emails from {input_type}")
        
        if input_type == 'file':
            emails = FileEmailRepository().read(input_data)
        elif input_type == 'list':
            emails = input_data.split(',') if isinstance(input_data, str) else input_data
        elif input_type == 'text':
            emails = [e.strip() for e in input_data.split('\n') if e.strip()]
        else:
            raise ValueError(f"Invalid input_type: {input_type}")
        
        logger.info(f"Extracted {len(emails)} emails")
        return emails
    
    def transform(self, emails: list, new_domain: str, error_logger: ErrorLogger = None) -> list:
        logger.info(f"Transforming {len(emails)} emails to domain {new_domain}")
        
        if error_logger is None:
            error_logger = ErrorLogger()
        
        # Use domain service
        result = self.service.transform_emails(emails, new_domain)
        
        transformed = []
        for email in result['emails']:
            transformed.append({
                'original': email.correo_original,
                'transformed': str(email),
                'valid': True
            })
        
        for error in result['error_details']:
            error_msg = error['error']
            # Extraer código de regla y descripción
            if ':' in error_msg:
                parts = error_msg.split(':', 1)
                rule = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else error_msg
            else:
                rule = 'UNKNOWN'
                description = error_msg
            error_logger.log_error(error['email'], rule, description)
            transformed.append({
                'original': error['email'],
                'valid': False,
                'error': error_msg
            })
        
        logger.info(f"Transformed {result['processed']}/{result['total']} emails successfully")
        return transformed
    
    def generate(self, transformed: list, output_type: str = 'csv', output_file: str = None):
        logger.info(f"Generating {len(transformed)} items in {output_type} format")
        
        if output_type == 'csv':
            if not output_file:
                raise ValueError("output_file required for csv")
            # Convert to Email objects
            email_objects = []
            for item in transformed:
                if item.get('valid'):
                    from src.features.email_processing.domain.email import Email
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
            CsvEmailWriter().write(email_objects, output_file)
            print(f"[OK] Saved to {output_file}")
            return len(email_objects)
        
        elif output_type == 'json':
            if not output_file:
                raise ValueError("output_file required for json")
            # Convert to Email objects
            email_objects = []
            for item in transformed:
                if item.get('valid'):
                    from src.features.email_processing.domain.email import Email
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
            from src.features.email_processing.adapters.output.json_adapter import JsonEmailWriter
            JsonEmailWriter().save_emails(email_objects, output_file)
            print(f"[OK] Saved to {output_file}")
            return len(email_objects)
        
        elif output_type == 'inline':
            emails = [item['transformed'] for item in transformed if item.get('valid')]
            for email in emails:
                print(email)
            return len(emails)
        
        elif output_type == 'silent':
            emails = [item['transformed'] for item in transformed if item.get('valid')]
            return len(emails)
        
        else:
            raise ValueError(f"Invalid output_type: {output_type}")
    
    def run(self, config: dict):
        start_time = time.time()
        error_logger = ErrorLogger()
        
        try:
            # Extract
            emails = self.extract(config['input'], config.get('input_type', 'file'))
            
            # Validar archivo vacío
            if len(emails) == 0:
                error_logger.log_warning("N/A", "Archivo de entrada vacío")
                logger.warning("Archivo de entrada vacío")
            
            # Transform
            transformed = self.transform(emails, config['new_domain'], error_logger)
            
            # Generate
            count = self.generate(transformed, config.get('output_type', 'csv'), config.get('output_file'))
            
            # Guardar error log
            error_logger.save()
            
            # Generar resumen
            duration = time.time() - start_time
            valid = sum(1 for t in transformed if t.get('valid'))
            stats = {
                'total': len(emails),
                'processed': valid,
                'errors': error_logger.get_error_count(),
                'duplicates': error_logger.get_warning_count(),
                'warnings': error_logger.get_warning_count(),
                'success_rate': (valid / len(emails) * 100) if emails else 0,
                'duration': f"{duration:.2f}s",
                'output_file': config.get('output_file', 'N/A'),
                'error_log': 'error_log.txt',
                'new_domain': config['new_domain']
            }
            
            SummaryGenerator.generate(stats)
            
            logger.info(f"Processed {valid}/{len(emails)} emails successfully")
            
            if config.get('output_type') != 'silent':
                print(f"\n[OK] Processed {valid}/{len(emails)} emails")
                print(f"[OK] Error log: error_log.txt")
                print(f"[OK] Summary: summary.txt")
        
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"[ERROR] {e}")
            raise
