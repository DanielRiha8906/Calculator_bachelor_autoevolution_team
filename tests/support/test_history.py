"""Tests for OperationHistory from src.support.history."""

import os
import pytest
import tempfile
from src.support.history import OperationHistory


class TestOperationHistoryInitialization:
    """Test OperationHistory initialization."""

    def test_history_default_filename(self):
        """Test default history filename."""
        history = OperationHistory()
        assert history.history_file == "history.txt"

    def test_history_custom_filename(self):
        """Test custom history filename."""
        history = OperationHistory("custom_history.txt")
        assert history.history_file == "custom_history.txt"

    def test_history_with_full_path(self):
        """Test history with full path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            assert history.history_file == filepath


class TestOperationHistoryClearHistory:
    """Test OperationHistory.clear_history method."""

    def test_clear_history_creates_file(self):
        """Test that clear_history creates the file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            history.clear_history()
            assert os.path.exists(filepath)

    def test_clear_history_truncates_existing_file(self):
        """Test that clear_history truncates existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            # Create file with content
            with open(filepath, "w") as f:
                f.write("old content\n")

            history = OperationHistory(filepath)
            history.clear_history()

            with open(filepath, "r") as f:
                content = f.read()
            assert content == ""

    def test_clear_history_idempotent(self):
        """Test that clear_history can be called multiple times."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            history.clear_history()
            history.clear_history()  # Should not raise
            assert os.path.exists(filepath)

    def test_clear_history_invalid_directory(self):
        """Test clear_history with invalid directory (gracefully handles error)."""
        history = OperationHistory("/invalid/directory/history.txt")
        # Should not raise, but logs to stderr
        history.clear_history()


class TestOperationHistoryRecordOperation:
    """Test OperationHistory.record_operation method."""

    def test_record_operation_single_entry(self):
        """Test recording a single operation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            history.clear_history()
            history.record_operation("add(2, 3) = 5")

            with open(filepath, "r") as f:
                content = f.read()
            assert content == "add(2, 3) = 5\n"

    def test_record_operation_multiple_entries(self):
        """Test recording multiple operations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            history.clear_history()
            history.record_operation("add(2, 3) = 5")
            history.record_operation("multiply(5, 2) = 10")
            history.record_operation("subtract(10, 5) = 5")

            with open(filepath, "r") as f:
                lines = f.readlines()
            assert len(lines) == 3
            assert lines[0].strip() == "add(2, 3) = 5"
            assert lines[1].strip() == "multiply(5, 2) = 10"
            assert lines[2].strip() == "subtract(10, 5) = 5"

    def test_record_operation_appends_to_existing(self):
        """Test that record_operation appends to existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            history.clear_history()
            history.record_operation("add(2, 3) = 5")
            history.record_operation("multiply(5, 2) = 10")

            with open(filepath, "r") as f:
                lines = f.readlines()
            assert len(lines) == 2

    def test_record_operation_empty_string(self):
        """Test recording empty string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            history.clear_history()
            history.record_operation("")

            with open(filepath, "r") as f:
                content = f.read()
            assert content == "\n"

    def test_record_operation_special_characters(self):
        """Test recording entry with special characters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            history.clear_history()
            entry = "operation: sqrt(-0.5) [error]"
            history.record_operation(entry)

            with open(filepath, "r") as f:
                content = f.read()
            assert content == entry + "\n"

    def test_record_operation_unicode(self):
        """Test recording entry with unicode characters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            history.clear_history()
            entry = "operation: sqrt(2) = 1.414... ✓"
            history.record_operation(entry)

            with open(filepath, "r") as f:
                content = f.read()
            assert content == entry + "\n"

    def test_record_operation_long_entry(self):
        """Test recording very long entry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            history.clear_history()
            entry = "x" * 10000
            history.record_operation(entry)

            with open(filepath, "r") as f:
                content = f.read()
            assert content == entry + "\n"

    def test_record_operation_invalid_directory(self):
        """Test record_operation with invalid directory (gracefully handles)."""
        history = OperationHistory("/invalid/directory/history.txt")
        # Should not raise
        history.record_operation("add(2, 3) = 5")


class TestOperationHistoryDisplayHistory:
    """Test OperationHistory.display_history method."""

    def test_display_history_empty(self):
        """Test display_history with empty history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            history.clear_history()

            result = history.display_history()
            assert result == []

    def test_display_history_nonexistent_file(self):
        """Test display_history with nonexistent file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "nonexistent.txt")
            history = OperationHistory(filepath)

            result = history.display_history()
            assert result == []

    def test_display_history_single_entry(self):
        """Test display_history with single entry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            history.clear_history()
            history.record_operation("add(2, 3) = 5")

            result = history.display_history()
            assert result == ["add(2, 3) = 5"]

    def test_display_history_multiple_entries(self):
        """Test display_history with multiple entries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            history.clear_history()
            entries = [
                "add(2, 3) = 5",
                "multiply(5, 2) = 10",
                "subtract(10, 5) = 5"
            ]
            for entry in entries:
                history.record_operation(entry)

            result = history.display_history()
            assert result == entries

    def test_display_history_strips_newlines(self):
        """Test that display_history strips trailing newlines."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            # Manually write file with newlines
            with open(filepath, "w") as f:
                f.write("add(2, 3) = 5\n")
                f.write("multiply(5, 2) = 10\n")

            history = OperationHistory(filepath)
            result = history.display_history()

            assert result == ["add(2, 3) = 5", "multiply(5, 2) = 10"]
            # Ensure no trailing newlines in entries
            for entry in result:
                assert not entry.endswith("\n")

    def test_display_history_returns_copy(self):
        """Test that display_history returns a fresh list each time."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            history.clear_history()
            history.record_operation("add(2, 3) = 5")

            result1 = history.display_history()
            result2 = history.display_history()

            # Should be equal content but different objects
            assert result1 == result2
            assert result1 is not result2

    def test_display_history_with_special_characters(self):
        """Test display_history with special characters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            history.clear_history()
            entry = "operation: sqrt(-0.5) [error]"
            history.record_operation(entry)

            result = history.display_history()
            assert result == [entry]

    def test_display_history_with_unicode(self):
        """Test display_history with unicode characters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)
            history.clear_history()
            entry = "operation: sqrt(2) = 1.414... ✓"
            history.record_operation(entry)

            result = history.display_history()
            assert result == [entry]


class TestOperationHistoryIntegration:
    """Integration tests for OperationHistory."""

    def test_clear_then_record_then_display(self):
        """Test workflow: clear -> record -> display."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)

            history.clear_history()
            assert history.display_history() == []

            history.record_operation("add(2, 3) = 5")
            history.record_operation("multiply(5, 2) = 10")

            result = history.display_history()
            assert len(result) == 2

    def test_multiple_clear_calls(self):
        """Test that multiple clear calls work correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")
            history = OperationHistory(filepath)

            history.clear_history()
            history.record_operation("add(2, 3) = 5")
            assert len(history.display_history()) == 1

            history.clear_history()
            assert history.display_history() == []

            history.record_operation("subtract(10, 5) = 5")
            assert history.display_history() == ["subtract(10, 5) = 5"]

    def test_session_isolation(self):
        """Test that different instances with same file are isolated."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "history.txt")

            history1 = OperationHistory(filepath)
            history1.clear_history()
            history1.record_operation("add(2, 3) = 5")

            # New instance with same file
            history2 = OperationHistory(filepath)
            result = history2.display_history()

            assert result == ["add(2, 3) = 5"]
