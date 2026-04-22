"""Unit tests for mode-related functionality in InputHandler and UserInterface."""

import pytest
from unittest.mock import patch, MagicMock
from src.io_handler import InputHandler, UserInterface


class TestInputHandlerGetOperationChoiceModeSentinels:
    """Test suite for mode sentinel recognition in InputHandler.get_operation_choice()."""

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

    @patch("builtins.input", return_value="mode")
    def test_get_operation_choice_mode_returns_mode(self, mock_input, handler, available_ops):
        """Test that input 'mode' returns 'mode'."""
        result = handler.get_operation_choice(available_ops)
        assert result == "mode"

    @patch("builtins.input", return_value="switch")
    def test_get_operation_choice_switch_returns_mode(self, mock_input, handler, available_ops):
        """Test that input 'switch' returns 'mode'."""
        result = handler.get_operation_choice(available_ops)
        assert result == "mode"

    @patch("builtins.input", return_value="m")
    def test_get_operation_choice_m_returns_mode(self, mock_input, handler, available_ops):
        """Test that input 'm' returns 'mode'."""
        result = handler.get_operation_choice(available_ops)
        assert result == "mode"

    @patch("builtins.input", return_value="MODE")
    def test_get_operation_choice_mode_uppercase_returns_mode(self, mock_input, handler, available_ops):
        """Test that input 'MODE' (uppercase) returns 'mode'."""
        result = handler.get_operation_choice(available_ops)
        assert result == "mode"

    @patch("builtins.input", return_value="SWITCH")
    def test_get_operation_choice_switch_uppercase_returns_mode(self, mock_input, handler, available_ops):
        """Test that input 'SWITCH' (uppercase) returns 'mode'."""
        result = handler.get_operation_choice(available_ops)
        assert result == "mode"

    @patch("builtins.input", return_value="M")
    def test_get_operation_choice_m_uppercase_returns_mode(self, mock_input, handler, available_ops):
        """Test that input 'M' (uppercase) returns 'mode'."""
        result = handler.get_operation_choice(available_ops)
        assert result == "mode"

    @patch("builtins.input", return_value=" mode ")
    def test_get_operation_choice_mode_with_whitespace_returns_mode(self, mock_input, handler, available_ops):
        """Test that 'mode' with whitespace is stripped and returns 'mode'."""
        result = handler.get_operation_choice(available_ops)
        assert result == "mode"

    @patch("builtins.input", return_value=" m ")
    def test_get_operation_choice_m_with_whitespace_returns_mode(self, mock_input, handler, available_ops):
        """Test that 'm' with whitespace is stripped and returns 'mode'."""
        result = handler.get_operation_choice(available_ops)
        assert result == "mode"


