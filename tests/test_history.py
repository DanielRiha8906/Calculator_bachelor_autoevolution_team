"""test_history.py — comprehensive tests for the Calculator history feature.

Tests cover:
- get_history() returns empty list on fresh instance
- History recording for all binary operations (add, subtract, multiply, divide, power)
- History recording for all unary operations (square, cube, factorial, square_root, cube_root, natural_log, log_base_10)
- Operand2 is None for unary operations
- History order is chronological
- Failed operations are not recorded
- History is independent across Calculator instances
- History structure and immutability guarantees
"""

import pytest
import math
from src import Calculator


@pytest.fixture
def calculator():
    """Fixture providing a fresh Calculator instance for tests."""
    return Calculator()


class TestHistoryInitialization:
    """Tests for history initialization and empty state."""

    def test_get_history_returns_empty_list_on_fresh_instance(self, calculator):
        """Test that get_history() returns an empty list for a fresh Calculator."""
        history = calculator.get_history()
        assert isinstance(history, list)
        assert len(history) == 0

    def test_get_history_returns_list_type(self, calculator):
        """Test that get_history() returns a list (not tuple or other sequence)."""
        history = calculator.get_history()
        assert type(history) is list


class TestBinaryOperationHistoryRecording:
    """Tests for history recording of two-operand operations."""

    def test_history_add_records_correct_entry(self, calculator):
        """Test that add(5, 3) records correct entry in history."""
        calculator.add(5, 3)
        history = calculator.get_history()
        assert len(history) == 1
        entry = history[0]
        assert entry["operand1"] == 5
        assert entry["operator"] == "add"
        assert entry["operand2"] == 3
        assert entry["result"] == 8

    def test_history_subtract_records_correct_entry(self, calculator):
        """Test that subtract(10, 4) records correct entry in history."""
        calculator.subtract(10, 4)
        history = calculator.get_history()
        assert len(history) == 1
        entry = history[0]
        assert entry["operand1"] == 10
        assert entry["operator"] == "subtract"
        assert entry["operand2"] == 4
        assert entry["result"] == 6

    def test_history_multiply_records_correct_entry(self, calculator):
        """Test that multiply(2, 3) records correct entry in history."""
        calculator.multiply(2, 3)
        history = calculator.get_history()
        assert len(history) == 1
        entry = history[0]
        assert entry["operand1"] == 2
        assert entry["operator"] == "multiply"
        assert entry["operand2"] == 3
        assert entry["result"] == 6

    def test_history_divide_records_correct_entry(self, calculator):
        """Test that divide(10, 2) records correct entry in history."""
        calculator.divide(10, 2)
        history = calculator.get_history()
        assert len(history) == 1
        entry = history[0]
        assert entry["operand1"] == 10
        assert entry["operator"] == "divide"
        assert entry["operand2"] == 2
        assert entry["result"] == 5.0

    def test_history_power_records_correct_entry(self, calculator):
        """Test that power(2, 8) records correct entry in history."""
        calculator.power(2, 8)
        history = calculator.get_history()
        assert len(history) == 1
        entry = history[0]
        assert entry["operand1"] == 2
        assert entry["operator"] == "power"
        assert entry["operand2"] == 8
        assert entry["result"] == 256

    @pytest.mark.parametrize("a,b,op_name,result", [
        (5, 3, "add", 8),
        (10, 4, "subtract", 6),
        (2, 3, "multiply", 6),
        (10, 2, "divide", 5.0),
        (2, 3, "power", 8),
    ])
    def test_history_binary_operations_various_inputs(self, calculator, a, b, op_name, result):
        """Test history recording for various binary operations and inputs."""
        method = getattr(calculator, op_name)
        method(a, b)
        history = calculator.get_history()
        assert len(history) == 1
        entry = history[0]
        assert entry["operand1"] == a
        assert entry["operator"] == op_name
        assert entry["operand2"] == b
        assert entry["result"] == result


