import pytest
from src.calculator import Calculator


class TestFactorial:
    """Test suite for Calculator.factorial() method."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance for each test."""
        return Calculator()

    # Happy Path Tests
    @pytest.mark.parametrize("n,expected", [
        (0, 1),
        (1, 1),
        (2, 2),
        (5, 120),
        (10, 3628800),
        (20, 2432902008176640000),
    ])
    def test_factorial_valid_inputs(self, calculator, n, expected):
        """Test factorial computation for valid non-negative integers."""
        result = calculator.factorial(n)
        assert result == expected

    # Edge Cases: Negative Integer Rejection
    @pytest.mark.parametrize("n", [-1, -5, -100])
    def test_factorial_negative_integer_raises_value_error(self, calculator, n):
        """Test factorial with negative integer raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(n)

    # Edge Cases: Type Rejection - Float
    @pytest.mark.parametrize("n", [1.0, 5.0])
    def test_factorial_float_raises_type_error(self, calculator, n):
        """Test factorial with float input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.factorial(n)

    # Edge Cases: Type Rejection - String
    @pytest.mark.parametrize("n", ["5", "hello"])
    def test_factorial_string_raises_type_error(self, calculator, n):
        """Test factorial with string input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.factorial(n)

    # Edge Cases: Type Rejection - None
    def test_factorial_none_raises_type_error(self, calculator):
        """Test factorial with None input raises TypeError."""
        with pytest.raises(TypeError):
            calculator.factorial(None)

    # Edge Cases: Type Rejection - Boolean
    @pytest.mark.parametrize("n", [True, False])
    def test_factorial_bool_raises_type_error(self, calculator, n):
        """Test factorial with boolean input raises TypeError (bool is subclass of int)."""
        with pytest.raises(TypeError):
            calculator.factorial(n)

    # Edge Cases: Type Rejection - Collections
    @pytest.mark.parametrize("n", [[], {}, (5,)])
    def test_factorial_collection_raises_type_error(self, calculator, n):
        """Test factorial with collection types (list, dict, tuple) raises TypeError."""
        with pytest.raises(TypeError):
            calculator.factorial(n)
