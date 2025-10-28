"""
Entidad Email - Core Domain (Pure Business Logic)
"""
from dataclasses import dataclass


@dataclass
class Email:
    nombre: str
    apellido: str
    correo_original: str
    correo_nuevo: str
    
    @classmethod
    def create(cls, nombre: str, apellido: str, correo_original: str, nuevo_dominio: str):
        """Factory method para crear Email con transformaciones TR-001 a TR-005."""
        correo_nuevo = f"{nombre.lower()}.{apellido.lower()}@{nuevo_dominio.lower()}"
        return cls(nombre.capitalize(), apellido.capitalize(), correo_original, correo_nuevo)
    
    def __str__(self):
        return self.correo_nuevo
    
    def to_dict(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo_original': self.correo_original,
            'correo_nuevo': self.correo_nuevo
        }
    
    def to_list(self):
        return [self.nombre, self.apellido, self.correo_original, self.correo_nuevo]