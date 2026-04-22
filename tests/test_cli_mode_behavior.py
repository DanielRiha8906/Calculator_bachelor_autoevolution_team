"""Test CLI mode behavior and fast-fail semantics.

Verifies that CLI mode exits immediately on invalid input,
while interactive mode allows retries.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

from src.validation import OperandValidationSession, OperationValidationSession, detect_mode
from src.session import CalculatorSession
from src.core.calculator import Calculator


class TestCLIModeBehavior:
    """Test CLI mode behavior with mocked stdin."""

    def test_cli_mode_fast_fail_invalid_operation(self):
        """Test that CLI mode exits immediately on invalid operation."""
        operations = ["add", "subtract", "multiply"]
        session = OperationValidationSession(mode="cli", available_ops=operations)

        def prompt_fn():
            return "invalid_op"

        with pytest.raises(SystemExit):
            session.validate_input(prompt_fn)

    def test_cli_mode_fast_fail_invalid_operand(self):
        """Test that CLI mode exits immediately on invalid operand."""
        session = OperandValidationSession(mode="cli")

        def prompt_fn():
            return "not_a_number"

        with pytest.raises(SystemExit):
            session.validate_input(prompt_fn, "Invalid input:")

    def test_cli_mode_successful_operation(self):
        """Test that valid input succeeds in CLI mode."""
        operations = ["add", "subtract", "multiply"]
        session = OperationValidationSession(mode="cli", available_ops=operations)

        def prompt_fn():
            return "add"

        result = session.validate_input(prompt_fn)
        assert result == "add"

    def test_cli_mode_successful_operand(self):
        """Test that valid operand succeeds in CLI mode."""
        session = OperandValidationSession(mode="cli")

        def prompt_fn():
            return "3.14"

        result = session.validate_input(prompt_fn, "Invalid input:")
        assert result == 3.14

    def test_interactive_mode_reprompt_on_invalid_operand(self):
        """Test that interactive mode reprompts on invalid operand."""
        session = OperandValidationSession(mode="interactive", max_retries=3)

        call_count = [0]

        def prompt_fn():
            call_count[0] += 1
            if call_count[0] == 1:
                return "invalid"
            elif call_count[0] == 2:
                return "also_invalid"
            else:
                return "3.14"

        result = session.validate_input(prompt_fn, "Invalid input:")
        assert result == 3.14
        # Should have been called 3 times
        assert call_count[0] == 3

    def test_interactive_mode_reprompt_on_invalid_operation(self, capsys):
        """Test that interactive mode reprompts on invalid operation."""
        operations = ["add", "subtract", "multiply"]
        session = OperationValidationSession(mode="interactive", available_ops=operations)

        call_count = [0]

        def prompt_fn():
            call_count[0] += 1
            if call_count[0] == 1:
                return "invalid"
            else:
                return "add"

        result = session.validate_input(prompt_fn)
        assert result == "add"
        assert call_count[0] == 2

    def test_interactive_mode_retry_limit_exceeded(self):
        """Test that interactive mode returns None after retry limit."""
        session = OperandValidationSession(mode="interactive", max_retries=2)

        call_count = [0]

        def prompt_fn():
            call_count[0] += 1
            return "invalid"

        result = session.validate_input(prompt_fn, "Invalid input:")
        assert result is None
        # Should have been called max_retries times
        assert call_count[0] == 2

    def test_detect_mode_with_tty(self):
        """Test detect_mode returns 'interactive' when stdin is TTY."""
        with patch("sys.stdin.isatty", return_value=True):
            mode = detect_mode()
            assert mode == "interactive"

    def test_detect_mode_without_tty(self):
        """Test detect_mode returns 'cli' when stdin is not TTY."""
        with patch("sys.stdin.isatty", return_value=False):
            mode = detect_mode()
            assert mode == "cli"

    def test_cli_mode_no_retry_on_first_failure(self):
        """Test that CLI mode does not retry on any invalid input."""
        session = OperandValidationSession(mode="cli")

        call_count = [0]

        def prompt_fn():
            call_count[0] += 1
            return "not_a_number"

        with pytest.raises(SystemExit):
            session.validate_input(prompt_fn, "Invalid input:")

        # Should only be called once
        assert call_count[0] == 1

    def test_interactive_mode_case_insensitive_match(self):
        """Test that interactive mode matches operations case-insensitively."""
        operations = ["add", "subtract", "multiply"]
        session = OperationValidationSession(mode="interactive", available_ops=operations)

        def prompt_fn():
            return "ADD"

        result = session.validate_input(prompt_fn)
        assert result == "add"

    def test_cli_mode_case_insensitive_match(self):
        """Test that CLI mode matches operations case-insensitively."""
        operations = ["add", "subtract", "multiply"]
        session = OperationValidationSession(mode="cli", available_ops=operations)

        def prompt_fn():
            return "SUBTRACT"

        result = session.validate_input(prompt_fn)
        assert result == "subtract"

    def test_cli_mode_systemExit_includes_message(self):
        """Test that SystemExit in CLI mode includes descriptive message."""
        session = OperandValidationSession(mode="cli")

        def prompt_fn():
            return "not_a_number"

        with pytest.raises(SystemExit) as exc_info:
            session.validate_input(prompt_fn, "Invalid input:")

        # The exception should contain information about the invalid input
        assert "not_a_number" in str(exc_info.value) or "valid number" in str(exc_info.value)

    def test_cli_mode_operation_systemExit_includes_message(self):
        """Test that SystemExit for invalid operation includes descriptive message."""
        operations = ["add", "subtract"]
        session = OperationValidationSession(mode="cli", available_ops=operations)

        def prompt_fn():
            return "invalid_op"

        with pytest.raises(SystemExit) as exc_info:
            session.validate_input(prompt_fn)

        # The exception message should mention the invalid operation
        assert "invalid_op" in str(exc_info.value) or "valid operation" in str(exc_info.value)

    def test_interactive_mode_operation_attempt_count(self):
        """Test that interactive mode tracks attempt count for operations."""
        operations = ["add", "subtract"]
        session = OperationValidationSession(mode="interactive", available_ops=operations)

        assert session.attempt_count == 0

        call_count = [0]

        def prompt_fn():
            call_count[0] += 1
            if call_count[0] <= 2:
                return "invalid"
            return "add"

        session.validate_input(prompt_fn)
        # Should have incremented attempt count for each invalid attempt
        assert session.attempt_count == 0  # Reset after success

    def test_interactive_mode_reset_counter(self):
        """Test that successful input resets the attempt counter."""
        session = OperandValidationSession(mode="interactive", max_retries=3)

        call_count = [0]

        def prompt_fn():
            call_count[0] += 1
            if call_count[0] == 1:
                return "invalid"
            else:
                return "5.0"

        result = session.validate_input(prompt_fn, "Invalid input:")
        assert result == 5.0
        # Counter should be reset to 0 after successful input
        assert session.attempt_count == 0

    def test_session_collect_operands_cli_mode_fast_fail(self):
        """Test CalculatorSession.collect_operands in CLI mode with invalid input."""
        session = CalculatorSession(Calculator())

        def mock_input(prompt):
            return "not_a_number"

        with patch("builtins.input", side_effect=mock_input):
            with pytest.raises(SystemExit):
                session.collect_operands(arity=1, mode="cli")

    def test_session_collect_operands_interactive_mode_retries(self):
        """Test CalculatorSession.collect_operands in interactive mode with retries."""
        session = CalculatorSession(Calculator())

        inputs = ["invalid", "also_invalid", "3.14"]
        input_iter = iter(inputs)

        def mock_input(prompt):
            return next(input_iter)

        with patch("builtins.input", side_effect=mock_input):
            with patch("builtins.print"):  # Suppress print output
                operands, exit_code = session.collect_operands(arity=1, mode="interactive")

        assert operands == [3.14]
        assert exit_code == 0

    @pytest.mark.parametrize("mode,should_exit", [
        ("cli", True),
        ("interactive", False),
    ])
    def test_operand_validation_mode_behavior(self, mode, should_exit):
        """Test operand validation behavior differs between modes."""
        session = OperandValidationSession(mode=mode, max_retries=1)

        def prompt_fn():
            return "invalid"

        if should_exit:
            with pytest.raises(SystemExit):
                session.validate_input(prompt_fn, "Invalid input:")
        else:
            result = session.validate_input(prompt_fn, "Invalid input:")
            assert result is None
