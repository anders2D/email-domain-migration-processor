"""
Tests Unitarios para RegexEmailValidator
Cubre reglas BR-001 a BR-005 del PDD
"""
import pytest
from src.shared.validation_adapter import RegexEmailValidator


# ============================================================================
# BR-001: Exactamente un @ en el email
# ============================================================================

def test_br001_valid_single_at(validator):
    """BR-001: Email con exactamente un @ es válido"""
    # Arrange
    email = "juan.perez@example.com"
    
    # Act
    nombre, apellido = validator.validate_and_parse(email)
    
    # Assert
    assert nombre == "juan"
    assert apellido == "perez"


def test_br001_missing_at(validator, invalid_emails_br001):
    """BR-001: Email sin @ es rechazado"""
    # Arrange
    email = invalid_emails_br001["missing"]
    
    # Act & Assert
    with pytest.raises(ValueError, match="BR-001"):
        validator.validate_and_parse(email)


def test_br001_multiple_at(validator, invalid_emails_br001):
    """BR-001: Email con múltiples @ es rechazado"""
    # Arrange
    email = invalid_emails_br001["multiple"]
    
    # Act & Assert
    with pytest.raises(ValueError, match="BR-001"):
        validator.validate_and_parse(email)


def test_br001_error_message_missing(validator):
    """BR-001: Mensaje de error correcto cuando falta @"""
    # Arrange
    email = "juan.perezexample.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Falta símbolo @"):
        validator.validate_and_parse(email)


def test_br001_error_message_multiple(validator):
    """BR-001: Mensaje de error correcto con múltiples @"""
    # Arrange
    email = "juan.perez@@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Múltiples símbolos @"):
        validator.validate_and_parse(email)


# ============================================================================
# BR-002: Exactamente un punto en prefijo
# ============================================================================

def test_br002_valid_single_dot(validator):
    """BR-002: Prefijo con exactamente un punto es válido"""
    # Arrange
    email = "juan.perez@example.com"
    
    # Act
    nombre, apellido = validator.validate_and_parse(email)
    
    # Assert
    assert nombre == "juan"
    assert apellido == "perez"


def test_br002_missing_dot(validator, invalid_emails_br002):
    """BR-002: Prefijo sin punto es rechazado"""
    # Arrange
    email = invalid_emails_br002["missing"]
    
    # Act & Assert
    with pytest.raises(ValueError, match="BR-002"):
        validator.validate_and_parse(email)


def test_br002_multiple_dots(validator, invalid_emails_br002):
    """BR-002: Prefijo con múltiples puntos es rechazado"""
    # Arrange
    email = invalid_emails_br002["multiple"]
    
    # Act & Assert
    with pytest.raises(ValueError, match="BR-002"):
        validator.validate_and_parse(email)


def test_br002_dot_at_start(validator):
    """BR-002: Punto al inicio del prefijo causa error al split"""
    # Arrange
    email = ".perez@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError):
        validator.validate_and_parse(email)


def test_br002_dot_at_end(validator):
    """BR-002: Punto al final del prefijo causa error al split"""
    # Arrange
    email = "juan.@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError):
        validator.validate_and_parse(email)


def test_br002_error_message_missing(validator):
    """BR-002: Mensaje de error correcto cuando falta punto"""
    # Arrange
    email = "juanperez@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Falta punto separador"):
        validator.validate_and_parse(email)


def test_br002_error_message_multiple(validator):
    """BR-002: Mensaje de error correcto con múltiples puntos"""
    # Arrange
    email = "juan.del.carmen@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Múltiples puntos"):
        validator.validate_and_parse(email)


# ============================================================================
# BR-003: Nombre 2-50 caracteres
# ============================================================================

def test_br003_valid_min_length(validator):
    """BR-003: Nombre con 2 caracteres es válido"""
    # Arrange
    email = "ab.perez@example.com"
    
    # Act
    nombre, apellido = validator.validate_and_parse(email)
    
    # Assert
    assert nombre == "ab"
    assert len(nombre) == 2


def test_br003_valid_max_length(validator):
    """BR-003: Nombre con 50 caracteres es válido"""
    # Arrange
    nombre_50 = "a" * 50
    email = f"{nombre_50}.perez@example.com"
    
    # Act
    nombre, apellido = validator.validate_and_parse(email)
    
    # Assert
    assert len(nombre) == 50


def test_br003_valid_medium_length(validator):
    """BR-003: Nombre con longitud media es válido"""
    # Arrange
    email = "juan.perez@example.com"
    
    # Act
    nombre, apellido = validator.validate_and_parse(email)
    
    # Assert
    assert 2 <= len(nombre) <= 50


