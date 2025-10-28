"""
Tests Unitarios - EmailProcessingAPI (Input Adapter)
Cobertura de API REST para procesamiento de emails
"""
import pytest
import json
from src.features.email_processing.adapters.input.api_adapter import EmailProcessingAPI


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def api_adapter():
    """Crea instancia de API adapter para tests"""
    return EmailProcessingAPI()


@pytest.fixture
def client(api_adapter):
    """Crea cliente de test de Flask"""
    api_adapter.app.config['TESTING'] = True
    return api_adapter.app.test_client()


@pytest.fixture
def valid_emails():
    """Lista de emails válidos para tests"""
    return ['juan.perez@old.com', 'maria.garcia@old.com']


@pytest.fixture
def invalid_emails():
    """Lista de emails inválidos para tests"""
    return ['invalid', 'no-dot@old.com', 'user@@old.com']


# ============================================================================
# Tests de Inicialización
# ============================================================================

def test_api_adapter_init():
    """APIAdapter: __init__() inicializa Flask app y dependencias"""
    # Arrange & Act
    api = EmailProcessingAPI()
    
    # Assert
    assert api.app is not None
    assert api.validator is not None
    assert api.logger is not None
    assert api.service is not None


def test_api_adapter_routes_registered(api_adapter):
    """APIAdapter: __init__() registra todas las rutas necesarias"""
    # Arrange
    expected_routes = ['/validate', '/extract', '/transform', '/generate']
    
    # Act
    registered_routes = [rule.rule for rule in api_adapter.app.url_map.iter_rules() if rule.rule != '/static/<path:filename>']
    
    # Assert
    for route in expected_routes:
        assert route in registered_routes


# ============================================================================
# Tests de /validate endpoint
# ============================================================================

