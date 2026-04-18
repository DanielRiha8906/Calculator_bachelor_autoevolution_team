"""Comprehensive tests for CalculatorWithHistory wrapper and history recording.

Tests cover:
- History recording for all operation types (binary and unary)
- Entry formatting
- History isolation (get_history returns a copy)
- Failed operations are not recorded
- History ordering
- Empty history before any operations
- Edge cases for each operation type
"""

import pytest
import math

from src.calculator_with_history import CalculatorWithHistory


# ===========================================================================
# Initialization and history state
# ===========================================================================

class TestInitialization:
    """Test CalculatorWithHistory initialization."""

    def test_init_creates_empty_history(self):
        """Verify that a new instance starts with an empty history."""
        calc = CalculatorWithHistory()
        assert calc.get_history() == []

    def test_init_creates_calculator_instance(self):
        """Verify that __init__ creates an underlying Calculator instance."""
        calc = CalculatorWithHistory()
        # The _calculator attribute should exist; we can verify it by
        # performing an operation and checking the result
        result = calc.add(2, 3)
        assert result == 5.0

    def test_multiple_instances_have_independent_histories(self):
        """Verify that separate instances maintain independent histories."""
        calc1 = CalculatorWithHistory()
        calc2 = CalculatorWithHistory()

        calc1.add(2, 3)
        calc2.multiply(5, 6)

        hist1 = calc1.get_history()
        hist2 = calc2.get_history()

        assert len(hist1) == 1
        assert "+" in hist1[0]
        assert len(hist2) == 1
        assert "*" in hist2[0]


# ===========================================================================
# Binary arithmetic operations — history recording
# ===========================================================================

class TestBinaryOperationsHistoryRecording:
    """Test that binary operations are correctly recorded."""

    def test_add_records_history_entry(self):
        """Verify add() records an entry in the format 'a + b = result'."""
        calc = CalculatorWithHistory()
        calc.add(2.0, 3.0)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0] == "2.0 + 3.0 = 5.0"

    def test_subtract_records_history_entry(self):
        """Verify subtract() records an entry in the format 'a - b = result'."""
        calc = CalculatorWithHistory()
        calc.subtract(10.0, 4.0)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0] == "10.0 - 4.0 = 6.0"

    def test_multiply_records_history_entry(self):
        """Verify multiply() records an entry in the format 'a * b = result'."""
        calc = CalculatorWithHistory()
        calc.multiply(6.0, 7.0)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0] == "6.0 * 7.0 = 42.0"

    def test_divide_records_history_entry(self):
        """Verify divide() records an entry in the format 'a / b = result'."""
        calc = CalculatorWithHistory()
        calc.divide(8.0, 2.0)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0] == "8.0 / 2.0 = 4.0"

    def test_divide_float_result_recorded_accurately(self):
        """Verify divide records fractional results correctly."""
        calc = CalculatorWithHistory()
        calc.divide(1.0, 3.0)
        history = calc.get_history()
        assert len(history) == 1
        # The result should be approximately 0.333...
        assert "1.0 / 3.0 =" in history[0]
        # Extract the result part
        result_str = history[0].split("=")[1].strip()
        result = float(result_str)
        assert result == pytest.approx(1.0 / 3.0)

    def test_add_with_negative_operands(self):
        """Verify add works with negative numbers."""
        calc = CalculatorWithHistory()
        calc.add(-3.0, -4.0)
        history = calc.get_history()
        assert history[0] == "-3.0 - 4.0 = -7.0" or history[0] == "-3.0 + -4.0 = -7.0"

    def test_subtract_producing_negative(self):
        """Verify subtract can produce negative results."""
        calc = CalculatorWithHistory()
        calc.subtract(3.0, 10.0)
        history = calc.get_history()
        assert "3.0 - 10.0 = -7.0" in history[0]

    def test_multiply_by_zero(self):
        """Verify multiply by zero is recorded."""
        calc = CalculatorWithHistory()
        calc.multiply(99.0, 0.0)
        history = calc.get_history()
        assert "99.0 * 0.0 = 0.0" in history[0]

    def test_divide_zero_by_nonzero(self):
        """Verify divide zero by nonzero is recorded."""
        calc = CalculatorWithHistory()
        calc.divide(0.0, 5.0)
        history = calc.get_history()
        assert "0.0 / 5.0 = 0.0" in history[0]


