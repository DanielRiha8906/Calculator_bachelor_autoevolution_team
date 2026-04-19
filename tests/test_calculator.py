import pytest
import math
from src.calculator import Calculator


# ==================== Addition Tests ====================

def test_add_normal_case():
    """Test normal addition: 2 + 3 = 5."""
    calc = Calculator()
    result = calc.add(2, 3)
    assert result == 5


def test_add_negative_numbers():
    """Test addition with negative numbers: -5 + 3 = -2."""
    calc = Calculator()
    result = calc.add(-5, 3)
    assert result == -2


def test_add_float_arithmetic():
    """Test addition with floats: 2.5 + 1.5 = 4.0."""
    calc = Calculator()
    result = calc.add(2.5, 1.5)
    assert result == 4.0


def test_add_with_zero_operand():
    """Test addition with zero operand: 0 + 5 = 5."""
    calc = Calculator()
    result = calc.add(0, 5)
    assert result == 5


def test_add_both_zero():
    """Test addition of two zeros: 0 + 0 = 0."""
    calc = Calculator()
    result = calc.add(0, 0)
    assert result == 0


def test_add_negative_plus_negative():
    """Test addition of two negative numbers: -3 + -2 = -5."""
    calc = Calculator()
    result = calc.add(-3, -2)
    assert result == -5


# ==================== Subtraction Tests ====================

def test_subtract_normal_case():
    """Test normal subtraction: 10 - 3 = 7."""
    calc = Calculator()
    result = calc.subtract(10, 3)
    assert result == 7


def test_subtract_resulting_in_negative():
    """Test subtraction resulting in negative: 3 - 10 = -7."""
    calc = Calculator()
    result = calc.subtract(3, 10)
    assert result == -7


def test_subtract_float_arithmetic():
    """Test subtraction with floats: 5.5 - 2.5 = 3.0."""
    calc = Calculator()
    result = calc.subtract(5.5, 2.5)
    assert result == 3.0


def test_subtract_with_zero_minuend():
    """Test subtraction from zero: 0 - 5 = -5."""
    calc = Calculator()
    result = calc.subtract(0, 5)
    assert result == -5


def test_subtract_with_zero_subtrahend():
    """Test subtraction with zero subtrahend: 10 - 0 = 10."""
    calc = Calculator()
    result = calc.subtract(10, 0)
    assert result == 10


def test_subtract_negative_minus_negative():
    """Test subtraction of negative numbers: -3 - -5 = 2."""
    calc = Calculator()
    result = calc.subtract(-3, -5)
    assert result == 2


# ==================== Multiplication Tests ====================

def test_multiply_normal_case():
    """Test normal multiplication: 3 * 4 = 12."""
    calc = Calculator()
    result = calc.multiply(3, 4)
    assert result == 12


def test_multiply_negative_by_positive():
    """Test multiplication with negative: -3 * 4 = -12."""
    calc = Calculator()
    result = calc.multiply(-3, 4)
    assert result == -12


def test_multiply_negative_by_negative():
    """Test multiplication of two negatives: -3 * -4 = 12."""
    calc = Calculator()
    result = calc.multiply(-3, -4)
    assert result == 12


def test_multiply_by_zero():
    """Test multiplication by zero: 5 * 0 = 0."""
    calc = Calculator()
    result = calc.multiply(5, 0)
    assert result == 0


def test_multiply_zero_by_zero():
    """Test multiplication of two zeros: 0 * 0 = 0."""
    calc = Calculator()
    result = calc.multiply(0, 0)
    assert result == 0


def test_multiply_float_by_integer():
    """Test multiplication with float: 2.5 * 2 = 5.0."""
    calc = Calculator()
    result = calc.multiply(2.5, 2)
    assert result == 5.0


def test_multiply_float_by_float():
    """Test multiplication of two floats: 1.5 * 2.5 = 3.75."""
    calc = Calculator()
    result = calc.multiply(1.5, 2.5)
    assert result == 3.75


# ==================== Division Tests ====================

def test_divide_normal_division():
    """Test normal division: 10 / 2 = 5.0."""
    calc = Calculator()
    result = calc.divide(10, 2)
    assert result == 5.0


def test_divide_resulting_in_float():
    """Test division resulting in float: 5 / 2 = 2.5."""
    calc = Calculator()
    result = calc.divide(5, 2)
    assert result == 2.5


def test_divide_negative_dividend():
    """Test division with negative dividend: -10 / 2 = -5.0."""
    calc = Calculator()
    result = calc.divide(-10, 2)
    assert result == -5.0


def test_divide_by_one():
    """Test division by one: 7 / 1 = 7.0."""
    calc = Calculator()
    result = calc.divide(7, 1)
    assert result == 7.0


def test_divide_zero_numerator():
    """Test division with zero numerator: 0 / 5 = 0.0."""
    calc = Calculator()
    result = calc.divide(0, 5)
    assert result == 0.0


# ==================== Division by Zero Tests (Issue #139) ====================

def test_divide_integer_by_zero_raises_error():
    """Test that dividing an integer by zero raises ZeroDivisionError."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)


def test_divide_float_by_zero_raises_error():
    """Test that dividing a float by zero raises ZeroDivisionError."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(10.5, 0.0)


def test_divide_negative_by_zero_raises_error():
    """Test that dividing a negative number by zero raises ZeroDivisionError."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(-5, 0)


# ==================== Invalid Input Tests ====================

def test_add_with_string_argument():
    """Test that add raises TypeError when passed a string."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.add("5", 3)


def test_add_with_none_argument():
    """Test that add raises TypeError when passed None."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.add(None, 5)


def test_subtract_with_string_argument():
    """Test that subtract raises TypeError when passed a string."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.subtract("10", 3)


def test_subtract_with_none_argument():
    """Test that subtract raises TypeError when passed None."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.subtract(None, 5)


def test_multiply_string_by_string_raises_error():
    """Test that multiply raises TypeError when both arguments are strings."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.multiply("3", "4")


def test_multiply_with_none_argument():
    """Test that multiply raises TypeError when passed None."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.multiply(None, 5)


def test_divide_with_string_argument():
    """Test that divide raises TypeError when passed a string."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.divide("10", 2)


def test_divide_with_none_argument():
    """Test that divide raises TypeError when passed None."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.divide(None, 5)