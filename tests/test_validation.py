"""Test suite for input validation and retry logic."""

import pytest
from unittest.mock import patch, MagicMock
import sys

from src.validation import (
    detect_mode,
    format_operation_error,
    OperandValidationSession,
    OperationValidationSession,
)


class TestDetectMode:
    """Test suite for detect_mode() function."""

    @patch("sys.stdin.isatty")
    def test_detect_mode_interactive(self, mock_isatty):
        """Should return 'interactive' when stdin is a TTY."""
        mock_isatty.return_value = True
        assert detect_mode() == "interactive"

    @patch("sys.stdin.isatty")
    def test_detect_mode_cli(self, mock_isatty):
        """Should return 'cli' when stdin is not a TTY."""
        mock_isatty.return_value = False
        assert detect_mode() == "cli"


class TestFormatOperationError:
    """Test suite for format_operation_error() function."""

    def test_format_operation_error_single_operation(self):
        """Should format error message with single operation."""
        result = format_operation_error(["add"])
        assert "Invalid operation" in result
        assert "add" in result
        assert "Available operations:" in result

    def test_format_operation_error_multiple_operations(self):
        """Should format error message with multiple operations."""
        ops = ["add", "subtract", "multiply"]
        result = format_operation_error(ops)
        assert "Invalid operation" in result
        assert "add" in result
        assert "subtract" in result
        assert "multiply" in result
        assert "Available operations:" in result

    def test_format_operation_error_comma_separated(self):
        """Should format operations as comma-separated list."""
        ops = ["add", "subtract", "multiply"]
        result = format_operation_error(ops)
        # Check that operations are joined by commas
        assert "add, subtract, multiply" in result

    def test_format_operation_error_many_operations(self):
        """Should handle a large list of operations."""
        ops = [
            "add", "subtract", "multiply", "divide", "power",
            "factorial", "square", "cube"
        ]
        result = format_operation_error(ops)
        assert "Invalid operation" in result
        assert all(op in result for op in ops)


