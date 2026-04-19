"""Unit tests for the history tracking module.

Tests for OperationRecord dataclass and OperationHistory class.
"""

import pytest
from datetime import datetime
from src.history import OperationRecord, OperationHistory


# ============================================================================
# OPERATION RECORD TESTS
# ============================================================================

class TestOperationRecord:
    """Test suite for OperationRecord dataclass."""

    def test_operation_record_creation_with_valid_inputs(self):
        """Test creating an OperationRecord with valid inputs."""
        timestamp = datetime.now()
        record = OperationRecord(
            operation_name="add",
            operands=[5, 3],
            result=8,
            timestamp=timestamp
        )
        assert record.operation_name == "add"
        assert record.operands == [5, 3]
        assert record.result == 8
        assert record.timestamp == timestamp

    def test_operation_record_fields_accessible(self):
        """Test that all fields of OperationRecord are accessible."""
        timestamp = datetime(2025, 1, 1, 12, 0, 0)
        record = OperationRecord(
            operation_name="multiply",
            operands=[4, 7],
            result=28,
            timestamp=timestamp
        )
        assert hasattr(record, "operation_name")
        assert hasattr(record, "operands")
        assert hasattr(record, "result")
        assert hasattr(record, "timestamp")

    def test_operation_record_with_float_operands(self):
        """Test creating a record with float operands."""
        timestamp = datetime.now()
        record = OperationRecord(
            operation_name="divide",
            operands=[10.5, 2.0],
            result=5.25,
            timestamp=timestamp
        )
        assert record.operands == [10.5, 2.0]
        assert record.result == 5.25

    def test_operation_record_with_single_operand(self):
        """Test creating a record with a single operand (unary operation)."""
        timestamp = datetime.now()
        record = OperationRecord(
            operation_name="square",
            operands=[5],
            result=25,
            timestamp=timestamp
        )
        assert record.operands == [5]
        assert record.result == 25

    def test_operation_record_with_negative_result(self):
        """Test creating a record with negative result."""
        timestamp = datetime.now()
        record = OperationRecord(
            operation_name="subtract",
            operands=[3, 5],
            result=-2,
            timestamp=timestamp
        )
        assert record.result == -2

    def test_operation_record_with_zero_result(self):
        """Test creating a record with zero result."""
        timestamp = datetime.now()
        record = OperationRecord(
            operation_name="subtract",
            operands=[5, 5],
            result=0,
            timestamp=timestamp
        )
        assert record.result == 0

    def test_operation_record_with_string_operation_name(self):
        """Test creating a record with string operation name."""
        timestamp = datetime.now()
        record = OperationRecord(
            operation_name="factorial",
            operands=[5],
            result=120,
            timestamp=timestamp
        )
        assert record.operation_name == "factorial"

    def test_operation_record_with_empty_operands_list(self):
        """Test creating a record with an empty operands list."""
        timestamp = datetime.now()
        record = OperationRecord(
            operation_name="constant_pi",
            operands=[],
            result=3.14159,
            timestamp=timestamp
        )
        assert record.operands == []

    def test_operation_record_equality(self):
        """Test that two records with same values are equal."""
        timestamp = datetime(2025, 1, 1, 12, 0, 0)
        record1 = OperationRecord(
            operation_name="add",
            operands=[5, 3],
            result=8,
            timestamp=timestamp
        )
        record2 = OperationRecord(
            operation_name="add",
            operands=[5, 3],
            result=8,
            timestamp=timestamp
        )
        assert record1 == record2

    def test_operation_record_inequality_different_operation(self):
        """Test that records with different operation names are not equal."""
        timestamp = datetime(2025, 1, 1, 12, 0, 0)
        record1 = OperationRecord(
            operation_name="add",
            operands=[5, 3],
            result=8,
            timestamp=timestamp
        )
        record2 = OperationRecord(
            operation_name="subtract",
            operands=[5, 3],
            result=2,
            timestamp=timestamp
        )
        assert record1 != record2

    def test_operation_record_with_various_result_types(self):
        """Test creating records with different result types."""
        timestamp = datetime.now()

        # Integer result
        rec_int = OperationRecord("add", [1, 2], 3, timestamp)
        assert rec_int.result == 3

        # Float result
        rec_float = OperationRecord("divide", [5, 2], 2.5, timestamp)
        assert rec_float.result == 2.5

        # String result (edge case)
        rec_str = OperationRecord("concat", ["a", "b"], "ab", timestamp)
        assert rec_str.result == "ab"

    def test_operation_record_with_complex_operands_list(self):
        """Test creating a record with a complex operands list."""
        timestamp = datetime.now()
        operands = [10, 5, 2, 1]
        record = OperationRecord(
            operation_name="multi_add",
            operands=operands,
            result=18,
            timestamp=timestamp
        )
        assert record.operands == operands
        assert len(record.operands) == 4


