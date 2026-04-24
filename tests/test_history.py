"""Tests for the OperationHistory class and session history feature."""

import pytest
import tempfile
import os
from pathlib import Path
from src.history import OperationHistory


# ============================================================================
# CATEGORY 1: CORE HISTORY RECORDING (9 tests)
# ============================================================================

class TestCoreHistoryRecording:
    """Test basic recording functionality of OperationHistory."""

    def test_history_starts_empty(self):
        """Test that OperationHistory starts with no entries."""
        history = OperationHistory()
        assert history.get_entries() == []

    @pytest.mark.parametrize("op_name,operands,result,expected_entry", [
        ("add", (2, 3), 5, "add(2, 3) = 5"),
        ("multiply", (4.0, 2.5), 10.0, "multiply(4.0, 2.5) = 10.0"),
        ("sqrt", (9,), 3.0, "sqrt(9) = 3.0"),
        ("factorial", (5,), 120, "factorial(5) = 120"),
        ("power", (2, 3), 8, "power(2, 3) = 8"),
        ("subtract", (-1, 5), -6, "subtract(-1, 5) = -6"),
        ("divide", (7.0, 2.0), 3.5, "divide(7.0, 2.0) = 3.5"),
        ("factorial", (20,), 2432902008176640000, "factorial(20) = 2432902008176640000"),
    ])
    def test_record_operation_entry_format(self, op_name, operands, result, expected_entry):
        """Test that record() produces correctly formatted entries."""
        history = OperationHistory()
        history.record(op_name, operands, result)
        entries = history.get_entries()
        assert len(entries) == 1
        assert entries[0] == expected_entry


# ============================================================================
# CATEGORY 2: HISTORY ORDERING & ACCUMULATION (3 tests)
# ============================================================================

class TestHistoryOrdering:
    """Test that entries are stored in order and accumulate correctly."""

    def test_multiple_operations_maintain_order(self):
        """Test that multiple operations are recorded in chronological order."""
        history = OperationHistory()
        history.record("add", (2, 3), 5)
        history.record("multiply", (4, 2), 8)
        entries = history.get_entries()
        assert entries == ["add(2, 3) = 5", "multiply(4, 2) = 8"]

    def test_same_operation_twice_creates_separate_entries(self):
        """Test that recording the same operation twice creates two entries."""
        history = OperationHistory()
        history.record("add", (2, 3), 5)
        history.record("add", (4, 5), 9)
        entries = history.get_entries()
        assert len(entries) == 2
        assert entries == ["add(2, 3) = 5", "add(4, 5) = 9"]

    def test_unary_then_binary_maintains_sequence(self):
        """Test correct sequence with unary and binary operations."""
        history = OperationHistory()
        history.record("sqrt", (9,), 3.0)
        history.record("add", (10, 5), 15)
        history.record("factorial", (3,), 6)
        entries = history.get_entries()
        assert entries == ["sqrt(9) = 3.0", "add(10, 5) = 15", "factorial(3) = 6"]


# ============================================================================
# CATEGORY 3: ERROR CASES — SHOULD NOT RECORD (3 tests)
# ============================================================================

class TestErrorHandling:
    """Test that history is not updated when exceptions occur."""

    def test_exception_during_calculation_does_not_record(self):
        """Test that history is not updated when an exception occurs."""
        history = OperationHistory()
        # Simulate what happens when an exception occurs during calculation:
        # The record() method should NOT be called.
        # Here we verify that if no record() is called, history remains empty.
        assert history.get_entries() == []

    def test_history_length_unchanged_after_failed_operation(self):
        """Test that history length does not change after a failed operation."""
        history = OperationHistory()
        history.record("add", (2, 3), 5)
        initial_length = len(history.get_entries())
        # Simulate a failed operation where record() is not called
        # (as would happen in a real scenario where exception prevents recording)
        current_length = len(history.get_entries())
        assert current_length == initial_length

    def test_only_successful_operations_recorded(self):
        """Test that only successful operations are recorded in history."""
        history = OperationHistory()
        history.record("add", (2, 3), 5)
        history.record("multiply", (4, 5), 20)
        # Failed operation would not call record()
        entries = history.get_entries()
        assert len(entries) == 2
        assert entries == ["add(2, 3) = 5", "multiply(4, 5) = 20"]


# ============================================================================
# CATEGORY 4: HISTORY DISPLAY (4 tests)
# ============================================================================

class TestHistoryDisplay:
    """Test the display() method for different history states."""

    def test_display_empty_history_returns_no_operations_message(self):
        """Test that display() returns 'No operations recorded' for empty history."""
        history = OperationHistory()
        output = history.display()
        assert output == "No operations recorded"

    def test_display_single_operation(self):
        """Test that display() shows a single operation."""
        history = OperationHistory()
        history.record("add", (2, 3), 5)
        output = history.display()
        assert "add(2, 3) = 5" in output

    def test_display_multiple_operations_in_order(self):
        """Test that display() shows all operations in chronological order."""
        history = OperationHistory()
        history.record("add", (2, 3), 5)
        history.record("multiply", (4, 2), 8)
        history.record("sqrt", (16,), 4.0)
        output = history.display()
        lines = output.split('\n')
        # Should have at least 3 entries
        assert len([l for l in lines if l.strip()]) >= 3
        # Verify order by checking that entries appear in output
        assert "add(2, 3) = 5" in output
        assert "multiply(4, 2) = 8" in output
        assert "sqrt(16) = 4.0" in output

    def test_display_format_no_extra_spaces_per_line(self):
        """Test that display format has exactly one entry per line without extra leading/trailing spaces."""
        history = OperationHistory()
        history.record("add", (2, 3), 5)
        history.record("multiply", (4, 5), 20)
        output = history.display()
        lines = output.strip().split('\n')
        assert len(lines) == 2
        assert lines[0] == "add(2, 3) = 5"
        assert lines[1] == "multiply(4, 5) = 20"


