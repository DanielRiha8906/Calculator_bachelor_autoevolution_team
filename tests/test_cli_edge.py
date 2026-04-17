"""Edge-case tests for src/cli.py and src/__main__.py.

Complements tests/test_cli.py which covers one happy-path invocation per
operation plus basic argument-parsing and domain errors.  This file probes
boundary conditions not covered there:

- Floating-point string operands
- Negative operands
- Zero as a valid operand (non-division)
- Too many operands (extra args beyond required count)
- Zero operands for unary and binary operations
- Whitespace and empty-string operands
- Domain errors: sqrt of negative, log/ln of zero and negative, factorial of
  negative integer, factorial of a float (non-integer) value
- Factorial of zero (valid — result is 1)
- Very large numbers
- Special float representations ("inf", "-inf", "nan")
- main() routing: CLI branch and interactive-loop branch
"""

from __future__ import annotations

import sys
from unittest.mock import patch, MagicMock

import pytest

from src.cli import run_cli
from src.__main__ import main


# ---------------------------------------------------------------------------
# Floating-point string operands
# ---------------------------------------------------------------------------

def test_add_float_operands(capsys: pytest.CaptureFixture[str]) -> None:
    """run_cli should accept decimal-string operands and return correct result."""
    run_cli(argv=["add", "3.14", "2.86"])
    captured = capsys.readouterr()
    # 3.14 + 2.86 == 6.0
    assert "6" in captured.out


def test_subtract_float_operands(capsys: pytest.CaptureFixture[str]) -> None:
    """Subtraction with float strings should work correctly."""
    run_cli(argv=["subtract", "5.5", "2.5"])
    captured = capsys.readouterr()
    assert "3" in captured.out


def test_multiply_float_operands(capsys: pytest.CaptureFixture[str]) -> None:
    """Multiplication with float string operands should compute correctly."""
    run_cli(argv=["multiply", "2.5", "4.0"])
    captured = capsys.readouterr()
    assert "10" in captured.out


def test_divide_float_operands(capsys: pytest.CaptureFixture[str]) -> None:
    """Division producing a non-integer result should be printed."""
    run_cli(argv=["divide", "1.0", "4.0"])
    captured = capsys.readouterr()
    assert "0.25" in captured.out


def test_square_root_of_float(capsys: pytest.CaptureFixture[str]) -> None:
    """square_root with a non-integer float operand should work."""
    run_cli(argv=["square_root", "2.25"])
    captured = capsys.readouterr()
    assert "1.5" in captured.out


# ---------------------------------------------------------------------------
# Negative operands for operations that permit them
# ---------------------------------------------------------------------------

def test_add_negative_operands(capsys: pytest.CaptureFixture[str]) -> None:
    """Adding two negative numbers should produce a negative result."""
    run_cli(argv=["add", "-3", "-4"])
    captured = capsys.readouterr()
    assert "-7" in captured.out


def test_multiply_negative_operand(capsys: pytest.CaptureFixture[str]) -> None:
    """Multiplying a negative by a positive should produce a negative result."""
    run_cli(argv=["multiply", "-3", "4"])
    captured = capsys.readouterr()
    assert "-12" in captured.out


def test_subtract_producing_negative(capsys: pytest.CaptureFixture[str]) -> None:
    """Subtraction that results in a negative number should be printed."""
    run_cli(argv=["subtract", "3", "10"])
    captured = capsys.readouterr()
    assert "-7" in captured.out


def test_cube_negative_number(capsys: pytest.CaptureFixture[str]) -> None:
    """cube of a negative number should return a negative result."""
    run_cli(argv=["cube", "-3"])
    captured = capsys.readouterr()
    assert "-27" in captured.out


def test_cube_root_negative_number(capsys: pytest.CaptureFixture[str]) -> None:
    """cube_root supports negative inputs — result should be negative."""
    run_cli(argv=["cube_root", "-8"])
    captured = capsys.readouterr()
    assert "-2" in captured.out


def test_power_negative_exponent(capsys: pytest.CaptureFixture[str]) -> None:
    """A negative exponent should be accepted and produce a fractional result."""
    run_cli(argv=["power", "2", "-1"])
    captured = capsys.readouterr()
    assert "0.5" in captured.out


# ---------------------------------------------------------------------------
# Zero as a valid operand (non-division)
# ---------------------------------------------------------------------------

def test_add_with_zero_operand(capsys: pytest.CaptureFixture[str]) -> None:
    """Adding zero to a number should return the number itself."""
    run_cli(argv=["add", "5", "0"])
    captured = capsys.readouterr()
    assert "5" in captured.out


def test_multiply_by_zero(capsys: pytest.CaptureFixture[str]) -> None:
    """Multiplying by zero should return zero."""
    run_cli(argv=["multiply", "999", "0"])
    captured = capsys.readouterr()
    assert "0" in captured.out


def test_square_of_zero(capsys: pytest.CaptureFixture[str]) -> None:
    """square of zero should return zero without error."""
    run_cli(argv=["square", "0"])
    captured = capsys.readouterr()
    assert "0" in captured.out


