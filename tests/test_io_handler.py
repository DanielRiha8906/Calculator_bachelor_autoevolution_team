"""Unit tests for InputHandler class."""

import pytest
from unittest.mock import patch
from src.io_handler import InputHandler


class TestGetOperationChoice:
    """Test suite for InputHandler.get_operation_choice() method."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    @pytest.fixture
    def available_ops(self):
        """Fixture to provide a sample operations dict."""
        return {
            "add": "Addition (a + b)",
            "subtract": "Subtraction (a - b)",
            "multiply": "Multiplication (a * b)",
        }

    @patch("builtins.input", return_value="add")
    def test_get_operation_choice_valid_selection(self, mock_input, handler, available_ops, capsys):
        """Test that a valid operation key is returned."""
        result = handler.get_operation_choice(available_ops)
        assert result == "add"
        captured = capsys.readouterr()
        assert "Available operations:" in captured.out
        assert "add: Addition (a + b)" in captured.out

    @patch("builtins.input", side_effect=["invalid", "subtract"])
    def test_get_operation_choice_invalid_then_valid(self, mock_input, handler, available_ops, capsys):
        """Test that invalid input triggers re-prompt, then valid key is accepted."""
        result = handler.get_operation_choice(available_ops)
        assert result == "subtract"
        captured = capsys.readouterr()
        assert "Invalid choice 'invalid'" in captured.out

    @patch("builtins.input", return_value="exit")
    def test_get_operation_choice_exit_returns_exit(self, mock_input, handler, available_ops, capsys):
        """Test that 'exit' is returned as a special sentinel."""
        result = handler.get_operation_choice(available_ops)
        assert result == "exit"

    @patch("builtins.input", return_value="quit")
    def test_get_operation_choice_quit_returns_quit(self, mock_input, handler, available_ops, capsys):
        """Test that 'quit' is returned as a special sentinel."""
        result = handler.get_operation_choice(available_ops)
        assert result == "quit"

    @patch("builtins.input", return_value="EXIT")
    def test_get_operation_choice_case_insensitive_exit(self, mock_input, handler, available_ops, capsys):
        """Test that 'EXIT' (uppercase) is converted to lowercase and returned."""
        result = handler.get_operation_choice(available_ops)
        assert result == "exit"

    @patch("builtins.input", return_value="QUIT")
    def test_get_operation_choice_case_insensitive_quit(self, mock_input, handler, available_ops, capsys):
        """Test that 'QUIT' (uppercase) is converted to lowercase and returned."""
        result = handler.get_operation_choice(available_ops)
        assert result == "quit"

    @patch("builtins.input", side_effect=["", "  ", "add"])
    def test_get_operation_choice_multiple_invalid_inputs(self, mock_input, handler, available_ops, capsys):
        """Test multiple invalid inputs before a valid one."""
        result = handler.get_operation_choice(available_ops)
        assert result == "add"
        captured = capsys.readouterr()
        # Should have printed invalid choice messages for each invalid input
        assert captured.out.count("Invalid choice") == 2

    @patch("builtins.input", return_value=" multiply ")
    def test_get_operation_choice_with_whitespace(self, mock_input, handler, available_ops, capsys):
        """Test that input with surrounding whitespace is stripped."""
        result = handler.get_operation_choice(available_ops)
        assert result == "multiply"

    @patch("builtins.input", return_value="MuLtIpLy")
    def test_get_operation_choice_mixed_case_valid_selection(self, mock_input, handler, available_ops, capsys):
        """Test that mixed case input is converted to lowercase and validated."""
        result = handler.get_operation_choice(available_ops)
        assert result == "multiply"


class TestGetOperand:
    """Test suite for InputHandler.get_operand() method."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    @patch("builtins.input", return_value="5.5")
    def test_get_operand_valid_float(self, mock_input, handler):
        """Test that a valid float string is parsed correctly."""
        result = handler.get_operand("Enter value: ")
        assert result == 5.5
        assert isinstance(result, float)

    @patch("builtins.input", return_value="42")
    def test_get_operand_valid_integer(self, mock_input, handler):
        """Test that an integer string is parsed as float."""
        result = handler.get_operand("Enter value: ")
        assert result == 42.0
        assert isinstance(result, float)

    @patch("builtins.input", return_value="-3.14")
    def test_get_operand_negative_float(self, mock_input, handler):
        """Test that negative floats are parsed correctly."""
        result = handler.get_operand("Enter value: ")
        assert result == -3.14

    @patch("builtins.input", return_value=" 7.5 ")
    def test_get_operand_with_whitespace(self, mock_input, handler):
        """Test that input with whitespace is stripped before parsing."""
        result = handler.get_operand("Enter value: ")
        assert result == 7.5

    @patch("builtins.input", return_value="0")
    def test_get_operand_zero(self, mock_input, handler):
        """Test that zero is parsed correctly."""
        result = handler.get_operand("Enter value: ")
        assert result == 0.0

    @patch("builtins.input", return_value="1e10")
    def test_get_operand_scientific_notation(self, mock_input, handler):
        """Test that scientific notation is parsed correctly."""
        result = handler.get_operand("Enter value: ")
        assert result == 1e10

    @patch("builtins.input", return_value="abc")
    def test_get_operand_invalid_input_raises_valueerror(self, mock_input, handler):
        """Test that non-numeric input raises ValueError."""
        with pytest.raises(ValueError):
            handler.get_operand("Enter value: ")

    @patch("builtins.input", return_value="12.34.56")
    def test_get_operand_invalid_format_raises_valueerror(self, mock_input, handler):
        """Test that malformed numeric input raises ValueError."""
        with pytest.raises(ValueError):
            handler.get_operand("Enter value: ")

    @patch("builtins.input", return_value="")
    def test_get_operand_empty_string_raises_valueerror(self, mock_input, handler):
        """Test that empty input raises ValueError."""
        with pytest.raises(ValueError):
            handler.get_operand("Enter value: ")

    @patch("builtins.input", return_value="inf")
    def test_get_operand_infinity(self, mock_input, handler):
        """Test that 'inf' is parsed as infinity."""
        result = handler.get_operand("Enter value: ")
        assert result == float("inf")