def test_br003_too_short_one_char(validator, invalid_emails_br003):
    """BR-003: Nombre con 1 carácter es rechazado"""
    # Arrange
    email = invalid_emails_br003["too_short"]
    
    # Act & Assert
    with pytest.raises(ValueError, match="BR-003"):
        validator.validate_and_parse(email)


def test_br003_too_long_51_chars(validator, invalid_emails_br003):
    """BR-003: Nombre con 51 caracteres es rechazado"""
    # Arrange
    email = invalid_emails_br003["too_long"]
    
    # Act & Assert
    with pytest.raises(ValueError, match="BR-003"):
        validator.validate_and_parse(email)


def test_br003_error_message_short(validator):
    """BR-003: Mensaje de error correcto para nombre corto"""
    # Arrange
    email = "a.perez@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Nombre muy corto"):
        validator.validate_and_parse(email)


def test_br003_error_message_long(validator):
    """BR-003: Mensaje de error correcto para nombre largo"""
    # Arrange
    email = f"{'a' * 51}.perez@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Nombre muy largo"):
        validator.validate_and_parse(email)


# ============================================================================
# BR-004: Apellido 2-50 caracteres
# ============================================================================

def test_br004_valid_min_length(validator):
    """BR-004: Apellido con 2 caracteres es válido"""
    # Arrange
    email = "juan.ab@example.com"
    
    # Act
    nombre, apellido = validator.validate_and_parse(email)
    
    # Assert
    assert apellido == "ab"
    assert len(apellido) == 2


def test_br004_valid_max_length(validator):
    """BR-004: Apellido con 50 caracteres es válido"""
    # Arrange
    apellido_50 = "a" * 50
    email = f"juan.{apellido_50}@example.com"
    
    # Act
    nombre, apellido = validator.validate_and_parse(email)
    
    # Assert
    assert len(apellido) == 50


def test_br004_valid_medium_length(validator):
    """BR-004: Apellido con longitud media es válido"""
    # Arrange
    email = "juan.perez@example.com"
    
    # Act
    nombre, apellido = validator.validate_and_parse(email)
    
    # Assert
    assert 2 <= len(apellido) <= 50


def test_br004_too_short_one_char(validator, invalid_emails_br004):
    """BR-004: Apellido con 1 carácter es rechazado"""
    # Arrange
    email = invalid_emails_br004["too_short"]
    
    # Act & Assert
    with pytest.raises(ValueError, match="BR-004"):
        validator.validate_and_parse(email)


def test_br004_too_long_51_chars(validator, invalid_emails_br004):
    """BR-004: Apellido con 51 caracteres es rechazado"""
    # Arrange
    email = invalid_emails_br004["too_long"]
    
    # Act & Assert
    with pytest.raises(ValueError, match="BR-004"):
        validator.validate_and_parse(email)


def test_br004_error_message_short(validator):
    """BR-004: Mensaje de error correcto para apellido corto"""
    # Arrange
    email = "juan.p@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Apellido muy corto"):
        validator.validate_and_parse(email)


def test_br004_error_message_long(validator):
    """BR-004: Mensaje de error correcto para apellido largo"""
    # Arrange
    email = f"juan.{'a' * 51}@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Apellido muy largo"):
        validator.validate_and_parse(email)


# ============================================================================
# BR-005: Solo letras (sin acentos)
# ============================================================================

def test_br005_valid_lowercase(validator):
    """BR-005: Letras minúsculas son válidas"""
    # Arrange
    email = "juan.perez@example.com"
    
    # Act
    nombre, apellido = validator.validate_and_parse(email)
    
    # Assert
    assert nombre == "juan"
    assert apellido == "perez"


def test_br005_valid_uppercase(validator):
    """BR-005: Letras mayúsculas son válidas"""
    # Arrange
    email = "JUAN.PEREZ@example.com"
    
    # Act
    nombre, apellido = validator.validate_and_parse(email)
    
    # Assert
    assert nombre == "juan"
    assert apellido == "perez"


def test_br005_valid_mixed_case(validator):
    """BR-005: Mezcla de mayúsculas y minúsculas es válida"""
    # Arrange
    email = "JuAn.PeReZ@example.com"
    
    # Act
    nombre, apellido = validator.validate_and_parse(email)
    
    # Assert
    assert nombre == "juan"
    assert apellido == "perez"


def test_br005_invalid_numbers(validator, invalid_emails_br005):
    """BR-005: Números son rechazados"""
    # Arrange
    email = invalid_emails_br005["numbers"]
    
    # Act & Assert
    with pytest.raises(ValueError, match="BR-005"):
        validator.validate_and_parse(email)


def test_br005_invalid_hyphen(validator, invalid_emails_br005):
    """BR-005: Guiones son rechazados"""
    # Arrange
    email = invalid_emails_br005["hyphen"]
    
    # Act & Assert
    with pytest.raises(ValueError, match="BR-005"):
        validator.validate_and_parse(email)


