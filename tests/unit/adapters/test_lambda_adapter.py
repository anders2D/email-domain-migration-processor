"""
Tests for LambdaAdapter - Input Layer
"""
import pytest
import base64
from src.features.email_processing.adapters.input.lambda_adapter import EmailProcessingLambda


class TestEmailProcessingLambda:
    """Test suite for EmailProcessingLambda."""

    def test_lambda_adapter_init(self):
        """Initialize LambdaAdapter correctly."""
        adapter = EmailProcessingLambda()
        assert adapter.validator is not None
        assert adapter.logger is not None
        assert adapter.service is not None

    def test_extract_from_list(self):
        """Extract emails from list."""
        adapter = EmailProcessingLambda()
        data = {
            'input_type': 'list',
            'input': ['juan.perez@old.com', 'maria.garcia@old.com']
        }
        result = adapter.extract(data)
        assert len(result) == 2

    def test_extract_from_text(self):
        """Extract emails from text."""
        adapter = EmailProcessingLambda()
        data = {
            'input_type': 'text',
            'input': 'juan.perez@old.com\nmaria.garcia@old.com'
        }
        result = adapter.extract(data)
        assert len(result) == 2

    def test_extract_from_file(self):
        """Extract emails from base64 file."""
        adapter = EmailProcessingLambda()
        content = "juan.perez@old.com\nmaria.garcia@old.com"
        encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        data = {
            'input_type': 'file',
            'file_content': encoded
        }
        result = adapter.extract(data)
        assert len(result) == 2

    def test_extract_invalid_type(self):
        """Handle invalid input type."""
        adapter = EmailProcessingLambda()
        data = {'input_type': 'invalid'}
        with pytest.raises(ValueError, match='Invalid input_type'):
            adapter.extract(data)

    def test_extract_missing_file_content(self):
        """Handle missing file content."""
        adapter = EmailProcessingLambda()
        data = {'input_type': 'file'}
        with pytest.raises(ValueError, match='file_content required'):
            adapter.extract(data)

    def test_transform_valid_emails(self):
        """Transform valid emails."""
        adapter = EmailProcessingLambda()
        emails = ['juan.perez@old.com', 'maria.garcia@old.com']
        result = adapter.transform(emails, 'new.com')
        assert result['total'] == 2
        assert result['processed'] == 2

    def test_transform_invalid_emails(self):
        """Handle invalid emails."""
        adapter = EmailProcessingLambda()
        emails = ['invalid', 'notanemail']
        result = adapter.transform(emails, 'new.com')
        assert result['total'] == 2
        assert result['processed'] == 0

    def test_generate_json_response(self):
        """Generate JSON response."""
        adapter = EmailProcessingLambda()
        emails = ['juan.perez@old.com']
        transform_result = adapter.transform(emails, 'new.com')
        result = adapter.generate(transform_result, 'json')
        assert result['success'] is True
        assert 'results' in result

    def test_generate_csv_response(self):
        """Generate CSV response."""
        adapter = EmailProcessingLambda()
        emails = ['juan.perez@old.com']
        transform_result = adapter.transform(emails, 'new.com')
        result = adapter.generate(transform_result, 'csv')
        assert 'csv' in result
        assert 'Nombre,Apellido' in result['csv']

    def test_process_complete_flow(self):
        """Complete processing flow."""
        adapter = EmailProcessingLambda()
        data = {
            'input_type': 'list',
            'input': ['juan.perez@old.com'],
            'new_domain': 'new.com',
            'output_type': 'json'
        }
        result = adapter.process(data)
        assert result['success'] is True
        assert result['total'] == 1

    def test_process_missing_domain(self):
        """Handle missing new_domain."""
        adapter = EmailProcessingLambda()
        data = {'input': ['test@old.com']}
        with pytest.raises(ValueError, match='Missing required field: new_domain'):
            adapter.process(data)

    def test_process_with_csv_output(self):
        """Process with CSV output."""
        adapter = EmailProcessingLambda()
        data = {
            'input': ['juan.perez@old.com'],
            'new_domain': 'new.com',
            'output_type': 'csv'
        }
        result = adapter.process(data)
        assert 'csv' in result

    def test_extract_default_input_type(self):
        """Extract with default input type."""
        adapter = EmailProcessingLambda()
        data = {'emails': ['juan.perez@old.com']}
        result = adapter.extract(data)
        assert len(result) == 1

    def test_generate_response_structure(self):
        """Verify response structure."""
        adapter = EmailProcessingLambda()
        emails = ['juan.perez@old.com']
        transform_result = adapter.transform(emails, 'new.com')
        result = adapter.generate(transform_result)
        assert 'success' in result
        assert 'processed' in result
        assert 'total' in result
        assert 'results' in result
