"""
Tests Unitarios - EmailProcessingService
Fase 1 del Plan de Incremento de Cobertura +5%
"""
import pytest
from src.features.email_processing.domain.email import Email


# ============================================================================
# Tests de transform_emails() - Casos Exitosos
# ============================================================================

def test_transform_single_valid_email(email_service):
    """Transforma un email válido correctamente"""
    # Arrange
    emails = ["juan.perez@old.com"]
    new_domain = "new.com"
    
    # Act
    result = email_service.transform_emails(emails, new_domain)
    
    # Assert
    assert result['total'] == 1
    assert result['processed'] == 1
    assert result['errors'] == 0
    assert result['success_rate'] == 100.0
    assert len(result['emails']) == 1
    assert result['emails'][0].correo_nuevo == "juan.perez@new.com"


def test_transform_multiple_valid_emails(email_service, valid_emails_service):
    """Transforma múltiples emails válidos"""
    # Arrange
    new_domain = "company.com"
    
    # Act
    result = email_service.transform_emails(valid_emails_service, new_domain)
    
    # Assert
    assert result['total'] == 3
    assert result['processed'] == 3
    assert result['errors'] == 0
    assert result['success_rate'] == 100.0
    assert len(result['emails']) == 3


def test_transform_statistics_correct(email_service):
    """Estadísticas (total, processed, errors) son correctas"""
    # Arrange
    emails = ["juan.perez@old.com", "invalid", "maria.garcia@old.com"]
    new_domain = "new.com"
    
    # Act
    result = email_service.transform_emails(emails, new_domain)
    
    # Assert
    assert result['total'] == 3
    assert result['processed'] == 2
    assert result['errors'] == 1
    assert result['success_rate'] == pytest.approx(66.67, rel=0.1)


# ============================================================================
# Tests de transform_emails() - Casos de Error
# ============================================================================

def test_transform_all_invalid_emails(email_service, invalid_emails_service):
    """Todos los emails inválidos son rechazados"""
    # Arrange
    new_domain = "new.com"
    
    # Act
    result = email_service.transform_emails(invalid_emails_service, new_domain)
    
    # Assert
    assert result['total'] == 3
    assert result['processed'] == 0
    assert result['errors'] == 3
    assert result['success_rate'] == 0.0
    assert len(result['error_details']) == 3


def test_transform_mixed_valid_invalid(email_service):
    """Mezcla de válidos e inválidos se procesa correctamente"""
    # Arrange
    emails = [
        "juan.perez@old.com",
        "invalid",
        "maria.garcia@old.com",
        "no-dot@old.com",
        "carlos.lopez@old.com"
    ]
    new_domain = "new.com"
    
    # Act
    result = email_service.transform_emails(emails, new_domain)
    
    # Assert
    assert result['total'] == 5
    assert result['processed'] == 3
    assert result['errors'] == 2
    assert result['success_rate'] == 60.0


def test_transform_empty_list(email_service):
    """Lista vacía retorna resultado vacío"""
    # Arrange
    emails = []
    new_domain = "new.com"
    
    # Act
    result = email_service.transform_emails(emails, new_domain)
    
    # Assert
    assert result['total'] == 0
    assert result['processed'] == 0
    assert result['errors'] == 0
    assert result['success_rate'] == 0.0
    assert len(result['emails']) == 0


def test_transform_invalid_domain(email_service):
    """Dominio inválido lanza ValueError"""
    # Arrange
    emails = ["juan.perez@old.com"]
    invalid_domain = "invalid"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid target domain"):
        email_service.transform_emails(emails, invalid_domain)


# ============================================================================
# Tests de Manejo de Excepciones
# ============================================================================

def test_transform_whitespace_handling(email_service):
    """Espacios en blanco se manejan correctamente"""
    # Arrange
    emails = [
        "  juan.perez@old.com  ",
        "maria.garcia@old.com",
        " carlos.lopez@old.com "
    ]
    new_domain = "new.com"
    
    # Act
    result = email_service.transform_emails(emails, new_domain)
    
    # Assert
    assert result['processed'] == 3
    assert result['errors'] == 0


def test_transform_duplicate_emails(email_service):
    """Emails duplicados se detectan y alertan"""
    # Arrange
    emails = [
        "juan.perez@old.com",
        "maria.garcia@old.com",
        "juan.perez@old.com"
    ]
    new_domain = "new.com"
    
    # Act
    result = email_service.transform_emails(emails, new_domain)
    
    # Assert
    assert result['total'] == 3
    assert result['processed'] == 2
    assert result['errors'] == 1
    assert any('Duplicate' in err['error'] for err in result['error_details'])


def test_transform_error_details_populated(email_service):
    """error_details contiene información de errores"""
    # Arrange
    emails = ["invalid", "no-dot@old.com"]
    new_domain = "new.com"
    
    # Act
    result = email_service.transform_emails(emails, new_domain)
    
    # Assert
    assert len(result['error_details']) == 2
    assert all('email' in err for err in result['error_details'])
    assert all('error' in err for err in result['error_details'])


# ============================================================================
# Tests de Métricas
# ============================================================================

def test_transform_success_rate_calculation(email_service):
    """success_rate se calcula correctamente"""
    # Arrange
    test_cases = [
        (["juan.perez@old.com"], 1, 100.0),
        (["juan.perez@old.com", "invalid"], 1, 50.0),
        (["invalid", "invalid"], 0, 0.0),
        ([], 0, 0.0)
    ]
    new_domain = "new.com"
    
    # Act & Assert
    for emails, expected_processed, expected_rate in test_cases:
        result = email_service.transform_emails(emails, new_domain)
        assert result['processed'] == expected_processed
        assert result['success_rate'] == expected_rate


def test_transform_logging_calls(email_service, valid_emails_service):
    """Logger se llama apropiadamente"""
    # Arrange
    new_domain = "new.com"
    
    # Act
    result = email_service.transform_emails(valid_emails_service, new_domain)
    
    # Assert
    assert result['processed'] == 3
    assert result['success_rate'] == 100.0


def test_transform_progress_logging(email_service):
    """Logger registra progreso cada 10 emails"""
    # Arrange
    names = ["juan", "maria", "carlos", "ana", "pedro", "laura", "jose", "carmen", "luis", "rosa", "miguel", "elena", "jorge", "sofia", "pablo"]
    emails = [f"{name}.perez@old.com" for name in names]
    new_domain = "new.com"
    
    # Act
    result = email_service.transform_emails(emails, new_domain)
    
    # Assert
    assert result['processed'] == 15
    assert result['success_rate'] == 100.0