class TestUnaryOperationHistoryRecording:
    """Tests for history recording of one-operand operations."""

    def test_history_square_records_correct_entry(self, calculator):
        """Test that square(5) records correct entry with operand2=None."""
        calculator.square(5)
        history = calculator.get_history()
        assert len(history) == 1
        entry = history[0]
        assert entry["operand1"] == 5
        assert entry["operator"] == "square"
        assert entry["operand2"] is None
        assert entry["result"] == 25

    def test_history_cube_records_correct_entry(self, calculator):
        """Test that cube(3) records correct entry with operand2=None."""
        calculator.cube(3)
        history = calculator.get_history()
        assert len(history) == 1
        entry = history[0]
        assert entry["operand1"] == 3
        assert entry["operator"] == "cube"
        assert entry["operand2"] is None
        assert entry["result"] == 27

    def test_history_factorial_records_correct_entry(self, calculator):
        """Test that factorial(5) records correct entry with operand2=None."""
        calculator.factorial(5)
        history = calculator.get_history()
        assert len(history) == 1
        entry = history[0]
        assert entry["operand1"] == 5
        assert entry["operator"] == "factorial"
        assert entry["operand2"] is None
        assert entry["result"] == 120

    def test_history_square_root_records_correct_entry(self, calculator):
        """Test that square_root(16) records correct entry with operand2=None."""
        calculator.square_root(16)
        history = calculator.get_history()
        assert len(history) == 1
        entry = history[0]
        assert entry["operand1"] == 16
        assert entry["operator"] == "square_root"
        assert entry["operand2"] is None
        assert entry["result"] == 4.0

    def test_history_cube_root_records_correct_entry(self, calculator):
        """Test that cube_root(8) records correct entry with operand2=None."""
        calculator.cube_root(8)
        history = calculator.get_history()
        assert len(history) == 1
        entry = history[0]
        assert entry["operand1"] == 8
        assert entry["operator"] == "cube_root"
        assert entry["operand2"] is None
        assert pytest.approx(entry["result"], rel=1e-10) == 2.0

    def test_history_natural_log_records_correct_entry(self, calculator):
        """Test that natural_log(1) records correct entry with operand2=None."""
        calculator.natural_log(1)
        history = calculator.get_history()
        assert len(history) == 1
        entry = history[0]
        assert entry["operand1"] == 1
        assert entry["operator"] == "natural_log"
        assert entry["operand2"] is None
        assert entry["result"] == 0

    def test_history_log_base_10_records_correct_entry(self, calculator):
        """Test that log_base_10(10) records correct entry with operand2=None."""
        calculator.log_base_10(10)
        history = calculator.get_history()
        assert len(history) == 1
        entry = history[0]
        assert entry["operand1"] == 10
        assert entry["operator"] == "log_base_10"
        assert entry["operand2"] is None
        assert entry["result"] == 1.0

    @pytest.mark.parametrize("x,op_name,result", [
        (5, "square", 25),
        (3, "cube", 27),
        (5, "factorial", 120),
        (16, "square_root", 4.0),
        (1, "natural_log", 0),
        (10, "log_base_10", 1.0),
    ])
    def test_history_unary_operations_various_inputs(self, calculator, x, op_name, result):
        """Test history recording for various unary operations."""
        method = getattr(calculator, op_name)
        method(x)
        history = calculator.get_history()
        assert len(history) == 1
        entry = history[0]
        assert entry["operand1"] == x
        assert entry["operator"] == op_name
        assert entry["operand2"] is None
        assert pytest.approx(entry["result"], rel=1e-10) == result


