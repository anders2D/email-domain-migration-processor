import json
from typing import List
from src.features.email_processing.domain.ports import EmailWriter, OutputFormatter
from src.features.email_processing.domain.email import Email


class JsonEmailWriter(EmailWriter):
    def save_emails(self, emails: List[Email], destination: str):
        data = {
            'emails': [
                {
                    'nombre': email.nombre,
                    'apellido': email.apellido,
                    'correo_original': email.correo_original,
                    'correo_nuevo': email.correo_nuevo
                }
                for email in emails
            ],
            'total': len(emails)
        }
        
        with open(destination, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


class JsonFormatter(OutputFormatter):
    """Formats emails to JSON string (for APIs)."""
    
    def format(self, emails: List[Email]) -> str:
        data = {
            'emails': [
                {
                    'nombre': email.nombre,
                    'apellido': email.apellido,
                    'correo_original': email.correo_original,
                    'correo_nuevo': email.correo_nuevo
                }
                for email in emails
            ],
            'total': len(emails)
        }
        return json.dumps(data, indent=2, ensure_ascii=False)