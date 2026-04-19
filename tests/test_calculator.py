import pytest
import math
import logging
from datetime import datetime
from src.logic import Calculator
from src.history import OperationRecord, OperationHistory


@pytest.fixture
def calculator():
    """Provides a fresh Calculator instance for each test."""
    return Calculator()


# ============================================================================
# ADD OPERATION TESTS
# ============================================================================

class TestAdd:
    """Test suite for the add operation."""

    def test_add_positive_integers(self, calculator):
        """Test adding two positive integers."""
        assert calculator.add(5, 3) == 8

    def test_add_positive_floats(self, calculator):
        """Test adding two positive floats."""
        assert calculator.add(5.5, 3.2) == pytest.approx(8.7)

    def test_add_positive_and_negative(self, calculator):
        """Test adding a positive and negative integer."""
        assert calculator.add(10, -3) == 7

    def test_add_negative_integers(self, calculator):
        """Test adding two negative integers."""
        assert calculator.add(-5, -3) == -8

    def test_add_negative_floats(self, calculator):
        """Test adding two negative floats."""
        assert calculator.add(-5.5, -3.2) == pytest.approx(-8.7)

    def test_add_zero_to_number(self, calculator):
        """Test adding zero to a number."""
        assert calculator.add(5, 0) == 5

    def test_add_number_to_zero(self, calculator):
        """Test adding a number to zero."""
        assert calculator.add(0, 5) == 5

    def test_add_zero_to_zero(self, calculator):
        """Test adding zero to zero."""
        assert calculator.add(0, 0) == 0

    def test_add_zero_to_negative(self, calculator):
        """Test adding zero to a negative number."""
        assert calculator.add(-5, 0) == -5

    def test_add_large_numbers(self, calculator):
        """Test adding large integers."""
        assert calculator.add(1000000, 2000000) == 3000000

    def test_add_large_floats(self, calculator):
        """Test adding large floats."""
        assert calculator.add(1e10, 2e10) == pytest.approx(3e10)

    def test_add_very_small_floats(self, calculator):
        """Test adding very small floats."""
        assert calculator.add(1e-10, 2e-10) == pytest.approx(3e-10)

    def test_add_none_first_operand(self, calculator):
        """Test adding None as first operand raises TypeError."""
        with pytest.raises(TypeError):
            calculator.add(None, 5)

    def test_add_none_second_operand(self, calculator):
        """Test adding None as second operand raises TypeError."""
        with pytest.raises(TypeError):
            calculator.add(5, None)

    def test_add_string_first_operand(self, calculator):
        """Test adding string as first operand raises TypeError."""
        with pytest.raises(TypeError):
            calculator.add("abc", 5)

    def test_add_string_second_operand(self, calculator):
        """Test adding string as second operand raises TypeError."""
        with pytest.raises(TypeError):
            calculator.add(5, "abc")

    def test_add_two_strings(self, calculator):
        """Test adding two strings (concatenation is allowed in Python)."""
        # Note: Python allows string concatenation with +
        assert calculator.add("hello", "world") == "helloworld"

    def test_add_mixed_string_number(self, calculator):
        """Test adding mixed string and number raises TypeError."""
        with pytest.raises(TypeError):
            calculator.add("5", 10)

    def test_add_empty_string_to_number(self, calculator):
        """Test adding empty string to number raises TypeError."""
        with pytest.raises(TypeError):
            calculator.add("", 5)

    def test_add_float_and_int(self, calculator):
        """Test adding float and int."""
        assert calculator.add(5, 3.5) == 8.5


# ============================================================================
# SUBTRACT OPERATION TESTS
# ============================================================================

class TestSubtract:
    """Test suite for the subtract operation."""

    def test_subtract_positive_integers(self, calculator):
        """Test subtracting two positive integers."""
        assert calculator.subtract(10, 3) == 7

    def test_subtract_positive_floats(self, calculator):
        """Test subtracting two positive floats."""
        assert calculator.subtract(10.5, 3.2) == pytest.approx(7.3)

    def test_subtract_positive_minus_negative(self, calculator):
        """Test subtracting negative from positive."""
        assert calculator.subtract(10, -3) == 13

    def test_subtract_negative_minus_positive(self, calculator):
        """Test subtracting positive from negative."""
        assert calculator.subtract(-10, 3) == -13

    def test_subtract_two_negatives(self, calculator):
        """Test subtracting two negative numbers."""
        assert calculator.subtract(-10, -3) == -7

    def test_subtract_zero_from_number(self, calculator):
        """Test subtracting zero from a number."""
        assert calculator.subtract(5, 0) == 5

    def test_subtract_number_from_zero(self, calculator):
        """Test subtracting a number from zero."""
        assert calculator.subtract(0, 5) == -5

    def test_subtract_zero_from_zero(self, calculator):
        """Test subtracting zero from zero."""
        assert calculator.subtract(0, 0) == 0

    def test_subtract_same_number(self, calculator):
        """Test subtracting a number from itself."""
        assert calculator.subtract(42, 42) == 0

    def test_subtract_large_numbers(self, calculator):
        """Test subtracting large integers."""
        assert calculator.subtract(5000000, 2000000) == 3000000

    def test_subtract_large_floats(self, calculator):
        """Test subtracting large floats."""
        assert calculator.subtract(5e10, 2e10) == pytest.approx(3e10)

    def test_subtract_very_small_floats(self, calculator):
        """Test subtracting very small floats."""
        assert calculator.subtract(3e-10, 2e-10) == pytest.approx(1e-10)

    def test_subtract_none_first_operand(self, calculator):
        """Test subtracting with None as first operand raises TypeError."""
        with pytest.raises(TypeError):
            calculator.subtract(None, 5)

    def test_subtract_none_second_operand(self, calculator):
        """Test subtracting with None as second operand raises TypeError."""
        with pytest.raises(TypeError):
            calculator.subtract(5, None)

    def test_subtract_string_first_operand(self, calculator):
        """Test subtracting with string as first operand raises TypeError."""
        with pytest.raises(TypeError):
            calculator.subtract("abc", 5)

    def test_subtract_string_second_operand(self, calculator):
        """Test subtracting with string as second operand raises TypeError."""
        with pytest.raises(TypeError):
            calculator.subtract(5, "abc")

    def test_subtract_float_and_int(self, calculator):
        """Test subtracting int from float."""
        assert calculator.subtract(10.5, 3) == 7.5

    def test_subtract_larger_from_smaller(self, calculator):
        """Test subtracting larger from smaller number (negative result)."""
        assert calculator.subtract(3, 10) == -7


# ============================================================================
# MULTIPLY OPERATION TESTS
# ============================================================================

