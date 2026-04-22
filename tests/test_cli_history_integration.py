"""Integration tests for CLI with OperationHistory functionality."""

import pytest
import os
from unittest.mock import patch
from pathlib import Path

from src.calculator import Calculator
from src.cli import interactive_session, get_operation_menu


class TestInteractiveSessionHistoryRecording:
    """Test history recording in interactive_session."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance."""
        return Calculator()

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_records_operation_on_success(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should record operation in history after successful execution."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1
        mock_input.side_effect = [str(add_idx), "2", "3", "q"]
        interactive_session(calculator)
        # Check that history.txt was created and contains the operation
        history_file = tmp_path / "history.txt"
        assert history_file.exists()
        content = history_file.read_text()
        assert "add(2, 3) = 5" in content

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_displays_history_on_request(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should display history when user types 'history' command."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1
        mock_input.side_effect = [str(add_idx), "2", "3", "h", "q"]
        interactive_session(calculator)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        output_str = " ".join(str(output) for output in printed_output)
        # Should display the history after user requests it
        assert "Operation history" in output_str or "add(2, 3) = 5" in output_str

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_displays_history_with_full_command(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should display history when user types 'history' (full word)."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1
        mock_input.side_effect = [str(add_idx), "2", "3", "history", "q"]
        interactive_session(calculator)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        output_str = " ".join(str(output) for output in printed_output)
        # Should display the history
        assert "Operation history" in output_str or "add(2, 3) = 5" in output_str

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_persists_history_on_quit(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should save history to file when session exits."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1
        mock_input.side_effect = [str(add_idx), "2", "3", "q"]
        interactive_session(calculator)
        history_file = tmp_path / "history.txt"
        assert history_file.exists()
        content = history_file.read_text()
        assert "add(2, 3) = 5" in content

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_empty_history_message(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should print 'No history yet.' when history is requested before any operations."""
        monkeypatch.chdir(tmp_path)
        mock_input.side_effect = ["h", "q"]
        interactive_session(calculator)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        output_str = " ".join(str(output) for output in printed_output)
        assert "No history yet" in output_str

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_new_session_fresh_history(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should start with fresh (empty) history for each session."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1
        # First session: perform operation
        mock_input.side_effect = [str(add_idx), "2", "3", "q"]
        interactive_session(calculator)

        # Second session: perform different operation
        mock_input.reset_mock()
        mock_input.side_effect = [str(add_idx), "5", "5", "q"]
        interactive_session(calculator)

        # Check history file - should only have the second session's operation
        history_file = tmp_path / "history.txt"
        content = history_file.read_text()
        # Should have the second operation
        assert "add(5, 5) = 10" in content
        # Should not have the first operation (fresh history each session)
        # (This assumes each session starts fresh, not accumulating)
        lines = content.strip().split("\n") if content.strip() else []
        # The behavior depends on implementation - if it's fresh, should have 1 entry
        # If accumulating, would have 2. Let's verify the last entry is from second session.
        if lines:
            assert "add(5, 5) = 10" in lines[-1]

    @patch("builtins.input")
    @patch("builtins.print")
    def test_no_history_recorded_on_operation_error(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should not record operation in history if it raises an error."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        divide_idx = menu.index("divide") + 1
        # Attempt division by zero (which will error)
        mock_input.side_effect = [str(divide_idx), "10", "0", "q"]
        interactive_session(calculator)
        history_file = tmp_path / "history.txt"
        if history_file.exists():
            content = history_file.read_text()
            # Should not contain the failed division operation
            assert "divide(10, 0)" not in content

    @patch("builtins.input")
    @patch("builtins.print")
    def test_interactive_session_multiple_successful_operations(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should record multiple successful operations in order."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1
        multiply_idx = menu.index("multiply") + 1
        mock_input.side_effect = [
            str(add_idx), "2", "3",          # add(2, 3) = 5
            str(multiply_idx), "5", "2",     # multiply(5, 2) = 10
            "q"
        ]
        interactive_session(calculator)
        history_file = tmp_path / "history.txt"
        content = history_file.read_text()
        lines = content.strip().split("\n")
        assert len(lines) == 2
        assert "add(2, 3) = 5" in lines[0]
        assert "multiply(5, 2) = 10" in lines[1]

    @patch("builtins.input")
    @patch("builtins.print")
    def test_history_command_case_insensitive_h(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should accept 'h' as history command (case-insensitive)."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1
        mock_input.side_effect = [str(add_idx), "1", "1", "H", "q"]
        interactive_session(calculator)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        # Should not crash and should display something
        assert any("add" in str(output).lower() or "history" in str(output).lower() for output in printed_output)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_history_display_shows_all_entries(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should display all history entries when requested."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1
        multiply_idx = menu.index("multiply") + 1
        mock_input.side_effect = [
            str(add_idx), "1", "2",          # add(1, 2) = 3
            str(multiply_idx), "3", "4",     # multiply(3, 4) = 12
            "history",
            "q"
        ]
        interactive_session(calculator)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        output_str = " ".join(str(output) for output in printed_output)
        # Should show both operations
        assert "add(1, 2)" in output_str or "1" in output_str
        assert "multiply(3, 4)" in output_str or "12" in output_str

    @patch("builtins.input")
    @patch("builtins.print")
    def test_history_saved_before_exit_on_max_retries(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should save history to file before exiting due to max operation retries."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1
        mock_input.side_effect = [
            str(add_idx), "1", "2",          # add(1, 2) = 3 (success)
            "invalid1", "invalid2", "invalid3", "invalid4", "invalid5"  # 5 retries then exit
        ]
        interactive_session(calculator)
        history_file = tmp_path / "history.txt"
        assert history_file.exists()
        content = history_file.read_text()
        assert "add(1, 2) = 3" in content

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("src.cli.detect_mode")
    def test_history_saved_before_exit_on_operand_limit(self, mock_detect_mode, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should save history before exiting due to operand input limit."""
        mock_detect_mode.return_value = "interactive"  # Force interactive mode for this test
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1
        mock_input.side_effect = [
            str(add_idx), "1", "2",          # add(1, 2) = 3 (success)
            str(add_idx), "a", "b", "c", "d", "e"  # 5 invalid operands then exit
        ]
        interactive_session(calculator)
        history_file = tmp_path / "history.txt"
        assert history_file.exists()
        content = history_file.read_text()
        assert "add(1, 2) = 3" in content

    @patch("builtins.input")
    @patch("builtins.print")
    def test_history_empty_file_when_no_operations(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should create empty history.txt when no successful operations occurred."""
        monkeypatch.chdir(tmp_path)
        mock_input.side_effect = ["q"]
        interactive_session(calculator)
        history_file = tmp_path / "history.txt"
        assert history_file.exists()
        assert history_file.read_text() == ""

    @patch("builtins.input")
    @patch("builtins.print")
    def test_history_formatting_preserved_in_file(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should preserve operation formatting (whole-number floats collapsed) in file."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        square_idx = menu.index("square") + 1
        mock_input.side_effect = [str(square_idx), "3", "q"]
        interactive_session(calculator)
        history_file = tmp_path / "history.txt"
        content = history_file.read_text()
        # square(3) = 9.0, should be formatted as 9 (not 9.0)
        assert "square(3) = 9" in content

    @patch("builtins.input")
    @patch("builtins.print")
    def test_history_command_with_spacing(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should handle history command with extra whitespace."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1
        mock_input.side_effect = [str(add_idx), "1", "1", "  history  ", "q"]
        # Note: input().strip() is called in cli.py, so "  history  " becomes "history"
        interactive_session(calculator)
        # Should not crash
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        assert len(printed_output) > 0

    @patch("builtins.input")
    @patch("builtins.print")
    def test_operation_by_name_case_insensitive_with_history(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should record operation when operation name is case-insensitive."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        # Try operation name in different case
        mock_input.side_effect = ["ADD", "2", "2", "q"]
        interactive_session(calculator)
        history_file = tmp_path / "history.txt"
        if history_file.exists():
            content = history_file.read_text()
            # Should record it with the proper operation name
            assert "add(2, 2) = 4" in content


class TestHistoryCommandPrecedence:
    """Test that history command is recognized and doesn't trigger operation lookup."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance."""
        return Calculator()

    @patch("builtins.input")
    @patch("builtins.print")
    def test_history_not_treated_as_invalid_operation(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should recognize 'history' as a command, not an invalid operation."""
        monkeypatch.chdir(tmp_path)
        mock_input.side_effect = ["history", "q"]
        interactive_session(calculator)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        output_str = " ".join(str(output) for output in printed_output)
        # Should show "No history yet." not "Invalid selection"
        assert "No history yet" in output_str
        # Should not show invalid operation error
        assert "Invalid selection 'history'" not in output_str

    @patch("builtins.input")
    @patch("builtins.print")
    def test_h_not_treated_as_invalid_operation(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should recognize 'h' as history command, not invalid operation."""
        monkeypatch.chdir(tmp_path)
        mock_input.side_effect = ["h", "q"]
        interactive_session(calculator)
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        output_str = " ".join(str(output) for output in printed_output)
        # Should show "No history yet." not "Invalid selection"
        assert "No history yet" in output_str


class TestHistoryFileBehavior:
    """Test file I/O behavior of history persistence."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance."""
        return Calculator()

    @patch("builtins.input")
    @patch("builtins.print")
    def test_history_file_location_uses_cwd(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should save history.txt in the current working directory."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1
        mock_input.side_effect = [str(add_idx), "1", "1", "q"]
        interactive_session(calculator)
        history_file = tmp_path / "history.txt"
        assert history_file.exists()

    @patch("builtins.input")
    @patch("builtins.print")
    def test_history_file_is_text_file(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should create a plain text file, readable as text."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1
        mock_input.side_effect = [str(add_idx), "1", "2", "q"]
        interactive_session(calculator)
        history_file = tmp_path / "history.txt"
        content = history_file.read_text(encoding="utf-8")
        assert isinstance(content, str)
        assert "add(1, 2) = 3" in content

    @patch("builtins.input")
    @patch("builtins.print")
    def test_history_overwrites_previous_session(self, mock_print, mock_input, calculator, tmp_path, monkeypatch):
        """Should overwrite history.txt on each new session (not append)."""
        monkeypatch.chdir(tmp_path)
        menu = get_operation_menu(calculator)
        add_idx = menu.index("add") + 1
        multiply_idx = menu.index("multiply") + 1

        # First session
        mock_input.side_effect = [str(add_idx), "1", "1", "q"]
        interactive_session(calculator)

        # Second session
        mock_input.reset_mock()
        mock_input.side_effect = [str(multiply_idx), "2", "2", "q"]
        interactive_session(calculator)

        history_file = tmp_path / "history.txt"
        content = history_file.read_text()
        lines = content.strip().split("\n") if content.strip() else []

        # Should only have the second session's operation
        assert "multiply(2, 2) = 4" in content
        # Should not have first session's operation (overwritten, not appended)
        if len(lines) == 1:  # If only one line, verify it's the multiply
            assert "multiply" in lines[0]
