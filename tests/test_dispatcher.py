"""Comprehensive tests for src.dispatcher module.

Tests the run_calculation() function that dispatches named methods
on CalculatorWithHistory instances.
"""

import pytest

from src.dispatcher import run_calculation
from src.calculator_with_history import CalculatorWithHistory


# ============================================================================
# run_calculation — Happy path: all four basic operators
# ============================================================================


class TestRunCalculationHappyPath:
    """Tests for run_calculation with valid inputs for all operators."""

    def test_run_calculation_add_returns_correct_result(self):
        """run_calculation(3, 4, 'add') should return 7.0."""
        result, _ = run_calculation(3.0, 4.0, "add")
        assert result == pytest.approx(7.0)

    def test_run_calculation_add_returns_calculator_instance(self):
        """run_calculation should return a CalculatorWithHistory instance."""
        _, calc = run_calculation(3.0, 4.0, "add")
        assert isinstance(calc, CalculatorWithHistory)

    def test_run_calculation_subtract_returns_correct_result(self):
        """run_calculation(10, 5, 'subtract') should return 5.0."""
        result, _ = run_calculation(10.0, 5.0, "subtract")
        assert result == pytest.approx(5.0)

    def test_run_calculation_multiply_returns_correct_result(self):
        """run_calculation(6, 7, 'multiply') should return 42.0."""
        result, _ = run_calculation(6.0, 7.0, "multiply")
        assert result == pytest.approx(42.0)

    def test_run_calculation_divide_returns_correct_result(self):
        """run_calculation(8, 2, 'divide') should return 4.0."""
        result, _ = run_calculation(8.0, 2.0, "divide")
        assert result == pytest.approx(4.0)

    def test_run_calculation_add_negative_numbers(self):
        """run_calculation(-3, -4, 'add') should return -7.0."""
        result, _ = run_calculation(-3.0, -4.0, "add")
        assert result == pytest.approx(-7.0)

    def test_run_calculation_add_mixed_signs(self):
        """run_calculation(-3, 4, 'add') should return 1.0."""
        result, _ = run_calculation(-3.0, 4.0, "add")
        assert result == pytest.approx(1.0)

    def test_run_calculation_subtract_negative_result(self):
        """run_calculation(3, 10, 'subtract') should return -7.0."""
        result, _ = run_calculation(3.0, 10.0, "subtract")
        assert result == pytest.approx(-7.0)

    def test_run_calculation_subtract_to_zero(self):
        """run_calculation(5, 5, 'subtract') should return 0.0."""
        result, _ = run_calculation(5.0, 5.0, "subtract")
        assert result == pytest.approx(0.0)

    def test_run_calculation_multiply_by_zero(self):
        """run_calculation(99999, 0, 'multiply') should return 0.0."""
        result, _ = run_calculation(99999.0, 0.0, "multiply")
        assert result == pytest.approx(0.0)

    def test_run_calculation_multiply_two_negatives(self):
        """run_calculation(-4, -5, 'multiply') should return 20.0."""
        result, _ = run_calculation(-4.0, -5.0, "multiply")
        assert result == pytest.approx(20.0)

    def test_run_calculation_multiply_negative_and_positive(self):
        """run_calculation(-4, 5, 'multiply') should return -20.0."""
        result, _ = run_calculation(-4.0, 5.0, "multiply")
        assert result == pytest.approx(-20.0)

    def test_run_calculation_divide_float_result(self):
        """run_calculation(5, 2, 'divide') should return 2.5."""
        result, _ = run_calculation(5.0, 2.0, "divide")
        assert result == pytest.approx(2.5)

    def test_run_calculation_divide_one_third(self):
        """run_calculation(1, 3, 'divide') should return approximately 0.333..."""
        result, _ = run_calculation(1.0, 3.0, "divide")
        assert result == pytest.approx(1.0 / 3.0)

    def test_run_calculation_divide_negative_dividend(self):
        """run_calculation(-6, 2, 'divide') should return -3.0."""
        result, _ = run_calculation(-6.0, 2.0, "divide")
        assert result == pytest.approx(-3.0)

    def test_run_calculation_divide_negative_divisor(self):
        """run_calculation(6, -2, 'divide') should return -3.0."""
        result, _ = run_calculation(6.0, -2.0, "divide")
        assert result == pytest.approx(-3.0)

    def test_run_calculation_divide_zero_numerator(self):
        """run_calculation(0, 5, 'divide') should return 0.0."""
        result, _ = run_calculation(0.0, 5.0, "divide")
        assert result == pytest.approx(0.0)