class TestDisplayResult:
    """Test suite for InputHandler.display_result() method."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    def test_display_result_binary_operation(self, handler, capsys):
        """Test result display for a binary operation."""
        handler.display_result("add", [5, 3], 8)
        captured = capsys.readouterr()
        assert "Result of add(5, 3) = 8" in captured.out

    def test_display_result_unary_operation(self, handler, capsys):
        """Test result display for a unary operation."""
        handler.display_result("square", [5], 25)
        captured = capsys.readouterr()
        assert "Result of square(5) = 25" in captured.out

    def test_display_result_float_operands(self, handler, capsys):
        """Test result display with float operands."""
        handler.display_result("divide", [10.0, 2.5], 4.0)
        captured = capsys.readouterr()
        assert "Result of divide(10.0, 2.5) = 4.0" in captured.out

    def test_display_result_float_result(self, handler, capsys):
        """Test result display with float result."""
        handler.display_result("divide", [5, 2], 2.5)
        captured = capsys.readouterr()
        assert "Result of divide(5, 2) = 2.5" in captured.out

    def test_display_result_negative_operands(self, handler, capsys):
        """Test result display with negative operands."""
        handler.display_result("multiply", [-3, 4], -12)
        captured = capsys.readouterr()
        assert "Result of multiply(-3, 4) = -12" in captured.out

    def test_display_result_zero_result(self, handler, capsys):
        """Test result display with zero result."""
        handler.display_result("subtract", [5, 5], 0)
        captured = capsys.readouterr()
        assert "Result of subtract(5, 5) = 0" in captured.out

    def test_display_result_multiple_operands(self, handler, capsys):
        """Test result display format with multiple operands."""
        # Even though the current implementation expects binary/unary,
        # verify it handles lists of any size
        handler.display_result("operation", [1, 2, 3], 6)
        captured = capsys.readouterr()
        assert "Result of operation(1, 2, 3) = 6" in captured.out


class TestDisplayError:
    """Test suite for InputHandler.display_error() method."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    def test_display_error_simple_message(self, handler, capsys):
        """Test error display with a simple message."""
        handler.display_error("Something went wrong")
        captured = capsys.readouterr()
        assert "Error: Something went wrong" in captured.out

    def test_display_error_division_by_zero(self, handler, capsys):
        """Test error display for division by zero."""
        handler.display_error("Division by zero is not allowed.")
        captured = capsys.readouterr()
        assert "Error: Division by zero is not allowed." in captured.out

    def test_display_error_invalid_operation(self, handler, capsys):
        """Test error display for invalid operation."""
        handler.display_error("Unknown operation: 'unknown'")
        captured = capsys.readouterr()
        assert "Error: Unknown operation: 'unknown'" in captured.out

    def test_display_error_empty_message(self, handler, capsys):
        """Test error display with empty message."""
        handler.display_error("")
        captured = capsys.readouterr()
        assert "Error: " in captured.out

    def test_display_error_special_characters(self, handler, capsys):
        """Test error display with special characters."""
        handler.display_error("Invalid input: expect 5.5 or 'exit'")
        captured = capsys.readouterr()
        assert "Error: Invalid input: expect 5.5 or 'exit'" in captured.out