class TestMultiply:
    """Test suite for the multiply operation."""

    def test_multiply_positive_integers(self, calculator):
        """Test multiplying two positive integers."""
        assert calculator.multiply(5, 3) == 15

    def test_multiply_positive_floats(self, calculator):
        """Test multiplying two positive floats."""
        assert calculator.multiply(5.5, 2.0) == pytest.approx(11.0)

    def test_multiply_positive_and_negative(self, calculator):
        """Test multiplying positive and negative integer."""
        assert calculator.multiply(10, -3) == -30

    def test_multiply_two_negatives(self, calculator):
        """Test multiplying two negative integers."""
        assert calculator.multiply(-5, -3) == 15

    def test_multiply_two_negative_floats(self, calculator):
        """Test multiplying two negative floats."""
        assert calculator.multiply(-5.5, -2.0) == pytest.approx(11.0)

    def test_multiply_by_zero(self, calculator):
        """Test multiplying any number by zero."""
        assert calculator.multiply(5, 0) == 0

    def test_multiply_zero_by_number(self, calculator):
        """Test multiplying zero by any number."""
        assert calculator.multiply(0, 5) == 0

    def test_multiply_zero_by_zero(self, calculator):
        """Test multiplying zero by zero."""
        assert calculator.multiply(0, 0) == 0

    def test_multiply_zero_by_negative(self, calculator):
        """Test multiplying zero by negative number."""
        assert calculator.multiply(0, -5) == 0

    def test_multiply_by_one(self, calculator):
        """Test multiplying by one (identity)."""
        assert calculator.multiply(5, 1) == 5

    def test_multiply_one_by_number(self, calculator):
        """Test multiplying one by a number."""
        assert calculator.multiply(1, 5) == 5

    def test_multiply_by_negative_one(self, calculator):
        """Test multiplying by negative one."""
        assert calculator.multiply(5, -1) == -5

    def test_multiply_large_numbers(self, calculator):
        """Test multiplying large integers."""
        assert calculator.multiply(1000000, 2000000) == 2000000000000

    def test_multiply_large_floats(self, calculator):
        """Test multiplying large floats."""
        assert calculator.multiply(1e5, 2e5) == pytest.approx(2e10)

    def test_multiply_very_small_floats(self, calculator):
        """Test multiplying very small floats."""
        assert calculator.multiply(1e-10, 2e-10) == pytest.approx(2e-20)

    def test_multiply_none_first_operand(self, calculator):
        """Test multiplying with None as first operand raises TypeError."""
        with pytest.raises(TypeError):
            calculator.multiply(None, 5)

    def test_multiply_none_second_operand(self, calculator):
        """Test multiplying with None as second operand raises TypeError."""
        with pytest.raises(TypeError):
            calculator.multiply(5, None)

    def test_multiply_string_first_operand(self, calculator):
        """Test multiplying string by integer (repetition allowed in Python)."""
        # Note: Python allows string repetition with * (int operand)
        assert calculator.multiply("ab", 3) == "ababab"

    def test_multiply_string_second_operand(self, calculator):
        """Test multiplying string as second operand."""
        # Note: Python allows string repetition with * (int operand)
        assert calculator.multiply("ab", 3) == "ababab"

    def test_multiply_float_and_int(self, calculator):
        """Test multiplying float and int."""
        assert calculator.multiply(5.5, 2) == 11.0

    def test_multiply_negative_float_and_positive_int(self, calculator):
        """Test multiplying negative float by positive int."""
        assert calculator.multiply(-5.5, 2) == pytest.approx(-11.0)


# ============================================================================
# DIVIDE OPERATION TESTS (KEEP EXISTING + ADD NEW)
# ============================================================================

class TestDivide:
    """Test suite for the divide operation."""

    # Existing tests - KEPT AS-IS
    def test_divide_by_zero_integer(self, calculator):
        """Verify that dividing by zero with integer raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)

    def test_divide_by_zero_float(self, calculator):
        """Verify that dividing by zero with float raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0.0)

    def test_divide_by_zero_negative_numerator(self, calculator):
        """Verify that dividing negative numerator by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(-10, 0)

    def test_divide_with_invalid_inputs(self, calculator):
        """Verify that dividing with invalid inputs (None, string) raises TypeError."""
        # Test with None divisor
        with pytest.raises(TypeError):
            calculator.divide(10, None)

        # Test with string divisor (non-numeric)
        with pytest.raises(TypeError):
            calculator.divide(10, "abc")

        # Test with empty string divisor
        with pytest.raises(TypeError):
            calculator.divide(10, "")

    # New tests
    def test_divide_positive_integers_no_remainder(self, calculator):
        """Test dividing positive integers with no remainder."""
        assert calculator.divide(10, 2) == 5.0

    def test_divide_positive_integers_with_remainder(self, calculator):
        """Test dividing positive integers with remainder."""
        assert calculator.divide(10, 3) == pytest.approx(3.333333, rel=1e-5)

    def test_divide_positive_floats(self, calculator):
        """Test dividing two positive floats."""
        assert calculator.divide(10.5, 2.5) == pytest.approx(4.2)

    def test_divide_positive_by_negative(self, calculator):
        """Test dividing positive by negative."""
        assert calculator.divide(10, -2) == -5.0

    def test_divide_negative_by_positive(self, calculator):
        """Test dividing negative by positive."""
        assert calculator.divide(-10, 2) == -5.0

    def test_divide_two_negatives(self, calculator):
        """Test dividing two negative numbers."""
        assert calculator.divide(-10, -2) == 5.0

    def test_divide_zero_by_number(self, calculator):
        """Test dividing zero by a non-zero number."""
        assert calculator.divide(0, 5) == 0.0

    def test_divide_zero_by_negative(self, calculator):
        """Test dividing zero by a negative number."""
        assert calculator.divide(0, -5) == 0.0

    def test_divide_by_one(self, calculator):
        """Test dividing by one (identity operation)."""
        assert calculator.divide(5, 1) == 5.0

    def test_divide_by_negative_one(self, calculator):
        """Test dividing by negative one."""
        assert calculator.divide(5, -1) == -5.0

    def test_divide_one_by_number(self, calculator):
        """Test dividing one by a number."""
        assert calculator.divide(1, 2) == 0.5

    def test_divide_produces_large_result(self, calculator):
        """Test division that produces a large result."""
        assert calculator.divide(1e10, 1) == pytest.approx(1e10)

    def test_divide_produces_very_small_result(self, calculator):
        """Test division that produces a very small result."""
        assert calculator.divide(1, 1e10) == pytest.approx(1e-10)

    def test_divide_large_by_small(self, calculator):
        """Test dividing large number by very small number."""
        assert calculator.divide(1000, 0.001) == pytest.approx(1e6)

    def test_divide_small_by_large(self, calculator):
        """Test dividing very small number by large number."""
        assert calculator.divide(0.001, 1000) == pytest.approx(1e-6)

    def test_divide_none_numerator(self, calculator):
        """Test dividing None raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(None, 5)

    def test_divide_string_numerator(self, calculator):
        """Test dividing string as numerator raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide("10", 2)


# ============================================================================
# FACTORIAL OPERATION TESTS
# ============================================================================

class TestFactorial:
    """Test suite for the factorial operation."""

    def test_factorial_base_case_zero(self, calculator):
        """Test factorial(0) == 1."""
        assert calculator.factorial(0) == 1

    def test_factorial_base_case_one(self, calculator):
        """Test factorial(1) == 1."""
        assert calculator.factorial(1) == 1

    def test_factorial_small_positive_integers(self, calculator):
        """Test factorial for small positive integers."""
        assert calculator.factorial(2) == 2
        assert calculator.factorial(3) == 6
        assert calculator.factorial(4) == 24
        assert calculator.factorial(5) == 120

    def test_factorial_moderate_integer(self, calculator):
        """Test factorial(10) == 3628800."""
        assert calculator.factorial(10) == 3628800

    def test_factorial_large_integer(self, calculator):
        """Test factorial(20) handles large Python integers."""
        assert calculator.factorial(20) == 2432902008176640000

    def test_factorial_even_larger_integer(self, calculator):
        """Test factorial(30) to verify Python handles very large integers."""
        assert calculator.factorial(30) == 265252859812191058636308480000000

    def test_factorial_float_equal_to_integer(self, calculator):
        """Test that float values equal to integers are accepted."""
        assert calculator.factorial(5.0) == 120
        assert calculator.factorial(0.0) == 1
        assert calculator.factorial(10.0) == 3628800

    def test_factorial_negative_integer_raises_valueerror(self, calculator):
        """Test that negative integers raise ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(-1)

        with pytest.raises(ValueError):
            calculator.factorial(-5)

        with pytest.raises(ValueError):
            calculator.factorial(-100)

    def test_factorial_negative_float_raises_valueerror(self, calculator):
        """Test that negative floats equal to integers raise ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(-1.0)

        with pytest.raises(ValueError):
            calculator.factorial(-5.0)

    def test_factorial_non_integer_float_raises_typeerror(self, calculator):
        """Test that float values not equal to integers raise TypeError."""
        with pytest.raises(TypeError):
            calculator.factorial(1.5)

        with pytest.raises(TypeError):
            calculator.factorial(5.5)

        with pytest.raises(TypeError):
            calculator.factorial(0.1)

        with pytest.raises(TypeError):
            calculator.factorial(10.9)

    def test_factorial_string_raises_typeerror(self, calculator):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.factorial("5")

        with pytest.raises(TypeError):
            calculator.factorial("")

    def test_factorial_none_raises_typeerror(self, calculator):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.factorial(None)

    def test_factorial_bool_true_raises_typeerror(self, calculator):
        """Test that boolean True raises TypeError (not treated as 1)."""
        with pytest.raises(TypeError):
            calculator.factorial(True)

    def test_factorial_bool_false_raises_typeerror(self, calculator):
        """Test that boolean False raises TypeError (not treated as 0)."""
        with pytest.raises(TypeError):
            calculator.factorial(False)

    def test_factorial_list_raises_typeerror(self, calculator):
        """Test that list input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.factorial([5])

        with pytest.raises(TypeError):
            calculator.factorial([])

    def test_factorial_dict_raises_typeerror(self, calculator):
        """Test that dict input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.factorial({"n": 5})

    def test_factorial_tuple_raises_typeerror(self, calculator):
        """Test that tuple input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.factorial((5,))

    def test_factorial_set_raises_typeerror(self, calculator):
        """Test that set input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.factorial({5})

    @pytest.mark.parametrize("n,expected", [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
        (6, 720),
        (7, 5040),
        (8, 40320),
        (9, 362880),
        (10, 3628800),
    ])
    def test_factorial_parametrized_small_values(self, calculator, n, expected):
        """Parametrized test for factorials of small values."""
        assert calculator.factorial(n) == expected

    @pytest.mark.parametrize("n", [
        0.0,
        1.0,
        5.0,
        10.0,
    ])
    def test_factorial_parametrized_integer_floats(self, calculator, n):
        """Parametrized test that integer-valued floats are accepted."""
        result = calculator.factorial(n)
        assert isinstance(result, int)
        assert result > 0

    @pytest.mark.parametrize("invalid_input", [
        -1,
        -10,
        -0.5,
        1.5,
        5.5,
        "5",
        None,
        True,
        False,
        [],
        {},
        (),
    ])
    def test_factorial_invalid_inputs(self, calculator, invalid_input):
        """Parametrized test that invalid inputs raise appropriate exceptions."""
        with pytest.raises((ValueError, TypeError)):
            calculator.factorial(invalid_input)


# ============================================================================
# CROSS-OPERATION EDGE CASES (IDENTITY OPERATIONS)
# ============================================================================

class TestSquare:
    """Test suite for the square operation."""

    def test_square_positive_integer(self, calculator):
        """Test squaring a positive integer."""
        assert calculator.square(5) == 25
        assert calculator.square(10) == 100

    def test_square_positive_float(self, calculator):
        """Test squaring a positive float."""
        assert calculator.square(5.5) == pytest.approx(30.25)
        assert calculator.square(2.5) == pytest.approx(6.25)

    def test_square_negative_integer(self, calculator):
        """Test squaring a negative integer."""
        assert calculator.square(-5) == 25
        assert calculator.square(-10) == 100

    def test_square_negative_float(self, calculator):
        """Test squaring a negative float."""
        assert calculator.square(-5.5) == pytest.approx(30.25)
        assert calculator.square(-2.5) == pytest.approx(6.25)

    def test_square_zero(self, calculator):
        """Test squaring zero."""
        assert calculator.square(0) == 0
        assert calculator.square(0.0) == 0.0

    def test_square_one(self, calculator):
        """Test squaring one."""
        assert calculator.square(1) == 1
        assert calculator.square(1.0) == 1.0

    def test_square_negative_one(self, calculator):
        """Test squaring negative one."""
        assert calculator.square(-1) == 1

    def test_square_large_integer(self, calculator):
        """Test squaring a large integer."""
        assert calculator.square(1000000) == 1000000000000

    def test_square_large_float(self, calculator):
        """Test squaring a large float."""
        assert calculator.square(1e5) == pytest.approx(1e10)

    def test_square_very_small_float(self, calculator):
        """Test squaring a very small float."""
        assert calculator.square(1e-5) == pytest.approx(1e-10)

    def test_square_returns_int_for_int_input(self, calculator):
        """Test that square returns int when given int input."""
        result = calculator.square(5)
        assert isinstance(result, int)

    def test_square_returns_float_for_float_input(self, calculator):
        """Test that square returns float when given float input."""
        result = calculator.square(5.0)
        assert isinstance(result, float)

    def test_square_bool_raises_typeerror(self, calculator):
        """Test that bool input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square(True)

        with pytest.raises(TypeError):
            calculator.square(False)

    def test_square_none_raises_typeerror(self, calculator):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square(None)

    def test_square_string_raises_typeerror(self, calculator):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square("5")

        with pytest.raises(TypeError):
            calculator.square("")

    def test_square_list_raises_typeerror(self, calculator):
        """Test that list input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square([5])

    def test_square_dict_raises_typeerror(self, calculator):
        """Test that dict input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square({"x": 5})

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (1, 1),
        (2, 4),
        (3, 9),
        (4, 16),
        (5, 25),
        (10, 100),
        (-1, 1),
        (-2, 4),
        (-5, 25),
    ])
    def test_square_parametrized(self, calculator, x, expected):
        """Parametrized test for square of various integers."""
        assert calculator.square(x) == expected