def test_api_validate_valid_email(client):
    """APIAdapter: POST /validate con email válido retorna valid=True"""
    # Arrange
    payload = {'email': 'juan.perez@example.com'}
    
    # Act
    response = client.post('/validate', 
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['valid'] is True
    assert data['email'] == 'juan.perez@example.com'


def test_api_validate_invalid_email(client):
    """APIAdapter: POST /validate con email inválido retorna valid=False"""
    # Arrange
    payload = {'email': 'invalid'}
    
    # Act
    response = client.post('/validate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['valid'] is False
    assert 'error' in data


def test_api_validate_missing_email(client):
    """APIAdapter: POST /validate sin campo 'email' retorna error 400"""
    # Arrange
    payload = {}
    
    # Act
    response = client.post('/validate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_api_validate_empty_email(client):
    """APIAdapter: POST /validate con email vacío retorna error 400"""
    # Arrange
    payload = {'email': ''}
    
    # Act
    response = client.post('/validate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 400


# ============================================================================
# Tests de /extract endpoint
# ============================================================================

def test_api_extract_from_list(client, valid_emails):
    """APIAdapter: POST /extract con input_type='list' retorna emails"""
    # Arrange
    payload = {
        'input_type': 'list',
        'input': valid_emails
    }
    
    # Act
    response = client.post('/extract',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['count'] == 2
    assert data['emails'] == valid_emails


def test_api_extract_from_text(client):
    """APIAdapter: POST /extract con input_type='text' separa por líneas"""
    # Arrange
    payload = {
        'input_type': 'text',
        'input': 'juan.perez@old.com\nmaria.garcia@old.com'
    }
    
    # Act
    response = client.post('/extract',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['count'] == 2
    assert len(data['emails']) == 2


def test_api_extract_empty_list(client):
    """APIAdapter: POST /extract con lista vacía retorna count=0"""
    # Arrange
    payload = {
        'input_type': 'list',
        'input': []
    }
    
    # Act
    response = client.post('/extract',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['count'] == 0


def test_api_extract_invalid_input_type(client):
    """APIAdapter: POST /extract con input_type inválido retorna error 400"""
    # Arrange
    payload = {
        'input_type': 'invalid',
        'input': []
    }
    
    # Act
    response = client.post('/extract',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_api_extract_missing_input(client):
    """APIAdapter: POST /extract sin campo 'input' retorna error 400"""
    # Arrange
    payload = {'input_type': 'list'}
    
    # Act
    response = client.post('/extract',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 400


# ============================================================================
# Tests de /transform endpoint
# ============================================================================

def test_api_transform_valid_emails(client, valid_emails):
    """APIAdapter: POST /transform con emails válidos retorna transformados"""
    # Arrange
    payload = {
        'emails': valid_emails,
        'new_domain': 'company.com'
    }
    
    # Act
    response = client.post('/transform',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total'] == 2
    assert data['valid'] == 2
    assert len(data['transformed']) == 2


def test_api_transform_single_email(client):
    """APIAdapter: POST /transform con un email válido"""
    # Arrange
    payload = {
        'emails': ['juan.perez@old.com'],
        'new_domain': 'new.com'
    }
    
    # Act
    response = client.post('/transform',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total'] == 1
    assert data['valid'] == 1


def test_api_transform_invalid_emails(client, invalid_emails):
    """APIAdapter: POST /transform con emails inválidos retorna valid=0"""
    # Arrange
    payload = {
        'emails': invalid_emails,
        'new_domain': 'company.com'
    }
    
    # Act
    response = client.post('/transform',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total'] == 3
    assert data['valid'] == 0


def test_api_transform_mixed_valid_invalid(client):
    """APIAdapter: POST /transform con mezcla procesa solo válidos"""
    # Arrange
    payload = {
        'emails': ['juan.perez@old.com', 'invalid', 'maria.garcia@old.com'],
        'new_domain': 'company.com'
    }
    
    # Act
    response = client.post('/transform',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total'] == 3
    assert data['valid'] == 2


def test_api_transform_empty_list(client):
    """APIAdapter: POST /transform con lista vacía retorna total=0"""
    # Arrange
    payload = {
        'emails': [],
        'new_domain': 'company.com'
    }
    
    # Act
    response = client.post('/transform',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total'] == 0
    assert data['valid'] == 0


def test_api_transform_missing_emails(client):
    """APIAdapter: POST /transform sin campo 'emails' retorna error 400"""
    # Arrange
    payload = {'new_domain': 'company.com'}
    
    # Act
    response = client.post('/transform',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 400


def test_api_transform_missing_domain(client):
    """APIAdapter: POST /transform sin 'new_domain' retorna error 400"""
    # Arrange
    payload = {'emails': ['juan.perez@old.com']}
    
    # Act
    response = client.post('/transform',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 400


def test_api_transform_response_structure(client):
    """APIAdapter: POST /transform retorna estructura correcta"""
    # Arrange
    payload = {
        'emails': ['juan.perez@old.com'],
        'new_domain': 'company.com'
    }
    
    # Act
    response = client.post('/transform',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    data = json.loads(response.data)
    assert 'transformed' in data
    assert 'valid' in data
    assert 'total' in data
    assert isinstance(data['transformed'], list)


# ============================================================================
# Tests de /generate endpoint
# ============================================================================

def test_api_generate_csv_format(client):
    """APIAdapter: POST /generate con output_type='csv' retorna CSV"""
    # Arrange
    payload = {
        'transformed': [
            {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True}
        ],
        'output_type': 'csv'
    }
    
    # Act
    response = client.post('/generate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['format'] == 'csv'
    assert 'content' in data


def test_api_generate_json_format(client):
    """APIAdapter: POST /generate con output_type='json' retorna JSON"""
    # Arrange
    payload = {
        'transformed': [
            {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True}
        ],
        'output_type': 'json'
    }
    
    # Act
    response = client.post('/generate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['format'] == 'json'


def test_api_generate_inline_format(client):
    """APIAdapter: POST /generate con output_type='inline' retorna lista"""
    # Arrange
    payload = {
        'transformed': [
            {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True}
        ],
        'output_type': 'inline'
    }
    
    # Act
    response = client.post('/generate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'emails' in data
    assert isinstance(data['emails'], list)


def test_api_generate_silent_format(client):
    """APIAdapter: POST /generate con output_type='silent' retorna count"""
    # Arrange
    payload = {
        'transformed': [
            {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True}
        ],
        'output_type': 'silent'
    }
    
    # Act
    response = client.post('/generate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'count' in data
    assert data['count'] == 1


def test_api_generate_invalid_output_type(client):
    """APIAdapter: POST /generate con output_type inválido retorna error 400"""
    # Arrange
    payload = {
        'transformed': [],
        'output_type': 'invalid'
    }
    
    # Act
    response = client.post('/generate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 400


def test_api_generate_empty_transformed(client):
    """APIAdapter: POST /generate con lista vacía retorna count=0"""
    # Arrange
    payload = {
        'transformed': [],
        'output_type': 'inline'
    }
    
    # Act
    response = client.post('/generate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['count'] == 0


def test_api_generate_default_output_type(client):
    """APIAdapter: POST /generate sin output_type usa 'inline' por defecto"""
    # Arrange
    payload = {
        'transformed': [
            {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True}
        ]
    }
    
    # Act
    response = client.post('/generate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'emails' in data


# ============================================================================
# Tests de Integración de Flujo Completo
# ============================================================================

def test_api_complete_flow_extract_transform_generate(client):
    """APIAdapter: Flujo completo extract -> transform -> generate"""
    # Arrange - Extract
    extract_payload = {
        'input_type': 'list',
        'input': ['juan.perez@old.com']
    }
    
    # Act - Extract
    extract_response = client.post('/extract',
                                   data=json.dumps(extract_payload),
                                   content_type='application/json')
    extract_data = json.loads(extract_response.data)
    
    # Arrange - Transform
    transform_payload = {
        'emails': extract_data['emails'],
        'new_domain': 'company.com'
    }
    
    # Act - Transform
    transform_response = client.post('/transform',
                                     data=json.dumps(transform_payload),
                                     content_type='application/json')
    transform_data = json.loads(transform_response.data)
    
    # Arrange - Generate
    generate_payload = {
        'transformed': transform_data['transformed'],
        'output_type': 'inline'
    }
    
    # Act - Generate
    generate_response = client.post('/generate',
                                    data=json.dumps(generate_payload),
                                    content_type='application/json')
    
    # Assert
    assert extract_response.status_code == 200
    assert transform_response.status_code == 200
    assert generate_response.status_code == 200
    generate_data = json.loads(generate_response.data)
    assert generate_data['count'] == 1
