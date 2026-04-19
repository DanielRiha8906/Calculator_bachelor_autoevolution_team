import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    """Fixture providing a Calculator instance."""
    return Calculator()


# ============================================================================
# ADDITION TESTS
# ============================================================================

def test_add_positive_integers(calc):
    """Verify addition of two positive integers."""
    result = calc.add(5, 3)
    assert result == 8


def test_add_positive_integers_large(calc):
    """Verify addition of large positive integers."""
    result = calc.add(1000000, 2000000)
    assert result == 3000000


def test_add_negative_integers(calc):
    """Verify addition of two negative integers."""
    result = calc.add(-5, -3)
    assert result == -8


def test_add_mixed_sign_positive_result(calc):
    """Verify addition of mixed sign numbers resulting in positive."""
    result = calc.add(10, -3)
    assert result == 7


def test_add_mixed_sign_negative_result(calc):
    """Verify addition of mixed sign numbers resulting in negative."""
    result = calc.add(3, -10)
    assert result == -7


def test_add_zero_left_operand(calc):
    """Verify addition with zero as left operand."""
    result = calc.add(0, 5)
    assert result == 5


def test_add_zero_right_operand(calc):
    """Verify addition with zero as right operand."""
    result = calc.add(5, 0)
    assert result == 5


def test_add_both_zeros(calc):
    """Verify addition of zero and zero."""
    result = calc.add(0, 0)
    assert result == 0


def test_add_floating_point(calc):
    """Verify addition of floating-point numbers."""
    result = calc.add(2.5, 3.7)
    assert abs(result - 6.2) < 1e-10


def test_add_floating_point_negative(calc):
    """Verify addition of negative floating-point numbers."""
    result = calc.add(-2.5, -3.7)
    assert abs(result - (-6.2)) < 1e-10


def test_add_floating_point_mixed_sign(calc):
    """Verify addition of mixed sign floating-point numbers."""
    result = calc.add(5.5, -2.3)
    assert abs(result - 3.2) < 1e-10


def test_add_integer_and_float(calc):
    """Verify addition of integer and float."""
    result = calc.add(10, 2.5)
    assert abs(result - 12.5) < 1e-10


# ============================================================================
# SUBTRACTION TESTS
# ============================================================================

def test_subtract_positive_integers(calc):
    """Verify subtraction of two positive integers."""
    result = calc.subtract(10, 3)
    assert result == 7


def test_subtract_positive_integers_result_zero(calc):
    """Verify subtraction resulting in zero."""
    result = calc.subtract(5, 5)
    assert result == 0


def test_subtract_positive_integers_result_negative(calc):
    """Verify subtraction of positive integers resulting in negative."""
    result = calc.subtract(3, 10)
    assert result == -7


def test_subtract_negative_integers(calc):
    """Verify subtraction of two negative integers."""
    result = calc.subtract(-10, -3)
    assert result == -7


def test_subtract_negative_from_positive(calc):
    """Verify subtracting a negative number from positive (double negative)."""
    result = calc.subtract(10, -5)
    assert result == 15


def test_subtract_positive_from_negative(calc):
    """Verify subtracting a positive number from negative."""
    result = calc.subtract(-10, 5)
    assert result == -15


def test_subtract_zero_left_operand(calc):
    """Verify subtraction with zero as left operand."""
    result = calc.subtract(0, 5)
    assert result == -5


def test_subtract_zero_right_operand(calc):
    """Verify subtraction with zero as right operand."""
    result = calc.subtract(5, 0)
    assert result == 5


def test_subtract_both_zeros(calc):
    """Verify subtraction of zero from zero."""
    result = calc.subtract(0, 0)
    assert result == 0


def test_subtract_floating_point(calc):
    """Verify subtraction of floating-point numbers."""
    result = calc.subtract(7.5, 2.3)
    assert abs(result - 5.2) < 1e-10


def test_subtract_floating_point_negative(calc):
    """Verify subtraction with negative floating-point numbers."""
    result = calc.subtract(-5.5, -2.3)
    assert abs(result - (-3.2)) < 1e-10


