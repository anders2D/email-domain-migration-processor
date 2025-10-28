"""
Tests Unitarios - EmailProcessingCLI (Input Adapter)
Cobertura de interfaz CLI
"""
import pytest
import tempfile
import os
from src.features.email_processing.adapters.input.cli_adapter import EmailProcessingCLI


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def cli_adapter():
    """Crea instancia de CLI adapter"""
    return EmailProcessingCLI()


@pytest.fixture
def temp_input_file():
    """Crea archivo temporal de entrada"""
    fd, path = tempfile.mkstemp(suffix='.txt')
    os.close(fd)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('juan.perez@old.com\nmaria.garcia@old.com\n')
    yield path
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def temp_output_file():
    """Crea path para archivo de salida"""
    fd, path = tempfile.mkstemp(suffix='.csv')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


# ============================================================================
# Tests de Inicialización
# ============================================================================

def test_cli_adapter_init():
    """CLIAdapter: __init__() inicializa dependencias"""
    # Arrange & Act
    cli = EmailProcessingCLI()
    
    # Assert
    assert cli.validator is not None
    assert cli.logger is not None
    assert cli.service is not None


# ============================================================================
# Tests de extract()
# ============================================================================

def test_cli_extract_from_file(temp_input_file):
    """CLIAdapter: extract() con input_type='file' lee archivo"""
    # Arrange
    input_type = 'file'
    
    # Act
    result = EmailProcessingCLI.extract(temp_input_file, input_type)
    
    # Assert
    assert isinstance(result, list)
    assert len(result) == 2


def test_cli_extract_from_list():
    """CLIAdapter: extract() con input_type='list' separa por comas"""
    # Arrange
    input_data = 'juan.perez@old.com,maria.garcia@old.com'
    input_type = 'list'
    
    # Act
    result = EmailProcessingCLI.extract(input_data, input_type)
    
    # Assert
    assert len(result) == 2


def test_cli_extract_from_text():
    """CLIAdapter: extract() con input_type='text' separa por líneas"""
    # Arrange
    input_data = 'juan.perez@old.com\nmaria.garcia@old.com'
    input_type = 'text'
    
    # Act
    result = EmailProcessingCLI.extract(input_data, input_type)
    
    # Assert
    assert len(result) == 2


def test_cli_extract_invalid_type():
    """CLIAdapter: extract() con input_type inválido lanza ValueError"""
    # Arrange
    input_data = []
    input_type = 'invalid'
    
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid input_type"):
        EmailProcessingCLI.extract(input_data, input_type)


# ============================================================================
# Tests de validate()
# ============================================================================

def test_cli_validate_valid_email(cli_adapter):
    """CLIAdapter: validate() con email válido retorna True"""
    # Arrange
    email = 'juan.perez@example.com'
    
    # Act
    result = cli_adapter.validate(email)
    
    # Assert
    assert result is True


def test_cli_validate_invalid_email(cli_adapter):
    """CLIAdapter: validate() con email inválido retorna False"""
    # Arrange
    email = 'invalid'
    
    # Act
    result = cli_adapter.validate(email)
    
    # Assert
    assert result is False


# ============================================================================
# Tests de transform()
# ============================================================================

def test_cli_transform_valid_emails(cli_adapter):
    """CLIAdapter: transform() con emails válidos retorna transformados"""
    # Arrange
    emails = ['juan.perez@old.com', 'maria.garcia@old.com']
    new_domain = 'company.com'
    
    # Act
    result = cli_adapter.transform(emails, new_domain)
    
    # Assert
    assert len(result) == 2
    assert all(item['valid'] for item in result)


def test_cli_transform_invalid_emails(cli_adapter):
    """CLIAdapter: transform() con emails inválidos registra errores"""
    # Arrange
    emails = ['invalid', 'no-dot@old.com']
    new_domain = 'company.com'
    
    # Act
    result = cli_adapter.transform(emails, new_domain)
    
    # Assert
    assert len(result) == 2
    assert all(not item['valid'] for item in result)


# ============================================================================
# Tests de generate()
# ============================================================================

def test_cli_generate_csv(cli_adapter, temp_output_file):
    """CLIAdapter: generate() con output_type='csv' crea archivo"""
    # Arrange
    transformed = [
        {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True}
    ]
    
    # Act
    result = cli_adapter.generate(transformed, 'csv', temp_output_file)
    
    # Assert
    assert result == 1
    assert os.path.exists(temp_output_file)


def test_cli_generate_silent(cli_adapter):
    """CLIAdapter: generate() con output_type='silent' retorna count"""
    # Arrange
    transformed = [
        {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True}
    ]
    
    # Act
    result = cli_adapter.generate(transformed, 'silent')
    
    # Assert
    assert result == 1


def test_cli_generate_csv_missing_file(cli_adapter):
    """CLIAdapter: generate() CSV sin output_file lanza ValueError"""
    # Arrange
    transformed = [
        {'original': 'juan.perez@old.com', 'transformed': 'juan.perez@new.com', 'valid': True}
    ]
    
    # Act & Assert
    with pytest.raises(ValueError, match="output_file required"):
        cli_adapter.generate(transformed, 'csv')


# ============================================================================
# Tests de run() - Flujo Completo
# ============================================================================

def test_cli_run_complete_flow(cli_adapter, temp_input_file, temp_output_file):
    """CLIAdapter: run() ejecuta flujo completo extract -> transform -> generate"""
    # Arrange
    config = {
        'input': temp_input_file,
        'input_type': 'file',
        'new_domain': 'company.com',
        'output_type': 'csv',
        'output_file': temp_output_file
    }
    
    # Act
    cli_adapter.run(config)
    
    # Assert
    assert os.path.exists(temp_output_file)
    assert os.path.exists('summary.txt')
    
    # Cleanup
    if os.path.exists('error_log.txt'):
        os.unlink('error_log.txt')
    if os.path.exists('summary.txt'):
        os.unlink('summary.txt')


def test_cli_run_silent_mode(cli_adapter, temp_input_file):
    """CLIAdapter: run() en modo silent genera summary"""
    # Arrange
    config = {
        'input': temp_input_file,
        'input_type': 'file',
        'new_domain': 'company.com',
        'output_type': 'silent'
    }
    
    # Act
    cli_adapter.run(config)
    
    # Assert
    assert os.path.exists('summary.txt')
    
    # Cleanup
    if os.path.exists('error_log.txt'):
        os.unlink('error_log.txt')
    if os.path.exists('summary.txt'):
        os.unlink('summary.txt')


# ============================================================================
# Tests de show_usage()
# ============================================================================

def test_cli_show_usage(capsys):
    """CLIAdapter: show_usage() muestra ayuda"""
    # Arrange & Act
    EmailProcessingCLI.show_usage()
    
    # Assert
    captured = capsys.readouterr()
    assert 'EMAIL PROCESSOR' in captured.out
    assert 'USAGE:' in captured.out
