import pytest
import math
from src.calculator import Calculator


class TestCalculatorDivide:
    """Test suite for Calculator.divide() method"""

    @pytest.fixture
    def calculator(self):
        """Fixture to provide a Calculator instance for each test"""
        return Calculator()

    def test_divide_positive_numbers(self, calculator):
        """Test division of two positive numbers"""
        assert calculator.divide(10, 2) == 5.0

    def test_divide_negative_numbers(self, calculator):
        """Test division with negative numbers"""
        assert calculator.divide(-10, 2) == -5.0
        assert calculator.divide(10, -2) == -5.0
        assert calculator.divide(-10, -2) == 5.0

    def test_divide_by_one(self, calculator):
        """Test division by one returns the dividend"""
        assert calculator.divide(5, 1) == 5.0
        assert calculator.divide(0, 1) == 0.0

    def test_divide_zero_dividend(self, calculator):
        """Test division where numerator is zero"""
        assert calculator.divide(0, 5) == 0.0
        assert calculator.divide(0, 1) == 0.0
        assert calculator.divide(0, -1) == -0.0

    def test_divide_by_zero(self, calculator):
        """Test that division by zero raises ZeroDivisionError"""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(5, 0)

    def test_divide_zero_by_zero(self, calculator):
        """Test that zero divided by zero raises ZeroDivisionError"""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(0, 0)

    def test_divide_fractional_result(self, calculator):
        """Test division that results in a fraction"""
        assert calculator.divide(5, 2) == 2.5
        assert calculator.divide(1, 3) == pytest.approx(0.333333, rel=1e-5)

    def test_divide_very_small_numbers(self, calculator):
        """Test division with very small numbers"""
        result = calculator.divide(1e-10, 1e-5)
        assert result == pytest.approx(1e-5)

    def test_divide_very_large_numbers(self, calculator):
        """Test division with very large numbers"""
        result = calculator.divide(1e100, 1e50)
        assert result == pytest.approx(1e50)


