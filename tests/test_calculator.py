import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calculator():
    """Fixture providing a Calculator instance for tests."""
    return Calculator()


class TestCalculatorAdd:
    """Test suite for Calculator.add() method."""

    def test_addition_positive_integers(self, calculator):
        """Verify addition of positive integers."""
        result = calculator.add(5, 3)
        assert result == 8

    def test_addition_negative_integers(self, calculator):
        """Verify addition of negative integers."""
        result = calculator.add(-5, -3)
        assert result == -8

    def test_addition_mixed_signs(self, calculator):
        """Verify addition with mixed sign operands."""
        result = calculator.add(-5, 8)
        assert result == 3

    def test_addition_with_floats(self, calculator):
        """Verify addition with float operands."""
        result = calculator.add(2.5, 3.5)
        assert result == 6.0

    def test_addition_with_zero(self, calculator):
        """Verify addition with zero as second operand."""
        result = calculator.add(5, 0)
        assert result == 5

    def test_addition_zero_to_zero(self, calculator):
        """Verify addition of zero and zero."""
        result = calculator.add(0, 0)
        assert result == 0


class TestCalculatorSubtract:
    """Test suite for Calculator.subtract() method."""

    def test_subtraction_positive_integers(self, calculator):
        """Verify subtraction of positive integers."""
        result = calculator.subtract(10, 3)
        assert result == 7

    def test_subtraction_negative_result(self, calculator):
        """Verify subtraction resulting in negative value."""
        result = calculator.subtract(3, 10)
        assert result == -7

    def test_subtraction_negative_operands(self, calculator):
        """Verify subtraction with negative operands."""
        result = calculator.subtract(-5, -3)
        assert result == -2

    def test_subtraction_with_floats(self, calculator):
        """Verify subtraction with float operands."""
        result = calculator.subtract(7.5, 2.5)
        assert result == 5.0

    def test_subtraction_with_zero_minuend(self, calculator):
        """Verify subtraction with zero as minuend."""
        result = calculator.subtract(0, 5)
        assert result == -5

    def test_subtraction_with_zero_subtrahend(self, calculator):
        """Verify subtraction with zero as subtrahend."""
        result = calculator.subtract(5, 0)
        assert result == 5


class TestCalculatorMultiply:
    """Test suite for Calculator.multiply() method."""

    def test_multiplication_positive_integers(self, calculator):
        """Verify multiplication of positive integers."""
        result = calculator.multiply(4, 3)
        assert result == 12

    def test_multiplication_negative_integers(self, calculator):
        """Verify multiplication of negative integers."""
        result = calculator.multiply(-4, -3)
        assert result == 12

    def test_multiplication_mixed_signs(self, calculator):
        """Verify multiplication with mixed sign operands."""
        result = calculator.multiply(-4, 3)
        assert result == -12

    def test_multiplication_with_floats(self, calculator):
        """Verify multiplication with float operands."""
        result = calculator.multiply(2.5, 4.0)
        assert result == 10.0

    def test_multiplication_by_zero(self, calculator):
        """Verify multiplication by zero."""
        result = calculator.multiply(5, 0)
        assert result == 0

    def test_multiplication_by_one(self, calculator):
        """Verify multiplication by one."""
        result = calculator.multiply(5, 1)
        assert result == 5


class TestCalculatorDivide:
    """Test suite for Calculator.divide() method."""

    def test_division_by_zero(self, calculator):
        """Verify that dividing by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)

    def test_division_normal(self, calculator):
        """Verify correct behavior with positive integer operands."""
        result = calculator.divide(10, 2)
        assert result == 5.0

    def test_division_with_floats(self, calculator):
        """Verify correct behavior with float operands."""
        result = calculator.divide(7.5, 2.5)
        assert result == 3.0

    def test_division_negative_divisor(self, calculator):
        """Verify correct behavior with negative divisor."""
        result = calculator.divide(10, -2)
        assert result == -5.0

    def test_division_zero_dividend(self, calculator):
        """Verify zero numerator is handled correctly."""
        result = calculator.divide(0, 5)
        assert result == 0.0


class TestCalculatorFactorial:
    """Test suite for Calculator.factorial() method."""

    def test_factorial_zero(self, calculator):
        """Verify factorial of zero returns 1."""
        result = calculator.factorial(0)
        assert result == 1

    def test_factorial_one(self, calculator):
        """Verify factorial of one returns 1."""
        result = calculator.factorial(1)
        assert result == 1

    def test_factorial_small_positive(self, calculator):
        """Verify factorial of small positive integer."""
        result = calculator.factorial(5)
        assert result == 120

    def test_factorial_moderate_positive(self, calculator):
        """Verify factorial of moderate positive integer."""
        result = calculator.factorial(10)
        assert result == 3628800

    def test_factorial_twenty(self, calculator):
        """Verify factorial of twenty."""
        result = calculator.factorial(20)
        assert result == 2432902008176640000

    def test_factorial_negative_raises_error(self, calculator):
        """Verify that factorial of negative integer raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(-1)

    def test_factorial_negative_five_raises_error(self, calculator):
        """Verify that factorial of -5 raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(-5)

    def test_factorial_float_raises_error(self, calculator):
        """Verify that factorial of float raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(5.5)

    def test_factorial_string_raises_error(self, calculator):
        """Verify that factorial of string raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial("5")

    def test_factorial_none_raises_error(self, calculator):
        """Verify that factorial of None raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(None)