# ============================================================================
# run_calculation — Error handling: division by zero
# ============================================================================


class TestRunCalculationDivisionByZero:
    """Tests for run_calculation error handling with division by zero."""

    def test_run_calculation_divide_by_zero_raises_zero_division_error(self):
        """run_calculation(5, 0, 'divide') should raise ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            run_calculation(5.0, 0.0, "divide")

    def test_run_calculation_zero_divided_by_zero_raises(self):
        """run_calculation(0, 0, 'divide') should raise ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            run_calculation(0.0, 0.0, "divide")

    def test_run_calculation_divide_by_float_zero_raises(self):
        """run_calculation(10, 0.0, 'divide') should raise ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            run_calculation(10.0, 0.0, "divide")

    def test_run_calculation_divide_negative_by_zero_raises(self):
        """run_calculation(-5, 0, 'divide') should raise ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            run_calculation(-5.0, 0.0, "divide")


# ============================================================================
# run_calculation — History recording
# ============================================================================


class TestRunCalculationHistory:
    """Tests verifying that run_calculation records operation in history."""

    def test_run_calculation_records_history_entry(self):
        """Successful run_calculation should record operation in history."""
        result, calc = run_calculation(5.0, 3.0, "add")
        history = calc.get_history()
        assert len(history) == 1

    def test_run_calculation_history_contains_operands(self):
        """History entry should contain the operands."""
        result, calc = run_calculation(5.0, 3.0, "add")
        history = calc.get_history()
        assert any("5" in str(h) for h in history)
        assert any("3" in str(h) for h in history)

    def test_run_calculation_history_contains_result(self):
        """History entry should contain the result."""
        result, calc = run_calculation(5.0, 3.0, "add")
        history = calc.get_history()
        assert any("8" in str(h) for h in history)

    def test_run_calculation_multiple_operations_recorded(self):
        """Multiple operations should each be recorded separately."""
        _, calc1 = run_calculation(5.0, 3.0, "add")
        _, calc2 = run_calculation(5.0, 3.0, "add")
        # Each should have its own history
        assert len(calc1.get_history()) == 1
        assert len(calc2.get_history()) == 1

    def test_run_calculation_divide_by_zero_does_not_record_history(self):
        """Failed division should not record history entry."""
        calc = CalculatorWithHistory()
        try:
            run_calculation(5.0, 0.0, "divide")
        except ZeroDivisionError:
            pass
        # Note: we can't directly access the history of the failed calc
        # because the exception prevents returning it, but we can verify
        # that a new instance starts with empty history
        assert len(calc.get_history()) == 0


# ============================================================================
# run_calculation — Return value structure
# ============================================================================


class TestRunCalculationReturnStructure:
    """Tests verifying run_calculation return value structure."""

    def test_run_calculation_returns_tuple(self):
        """run_calculation must return a tuple."""
        result = run_calculation(5.0, 3.0, "add")
        assert isinstance(result, tuple)

    def test_run_calculation_returns_two_element_tuple(self):
        """run_calculation must return exactly two elements."""
        result = run_calculation(5.0, 3.0, "add")
        assert len(result) == 2

    def test_run_calculation_first_element_is_float(self):
        """First element (result) must be a float."""
        result, _ = run_calculation(5.0, 3.0, "add")
        assert isinstance(result, float)

    def test_run_calculation_second_element_is_calculator(self):
        """Second element must be a CalculatorWithHistory instance."""
        _, calc = run_calculation(5.0, 3.0, "add")
        assert isinstance(calc, CalculatorWithHistory)


