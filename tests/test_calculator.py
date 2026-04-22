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