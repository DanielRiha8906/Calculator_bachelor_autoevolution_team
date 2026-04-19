import pytest
import math
from src.calculator import Calculator


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