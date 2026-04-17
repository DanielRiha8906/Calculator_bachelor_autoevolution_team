"""Tests for the CLI dispatch layer (src/cli.py).

All tests call ``run_cli`` directly (no subprocess).  Exit codes are asserted
via ``pytest.raises(SystemExit)``; stdout/stderr content is captured with the
``capsys`` fixture.
"""

from __future__ import annotations

import pytest

from src.cli import run_cli
from src.input_handler import OPERATIONS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _run(args: list[str], capsys) -> tuple[str, str, int]:
    """Invoke run_cli and return (stdout, stderr, exit_code)."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(args)
    captured = capsys.readouterr()
    return captured.out, captured.err, exc_info.value.code


# ---------------------------------------------------------------------------
# Successful operations
# ---------------------------------------------------------------------------


class TestSuccessfulCalls:
    def test_add_two_operands(self, capsys):
        out, err, code = _run(["add", "5", "7"], capsys)
        assert code == 0
        assert "12" in out
        assert err == ""

    def test_subtract(self, capsys):
        out, err, code = _run(["subtract", "10", "3"], capsys)
        assert code == 0
        assert "7" in out
        assert err == ""

    def test_multiply(self, capsys):
        out, err, code = _run(["multiply", "4", "3"], capsys)
        assert code == 0
        assert "12" in out
        assert err == ""

    def test_divide(self, capsys):
        out, err, code = _run(["divide", "10", "2"], capsys)
        assert code == 0
        assert "5" in out
        assert err == ""

    def test_power(self, capsys):
        out, err, code = _run(["power", "2", "8"], capsys)
        assert code == 0
        assert "256" in out
        assert err == ""

    def test_factorial_one_operand(self, capsys):
        out, err, code = _run(["factorial", "5"], capsys)
        assert code == 0
        assert "120" in out
        assert err == ""

    def test_square(self, capsys):
        out, err, code = _run(["square", "4"], capsys)
        assert code == 0
        assert "16" in out
        assert err == ""

    def test_cube(self, capsys):
        out, err, code = _run(["cube", "3"], capsys)
        assert code == 0
        assert "27" in out
        assert err == ""

    def test_square_root(self, capsys):
        out, err, code = _run(["square_root", "9"], capsys)
        assert code == 0
        assert "3" in out
        assert err == ""

    def test_cube_root(self, capsys):
        out, err, code = _run(["cube_root", "27"], capsys)
        assert code == 0
        assert "3" in out
        assert err == ""

    def test_log10(self, capsys):
        out, err, code = _run(["log10", "100"], capsys)
        assert code == 0
        assert "2" in out
        assert err == ""

    def test_ln(self, capsys):
        import math

        out, err, code = _run(["ln", "1"], capsys)
        assert code == 0
        assert "0" in out
        assert err == ""


# ---------------------------------------------------------------------------
# Parametrized smoke test across all OPERATIONS
# ---------------------------------------------------------------------------


def _sample_args(op_name: str) -> list[str]:
    """Return minimal valid args for *op_name* so the call succeeds."""
    sample_binary = ["1", "1"]
    sample_unary_float = ["4"]
    sample_factorial = ["5"]

    op = OPERATIONS[op_name]
    if op["arity"] == 2:
        return [op_name] + sample_binary
    if op_name == "factorial":
        return [op_name] + sample_factorial
    return [op_name] + sample_unary_float


@pytest.mark.parametrize("op_name", list(OPERATIONS.keys()))
def test_smoke_all_operations(op_name, capsys):
    """Each operation in OPERATIONS must succeed for valid input."""
    args = _sample_args(op_name)
    out, err, code = _run(args, capsys)
    assert code == 0, f"Operation '{op_name}' exited with code {code}; stderr: {err}"
    assert out.strip() != "", f"Operation '{op_name}' produced no stdout"
    assert err == ""


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------


class TestErrorPaths:
    def test_no_args_exits_1(self, capsys):
        out, err, code = _run([], capsys)
        assert code == 1

    def test_unknown_operation_exits_1(self, capsys):
        out, err, code = _run(["foobar"], capsys)
        assert code == 1
        assert "foobar" in err
        assert out == ""

    def test_unknown_operation_stderr_message(self, capsys):
        out, err, code = _run(["unknown_op"], capsys)
        assert code == 1
        assert "unknown_op" in err

    def test_too_few_operands_binary_op(self, capsys):
        out, err, code = _run(["add", "5"], capsys)
        assert code == 1
        assert "add" in err
        assert out == ""

    def test_too_many_operands_unary_op(self, capsys):
        out, err, code = _run(["square", "4", "9"], capsys)
        assert code == 1
        assert "square" in err
        assert out == ""

    def test_too_many_operands_binary_op(self, capsys):
        out, err, code = _run(["add", "1", "2", "3"], capsys)
        assert code == 1
        assert "add" in err
        assert out == ""

    def test_non_numeric_operand_exits_1(self, capsys):
        out, err, code = _run(["add", "five", "7"], capsys)
        assert code == 1
        assert "five" in err
        assert out == ""

    def test_non_numeric_second_operand(self, capsys):
        out, err, code = _run(["add", "5", "seven"], capsys)
        assert code == 1
        assert "seven" in err
        assert out == ""

    def test_divide_by_zero_exits_1(self, capsys):
        out, err, code = _run(["divide", "10", "0"], capsys)
        assert code == 1
        assert "zero" in err.lower()
        assert out == ""

    def test_square_root_negative_exits_1(self, capsys):
        out, err, code = _run(["square_root", "-1"], capsys)
        assert code == 1
        assert out == ""
        assert err != ""

    def test_log10_zero_exits_1(self, capsys):
        out, err, code = _run(["log10", "0"], capsys)
        assert code == 1
        assert out == ""
        assert err != ""

    def test_ln_negative_exits_1(self, capsys):
        out, err, code = _run(["ln", "-5"], capsys)
        assert code == 1
        assert out == ""
        assert err != ""

    def test_factorial_negative_exits_1(self, capsys):
        out, err, code = _run(["factorial", "-1"], capsys)
        assert code == 1
        assert out == ""
        assert err != ""

    def test_factorial_float_string_exits_1(self, capsys):
        # "3.5" cannot be coerced to int by int(), so should error before dispatch
        out, err, code = _run(["factorial", "3.5"], capsys)
        assert code == 1
        assert "3.5" in err
        assert out == ""


# ---------------------------------------------------------------------------
# Edge cases — very large numbers
# ---------------------------------------------------------------------------


class TestLargeNumbers:
    def test_add_large_numbers(self, capsys):
        """Addition with very large float values must succeed and exit 0."""
        out, err, code = _run(["add", "1e308", "1e308"], capsys)
        assert code == 0
        assert out.strip() != ""
        assert err == ""

    def test_multiply_large_numbers(self, capsys):
        """Multiplying two large floats (inf result) must still exit 0."""
        out, err, code = _run(["multiply", "1e308", "1e308"], capsys)
        assert code == 0
        assert "inf" in out.lower()
        assert err == ""

    def test_factorial_large_valid(self, capsys):
        """factorial(100) must succeed and produce a very large integer."""
        out, err, code = _run(["factorial", "100"], capsys)
        assert code == 0
        # The result of 100! has 158 digits; verify output is non-trivial
        assert len(out.strip()) > 100
        assert err == ""

    def test_power_large_exponent(self, capsys):
        """2 ** 1000 must succeed."""
        out, err, code = _run(["power", "2", "1000"], capsys)
        assert code == 0
        assert out.strip() != ""
        assert err == ""

    def test_subtract_large_negative_result(self, capsys):
        """Subtracting larger from smaller produces a large negative result."""
        out, err, code = _run(["subtract", "-1e300", "1e300"], capsys)
        assert code == 0
        assert "-" in out
        assert err == ""


# ---------------------------------------------------------------------------
# Edge cases — negative numbers as operands
# ---------------------------------------------------------------------------


class TestNegativeOperands:
    def test_add_both_negative(self, capsys):
        out, err, code = _run(["add", "-3", "-4"], capsys)
        assert code == 0
        assert "-7" in out
        assert err == ""

    def test_subtract_negative_from_negative(self, capsys):
        out, err, code = _run(["subtract", "-10", "-3"], capsys)
        assert code == 0
        assert "-7" in out
        assert err == ""

    def test_multiply_negative_by_negative(self, capsys):
        out, err, code = _run(["multiply", "-4", "-3"], capsys)
        assert code == 0
        assert "12" in out
        assert err == ""

    def test_divide_negative_by_positive(self, capsys):
        out, err, code = _run(["divide", "-10", "2"], capsys)
        assert code == 0
        assert "-5" in out
        assert err == ""

    def test_divide_positive_by_negative(self, capsys):
        out, err, code = _run(["divide", "10", "-2"], capsys)
        assert code == 0
        assert "-5" in out
        assert err == ""

    def test_power_negative_base_even_exponent(self, capsys):
        """(-2)^4 == 16.0 — negative base with even exponent yields positive."""
        out, err, code = _run(["power", "-2", "4"], capsys)
        assert code == 0
        assert "16" in out
        assert err == ""

    def test_power_negative_base_odd_exponent(self, capsys):
        """(-2)^3 == -8.0 — negative base with odd exponent yields negative."""
        out, err, code = _run(["power", "-2", "3"], capsys)
        assert code == 0
        assert "-8" in out
        assert err == ""

    def test_power_negative_exponent(self, capsys):
        """2^-1 == 0.5 — negative exponent is valid."""
        out, err, code = _run(["power", "2", "-1"], capsys)
        assert code == 0
        assert "0.5" in out
        assert err == ""

    def test_square_negative(self, capsys):
        """(-5)^2 == 25 — squaring a negative yields positive."""
        out, err, code = _run(["square", "-5"], capsys)
        assert code == 0
        assert "25" in out
        assert err == ""

    def test_cube_negative(self, capsys):
        """(-3)^3 == -27 — cube of a negative is negative."""
        out, err, code = _run(["cube", "-3"], capsys)
        assert code == 0
        assert "-27" in out
        assert err == ""

    def test_cube_root_negative(self, capsys):
        """cube_root(-8) == -2.0 — cube root of negative is valid."""
        out, err, code = _run(["cube_root", "-8"], capsys)
        assert code == 0
        assert "-2" in out
        assert err == ""

    def test_log10_negative_exits_1(self, capsys):
        """log10 of a negative number must fail."""
        out, err, code = _run(["log10", "-10"], capsys)
        assert code == 1
        assert out == ""
        assert err != ""

    def test_ln_zero_exits_1(self, capsys):
        """ln(0) is undefined — must fail with exit 1."""
        out, err, code = _run(["ln", "0"], capsys)
        assert code == 1
        assert out == ""
        assert err != ""


# ---------------------------------------------------------------------------
# Edge cases — float operands
# ---------------------------------------------------------------------------


class TestFloatOperands:
    def test_add_floats(self, capsys):
        out, err, code = _run(["add", "1.5", "2.5"], capsys)
        assert code == 0
        assert "4" in out
        assert err == ""

    def test_multiply_floats(self, capsys):
        out, err, code = _run(["multiply", "2.5", "4.0"], capsys)
        assert code == 0
        assert "10" in out
        assert err == ""

    def test_divide_floats(self, capsys):
        out, err, code = _run(["divide", "7.5", "2.5"], capsys)
        assert code == 0
        assert "3" in out
        assert err == ""

    def test_power_float_base_float_exponent(self, capsys):
        """9.0 ** 0.5 == 3.0."""
        out, err, code = _run(["power", "9.0", "0.5"], capsys)
        assert code == 0
        assert "3" in out
        assert err == ""

    def test_square_float(self, capsys):
        out, err, code = _run(["square", "1.5"], capsys)
        assert code == 0
        assert "2.25" in out
        assert err == ""

    def test_cube_float(self, capsys):
        out, err, code = _run(["cube", "2.0"], capsys)
        assert code == 0
        assert "8" in out
        assert err == ""

    def test_square_root_float(self, capsys):
        out, err, code = _run(["square_root", "2.0"], capsys)
        assert code == 0
        assert out.strip() != ""
        assert err == ""

    def test_log10_float(self, capsys):
        """log10(1000.0) == 3.0."""
        out, err, code = _run(["log10", "1000.0"], capsys)
        assert code == 0
        assert "3" in out
        assert err == ""

    def test_ln_float(self, capsys):
        """ln(e) == 1.0."""
        import math
        out, err, code = _run(["ln", str(math.e)], capsys)
        assert code == 0
        assert "1" in out
        assert err == ""


# ---------------------------------------------------------------------------
# Edge cases — whitespace and empty-string operands
# ---------------------------------------------------------------------------


class TestOperandFormatEdgeCases:
    def test_empty_string_operand_exits_1(self, capsys):
        """An empty string cannot be coerced to float — must exit 1."""
        out, err, code = _run(["add", "", "3"], capsys)
        assert code == 1
        assert out == ""
        assert err != ""

    def test_whitespace_only_operand_exits_1(self, capsys):
        """A whitespace-only string cannot be coerced to float — must exit 1."""
        out, err, code = _run(["add", "   ", "3"], capsys)
        assert code == 1
        assert out == ""
        assert err != ""

    def test_whitespace_operand_for_factorial_exits_1(self, capsys):
        """Whitespace-only string cannot be coerced to int — must exit 1."""
        out, err, code = _run(["factorial", "   "], capsys)
        assert code == 1
        assert out == ""
        assert err != ""

    def test_whitespace_padded_numeric_float_succeeds(self, capsys):
        """Python's float() accepts '  5  ', so the CLI passes it through."""
        out, err, code = _run(["add", "  5  ", "3"], capsys)
        assert code == 0
        assert "8" in out
        assert err == ""

    def test_whitespace_padded_numeric_int_succeeds(self, capsys):
        """Python's int() accepts '  5  ', so factorial passes it through."""
        out, err, code = _run(["factorial", "  5  "], capsys)
        assert code == 0
        assert "120" in out
        assert err == ""

    def test_special_char_operand_exits_1(self, capsys):
        """A string with special characters is not numeric — must exit 1."""
        out, err, code = _run(["add", "3!", "2"], capsys)
        assert code == 1
        assert out == ""
        assert err != ""

    def test_hex_string_operand_exits_1(self, capsys):
        """Hex literal '0xff' is not a valid float — must exit 1."""
        out, err, code = _run(["add", "0xff", "1"], capsys)
        assert code == 1
        assert out == ""
        assert err != ""

    def test_scientific_notation_operand_succeeds(self, capsys):
        """Scientific notation like '1e5' is valid for float operations."""
        out, err, code = _run(["add", "1e5", "2"], capsys)
        assert code == 0
        assert out.strip() != ""
        assert err == ""


