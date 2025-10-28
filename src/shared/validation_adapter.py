import re
from typing import Tuple
from src.features.email_processing.domain.ports import EmailValidator


class RegexEmailValidator(EmailValidator):
    def __init__(self):
        self.name_pattern = re.compile(r'^[a-zA-Z]+$')
        self.domain_pattern = re.compile(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def is_valid(self, email: str) -> bool:
        try:
            self.validate_and_parse(email)
            return True
        except:
            return False
    
    def validate_and_parse(self, email: str) -> Tuple[str, str]:
        email = email.strip()
        
        # BR-001: Exactamente un @
        if email.count('@') != 1:
            if email.count('@') == 0:
                raise ValueError(f"BR-001: Falta símbolo @")
            else:
                raise ValueError(f"BR-001: Múltiples símbolos @ detectados")
        
        local_part, domain = email.split('@')
        
        # BR-002: Exactamente un punto en prefijo
        dot_count = local_part.count('.')
        if dot_count != 1:
            if dot_count == 0:
                raise ValueError(f"BR-002: Falta punto separador en prefijo")
            else:
                raise ValueError(f"BR-002: Múltiples puntos en prefijo (formato debe ser nombre.apellido)")
        
        nombre, apellido = local_part.split('.')
        
        # BR-003: Nombre 2-50 caracteres
        if len(nombre) < 2:
            raise ValueError(f"BR-003: Nombre muy corto (mínimo 2 caracteres)")
        if len(nombre) > 50:
            raise ValueError(f"BR-003: Nombre muy largo (máximo 50 caracteres)")
        
        # BR-004: Apellido 2-50 caracteres
        if len(apellido) < 2:
            raise ValueError(f"BR-004: Apellido muy corto (mínimo 2 caracteres)")
        if len(apellido) > 50:
            raise ValueError(f"BR-004: Apellido muy largo (máximo 50 caracteres)")
        
        # BR-005: Solo letras (sin acentos)
        if not self.name_pattern.match(nombre):
            # Detectar tipo de carácter inválido
            if any(c.isdigit() for c in nombre):
                raise ValueError(f"BR-005: Nombre contiene números")
            elif '-' in nombre:
                raise ValueError(f"BR-005: Nombre contiene guiones")
            elif "'" in nombre:
                raise ValueError(f"BR-005: Nombre contiene apóstrofes")
            else:
                raise ValueError(f"BR-005: Nombre contiene caracteres no permitidos")
        
        if not self.name_pattern.match(apellido):
            # Detectar tipo de carácter inválido
            if any(c.isdigit() for c in apellido):
                raise ValueError(f"BR-005: Apellido contiene números")
            elif '-' in apellido:
                raise ValueError(f"BR-005: Apellido contiene guiones")
            elif "'" in apellido:
                raise ValueError(f"BR-005: Apellido contiene apóstrofes")
            else:
                raise ValueError(f"BR-005: Apellido contiene caracteres no permitidos")
        
        return nombre.lower(), apellido.lower()
    
    def validate_domain(self, domain: str) -> bool:
        """Valida formato DNS del dominio destino"""
        return bool(self.domain_pattern.match(domain))