class TestInputHandlerGetOperationChoiceCurrentModeParameter:
    """Test suite for current_mode parameter in InputHandler.get_operation_choice()."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    @pytest.fixture
    def available_ops(self):
        """Fixture to provide a sample operations dict."""
        return {"add": "Addition (a + b)"}

    @patch("builtins.input", return_value="add")
    def test_get_operation_choice_default_mode_is_normal(self, mock_input, handler, available_ops, capsys):
        """Test that default current_mode is 'Normal'."""
        handler.get_operation_choice(available_ops)
        captured = capsys.readouterr()
        assert "Current mode: Normal" in captured.out

    @patch("builtins.input", return_value="add")
    def test_get_operation_choice_displays_current_mode_normal(self, mock_input, handler, available_ops, capsys):
        """Test that 'Normal' mode is displayed in output."""
        handler.get_operation_choice(available_ops, current_mode="Normal")
        captured = capsys.readouterr()
        assert "Current mode: Normal" in captured.out

    @patch("builtins.input", return_value="add")
    def test_get_operation_choice_displays_current_mode_scientific(self, mock_input, handler, available_ops, capsys):
        """Test that 'Scientific' mode is displayed in output."""
        handler.get_operation_choice(available_ops, current_mode="Scientific")
        captured = capsys.readouterr()
        assert "Current mode: Scientific" in captured.out

    @patch("builtins.input", return_value="add")
    def test_get_operation_choice_displays_mode_toggle_help(self, mock_input, handler, available_ops, capsys):
        """Test that mode toggle help line is displayed."""
        handler.get_operation_choice(available_ops)
        captured = capsys.readouterr()
        assert "mode / switch / m: Toggle between Normal and Scientific mode" in captured.out

    @patch("builtins.input", return_value="add")
    def test_get_operation_choice_mode_toggle_help_appears_once(self, mock_input, handler, available_ops, capsys):
        """Test that mode toggle help line appears exactly once in output."""
        handler.get_operation_choice(available_ops)
        captured = capsys.readouterr()
        count = captured.out.count("mode / switch / m: Toggle between Normal and Scientific mode")
        assert count == 1


class TestInputHandlerGetOperationChoiceBackwardCompatibility:
    """Test that existing sentinel behavior is preserved."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    @pytest.fixture
    def available_ops(self):
        """Fixture to provide a sample operations dict."""
        return {"add": "Addition (a + b)"}

    @patch("builtins.input", return_value="exit")
    def test_get_operation_choice_exit_still_works(self, mock_input, handler, available_ops):
        """Test that 'exit' sentinel still returns 'exit'."""
        result = handler.get_operation_choice(available_ops)
        assert result == "exit"

    @patch("builtins.input", return_value="quit")
    def test_get_operation_choice_quit_still_works(self, mock_input, handler, available_ops):
        """Test that 'quit' sentinel still returns 'quit'."""
        result = handler.get_operation_choice(available_ops)
        assert result == "quit"

    @patch("builtins.input", side_effect=["history", "add"])
    def test_get_operation_choice_history_still_works(self, mock_input, handler, available_ops, capsys):
        """Test that 'history' sentinel still triggers history display and re-prompt."""
        result = handler.get_operation_choice(available_ops)
        assert result == "add"
        captured = capsys.readouterr()
        assert "No history available." in captured.out


