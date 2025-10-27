from typing import List
from src.features.email_processing.domain.ports import EmailWriter
from src.features.email_processing.domain.email import Email


class MemoryEmailWriter(EmailWriter):
    """Writer que guarda en memoria para testing o uso programático."""
    
    def __init__(self):
        self.emails = []
    
    def save_emails(self, emails: List[Email], destination: str = None):
        self.emails = emails.copy()
    
    def get_emails(self) -> List[Email]:
        return self.emails.copy()
    
    def clear(self):
        self.emails.clear()