# ===========================================================================
# Binary arithmetic operations — failed operations NOT recorded
# ===========================================================================

class TestBinaryOperationsFailureNotRecorded:
    """Verify that failed operations do not appear in history."""

    def test_divide_by_zero_not_recorded(self):
        """Verify division by zero raises but is NOT recorded in history."""
        calc = CalculatorWithHistory()
        with pytest.raises(ZeroDivisionError):
            calc.divide(5.0, 0.0)
        # History should still be empty
        assert calc.get_history() == []

    def test_divide_zero_by_zero_not_recorded(self):
        """Verify 0/0 raises but is NOT recorded in history."""
        calc = CalculatorWithHistory()
        with pytest.raises(ZeroDivisionError):
            calc.divide(0.0, 0.0)
        assert calc.get_history() == []

    def test_add_then_divide_by_zero_only_add_recorded(self):
        """Verify a failed operation doesn't erase prior successful ones."""
        calc = CalculatorWithHistory()
        calc.add(2.0, 3.0)
        with pytest.raises(ZeroDivisionError):
            calc.divide(5.0, 0.0)
        # Only the add should be recorded
        history = calc.get_history()
        assert len(history) == 1
        assert "+" in history[0]


# ===========================================================================
# Unary operations — history recording
# ===========================================================================

class TestUnaryOperationsHistoryRecording:
    """Test that unary operations are correctly recorded."""

    def test_factorial_records_history_entry(self):
        """Verify factorial() records an entry."""
        calc = CalculatorWithHistory()
        calc.factorial(5)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0] == "factorial(5) = 120"

    def test_square_records_history_entry(self):
        """Verify square() records an entry in the format 'square(x) = result'."""
        calc = CalculatorWithHistory()
        calc.square(4.0)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0] == "square(4.0) = 16.0"

    def test_cube_records_history_entry(self):
        """Verify cube() records an entry in the format 'cube(x) = result'."""
        calc = CalculatorWithHistory()
        calc.cube(3.0)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0] == "cube(3.0) = 27.0"

    def test_square_root_records_history_entry(self):
        """Verify square_root() records an entry."""
        calc = CalculatorWithHistory()
        calc.square_root(9.0)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0] == "square_root(9.0) = 3.0"

    def test_cube_root_records_history_entry(self):
        """Verify cube_root() records an entry."""
        calc = CalculatorWithHistory()
        calc.cube_root(27.0)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0] == "cube_root(27.0) = 3.0"

    def test_cube_root_negative_number(self):
        """Verify cube_root() handles negative numbers."""
        calc = CalculatorWithHistory()
        calc.cube_root(-8.0)
        history = calc.get_history()
        assert len(history) == 1
        assert "cube_root(-8.0) = -2.0" in history[0]

    def test_power_records_history_entry(self):
        """Verify power() records an entry."""
        calc = CalculatorWithHistory()
        calc.power(2.0, 3.0)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0] == "power(2.0, 3.0) = 8.0"

    def test_log_records_history_entry(self):
        """Verify log() (base-10) records an entry."""
        calc = CalculatorWithHistory()
        calc.log(100.0)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0] == "log(100.0) = 2.0"

    def test_ln_records_history_entry(self):
        """Verify ln() (natural log) records an entry."""
        calc = CalculatorWithHistory()
        calc.ln(1.0)  # ln(1) = 0
        history = calc.get_history()
        assert len(history) == 1
        assert history[0] == "ln(1.0) = 0.0"

    def test_factorial_zero(self):
        """Verify factorial(0) is recorded."""
        calc = CalculatorWithHistory()
        calc.factorial(0)
        history = calc.get_history()
        assert history[0] == "factorial(0) = 1"

    def test_square_negative_number(self):
        """Verify square of negative number is recorded."""
        calc = CalculatorWithHistory()
        calc.square(-5.0)
        history = calc.get_history()
        assert history[0] == "square(-5.0) = 25.0"

    def test_power_zero_exponent(self):
        """Verify x^0 = 1 is recorded."""
        calc = CalculatorWithHistory()
        calc.power(5.0, 0.0)
        history = calc.get_history()
        assert history[0] == "power(5.0, 0.0) = 1.0"


