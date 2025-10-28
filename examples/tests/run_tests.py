"""
Test Suite - CLI, Library, API
"""
import subprocess
import sys


def test_cli():
    print("Testing CLI...")
    result = subprocess.run([
        "email-processor",
        "--input-type", "list",
        "--input", "juan.perez@old.com",
        "--new-domain", "test.com",
        "--output-type", "inline"
    ], capture_output=True, text=True, shell=True)
    
    success = result.returncode == 0 and "juan.perez@test.com" in result.stdout
    print(f"[{'OK' if success else 'FAIL'}] CLI\n")
    return success


def test_library():
    print("Testing Library...")
    try:
        from src.features.email_processing.adapters.input.library_adapter import EmailProcessingLibrary
        
        emails = EmailProcessingLibrary.extract(["juan.perez@old.com"], "list")
        transformed = EmailProcessingLibrary.transform(emails, "test.com")
        result = EmailProcessingLibrary.generate(transformed, "inline")
        
        success = result[0] == "juan.perez@test.com"
        print(f"[{'OK' if success else 'FAIL'}] Library\n")
        return success
    except Exception as e:
        print(f"[FAIL] Library: {e}\n")
        return False


def test_api():
    print("Testing API (requires server running)...")
    try:
        import requests
        
        r1 = requests.post("http://localhost:5000/extract", json={
            "input_type": "list", "input": ["juan.perez@old.com"]
        }, timeout=2)
        
        r2 = requests.post("http://localhost:5000/transform", json={
            "emails": ["juan.perez@old.com"], "new_domain": "test.com"
        }, timeout=2)
        
        r3 = requests.post("http://localhost:5000/generate", json={
            "transformed": r2.json()["transformed"], "output_type": "inline"
        }, timeout=2)
        
        success = all([r1.status_code == 200, r2.status_code == 200, r3.status_code == 200])
        print(f"[{'OK' if success else 'FAIL'}] API\n")
        return success
    except Exception:
        print("[SKIP] API (server not running)\n")
        return None


if __name__ == "__main__":
    print("=== Email Processor Test Suite ===\n")
    
    results = [test_cli(), test_library(), test_api()]
    
    passed = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is False)
    skipped = sum(1 for r in results if r is None)
    
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")
    sys.exit(1 if failed > 0 else 0)
