"""
Tests Unitarios - Email Entity (TR-001 a TR-005)
Fase 2 del Plan Maestro de Tests
"""
import pytest
from src.features.email_processing.domain.email import Email


# ============================================================================
# TR-001: Capitalizar Nombre
# ============================================================================

def test_tr001_lowercase_to_capitalized():
    """TR-001: Nombre en minúsculas se capitaliza"""
    # Arrange & Act
    email = Email.create("juan", "perez", "juan.perez@old.com", "new.com")
    
    # Assert
    assert email.nombre == "Juan"


def test_tr001_uppercase_to_capitalized():
    """TR-001: Nombre en mayúsculas se capitaliza"""
    # Arrange & Act
    email = Email.create("MARIA", "garcia", "MARIA.garcia@old.com", "new.com")
    
    # Assert
    assert email.nombre == "Maria"


def test_tr001_mixed_case_to_capitalized():
    """TR-001: Nombre mixto se capitaliza"""
    # Arrange & Act
    email = Email.create("cArLoS", "lopez", "cArLoS.lopez@old.com", "new.com")
    
    # Assert
    assert email.nombre == "Carlos"


def test_tr001_already_capitalized():
    """TR-001: Nombre ya capitalizado se mantiene"""
    # Arrange & Act
    email = Email.create("Ana", "martinez", "Ana.martinez@old.com", "new.com")
    
    # Assert
    assert email.nombre == "Ana"


# ============================================================================
# TR-002: Capitalizar Apellido
# ============================================================================

def test_tr002_lowercase_to_capitalized():
    """TR-002: Apellido en minúsculas se capitaliza"""
    # Arrange & Act
    email = Email.create("juan", "perez", "juan.perez@old.com", "new.com")
    
    # Assert
    assert email.apellido == "Perez"


def test_tr002_uppercase_to_capitalized():
    """TR-002: Apellido en mayúsculas se capitaliza"""
    # Arrange & Act
    email = Email.create("maria", "GARCIA", "maria.GARCIA@old.com", "new.com")
    
    # Assert
    assert email.apellido == "Garcia"


def test_tr002_mixed_case_to_capitalized():
    """TR-002: Apellido mixto se capitaliza"""
    # Arrange & Act
    email = Email.create("carlos", "lOpEz", "carlos.lOpEz@old.com", "new.com")
    
    # Assert
    assert email.apellido == "Lopez"


def test_tr002_already_capitalized():
    """TR-002: Apellido ya capitalizado se mantiene"""
    # Arrange & Act
    email = Email.create("ana", "Martinez", "ana.Martinez@old.com", "new.com")
    
    # Assert
    assert email.apellido == "Martinez"


# ============================================================================
# TR-003: Minúsculas en Correo Generado
# ============================================================================

def test_tr003_lowercase_email():
    """TR-003: Correo generado está en minúsculas"""
    # Arrange & Act
    email = Email.create("juan", "perez", "juan.perez@old.com", "new.com")
    
    # Assert
    assert email.correo_nuevo == "juan.perez@new.com"
    assert email.correo_nuevo.islower()


def test_tr003_uppercase_input():
    """TR-003: Input en mayúsculas genera correo en minúsculas"""
    # Arrange & Act
    email = Email.create("MARIA", "GARCIA", "MARIA.GARCIA@OLD.COM", "NEW.COM")
    
    # Assert
    assert email.correo_nuevo == "maria.garcia@new.com"


def test_tr003_mixed_case_input():
    """TR-003: Input mixto genera correo en minúsculas"""
    # Arrange & Act
    email = Email.create("CaRlOs", "LoPeZ", "CaRlOs.LoPeZ@OlD.CoM", "NeW.CoM")
    
    # Assert
    assert email.correo_nuevo == "carlos.lopez@new.com"


def test_tr003_domain_lowercase():
    """TR-003: Dominio se convierte a minúsculas"""
    # Arrange & Act
    email = Email.create("ana", "martinez", "ana.martinez@old.com", "COMPANY.COM")
    
    # Assert
    assert email.correo_nuevo == "ana.martinez@company.com"
    assert "@company.com" in email.correo_nuevo


# ============================================================================
# TR-004: Preservar Correo Original
# ============================================================================

def test_tr004_original_preserved():
    """TR-004: Correo original se preserva sin cambios"""
    # Arrange
    original = "juan.perez@old.com"
    
    # Act
    email = Email.create("juan", "perez", original, "new.com")
    
    # Assert
    assert email.correo_original == original