class TestHistoryChronologicalOrder:
    """Tests for history order and accumulation."""

    def test_history_maintains_chronological_order(self, calculator):
        """Test that multiple operations are recorded in chronological order."""
        calculator.add(5, 3)
        calculator.multiply(2, 4)
        calculator.square(3)

        history = calculator.get_history()
        assert len(history) == 3
        assert history[0]["operator"] == "add"
        assert history[1]["operator"] == "multiply"
        assert history[2]["operator"] == "square"

    def test_history_accumulates_with_each_operation(self, calculator):
        """Test that history grows with each operation."""
        assert len(calculator.get_history()) == 0
        calculator.add(5, 3)
        assert len(calculator.get_history()) == 1
        calculator.subtract(10, 4)
        assert len(calculator.get_history()) == 2
        calculator.square(7)
        assert len(calculator.get_history()) == 3

    def test_history_multiple_mixed_operations(self, calculator):
        """Test history with alternating binary and unary operations."""
        calculator.add(5, 3)
        calculator.square(4)
        calculator.multiply(2, 3)
        calculator.factorial(5)
        calculator.divide(10, 2)

        history = calculator.get_history()
        assert len(history) == 5
        assert history[0]["operator"] == "add"
        assert history[1]["operator"] == "square"
        assert history[2]["operator"] == "multiply"
        assert history[3]["operator"] == "factorial"
        assert history[4]["operator"] == "divide"

    def test_history_with_repeated_operations(self, calculator):
        """Test that repeated operations are all recorded separately."""
        calculator.add(1, 1)
        calculator.add(2, 2)
        calculator.add(3, 3)

        history = calculator.get_history()
        assert len(history) == 3
        assert all(entry["operator"] == "add" for entry in history)
        assert history[0]["result"] == 2
        assert history[1]["result"] == 4
        assert history[2]["result"] == 6


class TestHistoryFailedOperationsNotRecorded:
    """Tests for ensuring failed operations do not update history."""

    def test_factorial_negative_not_recorded_in_history(self, calculator):
        """Test that factorial(-1) exception does not record in history."""
        assert len(calculator.get_history()) == 0
        with pytest.raises(ValueError):
            calculator.factorial(-1)
        assert len(calculator.get_history()) == 0

    def test_factorial_float_not_recorded_in_history(self, calculator):
        """Test that factorial(5.5) exception does not record in history."""
        assert len(calculator.get_history()) == 0
        with pytest.raises(TypeError):
            calculator.factorial(5.5)
        assert len(calculator.get_history()) == 0

    def test_divide_by_zero_not_recorded_in_history(self, calculator):
        """Test that divide(10, 0) exception does not record in history."""
        assert len(calculator.get_history()) == 0
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)
        assert len(calculator.get_history()) == 0

    def test_square_root_negative_not_recorded_in_history(self, calculator):
        """Test that square_root(-1) exception does not record in history."""
        assert len(calculator.get_history()) == 0
        with pytest.raises(ValueError):
            calculator.square_root(-1)
        assert len(calculator.get_history()) == 0

    def test_natural_log_zero_not_recorded_in_history(self, calculator):
        """Test that natural_log(0) exception does not record in history."""
        assert len(calculator.get_history()) == 0
        with pytest.raises(ValueError):
            calculator.natural_log(0)
        assert len(calculator.get_history()) == 0

    def test_log_base_10_negative_not_recorded_in_history(self, calculator):
        """Test that log_base_10(-5) exception does not record in history."""
        assert len(calculator.get_history()) == 0
        with pytest.raises(ValueError):
            calculator.log_base_10(-5)
        assert len(calculator.get_history()) == 0

    def test_failed_operation_does_not_affect_existing_history(self, calculator):
        """Test that a failed operation does not affect existing history."""
        calculator.add(5, 3)
        assert len(calculator.get_history()) == 1
        with pytest.raises(ValueError):
            calculator.factorial(-1)
        assert len(calculator.get_history()) == 1
        # Verify the existing entry is unchanged
        assert calculator.get_history()[0]["operator"] == "add"


