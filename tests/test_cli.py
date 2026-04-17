"""Comprehensive pytest tests for the src/cli.py CLI entry point.

Tests are organised into seven groups matching the implementer's specification:
  1. Correct arithmetic results (exit 0, correct numeric stdout)
  2. Wrong argument count (exit 2, usage hint on stderr)
  3. Non-numeric operands (exit 1, non-empty stderr)
  4. Unsupported operator (exit 1)
  5. Division by zero (exit 1, non-empty stderr)
  6. Float operands (exit 0, correct result)
  7. Negative operands (exit 0, correct result)
"""

import subprocess
import sys

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_cli(*args: str) -> subprocess.CompletedProcess:
    """Invoke `python -m src.cli <args>` and return the completed process."""
    return subprocess.run(
        [sys.executable, "-m", "src.cli", *args],
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# Group 1 — correct arithmetic results
# ---------------------------------------------------------------------------

class TestCorrectResults:
    """Happy-path tests: valid expressions should exit 0 with the right value."""

    @pytest.mark.parametrize(
        "operand1, operator, operand2, expected",
        [
            ("1", "+", "2", 3.0),
            ("10", "-", "3", 7.0),
            ("4", "*", "5", 20.0),
            ("10", "/", "2", 5.0),
        ],
    )
    def test_arithmetic_returns_correct_value(
        self, operand1, operator, operand2, expected
    ):
        result = run_cli(operand1, operator, operand2)
        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}. stderr: {result.stderr!r}"
        )
        assert float(result.stdout.strip()) == pytest.approx(expected)

    def test_stdout_is_bare_number_no_prefix(self):
        """stdout must be a bare float, NOT prefixed with 'Result:' or similar."""
        result = run_cli("1", "+", "2")
        assert result.returncode == 0
        stdout = result.stdout.strip()
        # Must be parseable as a float and contain no alphabetic characters
        assert float(stdout) == pytest.approx(3.0)
        assert not any(c.isalpha() for c in stdout), (
            f"stdout should be a bare number, got: {stdout!r}"
        )

    def test_stderr_is_empty_on_success(self):
        """No noise on stderr for a valid invocation."""
        result = run_cli("4", "*", "5")
        assert result.returncode == 0
        assert result.stderr == ""


# ---------------------------------------------------------------------------
# Group 2 — wrong argument count
# ---------------------------------------------------------------------------

class TestWrongArgCount:
    """CLI must exit 2 and print a usage hint to stderr for bad arg counts."""

    def test_zero_args_exits_2(self):
        result = run_cli()
        assert result.returncode == 2

    def test_zero_args_stderr_contains_usage(self):
        result = run_cli()
        assert "usage" in result.stderr.lower() or "python" in result.stderr.lower(), (
            f"Expected usage hint in stderr, got: {result.stderr!r}"
        )

    def test_one_arg_exits_2(self):
        result = run_cli("5")
        assert result.returncode == 2

    def test_one_arg_stderr_non_empty(self):
        result = run_cli("5")
        assert result.stderr.strip() != ""

    def test_two_args_exits_2(self):
        result = run_cli("5", "+")
        assert result.returncode == 2

    def test_two_args_stderr_non_empty(self):
        result = run_cli("5", "+")
        assert result.stderr.strip() != ""

    def test_four_positional_args_exits_2(self):
        """One extra argument beyond the expected three should exit 2."""
        result = run_cli("1", "+", "2", "extra")
        assert result.returncode == 2

    def test_four_positional_args_stderr_non_empty(self):
        result = run_cli("1", "+", "2", "extra")
        assert result.stderr.strip() != ""

    def test_wrong_arg_count_stdout_is_empty(self):
        """Nothing should be written to stdout when arg count is wrong."""
        result = run_cli("1", "+")
        assert result.stdout == ""


# ---------------------------------------------------------------------------
# Group 3 — non-numeric operands
# ---------------------------------------------------------------------------

class TestNonNumericOperands:
    """Non-numeric operands must exit 1 with a non-empty stderr message."""

    def test_non_numeric_operand_a_exits_1(self):
        result = run_cli("abc", "+", "2")
        assert result.returncode == 1

    def test_non_numeric_operand_a_stderr_non_empty(self):
        result = run_cli("abc", "+", "2")
        assert result.stderr.strip() != ""

    def test_non_numeric_operand_b_exits_1(self):
        result = run_cli("2", "+", "abc")
        assert result.returncode == 1

    def test_non_numeric_operand_b_stderr_non_empty(self):
        result = run_cli("2", "+", "abc")
        assert result.stderr.strip() != ""

    def test_non_numeric_operands_stdout_is_empty(self):
        """On error, stdout should be empty."""
        result = run_cli("abc", "+", "2")
        assert result.stdout == ""

    def test_special_chars_as_operand_exits_1(self):
        result = run_cli("@!", "+", "2")
        assert result.returncode == 1

    def test_empty_string_operand_exits_1(self):
        """An empty string cannot be parsed as a float."""
        result = run_cli("", "+", "2")
        assert result.returncode == 1