class TestInputHandlerGetOperationChoiceModeDoesNotCountAsRetry:
    """Test that mode sentinels are returned immediately without re-prompting."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    @pytest.fixture
    def available_ops(self):
        """Fixture to provide a sample operations dict."""
        return {"add": "Addition (a + b)"}

    @patch("builtins.input", return_value="mode")
    def test_mode_sentinel_returns_immediately(self, mock_input, handler, available_ops):
        """Test that 'mode' sentinel returns immediately without re-prompt."""
        result = handler.get_operation_choice(available_ops, max_retries=3)
        assert result == "mode"
        # Should only call input once, not multiple times
        assert mock_input.call_count == 1

    @patch("builtins.input", return_value="m")
    def test_m_sentinel_returns_immediately(self, mock_input, handler, available_ops):
        """Test that 'm' sentinel returns immediately."""
        result = handler.get_operation_choice(available_ops, max_retries=3)
        assert result == "mode"
        assert mock_input.call_count == 1

    @patch("builtins.input", return_value="switch")
    def test_switch_sentinel_returns_immediately(self, mock_input, handler, available_ops):
        """Test that 'switch' sentinel returns immediately."""
        result = handler.get_operation_choice(available_ops, max_retries=3)
        assert result == "mode"
        assert mock_input.call_count == 1


class TestUserInterfaceDisplayOperationsCurrentMode:
    """Test suite for UserInterface.display_operations() with mode parameter."""

    @pytest.fixture
    def ui(self):
        """Fixture to provide a UserInterface instance."""
        return UserInterface()

    @pytest.fixture
    def available_ops(self):
        """Fixture to provide a sample operations dict."""
        return {
            "add": "Addition (a + b)",
            "subtract": "Subtraction (a - b)",
        }

    def test_display_operations_default_mode_is_normal(self, ui, available_ops, capsys):
        """Test that default current_mode is 'Normal'."""
        ui.display_operations(available_ops)
        captured = capsys.readouterr()
        assert "Current mode: Normal" in captured.out

    def test_display_operations_displays_normal_mode(self, ui, available_ops, capsys):
        """Test that 'Normal' mode is displayed."""
        ui.display_operations(available_ops, current_mode="Normal")
        captured = capsys.readouterr()
        assert "Current mode: Normal" in captured.out

    def test_display_operations_displays_scientific_mode(self, ui, available_ops, capsys):
        """Test that 'Scientific' mode is displayed."""
        ui.display_operations(available_ops, current_mode="Scientific")
        captured = capsys.readouterr()
        assert "Current mode: Scientific" in captured.out

    def test_display_operations_shows_mode_toggle_help_normal(self, ui, available_ops, capsys):
        """Test that mode toggle help line appears in Normal mode."""
        ui.display_operations(available_ops, current_mode="Normal")
        captured = capsys.readouterr()
        assert "mode / switch / m: Toggle between Normal and Scientific mode" in captured.out

    def test_display_operations_shows_mode_toggle_help_scientific(self, ui, available_ops, capsys):
        """Test that mode toggle help line appears in Scientific mode."""
        ui.display_operations(available_ops, current_mode="Scientific")
        captured = capsys.readouterr()
        assert "mode / switch / m: Toggle between Normal and Scientific mode" in captured.out

    def test_display_operations_shows_operations(self, ui, available_ops, capsys):
        """Test that operations are displayed."""
        ui.display_operations(available_ops)
        captured = capsys.readouterr()
        assert "add: Addition (a + b)" in captured.out
        assert "subtract: Subtraction (a - b)" in captured.out

    def test_display_operations_shows_exit_quit_help(self, ui, available_ops, capsys):
        """Test that exit/quit help line is displayed."""
        ui.display_operations(available_ops)
        captured = capsys.readouterr()
        assert "exit / quit: Exit the calculator" in captured.out


class TestInputHandlerModeIntegration:
    """Integration tests for mode functionality in InputHandler."""

    @pytest.fixture
    def handler(self):
        """Fixture to provide an InputHandler instance."""
        return InputHandler()

    @pytest.fixture
    def normal_mode_ops(self):
        """Operations available in Normal mode."""
        return {
            "add": "Addition (a + b)",
            "multiply": "Multiplication (a * b)",
        }

    @pytest.fixture
    def scientific_mode_ops(self):
        """Operations available in Scientific mode."""
        return {
            "add": "Addition (a + b)",
            "multiply": "Multiplication (a * b)",
            "sin": "Sine of x in degrees (sin x°)",
        }

    @patch("builtins.input", return_value="add")
    def test_handler_works_with_normal_mode_ops(self, mock_input, handler, normal_mode_ops, capsys):
        """Test that handler displays only normal mode operations."""
        handler.get_operation_choice(normal_mode_ops, current_mode="Normal")
        captured = capsys.readouterr()
        assert "add: Addition (a + b)" in captured.out
        assert "sin" not in captured.out

    @patch("builtins.input", return_value="add")
    def test_handler_works_with_scientific_mode_ops(self, mock_input, handler, scientific_mode_ops, capsys):
        """Test that handler displays all operations in scientific mode."""
        handler.get_operation_choice(scientific_mode_ops, current_mode="Scientific")
        captured = capsys.readouterr()
        assert "add: Addition (a + b)" in captured.out
        assert "sin: Sine of x in degrees (sin x°)" in captured.out

    @patch("builtins.input", return_value="mode")
    def test_handler_accepts_mode_in_normal_mode(self, mock_input, handler, normal_mode_ops):
        """Test that 'mode' is accepted when displaying normal mode operations."""
        result = handler.get_operation_choice(normal_mode_ops, current_mode="Normal")
        assert result == "mode"

    @patch("builtins.input", return_value="mode")
    def test_handler_accepts_mode_in_scientific_mode(self, mock_input, handler, scientific_mode_ops):
        """Test that 'mode' is accepted when displaying scientific mode operations."""
        result = handler.get_operation_choice(scientific_mode_ops, current_mode="Scientific")
        assert result == "mode"