class TestHistoryIndependentInstances:
    """Tests for history independence across Calculator instances."""

    def test_two_calculator_instances_have_independent_histories(self):
        """Test that two separate Calculator instances maintain independent histories."""
        calc1 = Calculator()
        calc2 = Calculator()

        calc1.add(5, 3)
        calc2.multiply(2, 2)

        assert len(calc1.get_history()) == 1
        assert len(calc2.get_history()) == 1
        assert calc1.get_history()[0]["operator"] == "add"
        assert calc2.get_history()[0]["operator"] == "multiply"

    def test_operations_on_calc1_do_not_affect_calc2(self):
        """Test that operations on one calculator don't affect another."""
        calc1 = Calculator()
        calc2 = Calculator()

        calc1.add(1, 1)
        calc1.square(2)
        calc1.factorial(3)

        assert len(calc2.get_history()) == 0
        assert len(calc1.get_history()) == 3

    def test_three_instances_with_different_operations(self):
        """Test that three independent instances maintain separate histories."""
        calc1 = Calculator()
        calc2 = Calculator()
        calc3 = Calculator()

        calc1.add(5, 3)
        calc2.add(5, 3)
        calc3.add(5, 3)

        assert len(calc1.get_history()) == 1
        assert len(calc2.get_history()) == 1
        assert len(calc3.get_history()) == 1
        # Each should be a different entry object (not shared)
        assert calc1.get_history()[0] is not calc2.get_history()[0]


class TestHistoryStructure:
    """Tests for the structure and content of history entries."""

    def test_history_entry_has_required_keys(self, calculator):
        """Test that each history entry has all required keys."""
        calculator.add(5, 3)
        entry = calculator.get_history()[0]
        required_keys = {"operand1", "operator", "operand2", "result"}
        assert set(entry.keys()) == required_keys

    def test_history_entry_is_dict(self, calculator):
        """Test that each history entry is a dict."""
        calculator.add(5, 3)
        entry = calculator.get_history()[0]
        assert isinstance(entry, dict)

    def test_history_returns_list_of_dicts(self, calculator):
        """Test that get_history() returns a list containing only dicts."""
        calculator.add(5, 3)
        calculator.square(2)
        history = calculator.get_history()
        assert isinstance(history, list)
        assert all(isinstance(entry, dict) for entry in history)

    def test_history_entry_operand1_type_preservation(self, calculator):
        """Test that operand1 preserves its type (int or float)."""
        calculator.add(5, 3)
        calculator.add(5.5, 2.5)
        history = calculator.get_history()
        assert isinstance(history[0]["operand1"], int)
        assert isinstance(history[1]["operand1"], float)

    def test_history_entry_operand2_type_preservation(self, calculator):
        """Test that operand2 preserves its type for binary operations."""
        calculator.add(5, 3)
        calculator.add(5.5, 2.5)
        history = calculator.get_history()
        assert isinstance(history[0]["operand2"], int)
        assert isinstance(history[1]["operand2"], float)

    def test_history_entry_operand2_is_none_for_unary_ops(self, calculator):
        """Test that operand2 is None for all unary operations."""
        unary_ops = [
            ("square", 5),
            ("cube", 3),
            ("factorial", 5),
            ("square_root", 16),
            ("cube_root", 8),
            ("natural_log", 1),
            ("log_base_10", 10),
        ]
        for op_name, operand in unary_ops:
            calculator_fresh = Calculator()
            method = getattr(calculator_fresh, op_name)
            method(operand)
            assert calculator_fresh.get_history()[0]["operand2"] is None

    def test_history_result_type_matches_operation(self, calculator):
        """Test that result type makes sense for the operation."""
        calculator.add(5, 3)
        assert isinstance(calculator.get_history()[0]["result"], int)

        calculator_div = Calculator()
        calculator_div.divide(10, 2)
        assert isinstance(calculator_div.get_history()[0]["result"], float)


