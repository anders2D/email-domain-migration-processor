"""
Tests for CLI Entrypoint
"""
import pytest
import sys
from unittest.mock import patch, MagicMock
from src.features.email_processing.adapters.input.cli_entrypoint import main


class TestCLIEntrypoint:
    """Test suite for CLI entrypoint."""

    @patch('src.features.email_processing.adapters.input.cli_entrypoint.EmailProcessingCLI')
    @patch('sys.argv', ['email-processor', '--input-type', 'list', '--input', 'test@old.com', '--new-domain', 'new.com', '--output-type', 'inline'])
    def test_main_with_valid_args(self, mock_cli):
        """main() with valid arguments."""
        mock_instance = MagicMock()
        mock_cli.return_value = mock_instance
        main()
        mock_instance.run.assert_called_once()

    @patch('sys.argv', ['email-processor', '--help'])
    def test_main_with_help_flag(self):
        """main() with --help flag."""
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0

    @patch('sys.argv', ['email-processor'])
    def test_main_with_invalid_args(self):
        """main() with invalid arguments."""
        with pytest.raises(SystemExit):
            main()

    @patch('src.features.email_processing.adapters.input.cli_entrypoint.EmailProcessingCLI')
    @patch('sys.argv', ['email-processor', '--input', 'test@old.com', '--new-domain', 'new.com', '--output-type', 'csv', '--output', 'out.csv'])
    def test_main_exception_handling(self, mock_cli):
        """main() handles exceptions."""
        mock_instance = MagicMock()
        mock_instance.run.side_effect = Exception("Test error")
        mock_cli.return_value = mock_instance
        with pytest.raises(SystemExit):
            main()

    @patch('src.features.email_processing.adapters.input.cli_entrypoint.EmailProcessingCLI')
    @patch('sys.argv', ['email-processor', '--input', 'test.txt', '--new-domain', 'new.com', '--output-type', 'csv', '--output', 'out.csv'])
    def test_main_file_not_found(self, mock_cli):
        """main() handles FileNotFoundError."""
        mock_instance = MagicMock()
        mock_instance.run.side_effect = FileNotFoundError("File not found")
        mock_cli.return_value = mock_instance
        with pytest.raises(SystemExit):
            main()

    @patch('sys.argv', ['email-processor', '--input', 'test@old.com', '--new-domain', 'new.com', '--output-type', 'csv'])
    def test_main_missing_output(self):
        """main() requires --output for csv."""
        with pytest.raises(SystemExit):
            main()

    @patch('src.features.email_processing.adapters.input.cli_entrypoint.EmailProcessingCLI')
    @patch('sys.argv', ['email-processor', '--input-type', 'file', '--input', 'test.txt', '--new-domain', 'new.com', '--output-type', 'inline'])
    def test_main_with_file_input(self, mock_cli):
        """main() with file input type."""
        mock_instance = MagicMock()
        mock_cli.return_value = mock_instance
        main()
        mock_instance.run.assert_called_once()
