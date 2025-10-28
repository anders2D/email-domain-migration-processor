from flask import Flask, request, jsonify
import logging
import json
from src.features.email_processing.domain.email_service import EmailProcessingService
from src.features.email_processing.adapters.output.file_adapter import FileEmailRepository
from src.shared.validation_adapter import RegexEmailValidator
from src.shared.logging_adapter import PythonLogger

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EmailProcessingAPI:
    def __init__(self):
        self.app = Flask(__name__)
        # Dependency Injection
        self.validator = RegexEmailValidator()
        self.logger = PythonLogger("api")
        self.service = EmailProcessingService(self.validator, self.logger)
        self._setup_routes()
    
    def _setup_routes(self):
        @self.app.route('/validate', methods=['POST'])
        def validate():
            """
            Validate a single email.
            Body: {"email": "juan.perez@example.com"}
            """
            try:
                data = request.json
                email = data.get('email')
                if not email:
                    return jsonify({'error': 'Missing required field: email'}), 400
                
                try:
                    self.validator.validate_and_parse(email)
                    return jsonify({'valid': True, 'email': email})
                except Exception as e:
                    return jsonify({'valid': False, 'email': email, 'error': str(e)})
            except Exception as e:
                logger.error(f"Validate error: {e}")
                return jsonify({'error': str(e)}), 400
        
        @self.app.route('/extract', methods=['POST'])
        def extract():
            """
            Extract emails from input source.
            Body: {
                "input_type": "file|list|text",
                "input": "path/to/file.txt" | ["email1", "email2"] | "email1\nemail2"
            }
            """
            try:
                data = request.json
                input_type = data.get('input_type', 'file')
                input_data = data['input']
                
                logger.info(f"Extracting emails from {input_type}")
                
                if input_type == 'file':
                    repository = FileEmailRepository()
                    emails = repository.read(input_data)
                elif input_type == 'list':
                    emails = input_data
                elif input_type == 'text':
                    emails = [e.strip() for e in input_data.split('\n') if e.strip()]
                else:
                    return jsonify({'error': 'Invalid input_type. Use: file, list, or text'}), 400
                
                logger.info(f"Extracted {len(emails)} emails")
                return jsonify({'emails': emails, 'count': len(emails)})
            except Exception as e:
                logger.error(f"Extract error: {e}")
                return jsonify({'error': str(e)}), 400
        
        @self.app.route('/transform', methods=['POST'])
        def transform():
            """
            Transform emails with new domain.
            Body: {
                "emails": ["email1", "email2"],
                "new_domain": "company.com"
            }
            """
            try:
                data = request.json
                emails = data['emails']
                new_domain = data['new_domain']
                
                logger.info(f"Transforming {len(emails)} emails to domain {new_domain}")
                
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
                    transformed.append({
                        'original': error['email'],
                        'valid': False,
                        'error': error['error']
                    })
                
                logger.info(f"Transformed {result['processed']}/{result['total']} emails successfully")
                return jsonify({'transformed': transformed, 'valid': result['processed'], 'total': result['total']})
            except Exception as e:
                logger.error(f"Transform error: {e}")
                return jsonify({'error': str(e)}), 400
        
        @self.app.route('/generate', methods=['POST'])
        def generate():
            """
            Generate output in specified format.
            Body: {
                "transformed": [{"transformed": "email", "valid": true}],
                "output_type": "csv|json|inline|silent"
            }
            """
            try:
                data = request.json
                transformed = data['transformed']
                output_type = data.get('output_type', 'inline')
                
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
                
                logger.info(f"Generating {len(email_objects)} emails in {output_type} format")
                
                if output_type == 'csv':
                    from src.features.email_processing.adapters.output.csv_adapter import CsvFormatter
                    content = CsvFormatter().format(email_objects)
                    return jsonify({'content': content, 'format': 'csv', 'count': len(email_objects)})
                
                elif output_type == 'json':
                    from src.features.email_processing.adapters.output.json_adapter import JsonFormatter
                    content = JsonFormatter().format(email_objects)
                    return jsonify({'content': content, 'format': 'json', 'count': len(email_objects)})
                
                elif output_type == 'inline':
                    from src.features.email_processing.domain.output_service import OutputService
                    emails = OutputService.generate_inline(email_objects)
                    return jsonify({'emails': emails, 'count': len(emails)})
                
                elif output_type == 'silent':
                    from src.features.email_processing.domain.output_service import OutputService
                    count = OutputService.generate_silent(email_objects)
                    logger.info(f"Silent mode: {count} emails processed")
                    return jsonify({'count': count})
                
                else:
                    return jsonify({'error': 'Invalid output_type. Use: csv, json, inline, or silent'}), 400
                    
            except Exception as e:
                logger.error(f"Generate error: {e}")
                return jsonify({'error': str(e)}), 400
    
    def run(self, host='localhost', port=5000):
        """Run Flask server locally."""
        logger.info(f"Starting API server on {host}:{port}")
        self.app.run(host=host, port=port)


