import pytest
import math
from src.calculator import Calculator


class TestDivide:
    """Test suite for Calculator.divide() method."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance for each test."""
        return Calculator()

    # Happy Path Tests
    def test_divide_positive_numbers(self, calculator):
        """Test division of two positive numbers returns correct result."""
        result = calculator.divide(10, 2)
        assert result == 5.0

    def test_divide_negative_numerator(self, calculator):
        """Test division with negative numerator."""
        result = calculator.divide(-10, 2)
        assert result == -5.0

    def test_divide_negative_denominator(self, calculator):
        """Test division with negative denominator."""
        result = calculator.divide(10, -2)
        assert result == -5.0

    def test_divide_both_negative(self, calculator):
        """Test division with both negative numbers."""
        result = calculator.divide(-10, -2)
        assert result == 5.0

    def test_divide_fractional_result(self, calculator):
        """Test division that produces a fractional result."""
        result = calculator.divide(7, 2)
        assert result == 3.5

    def test_divide_zero_numerator(self, calculator):
        """Test division with zero numerator returns 0.0 without error."""
        result = calculator.divide(0, 5)
        assert result == 0.0

    def test_divide_zero_numerator_with_float_denominator(self, calculator):
        """Test division with zero numerator and float denominator."""
        result = calculator.divide(0, 2.5)
        assert result == 0.0

    def test_divide_floating_point_numbers(self, calculator):
        """Test division of floating point numbers."""
        result = calculator.divide(7.5, 2.5)
        assert result == 3.0

    # Edge Cases: Division by Zero
    @pytest.mark.parametrize("numerator", [0, 1, -1, 10, -10, 3.14, -2.71])
    def test_divide_by_zero_integer(self, calculator, numerator):
        """Test division by zero (integer) raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(numerator, 0)

    @pytest.mark.parametrize("numerator", [0, 1, -1, 10, -10, 3.14, -2.71])
    def test_divide_by_zero_float(self, calculator, numerator):
        """Test division by zero (float 0.0) raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(numerator, 0.0)

    # Edge Cases: Very Large and Very Small Numbers
    def test_divide_very_large_numbers(self, calculator):
        """Test division with very large numbers."""
        result = calculator.divide(1e100, 1e50)
        assert abs(result - 1e50) < 1e35

    def test_divide_very_small_numbers(self, calculator):
        """Test division with very small numbers."""
        result = calculator.divide(1e-100, 1e-50)
        assert result == 1e-50

    def test_divide_results_in_very_small_number(self, calculator):
        """Test division that results in a very small number."""
        result = calculator.divide(1e-100, 1e50)
        assert result == 1e-150

    # Edge Cases: Type Handling
    def test_divide_mixed_int_float(self, calculator):
        """Test division with mixed integer and float types."""
        result = calculator.divide(5, 2.0)
        assert result == 2.5

    def test_divide_float_numerator_int_denominator(self, calculator):
        """Test division with float numerator and int denominator."""
        result = calculator.divide(5.0, 2)
        assert result == 2.5

    # Edge Cases: Result Precision
    def test_divide_result_precision(self, calculator):
        """Test division precision with repeating decimal."""
        result = calculator.divide(1, 3)
        assert abs(result - 0.3333333333333333) < 1e-15

    # Edge Cases: Invalid Type Inputs
    @pytest.mark.parametrize("invalid_input", ["string", [], {}, None, (1, 2)])
    def test_divide_invalid_numerator(self, calculator, invalid_input):
        """Test division with invalid numerator type raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(invalid_input, 5)

    @pytest.mark.parametrize("invalid_input", ["string", [], {}, None, (1, 2)])
    def test_divide_invalid_denominator(self, calculator, invalid_input):
        """Test division with invalid denominator type raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(5, invalid_input)


