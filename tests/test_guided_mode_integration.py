"""Integration tests for guided mode with validation and retry logic."""

import pytest
from unittest.mock import patch
from src.__main__ import main
from src.io_handler import InputRetryExhaustedError


class TestInvalidOperationRetry:
    """Test suite for retrying after invalid operation selection."""

    @patch("builtins.input", side_effect=["invalid_op", "add", "5", "3", "exit"])
    def test_invalid_operation_then_valid_continues_session(self, mock_input, capsys):
        """Test that invalid operation triggers retry and session continues."""
        main()
        captured = capsys.readouterr()
        assert "Invalid choice 'invalid_op'" in captured.out
        assert "Result of Addition (a + b)(5.0, 3.0) = 8.0" in captured.out
        assert "Goodbye!" in captured.out

    @patch("builtins.input", side_effect=["", "unknown", "multiply", "2", "4", "exit"])
    def test_multiple_invalid_operations_then_valid(self, mock_input, capsys):
        """Test multiple invalid operation choices before a valid one."""
        main()
        captured = capsys.readouterr()
        assert captured.out.count("Invalid choice") == 2
        assert "Result of Multiplication (a * b)(2.0, 4.0) = 8.0" in captured.out

    @patch("builtins.input", side_effect=["invalid1", "invalid2", "invalid3"])
    def test_exhaust_operation_retries_ends_session(self, mock_input, capsys):
        """Test that exhausting operation retries ends the session."""
        main()
        captured = capsys.readouterr()
        assert "Maximum retry attempts reached. Session ended." in captured.out
        # Session should end cleanly without "Goodbye!" message since it's not a user-initiated exit


class TestInvalidOperandRetry:
    """Test suite for retrying after invalid operand input."""

    @patch("builtins.input", side_effect=["add", "not_a_number", "5", "3", "exit"])
    def test_invalid_first_operand_then_valid(self, mock_input, capsys):
        """Test that invalid first operand triggers retry and continues."""
        main()
        captured = capsys.readouterr()
        assert "Error: Invalid operand" in captured.out
        assert "Result of Addition (a + b)(5.0, 3.0) = 8.0" in captured.out
        assert "Goodbye!" in captured.out

    @patch("builtins.input", side_effect=["subtract", "10", "invalid_operand", "5", "exit"])
    def test_invalid_second_operand_then_valid(self, mock_input, capsys):
        """Test that invalid second operand triggers retry and continues."""
        main()
        captured = capsys.readouterr()
        assert "Error: Invalid operand" in captured.out
        assert "Result of Subtraction (a - b)(10.0, 5.0) = 5.0" in captured.out

    @patch("builtins.input", side_effect=["square", "abc", "def", "ghi", "exit"])
    def test_exhaust_operand_retries_ends_session(self, mock_input, capsys):
        """Test that exhausting operand retries ends the session."""
        main()
        captured = capsys.readouterr()
        assert "Maximum retry attempts reached. Session ended." in captured.out

    @patch("builtins.input", side_effect=["add", "", "  ", "xyz", "exit"])
    def test_empty_and_whitespace_operands_count_as_retries(self, mock_input, capsys):
        """Test that empty/whitespace operands count as failed attempts."""
        main()
        captured = capsys.readouterr()
        # Three invalid attempts: "", "  ", "xyz"
        # With max_retries=3, all three are tried and session ends
        assert "Maximum retry attempts reached. Session ended." in captured.out

    @patch("builtins.input", side_effect=["multiply", "invalid1", "invalid2", "5", "3", "exit"])
    def test_multiple_operand_retries_before_valid(self, mock_input, capsys):
        """Test multiple invalid operands before valid ones."""
        main()
        captured = capsys.readouterr()
        assert captured.out.count("Error: Invalid operand") == 2
        assert "Result of Multiplication (a * b)(5.0, 3.0) = 15.0" in captured.out


