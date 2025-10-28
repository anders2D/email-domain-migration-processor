"""
Tests Unitarios - Ports (Domain Layer)
Cobertura de interfaces abstractas (contratos)
"""
import pytest
from src.features.email_processing.domain.ports import (
    EmailValidator, Logger, EmailRepository, EmailWriter, OutputFormatter
)


# ============================================================================
# Mock Implementations para Tests
# ============================================================================


class MockEmailValidator(EmailValidator):
    def validate_and_parse(self, email: str) -> tuple[str, str]:
        return ("Juan", "Perez")
    
    def validate_domain(self, domain: str) -> bool:
        return True


class MockLogger(Logger):
    def info(self, message: str) -> None:
        pass
    
    def warning(self, message: str) -> None:
        pass
    
    def error(self, message: str) -> None:
        pass


class MockEmailRepository(EmailRepository):
    def read_emails(self, source: str):
        return []


class MockEmailWriter(EmailWriter):
    def save_emails(self, emails, destination: str) -> None:
        pass


class MockOutputFormatter(OutputFormatter):
    def format(self, emails) -> str:
        return ""


# ============================================================================
# Tests de EmailValidator Port
# ============================================================================

def test_port_email_validator_validate_and_parse_interface():
    """Port: EmailValidator.validate_and_parse() retorna tupla (nombre, apellido)"""
    # Arrange
    validator = MockEmailValidator()
    email = "juan.perez@test.com"
    
    # Act
    result = validator.validate_and_parse(email)
    
    # Assert
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_port_email_validator_validate_domain_interface():
    """Port: EmailValidator.validate_domain() retorna bool"""
    # Arrange
    validator = MockEmailValidator()
    domain = "test.com"
    
    # Act
    result = validator.validate_domain(domain)
    
    # Assert
    assert isinstance(result, bool)


# ============================================================================
# Tests de Logger Port
# ============================================================================

def test_port_logger_info_interface():
    """Port: Logger.info() acepta mensaje string"""
    # Arrange
    logger = MockLogger()
    
    # Act
    logger.info("test message")
    
    # Assert - No exception raised


def test_port_logger_warning_interface():
    """Port: Logger.warning() acepta mensaje string"""
    # Arrange
    logger = MockLogger()
    
    # Act
    logger.warning("test warning")
    
    # Assert - No exception raised


def test_port_logger_error_interface():
    """Port: Logger.error() acepta mensaje string"""
    # Arrange
    logger = MockLogger()
    
    # Act
    logger.error("test error")
    
    # Assert - No exception raised


# ============================================================================
# Tests de EmailRepository Port (Legacy)
# ============================================================================

def test_port_email_repository_read_emails_interface():
    """Port: EmailRepository.read_emails() retorna lista"""
    # Arrange
    repo = MockEmailRepository()
    source = "test.txt"
    
    # Act
    result = repo.read_emails(source)
    
    # Assert
    assert isinstance(result, list)


# ============================================================================
# Tests de EmailWriter Port (Legacy)
# ============================================================================

def test_port_email_writer_save_emails_interface():
    """Port: EmailWriter.save_emails() acepta lista y destino"""
    # Arrange
    writer = MockEmailWriter()
    
    # Act
    writer.save_emails([], "output.csv")
    
    # Assert - No exception raised


# ============================================================================
# Tests de OutputFormatter Port
# ============================================================================

def test_port_output_formatter_format_interface():
    """Port: OutputFormatter.format() retorna string"""
    # Arrange
    formatter = MockOutputFormatter()
    
    # Act
    result = formatter.format([])
    
    # Assert
    assert isinstance(result, str)