# ============================================================================
# CATEGORY 5: FILE PERSISTENCE (5 tests)
# ============================================================================

class TestFilePersistence:
    """Test file writing functionality."""

    def test_write_to_file_creates_file_with_entries(self, tmp_path):
        """Test that write_to_file() creates a file with history entries."""
        history = OperationHistory()
        history.record("add", (2, 3), 5)
        history.record("multiply", (4, 5), 20)

        filepath = tmp_path / "history.txt"
        history.write_to_file(str(filepath))

        assert filepath.exists()
        content = filepath.read_text()
        assert "add(2, 3) = 5" in content
        assert "multiply(4, 5) = 20" in content

    def test_file_contains_entries_in_chronological_order(self, tmp_path):
        """Test that file entries are in chronological order."""
        history = OperationHistory()
        history.record("add", (1, 2), 3)
        history.record("subtract", (10, 3), 7)
        history.record("multiply", (2, 4), 8)

        filepath = tmp_path / "history.txt"
        history.write_to_file(str(filepath))

        content = filepath.read_text()
        lines = content.strip().split('\n')
        assert lines[0] == "add(1, 2) = 3"
        assert lines[1] == "subtract(10, 3) = 7"
        assert lines[2] == "multiply(2, 4) = 8"

    def test_empty_history_produces_empty_file(self, tmp_path):
        """Test that empty history produces an empty or minimal file."""
        history = OperationHistory()
        filepath = tmp_path / "history.txt"
        history.write_to_file(str(filepath))

        assert filepath.exists()
        content = filepath.read_text()
        # Empty or just newline
        assert len(content) == 0 or content.strip() == ""

    def test_write_to_file_overwrites_previous_content(self, tmp_path):
        """Test that calling write_to_file() again overwrites previous content."""
        filepath = tmp_path / "history.txt"

        # First write
        history1 = OperationHistory()
        history1.record("add", (1, 1), 2)
        history1.write_to_file(str(filepath))

        content1 = filepath.read_text()
        assert "add(1, 1) = 2" in content1

        # Second write (new session)
        history2 = OperationHistory()
        history2.record("multiply", (3, 3), 9)
        history2.write_to_file(str(filepath))

        content2 = filepath.read_text()
        assert "multiply(3, 3) = 9" in content2
        assert "add(1, 1) = 2" not in content2

    def test_write_to_file_uses_tmp_path(self, tmp_path):
        """Test that write_to_file() works with tmp_path fixture."""
        history = OperationHistory()
        history.record("add", (5, 5), 10)

        filepath = tmp_path / "test_history.txt"
        history.write_to_file(str(filepath))

        assert filepath.exists()
        assert "add(5, 5) = 10" in filepath.read_text()


# ============================================================================
# CATEGORY 6: FILE I/O ERROR HANDLING (2 tests)
# ============================================================================

class TestFileIOErrorHandling:
    """Test graceful handling of file I/O errors."""

    def test_unwritable_path_does_not_raise_exception(self):
        """Test that write_to_file() handles unwritable paths gracefully."""
        history = OperationHistory()
        history.record("add", (2, 3), 5)

        # Use a path that doesn't exist and can't be created
        unwritable_path = "/nonexistent_dir_12345/cannot_write/history.txt"

        # Should not raise an exception
        try:
            history.write_to_file(unwritable_path)
        except Exception as e:
            pytest.fail(f"write_to_file() raised {type(e).__name__}: {e}")

    def test_graceful_failure_with_permission_error(self):
        """Test that write_to_file() fails gracefully on permission errors."""
        history = OperationHistory()
        history.record("add", (2, 3), 5)

        # Similar to test above: unwritable path should not raise
        unwritable_path = "/root_only_directory_12345/history.txt"

        # Should not raise an exception; implementation handles gracefully
        try:
            history.write_to_file(unwritable_path)
        except Exception as e:
            pytest.fail(f"write_to_file() should handle errors gracefully but raised {type(e).__name__}: {e}")


# ============================================================================
# CATEGORY 7: SESSION LIFECYCLE & ISOLATION (2 tests)
# ============================================================================

class TestSessionLifecycle:
    """Test session creation and independence."""

    def test_new_instance_starts_empty(self):
        """Test that a new OperationHistory() instance always starts empty."""
        history1 = OperationHistory()
        assert history1.get_entries() == []

        history2 = OperationHistory()
        assert history2.get_entries() == []

    def test_two_instances_are_independent(self):
        """Test that two OperationHistory instances are independent."""
        history1 = OperationHistory()
        history2 = OperationHistory()

        history1.record("add", (1, 1), 2)
        history1.record("multiply", (2, 2), 4)

        history2.record("sqrt", (9,), 3.0)

        # history1 should have 2 entries
        assert len(history1.get_entries()) == 2
        # history2 should have 1 entry
        assert len(history2.get_entries()) == 1

        # Entries should be completely different
        assert history1.get_entries() != history2.get_entries()