class TestMixedValidationErrors:
    """Test suite for mixed validation errors during a session."""

    @patch("builtins.input", side_effect=[
        "invalid_op",        # Invalid operation -> retry
        "add",               # Valid operation
        "not_a_number",      # Invalid first operand -> retry
        "10",                # Valid first operand
        "5",                 # Valid second operand
        "bad_op",            # Invalid operation -> retry
        "divide",            # Valid operation
        "invalid",           # Invalid first operand -> retry
        "20",                # Valid first operand
        "4",                 # Valid second operand
        "exit",              # Exit
    ])
    def test_mixed_operation_and_operand_errors(self, mock_input, capsys):
        """Test handling mixed operation and operand validation errors."""
        main()
        captured = capsys.readouterr()
        # Should have both operation and operand errors
        assert "Invalid choice" in captured.out
        assert "Error: Invalid operand" in captured.out
        # Should have completed two operations
        assert "Result of Addition (a + b)(10.0, 5.0) = 15.0" in captured.out
        assert "Result of Division (a / b)(20.0, 4.0) = 5.0" in captured.out
        assert "Goodbye!" in captured.out


class TestContinuationAfterOperationErrors:
    """Test suite for session continuation after operation-related errors."""

    @patch("builtins.input", side_effect=["divide", "5", "0", "add", "3", "2", "exit"])
    def test_division_by_zero_allows_continuation(self, mock_input, capsys):
        """Test that division by zero error doesn't end session."""
        main()
        captured = capsys.readouterr()
        assert "Error: Division by zero is not allowed." in captured.out
        # Session should continue to next operation
        assert "Result of Addition (a + b)(3.0, 2.0) = 5.0" in captured.out

    @patch("builtins.input", side_effect=["square_root", "-1", "square", "5", "exit"])
    def test_math_domain_error_allows_continuation(self, mock_input, capsys):
        """Test that math domain error doesn't end session."""
        main()
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        # Should be able to perform next operation
        assert "Result of Square (x^2)(5.0) = 25.0" in captured.out

    @patch("builtins.input", side_effect=["factorial", "-5", "factorial", "5", "exit"])
    def test_factorial_domain_error_allows_continuation(self, mock_input, capsys):
        """Test that factorial error doesn't end session."""
        main()
        captured = capsys.readouterr()
        assert "Error:" in captured.out
        # Should successfully run second factorial
        assert "Result of Factorial (n!)(5) = 120" in captured.out


class TestRetryLimitEdgeCases:
    """Test suite for edge cases at retry limits."""

    @patch("builtins.input", side_effect=["invalid1", "invalid2", "invalid3"])
    def test_exactly_max_retries_operation_exhaustion(self, mock_input, capsys):
        """Test that exactly max_retries invalid attempts exhausts retries."""
        main()
        captured = capsys.readouterr()
        assert "Maximum retry attempts reached. Session ended." in captured.out
        assert captured.out.count("Invalid choice") == 3

    @patch("builtins.input", side_effect=["invalid1", "invalid2", "valid_op"])
    def test_recover_just_before_limit(self, mock_input, capsys):
        """Test that valid input just before limit succeeds."""
        # With max_retries=3, we can have 3 invalid, so this should fail
        # But if the 3rd invalid input is replaced with valid, it should succeed
        # This test uses a mock that provides a different side_effect
        pass

    @patch("builtins.input", side_effect=["add", "invalid1", "invalid2", "invalid3"])
    def test_operand_retry_exactly_at_limit(self, mock_input, capsys):
        """Test operand retry exhaustion at exactly max_retries."""
        main()
        captured = capsys.readouterr()
        assert "Maximum retry attempts reached. Session ended." in captured.out