# ===========================================================================
# Unary operations — failed operations NOT recorded
# ===========================================================================

class TestUnaryOperationsFailureNotRecorded:
    """Verify that failed unary operations are not recorded."""

    def test_factorial_negative_not_recorded(self):
        """Verify factorial(-n) raises ValueError but is NOT recorded."""
        calc = CalculatorWithHistory()
        with pytest.raises(ValueError):
            calc.factorial(-5)
        assert calc.get_history() == []

    def test_factorial_non_integer_not_recorded(self):
        """Verify factorial(float) raises ValueError but is NOT recorded."""
        calc = CalculatorWithHistory()
        with pytest.raises(ValueError):
            calc.factorial(3.5)  # type: ignore[arg-type]
        assert calc.get_history() == []

    def test_square_root_negative_not_recorded(self):
        """Verify square_root(-x) raises ValueError but is NOT recorded."""
        calc = CalculatorWithHistory()
        with pytest.raises(ValueError):
            calc.square_root(-4.0)
        assert calc.get_history() == []

    def test_log_nonpositive_not_recorded(self):
        """Verify log(x<=0) raises ValueError but is NOT recorded."""
        calc = CalculatorWithHistory()
        with pytest.raises(ValueError):
            calc.log(0.0)
        with pytest.raises(ValueError):
            calc.log(-5.0)
        assert calc.get_history() == []

    def test_ln_nonpositive_not_recorded(self):
        """Verify ln(x<=0) raises ValueError but is NOT recorded."""
        calc = CalculatorWithHistory()
        with pytest.raises(ValueError):
            calc.ln(0.0)
        with pytest.raises(ValueError):
            calc.ln(-5.0)
        assert calc.get_history() == []

    def test_successful_then_failed_operation_only_successful_recorded(self):
        """Verify failed operation doesn't erase prior successful ones."""
        calc = CalculatorWithHistory()
        calc.square(5.0)
        with pytest.raises(ValueError):
            calc.square_root(-4.0)
        # Only the square should be recorded
        history = calc.get_history()
        assert len(history) == 1
        assert "square" in history[0]


# ===========================================================================
# History ordering and multiple operations
# ===========================================================================

class TestHistoryOrdering:
    """Test that history entries appear in chronological order."""

    def test_history_ordering_multiple_adds(self):
        """Verify operations are recorded in order."""
        calc = CalculatorWithHistory()
        calc.add(1.0, 2.0)
        calc.add(3.0, 4.0)
        calc.add(5.0, 6.0)
        history = calc.get_history()
        assert len(history) == 3
        assert "1.0 + 2.0" in history[0]
        assert "3.0 + 4.0" in history[1]
        assert "5.0 + 6.0" in history[2]

    def test_history_ordering_mixed_operations(self):
        """Verify mixed operation types are recorded in order."""
        calc = CalculatorWithHistory()
        calc.add(2.0, 3.0)
        calc.multiply(5.0, 6.0)
        calc.subtract(10.0, 2.0)
        calc.divide(8.0, 2.0)
        history = calc.get_history()
        assert len(history) == 4
        assert "+" in history[0]
        assert "*" in history[1]
        assert "-" in history[2]
        assert "/" in history[3]

    def test_history_ordering_unary_and_binary(self):
        """Verify unary and binary operations are recorded in order."""
        calc = CalculatorWithHistory()
        calc.add(2.0, 3.0)
        calc.square(4.0)
        calc.subtract(10.0, 2.0)
        calc.factorial(5)
        history = calc.get_history()
        assert len(history) == 4
        assert "+" in history[0]
        assert "square" in history[1]
        assert "-" in history[2]
        assert "factorial" in history[3]

    def test_ten_operations_all_recorded(self):
        """Verify many operations are all recorded."""
        calc = CalculatorWithHistory()
        for i in range(10):
            calc.add(float(i), 1.0)
        history = calc.get_history()
        assert len(history) == 10


# ===========================================================================
# get_history() isolation — returns a copy
# ===========================================================================

