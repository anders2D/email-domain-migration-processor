"""
Tests Unitarios - EmailProcessingLibrary (Input Adapter)
Cobertura de uso como librería Python
"""
import pytest
import tempfile
import os
from src.features.email_processing.adapters.input.library_adapter import EmailProcessingLibrary


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def temp_file():
    """Crea archivo temporal para tests"""
    fd, path = tempfile.mkstemp(suffix='.txt')
    os.close(fd)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('juan.perez@old.com\nmaria.garcia@old.com\n')
    yield path
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def temp_output():
    """Crea path para archivo de salida temporal"""
    fd, path = tempfile.mkstemp(suffix='.csv')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def valid_emails():
    """Lista de emails válidos"""
    return ['juan.perez@old.com', 'maria.garcia@old.com']


@pytest.fixture
def invalid_emails():
    """Lista de emails inválidos"""
    return ['invalid', 'no-dot@old.com']


# ============================================================================
# Tests de extract()
# ============================================================================

def test_library_extract_from_file(temp_file):
    """LibraryAdapter: extract() con input_type='file' lee archivo"""
    # Arrange
    input_type = 'file'
    
    # Act
    result = EmailProcessingLibrary.extract(temp_file, input_type)
    
    # Assert
    assert isinstance(result, list)
    assert len(result) == 2


def test_library_extract_from_list(valid_emails):
    """LibraryAdapter: extract() con input_type='list' retorna lista"""
    # Arrange
    input_type = 'list'
    
    # Act
    result = EmailProcessingLibrary.extract(valid_emails, input_type)
    
    # Assert
    assert result == valid_emails


def test_library_extract_from_text():
    """LibraryAdapter: extract() con input_type='text' separa por líneas"""
    # Arrange
    text = 'juan.perez@old.com\nmaria.garcia@old.com'
    input_type = 'text'
    
    # Act
    result = EmailProcessingLibrary.extract(text, input_type)
    
    # Assert
    assert len(result) == 2
    assert 'juan.perez@old.com' in result


def test_library_extract_empty_text():
    """LibraryAdapter: extract() con texto vacío retorna lista vacía"""
    # Arrange
    text = ''
    input_type = 'text'
    
    # Act
    result = EmailProcessingLibrary.extract(text, input_type)
    
    # Assert
    assert result == []


def test_library_extract_invalid_type():
    """LibraryAdapter: extract() con input_type inválido lanza ValueError"""
    # Arrange
    input_data = []
    input_type = 'invalid'
    
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid input_type"):
        EmailProcessingLibrary.extract(input_data, input_type)


def test_library_extract_default_type(temp_file):
    """LibraryAdapter: extract() usa 'file' por defecto"""
    # Arrange & Act
    result = EmailProcessingLibrary.extract(temp_file)
    
    # Assert
    assert isinstance(result, list)


# ============================================================================
# Tests de transform()
# ============================================================================

def test_library_transform_valid_emails(valid_emails):
    """LibraryAdapter: transform() con emails válidos retorna transformados"""
    # Arrange
    new_domain = 'company.com'
    
    # Act
    result = EmailProcessingLibrary.transform(valid_emails, new_domain)
    
    # Assert
    assert len(result) == 2
    assert all(item['valid'] for item in result)


def test_library_transform_single_email():
    """LibraryAdapter: transform() con un email válido"""
    # Arrange
    emails = ['juan.perez@old.com']
    new_domain = 'new.com'
    
    # Act
    result = EmailProcessingLibrary.transform(emails, new_domain)
    
    # Assert
    assert len(result) == 1
    assert result[0]['valid'] is True
    assert result[0]['transformed'] == 'juan.perez@new.com'


def test_library_transform_invalid_emails(invalid_emails):
    """LibraryAdapter: transform() con emails inválidos retorna valid=False"""
    # Arrange
    new_domain = 'company.com'
    
    # Act
    result = EmailProcessingLibrary.transform(invalid_emails, new_domain)
    
    # Assert
    assert len(result) == 2
    assert all(not item['valid'] for item in result)
    assert all('error' in item for item in result)