# ============================================================================
# OPERATION HISTORY TESTS
# ============================================================================

class TestOperationHistory:
    """Test suite for OperationHistory class."""

    def test_operation_history_initialization(self):
        """Test that OperationHistory initializes with empty history."""
        history = OperationHistory()
        assert len(history) == 0
        assert history.get_history() == []

    def test_add_record_single_record(self):
        """Test adding a single record to history."""
        history = OperationHistory()
        timestamp = datetime.now()
        history.add_record("add", [5, 3], 8, timestamp)

        assert len(history) == 1
        records = history.get_history()
        assert len(records) == 1
        assert records[0].operation_name == "add"

    def test_add_record_multiple_records(self):
        """Test adding multiple records to history."""
        history = OperationHistory()
        timestamp1 = datetime(2025, 1, 1, 12, 0, 0)
        timestamp2 = datetime(2025, 1, 1, 12, 0, 1)

        history.add_record("add", [5, 3], 8, timestamp1)
        history.add_record("multiply", [4, 2], 8, timestamp2)

        assert len(history) == 2

    def test_add_record_fields_preserved(self):
        """Test that all fields are preserved when adding a record."""
        history = OperationHistory()
        timestamp = datetime.now()
        operands = [10, 5]

        history.add_record("divide", operands, 2.0, timestamp)
        records = history.get_history()
        record = records[0]

        assert record.operation_name == "divide"
        assert record.operands == operands
        assert record.result == 2.0
        assert record.timestamp == timestamp

    def test_get_history_returns_copy(self):
        """Test that get_history returns a copy, not the internal list."""
        history = OperationHistory()
        timestamp = datetime.now()
        history.add_record("add", [5, 3], 8, timestamp)

        returned_list = history.get_history()
        returned_list.append(OperationRecord("subtract", [10, 2], 8, timestamp))

        # Internal history should still have only 1 record
        assert len(history.get_history()) == 1

    def test_get_history_mutation_does_not_affect_internal_state(self):
        """Test that mutating returned history does not affect internal state."""
        history = OperationHistory()
        timestamp = datetime.now()
        history.add_record("add", [5, 3], 8, timestamp)

        # Get history and mutate
        returned = history.get_history()
        returned.clear()

        # Internal should be unchanged
        assert len(history.get_history()) == 1

    def test_get_history_returns_records_in_order(self):
        """Test that get_history returns records in insertion order."""
        history = OperationHistory()
        ts1 = datetime(2025, 1, 1, 12, 0, 0)
        ts2 = datetime(2025, 1, 1, 12, 0, 1)
        ts3 = datetime(2025, 1, 1, 12, 0, 2)

        history.add_record("op1", [1], 1, ts1)
        history.add_record("op2", [2], 2, ts2)
        history.add_record("op3", [3], 3, ts3)

        records = history.get_history()
        assert records[0].operation_name == "op1"
        assert records[1].operation_name == "op2"
        assert records[2].operation_name == "op3"

    def test_clear_history(self):
        """Test that clear_history removes all records."""
        history = OperationHistory()
        timestamp = datetime.now()

        history.add_record("add", [5, 3], 8, timestamp)
        history.add_record("multiply", [4, 2], 8, timestamp)
        assert len(history) == 2

        history.clear_history()
        assert len(history) == 0
        assert history.get_history() == []

    def test_clear_history_on_empty_history(self):
        """Test that clear_history on empty history is safe."""
        history = OperationHistory()
        assert len(history) == 0
        history.clear_history()
        assert len(history) == 0

    def test_len_grows_with_add_record(self):
        """Test that __len__ grows as records are added."""
        history = OperationHistory()
        timestamp = datetime.now()

        assert len(history) == 0

        history.add_record("add", [1, 2], 3, timestamp)
        assert len(history) == 1

        history.add_record("subtract", [5, 2], 3, timestamp)
        assert len(history) == 2

        history.add_record("multiply", [3, 3], 9, timestamp)
        assert len(history) == 3

    def test_len_resets_to_zero_after_clear(self):
        """Test that __len__ is 0 after clear_history."""
        history = OperationHistory()
        timestamp = datetime.now()

        for i in range(5):
            history.add_record(f"op{i}", [i], i, timestamp)
        assert len(history) == 5

        history.clear_history()
        assert len(history) == 0

    def test_history_with_many_records(self):
        """Test history with many records (stress test)."""
        history = OperationHistory()
        timestamp = datetime.now()
        num_records = 100

        for i in range(num_records):
            history.add_record(f"op{i}", [i], i * 2, timestamp)

        assert len(history) == num_records
        records = history.get_history()
        assert len(records) == num_records
        assert records[0].operation_name == "op0"
        assert records[-1].operation_name == "op99"

    def test_history_with_identical_operations(self):
        """Test history with multiple identical operations."""
        history = OperationHistory()
        timestamp = datetime.now()

        for i in range(5):
            history.add_record("add", [2, 3], 5, timestamp)

        assert len(history) == 5
        records = history.get_history()
        for record in records:
            assert record.operation_name == "add"
            assert record.result == 5

    def test_history_with_special_values(self):
        """Test history with special numeric values."""
        history = OperationHistory()
        timestamp = datetime.now()

        history.add_record("special", [float('inf')], float('inf'), timestamp)
        history.add_record("special", [float('-inf')], float('-inf'), timestamp)

        records = history.get_history()
        assert len(records) == 2
        # Note: NaN != NaN, so we can't compare directly

    def test_history_with_none_as_result(self):
        """Test history can record None as result."""
        history = OperationHistory()
        timestamp = datetime.now()

        history.add_record("some_op", [5], None, timestamp)
        records = history.get_history()
        assert records[0].result is None

    def test_history_with_empty_operands(self):
        """Test history can record operations with empty operands."""
        history = OperationHistory()
        timestamp = datetime.now()

        history.add_record("constant_op", [], 42, timestamp)
        records = history.get_history()
        assert records[0].operands == []
        assert records[0].result == 42

    def test_get_history_list_type(self):
        """Test that get_history returns a list."""
        history = OperationHistory()
        result = history.get_history()
        assert isinstance(result, list)

    def test_add_record_with_large_operands_list(self):
        """Test adding a record with a large operands list."""
        history = OperationHistory()
        timestamp = datetime.now()
        large_operands = list(range(1000))

        history.add_record("large_op", large_operands, sum(large_operands), timestamp)

        records = history.get_history()
        assert len(records[0].operands) == 1000

    def test_multiple_clear_and_add_cycles(self):
        """Test multiple cycles of adding and clearing history."""
        history = OperationHistory()
        timestamp = datetime.now()

        for cycle in range(3):
            history.add_record("add", [1, 2], 3, timestamp)
            history.add_record("multiply", [3, 4], 12, timestamp)
            assert len(history) == 2

            history.clear_history()
            assert len(history) == 0

    def test_history_with_different_timestamp_values(self):
        """Test history preserves different timestamp values."""
        history = OperationHistory()
        ts1 = datetime(2025, 1, 1, 12, 0, 0)
        ts2 = datetime(2025, 1, 1, 12, 0, 1)
        ts3 = datetime(2025, 1, 1, 12, 0, 2)

        history.add_record("op1", [1], 1, ts1)
        history.add_record("op2", [2], 2, ts2)
        history.add_record("op3", [3], 3, ts3)

        records = history.get_history()
        assert records[0].timestamp == ts1
        assert records[1].timestamp == ts2
        assert records[2].timestamp == ts3

    def test_history_record_is_operation_record_type(self):
        """Test that records retrieved are OperationRecord instances."""
        history = OperationHistory()
        timestamp = datetime.now()
        history.add_record("add", [5, 3], 8, timestamp)

        records = history.get_history()
        assert isinstance(records[0], OperationRecord)

    def test_history_get_after_many_operations(self):
        """Test getting history after many add operations."""
        history = OperationHistory()
        timestamp = datetime.now()

        operations = ["add", "subtract", "multiply", "divide", "power"]
        for op in operations:
            history.add_record(op, [1, 2], 3, timestamp)

        records = history.get_history()
        assert len(records) == len(operations)
        assert [r.operation_name for r in records] == operations
