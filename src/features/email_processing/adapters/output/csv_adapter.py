import csv
from typing import List
from src.features.email_processing.domain.ports import EmailWriter
from src.features.email_processing.domain.email import Email


class CsvEmailWriter(EmailWriter):
    def __init__(self, headers: List[str] = None):
        self.headers = headers or ['Nombre', 'Apellido', 'Correo Original', 'Correo Nuevo']
    
    def save_emails(self, emails: List[Email], destination: str):
        with open(destination, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.headers)
            for email in emails:
                writer.writerow(email.to_list())
    
    def write(self, emails: List[str], destination: str):
        """Escribe lista de correos transformados (strings) a CSV"""
        with open(destination, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.headers)
            for email_str in emails:
                # Parsear email string para extraer componentes
                parts = email_str.split('@')
                if len(parts) == 2:
                    local_part = parts[0]
                    domain = parts[1]
                    if '.' in local_part:
                        nombre, apellido = local_part.split('.', 1)
                        writer.writerow([nombre.capitalize(), apellido.capitalize(), email_str, email_str])