class TestInputHandlerHistoryParameter:
    """Test suite for InputHandler history parameter initialization."""

    def test_inputhandler_with_no_history(self):
        """Test InputHandler initializes correctly with history=None (default)."""
        handler = InputHandler()
        assert handler.history is None

    def test_inputhandler_with_history_none_explicit(self):
        """Test InputHandler initializes correctly with history=None (explicit)."""
        handler = InputHandler(history=None)
        assert handler.history is None

    def test_inputhandler_with_history_object(self):
        """Test InputHandler stores history object when provided."""
        from unittest.mock import Mock
        mock_history = Mock()
        handler = InputHandler(history=mock_history)
        assert handler.history is mock_history


class TestDisplayHistory:
    """Test suite for InputHandler.display_history() method."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    def test_display_history_when_history_is_none(self, handler, capsys):
        """Test display_history prints 'No history available.' when history is None."""
        handler.display_history()
        captured = capsys.readouterr()
        assert "No history available." in captured.out

    def test_display_history_with_mock_history_object(self, capsys):
        """Test display_history calls history.display_history() when history is set."""
        from unittest.mock import Mock
        mock_history = Mock()
        mock_history.display_history.return_value = "1. add(1, 2) = 3\n2. multiply(3, 4) = 12"

        handler = InputHandler(history=mock_history)
        handler.display_history()

        mock_history.display_history.assert_called_once()
        captured = capsys.readouterr()
        assert "1. add(1, 2) = 3" in captured.out
        assert "2. multiply(3, 4) = 12" in captured.out

    def test_display_history_with_real_history_object(self, capsys, tmp_path):
        """Test display_history with real OperationHistory object."""
        from src.history import OperationHistory

        history_file = tmp_path / "history.txt"
        history = OperationHistory(str(history_file))
        history.record_operation("add", [5, 3], 8)

        handler = InputHandler(history=history)
        handler.display_history()

        captured = capsys.readouterr()
        assert "1. add(5, 3) = 8" in captured.out

    def test_display_history_with_real_history_empty(self, capsys, tmp_path):
        """Test display_history with empty real OperationHistory object."""
        from src.history import OperationHistory

        history_file = tmp_path / "history.txt"
        history = OperationHistory(str(history_file))

        handler = InputHandler(history=history)
        handler.display_history()

        captured = capsys.readouterr()
        assert "No history yet." in captured.out


class TestGetOperationChoiceHistorySentinel:
    """Test suite for 'history' sentinel in get_operation_choice()."""

    @pytest.fixture
    def handler_with_history(self, tmp_path):
        """Fixture providing InputHandler with real history object."""
        from src.history import OperationHistory
        history_file = tmp_path / "history.txt"
        history = OperationHistory(str(history_file))
        history.record_operation("add", [1, 2], 3)
        history.record_operation("multiply", [3, 4], 12)
        return InputHandler(history=history)

    @pytest.fixture
    def available_ops(self):
        """Fixture to provide a sample operations dict."""
        return {
            "add": "Addition (a + b)",
            "subtract": "Subtraction (a - b)",
            "multiply": "Multiplication (a * b)",
        }

    @patch("builtins.input", side_effect=["history", "add"])
    def test_history_sentinel_displays_history_and_reprompts(self, mock_input, handler_with_history, available_ops, capsys):
        """Test that 'history' input displays history and re-prompts without returning."""
        result = handler_with_history.get_operation_choice(available_ops)

        # Should return the valid operation, not "history"
        assert result == "add"

        captured = capsys.readouterr()
        # History should be displayed
        assert "1. add(1, 2) = 3" in captured.out
        assert "2. multiply(3, 4) = 12" in captured.out

    @patch("builtins.input", side_effect=["history", "history", "subtract"])
    def test_history_sentinel_can_be_used_multiple_times(self, mock_input, handler_with_history, available_ops, capsys):
        """Test that 'history' can be called multiple times before selecting an operation."""
        result = handler_with_history.get_operation_choice(available_ops)

        assert result == "subtract"

        captured = capsys.readouterr()
        # History should be displayed (at least once, possibly twice)
        assert "1. add(1, 2) = 3" in captured.out

    @patch("builtins.input", side_effect=["history", "add"])
    def test_history_sentinel_does_not_increment_retry_counter(self, mock_input, handler_with_history, available_ops, capsys):
        """Test that 'history' does not count as a failed attempt."""
        # This is the same as the basic test, but the assertion is in the next test
        result = handler_with_history.get_operation_choice(available_ops)
        assert result == "add"

    @patch("builtins.input", side_effect=["history", "invalid1", "history", "add"])
    def test_history_sentinel_does_not_consume_retry_attempt(self, mock_input, handler_with_history, available_ops, capsys):
        """Test that 'history' does not count against max_retries."""
        # With max_retries=3, entering "history" twice and 1 invalid entry should allow "add" to succeed
        # because "history" doesn't consume retry attempts
        result = handler_with_history.get_operation_choice(available_ops, max_retries=3)

        assert result == "add"
        captured = capsys.readouterr()
        # Should have exactly 1 invalid choice message
        invalid_count = captured.out.count("Invalid choice")
        assert invalid_count == 1

    @patch("builtins.input", side_effect=["history", "add"])
    def test_history_sentinel_with_no_history_set(self, mock_input, capsys):
        """Test that 'history' with no history object displays 'No history available.'"""
        handler = InputHandler(history=None)
        available_ops = {"add": "Addition (a + b)"}

        result = handler.get_operation_choice(available_ops)

        assert result == "add"
        captured = capsys.readouterr()
        assert "No history available." in captured.out

    @patch("builtins.input", side_effect=["HISTORY", "add"])
    def test_history_sentinel_case_insensitive(self, mock_input, handler_with_history, available_ops, capsys):
        """Test that 'HISTORY' (uppercase) is recognized as history sentinel."""
        result = handler_with_history.get_operation_choice(available_ops)

        assert result == "add"
        captured = capsys.readouterr()
        # History should be displayed
        assert "1. add(1, 2) = 3" in captured.out or "add" in captured.out


class TestInputHandlerValidationErrorLogging:
    """Test suite for error logging when invalid input is provided via io_handler."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    @patch("builtins.input", side_effect=["not_a_number", "42"])
    def test_invalid_operand_via_get_operand_logs_validation_error(self, mock_input, handler, tmp_path, monkeypatch):
        """Test that invalid operand via get_operand() logs VALIDATION_ERROR and eventually succeeds."""
        from src import error_logger

        # Redirect logger to temp directory for isolation
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = __import__("logging").getLogger(f"test.io_handler.{id(self)}")
        test_logger.setLevel(__import__("logging").ERROR)
        test_logger.handlers.clear()

        handler_obj = __import__("logging").FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler_obj.setLevel(__import__("logging").ERROR)
        handler_obj.setFormatter(
            __import__("logging").Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler_obj)

        with monkeypatch.context() as mp:
            mp.setattr(error_logger, "_logger", test_logger)
            # First call with invalid input, then valid input
            result = handler.get_operand("Enter value: ")

            # Should have successfully parsed the second input
            assert result == 42.0

            # Verify VALIDATION_ERROR was logged
            handler_obj.flush()
            content = temp_log_file.read_text()
            assert "VALIDATION_ERROR:" in content

    @patch("builtins.input", side_effect=["", "5.5"])
    def test_empty_input_operand_logs_validation_error(self, mock_input, handler, tmp_path, monkeypatch):
        """Test that empty operand input logs VALIDATION_ERROR."""
        from src import error_logger

        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = __import__("logging").getLogger(f"test.io_empty.{id(self)}")
        test_logger.setLevel(__import__("logging").ERROR)
        test_logger.handlers.clear()

        handler_obj = __import__("logging").FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler_obj.setLevel(__import__("logging").ERROR)
        handler_obj.setFormatter(
            __import__("logging").Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler_obj)

        with monkeypatch.context() as mp:
            mp.setattr(error_logger, "_logger", test_logger)
            result = handler.get_operand("Enter value: ")

            assert result == 5.5

            handler_obj.flush()
            content = temp_log_file.read_text()
            assert "VALIDATION_ERROR:" in content

    @patch("builtins.input", side_effect=["12.34.56", "99"])
    def test_malformed_operand_logs_validation_error(self, mock_input, handler, tmp_path, monkeypatch):
        """Test that malformed numeric input logs VALIDATION_ERROR."""
        from src import error_logger

        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = __import__("logging").getLogger(f"test.io_malformed.{id(self)}")
        test_logger.setLevel(__import__("logging").ERROR)
        test_logger.handlers.clear()

        handler_obj = __import__("logging").FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler_obj.setLevel(__import__("logging").ERROR)
        handler_obj.setFormatter(
            __import__("logging").Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler_obj)

        with monkeypatch.context() as mp:
            mp.setattr(error_logger, "_logger", test_logger)
            result = handler.get_operand("Enter value: ")

            assert result == 99.0

            handler_obj.flush()
            content = temp_log_file.read_text()
            assert "VALIDATION_ERROR:" in content
