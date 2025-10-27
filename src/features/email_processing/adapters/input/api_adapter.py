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
                "output_type": "csv|json|inline|silent",
                "output_file": "path/to/output.csv" (optional for csv/json)
            }
            """
            try:
                data = request.json
                transformed = data['transformed']
                output_type = data.get('output_type', 'csv')
                output_file = data.get('output_file')
                
                emails = [item['transformed'] for item in transformed if item.get('valid')]
                logger.info(f"Generating {len(emails)} emails in {output_type} format")
                
                if output_type == 'csv':
                    if not output_file:
                        return jsonify({'error': 'output_file required for csv'}), 400
                    from src.features.email_processing.adapters.output.csv_adapter import CsvEmailWriter
                    CsvEmailWriter().write(emails, output_file)
                    return jsonify({'output_file': output_file, 'count': len(emails)})
                
                elif output_type == 'json':
                    if not output_file:
                        return jsonify({'error': 'output_file required for json'}), 400
                    from src.features.email_processing.adapters.output.json_adapter import JsonEmailWriter
                    JsonEmailWriter().write(emails, output_file)
                    return jsonify({'output_file': output_file, 'count': len(emails)})
                
                elif output_type == 'inline':
                    return jsonify({'emails': emails, 'count': len(emails)})
                
                elif output_type == 'silent':
                    logger.info(f"Silent mode: {len(emails)} emails processed")
                    return jsonify({'count': len(emails)})
                
                else:
                    return jsonify({'error': 'Invalid output_type. Use: csv, json, inline, or silent'}), 400
                    
            except Exception as e:
                logger.error(f"Generate error: {e}")
                return jsonify({'error': str(e)}), 400
    
    def run(self, host='localhost', port=5000):
        """Run Flask server locally."""
        logger.info(f"Starting API server on {host}:{port}")
        self.app.run(host=host, port=port)