def test_subtract_floating_point_mixed_sign(calc):
    """Verify subtraction of mixed sign floating-point numbers."""
    result = calc.subtract(5.5, -2.3)
    assert abs(result - 7.8) < 1e-10


def test_subtract_integer_and_float(calc):
    """Verify subtraction of integer and float."""
    result = calc.subtract(10, 2.5)
    assert abs(result - 7.5) < 1e-10


# ============================================================================
# MULTIPLICATION TESTS
# ============================================================================

def test_multiply_positive_integers(calc):
    """Verify multiplication of two positive integers."""
    result = calc.multiply(5, 3)
    assert result == 15


def test_multiply_positive_integers_large(calc):
    """Verify multiplication of large positive integers."""
    result = calc.multiply(1000, 2000)
    assert result == 2000000


def test_multiply_by_zero_right(calc):
    """Verify multiplication by zero (right operand)."""
    result = calc.multiply(5, 0)
    assert result == 0


def test_multiply_by_zero_left(calc):
    """Verify multiplication by zero (left operand)."""
    result = calc.multiply(0, 5)
    assert result == 0


def test_multiply_both_zeros(calc):
    """Verify multiplication of zero by zero."""
    result = calc.multiply(0, 0)
    assert result == 0


def test_multiply_by_one_right(calc):
    """Verify multiplication by one (right operand)."""
    result = calc.multiply(5, 1)
    assert result == 5


def test_multiply_by_one_left(calc):
    """Verify multiplication by one (left operand)."""
    result = calc.multiply(1, 5)
    assert result == 5


def test_multiply_negative_integers(calc):
    """Verify multiplication of two negative integers."""
    result = calc.multiply(-5, -3)
    assert result == 15


def test_multiply_negative_positive_integers(calc):
    """Verify multiplication of negative and positive integers."""
    result = calc.multiply(-5, 3)
    assert result == -15


def test_multiply_positive_negative_integers(calc):
    """Verify multiplication of positive and negative integers."""
    result = calc.multiply(5, -3)
    assert result == -15


def test_multiply_floating_point(calc):
    """Verify multiplication of floating-point numbers."""
    result = calc.multiply(2.5, 4.0)
    assert abs(result - 10.0) < 1e-10


def test_multiply_floating_point_negative(calc):
    """Verify multiplication of negative floating-point numbers."""
    result = calc.multiply(-2.5, -4.0)
    assert abs(result - 10.0) < 1e-10


def test_multiply_floating_point_mixed_sign(calc):
    """Verify multiplication of mixed sign floating-point numbers."""
    result = calc.multiply(2.5, -4.0)
    assert abs(result - (-10.0)) < 1e-10


def test_multiply_integer_and_float(calc):
    """Verify multiplication of integer and float."""
    result = calc.multiply(5, 2.5)
    assert abs(result - 12.5) < 1e-10


def test_multiply_fraction_result(calc):
    """Verify multiplication resulting in fractional value."""
    result = calc.multiply(0.5, 0.5)
    assert abs(result - 0.25) < 1e-10


# ============================================================================
# DIVISION TESTS (EXISTING + ADDITIONAL)
# ============================================================================

def test_division_by_zero(calc):
    """Verify that dividing by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calc.divide(10, 0)


def test_division_by_zero_zero_numerator(calc):
    """Verify that 0/0 also raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calc.divide(0, 0)


def test_division_normal(calc):
    """Verify normal division works correctly (regression check)."""
    result = calc.divide(10, 2)
    assert result == 5.0


def test_division_positive_integers(calc):
    """Verify division of two positive integers."""
    result = calc.divide(20, 4)
    assert result == 5.0


def test_division_negative_integers(calc):
    """Verify division of two negative integers."""
    result = calc.divide(-20, -4)
    assert result == 5.0


def test_division_negative_positive_integers(calc):
    """Verify division of negative by positive integer."""
    result = calc.divide(-20, 4)
    assert result == -5.0


def test_division_positive_negative_integers(calc):
    """Verify division of positive by negative integer."""
    result = calc.divide(20, -4)
    assert result == -5.0