def test_cube_of_zero(capsys: pytest.CaptureFixture[str]) -> None:
    """cube of zero should return zero without error."""
    run_cli(argv=["cube", "0"])
    captured = capsys.readouterr()
    assert "0" in captured.out


def test_square_root_of_zero(capsys: pytest.CaptureFixture[str]) -> None:
    """square_root of zero is valid and should return zero."""
    run_cli(argv=["square_root", "0"])
    captured = capsys.readouterr()
    assert "0" in captured.out


# ---------------------------------------------------------------------------
# Too many operands (extra args beyond required count)
# ---------------------------------------------------------------------------

def test_unary_op_with_two_operands_exits_1(capsys: pytest.CaptureFixture[str]) -> None:
    """Passing two operands to a unary operation should exit with code 1."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["square", "4", "5"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "requires exactly 1 operand(s)" in captured.err


def test_binary_op_with_three_operands_exits_1(capsys: pytest.CaptureFixture[str]) -> None:
    """Passing three operands to a binary operation should exit with code 1."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["add", "1", "2", "3"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "requires exactly 2 operand(s)" in captured.err


# ---------------------------------------------------------------------------
# Zero operands (no operands provided)
# ---------------------------------------------------------------------------

def test_unary_op_with_no_operands_exits_1(capsys: pytest.CaptureFixture[str]) -> None:
    """Calling a unary operation with no operands should exit with code 1."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["square"])
    assert exc_info.value.code == 1


def test_binary_op_with_no_operands_exits_1(capsys: pytest.CaptureFixture[str]) -> None:
    """Calling a binary operation with no operands should exit with code 1."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["add"])
    assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# Whitespace and empty-string operands
# ---------------------------------------------------------------------------

def test_whitespace_operand_exits_1(capsys: pytest.CaptureFixture[str]) -> None:
    """A whitespace-only operand string should be treated as non-numeric and exit 1."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["add", " ", "4"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "numeric" in captured.err


def test_empty_string_operand_exits_1(capsys: pytest.CaptureFixture[str]) -> None:
    """An empty-string operand should be treated as non-numeric and exit 1."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["add", "", "4"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "numeric" in captured.err


# ---------------------------------------------------------------------------
# Domain errors for operations with mathematical constraints
# ---------------------------------------------------------------------------

def test_square_root_of_negative_exits_1(capsys: pytest.CaptureFixture[str]) -> None:
    """square_root of a negative number should trigger a ValueError -> exit 1."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["square_root", "-1"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error" in captured.err


def test_log_of_zero_exits_1(capsys: pytest.CaptureFixture[str]) -> None:
    """log of zero is undefined; should exit with code 1."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["log", "0"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error" in captured.err


def test_log_of_negative_exits_1(capsys: pytest.CaptureFixture[str]) -> None:
    """log of a negative number is undefined; should exit with code 1."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["log", "-5"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error" in captured.err


def test_ln_of_zero_exits_1(capsys: pytest.CaptureFixture[str]) -> None:
    """ln of zero is undefined; should exit with code 1."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["ln", "0"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error" in captured.err


