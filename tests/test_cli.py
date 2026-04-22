"""test_cli.py — comprehensive tests for the CLI mode.

Tests cover:
- CLIHandler.run(): success and error paths
- main_cli(): argument parsing and exit codes
- src.main.main(): routing logic between REPL and CLI modes
- src.__init__ exports
"""

import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

from src.cli import CLIHandler, main_cli
from src import CLIHandler as CLIHandlerExport


# =============================================================================
# TestCLIHandlerRun
# =============================================================================


class TestCLIHandlerRun:
    """Unit tests for CLIHandler.run() method."""

    # -------------------------------------------------------------------------
    # Success paths: two-operand operations
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("expression,expected_result", [
        ("add 5 3", 8),
        ("add 0 0", 0),
        ("add -5 3", -2),
        ("add 1.5 2.5", 4.0),
        ("subtract 10 4", 6),
        ("subtract 5 5", 0),
        ("subtract -10 5", -15),
        ("multiply 2 3", 6),
        ("multiply 0 100", 0),
        ("multiply -2 3", -6),
        ("multiply 2.5 4", 10.0),
        ("divide 10 2", 5.0),
        ("divide 15 3", 5.0),
        ("divide 1 2", 0.5),
        ("divide -10 2", -5.0),
        ("power 2 3", 8),
        ("power 2 10", 1024),
        ("power 5 0", 1),
        ("power 2 -1", 0.5),
    ])
    def test_clilhandler_run_two_operand_operations_success(
        self, expression, expected_result, capsys
    ):
        """Test CLIHandler.run() with valid two-operand operations."""
        handler = CLIHandler(expression)
        exit_code = handler.run()

        # Verify exit code
        assert exit_code == 0

        # Verify result is printed to stdout
        captured = capsys.readouterr()
        assert captured.out.strip() == str(expected_result)
        # Verify nothing is printed to stderr
        assert captured.err == ""

    # -------------------------------------------------------------------------
    # Success paths: one-operand operations
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("expression,expected_result", [
        ("factorial 0", 1),
        ("factorial 1", 1),
        ("factorial 5", 120),
        ("factorial 10", 3628800),
        ("square 2", 4),
        ("square 5", 25),
        ("square -3", 9),
        ("square 0.5", 0.25),
        ("cube 2", 8),
        ("cube 3", 27),
        ("cube -2", -8),
        ("square_root 4", 2.0),
        ("square_root 16", 4.0),
        ("square_root 0.25", 0.5),
        ("cube_root 8", 2.0),
        ("cube_root 27", 3.0),
        ("cube_root -8", -2.0),
    ])
    def test_clilhandler_run_one_operand_operations_success(
        self, expression, expected_result, capsys
    ):
        """Test CLIHandler.run() with valid one-operand operations."""
        handler = CLIHandler(expression)
        exit_code = handler.run()

        assert exit_code == 0

        captured = capsys.readouterr()
        # For floating point results, check approximate equality
        result_str = captured.out.strip()
        result_value = float(result_str)
        assert abs(result_value - expected_result) < 1e-9
        assert captured.err == ""

    @pytest.mark.parametrize("expression", [
        "natural_log 1",
        "natural_log 2.718",
        "log_base_10 1",
        "log_base_10 10",
        "log_base_10 100",
    ])
    def test_clilhandler_run_logarithm_operations_success(
        self, expression, capsys
    ):
        """Test CLIHandler.run() with logarithm operations."""
        handler = CLIHandler(expression)
        exit_code = handler.run()

        assert exit_code == 0

        captured = capsys.readouterr()
        # Just verify a numeric result is printed (don't test exact value)
        result = float(captured.out.strip())
        assert isinstance(result, float)
        assert captured.err == ""

    # -------------------------------------------------------------------------
    # Error paths: parse errors
    # -------------------------------------------------------------------------

    def test_clilhandler_run_empty_expression_returns_1(self, capsys):
        """Test that empty expression string returns exit code 1."""
        handler = CLIHandler("")
        exit_code = handler.run()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert "Input error:" in captured.err
        assert captured.out == ""

    def test_clilhandler_run_whitespace_only_expression_returns_1(self, capsys):
        """Test that whitespace-only expression returns exit code 1."""
        handler = CLIHandler("   ")
        exit_code = handler.run()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert "Input error:" in captured.err
        assert captured.out == ""

    @pytest.mark.parametrize("expression", [
        "add five 3",
        "subtract hello world",
        "multiply 2 abc",
        "divide 10 xyz",
        "square not_a_number",
        "add 5 3 abc",
    ])
    def test_clilhandler_run_non_numeric_operand_returns_1(
        self, expression, capsys
    ):
        """Test that non-numeric operands return exit code 1."""
        handler = CLIHandler(expression)
        exit_code = handler.run()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert "Input error:" in captured.err
        assert captured.out == ""

    # -------------------------------------------------------------------------
    # Error paths: validation errors
    # -------------------------------------------------------------------------

    def test_clilhandler_run_unknown_operation_returns_1(self, capsys):
        """Test that unknown operation returns exit code 1."""
        handler = CLIHandler("modulo 9 4")
        exit_code = handler.run()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert "Validation error:" in captured.err or "Unknown operation" in captured.err
        assert captured.out == ""

    @pytest.mark.parametrize("expression", [
        "add 5",          # Too few operands for 2-op
        "add 5 3 2",      # Too many operands for 2-op
        "multiply 10",    # Too few operands
        "divide 20",      # Too few operands
        "factorial",      # No operands for 1-op
        ("factorial 5 3"),  # Too many operands for 1-op
        ("square 3 3"),   # Too many operands
        ("cube 2 2"),     # Too many operands
        ("subtract"),     # No operands
    ])
    def test_clilhandler_run_wrong_operand_count_returns_1(
        self, expression, capsys
    ):
        """Test that wrong operand count returns exit code 1."""
        handler = CLIHandler(expression)
        exit_code = handler.run()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert "Validation error:" in captured.err or "expects" in captured.err
        assert captured.out == ""

    # -------------------------------------------------------------------------
    # Error paths: math errors
    # -------------------------------------------------------------------------

    def test_clilhandler_run_division_by_zero_returns_1(self, capsys):
        """Test that division by zero returns exit code 1."""
        handler = CLIHandler("divide 1 0")
        exit_code = handler.run()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert "Math error:" in captured.err or "division by zero" in captured.err
        assert captured.out == ""

    def test_clilhandler_run_square_root_negative_returns_1(self, capsys):
        """Test that square_root of negative number returns exit code 1."""
        handler = CLIHandler("square_root -4")
        exit_code = handler.run()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert "Math error:" in captured.err
        assert captured.out == ""

    def test_clilhandler_run_natural_log_zero_returns_1(self, capsys):
        """Test that natural_log of zero returns exit code 1."""
        handler = CLIHandler("natural_log 0")
        exit_code = handler.run()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert "Math error:" in captured.err
        assert captured.out == ""

    def test_clilhandler_run_natural_log_negative_returns_1(self, capsys):
        """Test that natural_log of negative number returns exit code 1."""
        handler = CLIHandler("natural_log -1")
        exit_code = handler.run()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert "Math error:" in captured.err
        assert captured.out == ""

    def test_clilhandler_run_log_base_10_zero_returns_1(self, capsys):
        """Test that log_base_10 of zero returns exit code 1."""
        handler = CLIHandler("log_base_10 0")
        exit_code = handler.run()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert "Math error:" in captured.err
        assert captured.out == ""

    def test_clilhandler_run_log_base_10_negative_returns_1(self, capsys):
        """Test that log_base_10 of negative number returns exit code 1."""
        handler = CLIHandler("log_base_10 -5")
        exit_code = handler.run()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert "Math error:" in captured.err
        assert captured.out == ""

    def test_clilhandler_run_factorial_negative_returns_1(self, capsys):
        """Test that factorial of negative number returns exit code 1."""
        handler = CLIHandler("factorial -1")
        exit_code = handler.run()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert "Math error:" in captured.err or "Validation error:" in captured.err
        assert captured.out == ""

    def test_clilhandler_run_factorial_float_returns_1(self, capsys):
        """Test that factorial of float returns exit code 1."""
        handler = CLIHandler("factorial 5.5")
        exit_code = handler.run()

        assert exit_code == 1

        captured = capsys.readouterr()
        # Could be type error or validation error
        assert ("error:" in captured.err.lower())
        assert captured.out == ""

    # -------------------------------------------------------------------------
    # Case insensitivity
    # -------------------------------------------------------------------------

    @pytest.mark.parametrize("expression", [
        "ADD 5 3",
        "Add 5 3",
        "aDD 5 3",
        "SQUARE 4",
        "Square 4",
        "FACTORIAL 5",
    ])
    def test_clilhandler_run_case_insensitive_operations(
        self, expression, capsys
    ):
        """Test that operation names are case-insensitive."""
        handler = CLIHandler(expression)
        exit_code = handler.run()

        assert exit_code == 0
        captured = capsys.readouterr()
        assert captured.err == ""
        # Just verify output is numeric
        float(captured.out.strip())

    # -------------------------------------------------------------------------
    # Output formatting
    # -------------------------------------------------------------------------

    def test_clilhandler_run_outputs_only_numeric_result(self, capsys):
        """Test that only the numeric result is output to stdout."""
        handler = CLIHandler("add 5 3")
        exit_code = handler.run()

        captured = capsys.readouterr()
        # Output should be exactly "8\n" or "8" (just the number)
        output = captured.out.strip()
        assert output == "8"
        assert "Result:" not in output
        assert "Error:" not in output

    def test_clilhandler_run_integer_result_not_formatted_as_float(self, capsys):
        """Test that integer results are printed as integers, not floats."""
        handler = CLIHandler("add 2 3")
        exit_code = handler.run()

        captured = capsys.readouterr()
        output = captured.out.strip()
        # Python will print "5" for int, "5.0" for float
        assert output == "5"