def test_division_zero_numerator(calc):
    """Verify division with zero as numerator."""
    result = calc.divide(0, 5)
    assert result == 0.0


def test_division_floating_point(calc):
    """Verify division of floating-point numbers."""
    result = calc.divide(7.5, 2.5)
    assert abs(result - 3.0) < 1e-10


def test_division_floating_point_negative(calc):
    """Verify division of negative floating-point numbers."""
    result = calc.divide(-7.5, -2.5)
    assert abs(result - 3.0) < 1e-10


def test_division_floating_point_mixed_sign(calc):
    """Verify division of mixed sign floating-point numbers."""
    result = calc.divide(7.5, -2.5)
    assert abs(result - (-3.0)) < 1e-10


def test_division_integer_and_float(calc):
    """Verify division of integer by float."""
    result = calc.divide(10, 2.5)
    assert abs(result - 4.0) < 1e-10


def test_division_fractional_result(calc):
    """Verify division resulting in fractional value."""
    result = calc.divide(1, 3)
    assert abs(result - (1/3)) < 1e-10


def test_division_result_less_than_one(calc):
    """Verify division with result less than one."""
    result = calc.divide(1, 2)
    assert abs(result - 0.5) < 1e-10


# ============================================================================
# RESULT CHAINING TESTS
# ============================================================================

def test_add_result_chains_to_multiply(calc):
    """Verify output of add can be input to multiply."""
    result_add = calc.add(2, 3)
    assert isinstance(result_add, (int, float))
    result_multiply = calc.multiply(result_add, 2)
    assert result_multiply == 10


def test_add_result_chains_to_subtract(calc):
    """Verify output of add can be input to subtract."""
    result_add = calc.add(10, 5)
    assert isinstance(result_add, (int, float))
    result_subtract = calc.subtract(result_add, 3)
    assert result_subtract == 12


def test_add_result_chains_to_divide(calc):
    """Verify output of add can be input to divide."""
    result_add = calc.add(4, 6)
    assert isinstance(result_add, (int, float))
    result_divide = calc.divide(result_add, 2)
    assert result_divide == 5.0


def test_subtract_result_chains_to_multiply(calc):
    """Verify output of subtract can be input to multiply."""
    result_subtract = calc.subtract(10, 3)
    assert isinstance(result_subtract, (int, float))
    result_multiply = calc.multiply(result_subtract, 2)
    assert result_multiply == 14


def test_subtract_result_chains_to_add(calc):
    """Verify output of subtract can be input to add."""
    result_subtract = calc.subtract(20, 5)
    assert isinstance(result_subtract, (int, float))
    result_add = calc.add(result_subtract, 3)
    assert result_add == 18


def test_subtract_result_chains_to_divide(calc):
    """Verify output of subtract can be input to divide."""
    result_subtract = calc.subtract(20, 2)
    assert isinstance(result_subtract, (int, float))
    result_divide = calc.divide(result_subtract, 2)
    assert result_divide == 9.0


def test_multiply_result_chains_to_add(calc):
    """Verify output of multiply can be input to add."""
    result_multiply = calc.multiply(5, 3)
    assert isinstance(result_multiply, (int, float))
    result_add = calc.add(result_multiply, 2)
    assert result_add == 17


def test_multiply_result_chains_to_subtract(calc):
    """Verify output of multiply can be input to subtract."""
    result_multiply = calc.multiply(5, 4)
    assert isinstance(result_multiply, (int, float))
    result_subtract = calc.subtract(result_multiply, 3)
    assert result_subtract == 17


def test_multiply_result_chains_to_divide(calc):
    """Verify output of multiply can be input to divide."""
    result_multiply = calc.multiply(4, 5)
    assert isinstance(result_multiply, (int, float))
    result_divide = calc.divide(result_multiply, 2)
    assert result_divide == 10.0


def test_divide_result_chains_to_add(calc):
    """Verify output of divide can be input to add."""
    result_divide = calc.divide(10, 2)
    assert isinstance(result_divide, (int, float))
    result_add = calc.add(result_divide, 3)
    assert result_add == 8.0


