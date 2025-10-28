"""
Tests Unitarios - TxtEmailWriter
Plan 26% → 36%: Fase 2
"""
import pytest
from src.features.email_processing.adapters.output.txt_adapter import TxtEmailWriter
from src.features.email_processing.domain.email import Email


@pytest.fixture
def sample_emails():
    return [
        Email.create("juan", "perez", "juan.perez@old.com", "new.com"),
        Email.create("maria", "garcia", "maria.garcia@old.com", "new.com")
    ]


def test_write_txt_correct_format(tmp_path, sample_emails):
    """Escribe TXT con formato correcto"""
    # Arrange
    file_path = tmp_path / "output.txt"
    writer = TxtEmailWriter()
    
    # Act
    writer.save_emails(sample_emails, str(file_path))
    
    # Assert
    content = file_path.read_text(encoding='utf-8')
    lines = content.strip().split('\n')
    assert len(lines) == 3  # Header + 2 emails


def test_write_txt_empty_list(tmp_path):
    """TXT con solo headers cuando lista vacía"""
    # Arrange
    file_path = tmp_path / "output.txt"
    writer = TxtEmailWriter()
    
    # Act
    writer.save_emails([], str(file_path))
    
    # Assert
    content = file_path.read_text(encoding='utf-8')
    lines = content.strip().split('\n')
    assert len(lines) == 1  # Solo headers


def test_write_txt_line_by_line(tmp_path, sample_emails):
    """Cada email en una línea"""
    # Arrange
    file_path = tmp_path / "output.txt"
    writer = TxtEmailWriter()
    
    # Act
    writer.save_emails(sample_emails, str(file_path))
    
    # Assert
    content = file_path.read_text(encoding='utf-8')
    assert 'Juan,Perez,juan.perez@old.com,juan.perez@new.com' in content


def test_write_txt_custom_headers(tmp_path, sample_emails):
    """Permite headers personalizados"""
    # Arrange
    file_path = tmp_path / "output.txt"
    custom_headers = ['Name', 'Surname', 'Old', 'New']
    writer = TxtEmailWriter(headers=custom_headers)
    
    # Act
    writer.save_emails(sample_emails, str(file_path))
    
    # Assert
    content = file_path.read_text(encoding='utf-8')
    assert 'Name,Surname,Old,New' in content
