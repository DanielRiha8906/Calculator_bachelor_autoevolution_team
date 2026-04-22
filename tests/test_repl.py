"""Comprehensive tests for CalculatorREPL class."""

import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock
from pathlib import Path

from src.repl import CalculatorREPL, main, _format_result


class TestREPLCommandExecution:
    """Test suite for REPL command execution and output."""

    @pytest.fixture
    def tmp_history_file(self, tmp_path):
        """Fixture providing a temporary history file path."""
        return str(tmp_path / "history.txt")

    @pytest.fixture
    def repl(self, tmp_history_file):
        """Fixture providing a CalculatorREPL with temp history file."""
        return CalculatorREPL(history_file=tmp_history_file)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_execute_add_command(self, mock_print, mock_input, repl):
        """Test that 'add 2 3' command prints result 5."""
        repl._execute_command("add 2 3")
        # Check that print was called with result
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("5" in str(call) for call in print_calls)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_execute_subtract_command(self, mock_print, mock_input, repl):
        """Test that 'subtract 10 4' command executes and prints 6."""
        repl._execute_command("subtract 10 4")
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("6" in str(call) for call in print_calls)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_execute_multiply_command(self, mock_print, mock_input, repl):
        """Test that 'multiply 3 4' command prints 12."""
        repl._execute_command("multiply 3 4")
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("12" in str(call) for call in print_calls)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_execute_divide_command(self, mock_print, mock_input, repl):
        """Test that 'divide 10 2' command prints 5."""
        repl._execute_command("divide 10 2")
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("5" in str(call) for call in print_calls)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_execute_square_command(self, mock_print, mock_input, repl):
        """Test that 'square 4' command prints 16."""
        repl._execute_command("square 4")
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("16" in str(call) for call in print_calls)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_execute_factorial_command(self, mock_print, mock_input, repl):
        """Test that 'factorial 5' command prints 120."""
        repl._execute_command("factorial 5")
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("120" in str(call) for call in print_calls)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_execute_power_command(self, mock_print, mock_input, repl):
        """Test that 'power 2 10' command prints 1024."""
        repl._execute_command("power 2 10")
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("1024" in str(call) for call in print_calls)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_execute_sqrt_alias(self, mock_print, mock_input, repl):
        """Test that 'sqrt 9' (alias for square_root) prints 3."""
        repl._execute_command("sqrt 9")
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("3" in str(call) for call in print_calls)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_execute_cube_command(self, mock_print, mock_input, repl):
        """Test that 'cube 3' command prints 27."""
        repl._execute_command("cube 3")
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("27" in str(call) for call in print_calls)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_execute_unknown_operation(self, mock_print, mock_input, repl):
        """Test that unknown operation prints error message."""
        repl._execute_command("badop 1 2")
        print_calls = [str(call) for call in mock_print.call_args_list]
        # Should print "Unknown operation: badop"
        assert any("Unknown" in str(call) for call in print_calls)

    @patch("builtins.print")
    def test_execute_wrong_arg_count_add(self, mock_print, repl):
        """Test that wrong number of args for 'add' raises ValueError."""
        with pytest.raises(ValueError) as excinfo:
            repl._execute_command("add 5")
        assert "expects 2 argument" in str(excinfo.value)

    @patch("builtins.print")
    def test_execute_wrong_arg_count_square(self, mock_print, repl):
        """Test that wrong number of args for 'square' raises ValueError."""
        with pytest.raises(ValueError) as excinfo:
            repl._execute_command("square 4 5")
        assert "expects 1 argument" in str(excinfo.value)

    @patch("builtins.print")
    def test_execute_non_numeric_arg(self, mock_print, repl):
        """Test that non-numeric argument raises ValueError."""
        with pytest.raises(ValueError) as excinfo:
            repl._execute_command("add abc 5")
        assert "must be numeric" in str(excinfo.value)

    @patch("builtins.print")
    def test_execute_non_numeric_second_arg(self, mock_print, repl):
        """Test that non-numeric second argument raises ValueError."""
        with pytest.raises(ValueError) as excinfo:
            repl._execute_command("add 5 xyz")
        assert "must be numeric" in str(excinfo.value)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_execute_factorial_converts_float_to_int(self, mock_print, mock_input, repl):
        """Test that factorial converts float argument to int."""
        repl._execute_command("factorial 5.0")
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("120" in str(call) for call in print_calls)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_execute_divide_with_floats(self, mock_print, mock_input, repl):
        """Test division with float arguments."""
        repl._execute_command("divide 7.0 2.0")
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("3.5" in str(call) for call in print_calls)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_execute_command_case_insensitive(self, mock_print, mock_input, repl):
        """Test that commands are case-insensitive."""
        repl._execute_command("ADD 2 3")
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("5" in str(call) for call in print_calls)