class TestOperandValidationSessionInteractive:
    """Test suite for OperandValidationSession in interactive mode."""

    @pytest.fixture
    def session(self):
        """Fixture providing an interactive OperandValidationSession."""
        return OperandValidationSession(mode="interactive", max_retries=5)

    def test_session_initial_attempt_count(self, session):
        """Session should start with attempt_count = 0."""
        assert session.attempt_count == 0

    def test_session_attempt_count_property(self, session):
        """attempt_count property should reflect current count."""
        session._attempt_count = 3
        assert session.attempt_count == 3

    @patch("builtins.input")
    def test_valid_input_returns_float(self, mock_input, session):
        """Should return float when valid numeric input is provided."""
        mock_input.return_value = "5.5"
        result = session.validate_input(
            prompt_fn=mock_input,
            error_msg="Invalid input:"
        )
        assert result == 5.5
        assert isinstance(result, float)

    @patch("builtins.input")
    def test_valid_input_resets_counter(self, mock_input, session):
        """Should reset counter to 0 after successful parse."""
        session._attempt_count = 3
        mock_input.return_value = "10.0"
        result = session.validate_input(
            prompt_fn=mock_input,
            error_msg="Invalid input:"
        )
        assert result == 10.0
        assert session.attempt_count == 0

    @patch("builtins.input")
    @patch("builtins.print")
    def test_invalid_then_valid_retries(self, mock_print, mock_input, session):
        """Should retry after invalid input and accept valid input."""
        mock_input.side_effect = ["abc", "5.0"]
        result = session.validate_input(
            prompt_fn=mock_input,
            error_msg="Invalid input:"
        )
        assert result == 5.0
        assert mock_input.call_count == 2
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_multiple_invalid_inputs_before_success(self, mock_print, mock_input, session):
        """Should retry multiple times before accepting valid input."""
        mock_input.side_effect = ["abc", "1.2.3", "", "3.14"]
        result = session.validate_input(
            prompt_fn=mock_input,
            error_msg="Invalid input:"
        )
        assert result == 3.14
        assert mock_input.call_count == 4

    @patch("builtins.input")
    @patch("builtins.print")
    def test_five_consecutive_failures_returns_none(self, mock_print, mock_input, session):
        """Should return None after 5 consecutive invalid inputs."""
        mock_input.side_effect = ["a", "b", "c", "d", "e"]
        result = session.validate_input(
            prompt_fn=mock_input,
            error_msg="Invalid input:"
        )
        assert result is None
        assert session.attempt_count == 5

    @patch("builtins.input")
    @patch("builtins.print")
    def test_five_consecutive_failures_prints_termination_message(self, mock_print, mock_input, session):
        """Should print termination message after 5 consecutive failures."""
        mock_input.side_effect = ["a", "b", "c", "d", "e"]
        session.validate_input(
            prompt_fn=mock_input,
            error_msg="Invalid input:"
        )
        # Check that termination message was printed
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        assert any("Maximum retry attempts" in str(output) for output in printed_output)
        assert any("Session terminated" in str(output) for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_counter_resets_mid_sequence(self, mock_print, mock_input, session):
        """Counter should reset on success, allowing new series of 5 failures."""
        # First: 2 failures, then success (counter resets)
        # Then: 5 new failures (counter reaches 5 and returns None)
        mock_input.side_effect = ["a", "b", "3.0", "x", "y", "z", "w", "v"]

        # First call: 2 fails + success
        result1 = session.validate_input(
            prompt_fn=lambda: mock_input(),
            error_msg="Invalid input:"
        )
        assert result1 == 3.0
        assert session.attempt_count == 0

        # Second call: 5 new failures
        result2 = session.validate_input(
            prompt_fn=lambda: mock_input(),
            error_msg="Invalid input:"
        )
        assert result2 is None
        assert session.attempt_count == 5

    @patch("builtins.input")
    def test_reset_counter_method(self, mock_input, session):
        """reset_counter() should set attempt_count to 0."""
        session._attempt_count = 3
        session.reset_counter()
        assert session.attempt_count == 0

    @patch("builtins.input")
    def test_parse_integer_as_float(self, mock_input, session):
        """Should parse integer strings as floats."""
        mock_input.return_value = "42"
        result = session.validate_input(
            prompt_fn=mock_input,
            error_msg="Invalid input:"
        )
        assert result == 42.0

    @patch("builtins.input")
    def test_parse_negative_number(self, mock_input, session):
        """Should parse negative numbers."""
        mock_input.return_value = "-5.5"
        result = session.validate_input(
            prompt_fn=mock_input,
            error_msg="Invalid input:"
        )
        assert result == -5.5

    @patch("builtins.input")
    def test_parse_scientific_notation(self, mock_input, session):
        """Should parse scientific notation."""
        mock_input.return_value = "1e-3"
        result = session.validate_input(
            prompt_fn=mock_input,
            error_msg="Invalid input:"
        )
        assert result == 0.001

    @patch("builtins.input")
    def test_parse_zero(self, mock_input, session):
        """Should parse zero correctly."""
        mock_input.return_value = "0"
        result = session.validate_input(
            prompt_fn=mock_input,
            error_msg="Invalid input:"
        )
        assert result == 0.0

    @patch("builtins.input")
    @patch("builtins.print")
    def test_error_message_printed_on_invalid(self, mock_print, mock_input, session):
        """Should print provided error message on invalid input."""
        mock_input.side_effect = ["invalid", "5.0"]
        session.validate_input(
            prompt_fn=mock_input,
            error_msg="Custom error:"
        )
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        assert any("Custom error:" in str(output) for output in printed_output)

    @patch("builtins.input")
    def test_custom_max_retries(self, mock_input):
        """Should respect custom max_retries value."""
        session = OperandValidationSession(mode="interactive", max_retries=2)
        mock_input.side_effect = ["a", "b"]
        with patch("builtins.print"):
            result = session.validate_input(
                prompt_fn=mock_input,
                error_msg="Invalid input:"
            )
        assert result is None
        assert session.attempt_count == 2


class TestOperandValidationSessionCLI:
    """Test suite for OperandValidationSession in CLI mode."""

    @pytest.fixture
    def session(self):
        """Fixture providing a CLI-mode OperandValidationSession."""
        return OperandValidationSession(mode="cli", max_retries=5)

    @patch("builtins.input")
    def test_cli_mode_valid_input_returns_float(self, mock_input, session):
        """CLI mode should return float for valid input."""
        mock_input.return_value = "5.5"
        result = session.validate_input(
            prompt_fn=mock_input,
            error_msg="Invalid input:"
        )
        assert result == 5.5

    @patch("builtins.input")
    def test_cli_mode_invalid_input_raises_system_exit(self, mock_input, session):
        """CLI mode should raise SystemExit on invalid input."""
        mock_input.return_value = "invalid"
        with pytest.raises(SystemExit):
            session.validate_input(
                prompt_fn=mock_input,
                error_msg="Invalid input:"
            )

    @patch("builtins.input")
    def test_cli_mode_no_retry_on_invalid(self, mock_input, session):
        """CLI mode should not retry; should fail on first invalid input."""
        mock_input.return_value = "invalid"
        try:
            session.validate_input(
                prompt_fn=mock_input,
                error_msg="Invalid input:"
            )
        except SystemExit:
            pass
        # Should only call input once (no retries)
        assert mock_input.call_count == 1

    @patch("builtins.input")
    def test_cli_mode_does_not_increment_attempt_count(self, mock_input, session):
        """CLI mode should not increment attempt_count (exits immediately)."""
        mock_input.return_value = "invalid"
        try:
            session.validate_input(
                prompt_fn=mock_input,
                error_msg="Invalid input:"
            )
        except SystemExit:
            pass
        # In CLI mode, counter should not be incremented
        assert session.attempt_count == 0


class TestOperationValidationSessionInteractive:
    """Test suite for OperationValidationSession in interactive mode."""

    @pytest.fixture
    def session(self):
        """Fixture providing an interactive OperationValidationSession."""
        return OperationValidationSession(
            mode="interactive",
            available_ops=["add", "subtract", "multiply"],
            max_retries=5
        )

    def test_session_initial_attempt_count(self, session):
        """Session should start with attempt_count = 0."""
        assert session.attempt_count == 0

    def test_session_attempt_count_property(self, session):
        """attempt_count property should reflect current count."""
        session._attempt_count = 2
        assert session.attempt_count == 2

    @patch("builtins.input")
    def test_valid_operation_returns_matched_name(self, mock_input, session):
        """Should return matched operation name for valid input."""
        mock_input.return_value = "add"
        result = session.validate_input(prompt_fn=mock_input)
        assert result == "add"

    @patch("builtins.input")
    def test_valid_operation_case_insensitive(self, mock_input, session):
        """Should match operation case-insensitively."""
        mock_input.return_value = "ADD"
        result = session.validate_input(prompt_fn=mock_input)
        assert result == "add"

    @patch("builtins.input")
    def test_valid_operation_mixed_case(self, mock_input, session):
        """Should match operation with mixed case input."""
        mock_input.return_value = "MuLtIpLy"
        result = session.validate_input(prompt_fn=mock_input)
        assert result == "multiply"

    @patch("builtins.input")
    def test_valid_operation_resets_counter(self, mock_input, session):
        """Should reset counter to 0 after successful match."""
        session._attempt_count = 3
        mock_input.return_value = "subtract"
        result = session.validate_input(prompt_fn=mock_input)
        assert result == "subtract"
        assert session.attempt_count == 0

    @patch("builtins.input")
    @patch("builtins.print")
    def test_invalid_then_valid_retries(self, mock_print, mock_input, session):
        """Should retry after invalid operation and accept valid one."""
        mock_input.side_effect = ["invalid", "add"]
        result = session.validate_input(prompt_fn=mock_input)
        assert result == "add"
        assert mock_input.call_count == 2
        assert mock_print.called

    @patch("builtins.input")
    @patch("builtins.print")
    def test_five_consecutive_failures_returns_none(self, mock_print, mock_input, session):
        """Should return None after 5 consecutive invalid inputs."""
        mock_input.side_effect = ["bad1", "bad2", "bad3", "bad4", "bad5"]
        result = session.validate_input(prompt_fn=mock_input)
        assert result is None
        assert session.attempt_count == 5

    @patch("builtins.input")
    @patch("builtins.print")
    def test_five_consecutive_failures_prints_termination_message(self, mock_print, mock_input, session):
        """Should print termination message after 5 consecutive failures."""
        mock_input.side_effect = ["bad1", "bad2", "bad3", "bad4", "bad5"]
        session.validate_input(prompt_fn=mock_input)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        assert any("Maximum retry attempts" in str(output) for output in printed_output)
        assert any("Session terminated" in str(output) for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_error_message_includes_available_operations(self, mock_print, mock_input, session):
        """Error message should include available operations."""
        mock_input.side_effect = ["invalid", "add"]
        session.validate_input(prompt_fn=mock_input)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        output_str = " ".join(str(output) for output in printed_output)
        assert "Invalid operation" in output_str
        assert "add" in output_str
        assert "subtract" in output_str
        assert "multiply" in output_str

    @patch("builtins.input")
    @patch("builtins.print")
    def test_counter_resets_mid_sequence(self, mock_print, mock_input, session):
        """Counter should reset on success, allowing new series of 5 failures."""
        # First: 2 failures, then success (counter resets)
        # Then: 5 new failures (counter reaches 5 and returns None)
        mock_input.side_effect = [
            "bad1", "bad2", "add",  # 2 failures + success
            "bad3", "bad4", "bad5", "bad6", "bad7"  # 5 new failures
        ]

        # First call: 2 fails + success
        result1 = session.validate_input(prompt_fn=lambda: mock_input())
        assert result1 == "add"
        assert session.attempt_count == 0

        # Second call: 5 new failures
        with patch("builtins.print"):
            result2 = session.validate_input(prompt_fn=lambda: mock_input())
        assert result2 is None
        assert session.attempt_count == 5

    @patch("builtins.input")
    def test_reset_counter_method(self, mock_input, session):
        """reset_counter() should set attempt_count to 0."""
        session._attempt_count = 3
        session.reset_counter()
        assert session.attempt_count == 0

    @patch("builtins.input")
    def test_input_with_whitespace_stripped(self, mock_input, session):
        """Should strip whitespace from input."""
        mock_input.return_value = "  add  "
        result = session.validate_input(prompt_fn=mock_input)
        assert result == "add"

    @patch("builtins.input")
    def test_custom_max_retries(self, mock_input):
        """Should respect custom max_retries value."""
        session = OperationValidationSession(
            mode="interactive",
            available_ops=["add"],
            max_retries=2
        )
        mock_input.side_effect = ["bad1", "bad2"]
        with patch("builtins.print"):
            result = session.validate_input(prompt_fn=mock_input)
        assert result is None
        assert session.attempt_count == 2


class TestOperationValidationSessionCLI:
    """Test suite for OperationValidationSession in CLI mode."""

    @pytest.fixture
    def session(self):
        """Fixture providing a CLI-mode OperationValidationSession."""
        return OperationValidationSession(
            mode="cli",
            available_ops=["add", "subtract", "multiply"],
            max_retries=5
        )

    @patch("builtins.input")
    def test_cli_mode_valid_operation_returns_matched_name(self, mock_input, session):
        """CLI mode should return matched operation for valid input."""
        mock_input.return_value = "add"
        result = session.validate_input(prompt_fn=mock_input)
        assert result == "add"

    @patch("builtins.input")
    def test_cli_mode_invalid_operation_raises_system_exit(self, mock_input, session):
        """CLI mode should raise SystemExit on invalid operation."""
        mock_input.return_value = "invalid"
        with pytest.raises(SystemExit):
            session.validate_input(prompt_fn=mock_input)

    @patch("builtins.input")
    def test_cli_mode_invalid_operation_no_retry(self, mock_input, session):
        """CLI mode should not retry; should fail on first invalid operation."""
        mock_input.return_value = "invalid"
        try:
            session.validate_input(prompt_fn=mock_input)
        except SystemExit:
            pass
        # Should only call input once (no retries)
        assert mock_input.call_count == 1

    @patch("builtins.input")
    @patch("builtins.print")
    def test_cli_mode_invalid_operation_prints_error_message(self, mock_print, mock_input, session):
        """CLI mode should print available operations error on invalid input."""
        mock_input.return_value = "invalid"
        try:
            session.validate_input(prompt_fn=mock_input)
        except SystemExit:
            pass
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        output_str = " ".join(str(output) for output in printed_output)
        assert "Invalid operation" in output_str
        assert any(op in output_str for op in ["add", "subtract", "multiply"])

    @patch("builtins.input")
    def test_cli_mode_case_insensitive_match(self, mock_input, session):
        """CLI mode should match operation case-insensitively."""
        mock_input.return_value = "SUBTRACT"
        result = session.validate_input(prompt_fn=mock_input)
        assert result == "subtract"

    @patch("builtins.input")
    def test_cli_mode_does_not_increment_attempt_count(self, mock_input, session):
        """CLI mode should not increment attempt_count (exits immediately)."""
        mock_input.return_value = "invalid"
        try:
            session.validate_input(prompt_fn=mock_input)
        except SystemExit:
            pass
        # In CLI mode, counter should not be incremented
        assert session.attempt_count == 0