class TestCalculatorBasicOperations:
    """Test suite for other Calculator operations"""

    @pytest.fixture
    def calculator(self):
        """Fixture to provide a Calculator instance for each test"""
        return Calculator()

    # ===== ADDITION TESTS =====

    def test_add_basic_positive_numbers(self, calculator):
        """Test addition of two basic positive numbers"""
        assert calculator.add(2, 3) == 5
        assert calculator.add(10, 20) == 30
        assert calculator.add(1, 1) == 2

    def test_add_negative_numbers(self, calculator):
        """Test addition with negative numbers"""
        assert calculator.add(-5, -3) == -8
        assert calculator.add(-10, 5) == -5
        assert calculator.add(10, -5) == 5

    def test_add_with_zero(self, calculator):
        """Test addition with zero operands"""
        assert calculator.add(0, 5) == 5
        assert calculator.add(5, 0) == 5
        assert calculator.add(0, 0) == 0
        assert calculator.add(0, -5) == -5

    def test_add_large_numbers(self, calculator):
        """Test addition of large numbers"""
        assert calculator.add(1e10, 2e10) == 3e10
        assert calculator.add(999999999, 1) == 1000000000

    def test_add_floating_point_numbers(self, calculator):
        """Test addition of floating-point numbers"""
        assert calculator.add(1.5, 2.5) == 4.0
        assert calculator.add(0.1, 0.2) == pytest.approx(0.3)
        assert calculator.add(1.1, 2.2) == pytest.approx(3.3)
        assert calculator.add(-1.5, 2.5) == 1.0

    # ===== SUBTRACTION TESTS =====

    def test_subtract_basic_positive_numbers(self, calculator):
        """Test subtraction of two basic positive numbers"""
        assert calculator.subtract(5, 3) == 2
        assert calculator.subtract(10, 5) == 5
        assert calculator.subtract(100, 1) == 99

    def test_subtract_larger_from_smaller(self, calculator):
        """Test subtraction where smaller is subtracted from larger and vice versa"""
        assert calculator.subtract(3, 5) == -2
        assert calculator.subtract(1, 10) == -9

    def test_subtract_negative_numbers(self, calculator):
        """Test subtraction with negative numbers"""
        assert calculator.subtract(-5, -3) == -2
        assert calculator.subtract(-10, 5) == -15
        assert calculator.subtract(10, -5) == 15
        assert calculator.subtract(-5, 10) == -15

    def test_subtract_with_zero(self, calculator):
        """Test subtraction with zero operands"""
        assert calculator.subtract(0, 5) == -5
        assert calculator.subtract(5, 0) == 5
        assert calculator.subtract(0, 0) == 0

    def test_subtract_self_subtraction(self, calculator):
        """Test subtracting a number from itself"""
        assert calculator.subtract(5, 5) == 0
        assert calculator.subtract(-10, -10) == 0
        assert calculator.subtract(1.5, 1.5) == 0.0

    def test_subtract_large_numbers(self, calculator):
        """Test subtraction of large numbers"""
        assert calculator.subtract(1e10, 5e9) == pytest.approx(5e9)
        assert calculator.subtract(999999999, 999999998) == 1

    def test_subtract_floating_point_numbers(self, calculator):
        """Test subtraction of floating-point numbers"""
        assert calculator.subtract(5.5, 2.5) == 3.0
        assert calculator.subtract(1.0, 0.1) == pytest.approx(0.9)
        assert calculator.subtract(2.2, 1.1) == pytest.approx(1.1)
        assert calculator.subtract(-1.5, 2.5) == -4.0

    # ===== MULTIPLICATION TESTS =====

    def test_multiply_basic_positive_numbers(self, calculator):
        """Test multiplication of two basic positive numbers"""
        assert calculator.multiply(4, 5) == 20
        assert calculator.multiply(2, 3) == 6
        assert calculator.multiply(10, 10) == 100

    def test_multiply_negative_numbers(self, calculator):
        """Test multiplication with negative numbers"""
        assert calculator.multiply(-4, -5) == 20
        assert calculator.multiply(-4, 5) == -20
        assert calculator.multiply(4, -5) == -20

    def test_multiply_with_zero(self, calculator):
        """Test multiplication with zero operands"""
        assert calculator.multiply(0, 5) == 0
        assert calculator.multiply(5, 0) == 0
        assert calculator.multiply(0, 0) == 0
        assert calculator.multiply(0, -5) == 0

    def test_multiply_with_one(self, calculator):
        """Test multiplication with one (identity property)"""
        assert calculator.multiply(1, 5) == 5
        assert calculator.multiply(5, 1) == 5
        assert calculator.multiply(1, -5) == -5
        assert calculator.multiply(1, 1) == 1

    def test_multiply_large_numbers(self, calculator):
        """Test multiplication of large numbers"""
        assert calculator.multiply(1e10, 2e10) == 2e20
        assert calculator.multiply(999999, 2) == 1999998

    def test_multiply_floating_point_numbers(self, calculator):
        """Test multiplication of floating-point numbers"""
        assert calculator.multiply(2.5, 4.0) == 10.0
        assert calculator.multiply(0.5, 0.5) == 0.25
        assert calculator.multiply(1.5, 2.0) == 3.0

    def test_multiply_fractional_results(self, calculator):
        """Test multiplication producing fractional results"""
        assert calculator.multiply(0.5, 0.5) == 0.25
        assert calculator.multiply(0.1, 0.1) == pytest.approx(0.01)
        assert calculator.multiply(1.5, 1.5) == 2.25
        assert calculator.multiply(-0.5, 2) == -1.0