class TestAdd:
    """Test suite for Calculator.add() method."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance for each test."""
        return Calculator()

    # Happy Path Tests
    @pytest.mark.parametrize("a,b,expected", [
        (3, 5, 8),
        (0, 0, 0),
        (100, 200, 300),
        (-1, 1, 0),
    ])
    def test_add_positive_integers(self, calculator, a, b, expected):
        """Test addition of positive integers."""
        result = calculator.add(a, b)
        assert result == expected

    def test_add_negative_numbers(self, calculator):
        """Test addition with negative numbers."""
        result = calculator.add(-3, 5)
        assert result == 2

    def test_add_both_negative(self, calculator):
        """Test addition of two negative numbers."""
        result = calculator.add(-3, -5)
        assert result == -8

    def test_add_zero_operand(self, calculator):
        """Test addition with zero operand."""
        result = calculator.add(0, 5)
        assert result == 5

    @pytest.mark.parametrize("a,b,expected", [
        (1.5, 2.5, 4.0),
        (0.1, 0.2, pytest.approx(0.3)),
        (3.7, 1.3, 5.0),
    ])
    def test_add_floats(self, calculator, a, b, expected):
        """Test addition of floating point numbers."""
        result = calculator.add(a, b)
        assert result == expected

    def test_add_mixed_int_float(self, calculator):
        """Test addition of mixed integer and float."""
        result = calculator.add(1, 2.5)
        assert result == 3.5

    def test_add_very_large_numbers(self, calculator):
        """Test addition with very large numbers."""
        result = calculator.add(10**15, 10**15)
        assert result == 2 * (10**15)

    def test_add_very_small_numbers(self, calculator):
        """Test addition with very small numbers."""
        result = calculator.add(1e-10, 2e-10)
        assert result == pytest.approx(3e-10)

    def test_add_result_near_zero(self, calculator):
        """Test addition that results in zero."""
        result = calculator.add(-5, 5)
        assert result == 0

    def test_add_float_precision(self, calculator):
        """Test addition with floating point precision."""
        result = calculator.add(0.1, 0.2)
        assert result == pytest.approx(0.3)

    # Edge Cases: Type Handling
    @pytest.mark.parametrize("invalid_input", ["string", [], {}, None, (1, 2)])
    def test_add_invalid_first_operand(self, calculator, invalid_input):
        """Test addition with invalid first operand type raises TypeError."""
        with pytest.raises(TypeError):
            calculator.add(invalid_input, 5)

    @pytest.mark.parametrize("invalid_input", ["string", [], {}, None, (1, 2)])
    def test_add_invalid_second_operand(self, calculator, invalid_input):
        """Test addition with invalid second operand type raises TypeError."""
        with pytest.raises(TypeError):
            calculator.add(5, invalid_input)


class TestSubtract:
    """Test suite for Calculator.subtract() method."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance for each test."""
        return Calculator()

    # Happy Path Tests
    @pytest.mark.parametrize("a,b,expected", [
        (10, 3, 7),
        (100, 50, 50),
        (1, 1, 0),
        (5, 0, 5),
    ])
    def test_subtract_positive_integers(self, calculator, a, b, expected):
        """Test subtraction of positive integers."""
        result = calculator.subtract(a, b)
        assert result == expected

    def test_subtract_negative_numbers(self, calculator):
        """Test subtraction with negative numbers."""
        result = calculator.subtract(-3, 5)
        assert result == -8

    def test_subtract_both_negative(self, calculator):
        """Test subtraction of two negative numbers."""
        result = calculator.subtract(-3, -5)
        assert result == 2

    def test_subtract_same_number(self, calculator):
        """Test subtraction of a number from itself."""
        result = calculator.subtract(5, 5)
        assert result == 0

    @pytest.mark.parametrize("a,b,expected", [
        (2.5, 1.5, 1.0),
        (5.5, 2.5, 3.0),
        (1.0, 0.5, 0.5),
    ])
    def test_subtract_floats(self, calculator, a, b, expected):
        """Test subtraction of floating point numbers."""
        result = calculator.subtract(a, b)
        assert result == expected

    def test_subtract_mixed_int_float(self, calculator):
        """Test subtraction with mixed integer and float."""
        result = calculator.subtract(5, 2.5)
        assert result == 2.5

    def test_subtract_very_large_numbers(self, calculator):
        """Test subtraction with very large numbers."""
        result = calculator.subtract(10**15, 10**15)
        assert result == 0

    def test_subtract_very_small_numbers(self, calculator):
        """Test subtraction with very small numbers."""
        result = calculator.subtract(3e-10, 1e-10)
        assert result == pytest.approx(2e-10)

    def test_subtract_results_in_negative(self, calculator):
        """Test subtraction that produces a negative result."""
        result = calculator.subtract(3, 10)
        assert result == -7

    def test_subtract_float_precision(self, calculator):
        """Test subtraction with floating point precision."""
        result = calculator.subtract(0.3, 0.2)
        assert result == pytest.approx(0.1)

    # Edge Cases: Type Handling
    @pytest.mark.parametrize("invalid_input", ["string", [], {}, None, (1, 2)])
    def test_subtract_invalid_first_operand(self, calculator, invalid_input):
        """Test subtraction with invalid first operand type raises TypeError."""
        with pytest.raises(TypeError):
            calculator.subtract(invalid_input, 5)

    @pytest.mark.parametrize("invalid_input", ["string", [], {}, None, (1, 2)])
    def test_subtract_invalid_second_operand(self, calculator, invalid_input):
        """Test subtraction with invalid second operand type raises TypeError."""
        with pytest.raises(TypeError):
            calculator.subtract(5, invalid_input)