def test_library_transform_mixed_valid_invalid():
    """LibraryAdapter: transform() con mezcla procesa ambos"""
    # Arrange
    emails = ['juan.perez@old.com', 'invalid', 'maria.garcia@old.com']
    new_domain = 'company.com'
    
    # Act
    result = EmailProcessingLibrary.transform(emails, new_domain)
    
    # Assert
    assert len(result) == 3
    valid_count = sum(1 for item in result if item['valid'])
    assert valid_count == 2


def test_library_transform_empty_list():
    """LibraryAdapter: transform() con lista vacía retorna lista vacía"""
    # Arrange
    emails = []
    new_domain = 'company.com'
    
    # Act
    result = EmailProcessingLibrary.transform(emails, new_domain)
    
    # Assert
    assert result == []


def test_library_transform_response_structure():
    """LibraryAdapter: transform() retorna estructura correcta"""
    # Arrange
    emails = ['juan.perez@old.com']
    new_domain = 'company.com'
    
    # Act
    result = EmailProcessingLibrary.transform(emails, new_domain)
    
    # Assert
    assert 'original' in result[0]
    assert 'transformed' in result[0]
    assert 'valid' in result[0]


def test_library_transform_with_logging():
    """LibraryAdapter: transform() con enable_logging=True genera log"""
    # Arrange
    emails = ['invalid']
    new_domain = 'company.com'
    
    # Act
    result = EmailProcessingLibrary.transform(emails, new_domain, enable_logging=True)
    
    # Assert
    assert len(result) == 1
    assert os.path.exists('error_log.txt')
    
    # Cleanup
    if os.path.exists('error_log.txt'):
        os.unlink('error_log.txt')


# ============================================================================
# Tests de generate()
# ============================================================================

def test_library_generate_csv(temp_output):
    """LibraryAdapter: generate() con output_type='csv' crea archivo"""
    # Arrange
    transformed = [
        {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True}
    ]
    
    # Act
    result = EmailProcessingLibrary.generate(transformed, 'csv', temp_output)
    
    # Assert
    assert result == 1
    assert os.path.exists(temp_output)


def test_library_generate_json(temp_output):
    """LibraryAdapter: generate() con output_type='json' crea archivo"""
    # Arrange
    transformed = [
        {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True}
    ]
    output_file = temp_output.replace('.csv', '.json')
    
    # Act
    result = EmailProcessingLibrary.generate(transformed, 'json', output_file)
    
    # Assert
    assert result == 1
    assert os.path.exists(output_file)
    
    # Cleanup
    if os.path.exists(output_file):
        os.unlink(output_file)


def test_library_generate_inline():
    """LibraryAdapter: generate() con output_type='inline' retorna lista"""
    # Arrange
    transformed = [
        {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True},
        {'original': 'maria.garcia@old.com', 'transformed': 'maria.garcia@new.com', 'valid': True}
    ]
    
    # Act
    result = EmailProcessingLibrary.generate(transformed, 'inline')
    
    # Assert
    assert isinstance(result, list)
    assert len(result) == 2


def test_library_generate_silent():
    """LibraryAdapter: generate() con output_type='silent' retorna count"""
    # Arrange
    transformed = [
        {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True}
    ]
    
    # Act
    result = EmailProcessingLibrary.generate(transformed, 'silent')
    
    # Assert
    assert result == 1


def test_library_generate_csv_missing_file():
    """LibraryAdapter: generate() CSV sin output_file lanza ValueError"""
    # Arrange
    transformed = [
        {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True}
    ]
    
    # Act & Assert
    with pytest.raises(ValueError, match="output_file required"):
        EmailProcessingLibrary.generate(transformed, 'csv')