# ---------------------------------------------------------------------------
# Edge cases — error priority (only first error is reported)
# ---------------------------------------------------------------------------


class TestErrorPriority:
    def test_unknown_op_takes_priority_over_operand_errors(self, capsys):
        """When op is unknown, that error is reported before arity/operand checks."""
        out, err, code = _run(["unknown_op", "abc", "xyz"], capsys)
        assert code == 1
        assert "unknown_op" in err
        assert out == ""

    def test_unknown_op_with_correct_arity_args_still_fails(self, capsys):
        """Unknown op with any number of args still gives an unknown-op error."""
        out, err, code = _run(["modulo", "10", "3"], capsys)
        assert code == 1
        assert "modulo" in err
        assert out == ""

    def test_arity_error_takes_priority_over_coerce_error(self, capsys):
        """Wrong arity is caught before operand coercion is attempted."""
        # 'add' needs 2 operands; providing 3 means arity fails first
        out, err, code = _run(["add", "abc", "def", "ghi"], capsys)
        assert code == 1
        assert "add" in err
        assert out == ""

    def test_no_args_error_takes_priority_over_everything(self, capsys):
        """Empty args list yields the usage message — no other check runs."""
        out, err, code = _run([], capsys)
        assert code == 1
        assert "Usage" in err
        assert out == ""


