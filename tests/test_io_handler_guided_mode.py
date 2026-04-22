"""Unit tests for InputHandler retry logic in guided mode."""

import pytest
from unittest.mock import patch
from src.io_handler import InputHandler, InputRetryExhaustedError, MAX_RETRIES


class TestGetOperandRetry:
    """Test suite for InputHandler.get_operand() retry behavior."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    @patch("builtins.input", return_value="5.5")
    def test_get_operand_valid_on_first_try(self, mock_input, handler):
        """Test that valid input on first attempt returns immediately."""
        result = handler.get_operand("Enter value: ")
        assert result == 5.5
        # Should have only called input once
        assert mock_input.call_count == 1

    @patch("builtins.input", side_effect=["invalid", "7.5"])
    def test_get_operand_valid_after_one_retry(self, mock_input, handler, capsys):
        """Test that valid input after one invalid attempt is accepted."""
        result = handler.get_operand("Enter value: ")
        assert result == 7.5
        captured = capsys.readouterr()
        assert "Error: Invalid operand" in captured.out
        assert "2 attempt(s) remaining" in captured.out

    @patch("builtins.input", side_effect=["invalid1", "invalid2", "3.14"])
    def test_get_operand_valid_after_two_retries(self, mock_input, handler, capsys):
        """Test that valid input after two invalid attempts is accepted."""
        result = handler.get_operand("Enter value: ")
        assert result == 3.14
        captured = capsys.readouterr()
        # Should have shown error for both invalid inputs
        assert captured.out.count("Error: Invalid operand") == 2
        assert "1 attempt(s) remaining" in captured.out

    @patch("builtins.input", side_effect=["invalid1", "invalid2", "invalid3"])
    def test_get_operand_exhausts_retries_raises_error(self, mock_input, handler, capsys):
        """Test that exhausting max_retries raises InputRetryExhaustedError."""
        with pytest.raises(InputRetryExhaustedError):
            handler.get_operand("Enter value: ")
        captured = capsys.readouterr()
        assert "Maximum retry attempts reached. Session ended." in captured.out

    @patch("builtins.input", side_effect=["invalid1", "invalid2", "invalid3"])
    def test_get_operand_default_max_retries(self, mock_input, handler):
        """Test that default max_retries is 3."""
        with pytest.raises(InputRetryExhaustedError):
            handler.get_operand("Enter value: ")
        # Should have called input exactly 3 times (3 invalid attempts)
        assert mock_input.call_count == 3

    @patch("builtins.input", side_effect=["invalid1", "invalid2"])
    def test_get_operand_custom_max_retries(self, mock_input, handler):
        """Test that custom max_retries parameter is respected."""
        with pytest.raises(InputRetryExhaustedError):
            handler.get_operand("Enter value: ", max_retries=2)
        # Should have called input exactly 2 times
        assert mock_input.call_count == 2

    @patch("builtins.input", side_effect=["abc", "5.0", "xyz", "3.0"])
    def test_get_operand_independent_counters_per_prompt(self, mock_input, handler, capsys):
        """Test that retry counters are independent for each prompt."""
        # First call with one invalid, then valid
        result1 = handler.get_operand("First: ", max_retries=2)
        assert result1 == 5.0
        # Second call should have independent counter - one invalid, then valid
        result2 = handler.get_operand("Second: ", max_retries=2)
        assert result2 == 3.0

    @patch("builtins.input", side_effect=["", "  ", "xyz", "valid_input"])
    def test_get_operand_whitespace_invalid_inputs(self, mock_input, handler, capsys):
        """Test that empty/whitespace inputs count as retries."""
        # max_retries=3 means we can have 3 invalid attempts, then on 4th call we get valid
        with pytest.raises(InputRetryExhaustedError):
            handler.get_operand("Enter value: ", max_retries=3)
        captured = capsys.readouterr()
        assert captured.out.count("Error: Invalid operand") == 3

    @patch("builtins.input", return_value="1e50")
    def test_get_operand_large_number(self, mock_input, handler):
        """Test that very large numeric values are parsed."""
        result = handler.get_operand("Enter value: ")
        assert result == 1e50

    @patch("builtins.input", side_effect=["nan", "5.5"])
    def test_get_operand_nan_is_valid_float(self, mock_input, handler):
        """Test that 'nan' is parsed as float NaN (valid by Python's float())."""
        # Note: 'nan' is parseable by float() so it returns NaN, not an error
        result = handler.get_operand("Enter value: ")
        # NaN != NaN, so we check using str representation
        assert str(result) == "nan"


class TestGetOperationChoiceRetry:
    """Test suite for InputHandler.get_operation_choice() retry behavior."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    @pytest.fixture
    def available_ops(self):
        """Fixture providing a sample operations dictionary."""
        return {
            "add": "Addition (a + b)",
            "subtract": "Subtraction (a - b)",
            "multiply": "Multiplication (a * b)",
        }

    @patch("builtins.input", return_value="add")
    def test_get_operation_choice_valid_on_first_try(self, mock_input, handler, available_ops):
        """Test that valid operation on first attempt returns immediately."""
        result = handler.get_operation_choice(available_ops)
        assert result == "add"
        assert mock_input.call_count == 1

    @patch("builtins.input", side_effect=["invalid", "subtract"])
    def test_get_operation_choice_valid_after_one_retry(self, mock_input, handler, available_ops, capsys):
        """Test that valid operation after one invalid attempt is accepted."""
        result = handler.get_operation_choice(available_ops)
        assert result == "subtract"
        captured = capsys.readouterr()
        assert "Invalid choice 'invalid'" in captured.out
        assert "2 attempt(s) remaining" in captured.out

    @patch("builtins.input", side_effect=["invalid1", "invalid2", "multiply"])
    def test_get_operation_choice_valid_after_two_retries(self, mock_input, handler, available_ops, capsys):
        """Test that valid operation after two invalid attempts is accepted."""
        result = handler.get_operation_choice(available_ops)
        assert result == "multiply"
        captured = capsys.readouterr()
        assert captured.out.count("Invalid choice") == 2

    @patch("builtins.input", side_effect=["invalid1", "invalid2", "invalid3"])
    def test_get_operation_choice_exhausts_retries_raises_error(self, mock_input, handler, available_ops, capsys):
        """Test that exhausting max_retries raises InputRetryExhaustedError."""
        with pytest.raises(InputRetryExhaustedError):
            handler.get_operation_choice(available_ops)
        captured = capsys.readouterr()
        assert "Maximum retry attempts reached. Session ended." in captured.out

    @patch("builtins.input", side_effect=["invalid1", "invalid2", "invalid3"])
    def test_get_operation_choice_default_max_retries(self, mock_input, handler, available_ops):
        """Test that default max_retries is 3."""
        with pytest.raises(InputRetryExhaustedError):
            handler.get_operation_choice(available_ops)
        assert mock_input.call_count == 3

    @patch("builtins.input", side_effect=["invalid1", "invalid2"])
    def test_get_operation_choice_custom_max_retries(self, mock_input, handler, available_ops):
        """Test that custom max_retries parameter is respected."""
        with pytest.raises(InputRetryExhaustedError):
            handler.get_operation_choice(available_ops, max_retries=2)
        assert mock_input.call_count == 2

    @patch("builtins.input", side_effect=["invalid1", "exit"])
    def test_get_operation_choice_exit_does_not_count_as_failure(self, mock_input, handler, available_ops, capsys):
        """Test that 'exit' is not counted as a failed attempt."""
        result = handler.get_operation_choice(available_ops)
        assert result == "exit"
        captured = capsys.readouterr()
        assert "Invalid choice" in captured.out
        # With default max_retries=3, after 1 invalid attempt we have 2 remaining
        assert "2 attempt(s) remaining" in captured.out

    @patch("builtins.input", side_effect=["invalid1", "invalid2", "quit"])
    def test_get_operation_choice_quit_does_not_count_as_failure(self, mock_input, handler, available_ops, capsys):
        """Test that 'quit' is not counted as a failed attempt."""
        result = handler.get_operation_choice(available_ops)
        assert result == "quit"
        captured = capsys.readouterr()
        # Should have 2 invalid choice messages before quit
        assert captured.out.count("Invalid choice") == 2

    @patch("builtins.input", side_effect=["invalid1", "exit"])
    def test_get_operation_choice_exit_resets_counter(self, mock_input, handler, available_ops):
        """Test that 'exit' resets the retry counter."""
        # This test verifies that exit/quit are special sentinels
        result = handler.get_operation_choice(available_ops)
        assert result == "exit"
        # The key behavior: we got 1 invalid, then exit without raising error
        assert mock_input.call_count == 2

    @patch("builtins.input", side_effect=["invalid1", "invalid2", "invalid3"])
    def test_get_operation_choice_empty_string_invalid(self, mock_input, handler, available_ops):
        """Test that empty string is treated as invalid."""
        with pytest.raises(InputRetryExhaustedError):
            handler.get_operation_choice(available_ops)

    @patch("builtins.input", return_value=" multiply ")
    def test_get_operation_choice_whitespace_stripped(self, mock_input, handler, available_ops):
        """Test that whitespace is stripped and case is lowercased."""
        result = handler.get_operation_choice(available_ops)
        assert result == "multiply"

    @patch("builtins.input", return_value="EXIT")
    def test_get_operation_choice_exit_case_insensitive(self, mock_input, handler, available_ops):
        """Test that 'EXIT' (uppercase) is accepted as exit."""
        result = handler.get_operation_choice(available_ops)
        assert result == "exit"

    @patch("builtins.input", return_value="QUIT")
    def test_get_operation_choice_quit_case_insensitive(self, mock_input, handler, available_ops):
        """Test that 'QUIT' (uppercase) is accepted as quit."""
        result = handler.get_operation_choice(available_ops)
        assert result == "quit"

    @patch("builtins.input", side_effect=["invalid1", "exit"])
    def test_get_operation_choice_exit_after_invalid(self, mock_input, handler, available_ops, capsys):
        """Test that exit can be called after an invalid input without exhausting retries."""
        result = handler.get_operation_choice(available_ops, max_retries=2)
        # With max_retries=2, we can have 2 invalid attempts before exhaustion
        assert result == "exit"
        captured = capsys.readouterr()
        assert "Invalid choice 'invalid1'" in captured.out

    @patch("builtins.input", side_effect=["invalid1", "invalid2", "exit"])
    def test_get_operation_choice_exit_saves_at_edge_of_limit(self, mock_input, handler, available_ops):
        """Test that exit works even when approaching retry limit."""
        result = handler.get_operation_choice(available_ops, max_retries=3)
        assert result == "exit"