# ============================================================================
# CUBE OPERATION TESTS
# ============================================================================

class TestCube:
    """Test suite for the cube operation."""

    def test_cube_positive_integer(self, calculator):
        """Test cubing a positive integer."""
        assert calculator.cube(2) == 8
        assert calculator.cube(3) == 27
        assert calculator.cube(5) == 125

    def test_cube_positive_float(self, calculator):
        """Test cubing a positive float."""
        assert calculator.cube(2.5) == pytest.approx(15.625)
        assert calculator.cube(1.5) == pytest.approx(3.375)

    def test_cube_negative_integer(self, calculator):
        """Test cubing a negative integer (result is negative)."""
        assert calculator.cube(-2) == -8
        assert calculator.cube(-3) == -27
        assert calculator.cube(-5) == -125

    def test_cube_negative_float(self, calculator):
        """Test cubing a negative float (result is negative)."""
        assert calculator.cube(-2.5) == pytest.approx(-15.625)
        assert calculator.cube(-1.5) == pytest.approx(-3.375)

    def test_cube_zero(self, calculator):
        """Test cubing zero."""
        assert calculator.cube(0) == 0
        assert calculator.cube(0.0) == 0.0

    def test_cube_one(self, calculator):
        """Test cubing one."""
        assert calculator.cube(1) == 1
        assert calculator.cube(1.0) == 1.0

    def test_cube_negative_one(self, calculator):
        """Test cubing negative one."""
        assert calculator.cube(-1) == -1

    def test_cube_large_integer(self, calculator):
        """Test cubing a large integer."""
        assert calculator.cube(1000) == 1000000000

    def test_cube_large_float(self, calculator):
        """Test cubing a large float."""
        assert calculator.cube(1e3) == pytest.approx(1e9)

    def test_cube_very_small_float(self, calculator):
        """Test cubing a very small float."""
        assert calculator.cube(1e-5) == pytest.approx(1e-15)

    def test_cube_returns_int_for_int_input(self, calculator):
        """Test that cube returns int when given int input."""
        result = calculator.cube(5)
        assert isinstance(result, int)

    def test_cube_returns_float_for_float_input(self, calculator):
        """Test that cube returns float when given float input."""
        result = calculator.cube(5.0)
        assert isinstance(result, float)

    def test_cube_bool_raises_typeerror(self, calculator):
        """Test that bool input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.cube(True)

        with pytest.raises(TypeError):
            calculator.cube(False)

    def test_cube_none_raises_typeerror(self, calculator):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.cube(None)

    def test_cube_string_raises_typeerror(self, calculator):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.cube("5")

        with pytest.raises(TypeError):
            calculator.cube("")

    def test_cube_list_raises_typeerror(self, calculator):
        """Test that list input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.cube([5])

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (1, 1),
        (2, 8),
        (3, 27),
        (4, 64),
        (5, 125),
        (-1, -1),
        (-2, -8),
        (-3, -27),
        (-5, -125),
    ])
    def test_cube_parametrized(self, calculator, x, expected):
        """Parametrized test for cube of various integers."""
        assert calculator.cube(x) == expected