class TestREPLHistoryDisplay:
    """Test suite for REPL history display functionality."""

    @pytest.fixture
    def tmp_history_file(self, tmp_path):
        """Fixture providing a temporary history file path."""
        return str(tmp_path / "history.txt")

    @pytest.fixture
    def repl(self, tmp_history_file):
        """Fixture providing a CalculatorREPL with temp history file."""
        return CalculatorREPL(history_file=tmp_history_file)

    @patch("builtins.print")
    def test_display_history_empty(self, mock_print, repl):
        """Test that empty history prints 'No history yet.'"""
        repl._display_history()
        mock_print.assert_called_with("No history yet.")

    @patch("builtins.print")
    def test_display_history_after_operation(self, mock_print, repl):
        """Test that history is displayed after an operation."""
        calc = repl._session.get_calculator()
        calc.add(2, 3)
        repl._display_history()
        # Verify print was called with the entry
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert any("add(2, 3) = 5" in str(call) for call in print_calls)

    @patch("builtins.print")
    def test_display_history_multiple_entries(self, mock_print, repl):
        """Test that multiple history entries are displayed."""
        calc = repl._session.get_calculator()
        calc.add(1, 1)
        calc.multiply(2, 2)
        repl._display_history()
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        assert any("add(1, 1) = 2" in str(call) for call in print_calls)
        assert any("multiply(2, 2) = 4" in str(call) for call in print_calls)


class TestREPLRun:
    """Test suite for REPL run loop using input mocking."""

    @pytest.fixture
    def tmp_history_file(self, tmp_path):
        """Fixture providing a temporary history file path."""
        return str(tmp_path / "history.txt")

    @pytest.fixture
    def repl(self, tmp_history_file):
        """Fixture providing a CalculatorREPL with temp history file."""
        return CalculatorREPL(history_file=tmp_history_file)

    @patch("builtins.input", side_effect=["add 2 3", "exit"])
    @patch("builtins.print")
    def test_run_exit_saves_and_exits(self, mock_print, mock_input, repl, tmp_history_file):
        """Test that 'exit' command saves history file and exits loop."""
        repl.run()
        # Verify history file was created
        assert Path(tmp_history_file).exists()
        # Verify "Goodbye!" was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Goodbye" in str(call) for call in print_calls)

    @patch("builtins.input", side_effect=["add 1 1", "history", "exit"])
    @patch("builtins.print")
    def test_run_history_command_calls_display(self, mock_print, mock_input, repl):
        """Test that 'history' command displays entries."""
        repl.run()
        # Verify history entry was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("add(1, 1) = 2" in str(call) for call in print_calls)

    @patch("builtins.input", side_effect=["help", "exit"])
    @patch("builtins.print")
    def test_run_help_command_displays_help(self, mock_print, mock_input, repl):
        """Test that 'help' command displays help message."""
        repl.run()
        print_calls = [str(call) for call in mock_print.call_args_list]
        # Should display available commands
        assert any("Available" in str(call) for call in print_calls)

    @patch("builtins.input", side_effect=["badcommand", "exit"])
    @patch("builtins.print")
    def test_run_unknown_command_does_not_crash(self, mock_print, mock_input, repl):
        """Test that bad input doesn't raise uncaught exception."""
        # Should not raise - only print error and continue
        repl.run()
        assert True  # If we get here, no uncaught exception

    @patch("builtins.input", side_effect=EOFError)
    @patch("builtins.print")
    def test_run_eof_exits_gracefully(self, mock_print, mock_input, repl, tmp_history_file):
        """Test that EOFError causes graceful exit and saves history."""
        repl.run()
        # Verify history file was created
        assert Path(tmp_history_file).exists()

    @patch("builtins.input", side_effect=["add 2 3", "quit"])
    @patch("builtins.print")
    def test_run_quit_command_exits(self, mock_print, mock_input, repl):
        """Test that 'quit' command exits like 'exit'."""
        repl.run()
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Goodbye" in str(call) for call in print_calls)

    @patch("builtins.input", side_effect=["add 2 3", "add 4 5", "history", "exit"])
    @patch("builtins.print")
    def test_run_accumulates_history(self, mock_print, mock_input, repl):
        """Test that multiple operations accumulate in history."""
        repl.run()
        print_calls = [str(call) for call in mock_print.call_args_list]
        # Both operations should appear in history
        assert any("add(2, 3) = 5" in str(call) for call in print_calls)
        assert any("add(4, 5) = 9" in str(call) for call in print_calls)

    @patch("builtins.input", side_effect=["", "add 1 1", "exit"])
    @patch("builtins.print")
    def test_run_empty_input_skipped(self, mock_print, mock_input, repl):
        """Test that empty input is skipped without error."""
        repl.run()
        entries = repl._session.get_history()
        assert len(entries) == 1
        assert entries[0] == "add(1, 1) = 2"

    @patch("builtins.input", side_effect=["add 1", "exit"])
    @patch("builtins.print")
    def test_run_catches_error_and_continues(self, mock_print, mock_input, repl):
        """Test that ValueError is caught and REPL continues."""
        repl.run()
        # Should print error message
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Error:" in str(call) for call in print_calls)


