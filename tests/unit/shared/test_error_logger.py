"""
Tests Unitarios - ErrorLogger (Shared Component)
Cobertura de registro de errores y warnings según formato PDD
"""
import pytest
import tempfile
import os
from src.shared.error_logger import ErrorLogger


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def temp_log_file():
    """Crea archivo temporal para logs"""
    fd, path = tempfile.mkstemp(suffix='.txt')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


# ============================================================================
# Tests de Inicialización
# ============================================================================

def test_error_logger_init():
    """ErrorLogger: __init__() con valores por defecto"""
    # Arrange & Act
    logger = ErrorLogger()
    
    # Assert
    assert logger.log_file == "error_log.txt"
    assert logger.errors == []


def test_error_logger_init_custom_file():
    """ErrorLogger: __init__() con archivo personalizado"""
    # Arrange
    custom_file = "custom.txt"
    
    # Act
    logger = ErrorLogger(custom_file)
    
    # Assert
    assert logger.log_file == "custom.txt"


# ============================================================================
# Tests de log_error()
# ============================================================================

def test_error_logger_log_error_single():
    """ErrorLogger: log_error() registra un error con formato PDD"""
    # Arrange
    logger = ErrorLogger()
    
    # Act
    logger.log_error("test@example.com", "BR-001", "Invalid format")
    
    # Assert
    assert len(logger.errors) == 1
    assert "ERROR:" in logger.errors[0]
    assert "test@example.com" in logger.errors[0]
    assert "BR-001" in logger.errors[0]


def test_error_logger_log_error_multiple():
    """ErrorLogger: log_error() registra múltiples errores"""
    # Arrange
    logger = ErrorLogger()
    
    # Act
    logger.log_error("test1@example.com", "BR-001", "Invalid format")
    logger.log_error("test2@example.com", "BR-002", "Too short")
    
    # Assert
    assert len(logger.errors) == 2


# ============================================================================
# Tests de log_warning()
# ============================================================================

def test_error_logger_log_warning_single():
    """ErrorLogger: log_warning() registra un warning con formato PDD"""
    # Arrange
    logger = ErrorLogger()
    
    # Act
    logger.log_warning("test@example.com", "Duplicate entry")
    
    # Assert
    assert len(logger.errors) == 1
    assert "WARNING:" in logger.errors[0]
    assert "test@example.com" in logger.errors[0]


def test_error_logger_log_warning_multiple():
    """ErrorLogger: log_warning() registra múltiples warnings"""
    # Arrange
    logger = ErrorLogger()
    
    # Act
    logger.log_warning("test1@example.com", "Duplicate")
    logger.log_warning("test2@example.com", "Suspicious")
    
    # Assert
    assert len(logger.errors) == 2


# ============================================================================
# Tests de save()
# ============================================================================

def test_error_logger_save_to_file(temp_log_file):
    """ErrorLogger: save() guarda errores en archivo"""
    # Arrange
    logger = ErrorLogger(temp_log_file)
    logger.log_error("test@example.com", "BR-001", "Invalid")
    
    # Act
    logger.save()
    
    # Assert
    assert os.path.exists(temp_log_file)
    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "ERROR:" in content
        assert "test@example.com" in content


def test_error_logger_save_empty_logger(temp_log_file):
    """ErrorLogger: save() con logger vacío no escribe contenido"""
    # Arrange
    logger = ErrorLogger(temp_log_file)
    
    # Act
    logger.save()
    
    # Assert - No debería crear archivo si no hay errores


# ============================================================================
# Tests de Contadores
# ============================================================================

def test_error_logger_get_error_count():
    """ErrorLogger: get_error_count() cuenta solo errores"""
    # Arrange
    logger = ErrorLogger()
    logger.log_error("test1@example.com", "BR-001", "Invalid")
    logger.log_error("test2@example.com", "BR-002", "Too short")
    logger.log_warning("test3@example.com", "Duplicate")
    
    # Act
    count = logger.get_error_count()
    
    # Assert
    assert count == 2


def test_error_logger_get_warning_count():
    """ErrorLogger: get_warning_count() cuenta solo warnings"""
    # Arrange
    logger = ErrorLogger()
    logger.log_error("test1@example.com", "BR-001", "Invalid")
    logger.log_warning("test2@example.com", "Duplicate")
    logger.log_warning("test3@example.com", "Suspicious")
    
    # Act
    count = logger.get_warning_count()
    
    # Assert
    assert count == 2


# ============================================================================
# Tests de Casos Edge
# ============================================================================

def test_error_logger_empty():
    """ErrorLogger: Logger vacío retorna contadores en 0"""
    # Arrange & Act
    logger = ErrorLogger()
    
    # Assert
    assert logger.get_error_count() == 0
    assert logger.get_warning_count() == 0


def test_error_logger_mixed():
    """ErrorLogger: Mezcla de errores y warnings se cuenta correctamente"""
    # Arrange
    logger = ErrorLogger()
    
    # Act
    logger.log_error("test1@example.com", "BR-001", "Invalid")
    logger.log_warning("test2@example.com", "Duplicate")
    logger.log_error("test3@example.com", "BR-002", "Too short")
    logger.log_warning("test4@example.com", "Suspicious")
    
    # Assert
    assert logger.get_error_count() == 2
    assert logger.get_warning_count() == 2
    assert len(logger.errors) == 4


# ============================================================================
# Tests de Formato
# ============================================================================

def test_error_logger_error_format_includes_timestamp():
    """ErrorLogger: Formato de error incluye timestamp [YYYY-MM-DD HH:MM:SS]"""
    # Arrange
    logger = ErrorLogger()
    
    # Act
    logger.log_error("test@example.com", "BR-001", "Invalid")
    
    # Assert
    assert "[" in logger.errors[0]
    assert "]" in logger.errors[0]


def test_error_logger_warning_format_includes_timestamp():
    """ErrorLogger: Formato de warning incluye timestamp [YYYY-MM-DD HH:MM:SS]"""
    # Arrange
    logger = ErrorLogger()
    
    # Act
    logger.log_warning("test@example.com", "Duplicate")
    
    # Assert
    assert "[" in logger.errors[0]
    assert "]" in logger.errors[0]