def test_divide_result_chains_to_subtract(calc):
    """Verify output of divide can be input to subtract."""
    result_divide = calc.divide(20, 4)
    assert isinstance(result_divide, (int, float))
    result_subtract = calc.subtract(result_divide, 2)
    assert result_subtract == 3.0


def test_divide_result_chains_to_multiply(calc):
    """Verify output of divide can be input to multiply."""
    result_divide = calc.divide(15, 3)
    assert isinstance(result_divide, (int, float))
    result_multiply = calc.multiply(result_divide, 2)
    assert result_multiply == 10.0


def test_complex_chaining_add_subtract_multiply(calc):
    """Verify complex chaining: add -> subtract -> multiply."""
    result1 = calc.add(5, 5)
    assert isinstance(result1, (int, float))
    result2 = calc.subtract(result1, 2)
    assert isinstance(result2, (int, float))
    result3 = calc.multiply(result2, 2)
    assert result3 == 16


def test_complex_chaining_multiply_divide_add(calc):
    """Verify complex chaining: multiply -> divide -> add."""
    result1 = calc.multiply(10, 4)
    assert isinstance(result1, (int, float))
    result2 = calc.divide(result1, 5)
    assert isinstance(result2, (int, float))
    result3 = calc.add(result2, 1)
    assert abs(result3 - 9.0) < 1e-10


# ============================================================================
# FACTORIAL TESTS
# ============================================================================

def test_factorial_zero(calc):
    """Verify factorial of zero returns 1."""
    result = calc.factorial(0)
    assert result == 1
    assert isinstance(result, int)


def test_factorial_one(calc):
    """Verify factorial of one returns 1."""
    result = calc.factorial(1)
    assert result == 1
    assert isinstance(result, int)


def test_factorial_two(calc):
    """Verify factorial of two returns 2."""
    result = calc.factorial(2)
    assert result == 2
    assert isinstance(result, int)


def test_factorial_three(calc):
    """Verify factorial of three returns 6."""
    result = calc.factorial(3)
    assert result == 6
    assert isinstance(result, int)


def test_factorial_five(calc):
    """Verify factorial of five returns 120."""
    result = calc.factorial(5)
    assert result == 120
    assert isinstance(result, int)


def test_factorial_ten(calc):
    """Verify factorial of ten returns 3628800."""
    result = calc.factorial(10)
    assert result == 3628800
    assert isinstance(result, int)


def test_factorial_large_value(calc):
    """Verify factorial of 20 returns 2432902008176640000."""
    result = calc.factorial(20)
    assert result == 2432902008176640000
    assert isinstance(result, int)


def test_factorial_result_type(calc):
    """Verify factorial result is always an integer."""
    result = calc.factorial(7)
    assert isinstance(result, int)
    assert result == 5040


def test_factorial_float_integer_value(calc):
    """Verify factorial with float representing integer (5.0) returns 120."""
    result = calc.factorial(5.0)
    assert result == 120
    assert isinstance(result, int)


def test_factorial_float_zero(calc):
    """Verify factorial with 0.0 returns 1."""
    result = calc.factorial(0.0)
    assert result == 1
    assert isinstance(result, int)


def test_factorial_negative_integer(calc):
    """Verify factorial of negative integer raises ValueError."""
    with pytest.raises(ValueError, match="factorial\\(\\) not defined for negative values"):
        calc.factorial(-5)


def test_factorial_negative_one(calc):
    """Verify factorial of -1 raises ValueError."""
    with pytest.raises(ValueError, match="factorial\\(\\) not defined for negative values"):
        calc.factorial(-1)


def test_factorial_float_non_integer(calc):
    """Verify factorial with non-integer float (5.5) raises TypeError."""
    with pytest.raises(TypeError, match="factorial\\(\\) only accepts integer values, not non-integer floats"):
        calc.factorial(5.5)


def test_factorial_negative_float(calc):
    """Verify factorial with negative float (-0.5) raises TypeError (type check first)."""
    with pytest.raises(TypeError, match="factorial\\(\\) only accepts integer values, not non-integer floats"):
        calc.factorial(-0.5)


