import os
from typing import List
from src.features.email_processing.domain.ports import EmailRepository


class FileEmailRepository(EmailRepository):
    def read_emails(self, source: str) -> List[str]:
        if not os.path.exists(source):
            raise FileNotFoundError(f"Archivo no encontrado: {source}")
        
        with open(source, 'r', encoding='utf-8') as file:
            emails = []
            for line in file:
                line = line.strip()
                if line and not line.startswith('#') and '@' in line:
                    emails.append(line)
            return emails
    
    def read(self, source: str) -> List[str]:
        """Alias para read_emails para compatibilidad"""
        return self.read_emails(source)