class TestCalculatorSquare:
    """Test suite for Calculator.square() method."""

    def test_square_positive_integer(self, calculator):
        """Verify square of positive integer."""
        result = calculator.square(4)
        assert result == 16

    def test_square_negative_integer(self, calculator):
        """Verify square of negative integer."""
        result = calculator.square(-5)
        assert result == 25

    def test_square_zero(self, calculator):
        """Verify square of zero."""
        result = calculator.square(0)
        assert result == 0

    def test_square_float(self, calculator):
        """Verify square of float."""
        result = calculator.square(2.5)
        assert result == 6.25

    def test_square_small_float(self, calculator):
        """Verify square of small float."""
        result = calculator.square(0.5)
        assert result == 0.25


class TestCalculatorCube:
    """Test suite for Calculator.cube() method."""

    def test_cube_positive_integer(self, calculator):
        """Verify cube of positive integer."""
        result = calculator.cube(3)
        assert result == 27

    def test_cube_negative_integer(self, calculator):
        """Verify cube of negative integer."""
        result = calculator.cube(-2)
        assert result == -8

    def test_cube_zero(self, calculator):
        """Verify cube of zero."""
        result = calculator.cube(0)
        assert result == 0

    def test_cube_float(self, calculator):
        """Verify cube of float."""
        result = calculator.cube(2.0)
        assert result == 8.0

    def test_cube_negative_float(self, calculator):
        """Verify cube of negative float."""
        result = calculator.cube(-1.5)
        assert result == -3.375


class TestCalculatorSquareRoot:
    """Test suite for Calculator.square_root() method."""

    def test_square_root_perfect_square(self, calculator):
        """Verify square root of perfect square."""
        result = calculator.square_root(9)
        assert result == 3.0

    def test_square_root_non_perfect(self, calculator):
        """Verify square root of non-perfect square."""
        result = calculator.square_root(2)
        assert result == pytest.approx(math.sqrt(2))

    def test_square_root_zero(self, calculator):
        """Verify square root of zero."""
        result = calculator.square_root(0)
        assert result == 0.0

    def test_square_root_float(self, calculator):
        """Verify square root of float."""
        result = calculator.square_root(2.25)
        assert result == 1.5

    def test_square_root_negative_raises_error(self, calculator):
        """Verify that square root of negative integer raises ValueError."""
        with pytest.raises(ValueError):
            calculator.square_root(-1)

    def test_square_root_negative_large_raises_error(self, calculator):
        """Verify that square root of large negative raises ValueError."""
        with pytest.raises(ValueError):
            calculator.square_root(-100)


class TestCalculatorCubeRoot:
    """Test suite for Calculator.cube_root() method."""

    def test_cube_root_positive_integer(self, calculator):
        """Verify cube root of positive integer."""
        result = calculator.cube_root(8)
        assert result == 2.0

    def test_cube_root_non_perfect(self, calculator):
        """Verify cube root of non-perfect cube."""
        result = calculator.cube_root(2)
        assert result == pytest.approx(2 ** (1/3))

    def test_cube_root_negative_integer(self, calculator):
        """Verify cube root of negative integer."""
        result = calculator.cube_root(-8)
        assert result == -2.0

    def test_cube_root_zero(self, calculator):
        """Verify cube root of zero."""
        result = calculator.cube_root(0)
        assert result == 0.0

    def test_cube_root_negative_float(self, calculator):
        """Verify cube root of negative float."""
        result = calculator.cube_root(-1.0)
        assert result == -1.0

    def test_cube_root_float(self, calculator):
        """Verify cube root of float."""
        result = calculator.cube_root(27.0)
        assert result == 3.0


