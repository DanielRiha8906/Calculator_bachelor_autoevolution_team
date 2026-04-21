import pytest
import math
from src.calculator import Calculator


class TestDivideHappyPath:
    """Test divide method with valid numeric inputs."""

    def test_divide_positive_numbers(self):
        """Test division of two positive numbers."""
        calc = Calculator()
        result = calc.divide(10, 2)
        assert result == 5

    def test_divide_negative_dividend(self):
        """Test division with negative dividend."""
        calc = Calculator()
        result = calc.divide(-10, 2)
        assert result == -5

    def test_divide_negative_divisor(self):
        """Test division with negative divisor."""
        calc = Calculator()
        result = calc.divide(10, -2)
        assert result == -5

    def test_divide_both_negative(self):
        """Test division with both operands negative."""
        calc = Calculator()
        result = calc.divide(-10, -2)
        assert result == 5

    def test_divide_floats(self):
        """Test division of float numbers."""
        calc = Calculator()
        result = calc.divide(7.5, 2.5)
        assert result == 3.0

    def test_divide_mixed_int_float(self):
        """Test division with mixed integer and float."""
        calc = Calculator()
        result = calc.divide(10, 2.5)
        assert result == 4.0

    def test_divide_result_in_fraction(self):
        """Test division resulting in fractional value."""
        calc = Calculator()
        result = calc.divide(10, 3)
        assert abs(result - 3.3333333333) < 1e-9

    def test_divide_small_numbers(self):
        """Test division of very small numbers."""
        calc = Calculator()
        result = calc.divide(0.001, 0.0001)
        assert abs(result - 10) < 1e-9

    def test_divide_zero_dividend(self):
        """Test division when dividend is zero."""
        calc = Calculator()
        result = calc.divide(0, 5)
        assert result == 0


class TestDivideByZero:
    """Test divide method with zero divisor."""

    def test_divide_by_zero_int(self):
        """Test division by integer zero raises ZeroDivisionError."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(10, 0)

    def test_divide_by_zero_float(self):
        """Test division by float zero also raises ZeroDivisionError in Python 3.12."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(10, 0.0)

    def test_divide_negative_by_zero_float(self):
        """Test division of negative number by float zero raises ZeroDivisionError."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(-10, 0.0)

    def test_divide_zero_by_zero_float(self):
        """Test division of zero by float zero raises ZeroDivisionError."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(0, 0.0)

    def test_divide_zero_by_zero_int(self):
        """Test division of zero by integer zero raises ZeroDivisionError."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(0, 0)


class TestDivideTypeErrors:
    """Test divide method with non-numeric inputs."""

    def test_divide_string_dividend(self):
        """Test division with non-numeric dividend raises TypeError."""
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.divide("a", 2)

    def test_divide_string_divisor(self):
        """Test division with non-numeric divisor raises TypeError."""
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.divide(2, "b")

    def test_divide_both_strings(self):
        """Test division with both arguments as strings raises TypeError."""
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.divide("10", "2")

    def test_divide_none_dividend(self):
        """Test division with None as dividend raises TypeError."""
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.divide(None, 2)

    def test_divide_none_divisor(self):
        """Test division with None as divisor raises TypeError."""
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.divide(10, None)

    def test_divide_both_none(self):
        """Test division with both arguments as None raises TypeError."""
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.divide(None, None)

    def test_divide_list_dividend(self):
        """Test division with list as dividend raises TypeError."""
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.divide([1, 2], 2)

    def test_divide_list_divisor(self):
        """Test division with list as divisor raises TypeError."""
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.divide(10, [2])

    def test_divide_dict_dividend(self):
        """Test division with dict as dividend raises TypeError."""
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.divide({"value": 10}, 2)

    def test_divide_dict_divisor(self):
        """Test division with dict as divisor raises TypeError."""
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.divide(10, {"value": 2})

    def test_divide_tuple_dividend(self):
        """Test division with tuple as dividend raises TypeError."""
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.divide((10,), 2)

    def test_divide_tuple_divisor(self):
        """Test division with tuple as divisor raises TypeError."""
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.divide(10, (2,))

    def test_divide_bool_dividend(self):
        """Test division with bool as dividend (valid in Python: True=1, False=0)."""
        calc = Calculator()
        result = calc.divide(True, 2)
        assert result == 0.5

    def test_divide_bool_divisor(self):
        """Test division with bool as divisor (valid in Python: True=1, False=0)."""
        calc = Calculator()
        result = calc.divide(10, True)
        assert result == 10


class TestDivideEdgeCases:
    """Test divide method with edge case numeric inputs."""

    def test_divide_very_large_numbers(self):
        """Test division with very large numbers."""
        calc = Calculator()
        result = calc.divide(10**100, 10**50)
        # Use approximate comparison due to floating-point precision
        assert abs(result - 10**50) < 1e40

    def test_divide_very_small_numbers(self):
        """Test division with very small numbers."""
        calc = Calculator()
        result = calc.divide(1e-100, 1e-50)
        assert result == 1e-50

    def test_divide_infinity(self):
        """Test division with infinity as dividend."""
        calc = Calculator()
        result = calc.divide(float('inf'), 2)
        assert math.isinf(result)

    def test_divide_by_infinity(self):
        """Test division by infinity."""
        calc = Calculator()
        result = calc.divide(10, float('inf'))
        assert result == 0.0

    def test_divide_nan(self):
        """Test division with NaN."""
        calc = Calculator()
        result = calc.divide(float('nan'), 2)
        assert math.isnan(result)

    def test_divide_by_nan(self):
        """Test division by NaN."""
        calc = Calculator()
        result = calc.divide(10, float('nan'))
        assert math.isnan(result)

    def test_divide_negative_infinity(self):
        """Test division with negative infinity."""
        calc = Calculator()
        result = calc.divide(float('-inf'), 2)
        assert math.isinf(result) and result < 0

    def test_divide_by_negative_infinity(self):
        """Test division by negative infinity."""
        calc = Calculator()
        result = calc.divide(10, float('-inf'))
        assert result == 0.0

    def test_divide_one(self):
        """Test division by one."""
        calc = Calculator()
        result = calc.divide(42, 1)
        assert result == 42

    def test_divide_number_by_itself(self):
        """Test division of a number by itself."""
        calc = Calculator()
        result = calc.divide(7, 7)
        assert result == 1

    def test_divide_negative_one(self):
        """Test division by negative one."""
        calc = Calculator()
        result = calc.divide(42, -1)
        assert result == -42


class TestDivideParametrized:
    """Test divide with parametrized inputs for concise coverage."""

    @pytest.mark.parametrize("dividend,divisor,expected", [
        (6, 2, 3),
        (8, 4, 2),
        (100, 10, 10),
        (5, 5, 1),
        (-6, 2, -3),
        (6, -2, -3),
        (-6, -2, 3),
    ])
    def test_divide_valid_integers(self, dividend, divisor, expected):
        """Test division with various valid integer pairs."""
        calc = Calculator()
        result = calc.divide(dividend, divisor)
        assert result == expected

    @pytest.mark.parametrize("dividend,divisor", [
        (10, "2"),
        ("10", 2),
        ("10", "2"),
        (10, None),
        (None, 2),
        (None, None),
        (10, [2]),
        ([10], 2),
        (10, {}),
        ({}, 2),
    ])
    def test_divide_invalid_types(self, dividend, divisor):
        """Test division with invalid type combinations."""
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.divide(dividend, divisor)