"""
Library Usage Examples - Modular & Stateless
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.features.email_processing.adapters.input.library_adapter import EmailProcessingLibrary


def example_extract():
    """Extract emails from different sources."""
    print("=== EXTRACT EXAMPLES ===\n")
    
    # From file
    emails = EmailProcessingLibrary.extract("file_examples/sample_emails.txt", "file")
    print(f"From file: {len(emails)} emails\n")
    
    # From list
    emails = EmailProcessingLibrary.extract(["user@old.com", "admin@old.com"], "list")
    print(f"From list: {emails}\n")
    
    # From text
    emails = EmailProcessingLibrary.extract("user@old.com\nadmin@old.com", "text")
    print(f"From text: {emails}\n")


def example_transform():
    """Transform emails with new domain."""
    print("=== TRANSFORM EXAMPLE ===\n")
    
    emails = ["juan.perez@old.com", "ana.garcia@old.com"]
    transformed = EmailProcessingLibrary.transform(emails, "company.com")
    
    for item in transformed:
        if item['valid']:
            print(f"{item['original']} -> {item['transformed']}")
    print()


def example_generate():
    """Generate output in different formats."""
    print("=== GENERATE EXAMPLES ===\n")
    
    transformed = [
        {"original": "user.test@old.com", "transformed": "user.test@new.com", "valid": True},
        {"original": "admin.root@old.com", "transformed": "admin.root@new.com", "valid": True}
    ]
    
    # CSV output
    count = EmailProcessingLibrary.generate(transformed, "csv", "output.csv")
    print(f"CSV: {count} emails saved\n")
    
    # Inline output
    emails = EmailProcessingLibrary.generate(transformed, "inline")
    print(f"Inline: {emails}\n")
    
    # Silent mode
    count = EmailProcessingLibrary.generate(transformed, "silent")
    print(f"Silent: {count} emails processed\n")


def example_validate():
    """Validate email format."""
    print("=== VALIDATE EXAMPLE ===\n")
    
    test_emails = ["juan.perez@example.com", "invalid_email", "ana@test.com"]
    
    for email in test_emails:
        is_valid = EmailProcessingLibrary.validate(email)
        print(f"{email}: {'VALID' if is_valid else 'INVALID'}")
    print()


def example_full_pipeline():
    """Complete pipeline: extract -> transform -> generate."""
    print("=== FULL PIPELINE ===\n")
    
    # 1. Extract
    emails = EmailProcessingLibrary.extract(["juan.perez@old.com", "ana.garcia@old.com"], "list")
    print(f"1. Extracted: {emails}")
    
    # 2. Transform
    transformed = EmailProcessingLibrary.transform(emails, "newcompany.com")
    print(f"2. Transformed: {len(transformed)} emails")
    
    # 3. Generate
    result = EmailProcessingLibrary.generate(transformed, "inline")
    print(f"3. Generated: {result}\n")


if __name__ == "__main__":
    example_extract()
    example_transform()
    example_generate()
    example_validate()
    example_full_pipeline()