def test_factorial_result_chains_to_add(calc):
    """Verify factorial result can be used as input to add."""
    result_factorial = calc.factorial(5)
    assert result_factorial == 120
    assert isinstance(result_factorial, int)
    result_add = calc.add(result_factorial, 30)
    assert result_add == 150


def test_factorial_result_chains_to_multiply(calc):
    """Verify factorial result can be used as input to multiply."""
    result_factorial = calc.factorial(5)
    assert result_factorial == 120
    assert isinstance(result_factorial, int)
    result_multiply = calc.multiply(result_factorial, 2)
    assert result_multiply == 240


def test_factorial_result_chains_to_divide(calc):
    """Verify factorial result can be used as input to divide."""
    result_factorial = calc.factorial(4)
    assert result_factorial == 24
    assert isinstance(result_factorial, int)
    result_divide = calc.divide(result_factorial, 2)
    assert result_divide == 12.0


def test_factorial_result_chains_to_subtract(calc):
    """Verify factorial result can be used as input to subtract."""
    result_factorial = calc.factorial(5)
    assert result_factorial == 120
    assert isinstance(result_factorial, int)
    result_subtract = calc.subtract(result_factorial, 20)
    assert result_subtract == 100


# ============================================================================
# SQUARE TESTS
# ============================================================================

def test_square_positive_integer(calc):
    """Verify square of positive integer."""
    result = calc.square(5)
    assert result == 25


def test_square_zero(calc):
    """Verify square of zero."""
    result = calc.square(0)
    assert result == 0


def test_square_negative_integer(calc):
    """Verify square of negative integer."""
    result = calc.square(-5)
    assert result == 25


def test_square_positive_float(calc):
    """Verify square of positive float."""
    result = calc.square(2.5)
    assert abs(result - 6.25) < 1e-10


def test_square_negative_float(calc):
    """Verify square of negative float."""
    result = calc.square(-2.5)
    assert abs(result - 6.25) < 1e-10


def test_square_one(calc):
    """Verify square of one."""
    result = calc.square(1)
    assert result == 1


def test_square_large_value(calc):
    """Verify square of large value."""
    result = calc.square(1000)
    assert result == 1000000


def test_square_small_float(calc):
    """Verify square of small float."""
    result = calc.square(0.5)
    assert abs(result - 0.25) < 1e-10


def test_square_result_chains_to_add(calc):
    """Verify output of square can be input to add."""
    result_square = calc.square(5)
    assert result_square == 25
    result_add = calc.add(result_square, 5)
    assert result_add == 30


def test_square_result_chains_to_multiply(calc):
    """Verify output of square can be input to multiply."""
    result_square = calc.square(4)
    assert result_square == 16
    result_multiply = calc.multiply(result_square, 2)
    assert result_multiply == 32


# ============================================================================
# CUBE TESTS
# ============================================================================

def test_cube_positive_integer(calc):
    """Verify cube of positive integer."""
    result = calc.cube(3)
    assert result == 27


def test_cube_zero(calc):
    """Verify cube of zero."""
    result = calc.cube(0)
    assert result == 0


def test_cube_negative_integer(calc):
    """Verify cube of negative integer."""
    result = calc.cube(-3)
    assert result == -27


def test_cube_positive_float(calc):
    """Verify cube of positive float."""
    result = calc.cube(2.0)
    assert abs(result - 8.0) < 1e-10


def test_cube_negative_float(calc):
    """Verify cube of negative float."""
    result = calc.cube(-2.0)
    assert abs(result - (-8.0)) < 1e-10


def test_cube_one(calc):
    """Verify cube of one."""
    result = calc.cube(1)
    assert result == 1


def test_cube_large_value(calc):
    """Verify cube of large value."""
    result = calc.cube(10)
    assert result == 1000


def test_cube_small_float(calc):
    """Verify cube of small float."""
    result = calc.cube(0.5)
    assert abs(result - 0.125) < 1e-10


def test_cube_result_chains_to_add(calc):
    """Verify output of cube can be input to add."""
    result_cube = calc.cube(3)
    assert result_cube == 27
    result_add = calc.add(result_cube, 3)
    assert result_add == 30


