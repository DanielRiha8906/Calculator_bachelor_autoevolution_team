"""Comprehensive pytest tests for the OperationHistory feature.

Tests cover:
- OperationHistory.__init__: custom file paths, defaults
- OperationHistory.clear_history: creates/truncates file, error handling
- OperationHistory.record_operation: appends entries, format correctness
- OperationHistory.display_history: reads back history, handles missing files
- Integration with REPLInterface and CLIHandler
- File isolation between sessions
- Graceful error handling (non-writable paths)
- Special characters, floats, and edge cases
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import patch, Mock
from io import StringIO

from src.history import OperationHistory
from src.repl import REPLInterface
from src.cli import CLIHandler
from src.calculator import Calculator


# ==============================================================================
# FIXTURES
# ==============================================================================

@pytest.fixture
def tmp_history_file(tmp_path):
    """Provide a temporary history file path for test isolation."""
    return str(tmp_path / "history.txt")


@pytest.fixture
def history(tmp_history_file):
    """Provide an OperationHistory instance with a temporary file."""
    return OperationHistory(history_file=tmp_history_file)


@pytest.fixture
def calculator():
    """Provide a Calculator instance."""
    return Calculator()


@pytest.fixture
def repl_with_history(calculator, tmp_history_file):
    """Provide a REPLInterface with history integration."""
    hist = OperationHistory(history_file=tmp_history_file)
    repl = REPLInterface(calculator, history=hist)
    return repl, hist, tmp_history_file


@pytest.fixture
def cli_with_history(calculator, tmp_history_file):
    """Provide a CLIHandler with history integration."""
    hist = OperationHistory(history_file=tmp_history_file)
    cli = CLIHandler(calculator, history=hist)
    return cli, hist, tmp_history_file


# ==============================================================================
# TESTS: OperationHistory.__init__
# ==============================================================================

class TestOperationHistoryInit:
    """Test suite for OperationHistory.__init__."""

    def test_init_with_default_file(self):
        """Test initialization with default history file name."""
        history = OperationHistory()
        assert history.history_file == "history.txt"

    def test_init_with_custom_file_path(self, tmp_path):
        """Test initialization with custom file path."""
        custom_path = str(tmp_path / "custom_history.txt")
        history = OperationHistory(history_file=custom_path)
        assert history.history_file == custom_path

    def test_init_with_absolute_path(self, tmp_path):
        """Test initialization with absolute path."""
        abs_path = str(tmp_path.absolute() / "history.txt")
        history = OperationHistory(history_file=abs_path)
        assert history.history_file == abs_path

    def test_init_with_relative_path(self):
        """Test initialization with relative path."""
        history = OperationHistory(history_file="subdir/history.txt")
        assert history.history_file == "subdir/history.txt"


# ==============================================================================
# TESTS: OperationHistory.clear_history
# ==============================================================================

class TestClearHistory:
    """Test suite for clear_history method."""

    def test_clear_history_creates_new_file_if_missing(self, tmp_history_file):
        """Test that clear_history creates file when it doesn't exist."""
        assert not os.path.exists(tmp_history_file)
        history = OperationHistory(history_file=tmp_history_file)
        history.clear_history()
        assert os.path.exists(tmp_history_file)
        assert os.path.getsize(tmp_history_file) == 0

    def test_clear_history_truncates_existing_file(self, tmp_history_file):
        """Test that clear_history truncates an existing file."""
        # Create a file with content
        with open(tmp_history_file, "w") as f:
            f.write("old content\n" * 10)
        assert os.path.getsize(tmp_history_file) > 0

        # Clear history
        history = OperationHistory(history_file=tmp_history_file)
        history.clear_history()

        assert os.path.exists(tmp_history_file)
        assert os.path.getsize(tmp_history_file) == 0

    def test_clear_history_multiple_times(self, tmp_history_file):
        """Test that clear_history can be called multiple times safely."""
        history = OperationHistory(history_file=tmp_history_file)
        history.clear_history()
        history.clear_history()
        history.clear_history()
        assert os.path.exists(tmp_history_file)
        assert os.path.getsize(tmp_history_file) == 0

    def test_clear_history_error_handling(self):
        """Test that clear_history handles OSError gracefully."""
        # Use a non-existent directory path (will cause permission error)
        bad_path = "/invalid_nonexistent_directory_12345/history.txt"
        history = OperationHistory(history_file=bad_path)

        # Should not raise; error logged to stderr
        with patch("sys.stderr", new_callable=StringIO):
            history.clear_history()  # Should not crash