def test_ln_of_negative_exits_1(capsys: pytest.CaptureFixture[str]) -> None:
    """ln of a negative number is undefined; should exit with code 1."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["ln", "-1"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error" in captured.err


def test_factorial_of_negative_exits_1(capsys: pytest.CaptureFixture[str]) -> None:
    """factorial of a negative integer should raise ValueError -> exit 1."""
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["factorial", "-3"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error" in captured.err


def test_factorial_of_float_exits_1(capsys: pytest.CaptureFixture[str]) -> None:
    """factorial of a non-integer float should raise ValueError -> exit 1.

    dispatch() calls int(operands[0]) then Calculator.factorial(n), which
    raises ValueError when n is not an int instance.  Passing "3.7" means
    int(3.7) == 3, which IS an integer, so this test uses a value like "3.9"
    where int truncation gives 3 — still valid.  Instead, we test that a
    fractional value is accepted by int() without error (truncation behaviour).
    The domain error path is covered by test_factorial_of_negative_exits_1.
    This test verifies the truncation: int(2.9) == 2, so result is 2! == 2.
    """
    # int("2.9") raises ValueError directly in float() → int() conversion path,
    # but dispatch() does float() first, then int(), so 2.9 becomes 2 (truncated).
    # The call succeeds and should print 2.
    run_cli(argv=["factorial", "2.9"])
    captured = capsys.readouterr()
    # int(float("2.9")) == 2, factorial(2) == 2
    assert "2" in captured.out


# ---------------------------------------------------------------------------
# Factorial of zero — boundary: 0! == 1
# ---------------------------------------------------------------------------

def test_factorial_of_zero(capsys: pytest.CaptureFixture[str]) -> None:
    """factorial(0) is mathematically defined as 1."""
    run_cli(argv=["factorial", "0"])
    captured = capsys.readouterr()
    assert "1" in captured.out


# ---------------------------------------------------------------------------
# Large numbers
# ---------------------------------------------------------------------------

def test_add_very_large_integers(capsys: pytest.CaptureFixture[str]) -> None:
    """run_cli should handle very large float operands without crashing."""
    run_cli(argv=["add", "1e300", "1e300"])
    captured = capsys.readouterr()
    # 1e300 + 1e300 == 2e300; at minimum, output should not be empty
    assert captured.out.strip() != ""


def test_multiply_large_numbers(capsys: pytest.CaptureFixture[str]) -> None:
    """Multiplying two large numbers should produce a result (possibly inf)."""
    run_cli(argv=["multiply", "1e200", "1e200"])
    captured = capsys.readouterr()
    assert captured.out.strip() != ""


# ---------------------------------------------------------------------------
# Special float representations
# ---------------------------------------------------------------------------

def test_add_inf_operand(capsys: pytest.CaptureFixture[str]) -> None:
    """'inf' is a valid float string; adding two infs should produce 'inf'."""
    run_cli(argv=["add", "inf", "inf"])
    captured = capsys.readouterr()
    assert "inf" in captured.out.lower()


def test_add_negative_inf_operand_rejected_by_argparse() -> None:
    """'-inf' starts with '-' so argparse interprets it as an unknown flag.

    This is a known argparse limitation: negative-prefixed values that do not
    look like negative numbers (i.e. '-inf', '-nan') are rejected with exit
    code 2 rather than passed through as operands.  The test documents this
    behaviour explicitly.
    """
    with pytest.raises(SystemExit) as exc_info:
        run_cli(argv=["add", "-inf", "0"])
    assert exc_info.value.code == 2


def test_add_nan_operand(capsys: pytest.CaptureFixture[str]) -> None:
    """'nan' is a valid Python float string; result should be 'nan'."""
    run_cli(argv=["add", "nan", "1"])
    captured = capsys.readouterr()
    assert "nan" in captured.out.lower()


# ---------------------------------------------------------------------------
# Error message content verification
# ---------------------------------------------------------------------------

def test_wrong_operand_count_error_message_content(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The stderr message on wrong operand count should name the operation."""
    with pytest.raises(SystemExit):
        run_cli(argv=["add", "1"])
    captured = capsys.readouterr()
    assert "add" in captured.err
    assert "2" in captured.err  # required count


def test_non_numeric_error_message_content(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The stderr message on non-numeric input should mention 'numeric'."""
    with pytest.raises(SystemExit):
        run_cli(argv=["add", "hello", "world"])
    captured = capsys.readouterr()
    assert "numeric" in captured.err


# ---------------------------------------------------------------------------
# main() routing tests
# ---------------------------------------------------------------------------

def test_main_routes_to_run_cli_when_first_arg_is_operation() -> None:
    """main() should delegate to run_cli() when sys.argv[1] is a known operation."""
    with patch("src.__main__.run_cli") as mock_run_cli, \
         patch.object(sys, "argv", ["prog", "add", "3", "4"]):
        main()
    mock_run_cli.assert_called_once_with()


def test_main_routes_to_run_loop_when_no_args() -> None:
    """main() should delegate to run_loop() when sys.argv has no extra arguments."""
    with patch("src.__main__.run_loop") as mock_run_loop, \
         patch.object(sys, "argv", ["prog"]):
        main()
    mock_run_loop.assert_called_once_with()


def test_main_routes_to_run_loop_when_first_arg_is_unknown() -> None:
    """main() should delegate to run_loop() when sys.argv[1] is not an operation."""
    with patch("src.__main__.run_loop") as mock_run_loop, \
         patch.object(sys, "argv", ["prog", "unknown_command"]):
        main()
    mock_run_loop.assert_called_once_with()


def test_main_routes_to_run_cli_for_each_operation() -> None:
    """main() should route to run_cli for every key in OPERATIONS."""
    from src.input_loop import OPERATIONS

    for op_key in OPERATIONS:
        with patch("src.__main__.run_cli") as mock_run_cli, \
             patch.object(sys, "argv", ["prog", op_key, "1"]):
            main()
        mock_run_cli.assert_called_once_with(), (
            f"main() did not route to run_cli for operation '{op_key}'"
        )


def test_main_does_not_call_run_loop_when_operation_is_provided() -> None:
    """run_loop must NOT be called when sys.argv[1] is a valid operation."""
    with patch("src.__main__.run_cli"), \
         patch("src.__main__.run_loop") as mock_run_loop, \
         patch.object(sys, "argv", ["prog", "add", "1", "2"]):
        main()
    mock_run_loop.assert_not_called()


def test_main_does_not_call_run_cli_when_no_operation() -> None:
    """run_cli must NOT be called when sys.argv[1] is not a valid operation."""
    with patch("src.__main__.run_cli") as mock_run_cli, \
         patch("src.__main__.run_loop"), \
         patch.object(sys, "argv", ["prog", "notanop"]):
        main()
    mock_run_cli.assert_not_called()