# ============================================================================
# SQUARE ROOT OPERATION TESTS
# ============================================================================

class TestSquareRoot:
    """Test suite for the square root operation."""

    def test_square_root_perfect_squares(self, calculator):
        """Test square root of perfect squares."""
        assert calculator.square_root(0) == pytest.approx(0.0)
        assert calculator.square_root(1) == pytest.approx(1.0)
        assert calculator.square_root(4) == pytest.approx(2.0)
        assert calculator.square_root(9) == pytest.approx(3.0)
        assert calculator.square_root(16) == pytest.approx(4.0)
        assert calculator.square_root(25) == pytest.approx(5.0)
        assert calculator.square_root(100) == pytest.approx(10.0)

    def test_square_root_non_perfect_squares(self, calculator):
        """Test square root of non-perfect squares."""
        assert calculator.square_root(2) == pytest.approx(1.41421356, rel=1e-7)
        assert calculator.square_root(3) == pytest.approx(1.73205080, rel=1e-7)
        assert calculator.square_root(5) == pytest.approx(2.23606797, rel=1e-7)
        assert calculator.square_root(10) == pytest.approx(3.16227766, rel=1e-7)

    def test_square_root_float_input(self, calculator):
        """Test square root with float input."""
        assert calculator.square_root(2.25) == pytest.approx(1.5)
        assert calculator.square_root(6.25) == pytest.approx(2.5)

    def test_square_root_large_number(self, calculator):
        """Test square root of large numbers."""
        assert calculator.square_root(1e6) == pytest.approx(1e3)
        assert calculator.square_root(1e10) == pytest.approx(1e5)

    def test_square_root_very_small_number(self, calculator):
        """Test square root of very small positive number."""
        assert calculator.square_root(1e-4) == pytest.approx(1e-2)
        assert calculator.square_root(1e-10) == pytest.approx(1e-5)

    def test_square_root_returns_float(self, calculator):
        """Test that square root always returns float."""
        result = calculator.square_root(25)
        assert isinstance(result, float)

    def test_square_root_negative_raises_valueerror(self, calculator):
        """Test that negative input raises ValueError."""
        with pytest.raises(ValueError):
            calculator.square_root(-1)

        with pytest.raises(ValueError):
            calculator.square_root(-5)

        with pytest.raises(ValueError):
            calculator.square_root(-0.5)

    def test_square_root_bool_raises_typeerror(self, calculator):
        """Test that bool input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square_root(True)

        with pytest.raises(TypeError):
            calculator.square_root(False)

    def test_square_root_none_raises_typeerror(self, calculator):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square_root(None)

    def test_square_root_string_raises_typeerror(self, calculator):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square_root("4")

        with pytest.raises(TypeError):
            calculator.square_root("")

    def test_square_root_list_raises_typeerror(self, calculator):
        """Test that list input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square_root([4])

    @pytest.mark.parametrize("x,expected", [
        (0, 0.0),
        (1, 1.0),
        (4, 2.0),
        (9, 3.0),
        (16, 4.0),
        (25, 5.0),
        (100, 10.0),
    ])
    def test_square_root_parametrized(self, calculator, x, expected):
        """Parametrized test for square root of perfect squares."""
        assert calculator.square_root(x) == pytest.approx(expected)


# ============================================================================
# CUBE ROOT OPERATION TESTS
# ============================================================================

class TestCubeRoot:
    """Test suite for the cube root operation."""

    def test_cube_root_positive_perfect_cubes(self, calculator):
        """Test cube root of positive perfect cubes."""
        assert calculator.cube_root(0) == pytest.approx(0.0)
        assert calculator.cube_root(1) == pytest.approx(1.0)
        assert calculator.cube_root(8) == pytest.approx(2.0)
        assert calculator.cube_root(27) == pytest.approx(3.0)
        assert calculator.cube_root(64) == pytest.approx(4.0)
        assert calculator.cube_root(125) == pytest.approx(5.0)
        assert calculator.cube_root(1000) == pytest.approx(10.0)

    def test_cube_root_negative_perfect_cubes(self, calculator):
        """Test cube root of negative perfect cubes."""
        assert calculator.cube_root(-1) == pytest.approx(-1.0)
        assert calculator.cube_root(-8) == pytest.approx(-2.0)
        assert calculator.cube_root(-27) == pytest.approx(-3.0)
        assert calculator.cube_root(-64) == pytest.approx(-4.0)
        assert calculator.cube_root(-125) == pytest.approx(-5.0)

    def test_cube_root_positive_non_perfect_cubes(self, calculator):
        """Test cube root of positive non-perfect cubes."""
        assert calculator.cube_root(2) == pytest.approx(1.25992104, rel=1e-7)
        assert calculator.cube_root(3) == pytest.approx(1.44224957, rel=1e-7)
        assert calculator.cube_root(10) == pytest.approx(2.15443469, rel=1e-7)

    def test_cube_root_negative_non_perfect_cubes(self, calculator):
        """Test cube root of negative non-perfect cubes."""
        assert calculator.cube_root(-2) == pytest.approx(-1.25992104, rel=1e-7)
        assert calculator.cube_root(-3) == pytest.approx(-1.44224957, rel=1e-7)
        assert calculator.cube_root(-10) == pytest.approx(-2.15443469, rel=1e-7)

    def test_cube_root_float_input(self, calculator):
        """Test cube root with float input."""
        assert calculator.cube_root(8.0) == pytest.approx(2.0)
        assert calculator.cube_root(27.0) == pytest.approx(3.0)

    def test_cube_root_large_number(self, calculator):
        """Test cube root of large numbers."""
        assert calculator.cube_root(1e9) == pytest.approx(1e3)
        assert calculator.cube_root(1e12) == pytest.approx(1e4)

    def test_cube_root_large_negative_number(self, calculator):
        """Test cube root of large negative numbers."""
        assert calculator.cube_root(-1e9) == pytest.approx(-1e3)
        assert calculator.cube_root(-1e12) == pytest.approx(-1e4)

    def test_cube_root_very_small_number(self, calculator):
        """Test cube root of very small positive number."""
        assert calculator.cube_root(1e-6) == pytest.approx(1e-2)

    def test_cube_root_very_small_negative_number(self, calculator):
        """Test cube root of very small negative number."""
        assert calculator.cube_root(-1e-6) == pytest.approx(-1e-2)

    def test_cube_root_returns_float(self, calculator):
        """Test that cube root always returns float."""
        result = calculator.cube_root(8)
        assert isinstance(result, float)

    def test_cube_root_bool_raises_typeerror(self, calculator):
        """Test that bool input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.cube_root(True)

        with pytest.raises(TypeError):
            calculator.cube_root(False)

    def test_cube_root_none_raises_typeerror(self, calculator):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.cube_root(None)

    def test_cube_root_string_raises_typeerror(self, calculator):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.cube_root("8")

        with pytest.raises(TypeError):
            calculator.cube_root("")

    def test_cube_root_list_raises_typeerror(self, calculator):
        """Test that list input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.cube_root([8])

    @pytest.mark.parametrize("x,expected", [
        (0, 0.0),
        (1, 1.0),
        (8, 2.0),
        (27, 3.0),
        (64, 4.0),
        (125, 5.0),
        (-1, -1.0),
        (-8, -2.0),
        (-27, -3.0),
    ])
    def test_cube_root_parametrized(self, calculator, x, expected):
        """Parametrized test for cube root of perfect cubes."""
        assert calculator.cube_root(x) == pytest.approx(expected)


