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

    def test_add(self, calculator):
        """Test addition"""
        assert calculator.add(2, 3) == 5

    def test_subtract(self, calculator):
        """Test subtraction"""
        assert calculator.subtract(5, 3) == 2

    def test_multiply(self, calculator):
        """Test multiplication"""
        assert calculator.multiply(4, 5) == 20