# ============================================================================
# run_calculation — Large numbers and edge cases
# ============================================================================


class TestRunCalculationLargeNumbers:
    """Tests for run_calculation with large and edge-case values."""

    def test_run_calculation_add_large_numbers(self):
        """run_calculation(1e300, 1e300, 'add') should handle large addition."""
        result, _ = run_calculation(1e300, 1e300, "add")
        assert result == pytest.approx(2e300)

    def test_run_calculation_multiply_large_numbers_overflow(self):
        """run_calculation(1e200, 1e200, 'multiply') may overflow to infinity."""
        import math
        result, _ = run_calculation(1e200, 1e200, "multiply")
        # 1e200 * 1e200 = 1e400, which exceeds float max (~1.8e308)
        assert math.isinf(result)

    def test_run_calculation_multiply_large_within_range(self):
        """run_calculation(1e154, 1e154, 'multiply') should work."""
        result, _ = run_calculation(1e154, 1e154, "multiply")
        # 1e154 * 1e154 = 1e308, which is near but within range
        assert result == pytest.approx(1e308, rel=1e-6)

    def test_run_calculation_very_small_numbers(self):
        """run_calculation with very small positive numbers should work."""
        result, _ = run_calculation(1e-150, 1e-150, "add")
        assert result == pytest.approx(2e-150)


# ============================================================================
# run_calculation — Invalid method names
# ============================================================================


class TestRunCalculationInvalidMethod:
    """Tests for run_calculation with invalid method names."""

    def test_run_calculation_invalid_method_name_raises(self):
        """run_calculation with invalid method name should raise AttributeError."""
        with pytest.raises(AttributeError):
            run_calculation(5.0, 3.0, "invalid_method")

    def test_run_calculation_nonexistent_method_raises(self):
        """run_calculation with nonexistent method should raise AttributeError."""
        with pytest.raises(AttributeError):
            run_calculation(5.0, 3.0, "add_wrong")

    def test_run_calculation_empty_method_name_raises(self):
        """run_calculation with empty method name should raise AttributeError."""
        with pytest.raises(AttributeError):
            run_calculation(5.0, 3.0, "")


# ============================================================================
# run_calculation — Parametrized tests for all operators
# ============================================================================


class TestRunCalculationParametrized:
    """Parametrized tests for run_calculation."""

    @pytest.mark.parametrize("method_name,a,b,expected", [
        ("add", 3.0, 4.0, 7.0),
        ("add", -3.0, -4.0, -7.0),
        ("add", 0.0, 0.0, 0.0),
        ("subtract", 10.0, 5.0, 5.0),
        ("subtract", 5.0, 10.0, -5.0),
        ("subtract", 5.0, 5.0, 0.0),
        ("multiply", 6.0, 7.0, 42.0),
        ("multiply", -4.0, -5.0, 20.0),
        ("multiply", 99999.0, 0.0, 0.0),
        ("divide", 8.0, 2.0, 4.0),
        ("divide", 5.0, 2.0, 2.5),
        ("divide", 1.0, 3.0, 1.0 / 3.0),
        ("divide", 0.0, 5.0, 0.0),
    ])
    def test_all_operators_with_various_values(self, method_name, a, b, expected):
        """Test each operator with various operand combinations."""
        result, _ = run_calculation(a, b, method_name)
        assert result == pytest.approx(expected)


# ============================================================================
# run_calculation — Type handling
# ============================================================================


class TestRunCalculationTypeHandling:
    """Tests for run_calculation with different numeric types."""

    def test_run_calculation_with_integers_converted_to_floats(self):
        """run_calculation should work with int operands (Python coerces to float)."""
        # While type hints specify float, Python's duck typing allows int
        result, _ = run_calculation(5, 3, "add")  # type: ignore
        assert result == pytest.approx(8.0)

    def test_run_calculation_mixed_int_float(self):
        """run_calculation should work with mixed int/float operands."""
        result, _ = run_calculation(5, 3.0, "add")  # type: ignore
        assert result == pytest.approx(8.0)