# ---------------------------------------------------------------------------
# Edge cases — boundary values (zero, identity elements)
# ---------------------------------------------------------------------------


class TestBoundaryValues:
    def test_add_zero_identity(self, capsys):
        """Adding zero is an identity operation."""
        out, err, code = _run(["add", "42", "0"], capsys)
        assert code == 0
        assert "42" in out
        assert err == ""

    def test_multiply_by_zero(self, capsys):
        out, err, code = _run(["multiply", "999", "0"], capsys)
        assert code == 0
        assert "0" in out
        assert err == ""

    def test_subtract_zero_identity(self, capsys):
        out, err, code = _run(["subtract", "7", "0"], capsys)
        assert code == 0
        assert "7" in out
        assert err == ""

    def test_subtract_self_yields_zero(self, capsys):
        out, err, code = _run(["subtract", "5", "5"], capsys)
        assert code == 0
        assert "0" in out
        assert err == ""

    def test_factorial_zero(self, capsys):
        """0! == 1 by convention."""
        out, err, code = _run(["factorial", "0"], capsys)
        assert code == 0
        assert "1" in out
        assert err == ""

    def test_factorial_one(self, capsys):
        """1! == 1."""
        out, err, code = _run(["factorial", "1"], capsys)
        assert code == 0
        assert "1" in out
        assert err == ""

    def test_power_zero_exponent(self, capsys):
        """Any base to the power 0 is 1."""
        out, err, code = _run(["power", "999", "0"], capsys)
        assert code == 0
        assert "1" in out
        assert err == ""

    def test_square_root_zero(self, capsys):
        """sqrt(0) == 0."""
        out, err, code = _run(["square_root", "0"], capsys)
        assert code == 0
        assert "0" in out
        assert err == ""

    def test_cube_root_zero(self, capsys):
        """cbrt(0) == 0."""
        out, err, code = _run(["cube_root", "0"], capsys)
        assert code == 0
        assert "0" in out
        assert err == ""

    def test_log10_one_yields_zero(self, capsys):
        """log10(1) == 0."""
        out, err, code = _run(["log10", "1"], capsys)
        assert code == 0
        assert "0" in out
        assert err == ""

    def test_ln_one_yields_zero(self, capsys):
        """ln(1) == 0."""
        out, err, code = _run(["ln", "1"], capsys)
        assert code == 0
        assert "0" in out
        assert err == ""