def test_br005_invalid_apostrophe(validator, invalid_emails_br005):
    """BR-005: Apóstrofes son rechazados"""
    # Arrange
    email = invalid_emails_br005["apostrophe"]
    
    # Act & Assert
    with pytest.raises(ValueError, match="BR-005"):
        validator.validate_and_parse(email)


def test_br005_invalid_accents(validator, invalid_emails_br005):
    """BR-005: Acentos son rechazados (á, é, í, ó, ú)"""
    # Arrange
    email = invalid_emails_br005["accents"]
    
    # Act & Assert
    with pytest.raises(ValueError, match="BR-005"):
        validator.validate_and_parse(email)


def test_br005_invalid_enie(validator, invalid_emails_br005):
    """BR-005: Letra ñ es rechazada"""
    # Arrange
    email = invalid_emails_br005["enie"]
    
    # Act & Assert
    with pytest.raises(ValueError, match="BR-005"):
        validator.validate_and_parse(email)


def test_br005_invalid_special_chars(validator):
    """BR-005: Caracteres especiales son rechazados"""
    # Arrange
    email = "juan$.perez@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="BR-005"):
        validator.validate_and_parse(email)


def test_br005_error_message_numbers(validator):
    """BR-005: Mensaje específico para números"""
    # Arrange
    email = "juan123.perez@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="contiene números"):
        validator.validate_and_parse(email)


def test_br005_error_message_hyphen(validator):
    """BR-005: Mensaje específico para guiones"""
    # Arrange
    email = "maria-jose.garcia@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="contiene guiones"):
        validator.validate_and_parse(email)


def test_br005_error_message_apostrophe(validator):
    """BR-005: Mensaje específico para apóstrofes"""
    # Arrange
    email = "o'brien.smith@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="contiene apóstrofes"):
        validator.validate_and_parse(email)


def test_br005_error_message_generic(validator):
    """BR-005: Mensaje genérico para otros caracteres"""
    # Arrange
    email = "josé.garcía@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="caracteres no permitidos"):
        validator.validate_and_parse(email)


def test_br005_apellido_invalid_numbers(validator):
    """BR-005: Números en apellido son rechazados"""
    # Arrange
    email = "juan.perez123@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Apellido contiene números"):
        validator.validate_and_parse(email)


def test_br005_apellido_invalid_hyphen(validator):
    """BR-005: Guiones en apellido son rechazados"""
    # Arrange
    email = "juan.perez-lopez@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Apellido contiene guiones"):
        validator.validate_and_parse(email)


def test_br005_apellido_invalid_apostrophe(validator):
    """BR-005: Apóstrofes en apellido son rechazados"""
    # Arrange
    email = "juan.o'brien@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Apellido contiene apóstrofes"):
        validator.validate_and_parse(email)


def test_br005_apellido_invalid_generic(validator):
    """BR-005: Caracteres no permitidos en apellido son rechazados"""
    # Arrange
    email = "juan.garcía@example.com"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Apellido contiene caracteres no permitidos"):
        validator.validate_and_parse(email)


# ============================================================================
# Tests Adicionales de Validación
# ============================================================================

def test_validate_domain_valid(validator):
    """Dominio válido es aceptado"""
    # Arrange
    domain = "example.com"
    
    # Act
    result = validator.validate_domain(domain)
    
    # Assert
    assert result is True


def test_validate_domain_invalid(validator):
    """Dominio inválido es rechazado"""
    # Arrange
    domain = "invalid"
    
    # Act
    result = validator.validate_domain(domain)
    
    # Assert
    assert result is False


def test_is_valid_method(validator):
    """Método is_valid() retorna bool correctamente"""
    # Arrange
    valid_email = "juan.perez@example.com"
    invalid_email = "invalid"
    
    # Act
    result_valid = validator.is_valid(valid_email)
    result_invalid = validator.is_valid(invalid_email)
    
    # Assert
    assert result_valid is True
    assert result_invalid is False


def test_strip_whitespace(validator):
    """Espacios en blanco son eliminados automáticamente"""
    # Arrange
    email = "  juan.perez@example.com  "
    
    # Act
    nombre, apellido = validator.validate_and_parse(email)
    
    # Assert
    assert nombre == "juan"
    assert apellido == "perez"


def test_case_insensitive_return(validator):
    """validate_and_parse retorna nombre y apellido en minúsculas"""
    # Arrange
    email = "JUAN.PEREZ@example.com"
    
    # Act
    nombre, apellido = validator.validate_and_parse(email)
    
    # Assert
    assert nombre == "juan"
    assert apellido == "perez"
    assert nombre.islower()
    assert apellido.islower()
