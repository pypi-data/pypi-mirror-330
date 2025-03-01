from unittest.mock import patch

import pyperclip
import pytest
from click.testing import CliRunner

from nocamel import main


class TestNoCamelCLI:
    @pytest.fixture
    def cli_runner(self):
        """Fixture providing a Click CLI test runner."""
        return CliRunner()

    def test_default_to_sentence(self, cli_runner):
        """Test that sentence case is the default conversion."""
        with patch("nocamel.converters.to_sentence", return_value="Test result") as mock_convert:
            with patch.object(pyperclip, "copy") as mock_copy:
                result = cli_runner.invoke(main, ["testInput"])

                assert result.exit_code == 0
                assert "Test result" in result.output
                assert "Result copied to clipboard!" in result.output
                mock_convert.assert_called_once_with("testInput")
                mock_copy.assert_called_once_with("Test result")

    def test_snake_case_option(self, cli_runner):
        """Test the --snake option."""
        with patch("nocamel.converters.to_snake", return_value="test_result") as mock_convert:
            with patch.object(pyperclip, "copy") as mock_copy:
                result = cli_runner.invoke(main, ["--snake", "testInput"])

                assert result.exit_code == 0
                assert "test_result" in result.output
                mock_convert.assert_called_once_with("testInput")
                mock_copy.assert_called_once_with("test_result")

    def test_lower_case_option(self, cli_runner):
        """Test the --lower option."""
        with patch("nocamel.converters.to_lower", return_value="test result") as mock_convert:
            with patch.object(pyperclip, "copy") as mock_copy:
                result = cli_runner.invoke(main, ["--lower", "TestInput"])

                assert result.exit_code == 0
                assert "test result" in result.output
                mock_convert.assert_called_once_with("TestInput")
                mock_copy.assert_called_once_with("test result")

    def test_sentence_case_option(self, cli_runner):
        """Test the --sentence option explicitly provided."""
        with patch("nocamel.converters.to_sentence", return_value="Test result") as mock_convert:
            with patch.object(pyperclip, "copy") as mock_copy:
                result = cli_runner.invoke(main, ["--sentence", "testInput"])

                assert result.exit_code == 0
                assert "Test result" in result.output
                mock_convert.assert_called_once_with("testInput")
                mock_copy.assert_called_once_with("Test result")

    def test_multiple_options_error(self, cli_runner):
        """Test that an error is raised when multiple conversion options are provided."""
        result = cli_runner.invoke(main, ["--snake", "--lower", "testInput"])

        assert result.exit_code != 0
        assert "Exactly one of --snake, --lower, or --sentence must be specified" in str(result.exception)

    def test_clipboard_error_handling(self, cli_runner):
        """Test that clipboard errors are handled gracefully."""
        with patch("nocamel.converters.to_sentence", return_value="Test result"):
            with patch.object(pyperclip, "copy", side_effect=Exception("Clipboard error")):
                result = cli_runner.invoke(main, ["testInput"])

                # Check that the command failed with a non-zero exit code
                assert result.exit_code != 0
                # Check that the error message contains our expected text
                assert "Failed to copy to clipboard" in result.output

    @patch("pyperclip.copy")
    def test_alternative_mock_approach(self, mock_copy, cli_runner):
        """Alternative approach to mocking using decorator."""
        with patch("nocamel.converters.to_sentence", return_value="Test result"):
            result = cli_runner.invoke(main, ["testInput"])

            assert result.exit_code == 0
            mock_copy.assert_called_once_with("Test result")

    @pytest.mark.parametrize(
        "option,converter_func,input_text,expected_output",
        [
            (None, "to_sentence", "testInput", "Test result"),
            ("--snake", "to_snake", "testInput", "test_result"),
            ("--lower", "to_lower", "testInput", "test result"),
            ("--sentence", "to_sentence", "testInput", "Test result"),
        ],
    )
    def test_conversion_options_parametrized(self, option, converter_func, input_text, expected_output, cli_runner):
        """Parametrized test covering all conversion options."""
        patch_path = f"nocamel.converters.{converter_func}"

        with patch(patch_path, return_value=expected_output) as mock_convert:
            with patch.object(pyperclip, "copy") as mock_copy:
                args = [input_text] if option is None else [option, input_text]
                result = cli_runner.invoke(main, args)

                assert result.exit_code == 0
                assert expected_output in result.output
                mock_convert.assert_called_once_with(input_text)
                mock_copy.assert_called_once_with(expected_output)
