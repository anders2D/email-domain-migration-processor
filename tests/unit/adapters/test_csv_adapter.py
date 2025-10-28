"""
Tests Unitarios - CsvEmailWriter y CsvFormatter
Plan 20% → 25%: Fase 2
"""
import pytest
import csv
from src.features.email_processing.adapters.output.csv_adapter import CsvEmailWriter, CsvFormatter
from src.features.email_processing.domain.email import Email


@pytest.fixture
def sample_emails():
    """Lista de objetos Email para tests"""
    return [
        Email.create("juan", "perez", "juan.perez@old.com", "new.com"),
        Email.create("maria", "garcia", "maria.garcia@old.com", "new.com")
    ]


# ============================================================================
# Tests de CsvEmailWriter
# ============================================================================

def test_write_csv_correct_headers(tmp_path, sample_emails):
    """Headers correctos: Nombre, Apellido, Correo Original, Correo Nuevo"""
    # Arrange
    file_path = tmp_path / "output.csv"
    writer = CsvEmailWriter()
    
    # Act
    writer.save_emails(sample_emails, str(file_path))
    
    # Assert
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        assert headers == ['Nombre', 'Apellido', 'Correo Original', 'Correo Nuevo']


def test_write_csv_correct_data(tmp_path, sample_emails):
    """Datos escritos correctamente en CSV"""
    # Arrange
    file_path = tmp_path / "output.csv"
    writer = CsvEmailWriter()
    
    # Act
    writer.save_emails(sample_emails, str(file_path))
    
    # Assert
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip headers
        row1 = next(reader)
        row2 = next(reader)
        assert row1 == ['Juan', 'Perez', 'juan.perez@old.com', 'juan.perez@new.com']
        assert row2 == ['Maria', 'Garcia', 'maria.garcia@old.com', 'maria.garcia@new.com']


def test_write_csv_empty_list(tmp_path):
    """CSV con solo headers cuando lista vacía"""
    # Arrange
    file_path = tmp_path / "output.csv"
    writer = CsvEmailWriter()
    
    # Act
    writer.save_emails([], str(file_path))
    
    # Assert
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        assert len(lines) == 1  # Solo headers


def test_write_csv_file_creation(tmp_path, sample_emails):
    """Crea archivo CSV si no existe"""
    # Arrange
    file_path = tmp_path / "new_output.csv"
    writer = CsvEmailWriter()
    
    # Act
    writer.save_emails(sample_emails, str(file_path))
    
    # Assert
    assert file_path.exists()


def test_write_csv_encoding(tmp_path, sample_emails):
    """Usa encoding UTF-8"""
    # Arrange
    file_path = tmp_path / "output.csv"
    writer = CsvEmailWriter()
    
    # Act
    writer.save_emails(sample_emails, str(file_path))
    
    # Assert
    content = file_path.read_text(encoding='utf-8')
    assert 'Juan' in content


def test_write_csv_custom_headers(tmp_path, sample_emails):
    """Permite headers personalizados"""
    # Arrange
    file_path = tmp_path / "output.csv"
    custom_headers = ['Name', 'Surname', 'Old Email', 'New Email']
    writer = CsvEmailWriter(headers=custom_headers)
    
    # Act
    writer.save_emails(sample_emails, str(file_path))
    
    # Assert
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        assert headers == custom_headers


# ============================================================================
# Tests de CsvFormatter
# ============================================================================

def test_format_csv_string(sample_emails):
    """Formatea emails a string CSV"""
    # Arrange
    formatter = CsvFormatter()
    
    # Act
    result = formatter.format(sample_emails)
    
    # Assert
    assert isinstance(result, str)
    assert 'Nombre,Apellido,Correo Original,Correo Nuevo' in result


def test_format_csv_contains_data(sample_emails):
    """String CSV contiene datos correctos"""
    # Arrange
    formatter = CsvFormatter()
    
    # Act
    result = formatter.format(sample_emails)
    
    # Assert
    assert 'Juan,Perez,juan.perez@old.com,juan.perez@new.com' in result
    assert 'Maria,Garcia,maria.garcia@old.com,maria.garcia@new.com' in result


def test_format_csv_empty_list():
    """Formatea lista vacía con solo headers"""
    # Arrange
    formatter = CsvFormatter()
    
    # Act
    result = formatter.format([])
    
    # Assert
    lines = result.strip().split('\n')
    assert len(lines) == 1  # Solo headers


def test_format_csv_custom_headers(sample_emails):
    """Formatter permite headers personalizados"""
    # Arrange
    custom_headers = ['Name', 'Surname', 'Old', 'New']
    formatter = CsvFormatter(headers=custom_headers)
    
    # Act
    result = formatter.format(sample_emails)
    
    # Assert
    assert 'Name,Surname,Old,New' in result