class TestCalculatorFactorial:
    """Test suite for Calculator.factorial() method"""

    @pytest.fixture
    def calculator(self):
        """Fixture to provide a Calculator instance for each test"""
        return Calculator()

    def test_factorial_zero(self, calculator):
        """Test factorial of zero (0! = 1)"""
        assert calculator.factorial(0) == 1

    def test_factorial_one(self, calculator):
        """Test factorial of one (1! = 1)"""
        assert calculator.factorial(1) == 1

    @pytest.mark.parametrize("n,expected", [
        (2, 2),
        (3, 6),
        (5, 120),
    ])
    def test_factorial_small_positive(self, calculator, n, expected):
        """Test factorial for small positive integers"""
        assert calculator.factorial(n) == expected

    def test_factorial_medium_value(self, calculator):
        """Test factorial of medium positive integer (10!)"""
        assert calculator.factorial(10) == 3628800

    def test_factorial_large_value(self, calculator):
        """Test factorial of large positive integer (20!)"""
        assert calculator.factorial(20) == 2432902008176640000

    def test_factorial_negative_input(self, calculator):
        """Test that negative inputs raise ValueError"""
        with pytest.raises(ValueError, match="Factorial is only defined for non-negative integers"):
            calculator.factorial(-1)

    @pytest.mark.parametrize("invalid_input", [
        3.0,
        "5",
    ])
    def test_factorial_invalid_type_input(self, calculator, invalid_input):
        """Test that non-integer inputs raise ValueError"""
        with pytest.raises(ValueError, match="Factorial is only defined for non-negative integers"):
            calculator.factorial(invalid_input)

    @pytest.mark.parametrize("bool_input", [True, False])
    def test_factorial_bool_input(self, calculator, bool_input):
        """Test that boolean inputs raise ValueError (bool is subclass of int but should be rejected)"""
        with pytest.raises(ValueError, match="Factorial is only defined for non-negative integers"):
            calculator.factorial(bool_input)


class TestCalculatorSquare:
    """Test suite for Calculator.square() method"""

    @pytest.fixture
    def calculator(self):
        """Fixture to provide a Calculator instance for each test"""
        return Calculator()

    @pytest.mark.parametrize("x,expected", [
        (2, 4),
        (3, 9),
        (5, 25),
        (-2, 4),
        (-5, 25),
        (0, 0),
        (1.5, 2.25),
        (0.5, 0.25),
    ])
    def test_square_various_values(self, calculator, x, expected):
        """Test square for positive, negative, zero, and floating-point values"""
        assert calculator.square(x) == expected


class TestCalculatorCube:
    """Test suite for Calculator.cube() method"""

    @pytest.fixture
    def calculator(self):
        """Fixture to provide a Calculator instance for each test"""
        return Calculator()

    @pytest.mark.parametrize("x,expected", [
        (2, 8),
        (3, 27),
        (-2, -8),
        (-3, -27),
        (0, 0),
        (1.5, 3.375),
    ])
    def test_cube_various_values(self, calculator, x, expected):
        """Test cube for positive, negative, zero, and floating-point values"""
        result = calculator.cube(x)
        assert result == pytest.approx(expected)


class TestCalculatorSquareRoot:
    """Test suite for Calculator.square_root() method"""

    @pytest.fixture
    def calculator(self):
        """Fixture to provide a Calculator instance for each test"""
        return Calculator()

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (1, 1),
        (4, 2),
        (9, 3),
        (100, 10),
        (0.25, 0.5),
    ])
    def test_square_root_perfect_squares(self, calculator, x, expected):
        """Test square root of perfect squares and floating-point values"""
        assert calculator.square_root(x) == expected

    def test_square_root_non_perfect_square(self, calculator):
        """Test square root of non-perfect square"""
        result = calculator.square_root(2)
        assert result == pytest.approx(1.4142, rel=1e-4)

    @pytest.mark.parametrize("x", [-1, -0.5])
    def test_square_root_negative_input(self, calculator, x):
        """Test that negative inputs raise ValueError"""
        with pytest.raises(ValueError, match="Square root is not defined for negative numbers"):
            calculator.square_root(x)


