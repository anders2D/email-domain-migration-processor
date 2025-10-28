import sys
import os
import json
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.features.email_processing.adapters.input.lambda_adapter import EmailProcessingLambda

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# API Key from environment
API_KEY = os.environ.get('API_KEY', 'dev-key-12345')

# Lambda adapter instance (Hexagonal Architecture)
lambda_adapter = EmailProcessingLambda()

def validate_api_key(event):
    headers = event.get('headers', {})
    api_key = headers.get('x-api-key') or headers.get('X-Api-Key')
    return api_key == API_KEY

def handler(event, context):
    try:
        logger.info(f"Event: {json.dumps(event)}")
        
        # Validate API Key
        if not validate_api_key(event):
            logger.warning("Unauthorized: Invalid or missing API key")
            return response(401, {'error': 'Unauthorized: Invalid or missing API key'})
        
        path = event.get('rawPath', event.get('path', ''))
        body = json.loads(event.get('body', '{}'))
        
        if '/validate' in path:
            return validate_email(body)
        elif '/extract' in path:
            return extract(body)
        elif '/transform' in path:
            return transform(body)
        elif '/generate' in path:
            return generate(body)
        else:
            return response(404, {'error': 'Not found'})
    
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return response(500, {'error': str(e)})

def validate_email(data):
    try:
        email = data.get('email')
        if not email:
            return response(400, {'error': 'Missing required field: email'})
        
        try:
            lambda_adapter.validator.validate_and_parse(email)
            return response(200, {'valid': True, 'email': email})
        except Exception as e:
            return response(200, {'valid': False, 'email': email, 'error': str(e)})
    except Exception as e:
        logger.error(f"Validate error: {e}", exc_info=True)
        return response(500, {'error': f'Internal server error: {str(e)}'})


def extract(data):
    try:
        emails = lambda_adapter.extract(data)
        return response(200, {'emails': emails, 'count': len(emails)})
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return response(400, {'error': str(e)})
    except Exception as e:
        logger.error(f"Extract error: {e}", exc_info=True)
        return response(500, {'error': f'Internal server error: {str(e)}'})

def transform(data):
    try:
        emails = data.get('emails', [])
        new_domain = data.get('new_domain')
        
        if not new_domain:
            return response(400, {'error': 'Missing required field: new_domain'})
        if not emails:
            return response(400, {'error': 'Missing required field: emails'})
        
        result = lambda_adapter.transform(emails, new_domain)
        
        # Format for next step
        transformed = []
        for email in result['emails']:
            transformed.append({
                'nombre': email.nombre,
                'apellido': email.apellido,
                'correo_original': email.correo_original,
                'correo_nuevo': str(email),
                'valid': True
            })
        
        return response(200, {
            'transformed': transformed,
            'valid': result['processed'],
            'total': result['total']
        })
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return response(400, {'error': str(e)})
    except Exception as e:
        logger.error(f"Transform error: {e}", exc_info=True)
        return response(500, {'error': f'Internal server error: {str(e)}'})

def generate(data):
    try:
        transformed = data.get('transformed', [])
        output_type = data.get('output_type', 'inline')
        
        if not transformed:
            return response(400, {'error': 'Missing required field: transformed'})
        
        # Convert to Email objects
        from src.features.email_processing.domain.email import Email
        email_objects = []
        for item in transformed:
            if item.get('valid', True):
                email_obj = Email.create(
                    nombre=item['nombre'],
                    apellido=item['apellido'],
                    correo_original=item['correo_original'],
                    nuevo_dominio=item['correo_nuevo'].split('@')[1]
                )
                email_objects.append(email_obj)
        
        if output_type == 'inline':
            from src.features.email_processing.domain.output_service import OutputService
            emails = OutputService.generate_inline(email_objects)
            return response(200, {'emails': emails, 'count': len(emails)})
        elif output_type == 'csv':
            from src.features.email_processing.adapters.output.csv_adapter import CsvFormatter
            content = CsvFormatter().format(email_objects)
            return response(200, {'content': content, 'format': 'csv', 'count': len(email_objects)})
        elif output_type == 'json':
            from src.features.email_processing.adapters.output.json_adapter import JsonFormatter
            content = JsonFormatter().format(email_objects)
            return response(200, {'content': content, 'format': 'json', 'count': len(email_objects)})
        elif output_type == 'silent':
            from src.features.email_processing.domain.output_service import OutputService
            count = OutputService.generate_silent(email_objects)
            return response(200, {'count': count})
        else:
            return response(400, {'error': f'Invalid output_type: {output_type}'})
    except Exception as e:
        logger.error(f"Generate error: {e}", exc_info=True)
        return response(500, {'error': f'Internal server error: {str(e)}'})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }
