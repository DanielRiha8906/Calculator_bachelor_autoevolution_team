import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calculator():
    """Fixture providing a Calculator instance for tests."""
    return Calculator()


class TestDivide:
    """Test suite for the divide method."""

    def test_divide_by_zero(self, calculator):
        """Test that dividing by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)

    def test_divide_zero_by_number(self, calculator):
        """Test that 0 divided by a number returns 0."""
        result = calculator.divide(0, 5)
        assert result == 0

    def test_divide_zero_by_negative_number(self, calculator):
        """Test that 0 divided by a negative number returns 0."""
        result = calculator.divide(0, -5)
        assert result == 0

    def test_divide_negative_by_positive(self, calculator):
        """Test that a negative number divided by a positive number returns a negative result."""
        result = calculator.divide(-10, 5)
        assert result == -2.0

    def test_divide_positive_by_negative(self, calculator):
        """Test that a positive number divided by a negative number returns a negative result."""
        result = calculator.divide(10, -5)
        assert result == -2.0

    def test_divide_negative_by_negative(self, calculator):
        """Test that a negative number divided by a negative number returns a positive result."""
        result = calculator.divide(-10, -5)
        assert result == 2.0

    def test_divide_normal_case(self, calculator):
        """Test normal division with positive integers."""
        result = calculator.divide(10, 2)
        assert result == 5.0

    def test_divide_fractional_result(self, calculator):
        """Test that division can produce fractional results."""
        result = calculator.divide(7, 2)
        assert result == 3.5


class TestAddition:
    """Test suite for the add method."""

    def test_add_positive_numbers(self, calculator):
        """Test addition of two positive numbers."""
        result = calculator.add(5, 3)
        assert result == 8

    def test_add_negative_numbers(self, calculator):
        """Test addition of two negative numbers."""
        result = calculator.add(-5, -3)
        assert result == -8

    def test_add_mixed_signs(self, calculator):
        """Test addition of numbers with mixed signs."""
        result = calculator.add(5, -3)
        assert result == 2

    def test_add_with_zero(self, calculator):
        """Test addition with zero."""
        result = calculator.add(5, 0)
        assert result == 5

    def test_add_floats(self, calculator):
        """Test addition of floating point numbers."""
        result = calculator.add(2.5, 3.7)
        assert result == pytest.approx(6.2)


class TestSubtraction:
    """Test suite for the subtract method."""

    def test_subtract_positive_numbers(self, calculator):
        """Test subtraction of positive numbers."""
        result = calculator.subtract(10, 3)
        assert result == 7

    def test_subtract_negative_numbers(self, calculator):
        """Test subtraction of negative numbers."""
        result = calculator.subtract(-10, -3)
        assert result == -7

    def test_subtract_mixed_signs(self, calculator):
        """Test subtraction with mixed signs."""
        result = calculator.subtract(5, -3)
        assert result == 8

    def test_subtract_resulting_in_zero(self, calculator):
        """Test subtraction resulting in zero."""
        result = calculator.subtract(5, 5)
        assert result == 0

    def test_subtract_floats(self, calculator):
        """Test subtraction of floating point numbers."""
        result = calculator.subtract(10.5, 3.2)
        assert result == pytest.approx(7.3)


class TestMultiplication:
    """Test suite for the multiply method."""

    def test_multiply_positive_numbers(self, calculator):
        """Test multiplication of positive numbers."""
        result = calculator.multiply(4, 5)
        assert result == 20

    def test_multiply_by_zero(self, calculator):
        """Test multiplication by zero."""
        result = calculator.multiply(5, 0)
        assert result == 0

    def test_multiply_negative_by_positive(self, calculator):
        """Test multiplication of negative by positive."""
        result = calculator.multiply(-4, 5)
        assert result == -20

    def test_multiply_negative_by_negative(self, calculator):
        """Test multiplication of two negative numbers."""
        result = calculator.multiply(-4, -5)
        assert result == 20

    def test_multiply_floats(self, calculator):
        """Test multiplication of floating point numbers."""
        result = calculator.multiply(2.5, 4.0)
        assert result == 10.0


class TestSquare:
    """Test suite for the square method."""

    def test_square_positive_integer(self, calculator):
        """Test square of a positive integer."""
        result = calculator.square(5)
        assert result == 25

    def test_square_negative_integer(self, calculator):
        """Test square of a negative integer."""
        result = calculator.square(-5)
        assert result == 25

    def test_square_zero(self, calculator):
        """Test square of zero."""
        result = calculator.square(0)
        assert result == 0

    def test_square_float(self, calculator):
        """Test square of a float."""
        result = calculator.square(2.5)
        assert result == 6.25


class TestCube:
    """Test suite for the cube method."""

    def test_cube_positive_integer(self, calculator):
        """Test cube of a positive integer."""
        result = calculator.cube(3)
        assert result == 27

    def test_cube_negative_integer(self, calculator):
        """Test cube of a negative integer."""
        result = calculator.cube(-3)
        assert result == -27

    def test_cube_zero(self, calculator):
        """Test cube of zero."""
        result = calculator.cube(0)
        assert result == 0

    def test_cube_float(self, calculator):
        """Test cube of a float."""
        result = calculator.cube(2.0)
        assert result == 8.0


class TestSquareRoot:
    """Test suite for the square_root method."""

    def test_square_root_positive_integer(self, calculator):
        """Test square root of a positive integer."""
        result = calculator.square_root(16)
        assert result == 4.0

    def test_square_root_perfect_square(self, calculator):
        """Test square root of a perfect square."""
        result = calculator.square_root(9)
        assert result == 3.0

    def test_square_root_non_perfect_square(self, calculator):
        """Test square root of a non-perfect square."""
        result = calculator.square_root(2)
        assert result == pytest.approx(1.4142135623730951)

    def test_square_root_zero(self, calculator):
        """Test square root of zero."""
        result = calculator.square_root(0)
        assert result == 0.0

    def test_square_root_negative_raises_error(self, calculator):
        """Test that square root of negative number raises ValueError."""
        with pytest.raises(ValueError):
            calculator.square_root(-4)

    def test_square_root_float(self, calculator):
        """Test square root of a float."""
        result = calculator.square_root(6.25)
        assert result == pytest.approx(2.5)


class TestCubeRoot:
    """Test suite for the cube_root method."""

    def test_cube_root_positive_integer(self, calculator):
        """Test cube root of a positive integer."""
        result = calculator.cube_root(8)
        assert result == pytest.approx(2.0)

    def test_cube_root_negative_integer(self, calculator):
        """Test cube root of a negative integer."""
        result = calculator.cube_root(-8)
        assert result == pytest.approx(-2.0)

    def test_cube_root_zero(self, calculator):
        """Test cube root of zero."""
        result = calculator.cube_root(0)
        assert result == 0.0

    def test_cube_root_non_perfect_cube(self, calculator):
        """Test cube root of a non-perfect cube."""
        result = calculator.cube_root(27)
        assert result == pytest.approx(3.0)

    def test_cube_root_float(self, calculator):
        """Test cube root of a float."""
        result = calculator.cube_root(1.728)
        assert result == pytest.approx(1.2)


class TestFactorial:
    """Test suite for the factorial method."""

    def test_factorial_small_positive_integer(self, calculator):
        """Test factorial of a small positive integer."""
        result = calculator.factorial(5)
        assert result == 120

    def test_factorial_zero(self, calculator):
        """Test factorial of zero."""
        result = calculator.factorial(0)
        assert result == 1

    def test_factorial_one(self, calculator):
        """Test factorial of one."""
        result = calculator.factorial(1)
        assert result == 1

    def test_factorial_large_integer(self, calculator):
        """Test factorial of a larger integer."""
        result = calculator.factorial(10)
        assert result == 3628800

    def test_factorial_negative_raises_error(self, calculator):
        """Test that factorial of negative number raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(-5)

    def test_factorial_non_integer_raises_error(self, calculator):
        """Test that factorial of non-integer raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(3.5)


class TestPower:
    """Test suite for the power method."""

    def test_power_positive_exponent(self, calculator):
        """Test power with positive exponent."""
        result = calculator.power(2, 3)
        assert result == 8

    def test_power_zero_exponent(self, calculator):
        """Test power with zero exponent."""
        result = calculator.power(5, 0)
        assert result == 1

    def test_power_negative_exponent(self, calculator):
        """Test power with negative exponent."""
        result = calculator.power(2, -2)
        assert result == pytest.approx(0.25)

    def test_power_fractional_exponent(self, calculator):
        """Test power with fractional exponent."""
        result = calculator.power(4, 0.5)
        assert result == pytest.approx(2.0)

    def test_power_base_zero(self, calculator):
        """Test power with base zero."""
        result = calculator.power(0, 3)
        assert result == 0

    def test_power_base_one(self, calculator):
        """Test power with base one."""
        result = calculator.power(1, 100)
        assert result == 1

    def test_power_negative_base_positive_exponent(self, calculator):
        """Test power with negative base and positive exponent."""
        result = calculator.power(-2, 3)
        assert result == -8

    def test_power_negative_base_even_exponent(self, calculator):
        """Test power with negative base and even exponent."""
        result = calculator.power(-2, 2)
        assert result == 4


class TestLog:
    """Test suite for the log method (base 10)."""

    def test_log10_positive_number(self, calculator):
        """Test base-10 logarithm of a positive number."""
        result = calculator.log(100)
        assert result == pytest.approx(2.0)

    def test_log10_one(self, calculator):
        """Test base-10 logarithm of one."""
        result = calculator.log(1)
        assert result == pytest.approx(0.0)

    def test_log10_ten(self, calculator):
        """Test base-10 logarithm of ten."""
        result = calculator.log(10)
        assert result == pytest.approx(1.0)

    def test_log10_fractional(self, calculator):
        """Test base-10 logarithm of a fractional number."""
        result = calculator.log(0.1)
        assert result == pytest.approx(-1.0)

    def test_log10_zero_raises_error(self, calculator):
        """Test that log of zero raises ValueError."""
        with pytest.raises(ValueError):
            calculator.log(0)

    def test_log10_negative_raises_error(self, calculator):
        """Test that log of negative number raises ValueError."""
        with pytest.raises(ValueError):
            calculator.log(-5)


class TestLn:
    """Test suite for the ln method (natural logarithm)."""

    def test_ln_positive_number(self, calculator):
        """Test natural logarithm of a positive number."""
        result = calculator.ln(10)
        assert result == pytest.approx(2.302585092994046)

    def test_ln_one(self, calculator):
        """Test natural logarithm of one."""
        result = calculator.ln(1)
        assert result == pytest.approx(0.0)

    def test_ln_e(self, calculator):
        """Test natural logarithm of e."""
        result = calculator.ln(math.e)
        assert result == pytest.approx(1.0)

    def test_ln_fractional(self, calculator):
        """Test natural logarithm of a fractional number."""
        result = calculator.ln(0.5)
        assert result == pytest.approx(-0.6931471805599453)

    def test_ln_zero_raises_error(self, calculator):
        """Test that ln of zero raises ValueError."""
        with pytest.raises(ValueError):
            calculator.ln(0)

    def test_ln_negative_raises_error(self, calculator):
        """Test that ln of negative number raises ValueError."""
        with pytest.raises(ValueError):
            calculator.ln(-5)