def test_cube_result_chains_to_multiply(calc):
    """Verify output of cube can be input to multiply."""
    result_cube = calc.cube(2)
    assert result_cube == 8
    result_multiply = calc.multiply(result_cube, 2)
    assert result_multiply == 16


# ============================================================================
# SQUARE ROOT TESTS
# ============================================================================

def test_square_root_perfect_square(calc):
    """Verify square root of perfect square."""
    result = calc.square_root(4)
    assert result == 2


def test_square_root_zero(calc):
    """Verify square root of zero."""
    result = calc.square_root(0)
    assert result == 0


def test_square_root_one(calc):
    """Verify square root of one."""
    result = calc.square_root(1)
    assert result == 1


def test_square_root_float(calc):
    """Verify square root of float."""
    result = calc.square_root(2.25)
    assert abs(result - 1.5) < 1e-10


def test_square_root_large_value(calc):
    """Verify square root of large value."""
    result = calc.square_root(10000)
    assert result == 100


def test_square_root_small_float(calc):
    """Verify square root of small float."""
    result = calc.square_root(0.25)
    assert abs(result - 0.5) < 1e-10


def test_square_root_non_perfect_square(calc):
    """Verify square root of non-perfect square with tolerance."""
    result = calc.square_root(2)
    assert abs(result - 1.41421356237) < 1e-10


def test_square_root_negative_integer(calc):
    """Verify square root of negative integer raises ValueError."""
    with pytest.raises(ValueError, match="square_root\\(\\) not defined for negative values"):
        calc.square_root(-1)


def test_square_root_negative_float(calc):
    """Verify square root of negative float raises ValueError."""
    with pytest.raises(ValueError, match="square_root\\(\\) not defined for negative values"):
        calc.square_root(-2.5)


def test_square_root_result_chains_to_add(calc):
    """Verify output of square_root can be input to add."""
    result_sqrt = calc.square_root(4)
    assert result_sqrt == 2
    result_add = calc.add(result_sqrt, 3)
    assert result_add == 5


def test_square_root_result_chains_to_multiply(calc):
    """Verify output of square_root can be input to multiply."""
    result_sqrt = calc.square_root(9)
    assert result_sqrt == 3
    result_multiply = calc.multiply(result_sqrt, 2)
    assert result_multiply == 6


def test_square_root_result_chains_to_divide(calc):
    """Verify output of square_root can be input to divide."""
    result_sqrt = calc.square_root(16)
    assert result_sqrt == 4
    result_divide = calc.divide(result_sqrt, 2)
    assert abs(result_divide - 2.0) < 1e-10


# ============================================================================
# CUBE ROOT TESTS
# ============================================================================

def test_cube_root_perfect_cube(calc):
    """Verify cube root of perfect cube."""
    result = calc.cube_root(8)
    assert abs(result - 2) < 1e-10


def test_cube_root_zero(calc):
    """Verify cube root of zero."""
    result = calc.cube_root(0)
    assert result == 0.0


def test_cube_root_one(calc):
    """Verify cube root of one."""
    result = calc.cube_root(1)
    assert abs(result - 1) < 1e-10


def test_cube_root_negative_integer(calc):
    """Verify cube root of negative integer."""
    result = calc.cube_root(-8)
    assert abs(result - (-2)) < 1e-10


def test_cube_root_negative_float(calc):
    """Verify cube root of negative float."""
    result = calc.cube_root(-27.0)
    assert abs(result - (-3.0)) < 1e-10


def test_cube_root_float(calc):
    """Verify cube root of float."""
    result = calc.cube_root(8.0)
    assert abs(result - 2.0) < 1e-10


def test_cube_root_large_value(calc):
    """Verify cube root of large value."""
    result = calc.cube_root(1000)
    assert abs(result - 10) < 1e-10


def test_cube_root_small_float(calc):
    """Verify cube root of small float."""
    result = calc.cube_root(0.125)
    assert abs(result - 0.5) < 1e-10


def test_cube_root_non_perfect_cube(calc):
    """Verify cube root of non-perfect cube."""
    result = calc.cube_root(2)
    assert abs(result - 1.2599210498948732) < 1e-9