# =============================================================================
# TestMainCliFunction
# =============================================================================


class TestMainCliFunction:
    """Tests for the main_cli() function."""

    def test_main_cli_with_valid_expression_exits_0(self, capsys):
        """Test that main_cli() exits with 0 for a valid expression."""
        with patch("sys.argv", ["calculator", "add 5 3"]):
            with pytest.raises(SystemExit) as exc_info:
                main_cli()

            assert exc_info.value.code == 0

            captured = capsys.readouterr()
            assert captured.out.strip() == "8"

    def test_main_cli_with_invalid_expression_exits_1(self, capsys):
        """Test that main_cli() exits with 1 for an invalid expression."""
        with patch("sys.argv", ["calculator", "add 5"]):
            with pytest.raises(SystemExit) as exc_info:
                main_cli()

            assert exc_info.value.code == 1

            captured = capsys.readouterr()
            assert "error:" in captured.err.lower()

    def test_main_cli_parses_expression_argument(self, capsys):
        """Test that main_cli() correctly parses the expression argument."""
        with patch("sys.argv", ["calculator", "multiply 6 7"]):
            with pytest.raises(SystemExit) as exc_info:
                main_cli()

            assert exc_info.value.code == 0

            captured = capsys.readouterr()
            assert captured.out.strip() == "42"

    def test_main_cli_with_empty_expression_exits_1(self, capsys):
        """Test that main_cli() exits with 1 for empty expression."""
        with patch("sys.argv", ["calculator", ""]):
            with pytest.raises(SystemExit) as exc_info:
                main_cli()

            assert exc_info.value.code == 1

            captured = capsys.readouterr()
            assert "error:" in captured.err.lower()


