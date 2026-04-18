"""Tests for src.input_handler — parse_input and run_calculation."""

import pytest

from src.input_handler import parse_input, run_calculation


# ---------------------------------------------------------------------------
# parse_input — valid inputs
# ---------------------------------------------------------------------------

def test_parse_input_addition_returns_correct_tuple():
    a, b, method = parse_input("3", "4", "+")
    assert a == 3.0
    assert b == 4.0
    assert method == "add"


def test_parse_input_subtraction_returns_correct_tuple():
    a, b, method = parse_input("10", "5", "-")
    assert a == 10.0
    assert b == 5.0
    assert method == "subtract"


def test_parse_input_multiplication_returns_correct_tuple():
    a, b, method = parse_input("6", "7", "*")
    assert a == 6.0
    assert b == 7.0
    assert method == "multiply"


def test_parse_input_division_returns_correct_tuple():
    a, b, method = parse_input("8", "2", "/")
    assert a == 8.0
    assert b == 2.0
    assert method == "divide"


def test_parse_input_float_strings_accepted():
    a, b, method = parse_input("1.5", "2.5", "+")
    assert a == pytest.approx(1.5)
    assert b == pytest.approx(2.5)
    assert method == "add"


def test_parse_input_whitespace_padded_operands_accepted():
    a, b, method = parse_input("  3  ", "  4  ", "+")
    assert a == 3.0
    assert b == 4.0
    assert method == "add"


def test_parse_input_negative_operands_accepted():
    a, b, method = parse_input("-3", "-4", "*")
    assert a == -3.0
    assert b == -4.0
    assert method == "multiply"


# ---------------------------------------------------------------------------
# parse_input — invalid operand_a
# ---------------------------------------------------------------------------

def test_parse_input_non_numeric_operand_a_raises_value_error():
    with pytest.raises(ValueError):
        parse_input("abc", "4", "+")


def test_parse_input_empty_string_operand_a_raises_value_error():
    with pytest.raises(ValueError):
        parse_input("", "4", "+")


def test_parse_input_whitespace_only_operand_a_raises_value_error():
    with pytest.raises(ValueError):
        parse_input("   ", "4", "+")


# ---------------------------------------------------------------------------
# parse_input — invalid operand_b
# ---------------------------------------------------------------------------

def test_parse_input_non_numeric_operand_b_raises_value_error():
    with pytest.raises(ValueError):
        parse_input("3", "xyz", "+")


def test_parse_input_empty_string_operand_b_raises_value_error():
    with pytest.raises(ValueError):
        parse_input("3", "", "+")


def test_parse_input_whitespace_only_operand_b_raises_value_error():
    with pytest.raises(ValueError):
        parse_input("3", "   ", "+")


# ---------------------------------------------------------------------------
# parse_input — unsupported operator
# ---------------------------------------------------------------------------

def test_parse_input_unsupported_operator_raises_value_error():
    with pytest.raises(ValueError):
        parse_input("3", "4", "%")


def test_parse_input_power_operator_not_supported_raises_value_error():
    with pytest.raises(ValueError):
        parse_input("2", "3", "**")


def test_parse_input_empty_operator_raises_value_error():
    with pytest.raises(ValueError):
        parse_input("3", "4", "")


def test_parse_input_word_operator_raises_value_error():
    with pytest.raises(ValueError):
        parse_input("3", "4", "add")


# ---------------------------------------------------------------------------
# run_calculation — correct dispatch for each operator
# ---------------------------------------------------------------------------

def test_run_calculation_add():
    result, _ = run_calculation(3.0, 4.0, "add")
    assert result == pytest.approx(7.0)


def test_run_calculation_subtract():
    result, _ = run_calculation(10.0, 5.0, "subtract")
    assert result == pytest.approx(5.0)


def test_run_calculation_multiply():
    result, _ = run_calculation(6.0, 7.0, "multiply")
    assert result == pytest.approx(42.0)


def test_run_calculation_divide():
    result, _ = run_calculation(8.0, 2.0, "divide")
    assert result == pytest.approx(4.0)


def test_run_calculation_divide_float_result():
    result, _ = run_calculation(1.0, 3.0, "divide")
    assert result == pytest.approx(1 / 3)


# ---------------------------------------------------------------------------
# run_calculation — error propagation
# ---------------------------------------------------------------------------

def test_run_calculation_division_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        run_calculation(5.0, 0.0, "divide")


def test_run_calculation_zero_divided_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        run_calculation(0.0, 0.0, "divide")