class TestCalculatorPower:
    """Test suite for Calculator.power() method."""

    def test_power_positive_exponent(self, calculator):
        """Verify power with positive exponent."""
        result = calculator.power(2, 3)
        assert result == 8

    def test_power_zero_exponent(self, calculator):
        """Verify power with zero exponent."""
        result = calculator.power(5, 0)
        assert result == 1

    def test_power_exponent_one(self, calculator):
        """Verify power with exponent of one."""
        result = calculator.power(7, 1)
        assert result == 7

    def test_power_negative_exponent(self, calculator):
        """Verify power with negative exponent."""
        result = calculator.power(2, -1)
        assert result == 0.5

    def test_power_float_base(self, calculator):
        """Verify power with float base."""
        result = calculator.power(2.5, 2)
        assert result == 6.25

    def test_power_float_exponent(self, calculator):
        """Verify power with float exponent."""
        result = calculator.power(4, 0.5)
        assert result == 2.0

    def test_power_negative_base_even_exp(self, calculator):
        """Verify power with negative base and even exponent."""
        result = calculator.power(-3, 2)
        assert result == 9

    def test_power_negative_base_odd_exp(self, calculator):
        """Verify power with negative base and odd exponent."""
        result = calculator.power(-2, 3)
        assert result == -8

    def test_power_negative_base_float_exp(self, calculator):
        """Verify that power with negative base and float exponent raises ValueError."""
        with pytest.raises(ValueError):
            calculator.power(-4, 0.5)

    def test_power_zero_base_positive_exp(self, calculator):
        """Verify power with zero base and positive exponent."""
        result = calculator.power(0, 3)
        assert result == 0

    def test_power_zero_base_zero_exp(self, calculator):
        """Verify power with zero base and zero exponent."""
        result = calculator.power(0, 0)
        assert result == 1


class TestCalculatorLog10:
    """Test suite for Calculator.log10() method."""

    def test_log10_ten(self, calculator):
        """Verify log base 10 of 10."""
        result = calculator.log10(10)
        assert result == 1.0

    def test_log10_one(self, calculator):
        """Verify log base 10 of 1."""
        result = calculator.log10(1)
        assert result == 0.0

    def test_log10_hundred(self, calculator):
        """Verify log base 10 of 100."""
        result = calculator.log10(100)
        assert result == 2.0

    def test_log10_float(self, calculator):
        """Verify log base 10 of float."""
        result = calculator.log10(2.5)
        assert result == pytest.approx(math.log10(2.5))

    def test_log10_small_positive(self, calculator):
        """Verify log base 10 of small positive value."""
        result = calculator.log10(0.1)
        assert result == pytest.approx(-1.0)

    def test_log10_zero_raises_error(self, calculator):
        """Verify that log10 of zero raises ValueError."""
        with pytest.raises(ValueError):
            calculator.log10(0)

    def test_log10_negative_raises_error(self, calculator):
        """Verify that log10 of negative integer raises ValueError."""
        with pytest.raises(ValueError):
            calculator.log10(-5)

    def test_log10_negative_float_raises_error(self, calculator):
        """Verify that log10 of negative float raises ValueError."""
        with pytest.raises(ValueError):
            calculator.log10(-2.5)


class TestCalculatorLn:
    """Test suite for Calculator.ln() method."""

    def test_ln_e(self, calculator):
        """Verify natural log of e."""
        result = calculator.ln(math.e)
        assert result == pytest.approx(1.0)

    def test_ln_one(self, calculator):
        """Verify natural log of 1."""
        result = calculator.ln(1)
        assert result == 0.0

    def test_ln_small_positive(self, calculator):
        """Verify natural log of small positive value."""
        result = calculator.ln(0.5)
        assert result == pytest.approx(math.log(0.5))

    def test_ln_large_positive(self, calculator):
        """Verify natural log of large positive value."""
        result = calculator.ln(100)
        assert result == pytest.approx(math.log(100))

    def test_ln_float(self, calculator):
        """Verify natural log of float approximately e."""
        result = calculator.ln(2.718)
        assert result == pytest.approx(1.0, abs=0.01)

    def test_ln_zero_raises_error(self, calculator):
        """Verify that ln of zero raises ValueError."""
        with pytest.raises(ValueError):
            calculator.ln(0)

    def test_ln_negative_raises_error(self, calculator):
        """Verify that ln of negative integer raises ValueError."""
        with pytest.raises(ValueError):
            calculator.ln(-1)

    def test_ln_negative_float_raises_error(self, calculator):
        """Verify that ln of negative float raises ValueError."""
        with pytest.raises(ValueError):
            calculator.ln(-10.5)