# ============================================================================
# POWER OPERATION TESTS
# ============================================================================

class TestPower:
    """Test suite for the power operation."""

    def test_power_positive_base_positive_exponent_int(self, calculator):
        """Test power with positive int base and positive int exponent."""
        assert calculator.power(2, 3) == pytest.approx(8.0)
        assert calculator.power(5, 2) == pytest.approx(25.0)
        assert calculator.power(10, 3) == pytest.approx(1000.0)

    def test_power_positive_base_positive_exponent_float(self, calculator):
        """Test power with positive base and positive float exponent."""
        assert calculator.power(2.0, 3.0) == pytest.approx(8.0)
        assert calculator.power(4.0, 0.5) == pytest.approx(2.0)
        assert calculator.power(27.0, 1.0 / 3.0) == pytest.approx(3.0, rel=1e-7)

    def test_power_mixed_base_and_exponent(self, calculator):
        """Test power with mixed int/float base and exponent."""
        assert calculator.power(2, 3.0) == pytest.approx(8.0)
        assert calculator.power(2.0, 3) == pytest.approx(8.0)
        assert calculator.power(4, 0.5) == pytest.approx(2.0)

    def test_power_zero_exponent(self, calculator):
        """Test power with zero exponent (should return 1.0)."""
        assert calculator.power(5, 0) == pytest.approx(1.0)
        assert calculator.power(10, 0.0) == pytest.approx(1.0)
        assert calculator.power(0, 0) == pytest.approx(1.0)
        assert calculator.power(-5, 0) == pytest.approx(1.0)

    def test_power_base_to_one(self, calculator):
        """Test any base raised to exponent 1."""
        assert calculator.power(5, 1) == pytest.approx(5.0)
        assert calculator.power(10, 1.0) == pytest.approx(10.0)
        assert calculator.power(-5, 1) == pytest.approx(-5.0)

    def test_power_one_to_any_exponent(self, calculator):
        """Test 1 raised to any exponent."""
        assert calculator.power(1, 5) == pytest.approx(1.0)
        assert calculator.power(1.0, 100) == pytest.approx(1.0)
        assert calculator.power(1, 0) == pytest.approx(1.0)

    def test_power_negative_base_positive_even_exponent(self, calculator):
        """Test negative base with even exponent (positive result)."""
        assert calculator.power(-2, 2) == pytest.approx(4.0)
        assert calculator.power(-5, 4) == pytest.approx(625.0)

    def test_power_negative_base_positive_odd_exponent(self, calculator):
        """Test negative base with odd exponent (negative result)."""
        assert calculator.power(-2, 3) == pytest.approx(-8.0)
        assert calculator.power(-5, 3) == pytest.approx(-125.0)

    def test_power_zero_base_positive_exponent(self, calculator):
        """Test zero base with positive exponent."""
        assert calculator.power(0, 1) == pytest.approx(0.0)
        assert calculator.power(0, 5) == pytest.approx(0.0)
        assert calculator.power(0.0, 10.0) == pytest.approx(0.0)

    def test_power_negative_base_fractional_exponent(self, calculator):
        """Test negative base with fractional exponent."""
        # Note: negative base with fractional exponent may produce complex numbers
        # Python's ** operator will raise ValueError for this
        # We test that the behavior is consistent
        with pytest.raises((ValueError, TypeError)):
            calculator.power(-1, 0.5)

    def test_power_large_numbers(self, calculator):
        """Test power with large results."""
        assert calculator.power(10, 6) == pytest.approx(1e6)
        assert calculator.power(2, 20) == pytest.approx(1048576.0)

    def test_power_fractional_base_large_exponent(self, calculator):
        """Test fractional base with large exponent (approaches zero)."""
        result = calculator.power(0.5, 10)
        assert result == pytest.approx(1.0 / 1024.0)

    def test_power_returns_float(self, calculator):
        """Test that power always returns float."""
        result = calculator.power(2, 3)
        assert isinstance(result, float)

    def test_power_bool_base_raises_typeerror(self, calculator):
        """Test that bool as base raises TypeError."""
        with pytest.raises(TypeError):
            calculator.power(True, 2)

        with pytest.raises(TypeError):
            calculator.power(False, 2)

    def test_power_bool_exponent_raises_typeerror(self, calculator):
        """Test that bool as exponent raises TypeError."""
        with pytest.raises(TypeError):
            calculator.power(2, True)

        with pytest.raises(TypeError):
            calculator.power(2, False)

    def test_power_none_base_raises_typeerror(self, calculator):
        """Test that None as base raises TypeError."""
        with pytest.raises(TypeError):
            calculator.power(None, 2)

    def test_power_none_exponent_raises_typeerror(self, calculator):
        """Test that None as exponent raises TypeError."""
        with pytest.raises(TypeError):
            calculator.power(2, None)

    def test_power_string_base_raises_typeerror(self, calculator):
        """Test that string as base raises TypeError."""
        with pytest.raises(TypeError):
            calculator.power("2", 3)

    def test_power_string_exponent_raises_typeerror(self, calculator):
        """Test that string as exponent raises TypeError."""
        with pytest.raises(TypeError):
            calculator.power(2, "3")

    def test_power_list_base_raises_typeerror(self, calculator):
        """Test that list as base raises TypeError."""
        with pytest.raises(TypeError):
            calculator.power([2], 3)

    def test_power_list_exponent_raises_typeerror(self, calculator):
        """Test that list as exponent raises TypeError."""
        with pytest.raises(TypeError):
            calculator.power(2, [3])

    @pytest.mark.parametrize("base,exp,expected", [
        (2, 0, 1.0),
        (2, 1, 2.0),
        (2, 3, 8.0),
        (2, 10, 1024.0),
        (5, 2, 25.0),
        (10, 3, 1000.0),
        (-2, 2, 4.0),
        (-2, 3, -8.0),
        (0, 1, 0.0),
        (1, 100, 1.0),
    ])
    def test_power_parametrized(self, calculator, base, exp, expected):
        """Parametrized test for various power operations."""
        assert calculator.power(base, exp) == pytest.approx(expected)


# ============================================================================
# LOG10 OPERATION TESTS
# ============================================================================

