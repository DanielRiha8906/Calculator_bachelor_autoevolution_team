import pytest
import math
from src.calculator import Calculator


class TestDivide:
    """Test suite for Calculator.divide() method."""

    @pytest.fixture
    def calculator(self):
        """Provide a Calculator instance for each test."""
        return Calculator()

    # ========== Happy Path / Normal Division ==========

    def test_divide_positive_integers(self, calculator):
        """Test division of positive integers returns correct quotient."""
        result = calculator.divide(10, 2)
        assert result == 5.0

    def test_divide_positive_floats(self, calculator):
        """Test division of positive floats returns correct quotient."""
        result = calculator.divide(10.5, 2.5)
        assert abs(result - 4.2) < 1e-9

    def test_divide_mixed_int_and_float(self, calculator):
        """Test division with mixed int and float types."""
        result = calculator.divide(10, 2.5)
        assert result == 4.0

    def test_divide_float_int(self, calculator):
        """Test division of float by int."""
        result = calculator.divide(10.0, 2)
        assert result == 5.0

    def test_divide_large_numbers(self, calculator):
        """Test division of very large numbers."""
        result = calculator.divide(1e10, 1e5)
        assert result == 1e5

    def test_divide_small_numbers(self, calculator):
        """Test division of very small numbers."""
        result = calculator.divide(1e-10, 1e-5)
        assert abs(result - 1e-5) < 1e-15

    def test_divide_negative_numbers(self, calculator):
        """Test division with negative numbers."""
        result = calculator.divide(-10, 2)
        assert result == -5.0

    def test_divide_both_negative(self, calculator):
        """Test division where both operands are negative."""
        result = calculator.divide(-10, -2)
        assert result == 5.0

    def test_divide_result_is_one(self, calculator):
        """Test division where dividend equals divisor."""
        result = calculator.divide(5, 5)
        assert result == 1.0

    def test_divide_result_less_than_one(self, calculator):
        """Test division where result is less than 1."""
        result = calculator.divide(1, 5)
        assert result == 0.2

    # ========== Zero Divisor - Exception Handling ==========

    def test_divide_by_integer_zero(self, calculator):
        """Test that dividing by integer zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(5, 0)

    def test_divide_by_float_zero(self, calculator):
        """Test that dividing by float zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(5, 0.0)

    def test_divide_zero_by_integer_zero(self, calculator):
        """Test that zero divided by integer zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(0, 0)

    def test_divide_zero_by_float_zero(self, calculator):
        """Test that zero divided by float zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(0, 0.0)

    def test_divide_large_number_by_zero(self, calculator):
        """Test that dividing a large number by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(1e10, 0)

    def test_divide_negative_by_zero(self, calculator):
        """Test that dividing a negative number by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(-5, 0)

    # ========== Non-Numeric String Inputs - TypeError ==========

    def test_divide_string_dividend_int_divisor(self, calculator):
        """Test that string dividend raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide("10", 5)

    def test_divide_int_dividend_string_divisor(self, calculator):
        """Test that string divisor raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(10, "5")

    def test_divide_both_string_operands(self, calculator):
        """Test that string operands raise TypeError."""
        with pytest.raises(TypeError):
            calculator.divide("10", "5")

    def test_divide_empty_string_dividend(self, calculator):
        """Test that empty string dividend raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide("", 5)

    def test_divide_empty_string_divisor(self, calculator):
        """Test that empty string divisor raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(5, "")

    def test_divide_numeric_string_dividend(self, calculator):
        """Test that numeric string dividend raises TypeError (not auto-converted)."""
        with pytest.raises(TypeError):
            calculator.divide("10.5", 2)

    def test_divide_whitespace_string_divisor(self, calculator):
        """Test that whitespace string divisor raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(10, "  ")

    # ========== None Inputs - TypeError ==========

    def test_divide_none_dividend(self, calculator):
        """Test that None dividend raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(None, 5)

    def test_divide_none_divisor(self, calculator):
        """Test that None divisor raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(10, None)

    def test_divide_both_none(self, calculator):
        """Test that both operands being None raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(None, None)

    # ========== Collection Inputs (List, Dict, Tuple, Set) - TypeError ==========

    def test_divide_list_dividend(self, calculator):
        """Test that list dividend raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide([1, 2], 5)

    def test_divide_list_divisor(self, calculator):
        """Test that list divisor raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(10, [5])

    def test_divide_dict_dividend(self, calculator):
        """Test that dict dividend raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide({"a": 10}, 5)

    def test_divide_dict_divisor(self, calculator):
        """Test that dict divisor raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(10, {"a": 5})

    def test_divide_tuple_dividend(self, calculator):
        """Test that tuple dividend raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide((10,), 5)

    def test_divide_tuple_divisor(self, calculator):
        """Test that tuple divisor raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(10, (5,))

    def test_divide_set_dividend(self, calculator):
        """Test that set dividend raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide({10}, 5)

    def test_divide_set_divisor(self, calculator):
        """Test that set divisor raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(10, {5})

    def test_divide_empty_list_dividend(self, calculator):
        """Test that empty list dividend raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide([], 5)

    def test_divide_empty_dict_dividend(self, calculator):
        """Test that empty dict dividend raises TypeError."""
        with pytest.raises(TypeError):
            calculator.divide({}, 5)

    # ========== Custom Object Inputs - TypeError ==========

    def test_divide_custom_object_dividend(self, calculator):
        """Test that custom object dividend raises TypeError."""
        class CustomObj:
            pass
        with pytest.raises(TypeError):
            calculator.divide(CustomObj(), 5)

    def test_divide_custom_object_divisor(self, calculator):
        """Test that custom object divisor raises TypeError."""
        class CustomObj:
            pass
        with pytest.raises(TypeError):
            calculator.divide(10, CustomObj())

    def test_divide_boolean_dividend(self, calculator):
        """Test division with boolean dividend (bool is int subclass, should work)."""
        # Note: In Python, bool is a subclass of int, so True==1, False==0
        result = calculator.divide(True, 1)
        assert result == 1.0

    def test_divide_boolean_divisor(self, calculator):
        """Test division with boolean divisor (bool is int subclass, should work)."""
        result = calculator.divide(10, True)
        assert result == 10.0

    # ========== Edge Cases with Infinity and NaN ==========

    def test_divide_by_positive_infinity(self, calculator):
        """Test dividing by positive infinity returns zero."""
        result = calculator.divide(10, float('inf'))
        assert result == 0.0

    def test_divide_by_negative_infinity(self, calculator):
        """Test dividing by negative infinity returns negative zero."""
        result = calculator.divide(10, float('-inf'))
        assert result == 0.0

    def test_divide_infinity_by_number(self, calculator):
        """Test dividing infinity by a number returns infinity."""
        result = calculator.divide(float('inf'), 2)
        assert result == float('inf')

    def test_divide_negative_infinity_by_number(self, calculator):
        """Test dividing negative infinity by a number returns negative infinity."""
        result = calculator.divide(float('-inf'), 2)
        assert result == float('-inf')

    def test_divide_infinity_by_infinity(self, calculator):
        """Test dividing infinity by infinity returns NaN."""
        result = calculator.divide(float('inf'), float('inf'))
        assert math.isnan(result)

    def test_divide_by_nan(self, calculator):
        """Test dividing by NaN returns NaN."""
        result = calculator.divide(10, float('nan'))
        assert math.isnan(result)

    def test_divide_nan_by_number(self, calculator):
        """Test dividing NaN by a number returns NaN."""
        result = calculator.divide(float('nan'), 2)
        assert math.isnan(result)

    # ========== Parametrized Tests for Better DRY Coverage ==========

    @pytest.mark.parametrize("dividend,divisor,expected", [
        (10, 2, 5.0),
        (15, 3, 5.0),
        (100, 10, 10.0),
        (-20, 4, -5.0),
        (20, -4, -5.0),
        (-20, -4, 5.0),
        (0, 5, 0.0),
        (1, 1, 1.0),
        (0.5, 0.5, 1.0),
    ])
    def test_divide_valid_inputs(self, calculator, dividend, divisor, expected):
        """Parametrized test for valid division inputs."""
        result = calculator.divide(dividend, divisor)
        assert abs(result - expected) < 1e-9

    @pytest.mark.parametrize("dividend,divisor", [
        (5, 0),
        (5, 0.0),
        (0, 0),
        (-10, 0),
        (1e10, 0),
    ])
    def test_divide_by_zero_parametrized(self, calculator, dividend, divisor):
        """Parametrized test for division by zero."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(dividend, divisor)

    @pytest.mark.parametrize("dividend,divisor", [
        ("10", 5),
        (10, "5"),
        ("10", "5"),
        ("", 5),
        (5, ""),
    ])
    def test_divide_string_inputs_parametrized(self, calculator, dividend, divisor):
        """Parametrized test for string inputs raising TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(dividend, divisor)

    @pytest.mark.parametrize("dividend,divisor", [
        (None, 5),
        (10, None),
        (None, None),
    ])
    def test_divide_none_inputs_parametrized(self, calculator, dividend, divisor):
        """Parametrized test for None inputs raising TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(dividend, divisor)

    @pytest.mark.parametrize("dividend,divisor", [
        ([1, 2], 5),
        (10, [5]),
        ({"a": 10}, 5),
        (10, {"a": 5}),
        ((10,), 5),
        (10, (5,)),
    ])
    def test_divide_collection_inputs_parametrized(self, calculator, dividend, divisor):
        """Parametrized test for collection inputs raising TypeError."""
        with pytest.raises(TypeError):
            calculator.divide(dividend, divisor)