class TestMultiply:
    """Test suite for Calculator.multiply() method."""

    @pytest.fixture
    def calculator(self):
        """Fixture providing a Calculator instance for each test."""
        return Calculator()

    # Happy Path Tests
    @pytest.mark.parametrize("a,b,expected", [
        (3, 4, 12),
        (0, 5, 0),
        (1, 5, 5),
        (2, 3, 6),
    ])
    def test_multiply_positive_integers(self, calculator, a, b, expected):
        """Test multiplication of positive integers."""
        result = calculator.multiply(a, b)
        assert result == expected

    def test_multiply_negative_numbers(self, calculator):
        """Test multiplication with negative numbers."""
        result = calculator.multiply(-3, 4)
        assert result == -12

    def test_multiply_both_negative(self, calculator):
        """Test multiplication of two negative numbers."""
        result = calculator.multiply(-3, -4)
        assert result == 12

    def test_multiply_zero_operand(self, calculator):
        """Test multiplication with zero operand."""
        result = calculator.multiply(5, 0)
        assert result == 0

    def test_multiply_one_operand(self, calculator):
        """Test multiplication with one as operand (identity)."""
        result = calculator.multiply(5, 1)
        assert result == 5

    @pytest.mark.parametrize("a,b,expected", [
        (1.5, 2.0, 3.0),
        (2.5, 4.0, 10.0),
        (0.5, 2.0, 1.0),
    ])
    def test_multiply_floats(self, calculator, a, b, expected):
        """Test multiplication of floating point numbers."""
        result = calculator.multiply(a, b)
        assert result == expected

    def test_multiply_mixed_int_float(self, calculator):
        """Test multiplication with mixed integer and float."""
        result = calculator.multiply(3, 1.5)
        assert result == 4.5

    def test_multiply_very_large_numbers(self, calculator):
        """Test multiplication with very large numbers."""
        result = calculator.multiply(10**10, 10**10)
        assert result == 10**20

    def test_multiply_very_small_numbers(self, calculator):
        """Test multiplication with very small numbers."""
        result = calculator.multiply(1e-10, 1e-10)
        assert result == pytest.approx(1e-20)

    def test_multiply_fractional_result(self, calculator):
        """Test multiplication that produces a fractional result."""
        result = calculator.multiply(0.5, 0.5)
        assert result == 0.25

    def test_multiply_float_precision(self, calculator):
        """Test multiplication with floating point precision."""
        result = calculator.multiply(0.1, 3)
        assert result == pytest.approx(0.3)

    # Edge Cases: Type Handling
    @pytest.mark.parametrize("invalid_input", [{}, None])
    def test_multiply_invalid_first_operand(self, calculator, invalid_input):
        """Test multiplication with invalid first operand type raises TypeError."""
        with pytest.raises(TypeError):
            calculator.multiply(invalid_input, 5)

    @pytest.mark.parametrize("invalid_input", [{}, None])
    def test_multiply_invalid_second_operand(self, calculator, invalid_input):
        """Test multiplication with invalid second operand type raises TypeError."""
        with pytest.raises(TypeError):
            calculator.multiply(5, invalid_input)


class TestCalculatorHistoryIntegration:
    """Test suite for Calculator integration with CalculatorSession and history."""

    @pytest.fixture
    def session(self):
        """Fixture providing a fresh CalculatorSession."""
        from src.session import CalculatorSession
        return CalculatorSession()

    def test_session_add_records_to_history(self, session):
        """Test that add operation via session records to history."""
        calc = session.get_calculator()
        result = calc.add(2, 3)
        assert result == 5
        entries = session.get_history()
        assert len(entries) == 1
        assert entries[0] == "add(2, 3) = 5"

    def test_session_multiply_records_to_history(self, session):
        """Test that multiply operation via session records to history."""
        calc = session.get_calculator()
        result = calc.multiply(4, 5)
        assert result == 20
        entries = session.get_history()
        assert len(entries) == 1
        assert entries[0] == "multiply(4, 5) = 20"

    def test_session_unary_records_to_history(self, session):
        """Test that unary operation (square) via session records to history."""
        calc = session.get_calculator()
        result = calc.square(5)
        assert result == 25.0
        entries = session.get_history()
        assert len(entries) == 1
        assert entries[0] == "square(5) = 25"

    def test_session_history_accumulates(self, session):
        """Test that multiple operations accumulate in session history."""
        calc = session.get_calculator()
        calc.add(1, 1)
        calc.multiply(2, 2)
        calc.subtract(10, 3)
        entries = session.get_history()
        assert len(entries) == 3
        assert entries[0] == "add(1, 1) = 2"
        assert entries[1] == "multiply(2, 2) = 4"
        assert entries[2] == "subtract(10, 3) = 7"

    def test_session_fresh_on_new_session(self):
        """Test that two sessions don't share history."""
        from src.session import CalculatorSession
        session1 = CalculatorSession()
        session2 = CalculatorSession()

        calc1 = session1.get_calculator()
        calc1.add(1, 1)

        # session2 should have empty history
        assert len(session2.get_history()) == 0
        assert len(session1.get_history()) == 1

    def test_session_divide_records_with_float_result(self, session):
        """Test that divide operation records float results correctly."""
        calc = session.get_calculator()
        result = calc.divide(7, 2)
        assert result == 3.5
        entries = session.get_history()
        assert entries[0] == "divide(7, 2) = 3.5"

    def test_session_factorial_records(self, session):
        """Test that factorial operation records to history."""
        calc = session.get_calculator()
        result = calc.factorial(5)
        assert result == 120
        entries = session.get_history()
        assert entries[0] == "factorial(5) = 120"

    def test_session_power_records(self, session):
        """Test that power operation records to history."""
        calc = session.get_calculator()
        result = calc.power(2, 8)
        assert result == 256.0
        entries = session.get_history()
        assert entries[0] == "power(2, 8) = 256"