def test_library_generate_json_missing_file():
    """LibraryAdapter: generate() JSON sin output_file lanza ValueError"""
    # Arrange
    transformed = [
        {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True}
    ]
    
    # Act & Assert
    with pytest.raises(ValueError, match="output_file required"):
        EmailProcessingLibrary.generate(transformed, 'json')


def test_library_generate_invalid_type():
    """LibraryAdapter: generate() con output_type inválido lanza ValueError"""
    # Arrange
    transformed = []
    
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid output_type"):
        EmailProcessingLibrary.generate(transformed, 'invalid')


def test_library_generate_empty_transformed():
    """LibraryAdapter: generate() con lista vacía retorna 0"""
    # Arrange
    transformed = []
    
    # Act
    result = EmailProcessingLibrary.generate(transformed, 'silent')
    
    # Assert
    assert result == 0


def test_library_generate_with_summary(temp_output):
    """LibraryAdapter: generate() con enable_summary=True genera summary.txt"""
    # Arrange
    transformed = [
        {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True}
    ]
    
    # Act
    result = EmailProcessingLibrary.generate(transformed, 'csv', temp_output, enable_summary=True)
    
    # Assert
    assert os.path.exists('summary.txt')
    
    # Cleanup
    if os.path.exists('summary.txt'):
        os.unlink('summary.txt')


def test_library_generate_filters_invalid():
    """LibraryAdapter: generate() filtra emails inválidos"""
    # Arrange
    transformed = [
        {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True},
        {'original': 'invalid', 'valid': False, 'error': 'Invalid format'}
    ]
    
    # Act
    result = EmailProcessingLibrary.generate(transformed, 'inline')
    
    # Assert
    assert len(result) == 1


# ============================================================================
# Tests de validate()
# ============================================================================

def test_library_validate_valid_email():
    """LibraryAdapter: validate() con email válido retorna True"""
    # Arrange
    email = 'juan.perez@example.com'
    
    # Act
    result = EmailProcessingLibrary.validate(email)
    
    # Assert
    assert result is True


def test_library_validate_invalid_email():
    """LibraryAdapter: validate() con email inválido retorna False"""
    # Arrange
    email = 'invalid'
    
    # Act
    result = EmailProcessingLibrary.validate(email)
    
    # Assert
    assert result is False


def test_library_validate_multiple_emails():
    """LibraryAdapter: validate() valida múltiples emails"""
    # Arrange
    emails = ['juan.perez@test.com', 'invalid', 'maria.garcia@test.com']
    
    # Act
    results = [EmailProcessingLibrary.validate(email) for email in emails]
    
    # Assert
    assert results == [True, False, True]


# ============================================================================
# Tests de Flujo Completo
# ============================================================================

def test_library_complete_flow_extract_transform_generate(temp_file, temp_output):
    """LibraryAdapter: Flujo completo extract -> transform -> generate"""
    # Arrange & Act - Extract
    emails = EmailProcessingLibrary.extract(temp_file, 'file')
    
    # Act - Transform
    transformed = EmailProcessingLibrary.transform(emails, 'company.com')
    
    # Act - Generate
    count = EmailProcessingLibrary.generate(transformed, 'csv', temp_output)
    
    # Assert
    assert len(emails) == 2
    assert len(transformed) == 2
    assert count == 2
    assert os.path.exists(temp_output)


def test_library_complete_flow_with_logging_and_summary(temp_file, temp_output):
    """LibraryAdapter: Flujo completo con logging y summary"""
    # Arrange & Act
    emails = EmailProcessingLibrary.extract(temp_file, 'file')
    transformed = EmailProcessingLibrary.transform(emails, 'company.com', enable_logging=True)
    count = EmailProcessingLibrary.generate(transformed, 'csv', temp_output, enable_summary=True)
    
    # Assert
    assert count == 2
    assert os.path.exists(temp_output)
    assert os.path.exists('summary.txt')
    
    # Cleanup
    if os.path.exists('summary.txt'):
        os.unlink('summary.txt')
    if os.path.exists('error_log.txt'):
        os.unlink('error_log.txt')
