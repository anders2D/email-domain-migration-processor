"""
API Usage Examples - Modular & Stateless
"""
import requests
import json


BASE_URL = "http://localhost:5000"


def example_extract():
    """Extract emails from different input types."""
    print("=== EXTRACT EXAMPLES ===\n")
    
    # From file
    response = requests.post(f"{BASE_URL}/extract", json={
        "input_type": "file",
        "input": "sample_emails.txt"
    })
    print(f"From file: {response.json()}\n")
    
    # From list
    response = requests.post(f"{BASE_URL}/extract", json={
        "input_type": "list",
        "input": ["user@old.com", "admin@old.com"]
    })
    print(f"From list: {response.json()}\n")
    
    # From text
    response = requests.post(f"{BASE_URL}/extract", json={
        "input_type": "text",
        "input": "user@old.com\nadmin@old.com"
    })
    print(f"From text: {response.json()}\n")


def example_transform():
    """Transform emails with new domain."""
    print("=== TRANSFORM EXAMPLE ===\n")
    
    response = requests.post(f"{BASE_URL}/transform", json={
        "emails": ["juan.perez@old.com", "ana.garcia@old.com"],
        "new_domain": "company.com"
    })
    print(json.dumps(response.json(), indent=2))


def example_generate():
    """Generate output in different formats."""
    print("\n=== GENERATE EXAMPLES ===\n")
    
    transformed = [
        {"original": "user@old.com", "transformed": "user@new.com", "valid": True},
        {"original": "admin@old.com", "transformed": "admin@new.com", "valid": True}
    ]
    
    # CSV output
    response = requests.post(f"{BASE_URL}/generate", json={
        "transformed": transformed,
        "output_type": "csv",
        "output_file": "output.csv"
    })
    print(f"CSV: {response.json()}\n")
    
    # Inline output
    response = requests.post(f"{BASE_URL}/generate", json={
        "transformed": transformed,
        "output_type": "inline"
    })
    print(f"Inline: {response.json()}\n")
    
    # Silent mode
    response = requests.post(f"{BASE_URL}/generate", json={
        "transformed": transformed,
        "output_type": "silent"
    })
    print(f"Silent: {response.json()}\n")


def example_full_pipeline():
    """Complete pipeline: extract -> transform -> generate."""
    print("=== FULL PIPELINE ===\n")
    
    # 1. Extract
    extract_response = requests.post(f"{BASE_URL}/extract", json={
        "input_type": "list",
        "input": ["juan.perez@old.com", "ana.garcia@old.com"]
    })
    emails = extract_response.json()["emails"]
    print(f"1. Extracted: {emails}")
    
    # 2. Transform
    transform_response = requests.post(f"{BASE_URL}/transform", json={
        "emails": emails,
        "new_domain": "newcompany.com"
    })
    transformed = transform_response.json()["transformed"]
    print(f"2. Transformed: {len(transformed)} emails")
    
    # 3. Generate
    generate_response = requests.post(f"{BASE_URL}/generate", json={
        "transformed": transformed,
        "output_type": "inline"
    })
    result = generate_response.json()
    print(f"3. Generated: {result['emails']}\n")


if __name__ == "__main__":
    try:
        example_extract()
        example_transform()
        example_generate()
        example_full_pipeline()
    except requests.exceptions.ConnectionError:
        print("❌ Error: API not running")
        print("💡 Run: python main_api.py")
