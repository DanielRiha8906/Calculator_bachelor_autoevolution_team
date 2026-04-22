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
        (3, 6),
        (4, 24),
        (5, 120),
        (10, 3628800),
    ])
    def test_factorial_non_negative_integers(self, calculator, n, expected):
        """Test factorial of non-negative integers returns correct result."""
        result = calculator.factorial(n)
        assert result == expected

    def test_factorial_zero(self, calculator):
        """Test factorial of 0 returns 1."""
        result = calculator.factorial(0)
        assert result == 1

    def test_factorial_one(self, calculator):
        """Test factorial of 1 returns 1."""
        result = calculator.factorial(1)
        assert result == 1

    # Edge Cases: Negative Integers
    @pytest.mark.parametrize("n", [-1, -5, -100])
    def test_factorial_negative_integers(self, calculator, n):
        """Test factorial of negative integers raises ValueError."""
        with pytest.raises(ValueError, match="factorial\\(\\) not defined for negative values"):
            calculator.factorial(n)

    # Edge Cases: Non-Integer Types - TypeError
    @pytest.mark.parametrize("invalid_input", [5.0, 3.5, 0.0])
    def test_factorial_float_arguments(self, calculator, invalid_input):
        """Test factorial with float arguments raises TypeError."""
        with pytest.raises(TypeError, match=r"factorial\(\) argument must be an integer, not float"):
            calculator.factorial(invalid_input)

    @pytest.mark.parametrize("invalid_input", ["5", "factorial", ""])
    def test_factorial_string_arguments(self, calculator, invalid_input):
        """Test factorial with string arguments raises TypeError."""
        with pytest.raises(TypeError, match=r"factorial\(\) argument must be an integer, not str"):
            calculator.factorial(invalid_input)

    def test_factorial_none_argument(self, calculator):
        """Test factorial with None argument raises TypeError."""
        with pytest.raises(TypeError, match=r"factorial\(\) argument must be an integer, not NoneType"):
            calculator.factorial(None)

    def test_factorial_list_argument(self, calculator):
        """Test factorial with list argument raises TypeError."""
        with pytest.raises(TypeError, match=r"factorial\(\) argument must be an integer, not list"):
            calculator.factorial([])

    def test_factorial_dict_argument(self, calculator):
        """Test factorial with dict argument raises TypeError."""
        with pytest.raises(TypeError, match=r"factorial\(\) argument must be an integer, not dict"):
            calculator.factorial({})

    def test_factorial_tuple_argument(self, calculator):
        """Test factorial with tuple argument raises TypeError."""
        with pytest.raises(TypeError, match=r"factorial\(\) argument must be an integer, not tuple"):
            calculator.factorial((1, 2))

    # Edge Cases: Boolean (subclass of int) - must be rejected
    @pytest.mark.parametrize("invalid_bool", [True, False])
    def test_factorial_bool_arguments(self, calculator, invalid_bool):
        """Test factorial with bool arguments raises TypeError (bool is subclass of int, must be rejected)."""
        with pytest.raises(TypeError, match=r"factorial\(\) argument must be an integer, not bool"):
            calculator.factorial(invalid_bool)

    # Edge Cases: Large integers
    def test_factorial_large_integer(self, calculator):
        """Test factorial with a large integer (20)."""
        result = calculator.factorial(20)
        assert result == 2432902008176640000

    def test_factorial_very_large_integer(self, calculator):
        """Test factorial with a very large integer (100)."""
        result = calculator.factorial(100)
        assert result == 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000
