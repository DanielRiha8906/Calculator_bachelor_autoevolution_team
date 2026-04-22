import pytest
import math
from src import Calculator


@pytest.fixture
def calculator():
    """Fixture providing a fresh Calculator instance for tests."""
    return Calculator()


class TestDivision:
    """Tests for the divide method with valid and invalid inputs."""

    def test_divide_positive_numbers(self, calculator):
        """Test division with positive integers."""
        assert calculator.divide(10, 2) == 5

    def test_divide_with_floats(self, calculator):
        """Test division with floating point numbers."""
        assert calculator.divide(7.5, 2.5) == 3.0

    def test_divide_negative_numbers(self, calculator):
        """Test division with negative numbers."""
        assert calculator.divide(-10, 2) == -5
        assert calculator.divide(10, -2) == -5

    def test_divide_by_zero_raises_exception(self, calculator):
        """Test that division by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)

    def test_divide_zero_by_nonzero(self, calculator):
        """Test dividing zero by a nonzero number returns zero."""
        assert calculator.divide(0, 5) == 0

    @pytest.mark.parametrize("invalid_a,invalid_b", [
        ("10", 2),       # string as dividend
        (10, "2"),       # string as divisor
        (None, 5),       # None as dividend
        (5, None),       # None as divisor
        ([10], 2),       # list as dividend
        (10, [2]),       # list as divisor
    ])
    def test_divide_non_numeric_inputs_raise_typeerror(self, calculator, invalid_a, invalid_b):
        """Test that non-numeric inputs (string, None, list) raise TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(invalid_a, invalid_b)

    def test_divide_result_precision(self, calculator):
        """Test division result with expected precision."""
        result = calculator.divide(10, 3)
        assert abs(result - 3.333333333333333) < 1e-10

    def test_divide_large_numbers(self, calculator):
        """Test division with very large numbers."""
        assert calculator.divide(10**15, 10**10) == 10**5

    def test_divide_very_small_numbers(self, calculator):
        """Test division with very small numbers."""
        result = calculator.divide(1e-10, 1e-5)
        assert abs(result - 1e-5) < 1e-15


class TestAddition:
    """Tests for the add method with various inputs."""

    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 5),
        (0, 5, 5),
        (5, 0, 5),
        (0, 0, 0),
        (-2, 3, 1),
        (3, -2, 1),
        (-2, -3, -5),
        (1.5, 2.5, 4.0),
        (0.1, 0.2, pytest.approx(0.3)),
        (10**15, 1, 10**15 + 1),
        (1e-10, 1e-10, pytest.approx(2e-10)),
    ])
    def test_add_various_numbers(self, calculator, a, b, expected):
        """Test addition with positive, negative, zero, and floating point numbers."""
        assert calculator.add(a, b) == expected

    @pytest.mark.parametrize("invalid_a,invalid_b", [
        ("10", 2),
        (10, "2"),
        (None, 5),
        (5, None),
        ([10], 2),
        (10, [2]),
        ({}, 5),
        (5, {}),
    ])
    def test_add_non_numeric_inputs_raise_typeerror(self, calculator, invalid_a, invalid_b):
        """Test that non-numeric inputs raise TypeError."""
        with pytest.raises(TypeError):
            calculator.add(invalid_a, invalid_b)


class TestSubtraction:
    """Tests for the subtract method with various inputs."""

    @pytest.mark.parametrize("a,b,expected", [
        (5, 2, 3),
        (2, 5, -3),
        (5, 0, 5),
        (0, 5, -5),
        (0, 0, 0),
        (-2, 3, -5),
        (3, -2, 5),
        (-2, -3, 1),
        (2.5, 1.5, 1.0),
        (0.3, 0.1, pytest.approx(0.2)),
        (10**15, 1, 10**15 - 1),
        (1e-10, 1e-10, pytest.approx(0, abs=1e-15)),
    ])
    def test_subtract_various_numbers(self, calculator, a, b, expected):
        """Test subtraction with positive, negative, zero, and floating point numbers."""
        assert calculator.subtract(a, b) == expected

    @pytest.mark.parametrize("invalid_a,invalid_b", [
        ("5", 2),
        (5, "2"),
        (None, 5),
        (5, None),
        ([5], 2),
        (5, [2]),
        ({}, 5),
        (5, {}),
    ])
    def test_subtract_non_numeric_inputs_raise_typeerror(self, calculator, invalid_a, invalid_b):
        """Test that non-numeric inputs raise TypeError."""
        with pytest.raises(TypeError):
            calculator.subtract(invalid_a, invalid_b)


class TestMultiplication:
    """Tests for the multiply method with various inputs."""

    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 6),
        (5, 0, 0),
        (0, 5, 0),
        (0, 0, 0),
        (-2, 3, -6),
        (3, -2, -6),
        (-2, -3, 6),
        (2.5, 2, 5.0),
        (1.5, 2.5, pytest.approx(3.75)),
        (10**10, 10**10, 10**20),
        (1e-10, 1e5, pytest.approx(1e-5)),
    ])
    def test_multiply_various_numbers(self, calculator, a, b, expected):
        """Test multiplication with positive, negative, zero, and floating point numbers."""
        assert calculator.multiply(a, b) == expected

    @pytest.mark.parametrize("invalid_a,invalid_b", [
        (None, 5),
        (5, None),
        ({}, 5),
        (5, {}),
    ])
    def test_multiply_non_numeric_inputs_raise_typeerror(self, calculator, invalid_a, invalid_b):
        """Test that unsupported types (None, dict) raise TypeError."""
        with pytest.raises(TypeError):
            calculator.multiply(invalid_a, invalid_b)

    @pytest.mark.parametrize("a,b,expected", [
        ("2", 3, "222"),
        ([2], 3, [2, 2, 2]),
    ])
    def test_multiply_with_strings_and_lists(self, calculator, a, b, expected):
        """Test that multiply with strings/lists works due to Python's * operator behavior."""
        assert calculator.multiply(a, b) == expected