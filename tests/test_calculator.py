import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero():
    """Assert that dividing by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        Calculator().divide(1, 0)
    with pytest.raises(ZeroDivisionError):
        Calculator().divide(1.0, 0.0)


# ---------------------------------------------------------------------------
# Edge-case tests for Calculator.divide — zero-divisor scenarios
# ---------------------------------------------------------------------------

@pytest.fixture
def calc():
    return Calculator()


@pytest.mark.parametrize("numerator", [-1, -1000, -(10**18)])
def test_divide_negative_int_numerator_int_zero(calc, numerator):
    """Negative integer numerators with an integer zero divisor still raise."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(numerator, 0)


@pytest.mark.parametrize("numerator", [-1.0, -0.001, -1e308])
def test_divide_negative_float_numerator_float_zero(calc, numerator):
    """Negative float numerators with a float zero divisor still raise."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(numerator, 0.0)


def test_divide_zero_numerator_int_zero(calc):
    """0 / 0 with integer operands must raise ZeroDivisionError (not return NaN)."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(0, 0)


def test_divide_zero_numerator_float_zero(calc):
    """0.0 / 0.0 must raise ZeroDivisionError (Python does not return NaN here)."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(0.0, 0.0)


def test_divide_large_int_numerator_int_zero(calc):
    """Very large integer numerator does not change zero-divisor behavior."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(10**18, 0)


def test_divide_large_float_numerator_float_zero(calc):
    """Very large float numerator does not change zero-divisor behavior."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(1e308, 0.0)


def test_divide_inf_numerator_float_zero(calc):
    """float('inf') as numerator with float zero divisor raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(float("inf"), 0.0)


def test_divide_negative_float_zero_divisor(calc):
    """IEEE 754 negative zero (-0.0) as divisor is still treated as zero by Python."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(1.0, -0.0)


def test_divide_negative_float_zero_divisor_negative_numerator(calc):
    """-0.0 divisor with a negative numerator still raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(-1.0, -0.0)


# ---------------------------------------------------------------------------
# Happy-path tests for Calculator.divide (non-zero denominators)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5.0),
    (-10, 2, -5.0),
    (10, -2, -5.0),
    (-10, -2, 5.0),
    (1, 3, 1 / 3),
    (0, 5, 0.0),
    (1e10, 1e5, 1e5),
])
def test_divide_normal_cases(calc, a, b, expected):
    """Normal division cases return the correct quotient."""
    result = calc.divide(a, b)
    assert math.isclose(result, expected, rel_tol=1e-9), (
        f"divide({a}, {b}) returned {result!r}, expected {expected!r}"
    )


def test_divide_result_is_float_for_int_operands(calc):
    """Python's / operator always returns a float, even for integer operands."""
    result = calc.divide(10, 2)
    assert isinstance(result, float)


def test_divide_does_not_mutate_inputs(calc):
    """divide must be side-effect-free on its arguments."""
    a, b = 6, 3
    calc.divide(a, b)
    assert a == 6
    assert b == 3