class TestHistoryImmutability:
    """Tests for protecting history from unintended mutations."""

    def test_get_history_returns_reference_to_internal_list(self, calculator):
        """Test that get_history() returns the actual internal list (not a copy)."""
        calculator.add(5, 3)
        history1 = calculator.get_history()
        history2 = calculator.get_history()
        # Both should refer to the same object
        assert history1 is history2

    def test_mutating_returned_history_affects_internal_state(self, calculator):
        """Test that modifications to returned history affect internal state.

        This is documenting current behavior. If immutability is desired,
        get_history() should return a copy instead.
        """
        calculator.add(5, 3)
        history = calculator.get_history()
        original_length = len(history)
        # Mutate the returned list
        history.append({"operand1": 999, "operator": "test", "operand2": None, "result": 999})
        # Check that the internal state changed
        assert len(calculator.get_history()) == original_length + 1

    def test_modifying_entry_in_history_affects_get_history(self, calculator):
        """Test that modifications to entry dicts affect get_history()."""
        calculator.add(5, 3)
        history = calculator.get_history()
        entry = history[0]
        # Modify the entry
        original_result = entry["result"]
        entry["result"] = 999
        # Check that get_history() reflects the change
        assert calculator.get_history()[0]["result"] == 999
        # Restore for other tests
        entry["result"] = original_result


class TestHistoryNegativeAndSpecialValues:
    """Tests for history with negative, zero, and special numeric values."""

    def test_history_with_negative_operands(self, calculator):
        """Test history recording with negative operands."""
        calculator.add(-5, -3)
        calculator.multiply(-2, 3)
        history = calculator.get_history()
        assert history[0]["operand1"] == -5
        assert history[0]["operand2"] == -3
        assert history[1]["operand1"] == -2
        assert history[1]["operand2"] == 3

    def test_history_with_zero_operands(self, calculator):
        """Test history recording with zero operands."""
        calculator.add(0, 5)
        calculator.multiply(0, 10)
        history = calculator.get_history()
        assert history[0]["operand1"] == 0
        assert history[0]["result"] == 5
        assert history[1]["operand1"] == 0
        assert history[1]["result"] == 0

    def test_history_with_floating_point_operands(self, calculator):
        """Test history recording with floating-point operands."""
        calculator.add(0.1, 0.2)
        history = calculator.get_history()
        assert history[0]["operand1"] == 0.1
        assert history[0]["operand2"] == 0.2

    def test_history_with_large_numbers(self, calculator):
        """Test history recording with very large numbers."""
        large = 10 ** 100
        calculator.add(large, 1)
        history = calculator.get_history()
        assert history[0]["operand1"] == large
        assert history[0]["operand2"] == 1
        assert history[0]["result"] == large + 1

    def test_history_with_very_small_numbers(self, calculator):
        """Test history recording with very small floating-point numbers."""
        small = 1e-100
        calculator.add(small, small)
        history = calculator.get_history()
        assert history[0]["operand1"] == small
        assert history[0]["operand2"] == small


class TestHistoryComprehensive:
    """Integration tests combining multiple history features."""

    def test_long_sequence_of_operations_maintains_history(self, calculator):
        """Test history with a long sequence of varied operations."""
        operations = [
            ("add", (5, 3)),
            ("subtract", (10, 4)),
            ("multiply", (2, 3)),
            ("divide", (10, 2)),
            ("square", (4,)),
            ("cube", (2,)),
            ("factorial", (5,)),
            ("power", (2, 8)),
        ]
        for op_name, args in operations:
            method = getattr(calculator, op_name)
            method(*args)

        history = calculator.get_history()
        assert len(history) == len(operations)
        for i, (op_name, _) in enumerate(operations):
            assert history[i]["operator"] == op_name

    def test_history_preserves_all_calculation_context(self, calculator):
        """Test that history preserves full calculation context for reproducibility."""
        # Perform a calculation
        result1 = calculator.add(5, 3)
        # Get history
        history = calculator.get_history()
        entry = history[0]
        # Verify we can reconstruct the calculation
        assert entry["operand1"] + entry["operand2"] == entry["result"]
        assert result1 == entry["result"]

    def test_history_allows_audit_trail_of_calculations(self, calculator):
        """Test that history provides an audit trail for all calculations."""
        calculator.add(10, 5)
        calculator.multiply(3, 2)
        calculator.square(4)
        calculator.factorial(5)

        history = calculator.get_history()
        # Build an audit trail
        for i, entry in enumerate(history, start=1):
            assert "operand1" in entry
            assert "operator" in entry
            assert "result" in entry
            # operand2 can be None for unary, or present for binary
            assert "operand2" in entry
