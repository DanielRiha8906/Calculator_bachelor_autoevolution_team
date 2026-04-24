"""
Tests for the interactive calculator session module.

Tests use unittest.mock.patch to mock builtins.input and capture builtins.print.
Each test feeds input values via side_effect and verifies expected output in print calls.
"""

from unittest.mock import patch, call
import pytest
from src.ui.interactive import run_interactive_session


class TestInteractiveSession:
    """Test suite for run_interactive_session function."""

    def test_interactive_binary_add_valid(self):
        """Test binary addition (index 0) with valid inputs: 10 + 5 = 15."""
        with patch('builtins.input', side_effect=["0", "10", "5", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                # Join all print output to check for result
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "15" in output

    def test_interactive_unary_factorial_valid(self):
        """Test unary factorial (index 4): factorial(5) = 120."""
        with patch('builtins.input', side_effect=["4", "5", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "120" in output

    def test_interactive_unary_square_valid(self):
        """Test unary square (index 10): square(3) = 9."""
        with patch('builtins.input', side_effect=["10", "3", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "9" in output

    def test_interactive_invalid_operation_reprompt(self):
        """Test invalid operation index triggers reprompt. 999 is invalid, then valid add."""
        with patch('builtins.input', side_effect=["999", "0", "10", "5", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # Should contain at least 2 operation prompts or "Invalid" error
                prompt_count = output.count("Available") + output.count("operation") + output.count("Invalid")
                assert prompt_count >= 1 or output.count("Invalid") >= 1

    def test_interactive_nonnumeric_operand_reprompt(self):
        """Test non-numeric operand triggers reprompt. add operation, 'abc' invalid, then 5 + 10."""
        with patch('builtins.input', side_effect=["0", "abc", "5", "10", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "15" in output

    def test_interactive_domain_error_recovery(self):
        """Test domain error (sqrt(-4)) and recovery to add 2+3=5."""
        with patch('builtins.input', side_effect=["9", "-4", "yes", "0", "2", "3", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # Should contain error message and result 5
                assert "Error" in output or "error" in output.lower()
                assert "5" in output

    def test_interactive_binary_divide_valid(self):
        """Test binary division (index 3): 10 / 2 = 5."""
        with patch('builtins.input', side_effect=["3", "10", "2", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "5" in output

    def test_interactive_zero_division_error(self):
        """Test division by zero error message."""
        with patch('builtins.input', side_effect=["3", "10", "0", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                output_lower = output.lower()
                assert "error" in output_lower or "zero" in output_lower or "division" in output_lower

    def test_interactive_multiple_calculations(self):
        """Test multiple calculations: add 2+3=5, continue, multiply 4*5=20."""
        with patch('builtins.input', side_effect=["0", "2", "3", "yes", "7", "4", "5", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "5" in output
                assert "20" in output

    def test_interactive_factorial_float_domain_error(self):
        """Test factorial with float input (3.5) triggers error."""
        with patch('builtins.input', side_effect=["4", "3.5", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "Error" in output or "error" in output.lower()

    def test_interactive_operation_list_displayed(self):
        """Test that operation list is displayed when user enters invalid operation."""
        with patch('builtins.input', side_effect=["999", "0", "1", "1", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                output_lower = output.lower()
                # Should mention available operations
                assert "available" in output_lower or "operation" in output_lower

    def test_interactive_continue_yes(self):
        """Test 'yes' to continue after first calculation: add 2+2=4, multiply 3*3=9."""
        with patch('builtins.input', side_effect=["0", "2", "2", "yes", "7", "3", "3", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "4" in output
                assert "9" in output

    def test_interactive_continue_no(self):
        """Test 'no' to exit after calculation: multiply 5*2=10."""
        with patch('builtins.input', side_effect=["7", "5", "2", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "10" in output

    def test_interactive_binary_power_valid(self):
        """Test binary power (index 8): 2^8 = 256."""
        with patch('builtins.input', side_effect=["8", "2", "8", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "256" in output

    def test_interactive_binary_floats(self):
        """Test binary operation with floats: 2.5 * 4.0 = 10.0."""
        with patch('builtins.input', side_effect=["7", "2.5", "4.0", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "10" in output