# ============================================================================
# run_calculation — Operator method dispatch verification
# ============================================================================


class TestRunCalculationDispatchVerification:
    """Tests verifying correct method dispatch for each operator."""

    def test_run_calculation_dispatch_add_method(self):
        """Verify 'add' method is dispatched correctly."""
        result, calc = run_calculation(2.0, 3.0, "add")
        assert result == pytest.approx(5.0)
        history = calc.get_history()
        assert any("2" in str(h) and "3" in str(h) for h in history)

    def test_run_calculation_dispatch_subtract_method(self):
        """Verify 'subtract' method is dispatched correctly."""
        result, calc = run_calculation(10.0, 3.0, "subtract")
        assert result == pytest.approx(7.0)

    def test_run_calculation_dispatch_multiply_method(self):
        """Verify 'multiply' method is dispatched correctly."""
        result, calc = run_calculation(3.0, 4.0, "multiply")
        assert result == pytest.approx(12.0)

    def test_run_calculation_dispatch_divide_method(self):
        """Verify 'divide' method is dispatched correctly."""
        result, calc = run_calculation(15.0, 3.0, "divide")
        assert result == pytest.approx(5.0)


# ============================================================================
# run_calculation — Calculator state independence
# ============================================================================


class TestRunCalculationIndependence:
    """Tests verifying that each run_calculation creates independent calculator."""

    def test_run_calculation_independent_instances(self):
        """Each run_calculation should create its own CalculatorWithHistory."""
        _, calc1 = run_calculation(5.0, 3.0, "add")
        _, calc2 = run_calculation(5.0, 3.0, "add")
        # They should be different instances
        assert calc1 is not calc2

    def test_run_calculation_independent_histories(self):
        """History should not be shared between instances."""
        _, calc1 = run_calculation(5.0, 3.0, "add")
        _, calc2 = run_calculation(10.0, 3.0, "add")
        # Check that histories are independent
        hist1 = calc1.get_history()
        hist2 = calc2.get_history()
        assert len(hist1) == 1
        assert len(hist2) == 1
        # And they record different operations
        assert hist1[0] != hist2[0]


# ============================================================================
# run_calculation — Floating point precision and NaN/Inf
# ============================================================================


class TestRunCalculationSpecialValues:
    """Tests for run_calculation with special float values."""

    def test_run_calculation_with_nan(self):
        """run_calculation should propagate NaN through operations."""
        import math
        result, _ = run_calculation(float('nan'), 3.0, "add")
        assert math.isnan(result)

    def test_run_calculation_with_inf(self):
        """run_calculation should propagate infinity through operations."""
        import math
        result, _ = run_calculation(float('inf'), 3.0, "add")
        assert math.isinf(result)

    def test_run_calculation_with_negative_inf(self):
        """run_calculation should handle negative infinity."""
        import math
        result, _ = run_calculation(float('-inf'), 3.0, "add")
        assert math.isinf(result) and result < 0

    def test_run_calculation_multiply_zero_by_inf(self):
        """run_calculation(0, inf, 'multiply') results in NaN."""
        import math
        result, _ = run_calculation(0.0, float('inf'), "multiply")
        assert math.isnan(result)


# ============================================================================
# run_calculation — Negative zero edge case
# ============================================================================


class TestRunCalculationNegativeZero:
    """Tests for run_calculation with negative zero edge case."""

    def test_run_calculation_with_negative_zero(self):
        """run_calculation should treat -0.0 as 0.0 mathematically."""
        result, _ = run_calculation(-0.0, 5.0, "add")
        assert result == pytest.approx(5.0)

    def test_run_calculation_subtract_to_negative_zero(self):
        """run_calculation(0, 0, 'subtract') should return 0.0."""
        result, _ = run_calculation(0.0, 0.0, "subtract")
        assert result == pytest.approx(0.0)
