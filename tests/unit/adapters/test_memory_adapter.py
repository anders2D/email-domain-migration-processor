"""
Tests Unitarios - MemoryEmailWriter
Plan 26% → 36%: Fase 3
"""
import pytest
from src.features.email_processing.adapters.output.memory_adapter import MemoryEmailWriter
from src.features.email_processing.domain.email import Email


@pytest.fixture
def sample_emails():
    return [
        Email.create("juan", "perez", "juan.perez@old.com", "new.com"),
        Email.create("maria", "garcia", "maria.garcia@old.com", "new.com")
    ]


def test_save_emails_in_memory(sample_emails):
    """Guarda emails en memoria"""
    # Arrange
    writer = MemoryEmailWriter()
    
    # Act
    writer.save_emails(sample_emails)
    
    # Assert
    assert len(writer.emails) == 2


def test_get_saved_emails(sample_emails):
    """Recupera emails guardados"""
    # Arrange
    writer = MemoryEmailWriter()
    writer.save_emails(sample_emails)
    
    # Act
    result = writer.get_emails()
    
    # Assert
    assert len(result) == 2
    assert result[0].nombre == 'Juan'


def test_memory_isolation(sample_emails):
    """get_emails retorna copia, no referencia"""
    # Arrange
    writer = MemoryEmailWriter()
    writer.save_emails(sample_emails)
    
    # Act
    result1 = writer.get_emails()
    result2 = writer.get_emails()
    
    # Assert
    assert result1 is not result2


def test_clear_memory(sample_emails):
    """Limpia memoria correctamente"""
    # Arrange
    writer = MemoryEmailWriter()
    writer.save_emails(sample_emails)
    
    # Act
    writer.clear()
    
    # Assert
    assert len(writer.emails) == 0