class TestGetHistoryIsolation:
    """Verify that get_history() returns a copy, not the internal list."""

    def test_get_history_returns_list(self):
        """Verify get_history() returns a list."""
        calc = CalculatorWithHistory()
        history = calc.get_history()
        assert isinstance(history, list)

    def test_get_history_returns_copy_not_reference(self):
        """Verify modifying returned list doesn't affect internal history."""
        calc = CalculatorWithHistory()
        calc.add(2.0, 3.0)

        history1 = calc.get_history()
        history1.append("FAKE ENTRY")

        history2 = calc.get_history()
        assert len(history2) == 1
        assert history2[0] != "FAKE ENTRY"
        assert "+" in history2[0]

    def test_get_history_returns_new_copy_each_time(self):
        """Verify multiple calls to get_history() return independent lists."""
        calc = CalculatorWithHistory()
        calc.add(2.0, 3.0)

        history1 = calc.get_history()
        history2 = calc.get_history()

        # They should be equal but not the same object
        assert history1 == history2
        assert history1 is not history2

    def test_mutating_returned_list_doesnt_affect_subsequent_calls(self):
        """Verify mutation of returned list doesn't affect future calls."""
        calc = CalculatorWithHistory()
        calc.add(1.0, 2.0)
        calc.add(3.0, 4.0)

        history1 = calc.get_history()
        original_len = len(history1)
        history1.pop()
        history1[0] = "MODIFIED"

        # The internal history should be unaffected
        history2 = calc.get_history()
        assert len(history2) == original_len
        assert history2[0] != "MODIFIED"

    def test_get_history_empty_returns_empty_list(self):
        """Verify get_history() returns an empty list when no operations."""
        calc = CalculatorWithHistory()
        history = calc.get_history()
        assert isinstance(history, list)
        assert len(history) == 0


# ===========================================================================
# Edge cases — large numbers, special values
# ===========================================================================

class TestEdgeCasesLargeNumbers:
    """Test history recording with large numbers."""

    def test_add_very_large_numbers(self):
        """Verify adding very large numbers is recorded."""
        calc = CalculatorWithHistory()
        calc.add(1e308, 1e307)
        history = calc.get_history()
        assert len(history) == 1
        assert "=" in history[0]

    def test_multiply_resulting_in_overflow_to_inf(self):
        """Verify multiply overflow to infinity is recorded."""
        calc = CalculatorWithHistory()
        calc.multiply(1e200, 1e200)
        history = calc.get_history()
        assert len(history) == 1
        assert "=" in history[0]

    def test_very_small_positive_float(self):
        """Verify very small positive floats are recorded."""
        calc = CalculatorWithHistory()
        calc.add(1e-308, 1e-308)
        history = calc.get_history()
        assert len(history) == 1

    def test_log_large_number(self):
        """Verify log of large number is recorded."""
        calc = CalculatorWithHistory()
        calc.log(1e100)
        history = calc.get_history()
        assert len(history) == 1
        assert "log(1e+100)" in history[0]


# ===========================================================================
# Edge cases — multiple failures mixed with successes
# ===========================================================================

class TestEdgeCasesMultipleFailures:
    """Test that multiple failed operations don't affect history."""

    def test_multiple_division_by_zero_attempts(self):
        """Verify multiple failed division attempts don't create entries."""
        calc = CalculatorWithHistory()
        calc.add(1.0, 2.0)
        with pytest.raises(ZeroDivisionError):
            calc.divide(5.0, 0.0)
        with pytest.raises(ZeroDivisionError):
            calc.divide(10.0, 0.0)
        calc.multiply(3.0, 4.0)
        history = calc.get_history()
        # Only the two successful operations should be recorded
        assert len(history) == 2
        assert "+" in history[0]
        assert "*" in history[1]

    def test_multiple_invalid_factorial_attempts(self):
        """Verify multiple failed factorial attempts don't create entries."""
        calc = CalculatorWithHistory()
        calc.add(2.0, 3.0)
        with pytest.raises(ValueError):
            calc.factorial(-1)
        with pytest.raises(ValueError):
            calc.factorial(-5)
        calc.square(3.0)
        history = calc.get_history()
        assert len(history) == 2
        assert "+" in history[0]
        assert "square" in history[1]


# ===========================================================================
# Edge cases — special numeric values
# ===========================================================================

