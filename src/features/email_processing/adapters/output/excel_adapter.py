from typing import List
from src.features.email_processing.domain.ports import EmailWriter
from src.features.email_processing.domain.email import Email


class ExcelEmailWriter(EmailWriter):
    def __init__(self, headers: List[str] = None):
        self.headers = headers or ['Nombre', 'Apellido', 'Correo Original', 'Correo Nuevo']
    
    def save_emails(self, emails: List[Email], destination: str):
        try:
            import openpyxl
            from openpyxl import Workbook
        except ImportError:
            raise ImportError("openpyxl required for Excel output. Install: pip install openpyxl")
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Correos Procesados"
        
        # Headers
        ws.append(self.headers)
        
        # Data
        for email in emails:
            ws.append(email.to_list())
        
        wb.save(destination)