def test_cube_root_negative_non_perfect(calc):
    """Verify cube root of negative non-perfect cube."""
    result = calc.cube_root(-2)
    assert abs(result - (-1.2599210498948732)) < 1e-9


def test_cube_root_result_chains_to_add(calc):
    """Verify output of cube_root can be input to add."""
    result_cbrt = calc.cube_root(8)
    assert abs(result_cbrt - 2) < 1e-10
    result_add = calc.add(result_cbrt, 3)
    assert abs(result_add - 5) < 1e-10


def test_cube_root_result_chains_to_multiply(calc):
    """Verify output of cube_root can be input to multiply."""
    result_cbrt = calc.cube_root(27)
    assert abs(result_cbrt - 3) < 1e-10
    result_multiply = calc.multiply(result_cbrt, 2)
    assert abs(result_multiply - 6) < 1e-10


# ============================================================================
# POWER TESTS
# ============================================================================

def test_power_positive_integer_exponent(calc):
    """Verify power with positive integer exponent."""
    result = calc.power(2, 5)
    assert result == 32


def test_power_zero_base(calc):
    """Verify power with zero base."""
    result = calc.power(0, 3)
    assert result == 0


def test_power_one_base(calc):
    """Verify power with one base."""
    result = calc.power(1, 5)
    assert result == 1


def test_power_zero_exponent(calc):
    """Verify power with zero exponent."""
    result = calc.power(5, 0)
    assert result == 1


def test_power_one_exponent(calc):
    """Verify power with one exponent."""
    result = calc.power(5, 1)
    assert result == 5


def test_power_negative_integer_base(calc):
    """Verify power with negative integer base and even exponent."""
    result = calc.power(-2, 4)
    assert result == 16


def test_power_negative_integer_base_odd_exponent(calc):
    """Verify power with negative integer base and odd exponent."""
    result = calc.power(-2, 3)
    assert result == -8


def test_power_float_base(calc):
    """Verify power with float base."""
    result = calc.power(2.5, 2)
    assert abs(result - 6.25) < 1e-10


def test_power_float_exponent(calc):
    """Verify power with float exponent (square root case)."""
    result = calc.power(4, 0.5)
    assert abs(result - 2.0) < 1e-10


def test_power_negative_float_base(calc):
    """Verify power with negative float base and even exponent."""
    result = calc.power(-2.0, 2)
    assert abs(result - 4.0) < 1e-10


def test_power_both_floats(calc):
    """Verify power with both base and exponent as floats."""
    result = calc.power(2.0, 3.0)
    assert abs(result - 8.0) < 1e-10


def test_power_fractional_exponent(calc):
    """Verify power with fractional exponent."""
    result = calc.power(8, 1/3)
    assert abs(result - 2.0) < 1e-10


def test_power_result_chains_to_add(calc):
    """Verify output of power can be input to add."""
    result_power = calc.power(2, 3)
    assert result_power == 8
    result_add = calc.add(result_power, 2)
    assert result_add == 10


def test_power_result_chains_to_multiply(calc):
    """Verify output of power can be input to multiply."""
    result_power = calc.power(3, 2)
    assert result_power == 9
    result_multiply = calc.multiply(result_power, 2)
    assert result_multiply == 18


# ============================================================================
# LOGARITHM (BASE 10) TESTS
# ============================================================================

def test_logarithm_one(calc):
    """Verify logarithm of one equals zero."""
    result = calc.logarithm(1)
    assert result == 0


def test_logarithm_ten(calc):
    """Verify logarithm of ten equals one."""
    result = calc.logarithm(10)
    assert abs(result - 1) < 1e-10


def test_logarithm_hundred(calc):
    """Verify logarithm of hundred equals two."""
    result = calc.logarithm(100)
    assert abs(result - 2) < 1e-10


def test_logarithm_decimal_less_than_one(calc):
    """Verify logarithm of 0.1 equals -1."""
    result = calc.logarithm(0.1)
    assert abs(result - (-1)) < 1e-10


def test_logarithm_decimal_value(calc):
    """Verify logarithm of 2 approximately."""
    result = calc.logarithm(2)
    assert abs(result - 0.30103) < 1e-8