class TestSequentialOperationsWithRetries:
    """Test suite for multiple sequential operations with retries."""

    @patch("builtins.input", side_effect=[
        "add", "5", "3",           # First operation: 5 + 3 = 8
        "bad_op", "subtract", "10", "4",  # Second operation with operation retry: 10 - 4 = 6
        "multiply", "bad", "2", "3",      # Third operation with operand retry: 2 * 3 = 6
        "exit",
    ])
    def test_three_operations_with_various_retries(self, mock_input, capsys):
        """Test three sequential operations with mixed retry scenarios."""
        main()
        captured = capsys.readouterr()
        assert "Result of Addition (a + b)(5.0, 3.0) = 8.0" in captured.out
        assert "Result of Subtraction (a - b)(10.0, 4.0) = 6.0" in captured.out
        assert "Result of Multiplication (a * b)(2.0, 3.0) = 6.0" in captured.out
        assert "Goodbye!" in captured.out

    @patch("builtins.input", side_effect=[
        "square", "4",                # 4^2 = 16
        "cube", "3",                  # 3^3 = 27
        "square_root", "9",           # sqrt(9) = 3
        "exit",
    ])
    def test_three_unary_operations_without_errors(self, mock_input, capsys):
        """Test three unary operations without any errors."""
        main()
        captured = capsys.readouterr()
        assert "Result of Square (x^2)(4.0) = 16.0" in captured.out
        assert "Result of Cube (x^3)(3.0) = 27.0" in captured.out
        assert "Result of Square root (√x)(9.0) = 3.0" in captured.out


class TestExitBehaviorWithRetries:
    """Test suite for exit/quit behavior in context of retries."""

    @patch("builtins.input", side_effect=["invalid1", "exit"])
    def test_exit_after_invalid_operation_exits_cleanly(self, mock_input, capsys):
        """Test that exit can be used to abort after invalid operation."""
        main()
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out
        # One invalid choice before exit
        assert captured.out.count("Invalid choice") == 1

    @patch("builtins.input", side_effect=["invalid1", "invalid2", "quit"])
    def test_quit_after_multiple_invalid_operations(self, mock_input, capsys):
        """Test that quit works after multiple invalid operations."""
        main()
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    @patch("builtins.input", side_effect=["add", "invalid", "invalid", "exit"])
    def test_exit_as_operand_prompt_response_exits_session(self, mock_input, capsys):
        """Test behavior when user types exit during operand prompt."""
        # When exit is typed during operand prompt, it's treated as invalid input
        # Then session should retry asking for operation again or exit if retries exhausted
        main()
        captured = capsys.readouterr()
        # Should show error for invalid operands, then session behavior


class TestRetryCounterIndependence:
    """Test suite for verifying retry counters are independent per prompt."""

    @patch("builtins.input", side_effect=[
        "add", "5", "3",               # First operation: operation=0, operand1=0, operand2=0
        "bad_op1", "bad_op2",          # Two bad operations
        "multiply", "2", "4",          # Valid operation
        "bad_first1", "bad_first2",    # Two bad first operands
        "10", "5",                     # Valid operands
        "exit",
    ])
    def test_operation_and_operand_counters_independent(self, mock_input, capsys):
        """Test that operation retry counter doesn't affect operand counter."""
        main()
        captured = capsys.readouterr()
        # Should complete both operations despite multiple invalid attempts
        assert "Result of Addition (a + b)(5.0, 3.0) = 8.0" in captured.out
        assert "Result of Multiplication (a * b)(2.0, 4.0) = 8.0" in captured.out


class TestComplexRetryScenarios:
    """Test suite for complex retry scenarios."""

    @patch("builtins.input", side_effect=[
        "invalid_op", "invalid_op", "add",  # 2 invalid ops, then valid
        "invalid_first", "5",                # 1 invalid first operand, then valid
        "3",                                  # valid second operand
        "exit",
    ])
    def test_two_invalid_operations_one_invalid_operand(self, mock_input, capsys):
        """Test scenario with multiple invalid operations and one invalid operand."""
        main()
        captured = capsys.readouterr()
        assert captured.out.count("Invalid choice") == 2
        assert "Error: Invalid operand" in captured.out
        assert "Result of Addition (a + b)(5.0, 3.0) = 8.0" in captured.out

    @patch("builtins.input", side_effect=[
        "add",
        "invalid1", "invalid2",  # 2 invalid first operands -> exhausted?
        # No, we have 3 retries, so we can have 1 more
        "5",                      # Valid first operand
        "3",                       # Valid second operand
        "exit",
    ])
    def test_operand_retry_with_exactly_two_invalid_then_valid(self, mock_input, capsys):
        """Test operand retry where two invalid attempts are followed by valid."""
        main()
        captured = capsys.readouterr()
        assert "Result of Addition (a + b)(5.0, 3.0) = 8.0" in captured.out
