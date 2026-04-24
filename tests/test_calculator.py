import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    """Fixture to provide a Calculator instance."""
    return Calculator()


# ============================================================================
# CATEGORY 1: ADDITION TESTS (9 new)
# ============================================================================

@pytest.mark.parametrize("a,b,expected", [
    (5, 3, 8),                          # test_add_positive_integers
    (-5, -3, -8),                       # test_add_negative_integers
    (5, -3, 2),                         # test_add_positive_and_negative
    (-5, 3, -2),                        # test_add_negative_and_positive
    (0, 5, 5),                          # test_add_zero_with_positive
    (0, -5, -5),                        # test_add_zero_with_negative
    (0, 0, 0),                          # test_add_both_zero
    (10**15, 10**15, 2 * 10**15),      # test_add_large_numbers
])
def test_add(calc, a, b, expected):
    """Test addition with various valid inputs."""
    assert calc.add(a, b) == expected


def test_add_floats_precise(calc):
    """Test addition of floats with precision handling."""
    assert calc.add(1.5, 2.5) == pytest.approx(4.0)


# ============================================================================
# CATEGORY 2: SUBTRACTION TESTS (9 new)
# ============================================================================

@pytest.mark.parametrize("a,b,expected", [
    (10, 3, 7),                         # test_subtract_positive_integers
    (3, 10, -7),                        # test_subtract_negative_result
    (-10, -3, -7),                      # test_subtract_negative_operands
    (10, -3, 13),                       # test_subtract_negative_from_positive
    (-10, 3, -13),                      # test_subtract_positive_from_negative
    (5, 0, 5),                          # test_subtract_zero_from_positive
    (0, 5, -5),                         # test_subtract_positive_from_zero
    (10**15, 10**14, 9 * 10**14),      # test_subtract_large_numbers
])
def test_subtract(calc, a, b, expected):
    """Test subtraction with various valid inputs."""
    assert calc.subtract(a, b) == expected


def test_subtract_floats_precise(calc):
    """Test subtraction of floats with precision handling."""
    assert calc.subtract(5.5, 2.3) == pytest.approx(3.2)


# ============================================================================
# CATEGORY 3: MULTIPLICATION TESTS (10 new)
# ============================================================================

@pytest.mark.parametrize("a,b,expected", [
    (4, 5, 20),                         # test_multiply_positive_integers
    (-4, -5, 20),                       # test_multiply_negative_integers
    (4, -5, -20),                       # test_multiply_positive_by_negative
    (-4, 5, -20),                       # test_multiply_negative_by_positive
    (5, 0, 0),                          # test_multiply_by_zero
    (0, 5, 0),                          # test_multiply_zero_by_number
    (7, 1, 7),                          # test_multiply_by_one
    (1, 7, 7),                          # test_multiply_one_by_number
    (10**8, 10**8, 10**16),            # test_multiply_large_numbers
])
def test_multiply(calc, a, b, expected):
    """Test multiplication with various valid inputs."""
    assert calc.multiply(a, b) == expected


def test_multiply_floats_precise(calc):
    """Test multiplication of floats with precision handling."""
    assert calc.multiply(2.5, 4.0) == pytest.approx(10.0)


# ============================================================================
# CATEGORY 4: DIVISION TESTS (7 new, 3 existing preserved)
# ============================================================================

# Existing division-by-zero tests (preserved exactly)
def test_divide_by_zero_integer(calc):
    """Test that dividing by zero with integer raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)


def test_divide_by_zero_float(calc):
    """Test that dividing by zero with float raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(10.5, 0.0)


def test_divide_by_zero_mixed(calc):
    """Test that dividing by zero with mixed int/float raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(7, 0.0)


# New division tests (7 new)
@pytest.mark.parametrize("a,b,expected", [
    (10, 2, 5.0),                       # test_divide_normal_positive
    (-10, 2, -5.0),                     # test_divide_negative_by_positive
    (10, -2, -5.0),                     # test_divide_positive_by_negative
    (-10, -2, 5.0),                     # test_divide_negative_by_negative
])
def test_divide(calc, a, b, expected):
    """Test division with various valid inputs."""
    assert calc.divide(a, b) == expected


def test_divide_result_float(calc):
    """Test division that results in a float."""
    assert calc.divide(7, 2) == pytest.approx(3.5)


def test_divide_floats_precise(calc):
    """Test division of floats with precision handling."""
    assert calc.divide(7.5, 2.5) == pytest.approx(3.0)


def test_divide_large_numbers(calc):
    """Test division with very large numbers."""
    assert calc.divide(10**15, 10**7) == pytest.approx(10**8)


# ============================================================================
# CATEGORY 5: INVALID INPUT TESTS (8 new)
# ============================================================================

@pytest.mark.parametrize("operation,a,b,exception", [
    ("add", "hello", 5, TypeError),                 # test_add_string_and_number
    ("add", None, 5, TypeError),                    # test_add_none_and_number
    ("multiply", None, 5, TypeError),               # test_multiply_none_and_number
    ("divide", "hello", 5, TypeError),              # test_divide_string_and_number
    ("divide", 10, "2", TypeError),                 # test_divide_number_and_string
    ("subtract", None, 5, TypeError),               # test_subtract_none_and_number
])
def test_invalid_inputs_raise_type_error(calc, operation, a, b, exception):
    """Test that invalid input types raise TypeError as expected."""
    method = getattr(calc, operation)
    with pytest.raises(exception):
        method(a, b)


def test_multiply_string_and_int(calc):
    """Test that multiplying string by int works (valid Python behavior)."""
    assert calc.multiply("ab", 3) == "ababab"


def test_add_bool_and_number(calc):
    """Test that adding bool to number works (bool is subclass of int)."""
    assert calc.add(True, 5) == 6


# ============================================================================
# CATEGORY 6: CONSISTENCY AND CROSS-OPERATION TESTS (6 new)
# ============================================================================

def test_add_commutative(calc):
    """Test that addition is commutative: a + b = b + a."""
    assert calc.add(3, 5) == calc.add(5, 3)


def test_subtract_not_commutative(calc):
    """Test that subtraction is not commutative: a - b ≠ b - a."""
    assert calc.subtract(10, 3) != calc.subtract(3, 10)


def test_multiply_commutative(calc):
    """Test that multiplication is commutative: a * b = b * a."""
    assert calc.multiply(4, 5) == calc.multiply(5, 4)


def test_divide_not_commutative(calc):
    """Test that division is not commutative: a / b ≠ b / a."""
    assert calc.divide(10, 2) != calc.divide(2, 10)


def test_addition_inverse_subtraction(calc):
    """Test that subtraction is the inverse of addition."""
    assert calc.subtract(calc.add(7, 3), 3) == 7


def test_multiplication_inverse_division(calc):
    """Test that division is the inverse of multiplication."""
    assert calc.divide(calc.multiply(6, 4), 4) == pytest.approx(6)