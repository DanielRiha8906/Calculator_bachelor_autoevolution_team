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


# ============================================================================
# CATEGORY 7: FACTORIAL TESTS
# ============================================================================

# Category 1: Valid Non-Negative Integers
def test_factorial_zero(calc):
    """Test factorial of 0 equals 1 (by definition)."""
    assert calc.factorial(0) == 1


def test_factorial_one(calc):
    """Test factorial of 1 equals 1."""
    assert calc.factorial(1) == 1


@pytest.mark.parametrize("n,expected", [
    (2, 2),
    (3, 6),
    (5, 120),
    (10, 3628800),
])
def test_factorial_positive_integers(calc, n, expected):
    """Test factorial computation for positive integers."""
    assert calc.factorial(n) == expected


def test_factorial_large_number(calc):
    """Test factorial of a larger number."""
    assert calc.factorial(20) == 2432902008176640000


# Category 2: Negative Integers
@pytest.mark.parametrize("n", [-1, -5, -100])
def test_factorial_negative_integers_raise_value_error(calc, n):
    """Test that negative integers raise ValueError with 'negative' in message."""
    with pytest.raises(ValueError) as exc_info:
        calc.factorial(n)
    assert "negative" in str(exc_info.value).lower()


# Category 3: Non-Integer Types
def test_factorial_float_raises_error(calc):
    """Test that float input raises ValueError or TypeError."""
    with pytest.raises((ValueError, TypeError)):
        calc.factorial(3.5)


def test_factorial_string_raises_error(calc):
    """Test that string input raises ValueError or TypeError."""
    with pytest.raises((ValueError, TypeError)):
        calc.factorial("5")


def test_factorial_none_raises_error(calc):
    """Test that None input raises ValueError or TypeError."""
    with pytest.raises((ValueError, TypeError)):
        calc.factorial(None)


@pytest.mark.parametrize("b", [True, False])
def test_factorial_bool_raises_error(calc, b):
    """Test that bool input raises ValueError or TypeError (bool is subclass of int)."""
    with pytest.raises((ValueError, TypeError)):
        calc.factorial(b)


# Category 4: Type Consistency
def test_factorial_returns_int(calc):
    """Test that factorial always returns int type."""
    result = calc.factorial(5)
    assert isinstance(result, int)


@pytest.mark.parametrize("n", [0, 1, 5, 10, 15])
def test_factorial_matches_math_factorial(calc, n):
    """Test factorial matches math.factorial() for validation."""
    assert calc.factorial(n) == math.factorial(n)


# ============================================================================
# CATEGORY 8: UNARY OPERATIONS - SQUARE
# ============================================================================

@pytest.mark.parametrize("x,expected", [
    (0, 0),
    (5, 25),
    (-3, 9),
    (2.5, 6.25),
    (1000, 1000000),
])
def test_square(calc, x, expected):
    """Test square operation with various valid inputs."""
    assert calc.square(x) == expected


# ============================================================================
# CATEGORY 9: UNARY OPERATIONS - CUBE
# ============================================================================

@pytest.mark.parametrize("x,expected", [
    (0, 0),
    (3, 27),
    (-2, -8),
    (2.0, 8.0),
    (100, 1000000),
])
def test_cube(calc, x, expected):
    """Test cube operation with various valid inputs."""
    assert calc.cube(x) == expected


# ============================================================================
# CATEGORY 10: UNARY OPERATIONS - SQUARE ROOT
# ============================================================================

@pytest.mark.parametrize("x,expected", [
    (0, 0.0),
    (9, 3.0),
    (4.0, 2.0),
    (1, 1.0),
])
def test_sqrt_valid_inputs(calc, x, expected):
    """Test square root with valid inputs."""
    assert calc.sqrt(x) == expected


def test_sqrt_non_perfect_square(calc):
    """Test square root of non-perfect square."""
    assert calc.sqrt(2) == pytest.approx(1.4142135623730951)


@pytest.mark.parametrize("x", [-1, -100])
def test_sqrt_negative_raises_value_error(calc, x):
    """Test that negative input to sqrt raises ValueError."""
    with pytest.raises(ValueError):
        calc.sqrt(x)


# ============================================================================
# CATEGORY 11: UNARY OPERATIONS - CUBE ROOT
# ============================================================================

@pytest.mark.parametrize("x,expected", [
    (0, 0.0),
    (8, 2.0),
    (-8, -2.0),
    (1, 1.0),
    (-1, -1.0),
    (27.0, 3.0),
    (-27.0, -3.0),
])
def test_cbrt_valid_inputs(calc, x, expected):
    """Test cube root with valid inputs."""
    assert calc.cbrt(x) == expected


def test_cbrt_non_perfect_cube(calc):
    """Test cube root of non-perfect cube."""
    assert calc.cbrt(2) == pytest.approx(1.2599210498948732)


# ============================================================================
# CATEGORY 12: UNARY OPERATIONS - LOG BASE 10
# ============================================================================

@pytest.mark.parametrize("x,expected", [
    (1, 0.0),
    (10, 1.0),
    (100, 2.0),
])
def test_log10_valid_inputs(calc, x, expected):
    """Test log base 10 with valid inputs."""
    assert calc.log10(x) == expected


def test_log10_float(calc):
    """Test log base 10 with float input."""
    assert calc.log10(10.5) == pytest.approx(1.0211892990699383)


@pytest.mark.parametrize("x", [0, -5, -100])
def test_log10_invalid_raises_value_error(calc, x):
    """Test that zero or negative inputs to log10 raise ValueError."""
    with pytest.raises(ValueError):
        calc.log10(x)


# ============================================================================
# CATEGORY 13: UNARY OPERATIONS - NATURAL LOGARITHM (LN)
# ============================================================================

@pytest.mark.parametrize("x,expected", [
    (1, 0.0),
    (math.e, pytest.approx(1.0)),
])
def test_ln_valid_inputs(calc, x, expected):
    """Test natural logarithm with valid inputs."""
    assert calc.ln(x) == expected


def test_ln_float_input(calc):
    """Test natural logarithm with float input."""
    assert calc.ln(2.718) == pytest.approx(0.9998962584672666)


def test_ln_ten(calc):
    """Test natural logarithm of 10."""
    assert calc.ln(10) == pytest.approx(2.302585092994046)


@pytest.mark.parametrize("x", [0, -1, -100])
def test_ln_invalid_raises_value_error(calc, x):
    """Test that zero or negative inputs to ln raise ValueError."""
    with pytest.raises(ValueError):
        calc.ln(x)


# ============================================================================
# CATEGORY 14: BINARY OPERATION - POWER
# ============================================================================

@pytest.mark.parametrize("base,exp,expected", [
    (2, 3, 8),
    (5, 0, 1),
    (2, -1, 0.5),
    (-2, 2, 4),
    (-2, 3, -8),
    (1, 100, 1),
    (0, 5, 0),
    (0, 0, 1),
    (2.5, 2, 6.25),
    (4, 0.5, pytest.approx(2.0)),
    (2, 10, 1024),
])
def test_power(calc, base, exp, expected):
    """Test power operation with various valid inputs."""
    assert calc.power(base, exp) == expected