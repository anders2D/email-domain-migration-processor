from abc import ABC, abstractmethod
from typing import List


class EmailValidator(ABC):
    """Port for email validation (BR-001 to BR-005)."""
    
    @abstractmethod
    def validate_and_parse(self, email: str) -> tuple[str, str]:
        """Validate email and return (nombre, apellido)."""
        pass
    
    @abstractmethod
    def validate_domain(self, domain: str) -> bool:
        """Validate domain format."""
        pass


class Logger(ABC):
    """Port for logging."""
    
    @abstractmethod
    def info(self, message: str) -> None:
        pass
    
    @abstractmethod
    def warning(self, message: str) -> None:
        pass
    
    @abstractmethod
    def error(self, message: str) -> None:
        pass


# Legacy ports (kept for backward compatibility)
class EmailRepository(ABC):
    @abstractmethod
    def read_emails(self, source: str) -> List[str]:
        pass


class EmailWriter(ABC):
    @abstractmethod
    def save_emails(self, emails: List, destination: str) -> None:
        pass


class OutputFormatter(ABC):
    """Port for output formatting (returns string instead of writing to file)."""
    
    @abstractmethod
    def format(self, emails: List) -> str:
        """Format emails to string representation."""
        pass