"""API Entry Point - main_api.py"""
from src.features.email_processing.adapters.input.api_adapter import EmailProcessingAPI

if __name__ == "__main__":
    print("=== Email Processing API - Modular & Stateless ===")
    print("Server: http://localhost:5000")
    print("\nEndpoints:")
    print("  POST /validate   - Validate a single email")
    print("  POST /extract    - Extract emails from source")
    print("  POST /transform  - Transform emails with new domain")
    print("  POST /generate   - Generate output in format")
    print("\nTest: python examples/api_example.py")
    print("\nStarting server...\n")
    
    api = EmailProcessingAPI()
    api.run(host='0.0.0.0', port=5000)