class TestCalculatorCubeRoot:
    """Test suite for Calculator.cube_root() method"""

    @pytest.fixture
    def calculator(self):
        """Fixture to provide a Calculator instance for each test"""
        return Calculator()

    @pytest.mark.parametrize("x,expected", [
        (0, 0),
        (1, 1),
        (8, 2),
        (27, 3),
        (-1, -1),
        (-8, -2),
        (-27, -3),
    ])
    def test_cube_root_perfect_cubes(self, calculator, x, expected):
        """Test cube root of perfect cubes (positive and negative)"""
        result = calculator.cube_root(x)
        assert result == pytest.approx(expected)

    @pytest.mark.parametrize("x,expected", [
        (2, 1.2599),
        (-2, -1.2599),
    ])
    def test_cube_root_non_perfect_cubes(self, calculator, x, expected):
        """Test cube root of non-perfect cubes with sign preservation"""
        result = calculator.cube_root(x)
        assert result == pytest.approx(expected, rel=1e-4)

    def test_cube_root_large_value(self, calculator):
        """Test cube root of large value"""
        result = calculator.cube_root(1e9)
        assert result == pytest.approx(1000, rel=1e-4)


class TestCalculatorPower:
    """Test suite for Calculator.power() method"""

    @pytest.fixture
    def calculator(self):
        """Fixture to provide a Calculator instance for each test"""
        return Calculator()

    @pytest.mark.parametrize("x,y,expected", [
        (2, 3, 8),
        (5, 2, 25),
        (10, 0, 1),
        (0, 2, 0),
        (2, -1, 0.5),
        (4, -2, 0.0625),
        (4, 0.5, 2.0),
        (-2, 2, 4),
        (-2, 3, -8),
    ])
    def test_power_various_exponents(self, calculator, x, y, expected):
        """Test power with integer, negative, and float exponents"""
        result = calculator.power(x, y)
        assert result == pytest.approx(expected)

    @pytest.mark.parametrize("y", [-1, -2])
    def test_power_zero_base_negative_exponent(self, calculator, y):
        """Test that 0^(-n) raises ValueError"""
        with pytest.raises(ValueError, match="0 raised to a negative power is undefined"):
            calculator.power(0, y)


class TestCalculatorLog:
    """Test suite for Calculator.log() method (base-10 logarithm)"""

    @pytest.fixture
    def calculator(self):
        """Fixture to provide a Calculator instance for each test"""
        return Calculator()

    @pytest.mark.parametrize("x,expected", [
        (1, 0),
        (10, 1),
        (100, 2),
        (1000, 3),
        (0.1, -1),
        (0.01, -2),
    ])
    def test_log_powers_of_ten(self, calculator, x, expected):
        """Test log (base-10) of powers of 10"""
        result = calculator.log(x)
        assert result == pytest.approx(expected)

    def test_log_non_power_of_ten(self, calculator):
        """Test log of non-power-of-ten value"""
        result = calculator.log(2)
        assert result == pytest.approx(0.3010, rel=1e-3)

    @pytest.mark.parametrize("x", [0, -1])
    def test_log_non_positive_input(self, calculator, x):
        """Test that zero and negative inputs raise ValueError"""
        with pytest.raises(ValueError, match="Logarithm is only defined for positive numbers"):
            calculator.log(x)


class TestCalculatorLn:
    """Test suite for Calculator.ln() method (natural logarithm)"""

    @pytest.fixture
    def calculator(self):
        """Fixture to provide a Calculator instance for each test"""
        return Calculator()

    def test_ln_one(self, calculator):
        """Test natural log of 1"""
        assert calculator.ln(1) == 0

    def test_ln_e(self, calculator):
        """Test natural log of e (should be ~1.0)"""
        result = calculator.ln(math.e)
        assert result == pytest.approx(1.0)

    def test_ln_two(self, calculator):
        """Test natural log of 2"""
        result = calculator.ln(2)
        assert result == pytest.approx(0.6931, rel=1e-4)

    def test_ln_half(self, calculator):
        """Test natural log of 0.5 (should be negative)"""
        result = calculator.ln(0.5)
        assert result < 0

    @pytest.mark.parametrize("x", [0, -1])
    def test_ln_non_positive_input(self, calculator, x):
        """Test that zero and negative inputs raise ValueError"""
        with pytest.raises(ValueError, match="Natural logarithm is only defined for positive numbers"):
            calculator.ln(x)