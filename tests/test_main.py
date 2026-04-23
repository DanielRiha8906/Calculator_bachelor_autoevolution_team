"""test_main.py — integration tests for the main entry point.

Tests the main() function, verifying that it:
- Initializes correctly
- Processes user input through the REPL
- Handles exit commands gracefully
- Handles KeyboardInterrupt gracefully
"""

import pytest
from unittest.mock import patch, MagicMock
from src.main import main


class TestMainEntryPoint:
    """Integration tests for the main() entry point function."""

    def test_main_initializes_without_error(self):
        """Test that main() can be called and initializes correctly."""
        # This test patches input to immediately exit so main terminates
        with patch("builtins.input", side_effect=["exit"]):
            # Should not raise any exception
            main()

    def test_main_with_valid_operation_executes_correctly(self, capsys):
        """Test that main() processes a valid operation and prints the result."""
        with patch("builtins.input", side_effect=["add 5 3", "exit"]):
            main()

        captured = capsys.readouterr()
        assert "Result: 8" in captured.out

    def test_main_with_invalid_operation_prints_error_and_continues(self, capsys):
        """Test that main() handles invalid operations gracefully and continues."""
        with patch("builtins.input", side_effect=["unknown_op 5", "exit"]):
            main()

        captured = capsys.readouterr()
        assert "Validation error:" in captured.out or "Unknown operation" in captured.out
        assert "Goodbye!" in captured.out

    def test_main_exits_gracefully_on_exit_command(self, capsys):
        """Test that main() exits cleanly when 'exit' is entered."""
        with patch("builtins.input", side_effect=["exit"]):
            main()

        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    def test_main_exits_gracefully_on_quit_command(self, capsys):
        """Test that main() exits cleanly when 'quit' is entered."""
        with patch("builtins.input", side_effect=["quit"]):
            main()

        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    def test_main_handles_keyboard_interrupt_gracefully(self, capsys):
        """Test that main() handles KeyboardInterrupt and exits cleanly."""
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            # Should not raise, main() swallows the interrupt in CalculatorREPL.run()
            main()

        captured = capsys.readouterr()
        # The REPL prints "Interrupted. Goodbye!" on KeyboardInterrupt
        assert "Interrupted" in captured.out or "Goodbye" in captured.out

    def test_main_processes_multiple_operations_in_sequence(self, capsys):
        """Test that main() can process multiple operations before exiting."""
        inputs = [
            "add 5 3",
            "multiply 2 4",
            "square 3",
            "exit",
        ]
        with patch("builtins.input", side_effect=inputs):
            main()

        captured = capsys.readouterr()
        assert "Result: 8" in captured.out
        assert "Result: 8" in captured.out  # multiply 2 4 = 8
        assert "Result: 9" in captured.out  # square 3 = 9
        assert "Goodbye!" in captured.out

    def test_main_displays_welcome_message(self, capsys):
        """Test that main() displays the welcome message and operation list."""
        with patch("builtins.input", side_effect=["exit"]):
            main()

        captured = capsys.readouterr()
        assert "Calculator" in captured.out
        assert "mode basic" in captured.out or "mode advanced" in captured.out or "mode scientific" in captured.out

    def test_main_with_eof_error_exits_cleanly(self, capsys):
        """Test that main() handles EOFError (exhausted piped input) gracefully."""
        with patch("builtins.input", side_effect=EOFError):
            main()

        # Should not raise; EOFError is caught by CalculatorREPL.run()

    def test_main_with_all_operations(self, capsys):
        """Test that main() can execute all supported operations."""
        inputs = [
            "add 5 3",
            "subtract 10 4",
            "multiply 2 3",
            "divide 10 2",
            "power 2 3",
            "factorial 5",
            "square 4",
            "cube 2",
            "square_root 16",
            "cube_root 8",
            "natural_log 2.718",
            "log_base_10 100",
            "exit",
        ]
        with patch("builtins.input", side_effect=inputs):
            main()

        captured = capsys.readouterr()
        # Verify that results are printed for all operations
        assert captured.out.count("Result:") >= 12

    def test_main_with_error_operation_continues_to_accept_input(self, capsys):
        """Test that main() continues processing after an error."""
        inputs = [
            "invalid_op 5",      # Error
            "add 5 3",           # Valid operation after error
            "exit",
        ]
        with patch("builtins.input", side_effect=inputs):
            main()

        captured = capsys.readouterr()
        # Should see error message for invalid op
        assert "Validation error:" in captured.out or "Unknown operation" in captured.out
        # Should still see result of valid op after error
        assert "Result: 8" in captured.out
        assert "Goodbye!" in captured.out

    def test_main_with_empty_lines_between_operations(self, capsys):
        """Test that main() skips empty lines and continues processing."""
        inputs = [
            "",
            "add 5 3",
            "",
            "",
            "square 2",
            "",
            "exit",
        ]
        with patch("builtins.input", side_effect=inputs):
            main()

        captured = capsys.readouterr()
        assert "Result: 8" in captured.out
        assert "Result: 4" in captured.out
        assert "Goodbye!" in captured.out