class TestEdgeCasesSpecialValues:
    """Test edge cases with special numeric values."""

    def test_add_zero_to_number(self):
        """Verify adding zero is recorded."""
        calc = CalculatorWithHistory()
        calc.add(5.0, 0.0)
        history = calc.get_history()
        assert history[0] == "5.0 + 0.0 = 5.0"

    def test_multiply_by_one(self):
        """Verify multiplying by one is recorded."""
        calc = CalculatorWithHistory()
        calc.multiply(7.0, 1.0)
        history = calc.get_history()
        assert history[0] == "7.0 * 1.0 = 7.0"

    def test_divide_by_one(self):
        """Verify dividing by one is recorded."""
        calc = CalculatorWithHistory()
        calc.divide(7.0, 1.0)
        history = calc.get_history()
        assert history[0] == "7.0 / 1.0 = 7.0"

    def test_subtract_from_itself(self):
        """Verify x - x = 0 is recorded."""
        calc = CalculatorWithHistory()
        calc.subtract(5.0, 5.0)
        history = calc.get_history()
        assert history[0] == "5.0 - 5.0 = 0.0"

    def test_square_root_one(self):
        """Verify sqrt(1) = 1 is recorded."""
        calc = CalculatorWithHistory()
        calc.square_root(1.0)
        history = calc.get_history()
        assert history[0] == "square_root(1.0) = 1.0"

    def test_square_zero(self):
        """Verify 0^2 = 0 is recorded."""
        calc = CalculatorWithHistory()
        calc.square(0.0)
        history = calc.get_history()
        assert history[0] == "square(0.0) = 0.0"

    def test_cube_zero(self):
        """Verify 0^3 = 0 is recorded."""
        calc = CalculatorWithHistory()
        calc.cube(0.0)
        history = calc.get_history()
        assert history[0] == "cube(0.0) = 0.0"

    def test_cube_one(self):
        """Verify 1^3 = 1 is recorded."""
        calc = CalculatorWithHistory()
        calc.cube(1.0)
        history = calc.get_history()
        assert history[0] == "cube(1.0) = 1.0"


# ===========================================================================
# Integration-like tests — realistic usage patterns
# ===========================================================================

class TestRealisticUsagePatterns:
    """Test realistic patterns of calculator usage."""

    def test_sequence_of_calculations(self):
        """Simulate a realistic sequence of calculations."""
        calc = CalculatorWithHistory()
        calc.add(10.0, 5.0)  # 15
        calc.multiply(3.0, 4.0)  # 12
        calc.divide(20.0, 4.0)  # 5
        calc.square(2.0)  # 4
        history = calc.get_history()
        assert len(history) == 4

    def test_chaining_operations_result_of_one_used_in_next(self):
        """Verify history records each operation even when results are chained."""
        calc = CalculatorWithHistory()
        result1 = calc.add(2.0, 3.0)  # 5
        result2 = calc.multiply(result1, 2.0)  # 10
        result3 = calc.square(result2)  # 100
        history = calc.get_history()
        assert len(history) == 3
        assert "2.0 + 3.0" in history[0]
        assert "5.0 * 2.0" in history[1]
        assert "10.0)" in history[2]  # The power/square uses the result

    def test_history_reflects_actual_calculations_not_intended_calculations(self):
        """Verify history is based on what actually happened."""
        calc = CalculatorWithHistory()
        a = 10.0
        b = 3.0
        result = calc.divide(a, b)
        history = calc.get_history()
        assert "10.0 / 3.0" in history[0]
        # The actual result should be in the history
        assert result == pytest.approx(float(history[0].split("=")[1]))

    def test_all_operations_in_one_calculator(self):
        """Test using all available operations on one calculator."""
        calc = CalculatorWithHistory()
        calc.add(1.0, 2.0)
        calc.subtract(5.0, 3.0)
        calc.multiply(4.0, 5.0)
        calc.divide(20.0, 4.0)
        calc.factorial(5)
        calc.square(3.0)
        calc.cube(2.0)
        calc.square_root(16.0)
        calc.cube_root(8.0)
        calc.power(2.0, 4.0)
        calc.log(100.0)
        calc.ln(2.718281828)

        history = calc.get_history()
        assert len(history) == 12
