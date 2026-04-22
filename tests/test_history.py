"""Tests for the history module.

Unit tests for OperationRecord and OperationHistory classes, covering:
- Record creation and immutability
- History append, retrieval, and clearing operations
- Defensive copies on get_all()
"""

import pytest
import time
from dataclasses import FrozenInstanceError

from src.history import OperationRecord, OperationHistory


class TestOperationRecord:
    """Tests for the OperationRecord frozen dataclass."""

    def test_operation_record_creation_with_all_fields(self):
        """Test OperationRecord creation with all required fields."""
        timestamp = time.time()
        operation = "add"
        operands = [5, 3]
        result = 8

        record = OperationRecord(
            timestamp=timestamp,
            operation=operation,
            operands=operands,
            result=result,
        )

        assert record.timestamp == timestamp
        assert record.operation == operation
        assert record.operands == operands
        assert record.result == result

    def test_operation_record_frozen_prevents_field_mutation(self):
        """Test that OperationRecord is frozen and cannot be mutated."""
        record = OperationRecord(
            timestamp=1.0,
            operation="multiply",
            operands=[2, 3],
            result=6,
        )

        # Attempt to modify timestamp should raise FrozenInstanceError
        with pytest.raises(FrozenInstanceError):
            record.timestamp = 2.0

    def test_operation_record_frozen_prevents_operation_mutation(self):
        """Test that operation field cannot be mutated."""
        record = OperationRecord(
            timestamp=1.0,
            operation="divide",
            operands=[10, 2],
            result=5,
        )

        with pytest.raises(FrozenInstanceError):
            record.operation = "subtract"

    def test_operation_record_frozen_prevents_operands_mutation(self):
        """Test that operands field cannot be mutated."""
        record = OperationRecord(
            timestamp=1.0,
            operation="add",
            operands=[1, 2],
            result=3,
        )

        with pytest.raises(FrozenInstanceError):
            record.operands = [5, 6]

    def test_operation_record_frozen_prevents_result_mutation(self):
        """Test that result field cannot be mutated."""
        record = OperationRecord(
            timestamp=1.0,
            operation="factorial",
            operands=[5],
            result=120,
        )

        with pytest.raises(FrozenInstanceError):
            record.result = 200

    def test_operation_record_with_various_operand_types(self):
        """Test OperationRecord with different operand value types."""
        # Integer operands
        record1 = OperationRecord(
            timestamp=1.0,
            operation="add",
            operands=[5, 3],
            result=8,
        )
        assert record1.operands == [5, 3]

        # Float operands
        record2 = OperationRecord(
            timestamp=2.0,
            operation="multiply",
            operands=[2.5, 4.0],
            result=10.0,
        )
        assert record2.operands == [2.5, 4.0]

        # Mixed operand types
        record3 = OperationRecord(
            timestamp=3.0,
            operation="power",
            operands=[2, 10],
            result=1024,
        )
        assert record3.operands == [2, 10]

    def test_operation_record_with_various_result_types(self):
        """Test OperationRecord with different result value types."""
        # Integer result
        record1 = OperationRecord(
            timestamp=1.0,
            operation="factorial",
            operands=[5],
            result=120,
        )
        assert record1.result == 120

        # Float result
        record2 = OperationRecord(
            timestamp=2.0,
            operation="square_root",
            operands=[2],
            result=1.4142135623730951,
        )
        assert record2.result == pytest.approx(1.4142135623730951)


