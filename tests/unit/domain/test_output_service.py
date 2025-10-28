"""
Tests Unitarios - OutputService (Domain Layer)
Cobertura de métodos de generación de salida
"""
import pytest
from src.features.email_processing.domain.output_service import OutputService
from src.features.email_processing.domain.email import Email


# ============================================================================
# Tests de generate_inline()
# ============================================================================

def test_output_generate_inline_empty_list():
    """OutputService: generate_inline() con lista vacía retorna lista vacía"""
    # Arrange
    emails = []
    
    # Act
    result = OutputService.generate_inline(emails)
    
    # Assert
    assert result == []


def test_output_generate_inline_single_email():
    """OutputService: generate_inline() con un email retorna string del correo"""
    # Arrange
    email = Email("Juan", "Perez", "juan.perez@old.com", "juan.perez@new.com")
    
    # Act
    result = OutputService.generate_inline([email])
    
    # Assert
    assert len(result) == 1
    assert result[0] == "juan.perez@new.com"


def test_output_generate_inline_multiple_emails():
    """OutputService: generate_inline() con múltiples emails retorna lista de strings"""
    # Arrange
    emails = [
        Email("Juan", "Perez", "juan.perez@old.com", "juan.perez@new.com"),
        Email("Maria", "Garcia", "maria.garcia@old.com", "maria.garcia@new.com")
    ]
    
    # Act
    result = OutputService.generate_inline(emails)
    
    # Assert
    assert len(result) == 2


# ============================================================================
# Tests de generate_silent()
# ============================================================================

def test_output_generate_silent_returns_count():
    """OutputService: generate_silent() retorna conteo de emails"""
    # Arrange
    emails = [
        Email("Juan", "Perez", "juan.perez@old.com", "juan.perez@new.com"),
        Email("Maria", "Garcia", "maria.garcia@old.com", "maria.garcia@new.com")
    ]
    
    # Act
    result = OutputService.generate_silent(emails)
    
    # Assert
    assert result == 2


def test_output_generate_silent_empty():
    """OutputService: generate_silent() con lista vacía retorna 0"""
    # Arrange
    emails = []
    
    # Act
    result = OutputService.generate_silent(emails)
    
    # Assert
    assert result == 0


# ============================================================================
# Tests de to_dict_list()
# ============================================================================

def test_output_to_dict_list_empty():
    """OutputService: to_dict_list() con lista vacía retorna lista vacía"""
    # Arrange
    emails = []
    
    # Act
    result = OutputService.to_dict_list(emails)
    
    # Assert
    assert result == []


def test_output_to_dict_list_single():
    """OutputService: to_dict_list() con un email retorna dict con 4 campos"""
    # Arrange
    email = Email("Juan", "Perez", "juan.perez@old.com", "juan.perez@new.com")
    
    # Act
    result = OutputService.to_dict_list([email])
    
    # Assert
    assert len(result) == 1
    assert result[0]['nombre'] == 'Juan'
    assert result[0]['apellido'] == 'Perez'
    assert result[0]['correo_original'] == 'juan.perez@old.com'
    assert result[0]['correo_nuevo'] == 'juan.perez@new.com'


def test_output_to_dict_list_multiple():
    """OutputService: to_dict_list() con múltiples emails retorna lista de dicts"""
    # Arrange
    emails = [
        Email("Juan", "Perez", "juan.perez@old.com", "juan.perez@new.com"),
        Email("Maria", "Garcia", "maria.garcia@old.com", "maria.garcia@new.com")
    ]
    
    # Act
    result = OutputService.to_dict_list(emails)
    
    # Assert
    assert len(result) == 2
    assert result[0]['nombre'] == 'Juan'
    assert result[1]['nombre'] == 'Maria'
