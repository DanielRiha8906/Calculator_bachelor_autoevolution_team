import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError) as exc_info:
        calc.divide(10, 0)
    assert str(exc_info.value) == "Cannot divide by zero"


def test_divide_by_zero_with_negative_numerator():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.divide(-5, 0)


def test_divide_non_numeric_divisor_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.divide(10, "a")


def test_divide_non_numeric_numerator_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.divide("a", 2)


def test_divide_normal_case():
    calc = Calculator()
    assert calc.divide(10, 2) == pytest.approx(5.0)


# --- Float zero as divisor ---

def test_divide_by_float_zero_raises_value_error():
    """0.0 == 0 is True, so float zero must also raise ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError) as exc_info:
        calc.divide(10, 0.0)
    assert str(exc_info.value) == "Cannot divide by zero"


def test_divide_by_negative_float_zero_raises_value_error():
    """-0.0 == 0 is True in Python, so it must also raise ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.divide(10, -0.0)


def test_divide_float_numerator_by_zero_raises_value_error():
    """Float numerator with integer zero divisor must raise ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.divide(3.14, 0)


def test_divide_float_numerator_by_float_zero_raises_value_error():
    """Float numerator with float zero divisor must raise ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.divide(3.14, 0.0)


# --- Boolean divisor edge cases ---

def test_divide_by_false_raises_value_error():
    """False == 0 in Python; dividing by False must raise ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.divide(10, False)


def test_divide_by_true_returns_numerator():
    """True == 1 in Python; dividing by True should return a / 1."""
    calc = Calculator()
    assert calc.divide(10, True) == pytest.approx(10.0)


# --- Negative operands ---

def test_divide_negative_by_positive():
    calc = Calculator()
    assert calc.divide(-10, 2) == pytest.approx(-5.0)


def test_divide_positive_by_negative():
    calc = Calculator()
    assert calc.divide(10, -2) == pytest.approx(-5.0)


def test_divide_negative_by_negative_returns_positive():
    calc = Calculator()
    assert calc.divide(-10, -2) == pytest.approx(5.0)


# --- Zero numerator ---

def test_divide_zero_numerator_returns_zero():
    """0 / non-zero should return 0, not raise."""
    calc = Calculator()
    assert calc.divide(0, 5) == pytest.approx(0.0)


def test_divide_zero_float_numerator_returns_zero():
    calc = Calculator()
    assert calc.divide(0.0, 5) == pytest.approx(0.0)


# --- Float operands (normal path) ---

def test_divide_floats_normal_case():
    calc = Calculator()
    result = calc.divide(7.5, 2.5)
    assert result == pytest.approx(3.0)


# --- Very large numbers ---

def test_divide_very_large_numbers():
    calc = Calculator()
    result = calc.divide(10 ** 18, 10 ** 9)
    assert result == pytest.approx(10 ** 9)


def test_divide_very_large_float_by_small_float():
    calc = Calculator()
    result = calc.divide(1e300, 1e150)
    assert result == pytest.approx(1e150)


# --- Small non-zero denominator ---

def test_divide_by_very_small_denominator():
    """A very small but non-zero denominator should not raise."""
    calc = Calculator()
    result = calc.divide(1.0, 1e-300)
    assert math.isfinite(result) or math.isinf(result)  # no exception expected


# --- Infinity inputs ---

def test_divide_infinity_numerator_by_finite():
    calc = Calculator()
    result = calc.divide(float('inf'), 2)
    assert math.isinf(result)


def test_divide_finite_by_infinity():
    calc = Calculator()
    result = calc.divide(10, float('inf'))
    assert result == pytest.approx(0.0)


def test_divide_infinity_by_infinity_returns_nan():
    calc = Calculator()
    result = calc.divide(float('inf'), float('inf'))
    assert math.isnan(result)


# --- NaN inputs ---

def test_divide_nan_numerator_returns_nan():
    calc = Calculator()
    result = calc.divide(float('nan'), 2)
    assert math.isnan(result)


def test_divide_nan_divisor_returns_nan():
    calc = Calculator()
    result = calc.divide(10, float('nan'))
    assert math.isnan(result)


# --- None inputs ---

def test_divide_none_numerator_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.divide(None, 2)


def test_divide_none_divisor_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.divide(10, None)


# --- Parametrized normal-path cases ---

@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 1.0),
    (9, 3, 3.0),
    (100, 4, 25.0),
    (-9, 3, -3.0),
    (9, -3, -3.0),
    (-9, -3, 3.0),
    (1, 2, 0.5),
    (0, 7, 0.0),
])
def test_divide_parametrized(a, b, expected):
    calc = Calculator()
    assert calc.divide(a, b) == pytest.approx(expected)


# --- Error message exactness ---

def test_divide_by_zero_error_message_exact():
    """Verify the exact error message text is preserved."""
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(0, 0)