def test_tr004_original_uppercase_preserved():
    """TR-004: Correo original en mayúsculas se preserva"""
    # Arrange
    original = "MARIA.GARCIA@OLD.COM"
    
    # Act
    email = Email.create("MARIA", "GARCIA", original, "new.com")
    
    # Assert
    assert email.correo_original == original


def test_tr004_original_different_domain():
    """TR-004: Dominio original se preserva"""
    # Arrange
    original = "carlos.lopez@example.com"
    
    # Act
    email = Email.create("carlos", "lopez", original, "company.com")
    
    # Assert
    assert email.correo_original == original
    assert "@example.com" in email.correo_original


# ============================================================================
# TR-005: Aplicar Nuevo Dominio
# ============================================================================

def test_tr005_new_domain_applied():
    """TR-005: Nuevo dominio se aplica correctamente"""
    # Arrange & Act
    email = Email.create("juan", "perez", "juan.perez@old.com", "company.com")
    
    # Assert
    assert "@company.com" in email.correo_nuevo
    assert email.correo_nuevo == "juan.perez@company.com"


def test_tr005_format_correct():
    """TR-005: Formato nombre.apellido@dominio es correcto"""
    # Arrange & Act
    email = Email.create("maria", "garcia", "maria.garcia@old.com", "newdomain.com")
    
    # Assert
    assert email.correo_nuevo == "maria.garcia@newdomain.com"
    parts = email.correo_nuevo.split("@")
    assert len(parts) == 2
    assert "." in parts[0]


def test_tr005_different_domains():
    """TR-005: Diferentes dominios se aplican correctamente"""
    # Arrange & Act
    email1 = Email.create("ana", "lopez", "ana.lopez@old.com", "domain1.com")
    email2 = Email.create("ana", "lopez", "ana.lopez@old.com", "domain2.com")
    email3 = Email.create("ana", "lopez", "ana.lopez@old.com", "domain3.org")
    
    # Assert
    assert email1.correo_nuevo == "ana.lopez@domain1.com"
    assert email2.correo_nuevo == "ana.lopez@domain2.com"
    assert email3.correo_nuevo == "ana.lopez@domain3.org"


# ============================================================================
# Tests Adicionales de Email Entity
# ============================================================================

def test_email_create_factory():
    """Método create() funciona como factory"""
    # Arrange & Act
    email = Email.create("juan", "perez", "juan.perez@old.com", "new.com")
    
    # Assert
    assert isinstance(email, Email)
    assert email.nombre == "Juan"
    assert email.apellido == "Perez"
    assert email.correo_original == "juan.perez@old.com"
    assert email.correo_nuevo == "juan.perez@new.com"


def test_email_to_dict():
    """Método to_dict() retorna diccionario correcto"""
    # Arrange
    email = Email.create("maria", "garcia", "maria.garcia@old.com", "new.com")
    
    # Act
    result = email.to_dict()
    
    # Assert
    assert isinstance(result, dict)
    assert result == {
        'nombre': 'Maria',
        'apellido': 'Garcia',
        'correo_original': 'maria.garcia@old.com',
        'correo_nuevo': 'maria.garcia@new.com'
    }


def test_email_to_list():
    """Método to_list() retorna lista en orden correcto"""
    # Arrange
    email = Email.create("carlos", "lopez", "carlos.lopez@old.com", "new.com")
    
    # Act
    result = email.to_list()
    
    # Assert
    assert isinstance(result, list)
    assert result == ['Carlos', 'Lopez', 'carlos.lopez@old.com', 'carlos.lopez@new.com']
    assert len(result) == 4


def test_email_str_representation():
    """__str__() retorna correo_nuevo"""
    # Arrange
    email = Email.create("ana", "martinez", "ana.martinez@old.com", "company.com")
    
    # Act
    result = str(email)
    
    # Assert
    assert result == "ana.martinez@company.com"
    assert result == email.correo_nuevo


def test_email_dataclass_attributes():
    """Atributos de dataclass son accesibles"""
    # Arrange & Act
    email = Email.create("pedro", "sanchez", "pedro.sanchez@old.com", "new.com")
    
    # Assert
    assert hasattr(email, 'nombre')
    assert hasattr(email, 'apellido')
    assert hasattr(email, 'correo_original')
    assert hasattr(email, 'correo_nuevo')
    assert email.nombre == "Pedro"
    assert email.apellido == "Sanchez"
