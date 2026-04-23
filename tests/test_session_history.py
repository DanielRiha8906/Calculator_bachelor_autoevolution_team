"""Unit tests for SessionHistory class."""

import pytest
from src.session_history import SessionHistory


class TestSessionHistoryInitialization:
    """Test suite for SessionHistory initialization."""

    def test_init_empty(self):
        """Verify that a new SessionHistory instance starts empty."""
        history = SessionHistory()
        assert history.is_empty() is True
        assert history.get_history() == []


class TestSessionHistoryRecordOperation:
    """Test suite for SessionHistory.record_operation()."""

    def test_record_single_operation(self):
        """Verify that a single operation is recorded correctly."""
        history = SessionHistory()
        history.record_operation("add", [1.0, 2.0], 3.0)

        entries = history.get_history()
        assert len(entries) == 1
        assert entries[0] == {
            "operation": "add",
            "operands": [1.0, 2.0],
            "result": 3.0,
        }

    def test_record_multiple_operations(self):
        """Verify that multiple operations are stored in order."""
        history = SessionHistory()
        history.record_operation("add", [1.0, 2.0], 3.0)
        history.record_operation("multiply", [3.0, 4.0], 12.0)
        history.record_operation("divide", [12.0, 2.0], 6.0)

        entries = history.get_history()
        assert len(entries) == 3
        assert entries[0]["operation"] == "add"
        assert entries[1]["operation"] == "multiply"
        assert entries[2]["operation"] == "divide"

    def test_record_operation_with_single_operand(self):
        """Verify recording of unary operations."""
        history = SessionHistory()
        history.record_operation("square", [5.0], 25.0)

        entries = history.get_history()
        assert len(entries) == 1
        assert entries[0]["operands"] == [5.0]
        assert entries[0]["result"] == 25.0

    def test_record_operation_with_negative_operands(self):
        """Verify recording with negative operands."""
        history = SessionHistory()
        history.record_operation("add", [-5.0, 3.0], -2.0)

        entries = history.get_history()
        assert entries[0]["operands"] == [-5.0, 3.0]
        assert entries[0]["result"] == -2.0

    def test_record_operation_with_zero_result(self):
        """Verify recording when result is zero."""
        history = SessionHistory()
        history.record_operation("subtract", [5.0, 5.0], 0.0)

        entries = history.get_history()
        assert entries[0]["result"] == 0.0

    def test_record_operation_operands_copied(self):
        """Verify that operands list is copied (not referenced)."""
        history = SessionHistory()
        operands = [1.0, 2.0]
        history.record_operation("add", operands, 3.0)
        operands[0] = 999.0

        entries = history.get_history()
        assert entries[0]["operands"] == [1.0, 2.0]


class TestSessionHistoryGetHistory:
    """Test suite for SessionHistory.get_history()."""

    def test_get_history_returns_list_of_dicts(self):
        """Verify get_history returns list with correct dict keys."""
        history = SessionHistory()
        history.record_operation("add", [1.0, 2.0], 3.0)

        result = history.get_history()
        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert set(result[0].keys()) == {"operation", "operands", "result"}

    def test_get_history_returns_copy(self):
        """Verify get_history returns a copy, not a reference."""
        history = SessionHistory()
        history.record_operation("add", [1.0, 2.0], 3.0)

        entries1 = history.get_history()
        entries1.append({"operation": "fake", "operands": [], "result": 0.0})

        entries2 = history.get_history()
        assert len(entries2) == 1


class TestSessionHistoryDisplayHistory:
    """Test suite for SessionHistory.display_history()."""

    def test_display_history_empty(self):
        """Verify display_history returns correct message when empty."""
        history = SessionHistory()
        assert history.display_history() == "No history yet."

    def test_display_history_single_entry(self):
        """Verify display_history formats a single entry correctly."""
        history = SessionHistory()
        history.record_operation("add", [1.0, 2.0], 3.0)

        display = history.display_history()
        assert display == "1. add(1.0, 2.0) = 3.0"

    def test_display_history_multiple_entries(self):
        """Verify display_history formats multiple entries with numbering."""
        history = SessionHistory()
        history.record_operation("add", [1.0, 2.0], 3.0)
        history.record_operation("multiply", [3.0, 4.0], 12.0)
        history.record_operation("divide", [12.0, 2.0], 6.0)

        display = history.display_history()
        lines = display.split("\n")
        assert len(lines) == 3
        assert lines[0] == "1. add(1.0, 2.0) = 3.0"
        assert lines[1] == "2. multiply(3.0, 4.0) = 12.0"
        assert lines[2] == "3. divide(12.0, 2.0) = 6.0"

    def test_display_history_single_operand_operation(self):
        """Verify display of unary operations."""
        history = SessionHistory()
        history.record_operation("square", [5.0], 25.0)

        display = history.display_history()
        assert display == "1. square(5.0) = 25.0"

    def test_display_history_with_negative_numbers(self):
        """Verify formatting with negative operands and results."""
        history = SessionHistory()
        history.record_operation("add", [-5.0, 3.0], -2.0)

        display = history.display_history()
        assert display == "1. add(-5.0, 3.0) = -2.0"

    def test_display_history_with_fractional_results(self):
        """Verify display of fractional results."""
        history = SessionHistory()
        history.record_operation("divide", [5.0, 2.0], 2.5)

        display = history.display_history()
        assert display == "1. divide(5.0, 2.0) = 2.5"


class TestSessionHistoryClear:
    """Test suite for SessionHistory.clear()."""

    def test_clear_history(self):
        """Verify that clear() removes all operations."""
        history = SessionHistory()
        history.record_operation("add", [1.0, 2.0], 3.0)
        history.record_operation("multiply", [3.0, 4.0], 12.0)

        history.clear()

        assert history.is_empty() is True
        assert history.get_history() == []

    def test_clear_empty_history(self):
        """Verify that clear() on empty history is idempotent."""
        history = SessionHistory()
        history.clear()

        assert history.is_empty() is True

    def test_clear_and_record_again(self):
        """Verify that operations can be recorded after clearing."""
        history = SessionHistory()
        history.record_operation("add", [1.0, 2.0], 3.0)
        history.clear()
        history.record_operation("subtract", [5.0, 3.0], 2.0)

        entries = history.get_history()
        assert len(entries) == 1
        assert entries[0]["operation"] == "subtract"


class TestSessionHistoryIsEmpty:
    """Test suite for SessionHistory.is_empty()."""

    def test_is_empty_true_initially(self):
        """Verify is_empty returns True before any records."""
        history = SessionHistory()
        assert history.is_empty() is True

    def test_is_empty_false_after_record(self):
        """Verify is_empty returns False after recording one operation."""
        history = SessionHistory()
        history.record_operation("add", [1.0, 2.0], 3.0)
        assert history.is_empty() is False

    def test_is_empty_false_multiple_records(self):
        """Verify is_empty returns False with multiple records."""
        history = SessionHistory()
        history.record_operation("add", [1.0, 2.0], 3.0)
        history.record_operation("multiply", [3.0, 4.0], 12.0)
        assert history.is_empty() is False

    def test_is_empty_true_after_clear(self):
        """Verify is_empty returns True after clearing history."""
        history = SessionHistory()
        history.record_operation("add", [1.0, 2.0], 3.0)
        history.clear()
        assert history.is_empty() is True