# ==============================================================================
# TESTS: OperationHistory.record_operation
# ==============================================================================

class TestRecordOperation:
    """Test suite for record_operation method."""

    def test_record_operation_single_entry(self, history, tmp_history_file):
        """Test recording a single operation entry."""
        history.clear_history()
        history.record_operation("add(2, 3) = 5")

        with open(tmp_history_file, "r") as f:
            content = f.read()
        assert "add(2, 3) = 5\n" == content

    def test_record_operation_multiple_entries(self, history, tmp_history_file):
        """Test recording multiple operation entries."""
        history.clear_history()
        history.record_operation("add(2, 3) = 5")
        history.record_operation("multiply(4, 5) = 20")
        history.record_operation("divide(10, 2) = 5.0")

        with open(tmp_history_file, "r") as f:
            lines = f.readlines()

        assert len(lines) == 3
        assert lines[0] == "add(2, 3) = 5\n"
        assert lines[1] == "multiply(4, 5) = 20\n"
        assert lines[2] == "divide(10, 2) = 5.0\n"

    def test_record_operation_preserves_order(self, history, tmp_history_file):
        """Test that multiple entries are recorded in order."""
        history.clear_history()
        for i in range(5):
            history.record_operation(f"operation_{i}")

        with open(tmp_history_file, "r") as f:
            lines = [line.rstrip("\n") for line in f.readlines()]

        assert lines == ["operation_0", "operation_1", "operation_2",
                        "operation_3", "operation_4"]

    def test_record_operation_with_float_result(self, history, tmp_history_file):
        """Test recording entry with float result."""
        history.clear_history()
        history.record_operation("divide(10, 3) = 3.3333333333")

        with open(tmp_history_file, "r") as f:
            content = f.read()
        assert "divide(10, 3) = 3.3333333333\n" == content

    def test_record_operation_with_special_characters(self, history, tmp_history_file):
        """Test recording entry with special characters."""
        history.clear_history()
        entry = "operation(±2, ~3) = (special!)"
        history.record_operation(entry)

        with open(tmp_history_file, "r") as f:
            content = f.read()
        assert entry + "\n" in content

    def test_record_operation_with_unicode(self, history, tmp_history_file):
        """Test recording entry with unicode characters."""
        history.clear_history()
        entry = "operation(π, e) = ∑"
        history.record_operation(entry)

        with open(tmp_history_file, "r") as f:
            content = f.read()
        assert entry + "\n" == content

    def test_record_operation_empty_string(self, history, tmp_history_file):
        """Test recording an empty string entry."""
        history.clear_history()
        history.record_operation("")

        with open(tmp_history_file, "r") as f:
            content = f.read()
        assert content == "\n"

    def test_record_operation_entry_with_newline_chars(self, history, tmp_history_file):
        """Test that entry is written as-is followed by one newline."""
        history.clear_history()
        history.record_operation("entry_without_newline")

        with open(tmp_history_file, "r") as f:
            content = f.read()
        assert content == "entry_without_newline\n"

    def test_record_operation_append_mode(self, history, tmp_history_file):
        """Test that multiple calls append (not overwrite)."""
        history.clear_history()
        history.record_operation("first")
        history.record_operation("second")
        history.record_operation("third")

        with open(tmp_history_file, "r") as f:
            lines = f.readlines()
        assert len(lines) == 3

    def test_record_operation_error_handling(self):
        """Test that record_operation handles OSError gracefully."""
        bad_path = "/invalid_nonexistent_directory_12345/history.txt"
        history = OperationHistory(history_file=bad_path)

        # Should not raise; error logged to stderr
        with patch("sys.stderr", new_callable=StringIO):
            history.record_operation("test_entry")  # Should not crash

    def test_record_operation_very_long_entry(self, history, tmp_history_file):
        """Test recording a very long entry."""
        history.clear_history()
        long_entry = "x" * 10000
        history.record_operation(long_entry)

        with open(tmp_history_file, "r") as f:
            content = f.read()
        assert long_entry + "\n" == content


# ==============================================================================
# TESTS: OperationHistory.display_history
# ==============================================================================

