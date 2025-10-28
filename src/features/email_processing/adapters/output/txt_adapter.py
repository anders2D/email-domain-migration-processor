from typing import List
from src.features.email_processing.domain.ports import EmailWriter
from src.features.email_processing.domain.email import Email


class TxtEmailWriter(EmailWriter):
    def __init__(self, headers: List[str] = None):
        self.headers = headers or ['Nombre', 'Apellido', 'Correo Original', 'Correo Nuevo']
    
    def save_emails(self, emails: List[Email], destination: str):
        with open(destination, 'w', encoding='utf-8') as f:
            # Headers
            f.write(','.join(self.headers) + '\n')
            
            # Data
            for email in emails:
                f.write(','.join(email.to_list()) + '\n')
