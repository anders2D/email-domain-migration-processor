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
        
        if '/extract' in path:
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
        
        # Filter valid emails
        valid_items = [item for item in transformed if item.get('valid', True)]
        
        if output_type == 'inline':
            return response(200, {'data': valid_items, 'count': len(valid_items)})
        elif output_type == 'csv':
            csv_lines = ['Nombre,Apellido,Correo Original,Correo Nuevo']
            for item in valid_items:
                csv_lines.append(f"{item['nombre']},{item['apellido']},{item['correo_original']},{item['correo_nuevo']}")
            return response(200, {'output': '\n'.join(csv_lines), 'format': 'csv', 'count': len(valid_items)})
        elif output_type == 'json':
            return response(200, {'data': valid_items, 'format': 'json', 'count': len(valid_items)})
        elif output_type == 'silent':
            return response(200, {'count': len(valid_items), 'status': 'processed'})
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