# ---------------------------------------------------------------------------
# Edge cases — _die function directly
# ---------------------------------------------------------------------------


class TestDieFunction:
    def test_die_exits_with_code_1(self, capsys):
        from src.cli import _die
        with pytest.raises(SystemExit) as exc_info:
            _die("some error")
        assert exc_info.value.code == 1

    def test_die_writes_to_stderr(self, capsys):
        from src.cli import _die
        with pytest.raises(SystemExit):
            _die("fatal error message")
        captured = capsys.readouterr()
        assert "fatal error message" in captured.err
        assert captured.out == ""

    def test_die_empty_message(self, capsys):
        """_die with an empty string still exits 1 with a blank stderr line."""
        from src.cli import _die
        with pytest.raises(SystemExit) as exc_info:
            _die("")
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_die_multiline_message(self, capsys):
        """_die passes the full multi-line string to stderr unchanged."""
        from src.cli import _die
        msg = "line one\nline two\nline three"
        with pytest.raises(SystemExit) as exc_info:
            _die(msg)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "line one" in captured.err
        assert "line two" in captured.err


# ---------------------------------------------------------------------------
# Edge cases — no_args message content
# ---------------------------------------------------------------------------


class TestNoArgsMessage:
    def test_no_args_mentions_usage(self, capsys):
        out, err, code = _run([], capsys)
        assert code == 1
        assert "Usage" in err

    def test_no_args_lists_operations(self, capsys):
        out, err, code = _run([], capsys)
        assert code == 1
        # At minimum the operations should be mentioned in the message
        assert "add" in err

    def test_no_args_nothing_to_stdout(self, capsys):
        out, err, code = _run([], capsys)
        assert out == ""