# =============================================================================
# TestMainRoutingLogic
# =============================================================================


class TestMainRoutingLogic:
    """Tests for src.main.main() CLI vs REPL routing."""

    def test_main_with_no_arguments_starts_repl(self):
        """Test that main() with no arguments delegates to CalculatorREPL."""
        from src.main import main

        with patch("sys.argv", ["src"]):
            with patch("src.main.CalculatorREPL") as mock_repl_class:
                mock_repl = MagicMock()
                mock_repl_class.return_value = mock_repl

                main()

                # Verify CalculatorREPL was instantiated and run() was called
                mock_repl_class.assert_called_once()
                mock_repl.run.assert_called_once()

    def test_main_with_expression_argument_uses_cli(self, capsys):
        """Test that main() with an argument delegates to CLIHandler."""
        from src.main import main

        with patch("sys.argv", ["src", "add 5 3"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

            captured = capsys.readouterr()
            assert captured.out.strip() == "8"

    def test_main_with_expression_does_not_start_repl(self):
        """Test that main() in CLI mode does not start the REPL."""
        from src.main import main

        with patch("sys.argv", ["src", "square 4"]):
            with patch("src.main.CalculatorREPL") as mock_repl_class:
                with pytest.raises(SystemExit):
                    main()

                # REPL should not be instantiated
                mock_repl_class.assert_not_called()

    def test_main_with_invalid_cli_expression_returns_1(self, capsys):
        """Test that main() returns 1 for invalid CLI expression."""
        from src.main import main

        with patch("sys.argv", ["src", "invalid_op 5"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1


# =============================================================================
# TestExports
# =============================================================================


class TestExports:
    """Tests for src.__init__ exports."""

    def test_clilhandler_importable_from_src(self):
        """Test that CLIHandler can be imported directly from src."""
        # Verify the import itself works
        assert CLIHandlerExport is not None
        assert CLIHandlerExport.__name__ == "CLIHandler"

    def test_clilhandler_is_correct_class(self):
        """Test that the exported CLIHandler is the correct class."""
        # Verify it's the same class we imported directly
        assert CLIHandlerExport is CLIHandler

    def test_clilhandler_has_run_method(self):
        """Test that exported CLIHandler has the run method."""
        assert hasattr(CLIHandlerExport, "run")
        assert callable(getattr(CLIHandlerExport, "run"))


# =============================================================================
# Integration tests
# =============================================================================


class TestCLIIntegration:
    """Integration tests for CLI functionality."""

    def test_cli_all_two_operand_operations(self, capsys):
        """Test that all two-operand operations work correctly."""
        operations = [
            ("add 1 1", 2),
            ("subtract 5 3", 2),
            ("multiply 3 4", 12),
            ("divide 10 5", 2.0),
            ("power 2 5", 32),
        ]

        for expression, expected in operations:
            handler = CLIHandler(expression)
            exit_code = handler.run()

            assert exit_code == 0

            captured = capsys.readouterr()
            result = float(captured.out.strip())
            assert abs(result - expected) < 1e-9

    def test_cli_all_one_operand_operations(self, capsys):
        """Test that all one-operand operations work correctly."""
        operations = [
            "factorial 3",
            "square 3",
            "cube 2",
            "square_root 9",
            "cube_root 27",
            "natural_log 1",
            "log_base_10 10",
        ]

        for expression in operations:
            handler = CLIHandler(expression)
            exit_code = handler.run()

            assert exit_code == 0

            captured = capsys.readouterr()
            result = float(captured.out.strip())
            assert isinstance(result, (int, float))

    def test_cli_numeric_output_can_be_piped(self, capsys):
        """Test that CLI output is suitable for piping to other commands."""
        handler = CLIHandler("add 100 200")
        exit_code = handler.run()

        captured = capsys.readouterr()
        output = captured.out.strip()

        # Verify output is exactly a number (no extra text)
        # and can be parsed back
        result = float(output)
        assert result == 300.0
        assert "\n" not in output  # Only one line

    def test_cli_error_messages_go_to_stderr(self, capsys):
        """Test that error messages go to stderr, not stdout."""
        handler = CLIHandler("invalid_operation 5 3")
        exit_code = handler.run()

        assert exit_code == 1

        captured = capsys.readouterr()
        assert captured.err != ""
        assert captured.out == ""