class TestREPLMain:
    """Test suite for module-level main function."""

    @patch("src.repl.CalculatorREPL.run")
    def test_main_runs_repl(self, mock_run):
        """Test that main() creates and runs a CalculatorREPL."""
        main()
        mock_run.assert_called_once()

    @patch("src.repl.CalculatorREPL")
    def test_main_creates_repl(self, mock_repl_class):
        """Test that main creates a CalculatorREPL instance."""
        mock_instance = MagicMock()
        mock_repl_class.return_value = mock_instance
        main()
        mock_repl_class.assert_called_once()
        mock_instance.run.assert_called_once()


class TestFormatResult:
    """Test suite for _format_result helper function."""

    def test_format_whole_number_float(self):
        """Test that 5.0 is formatted as '5'."""
        result = _format_result(5.0)
        assert result == "5"

    def test_format_fractional_float(self):
        """Test that 3.5 is formatted as '3.5'."""
        result = _format_result(3.5)
        assert result == "3.5"

    def test_format_integer(self):
        """Test that integer 5 is formatted as '5'."""
        result = _format_result(5)
        assert result == "5"

    def test_format_negative_whole_float(self):
        """Test that -5.0 is formatted as '-5'."""
        result = _format_result(-5.0)
        assert result == "-5"

    def test_format_very_small_float(self):
        """Test that very small floats are preserved."""
        result = _format_result(1e-10)
        assert "e-" in result or "0.0000000001" in result

    def test_format_very_large_float(self):
        """Test that very large floats are preserved."""
        result = _format_result(1e20)
        assert "e+" in result or "100000000000000000000" in result

    def test_format_zero(self):
        """Test that 0.0 is formatted as '0'."""
        result = _format_result(0.0)
        assert result == "0"

    def test_format_bool_not_treated_as_float(self):
        """Test that bool True is not formatted as float."""
        result = _format_result(True)
        assert result == "True"

    def test_format_bool_false_not_treated_as_float(self):
        """Test that bool False is not formatted as float."""
        result = _format_result(False)
        assert result == "False"

    def test_format_string(self):
        """Test that string values are converted to string."""
        result = _format_result("hello")
        assert result == "hello"


class TestREPLInitialization:
    """Test suite for CalculatorREPL initialization."""

    def test_repl_init_default_history_file(self):
        """Test that default history file is 'history.txt'."""
        repl = CalculatorREPL()
        assert repl._session._history_file == "history.txt"

    def test_repl_init_custom_history_file(self, tmp_path):
        """Test that custom history file is stored."""
        filepath = str(tmp_path / "custom.txt")
        repl = CalculatorREPL(history_file=filepath)
        assert repl._session._history_file == filepath

    def test_repl_has_session(self):
        """Test that REPL has a CalculatorSession."""
        repl = CalculatorREPL()
        assert repl._session is not None