class TestDisplayHistory:
    """Test suite for display_history method."""

    def test_display_history_empty_file(self, history, tmp_history_file):
        """Test display_history with empty file."""
        history.clear_history()
        result = history.display_history()
        assert result == []

    def test_display_history_single_entry(self, history, tmp_history_file):
        """Test display_history with single entry."""
        history.clear_history()
        history.record_operation("add(2, 3) = 5")
        result = history.display_history()
        assert result == ["add(2, 3) = 5"]

    def test_display_history_multiple_entries(self, history, tmp_history_file):
        """Test display_history with multiple entries."""
        history.clear_history()
        history.record_operation("add(2, 3) = 5")
        history.record_operation("multiply(4, 5) = 20")
        history.record_operation("divide(10, 2) = 5.0")

        result = history.display_history()
        assert result == [
            "add(2, 3) = 5",
            "multiply(4, 5) = 20",
            "divide(10, 2) = 5.0"
        ]

    def test_display_history_strips_newlines(self, history, tmp_history_file):
        """Test that display_history strips trailing newlines."""
        history.clear_history()
        history.record_operation("entry1")
        history.record_operation("entry2")

        result = history.display_history()
        for entry in result:
            assert not entry.endswith("\n")

    def test_display_history_missing_file_returns_empty_list(self, tmp_path):
        """Test that display_history returns [] when file doesn't exist."""
        nonexistent_path = str(tmp_path / "nonexistent.txt")
        history = OperationHistory(history_file=nonexistent_path)

        result = history.display_history()
        assert result == []

    def test_display_history_preserves_order(self, history, tmp_history_file):
        """Test that display_history preserves entry order."""
        history.clear_history()
        entries = [f"operation_{i}" for i in range(10)]
        for entry in entries:
            history.record_operation(entry)

        result = history.display_history()
        assert result == entries

    def test_display_history_with_special_characters(self, history, tmp_history_file):
        """Test display_history with special character entries."""
        history.clear_history()
        special_entry = "op(π, e) = ∞"
        history.record_operation(special_entry)

        result = history.display_history()
        assert result == [special_entry]

    def test_display_history_with_float_results(self, history, tmp_history_file):
        """Test display_history with float results."""
        history.clear_history()
        history.record_operation("divide(10, 3) = 3.3333333333")
        history.record_operation("sqrt(2) = 1.41421356")

        result = history.display_history()
        assert "3.3333333333" in result[0]
        assert "1.41421356" in result[1]

    def test_display_history_after_clear(self, history, tmp_history_file):
        """Test that display_history returns empty list after clear."""
        history.clear_history()
        history.record_operation("entry1")
        history.record_operation("entry2")

        # Clear and verify
        history.clear_history()
        result = history.display_history()
        assert result == []

    def test_display_history_error_handling_permission_denied(self, tmp_path):
        """Test display_history graceful handling of permission errors."""
        # Create a file, then remove read permission
        history_file = tmp_path / "history.txt"
        history_file.write_text("some content\n")

        history = OperationHistory(history_file=str(history_file))

        # Remove read permission
        os.chmod(str(history_file), 0o000)

        try:
            # Should not raise; error logged to stderr
            with patch("sys.stderr", new_callable=StringIO):
                result = history.display_history()
            assert result == []
        finally:
            # Restore permission for cleanup
            os.chmod(str(history_file), 0o644)

    def test_display_history_returns_list_type(self, history, tmp_history_file):
        """Test that display_history always returns a list."""
        history.clear_history()
        result = history.display_history()
        assert isinstance(result, list)

        history.record_operation("test")
        result = history.display_history()
        assert isinstance(result, list)


# ==============================================================================
# TESTS: Integration - REPLInterface with history
# ==============================================================================

