"""Tests for src.__main__ — cli_main function and __main__ dispatch guard.

Covers:
- cli_main happy paths (all four operators)
- cli_main ValueError exit (invalid operand, unsupported operator)
- cli_main ZeroDivisionError exit (divide by zero)
- cli_main wrong arg count (argparse exits 2)
- cli_main called with None uses sys.argv[1:] fall-through path
- __main__ guard dispatch: sys.argv > 1 routes to cli_main, else to main()
"""

import subprocess
import sys

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_module(*args, stdin_text=""):
    """Invoke 'python -m src' with the given positional CLI args.

    Returns a CompletedProcess with stdout/stderr captured.
    """
    return subprocess.run(
        [sys.executable, "-m", "src"] + list(args),
        capture_output=True,
        text=True,
        input=stdin_text,
    )


# ---------------------------------------------------------------------------
# cli_main — direct invocation (all four operators, happy path)
# ---------------------------------------------------------------------------

class TestCliMainHappyPath:
    """cli_main called with valid args must print 'Result: ...' and return normally (no SystemExit)."""

    def test_addition_prints_result(self, capsys):
        from src.__main__ import cli_main

        cli_main(["3", "+", "4"])
        captured = capsys.readouterr()
        assert "Result: 7.0" in captured.out

    def test_subtraction_prints_result(self, capsys):
        from src.__main__ import cli_main

        cli_main(["10", "-", "3"])
        captured = capsys.readouterr()
        assert "Result: 7.0" in captured.out

    def test_multiplication_prints_result(self, capsys):
        from src.__main__ import cli_main

        cli_main(["6", "*", "7"])
        captured = capsys.readouterr()
        assert "Result: 42.0" in captured.out

    def test_division_prints_result(self, capsys):
        from src.__main__ import cli_main

        cli_main(["8", "/", "2"])
        captured = capsys.readouterr()
        assert "Result: 4.0" in captured.out

    def test_float_operands_accepted(self, capsys):
        from src.__main__ import cli_main

        cli_main(["1.5", "+", "2.5"])
        captured = capsys.readouterr()
        assert "Result: 4.0" in captured.out

    def test_negative_operands_accepted(self, capsys):
        from src.__main__ import cli_main

        cli_main(["-3", "+", "-4"])
        captured = capsys.readouterr()
        assert "Result: -7.0" in captured.out

    def test_zero_operands_addition(self, capsys):
        from src.__main__ import cli_main

        cli_main(["0", "+", "0"])
        captured = capsys.readouterr()
        assert "Result: 0.0" in captured.out

    def test_nothing_on_stderr_for_valid_input(self, capsys):
        from src.__main__ import cli_main

        cli_main(["5", "*", "5"])
        captured = capsys.readouterr()
        assert captured.err == ""


# ---------------------------------------------------------------------------
# cli_main — ValueError exit (exit code 1)
# ---------------------------------------------------------------------------

