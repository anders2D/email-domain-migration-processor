import csv
import io
from typing import List
from src.features.email_processing.domain.ports import EmailWriter, OutputFormatter
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


class CsvFormatter(OutputFormatter):
    """Formats emails to CSV string (for APIs)."""
    
    def __init__(self, headers: List[str] = None):
        self.headers = headers or ['Nombre', 'Apellido', 'Correo Original', 'Correo Nuevo']
    
    def format(self, emails: List[Email]) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(self.headers)
        for email in emails:
            writer.writerow(email.to_list())
        return output.getvalue()