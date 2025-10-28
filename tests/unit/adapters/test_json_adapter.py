"""
Tests Unitarios - JsonEmailWriter y JsonFormatter
Plan 26% → 36%: Fase 1
"""
import pytest
import json
from src.features.email_processing.adapters.output.json_adapter import JsonEmailWriter, JsonFormatter
from src.features.email_processing.domain.email import Email


@pytest.fixture
def sample_emails():
    return [
        Email.create("juan", "perez", "juan.perez@old.com", "new.com"),
        Email.create("maria", "garcia", "maria.garcia@old.com", "new.com")
    ]


def test_write_json_correct_format(tmp_path, sample_emails):
    """Escribe JSON con formato correcto"""
    # Arrange
    file_path = tmp_path / "output.json"
    writer = JsonEmailWriter()
    
    # Act
    writer.save_emails(sample_emails, str(file_path))
    
    # Assert
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert 'emails' in data
        assert 'total' in data
        assert data['total'] == 2


def test_write_json_empty_list(tmp_path):
    """JSON con lista vacía"""
    # Arrange
    file_path = tmp_path / "output.json"
    writer = JsonEmailWriter()
    
    # Act
    writer.save_emails([], str(file_path))
    
    # Assert
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert data['total'] == 0
        assert len(data['emails']) == 0


def test_format_json_string(sample_emails):
    """Formatea emails a string JSON"""
    # Arrange
    formatter = JsonFormatter()
    
    # Act
    result = formatter.format(sample_emails)
    
    # Assert
    assert isinstance(result, str)
    data = json.loads(result)
    assert data['total'] == 2


def test_format_json_contains_data(sample_emails):
    """String JSON contiene datos correctos"""
    # Arrange
    formatter = JsonFormatter()
    
    # Act
    result = formatter.format(sample_emails)
    data = json.loads(result)
    
    # Assert
    assert data['emails'][0]['nombre'] == 'Juan'
    assert data['emails'][0]['correo_nuevo'] == 'juan.perez@new.com'


def test_format_json_custom_structure(sample_emails):
    """JSON tiene estructura esperada"""
    # Arrange
    formatter = JsonFormatter()
    
    # Act
    result = formatter.format(sample_emails)
    data = json.loads(result)
    
    # Assert
    assert all(key in data['emails'][0] for key in ['nombre', 'apellido', 'correo_original', 'correo_nuevo'])