# ---------------------------------------------------------------------------
# Group 4 — unsupported operator
# ---------------------------------------------------------------------------

class TestUnsupportedOperator:
    """Unsupported operator symbols must exit 1."""

    def test_modulo_exits_1(self):
        result = run_cli("5", "%", "2")
        assert result.returncode == 1

    def test_modulo_stderr_non_empty(self):
        result = run_cli("5", "%", "2")
        assert result.stderr.strip() != ""

    def test_exponent_exits_1(self):
        result = run_cli("2", "**", "3")
        assert result.returncode == 1

    def test_exponent_stderr_non_empty(self):
        result = run_cli("2", "**", "3")
        assert result.stderr.strip() != ""

    def test_unsupported_operator_stdout_is_empty(self):
        result = run_cli("5", "%", "2")
        assert result.stdout == ""

    @pytest.mark.parametrize("op", ["//", "^", "&", "|", ">>", "<<", "~"])
    def test_various_unsupported_operators_exit_1(self, op):
        result = run_cli("4", op, "2")
        assert result.returncode == 1


# ---------------------------------------------------------------------------
# Group 5 — division by zero
# ---------------------------------------------------------------------------

class TestDivisionByZero:
    """Division by zero must exit 1 with a non-empty stderr message."""

    def test_division_by_zero_exits_1(self):
        result = run_cli("5", "/", "0")
        assert result.returncode == 1

    def test_division_by_zero_stderr_non_empty(self):
        result = run_cli("5", "/", "0")
        assert result.stderr.strip() != ""

    def test_division_by_zero_stdout_is_empty(self):
        result = run_cli("5", "/", "0")
        assert result.stdout == ""

    def test_division_by_zero_float_denominator_exits_1(self):
        """0.0 as denominator should also trigger the error path."""
        result = run_cli("5", "/", "0.0")
        assert result.returncode == 1


# ---------------------------------------------------------------------------
# Group 6 — float operands
# ---------------------------------------------------------------------------

class TestFloatOperands:
    """Floating-point operands must be accepted and yield correct results."""

    def test_float_addition_exits_0(self):
        result = run_cli("1.5", "+", "2.5")
        assert result.returncode == 0

    def test_float_addition_correct_result(self):
        result = run_cli("1.5", "+", "2.5")
        assert float(result.stdout.strip()) == pytest.approx(4.0)

    def test_float_subtraction(self):
        result = run_cli("3.75", "-", "1.25")
        assert result.returncode == 0
        assert float(result.stdout.strip()) == pytest.approx(2.5)

    def test_float_multiplication(self):
        result = run_cli("2.5", "*", "4.0")
        assert result.returncode == 0
        assert float(result.stdout.strip()) == pytest.approx(10.0)

    def test_float_division(self):
        result = run_cli("7.5", "/", "2.5")
        assert result.returncode == 0
        assert float(result.stdout.strip()) == pytest.approx(3.0)

    def test_float_result_parseable_as_float(self):
        """Ensure output for float inputs is always parseable as a Python float."""
        result = run_cli("1.5", "+", "2.5")
        assert result.returncode == 0
        # Must not raise
        parsed = float(result.stdout.strip())
        assert isinstance(parsed, float)


# ---------------------------------------------------------------------------
# Group 7 — negative operands
# ---------------------------------------------------------------------------

class TestNegativeOperands:
    """Negative numbers as CLI arguments must be handled correctly."""

    def test_negative_operand_a_multiplication(self):
        """'-3 * 2' should yield -6.0; pass '--' to avoid flag misinterpretation."""
        result = run_cli("--", "-3", "*", "2")
        # If '--' causes arg count to be 4 from Python's perspective the CLI
        # receives exactly [script, '-3', '*', '2'] — correct.
        if result.returncode == 2:
            # Some environments pass '--' through to sys.argv; fall back without it.
            result = run_cli("-3", "*", "2")
        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}. stderr: {result.stderr!r}"
        )
        assert float(result.stdout.strip()) == pytest.approx(-6.0)

    def test_negative_operand_b(self):
        result = run_cli("10", "+", "-4")
        assert result.returncode == 0
        assert float(result.stdout.strip()) == pytest.approx(6.0)

    def test_both_operands_negative(self):
        result = run_cli("-2", "*", "-3")
        assert result.returncode == 0
        assert float(result.stdout.strip()) == pytest.approx(6.0)

    def test_negative_float_operand(self):
        result = run_cli("-1.5", "+", "0.5")
        assert result.returncode == 0
        assert float(result.stdout.strip()) == pytest.approx(-1.0)

    def test_subtract_giving_negative_result(self):
        result = run_cli("3", "-", "10")
        assert result.returncode == 0
        assert float(result.stdout.strip()) == pytest.approx(-7.0)