class TestCliMainValueError:
    """cli_main must print 'Error: ...' to stderr and exit 1 on ValueError."""

    def test_non_numeric_operand_a_exits_1(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit) as exc_info:
            cli_main(["abc", "+", "4"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert captured.out == ""

    def test_non_numeric_operand_b_exits_1(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit) as exc_info:
            cli_main(["3", "+", "xyz"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_unsupported_operator_exits_1(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit) as exc_info:
            cli_main(["3", "%", "4"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_power_operator_not_supported_exits_1(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit) as exc_info:
            cli_main(["2", "**", "3"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_word_operator_exits_1(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit) as exc_info:
            cli_main(["3", "add", "4"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_empty_string_operand_a_exits_1(self, capsys):
        from src.__main__ import cli_main

        # argparse treats "" as a valid positional string, so parse_input
        # will raise ValueError when trying to cast "" to float
        with pytest.raises(SystemExit) as exc_info:
            cli_main(["", "+", "4"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err


# ---------------------------------------------------------------------------
# cli_main — ZeroDivisionError exit (exit code 1)
# ---------------------------------------------------------------------------

class TestCliMainZeroDivision:
    """cli_main must print 'Error: ...' to stderr and exit 1 on ZeroDivisionError."""

    def test_divide_by_zero_exits_1(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit) as exc_info:
            cli_main(["5", "/", "0"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert captured.out == ""

    def test_zero_divided_by_zero_exits_1(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit) as exc_info:
            cli_main(["0", "/", "0"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_float_zero_denominator_exits_1(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit) as exc_info:
            cli_main(["7.5", "/", "0.0"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_negative_divided_by_zero_exits_1(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit) as exc_info:
            cli_main(["-3", "/", "0"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err


# ---------------------------------------------------------------------------
# cli_main — wrong argument count (argparse exits 2)
# ---------------------------------------------------------------------------

class TestCliMainWrongArgCount:
    """argparse must exit with code 2 when the wrong number of args is given."""

    def test_no_args_exits_2(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit) as exc_info:
            cli_main([])
        assert exc_info.value.code == 2

    def test_one_arg_exits_2(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit) as exc_info:
            cli_main(["3"])
        assert exc_info.value.code == 2

    def test_two_args_exits_2(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit) as exc_info:
            cli_main(["3", "+"])
        assert exc_info.value.code == 2

    def test_four_args_exits_2(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit) as exc_info:
            cli_main(["3", "+", "4", "extra"])
        assert exc_info.value.code == 2

    def test_five_args_exits_2(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit) as exc_info:
            cli_main(["3", "+", "4", "5", "6"])
        assert exc_info.value.code == 2


# ---------------------------------------------------------------------------
# cli_main — None args reads sys.argv[1:] (argparse fallback path)
# ---------------------------------------------------------------------------

class TestCliMainNoneArgsFallback:
    """When args=None, cli_main must read sys.argv[1:] via argparse."""

    def test_none_args_reads_sys_argv(self, monkeypatch, capsys):
        from src.__main__ import cli_main

        monkeypatch.setattr(sys, "argv", ["prog", "3", "+", "4"])
        cli_main(None)
        captured = capsys.readouterr()
        assert "Result: 7.0" in captured.out

    def test_none_args_with_bad_operand_exits_1(self, monkeypatch, capsys):
        from src.__main__ import cli_main

        monkeypatch.setattr(sys, "argv", ["prog", "bad", "+", "4"])
        with pytest.raises(SystemExit) as exc_info:
            cli_main(None)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    def test_none_args_with_too_few_args_exits_2(self, monkeypatch, capsys):
        from src.__main__ import cli_main

        monkeypatch.setattr(sys, "argv", ["prog"])
        with pytest.raises(SystemExit) as exc_info:
            cli_main(None)
        assert exc_info.value.code == 2


# ---------------------------------------------------------------------------
# __main__ guard — subprocess-level dispatch tests
# ---------------------------------------------------------------------------

class TestMainGuardDispatch:
    """The if __name__ == '__main__' block must route correctly based on sys.argv."""

    def test_cli_args_present_routes_to_cli_main(self):
        """With >1 argv, module should evaluate the expression via cli_main."""
        result = run_module("3", "+", "4")
        assert result.returncode == 0
        assert "Result: 7.0" in result.stdout

    def test_cli_args_subtraction(self):
        result = run_module("10", "-", "3")
        assert result.returncode == 0
        assert "Result: 7.0" in result.stdout

    def test_cli_args_multiplication(self):
        result = run_module("6", "*", "7")
        assert result.returncode == 0
        assert "Result: 42.0" in result.stdout

    def test_cli_args_division(self):
        result = run_module("8", "/", "2")
        assert result.returncode == 0
        assert "Result: 4.0" in result.stdout

    def test_cli_args_value_error_exits_1(self):
        """With invalid operator, subprocess must exit 1."""
        result = run_module("3", "%", "4")
        assert result.returncode == 1
        assert "Error:" in result.stderr

    def test_cli_args_zero_division_exits_1(self):
        result = run_module("5", "/", "0")
        assert result.returncode == 1
        assert "Error:" in result.stderr

    def test_cli_args_wrong_count_exits_2(self):
        """Too few args: argparse exits 2."""
        result = run_module("3", "+")
        assert result.returncode == 2

    def test_no_cli_args_routes_to_main_interactive(self):
        """With no extra argv, module falls into interactive main().

        We supply valid input on stdin so main() completes normally.
        """
        result = run_module(stdin_text="3\n4\n+\n")
        assert result.returncode == 0
        assert "Result: 7.0" in result.stdout

    def test_no_cli_args_interactive_error_exits_1(self):
        """With no extra argv, main() handles ValueError and exits 1."""
        result = run_module(stdin_text="abc\n4\n+\n")
        assert result.returncode == 1
        assert "Error:" in result.stderr


# ---------------------------------------------------------------------------
# cli_main — output format verification
# ---------------------------------------------------------------------------

class TestCliMainOutputFormat:
    """Verify the exact output format produced by cli_main."""

    def test_result_prefix_is_exact(self, capsys):
        from src.__main__ import cli_main

        cli_main(["3", "+", "4"])
        captured = capsys.readouterr()
        assert captured.out.startswith("Result: ")

    def test_error_prefix_is_exact_on_value_error(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit):
            cli_main(["bad", "+", "4"])
        captured = capsys.readouterr()
        assert captured.err.startswith("Error: ")

    def test_error_prefix_is_exact_on_zero_division(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit):
            cli_main(["5", "/", "0"])
        captured = capsys.readouterr()
        assert captured.err.startswith("Error: ")

    def test_stdout_empty_on_value_error(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit):
            cli_main(["bad", "+", "4"])
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_stdout_empty_on_zero_division(self, capsys):
        from src.__main__ import cli_main

        with pytest.raises(SystemExit):
            cli_main(["5", "/", "0"])
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_stderr_empty_on_success(self, capsys):
        from src.__main__ import cli_main

        cli_main(["3", "+", "4"])
        captured = capsys.readouterr()
        assert captured.err == ""