class TestLog10:
    """Test suite for the base-10 logarithm operation."""

    def test_log10_one(self, calculator):
        """Test log10(1) == 0."""
        assert calculator.log10(1) == pytest.approx(0.0)
        assert calculator.log10(1.0) == pytest.approx(0.0)

    def test_log10_ten(self, calculator):
        """Test log10(10) == 1."""
        assert calculator.log10(10) == pytest.approx(1.0)
        assert calculator.log10(10.0) == pytest.approx(1.0)

    def test_log10_hundred(self, calculator):
        """Test log10(100) == 2."""
        assert calculator.log10(100) == pytest.approx(2.0)
        assert calculator.log10(100.0) == pytest.approx(2.0)

    def test_log10_thousand(self, calculator):
        """Test log10(1000) == 3."""
        assert calculator.log10(1000) == pytest.approx(3.0)

    def test_log10_tenth(self, calculator):
        """Test log10(0.1) == -1."""
        assert calculator.log10(0.1) == pytest.approx(-1.0)

    def test_log10_hundredth(self, calculator):
        """Test log10(0.01) == -2."""
        assert calculator.log10(0.01) == pytest.approx(-2.0)

    def test_log10_arbitrary_positive_numbers(self, calculator):
        """Test log10 for arbitrary positive numbers."""
        assert calculator.log10(2) == pytest.approx(0.30102999566, rel=1e-7)
        assert calculator.log10(5) == pytest.approx(0.69897000433, rel=1e-7)
        assert calculator.log10(100.5) == pytest.approx(2.00216606642, rel=1e-7)

    def test_log10_large_positive_number(self, calculator):
        """Test log10 of large positive numbers."""
        assert calculator.log10(1e10) == pytest.approx(10.0)
        assert calculator.log10(1e20) == pytest.approx(20.0)

    def test_log10_very_small_positive_number(self, calculator):
        """Test log10 of very small positive numbers."""
        assert calculator.log10(1e-5) == pytest.approx(-5.0)
        assert calculator.log10(1e-10) == pytest.approx(-10.0)

    def test_log10_returns_float(self, calculator):
        """Test that log10 always returns float."""
        result = calculator.log10(10)
        assert isinstance(result, float)

    def test_log10_zero_raises_valueerror(self, calculator):
        """Test that log10(0) raises ValueError."""
        with pytest.raises(ValueError):
            calculator.log10(0)

        with pytest.raises(ValueError):
            calculator.log10(0.0)

    def test_log10_negative_raises_valueerror(self, calculator):
        """Test that log10 of negative numbers raises ValueError."""
        with pytest.raises(ValueError):
            calculator.log10(-1)

        with pytest.raises(ValueError):
            calculator.log10(-10)

        with pytest.raises(ValueError):
            calculator.log10(-0.5)

    def test_log10_bool_raises_typeerror(self, calculator):
        """Test that bool input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.log10(True)

        with pytest.raises(TypeError):
            calculator.log10(False)

    def test_log10_none_raises_typeerror(self, calculator):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.log10(None)

    def test_log10_string_raises_typeerror(self, calculator):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.log10("10")

        with pytest.raises(TypeError):
            calculator.log10("")

    def test_log10_list_raises_typeerror(self, calculator):
        """Test that list input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.log10([10])

    @pytest.mark.parametrize("x,expected", [
        (1, 0.0),
        (10, 1.0),
        (100, 2.0),
        (1000, 3.0),
        (0.1, -1.0),
        (0.01, -2.0),
    ])
    def test_log10_parametrized(self, calculator, x, expected):
        """Parametrized test for log10 of specific values."""
        assert calculator.log10(x) == pytest.approx(expected)


# ============================================================================
# NATURAL LOG OPERATION TESTS
# ============================================================================

