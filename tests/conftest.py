"""
Fixtures compartidos para todos los tests
"""
import pytest
from src.shared.validation_adapter import RegexEmailValidator


@pytest.fixture
def validator():
    """Fixture para validator reutilizable en todos los tests"""
    return RegexEmailValidator()


@pytest.fixture
def valid_emails():
    """Lista de emails válidos para tests"""
    return [
        "juan.perez@example.com",
        "maria.garcia@test.com",
        "ana.lopez@domain.com",
        "carlos.rodriguez@company.com",
        "laura.martinez@email.com"
    ]


@pytest.fixture
def invalid_emails_br001():
    """Emails que violan BR-001 (@ faltante o múltiple)"""
    return {
        "missing": "juan.perezexample.com",
        "multiple": "juan.perez@@example.com"
    }


@pytest.fixture
def invalid_emails_br002():
    """Emails que violan BR-002 (punto faltante o múltiple)"""
    return {
        "missing": "juanperez@example.com",
        "multiple": "juan.del.carmen@example.com"
    }


@pytest.fixture
def invalid_emails_br003():
    """Emails que violan BR-003 (longitud nombre)"""
    return {
        "too_short": "a.perez@example.com",
        "too_long": f"{'a' * 51}.perez@example.com"
    }


@pytest.fixture
def invalid_emails_br004():
    """Emails que violan BR-004 (longitud apellido)"""
    return {
        "too_short": "juan.p@example.com",
        "too_long": f"juan.{'a' * 51}@example.com"
    }


@pytest.fixture
def invalid_emails_br005():
    """Emails que violan BR-005 (caracteres no permitidos)"""
    return {
        "numbers": "juan123.perez@example.com",
        "hyphen": "maria-jose.garcia@example.com",
        "apostrophe": "o'brien.smith@example.com",
        "accents": "josé.garcía@example.com",
        "enie": "muñoz.lopez@example.com",
        "special": "juan@perez.test@example.com"
    }


# ============================================================================
# Fixtures para EmailProcessingService
# ============================================================================

@pytest.fixture
def email_service():
    """EmailProcessingService con dependencias reales"""
    from src.features.email_processing.domain.email_service import EmailProcessingService
    from src.shared.logging_adapter import PythonLogger
    
    validator = RegexEmailValidator()
    logger = PythonLogger("test")
    return EmailProcessingService(validator, logger)


@pytest.fixture
def valid_emails_service():
    """Lista de emails válidos para service tests"""
    return [
        "juan.perez@old.com",
        "maria.garcia@old.com",
        "carlos.lopez@old.com"
    ]


@pytest.fixture
def invalid_emails_service():
    """Lista de emails inválidos para service tests"""
    return [
        "invalid",
        "no-dot@example.com",
        "josé.garcía@old.com"
    ]
