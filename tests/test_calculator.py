import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(10, 0)


def test_divide_by_float_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(10, 0.0)


def test_divide_negative_numerator_by_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(-5, 0)


def test_divide_zero_by_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(0, 0)


def test_divide_normal_case_returns_correct_result():
    calc = Calculator()
    result = calc.divide(10, 2)
    assert result == 5.0


def test_divide_zero_numerator_nonzero_denominator_returns_zero():
    calc = Calculator()
    result = calc.divide(0, 5)
    assert result == 0.0


def test_add_positive_integers():
    calc = Calculator()
    assert calc.add(3, 4) == 7


def test_add_negative_integers():
    calc = Calculator()
    assert calc.add(-3, -4) == -7


def test_add_float_operands():
    calc = Calculator()
    assert calc.add(1.5, 2.5) == 4.0


def test_add_zero_operand():
    calc = Calculator()
    assert calc.add(0, 5) == 5


def test_subtract_positive_result():
    calc = Calculator()
    assert calc.subtract(10, 3) == 7


def test_subtract_negative_result():
    calc = Calculator()
    assert calc.subtract(3, 10) == -7


def test_subtract_zero_result():
    calc = Calculator()
    assert calc.subtract(5, 5) == 0


def test_subtract_float_operands():
    calc = Calculator()
    assert calc.subtract(5.5, 2.5) == 3.0


def test_multiply_positive_integers():
    calc = Calculator()
    assert calc.multiply(3, 4) == 12


def test_multiply_negative_integers():
    calc = Calculator()
    assert calc.multiply(-3, 4) == -12


def test_multiply_zero_multiplier():
    calc = Calculator()
    assert calc.multiply(5, 0) == 0


def test_multiply_float_operands():
    calc = Calculator()
    assert calc.multiply(2.5, 4.0) == 10.0


# ---------------------------------------------------------------------------
# add – additional edge cases
# ---------------------------------------------------------------------------

def test_add_both_zero():
    calc = Calculator()
    assert calc.add(0, 0) == 0


def test_add_mixed_sign():
    calc = Calculator()
    assert calc.add(-5, 3) == -2


def test_add_large_integers():
    calc = Calculator()
    assert calc.add(10**18, 10**18) == 2 * 10**18


def test_add_float_precision_known_inexact():
    # 0.1 + 0.2 is a well-known IEEE-754 inexactness; use math.isclose
    calc = Calculator()
    result = calc.add(0.1, 0.2)
    assert math.isclose(result, 0.3, rel_tol=1e-9)


def test_add_float_and_int():
    calc = Calculator()
    assert calc.add(1, 0.5) == 1.5


def test_add_none_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.add(None, 1)


def test_add_string_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.add("a", 1)


def test_add_negative_and_positive_cancel():
    calc = Calculator()
    assert calc.add(7, -7) == 0


# ---------------------------------------------------------------------------
# subtract – additional edge cases
# ---------------------------------------------------------------------------

def test_subtract_both_zero():
    calc = Calculator()
    assert calc.subtract(0, 0) == 0


def test_subtract_negative_minus_negative():
    calc = Calculator()
    assert calc.subtract(-3, -8) == 5


def test_subtract_large_integers():
    calc = Calculator()
    assert calc.subtract(10**18, 1) == 10**18 - 1


def test_subtract_float_precision_known_inexact():
    calc = Calculator()
    result = calc.subtract(0.3, 0.1)
    assert math.isclose(result, 0.2, rel_tol=1e-9)


def test_subtract_none_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.subtract(None, 1)


def test_subtract_string_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.subtract("a", 1)


def test_subtract_zero_from_negative():
    calc = Calculator()
    assert calc.subtract(-5, 0) == -5


# ---------------------------------------------------------------------------
# multiply – additional edge cases
# ---------------------------------------------------------------------------

def test_multiply_both_negative_gives_positive():
    calc = Calculator()
    assert calc.multiply(-3, -4) == 12


def test_multiply_by_one_identity():
    calc = Calculator()
    assert calc.multiply(99, 1) == 99


def test_multiply_by_negative_one():
    calc = Calculator()
    assert calc.multiply(7, -1) == -7


def test_multiply_both_zero():
    calc = Calculator()
    assert calc.multiply(0, 0) == 0


def test_multiply_large_integers():
    calc = Calculator()
    assert calc.multiply(10**9, 10**9) == 10**18


def test_multiply_float_precision_known_inexact():
    calc = Calculator()
    result = calc.multiply(0.1, 3)
    assert math.isclose(result, 0.3, rel_tol=1e-9)


def test_multiply_none_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.multiply(None, 2)


def test_multiply_string_raises_type_error():
    # "a" * 2 is valid Python (string repetition), but "a" * "b" is not.
    # Use two string operands to guarantee a TypeError from the * operator.
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.multiply("a", "b")