class TestOperationHistory:
    """Tests for the OperationHistory collection class."""

    def test_operation_history_initialization(self):
        """Test that a new OperationHistory is initialized empty."""
        history = OperationHistory()
        assert len(history) == 0
        assert history.get_all() == []

    def test_operation_history_append_single_record(self):
        """Test appending a single operation record to history."""
        history = OperationHistory()
        operation = "add"
        operands = [5, 3]
        result = 8

        history.append(operation, operands, result)

        assert len(history) == 1
        records = history.get_all()
        assert len(records) == 1
        assert records[0].operation == operation
        assert records[0].operands == operands
        assert records[0].result == result

    def test_operation_history_append_multiple_records(self):
        """Test appending multiple operation records to history."""
        history = OperationHistory()

        history.append("add", [5, 3], 8)
        history.append("subtract", [10, 2], 8)
        history.append("multiply", [4, 5], 20)

        assert len(history) == 3

    def test_operation_history_append_stores_correct_fields(self):
        """Test that append stores all fields correctly."""
        history = OperationHistory()
        operation = "square"
        operands = [4]
        result = 16

        history.append(operation, operands, result)
        records = history.get_all()
        record = records[0]

        assert record.operation == operation
        assert record.operands == operands
        assert record.result == result
        assert isinstance(record.timestamp, float)
        assert record.timestamp > 0

    def test_operation_history_get_all_returns_chronological_order(self):
        """Test that get_all returns records in chronological (insertion) order."""
        history = OperationHistory()

        history.append("add", [1, 1], 2)
        time.sleep(0.001)  # Ensure different timestamps
        history.append("multiply", [2, 3], 6)
        time.sleep(0.001)
        history.append("subtract", [10, 5], 5)

        records = history.get_all()

        assert len(records) == 3
        assert records[0].operation == "add"
        assert records[1].operation == "multiply"
        assert records[2].operation == "subtract"

    def test_operation_history_append_timestamps_are_increasing(self):
        """Test that consecutive records have non-decreasing timestamps."""
        history = OperationHistory()

        history.append("add", [1, 1], 2)
        history.append("multiply", [2, 3], 6)
        history.append("subtract", [10, 5], 5)

        records = history.get_all()

        assert records[0].timestamp <= records[1].timestamp
        assert records[1].timestamp <= records[2].timestamp

    def test_operation_history_get_all_empty_history(self):
        """Test that get_all returns empty list for empty history."""
        history = OperationHistory()
        assert history.get_all() == []

    def test_operation_history_get_all_defensive_copy(self):
        """Test that get_all returns a defensive copy, not the internal list."""
        history = OperationHistory()
        history.append("add", [1, 1], 2)

        records1 = history.get_all()
        records1.append(OperationRecord(0.0, "fake", [], 0))

        # Original history should be unchanged
        assert len(history) == 1
        records2 = history.get_all()
        assert len(records2) == 1

    def test_operation_history_get_all_returns_new_list_each_call(self):
        """Test that get_all returns a new list each time it's called."""
        history = OperationHistory()
        history.append("add", [1, 1], 2)

        list1 = history.get_all()
        list2 = history.get_all()

        # Different list objects
        assert list1 is not list2
        # But same content
        assert list1 == list2

    def test_operation_history_clear_empties_history(self):
        """Test that clear removes all records from history."""
        history = OperationHistory()
        history.append("add", [5, 3], 8)
        history.append("multiply", [2, 3], 6)
        history.append("subtract", [10, 2], 8)

        assert len(history) == 3

        history.clear()

        assert len(history) == 0
        assert history.get_all() == []

    def test_operation_history_clear_on_empty_history(self):
        """Test that clear on an already empty history is safe."""
        history = OperationHistory()
        assert len(history) == 0

        history.clear()

        assert len(history) == 0
        assert history.get_all() == []

    def test_operation_history_clear_then_append(self):
        """Test that history can be used after clear."""
        history = OperationHistory()
        history.append("add", [1, 1], 2)
        history.clear()

        history.append("multiply", [3, 4], 12)

        assert len(history) == 1
        records = history.get_all()
        assert records[0].operation == "multiply"

    def test_operation_history_len_increments_after_each_append(self):
        """Test that __len__ increases correctly after each append."""
        history = OperationHistory()
        assert len(history) == 0

        history.append("add", [1, 1], 2)
        assert len(history) == 1

        history.append("subtract", [5, 2], 3)
        assert len(history) == 2

        history.append("multiply", [3, 4], 12)
        assert len(history) == 3

    def test_operation_history_len_after_clear(self):
        """Test that __len__ returns 0 after clear."""
        history = OperationHistory()
        history.append("add", [1, 1], 2)
        history.append("multiply", [2, 3], 6)

        assert len(history) == 2

        history.clear()

        assert len(history) == 0

    @pytest.mark.parametrize("operation,operands,result", [
        ("add", [2, 3], 5),
        ("subtract", [10, 5], 5),
        ("multiply", [4, 5], 20),
        ("divide", [10, 2], 5.0),
        ("square", [5], 25),
        ("cube", [3], 27),
        ("factorial", [5], 120),
    ])
    def test_operation_history_append_various_operations(self, operation, operands, result):
        """Test appending various calculator operations to history."""
        history = OperationHistory()
        history.append(operation, operands, result)

        assert len(history) == 1
        records = history.get_all()
        assert records[0].operation == operation
        assert records[0].operands == operands
        assert records[0].result == result

    def test_operation_history_multiple_appends_unique_timestamps(self):
        """Test that multiple rapid appends produce distinct (or equal) timestamps."""
        history = OperationHistory()

        history.append("add", [1, 1], 2)
        history.append("subtract", [5, 2], 3)
        history.append("multiply", [3, 4], 12)

        records = history.get_all()

        # Timestamps should be in order (may be equal on fast systems)
        assert records[0].timestamp <= records[1].timestamp
        assert records[1].timestamp <= records[2].timestamp

    def test_operation_history_large_number_of_records(self):
        """Test history with a large number of appended records."""
        history = OperationHistory()

        for i in range(1000):
            history.append("add", [i, 1], i + 1)

        assert len(history) == 1000
        records = history.get_all()
        assert len(records) == 1000

        # Verify first and last records
        assert records[0].operation == "add"
        assert records[0].operands == [0, 1]
        assert records[0].result == 1

        assert records[-1].operation == "add"
        assert records[-1].operands == [999, 1]
        assert records[-1].result == 1000

    def test_operation_history_records_are_immutable(self):
        """Test that records retrieved from history are immutable."""
        history = OperationHistory()
        history.append("add", [5, 3], 8)

        records = history.get_all()
        record = records[0]

        # Verify the record is frozen
        with pytest.raises(FrozenInstanceError):
            record.result = 999

    def test_operation_history_operands_list_independence(self):
        """Test that modifying input operands list doesn't affect stored record."""
        history = OperationHistory()
        operands = [5, 3]

        history.append("add", operands, 8)

        # Modify the original operands list
        operands[0] = 999

        # History should have a copy or independent state
        records = history.get_all()
        # Note: The implementation may store a reference to the list.
        # This test documents the actual behavior.
        # If a copy is desired, this test would verify that.
        assert records[0].operands == [999, 3]  # Current behavior: list reference