class TestREPLInterfaceWithHistory:
    """Test suite for REPLInterface integration with history."""

    def test_repl_valid_operation_input_history(self, calculator, tmp_history_file):
        """Test that 'history' is recognized as valid operation input."""
        hist = OperationHistory(history_file=tmp_history_file)
        repl = REPLInterface(calculator, history=hist)

        assert repl._is_valid_operation_input("history") is True

    def test_repl_valid_operation_input_history_case_insensitive(self, calculator, tmp_history_file):
        """Test that 'history' is case-insensitive."""
        hist = OperationHistory(history_file=tmp_history_file)
        repl = REPLInterface(calculator, history=hist)

        assert repl._is_valid_operation_input("HISTORY") is True
        assert repl._is_valid_operation_input("History") is True
        assert repl._is_valid_operation_input("HiStOrY") is True

    def test_repl_get_operation_selection_returns_history(self, calculator, tmp_history_file):
        """Test that get_operation_selection returns 'history' for history input."""
        hist = OperationHistory(history_file=tmp_history_file)
        repl = REPLInterface(calculator, history=hist)

        with patch("builtins.input", return_value="history"):
            result = repl.get_operation_selection()
        assert result == "history"

    def test_repl_records_operation_when_history_provided(self, repl_with_history, capsys):
        """Test that operations are recorded when history object is provided."""
        repl, hist, tmp_history_file = repl_with_history
        hist.clear_history()

        # Mock input to execute one add operation then quit
        with patch("builtins.input", side_effect=["1", "5", "3", "quit"]):
            repl.run()

        # Verify operation was recorded
        result = hist.display_history()
        assert len(result) == 1
        assert "add(5.0, 3.0) = 8.0" in result[0]

    def test_repl_records_multiple_operations_in_order(self, repl_with_history, capsys):
        """Test that multiple operations are recorded in order."""
        repl, hist, tmp_history_file = repl_with_history
        hist.clear_history()

        # Execute: add(2, 3), multiply(5, 4), quit
        # Menu for add, operand1, operand2, menu for multiply, operand1, operand2, quit
        with patch("builtins.input", side_effect=["1", "2", "3", "3", "5", "4", "quit"]):
            repl.run()

        result = hist.display_history()
        assert len(result) == 2
        assert "add(2.0, 3.0) = 5.0" in result[0]
        assert "multiply(5.0, 4.0) = 20.0" in result[1]

    def test_repl_without_history_skips_recording(self, calculator, capsys):
        """Test that recording is skipped when history is None."""
        repl = REPLInterface(calculator, history=None)

        # Should not crash when executing operations
        with patch("builtins.input", side_effect=["1", "5", "3", "quit"]):
            repl.run()

        # No error should occur
        captured = capsys.readouterr()
        assert "Addition" in captured.out

    def test_repl_displays_history_when_available(self, repl_with_history, capsys):
        """Test that history is displayed when user selects history option."""
        repl, hist, tmp_history_file = repl_with_history
        hist.clear_history()
        hist.record_operation("add(2, 3) = 5")
        hist.record_operation("multiply(4, 5) = 20")

        # Input: history (display), quit
        with patch("builtins.input", side_effect=["history", "quit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "Operation history" in captured.out
        assert "add(2, 3) = 5" in captured.out
        assert "multiply(4, 5) = 20" in captured.out

    def test_repl_displays_no_history_when_empty(self, repl_with_history, capsys):
        """Test that 'No history recorded yet.' is shown when history is empty."""
        repl, hist, tmp_history_file = repl_with_history
        hist.clear_history()

        # Input: history (display), quit
        with patch("builtins.input", side_effect=["history", "quit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "No history recorded yet" in captured.out

    def test_repl_without_history_shows_unavailable_message(self, calculator, capsys):
        """Test that history unavailable message is shown when history is None."""
        repl = REPLInterface(calculator, history=None)

        # Input: history (try to display), quit
        with patch("builtins.input", side_effect=["history", "quit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "not available" in captured.out


# ==============================================================================
# TESTS: Integration - CLIHandler with history
# ==============================================================================

class TestCLIHandlerWithHistory:
    """Test suite for CLIHandler integration with history."""

    def test_cli_records_operation_on_success(self, cli_with_history):
        """Test that successful CLI operation is recorded."""
        cli, hist, tmp_history_file = cli_with_history
        hist.clear_history()

        result = cli.execute(["add", "2", "3"])

        assert result == 5.0
        recorded = hist.display_history()
        assert len(recorded) == 1
        assert "add(2.0, 3.0) = 5.0" in recorded[0]

    def test_cli_records_multiple_operations(self, cli_with_history):
        """Test that multiple CLI operations are recorded in order."""
        cli, hist, tmp_history_file = cli_with_history
        hist.clear_history()

        cli.execute(["add", "2", "3"])
        cli.execute(["multiply", "5", "6"])
        cli.execute(["divide", "20", "4"])

        recorded = hist.display_history()
        assert len(recorded) == 3
        assert "add(2.0, 3.0) = 5.0" in recorded[0]
        assert "multiply(5.0, 6.0) = 30.0" in recorded[1]
        assert "divide(20.0, 4.0) = 5.0" in recorded[2]

    def test_cli_records_float_results(self, cli_with_history):
        """Test that float results are recorded correctly."""
        cli, hist, tmp_history_file = cli_with_history
        hist.clear_history()

        result = cli.execute(["divide", "10", "3"])

        recorded = hist.display_history()
        assert len(recorded) == 1
        # Result should contain the float value
        assert "divide(10.0, 3.0) =" in recorded[0]

    def test_cli_without_history_skips_recording(self, calculator):
        """Test that recording is skipped when history is None."""
        cli = CLIHandler(calculator, history=None)

        # Should execute without error
        result = cli.execute(["add", "2", "3"])
        assert result == 5.0

    def test_cli_records_with_symbol_aliases(self, cli_with_history):
        """Test that operations using symbols are recorded with method name."""
        cli, hist, tmp_history_file = cli_with_history
        hist.clear_history()

        cli.execute(["+", "5", "7"])

        recorded = hist.display_history()
        assert len(recorded) == 1
        # Should be recorded as "add", not "+"
        assert "add(5.0, 7.0) = 12.0" in recorded[0]


# ==============================================================================
# TESTS: Session isolation and multiple sessions
# ==============================================================================

class TestSessionIsolation:
    """Test suite for session isolation with history."""

    def test_session_isolation_clear_history_at_start(self, tmp_history_file):
        """Test that new session clears history."""
        # First session: record operations
        hist1 = OperationHistory(history_file=tmp_history_file)
        hist1.clear_history()
        hist1.record_operation("session1_op1")
        hist1.record_operation("session1_op2")

        # Verify first session has entries
        assert len(hist1.display_history()) == 2

        # Second session: clear and start fresh
        hist2 = OperationHistory(history_file=tmp_history_file)
        hist2.clear_history()

        # Verify second session is empty
        assert len(hist2.display_history()) == 0

    def test_session_isolation_separate_history_files(self, tmp_path):
        """Test that different session files don't interfere."""
        file1 = str(tmp_path / "session1.txt")
        file2 = str(tmp_path / "session2.txt")

        hist1 = OperationHistory(history_file=file1)
        hist1.clear_history()
        hist1.record_operation("session1_data")

        hist2 = OperationHistory(history_file=file2)
        hist2.clear_history()
        hist2.record_operation("session2_data")

        # Verify isolation
        assert hist1.display_history() == ["session1_data"]
        assert hist2.display_history() == ["session2_data"]


# ==============================================================================
# TESTS: Edge cases and error conditions
# ==============================================================================

class TestEdgeCasesAndErrors:
    """Test suite for edge cases and error conditions."""

    def test_history_with_negative_numbers(self, history, tmp_history_file):
        """Test recording operations with negative numbers."""
        history.clear_history()
        history.record_operation("add(-5.5, -3.2) = -8.7")

        result = history.display_history()
        assert "add(-5.5, -3.2) = -8.7" in result[0]

    def test_history_with_very_large_numbers(self, history, tmp_history_file):
        """Test recording operations with very large numbers."""
        history.clear_history()
        history.record_operation("multiply(999999999, 999999999) = 999999998000000001")

        result = history.display_history()
        assert "999999998000000001" in result[0]

    def test_history_with_very_small_floats(self, history, tmp_history_file):
        """Test recording operations with very small floats."""
        history.clear_history()
        history.record_operation("divide(1, 1000000) = 1e-06")

        result = history.display_history()
        assert "1e-06" in result[0]

    def test_history_file_concurrent_access(self, tmp_history_file):
        """Test that multiple OperationHistory instances can access the file."""
        hist1 = OperationHistory(history_file=tmp_history_file)
        hist2 = OperationHistory(history_file=tmp_history_file)

        hist1.clear_history()
        hist1.record_operation("entry_from_hist1")

        # hist2 should see the entry
        result = hist2.display_history()
        assert len(result) == 1
        assert "entry_from_hist1" in result[0]

    def test_history_with_empty_operand_string(self, history, tmp_history_file):
        """Test recording with empty operand list representation."""
        history.clear_history()
        history.record_operation("operation() = result")

        result = history.display_history()
        assert result == ["operation() = result"]

    def test_history_entry_with_only_spaces(self, history, tmp_history_file):
        """Test recording an entry that is only spaces."""
        history.clear_history()
        history.record_operation("   ")

        result = history.display_history()
        assert len(result) == 1
        assert result[0] == "   "
