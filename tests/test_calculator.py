import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(10, 0)


def test_divide_happy_path():
    calc = Calculator()
    assert calc.divide(10, 5) == 2.0


# --- Addition tests ---

def test_add_two_positive_integers():
    calc = Calculator()
    assert calc.add(3, 4) == 7


def test_add_negative_numbers():
    calc = Calculator()
    assert calc.add(-3, -7) == -10


def test_add_zero_operand():
    calc = Calculator()
    assert calc.add(0, 5) == 5
    assert calc.add(5, 0) == 5


def test_add_floats():
    calc = Calculator()
    result = calc.add(0.1, 0.2)
    assert math.isclose(result, 0.3, rel_tol=1e-9, abs_tol=1e-9)


def test_add_invalid_type_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.add("a", 1)


# --- Subtraction tests ---

def test_subtract_positive_result():
    calc = Calculator()
    assert calc.subtract(10, 3) == 7


def test_subtract_negative_result():
    calc = Calculator()
    assert calc.subtract(3, 10) == -7


def test_subtract_zero_operand():
    calc = Calculator()
    assert calc.subtract(5, 0) == 5


def test_subtract_floats():
    calc = Calculator()
    result = calc.subtract(1.5, 0.5)
    assert math.isclose(result, 1.0, rel_tol=1e-9, abs_tol=1e-9)


def test_subtract_invalid_type_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.subtract("a", 1)


# --- Multiplication tests ---

def test_multiply_two_positive_integers():
    calc = Calculator()
    assert calc.multiply(3, 4) == 12


def test_multiply_by_zero():
    calc = Calculator()
    assert calc.multiply(99, 0) == 0
    assert calc.multiply(0, 99) == 0


def test_multiply_negative_numbers():
    calc = Calculator()
    assert calc.multiply(-3, 4) == -12
    assert calc.multiply(-3, -4) == 12


def test_multiply_large_values():
    calc = Calculator()
    assert calc.multiply(10**6, 10**6) == 10**12


def test_multiply_invalid_type_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.multiply("a", "b")  # str * str is not defined


# --- Division tests (additional) ---

def test_divide_negative_dividend():
    calc = Calculator()
    result = calc.divide(-10, 2)
    assert math.isclose(result, -5.0, rel_tol=1e-9, abs_tol=1e-9)


def test_divide_float_result():
    calc = Calculator()
    result = calc.divide(1, 3)
    assert math.isclose(result, 1/3, rel_tol=1e-9)


def test_divide_large_values():
    calc = Calculator()
    result = calc.divide(10**12, 10**6)
    assert math.isclose(result, 10**6, rel_tol=1e-9)


def test_divide_invalid_type_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.divide("a", 1)