import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(1, 0)


def test_divide_by_false():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(1, False)


@pytest.mark.parametrize("b", ["string", None])
def test_divide_by_non_numeric(b):
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.divide(1, b)


def test_divide_by_infinity():
    calc = Calculator()
    result = calc.divide(1.0, float('inf'))
    assert result == 0.0


def test_divide_by_nan():
    calc = Calculator()
    result = calc.divide(1.0, float('nan'))
    assert math.isnan(result)


@pytest.fixture
def calc():
    return Calculator()


# --- add ---

def test_add_two_positive_integers(calc):
    assert calc.add(2, 3) == 5


def test_add_positive_and_negative(calc):
    assert calc.add(10, -4) == 6


def test_add_two_negatives(calc):
    assert calc.add(-3, -7) == -10


def test_add_with_zero(calc):
    assert calc.add(0, 5) == 5
    assert calc.add(5, 0) == 5


def test_add_floats(calc):
    assert calc.add(1.5, 2.5) == 4.0


def test_add_float_and_integer(calc):
    assert calc.add(1, 0.5) == 1.5


@pytest.mark.parametrize("b", ["string", None])
def test_add_non_numeric_raises(calc, b):
    with pytest.raises(TypeError):
        calc.add(1, b)


# --- subtract ---

def test_subtract_positive_result(calc):
    assert calc.subtract(10, 3) == 7


def test_subtract_negative_result(calc):
    assert calc.subtract(3, 10) == -7


def test_subtract_same_values(calc):
    assert calc.subtract(5, 5) == 0


def test_subtract_with_zero(calc):
    assert calc.subtract(7, 0) == 7
    assert calc.subtract(0, 7) == -7


def test_subtract_floats(calc):
    assert calc.subtract(3.5, 1.5) == 2.0


@pytest.mark.parametrize("b", ["string", None])
def test_subtract_non_numeric_raises(calc, b):
    with pytest.raises(TypeError):
        calc.subtract(1, b)


# --- multiply ---

def test_multiply_two_positive_integers(calc):
    assert calc.multiply(3, 4) == 12


def test_multiply_by_zero(calc):
    assert calc.multiply(99, 0) == 0
    assert calc.multiply(0, 99) == 0


def test_multiply_by_one(calc):
    assert calc.multiply(7, 1) == 7


def test_multiply_two_negatives(calc):
    assert calc.multiply(-3, -4) == 12


def test_multiply_positive_and_negative(calc):
    assert calc.multiply(3, -4) == -12


def test_multiply_floats(calc):
    assert calc.multiply(2.5, 4.0) == 10.0


@pytest.mark.parametrize("b", ["string", None])
def test_multiply_non_numeric_raises(calc, b):
    # Use 1.5 as `a` because int * str is valid Python (string repetition),
    # whereas float * str always raises TypeError as intended.
    with pytest.raises(TypeError):
        calc.multiply(1.5, b)