class TestNaturalLog:
    """Test suite for the natural logarithm (base e) operation."""

    def test_natural_log_one(self, calculator):
        """Test ln(1) == 0."""
        assert calculator.natural_log(1) == pytest.approx(0.0)
        assert calculator.natural_log(1.0) == pytest.approx(0.0)

    def test_natural_log_e(self, calculator):
        """Test ln(e) == 1."""
        assert calculator.natural_log(math.e) == pytest.approx(1.0)

    def test_natural_log_e_squared(self, calculator):
        """Test ln(e^2) == 2."""
        assert calculator.natural_log(math.e ** 2) == pytest.approx(2.0)

    def test_natural_log_sqrt_e(self, calculator):
        """Test ln(sqrt(e)) == 0.5."""
        assert calculator.natural_log(math.sqrt(math.e)) == pytest.approx(0.5, rel=1e-7)

    def test_natural_log_one_over_e(self, calculator):
        """Test ln(1/e) == -1."""
        assert calculator.natural_log(1.0 / math.e) == pytest.approx(-1.0, rel=1e-7)

    def test_natural_log_arbitrary_positive_numbers(self, calculator):
        """Test natural log for arbitrary positive numbers."""
        assert calculator.natural_log(2) == pytest.approx(0.69314718055, rel=1e-7)
        assert calculator.natural_log(10) == pytest.approx(2.30258509299, rel=1e-7)

    def test_natural_log_large_positive_number(self, calculator):
        """Test natural log of large positive numbers."""
        assert calculator.natural_log(1e5) == pytest.approx(11.51292546497, rel=1e-7)

    def test_natural_log_very_small_positive_number(self, calculator):
        """Test natural log of very small positive numbers."""
        assert calculator.natural_log(1e-5) == pytest.approx(-11.51292546497, rel=1e-7)

    def test_natural_log_returns_float(self, calculator):
        """Test that natural log always returns float."""
        result = calculator.natural_log(10)
        assert isinstance(result, float)

    def test_natural_log_zero_raises_valueerror(self, calculator):
        """Test that ln(0) raises ValueError."""
        with pytest.raises(ValueError):
            calculator.natural_log(0)

        with pytest.raises(ValueError):
            calculator.natural_log(0.0)

    def test_natural_log_negative_raises_valueerror(self, calculator):
        """Test that natural log of negative numbers raises ValueError."""
        with pytest.raises(ValueError):
            calculator.natural_log(-1)

        with pytest.raises(ValueError):
            calculator.natural_log(-10)

        with pytest.raises(ValueError):
            calculator.natural_log(-0.5)

    def test_natural_log_bool_raises_typeerror(self, calculator):
        """Test that bool input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.natural_log(True)

        with pytest.raises(TypeError):
            calculator.natural_log(False)

    def test_natural_log_none_raises_typeerror(self, calculator):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.natural_log(None)

    def test_natural_log_string_raises_typeerror(self, calculator):
        """Test that string input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.natural_log("10")

        with pytest.raises(TypeError):
            calculator.natural_log("")

    def test_natural_log_list_raises_typeerror(self, calculator):
        """Test that list input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.natural_log([10])

    @pytest.mark.parametrize("x,expected", [
        (1, 0.0),
        (math.e, 1.0),
    ])
    def test_natural_log_parametrized_special_values(self, calculator, x, expected):
        """Parametrized test for natural log of special values."""
        assert calculator.natural_log(x) == pytest.approx(expected, rel=1e-7)


# ============================================================================
# CROSS-OPERATION EDGE CASES (IDENTITY OPERATIONS)
# ============================================================================

class TestCrossOperationEdgeCases:
    """Test suite for identity operations and cross-operation edge cases."""

    def test_add_zero_identity(self, calculator):
        """Test that adding zero is identity operation."""
        values = [0, 1, -1, 100, -100, 0.5, -0.5, 1e10, 1e-10]
        for val in values:
            assert calculator.add(val, 0) == val
            assert calculator.add(0, val) == val

    def test_subtract_zero_identity(self, calculator):
        """Test that subtracting zero is identity operation."""
        values = [0, 1, -1, 100, -100, 0.5, -0.5, 1e10, 1e-10]
        for val in values:
            assert calculator.subtract(val, 0) == val

    def test_multiply_one_identity(self, calculator):
        """Test that multiplying by one is identity operation."""
        values = [0, 1, -1, 100, -100, 0.5, -0.5, 1e10, 1e-10]
        for val in values:
            assert calculator.multiply(val, 1) == val
            assert calculator.multiply(1, val) == val

    def test_divide_one_identity(self, calculator):
        """Test that dividing by one is identity operation."""
        values = [1, -1, 100, -100, 0.5, -0.5, 1e10, 1e-10]
        for val in values:
            assert calculator.divide(val, 1) == val

    def test_commutative_add(self, calculator):
        """Test that addition is commutative."""
        pairs = [(5, 3), (10, -5), (-3, -7), (0, 0), (1.5, 2.5)]
        for a, b in pairs:
            assert calculator.add(a, b) == calculator.add(b, a)

    def test_commutative_multiply(self, calculator):
        """Test that multiplication is commutative."""
        pairs = [(5, 3), (10, -5), (-3, -7), (0, 0), (1.5, 2.5)]
        for a, b in pairs:
            assert calculator.multiply(a, b) == calculator.multiply(b, a)

    def test_associative_add(self, calculator):
        """Test that addition is associative: (a + b) + c = a + (b + c)."""
        a, b, c = 5, 3, 2
        left = calculator.add(calculator.add(a, b), c)
        right = calculator.add(a, calculator.add(b, c))
        assert left == right

    def test_associative_multiply(self, calculator):
        """Test that multiplication is associative: (a * b) * c = a * (b * c)."""
        a, b, c = 5, 3, 2
        left = calculator.multiply(calculator.multiply(a, b), c)
        right = calculator.multiply(a, calculator.multiply(b, c))
        assert left == right

    def test_distributive_property(self, calculator):
        """Test distributive property: a * (b + c) = (a * b) + (a * c)."""
        a, b, c = 5, 3, 2
        left = calculator.multiply(a, calculator.add(b, c))
        right = calculator.add(calculator.multiply(a, b), calculator.multiply(a, c))
        assert left == right


# ============================================================================
# CALCULATOR HISTORY INTEGRATION TESTS
# ============================================================================

class TestCalculatorHistory:
    """Test suite for calculator history tracking integration."""

    def test_calculator_initializes_with_empty_history(self, calculator):
        """Test that a new calculator has empty history."""
        assert len(calculator.get_history()) == 0

    def test_add_operation_recorded_in_history(self, calculator):
        """Test that add operation is recorded in history."""
        calculator.add(5, 3)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "add"
        assert record.operands == [5, 3]
        assert record.result == 8

    def test_subtract_operation_recorded_in_history(self, calculator):
        """Test that subtract operation is recorded in history."""
        calculator.subtract(10, 3)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "subtract"
        assert record.operands == [10, 3]
        assert record.result == 7

    def test_multiply_operation_recorded_in_history(self, calculator):
        """Test that multiply operation is recorded in history."""
        calculator.multiply(6, 7)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "multiply"
        assert record.operands == [6, 7]
        assert record.result == 42

    def test_divide_operation_recorded_in_history(self, calculator):
        """Test that divide operation is recorded in history."""
        calculator.divide(10, 2)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "divide"
        assert record.operands == [10, 2]
        assert record.result == 5.0

    def test_factorial_operation_recorded_in_history(self, calculator):
        """Test that factorial operation is recorded in history."""
        calculator.factorial(5)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "factorial"
        assert record.operands == [5]
        assert record.result == 120

    def test_square_operation_recorded_in_history(self, calculator):
        """Test that square operation is recorded in history."""
        calculator.square(7)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "square"
        assert record.operands == [7]
        assert record.result == 49

    def test_cube_operation_recorded_in_history(self, calculator):
        """Test that cube operation is recorded in history."""
        calculator.cube(3)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "cube"
        assert record.operands == [3]
        assert record.result == 27

    def test_square_root_operation_recorded_in_history(self, calculator):
        """Test that square_root operation is recorded in history."""
        calculator.square_root(25)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "square_root"
        assert record.operands == [25]
        assert record.result == pytest.approx(5.0)

    def test_cube_root_operation_recorded_in_history(self, calculator):
        """Test that cube_root operation is recorded in history."""
        calculator.cube_root(8)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "cube_root"
        assert record.operands == [8]
        assert record.result == pytest.approx(2.0)

    def test_power_operation_recorded_in_history(self, calculator):
        """Test that power operation is recorded in history."""
        calculator.power(2, 5)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "power"
        assert record.operands == [2, 5]
        assert record.result == pytest.approx(32.0)

    def test_log10_operation_recorded_in_history(self, calculator):
        """Test that log10 operation is recorded in history."""
        calculator.log10(100)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "log10"
        assert record.operands == [100]
        assert record.result == pytest.approx(2.0)

    def test_natural_log_operation_recorded_in_history(self, calculator):
        """Test that natural_log operation is recorded in history."""
        calculator.natural_log(math.e)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "natural_log"
        assert record.operands == [math.e]
        assert record.result == pytest.approx(1.0)

    def test_history_contains_correct_timestamp(self, calculator):
        """Test that history records contain a datetime timestamp."""
        before = datetime.now()
        calculator.add(5, 3)
        after = datetime.now()

        history = calculator.get_history()
        record = history[0]

        assert isinstance(record.timestamp, datetime)
        assert before <= record.timestamp <= after

    def test_history_persists_across_multiple_operations(self, calculator):
        """Test that history persists across multiple operations."""
        calculator.add(5, 3)
        calculator.multiply(4, 2)
        calculator.subtract(10, 3)

        history = calculator.get_history()
        assert len(history) == 3
        assert history[0].operation_name == "add"
        assert history[1].operation_name == "multiply"
        assert history[2].operation_name == "subtract"

    def test_history_operations_recorded_in_order(self, calculator):
        """Test that operations are recorded in the order they were called."""
        operations = [
            ("add", lambda: calculator.add(1, 2)),
            ("subtract", lambda: calculator.subtract(5, 2)),
            ("multiply", lambda: calculator.multiply(3, 4)),
            ("divide", lambda: calculator.divide(10, 2)),
            ("factorial", lambda: calculator.factorial(4)),
        ]

        for op_name, op_func in operations:
            op_func()

        history = calculator.get_history()
        recorded_names = [r.operation_name for r in history]
        expected_names = [op[0] for op in operations]

        assert recorded_names == expected_names

    def test_get_history_returns_copy(self, calculator):
        """Test that get_history returns a copy, not internal reference."""
        calculator.add(5, 3)
        hist1 = calculator.get_history()
        hist1.clear()

        hist2 = calculator.get_history()
        assert len(hist2) == 1

    def test_clear_history_removes_all_records(self, calculator):
        """Test that clear_history removes all recorded operations."""
        calculator.add(5, 3)
        calculator.multiply(4, 2)
        assert len(calculator.get_history()) == 2

        calculator.clear_history()
        assert len(calculator.get_history()) == 0

    def test_divide_by_zero_does_not_record_history(self, calculator):
        """Test that division by zero error does not record to history."""
        try:
            calculator.divide(10, 0)
        except ZeroDivisionError:
            pass

        history = calculator.get_history()
        assert len(history) == 0

    def test_square_root_negative_does_not_record_history(self, calculator):
        """Test that square_root of negative does not record to history."""
        try:
            calculator.square_root(-1)
        except ValueError:
            pass

        history = calculator.get_history()
        assert len(history) == 0

    def test_factorial_negative_does_not_record_history(self, calculator):
        """Test that factorial of negative does not record to history."""
        try:
            calculator.factorial(-5)
        except ValueError:
            pass

        history = calculator.get_history()
        assert len(history) == 0

    def test_factorial_invalid_type_does_not_record_history(self, calculator):
        """Test that factorial with invalid type does not record to history."""
        try:
            calculator.factorial("5")
        except TypeError:
            pass

        history = calculator.get_history()
        assert len(history) == 0

    def test_log10_zero_does_not_record_history(self, calculator):
        """Test that log10(0) does not record to history."""
        try:
            calculator.log10(0)
        except ValueError:
            pass

        history = calculator.get_history()
        assert len(history) == 0

    def test_log10_negative_does_not_record_history(self, calculator):
        """Test that log10 of negative does not record to history."""
        try:
            calculator.log10(-5)
        except ValueError:
            pass

        history = calculator.get_history()
        assert len(history) == 0

    def test_natural_log_zero_does_not_record_history(self, calculator):
        """Test that natural_log(0) does not record to history."""
        try:
            calculator.natural_log(0)
        except ValueError:
            pass

        history = calculator.get_history()
        assert len(history) == 0

    def test_natural_log_negative_does_not_record_history(self, calculator):
        """Test that natural_log of negative does not record to history."""
        try:
            calculator.natural_log(-5)
        except ValueError:
            pass

        history = calculator.get_history()
        assert len(history) == 0

    def test_square_invalid_type_does_not_record_history(self, calculator):
        """Test that square with invalid type does not record to history."""
        try:
            calculator.square(True)
        except TypeError:
            pass

        history = calculator.get_history()
        assert len(history) == 0

    def test_cube_invalid_type_does_not_record_history(self, calculator):
        """Test that cube with invalid type does not record to history."""
        try:
            calculator.cube(None)
        except TypeError:
            pass

        history = calculator.get_history()
        assert len(history) == 0

    def test_power_invalid_base_does_not_record_history(self, calculator):
        """Test that power with invalid base does not record to history."""
        try:
            calculator.power(True, 2)
        except TypeError:
            pass

        history = calculator.get_history()
        assert len(history) == 0

    def test_power_invalid_exponent_does_not_record_history(self, calculator):
        """Test that power with invalid exponent does not record to history."""
        try:
            calculator.power(2, None)
        except TypeError:
            pass

        history = calculator.get_history()
        assert len(history) == 0

    def test_history_with_float_operands_and_results(self, calculator):
        """Test that float operands and results are correctly recorded."""
        calculator.divide(7.5, 2.5)
        history = calculator.get_history()

        record = history[0]
        assert record.operands == [7.5, 2.5]
        assert record.result == pytest.approx(3.0)

    def test_history_with_negative_operands(self, calculator):
        """Test that negative operands are correctly recorded."""
        calculator.add(-5, -3)
        history = calculator.get_history()

        record = history[0]
        assert record.operands == [-5, -3]
        assert record.result == -8

    def test_history_with_zero_operand(self, calculator):
        """Test that zero operands are correctly recorded."""
        calculator.multiply(0, 5)
        history = calculator.get_history()

        record = history[0]
        assert record.operands == [0, 5]
        assert record.result == 0

    def test_mixed_operations_with_failures_and_successes(self, calculator):
        """Test history with a mix of successful and failed operations."""
        calculator.add(5, 3)

        try:
            calculator.divide(10, 0)
        except ZeroDivisionError:
            pass

        calculator.multiply(4, 2)

        history = calculator.get_history()
        assert len(history) == 2
        assert history[0].operation_name == "add"
        assert history[1].operation_name == "multiply"

    def test_get_history_returns_operation_record_instances(self, calculator):
        """Test that get_history returns OperationRecord instances."""
        calculator.add(5, 3)
        history = calculator.get_history()

        assert len(history) == 1
        assert isinstance(history[0], OperationRecord)

    def test_clear_history_followed_by_new_operations(self, calculator):
        """Test that history works correctly after clearing."""
        calculator.add(5, 3)
        calculator.clear_history()

        calculator.multiply(4, 2)
        history = calculator.get_history()

        assert len(history) == 1
        assert history[0].operation_name == "multiply"

    def test_history_with_large_numbers(self, calculator):
        """Test history with very large numbers."""
        large_num = 1e100
        calculator.add(large_num, large_num)

        history = calculator.get_history()
        record = history[0]
        assert record.operands[0] == large_num
        assert record.result == pytest.approx(2 * large_num)

    def test_history_with_very_small_numbers(self, calculator):
        """Test history with very small numbers."""
        small_num = 1e-100
        calculator.add(small_num, small_num)

        history = calculator.get_history()
        record = history[0]
        assert record.operands[0] == pytest.approx(small_num)
        assert record.result == pytest.approx(2 * small_num)

    def test_history_records_unary_operations_with_single_operand(self, calculator):
        """Test that unary operations are recorded with single operand in list."""
        calculator.square(5)
        calculator.factorial(4)

        history = calculator.get_history()
        assert len(history[0].operands) == 1
        assert len(history[1].operands) == 1

    def test_history_records_binary_operations_with_two_operands(self, calculator):
        """Test that binary operations are recorded with two operands in list."""
        calculator.add(5, 3)
        calculator.power(2, 8)

        history = calculator.get_history()
        assert len(history[0].operands) == 2
        assert len(history[1].operands) == 2

    def test_multiple_calculators_have_independent_history(self):
        """Test that multiple calculator instances have independent histories."""
        calc1 = Calculator()
        calc2 = Calculator()

        calc1.add(5, 3)
        calc2.multiply(4, 2)

        hist1 = calc1.get_history()
        hist2 = calc2.get_history()

        assert len(hist1) == 1
        assert len(hist2) == 1
        assert hist1[0].operation_name == "add"
        assert hist2[0].operation_name == "multiply"

    def test_timestamps_increase_for_consecutive_operations(self, calculator):
        """Test that timestamps generally increase for consecutive operations."""
        calculator.add(5, 3)
        calculator.multiply(4, 2)
        calculator.subtract(10, 3)

        history = calculator.get_history()
        ts1 = history[0].timestamp
        ts2 = history[1].timestamp
        ts3 = history[2].timestamp

        # Timestamps should be in chronological order
        # Note: very fast execution might result in same microsecond
        assert ts1 <= ts2 <= ts3


# ============================================================================
# ERROR LOGGING TESTS
# ============================================================================

class TestCalculatorErrorLogging:
    """Test suite for error logging in Calculator methods."""

    def test_divide_by_zero_error_is_logged(self, calculator, caplog):
        """Verify that ZeroDivisionError in divide() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ZeroDivisionError):
                calculator.divide(10, 0)

        assert any("divide" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_factorial_negative_value_error_is_logged(self, calculator, caplog):
        """Verify that ValueError in factorial() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                calculator.factorial(-5)

        assert any("factorial" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_factorial_bool_type_error_is_logged(self, calculator, caplog):
        """Verify that TypeError for bool in factorial() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.factorial(True)

        assert any("factorial" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_factorial_non_integer_float_type_error_is_logged(self, calculator, caplog):
        """Verify that TypeError for non-integer float in factorial() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.factorial(5.5)

        assert any("factorial" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_factorial_string_type_error_is_logged(self, calculator, caplog):
        """Verify that TypeError for string in factorial() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.factorial("5")

        assert any("factorial" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_square_bool_type_error_is_logged(self, calculator, caplog):
        """Verify that TypeError for bool in square() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.square(True)

        assert any("square" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_square_string_type_error_is_logged(self, calculator, caplog):
        """Verify that TypeError for string in square() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.square("5")

        assert any("square" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_cube_bool_type_error_is_logged(self, calculator, caplog):
        """Verify that TypeError for bool in cube() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.cube(False)

        assert any("cube" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_cube_none_type_error_is_logged(self, calculator, caplog):
        """Verify that TypeError for None in cube() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.cube(None)

        assert any("cube" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_square_root_negative_value_error_is_logged(self, calculator, caplog):
        """Verify that ValueError in square_root() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                calculator.square_root(-1)

        assert any("square_root" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_square_root_bool_type_error_is_logged(self, calculator, caplog):
        """Verify that TypeError for bool in square_root() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.square_root(True)

        assert any("square_root" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_cube_root_bool_type_error_is_logged(self, calculator, caplog):
        """Verify that TypeError for bool in cube_root() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.cube_root(False)

        assert any("cube_root" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_power_bool_base_type_error_is_logged(self, calculator, caplog):
        """Verify that TypeError for bool base in power() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.power(True, 2)

        assert any("power" in record.message.lower() for record in caplog.records)
        assert any("base" in record.message.lower() for record in caplog.records)

    def test_power_bool_exponent_type_error_is_logged(self, calculator, caplog):
        """Verify that TypeError for bool exponent in power() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.power(2, False)

        assert any("power" in record.message.lower() for record in caplog.records)
        assert any("exponent" in record.message.lower() for record in caplog.records)

    def test_log10_zero_value_error_is_logged(self, calculator, caplog):
        """Verify that ValueError for log10(0) is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                calculator.log10(0)

        assert any("log10" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_log10_negative_value_error_is_logged(self, calculator, caplog):
        """Verify that ValueError for negative in log10() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                calculator.log10(-5)

        assert any("log10" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_log10_bool_type_error_is_logged(self, calculator, caplog):
        """Verify that TypeError for bool in log10() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.log10(True)

        assert any("log10" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_natural_log_zero_value_error_is_logged(self, calculator, caplog):
        """Verify that ValueError for natural_log(0) is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                calculator.natural_log(0)

        assert any("natural_log" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_natural_log_negative_value_error_is_logged(self, calculator, caplog):
        """Verify that ValueError for negative in natural_log() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                calculator.natural_log(-5)

        assert any("natural_log" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_natural_log_bool_type_error_is_logged(self, calculator, caplog):
        """Verify that TypeError for bool in natural_log() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.natural_log(True)

        assert any("natural_log" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)