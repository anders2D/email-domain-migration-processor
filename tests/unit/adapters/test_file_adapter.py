"""
Tests Unitarios - FileEmailRepository
Plan 20% → 25%: Fase 1
"""
import pytest
from src.features.email_processing.adapters.output.file_adapter import FileEmailRepository


def test_read_valid_file(tmp_path):
    """Lee archivo válido correctamente"""
    # Arrange
    file_path = tmp_path / "emails.txt"
    file_path.write_text("juan.perez@old.com\nmaria.garcia@old.com\n", encoding='utf-8')
    repo = FileEmailRepository()
    
    # Act
    emails = repo.read_emails(str(file_path))
    
    # Assert
    assert len(emails) == 2
    assert "juan.perez@old.com" in emails
    assert "maria.garcia@old.com" in emails


def test_read_empty_file(tmp_path):
    """Archivo vacío retorna lista vacía"""
    # Arrange
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding='utf-8')
    repo = FileEmailRepository()
    
    # Act
    emails = repo.read_emails(str(file_path))
    
    # Assert
    assert emails == []


def test_read_file_with_empty_lines(tmp_path):
    """Ignora líneas vacías"""
    # Arrange
    file_path = tmp_path / "emails.txt"
    file_path.write_text("juan.perez@old.com\n\n\nmaria.garcia@old.com\n", encoding='utf-8')
    repo = FileEmailRepository()
    
    # Act
    emails = repo.read_emails(str(file_path))
    
    # Assert
    assert len(emails) == 2


def test_read_file_not_found():
    """FileNotFoundError cuando archivo no existe"""
    # Arrange
    repo = FileEmailRepository()
    
    # Act & Assert
    with pytest.raises(FileNotFoundError, match="Archivo no encontrado"):
        repo.read_emails("nonexistent.txt")


def test_read_file_encoding(tmp_path):
    """Maneja encoding UTF-8 correctamente"""
    # Arrange
    file_path = tmp_path / "emails.txt"
    file_path.write_text("juan.perez@old.com\n", encoding='utf-8')
    repo = FileEmailRepository()
    
    # Act
    emails = repo.read_emails(str(file_path))
    
    # Assert
    assert len(emails) == 1


def test_read_file_strips_whitespace(tmp_path):
    """Elimina espacios en blanco de cada línea"""
    # Arrange
    file_path = tmp_path / "emails.txt"
    file_path.write_text("  juan.perez@old.com  \n  maria.garcia@old.com  \n", encoding='utf-8')
    repo = FileEmailRepository()
    
    # Act
    emails = repo.read_emails(str(file_path))
    
    # Assert
    assert emails[0] == "juan.perez@old.com"
    assert emails[1] == "maria.garcia@old.com"


def test_read_alias_method(tmp_path):
    """Método read() funciona como alias"""
    # Arrange
    file_path = tmp_path / "emails.txt"
    file_path.write_text("juan.perez@old.com\n", encoding='utf-8')
    repo = FileEmailRepository()
    
    # Act
    emails = repo.read(str(file_path))
    
    # Assert
    assert len(emails) == 1


def test_read_ignores_comments(tmp_path):
    """Ignora líneas que empiezan con #"""
    # Arrange
    file_path = tmp_path / "emails.txt"
    file_path.write_text("# Comentario\njuan.perez@old.com\n# Otro comentario\nmaria.garcia@old.com\n", encoding='utf-8')
    repo = FileEmailRepository()
    
    # Act
    emails = repo.read_emails(str(file_path))
    
    # Assert
    assert len(emails) == 2


def test_read_ignores_lines_without_at(tmp_path):
    """Ignora líneas sin símbolo @"""
    # Arrange
    file_path = tmp_path / "emails.txt"
    file_path.write_text("invalid line\njuan.perez@old.com\nanother invalid\n", encoding='utf-8')
    repo = FileEmailRepository()
    
    # Act
    emails = repo.read_emails(str(file_path))
    
    # Assert
    assert len(emails) == 1
    assert emails[0] == "juan.perez@old.com"
