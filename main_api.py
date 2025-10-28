"""
API REST Interface - Hexagonal Architecture
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.features.email_processing.adapters.input.api_adapter import EmailProcessingAPI


def main():
    api = EmailProcessingAPI()
    print("=== Email Processing API - Modular & Stateless ===")
    print("Server: http://localhost:5000")
    print("\nEndpoints:")
    print("  POST /validate   - Validate a single email")
    print("  POST /extract    - Extract emails from source")
    print("  POST /transform  - Transform emails with new domain")
    print("  POST /generate   - Generate output in format")
    print("\nTest: python test_api.py\n")
    api.run()


if __name__ == "__main__":
    main()