def test_logarithm_zero(calc):
    """Verify logarithm of zero raises ValueError."""
    with pytest.raises(ValueError, match="logarithm\\(\\) not defined for non-positive values"):
        calc.logarithm(0)


def test_logarithm_negative_integer(calc):
    """Verify logarithm of negative integer raises ValueError."""
    with pytest.raises(ValueError, match="logarithm\\(\\) not defined for non-positive values"):
        calc.logarithm(-5)


def test_logarithm_negative_float(calc):
    """Verify logarithm of negative float raises ValueError."""
    with pytest.raises(ValueError, match="logarithm\\(\\) not defined for non-positive values"):
        calc.logarithm(-1.5)


def test_logarithm_large_value(calc):
    """Verify logarithm of large value."""
    result = calc.logarithm(1000000)
    assert abs(result - 6) < 1e-10


def test_logarithm_small_positive_value(calc):
    """Verify logarithm of small positive value."""
    result = calc.logarithm(0.001)
    assert abs(result - (-3)) < 1e-10


def test_logarithm_result_chains_to_add(calc):
    """Verify output of logarithm can be input to add."""
    result_log = calc.logarithm(100)
    assert abs(result_log - 2) < 1e-10
    result_add = calc.add(result_log, 3)
    assert abs(result_add - 5) < 1e-10


# ============================================================================
# NATURAL LOGARITHM (BASE E) TESTS
# ============================================================================

def test_natural_logarithm_one(calc):
    """Verify natural logarithm of one equals zero."""
    result = calc.natural_logarithm(1)
    assert result == 0


def test_natural_logarithm_e(calc):
    """Verify natural logarithm of e equals one."""
    result = calc.natural_logarithm(math.e)
    assert abs(result - 1.0) < 1e-10


def test_natural_logarithm_decimal_less_than_one(calc):
    """Verify natural logarithm of 0.5."""
    result = calc.natural_logarithm(0.5)
    assert abs(result - (-0.6931471805599453)) < 1e-9


def test_natural_logarithm_value(calc):
    """Verify natural logarithm of 2."""
    result = calc.natural_logarithm(2)
    assert abs(result - 0.6931471805599453) < 1e-9


def test_natural_logarithm_large_value(calc):
    """Verify natural logarithm of large value."""
    result = calc.natural_logarithm(1000)
    assert abs(result - 6.907755278982137) < 1e-8


def test_natural_logarithm_zero(calc):
    """Verify natural logarithm of zero raises ValueError."""
    with pytest.raises(ValueError, match="natural_logarithm\\(\\) not defined for non-positive values"):
        calc.natural_logarithm(0)


def test_natural_logarithm_negative_integer(calc):
    """Verify natural logarithm of negative integer raises ValueError."""
    with pytest.raises(ValueError, match="natural_logarithm\\(\\) not defined for non-positive values"):
        calc.natural_logarithm(-5)


def test_natural_logarithm_negative_float(calc):
    """Verify natural logarithm of negative float raises ValueError."""
    with pytest.raises(ValueError, match="natural_logarithm\\(\\) not defined for non-positive values"):
        calc.natural_logarithm(-1.5)


def test_natural_logarithm_small_positive_value(calc):
    """Verify natural logarithm of small positive value."""
    result = calc.natural_logarithm(0.001)
    assert abs(result - (-6.907755278982137)) < 1e-8


def test_natural_logarithm_result_chains_to_add(calc):
    """Verify output of natural_logarithm can be input to add."""
    result_ln = calc.natural_logarithm(math.e)
    assert abs(result_ln - 1.0) < 1e-10
    result_add = calc.add(result_ln, 2)
    assert abs(result_add - 3.0) < 1e-10


def test_natural_logarithm_result_chains_to_multiply(calc):
    """Verify output of natural_logarithm can be input to multiply."""
    result_ln = calc.natural_logarithm(math.e)
    assert abs(result_ln - 1.0) < 1e-10
    result_multiply = calc.multiply(result_ln, 5)
    assert abs(result_multiply - 5.0) < 1e-10