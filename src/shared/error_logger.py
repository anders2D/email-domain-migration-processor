"""
Error Logger - Genera error_log.txt según formato PDD
"""
from datetime import datetime
from pathlib import Path


class ErrorLogger:
    def __init__(self, log_file: str = "error_log.txt"):
        self.log_file = log_file
        self.errors = []
    
    def log_error(self, email: str, rule: str, description: str):
        """Registra error en formato PDD: [TIMESTAMP] ERROR: {correo} - {regla} - {descripción}"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_line = f"[{timestamp}] ERROR: {email} - {rule} - {description}"
        self.errors.append(error_line)
    
    def log_warning(self, email: str, message: str):
        """Registra advertencia (duplicados, etc)"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        warning_line = f"[{timestamp}] WARNING: {email} - {message}"
        self.errors.append(warning_line)
    
    def save(self):
        """Guarda errores en archivo"""
        if self.errors:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.errors))
    
    def get_error_count(self) -> int:
        return len([e for e in self.errors if 'ERROR:' in e])
    
    def get_warning_count(self) -> int:
        return len([e for e in self.errors if 'WARNING:' in e])
