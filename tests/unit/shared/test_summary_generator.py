"""
Tests Unitarios - SummaryGenerator (Shared Component)
Cobertura de generación de summary.txt según formato PDD
"""
import pytest
import tempfile
import os
from src.shared.summary_generator import SummaryGenerator


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def temp_summary_file():
    """Crea archivo temporal para summary"""
    fd, path = tempfile.mkstemp(suffix='.txt')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


# ============================================================================
# Tests de generate() - Casos Exitosos
# ============================================================================

def test_summary_generate_all_valid(temp_summary_file):
    """SummaryGenerator: generate() con todos los emails válidos"""
    # Arrange
    stats = {
        'total': 10,
        'processed': 10,
        'errors': 0,
        'success_rate': 100.0,
        'duplicates': 0,
        'warnings': 0,
        'duration': '2.5s',
        'output_file': 'output.csv',
        'error_log': 'error_log.txt',
        'new_domain': 'company.com'
    }
    
    # Act
    result = SummaryGenerator.generate(stats, temp_summary_file)
    
    # Assert
    assert result == temp_summary_file
    assert os.path.exists(temp_summary_file)


def test_summary_generate_all_invalid(temp_summary_file):
    """SummaryGenerator: generate() con todos los emails inválidos"""
    # Arrange
    stats = {
        'total': 10,
        'processed': 0,
        'errors': 10,
        'success_rate': 0.0,
        'duplicates': 0,
        'warnings': 0,
        'duration': '1.2s',
        'output_file': 'output.csv',
        'error_log': 'error_log.txt',
        'new_domain': 'company.com'
    }
    
    # Act
    result = SummaryGenerator.generate(stats, temp_summary_file)
    
    # Assert
    assert os.path.exists(temp_summary_file)


def test_summary_generate_mixed(temp_summary_file):
    """SummaryGenerator: generate() con mezcla de válidos e inválidos"""
    # Arrange
    stats = {
        'total': 100,
        'processed': 85,
        'errors': 15,
        'success_rate': 85.0,
        'duplicates': 5,
        'warnings': 3,
        'duration': '5.7s',
        'output_file': 'output.csv',
        'error_log': 'error_log.txt',
        'new_domain': 'newcompany.com'
    }
    
    # Act
    result = SummaryGenerator.generate(stats, temp_summary_file)
    
    # Assert
    assert os.path.exists(temp_summary_file)


def test_summary_generate_empty(temp_summary_file):
    """SummaryGenerator: generate() con lista vacía (0 emails)"""
    # Arrange
    stats = {
        'total': 0,
        'processed': 0,
        'errors': 0,
        'success_rate': 0.0
    }
    
    # Act
    result = SummaryGenerator.generate(stats, temp_summary_file)
    
    # Assert
    assert os.path.exists(temp_summary_file)


# ============================================================================
# Tests de Integridad de Archivo
# ============================================================================

def test_summary_generate_file_created(temp_summary_file):
    """SummaryGenerator: generate() crea archivo con contenido"""
    # Arrange
    stats = {
        'total': 5,
        'processed': 5,
        'errors': 0,
        'success_rate': 100.0
    }
    
    # Act
    SummaryGenerator.generate(stats, temp_summary_file)
    
    # Assert
    assert os.path.exists(temp_summary_file)
    assert os.path.getsize(temp_summary_file) > 0


def test_summary_generate_content_correct(temp_summary_file):
    """SummaryGenerator: Contenido del resumen sigue formato PDD"""
    # Arrange
    stats = {
        'total': 10,
        'processed': 8,
        'errors': 2,
        'success_rate': 80.0,
        'duplicates': 1,
        'warnings': 1,
        'duration': '3.2s',
        'output_file': 'result.csv',
        'error_log': 'errors.txt',
        'new_domain': 'test.com'
    }
    
    # Act
    SummaryGenerator.generate(stats, temp_summary_file)
    
    # Assert
    with open(temp_summary_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'REPORTE DE PROCESAMIENTO DE CORREOS' in content
        assert 'Total procesados:     10' in content
        assert 'Exitosos:             8' in content
        assert 'Rechazados:           2' in content
        assert 'test.com' in content


def test_summary_generate_with_minimal_stats(temp_summary_file):
    """SummaryGenerator: generate() con stats mínimos usa valores N/A"""
    # Arrange
    stats = {
        'total': 1,
        'processed': 1,
        'errors': 0,
        'success_rate': 100.0
    }
    
    # Act
    result = SummaryGenerator.generate(stats, temp_summary_file)
    
    # Assert
    assert os.path.exists(temp_summary_file)
    with open(temp_summary_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'N/A' in content  # Para campos opcionales


def test_summary_generate_default_output_file():
    """SummaryGenerator: generate() usa 'summary.txt' por defecto"""
    # Arrange
    stats = {
        'total': 1,
        'processed': 1,
        'errors': 0,
        'success_rate': 100.0
    }
    
    # Act
    result = SummaryGenerator.generate(stats)
    
    # Assert
    assert result == "summary.txt"
    
    # Cleanup
    if os.path.exists("summary.txt"):
        os.unlink("summary.txt")
