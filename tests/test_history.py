"""Tests for the history tracking module."""

import pytest
import tempfile
import os
from pathlib import Path
from io import StringIO
import sys
from unittest.mock import patch

from src.support.history import HistoryTracker


# ==================== HistoryTracker Initialization ====================


def test_history_tracker_initializes_empty():
    """Verify that a new tracker has empty history."""
    tracker = HistoryTracker()
    assert tracker.get_history() == []


def test_history_tracker_initializes_with_list():
    """Verify that internal history is initialized as a list."""
    tracker = HistoryTracker()
    history = tracker.get_history()
    assert isinstance(history, list)


# ==================== record() - Happy Path ====================


def test_record_binary_operation():
    """Test recording a binary operation (add 2 + 3 = 5)."""
    tracker = HistoryTracker()
    tracker.record("add", [2, 3], 5)
    history = tracker.get_history()
    assert len(history) == 1
    assert history[0] == "add(2, 3) = 5"


def test_record_unary_operation():
    """Test recording a unary operation (factorial 5 = 120)."""
    tracker = HistoryTracker()
    tracker.record("factorial", [5], 120)
    history = tracker.get_history()
    assert len(history) == 1
    assert history[0] == "factorial(5) = 120"


def test_record_single_operand():
    """Test recording an operation with a single operand."""
    tracker = HistoryTracker()
    tracker.record("square", [4], 16)
    history = tracker.get_history()
    assert history[0] == "square(4) = 16"


def test_record_float_result():
    """Test recording an operation with float result."""
    tracker = HistoryTracker()
    tracker.record("divide", [5, 2], 2.5)
    history = tracker.get_history()
    assert history[0] == "divide(5, 2) = 2.5"


def test_record_multiple_operations():
    """Test recording multiple operations in sequence."""
    tracker = HistoryTracker()
    tracker.record("add", [2, 3], 5)
    tracker.record("multiply", [4, 5], 20)
    tracker.record("divide", [20, 2], 10.0)
    history = tracker.get_history()
    assert len(history) == 3
    assert history[0] == "add(2, 3) = 5"
    assert history[1] == "multiply(4, 5) = 20"
    assert history[2] == "divide(20, 2) = 10.0"


def test_record_with_negative_operands():
    """Test recording operations with negative operands."""
    tracker = HistoryTracker()
    tracker.record("subtract", [-5, 3], -8)
    history = tracker.get_history()
    assert history[0] == "subtract(-5, 3) = -8"


def test_record_with_zero_result():
    """Test recording operations with zero result."""
    tracker = HistoryTracker()
    tracker.record("subtract", [5, 5], 0)
    history = tracker.get_history()
    assert history[0] == "subtract(5, 5) = 0"


def test_record_with_zero_operand():
    """Test recording operations with zero operand."""
    tracker = HistoryTracker()
    tracker.record("power", [0, 5], 0)
    history = tracker.get_history()
    assert history[0] == "power(0, 5) = 0"


def test_record_with_large_numbers():
    """Test recording operations with very large numbers."""
    tracker = HistoryTracker()
    tracker.record("multiply", [999999999, 888888888], 888888887111111112)
    history = tracker.get_history()
    assert "multiply" in history[0]
    assert "999999999" in history[0]


def test_record_with_very_small_floats():
    """Test recording operations with very small floats."""
    tracker = HistoryTracker()
    tracker.record("divide", [1, 1000000], 1e-6)
    history = tracker.get_history()
    # Python's str() converts very small floats to scientific notation
    assert "1e-06" in history[0] or "0.000001" in history[0]


def test_record_three_operands():
    """Test recording an operation with three operands (hypothetically)."""
    tracker = HistoryTracker()
    tracker.record("custom_op", [1, 2, 3], 6)
    history = tracker.get_history()
    assert history[0] == "custom_op(1, 2, 3) = 6"


def test_record_string_result():
    """Test recording an operation with string result."""
    tracker = HistoryTracker()
    tracker.record("format", [42], "forty-two")
    history = tracker.get_history()
    assert history[0] == "format(42) = forty-two"


def test_record_empty_operands_list():
    """Test recording with an empty operands list."""
    tracker = HistoryTracker()
    tracker.record("constant", [], 3.14159)
    history = tracker.get_history()
    assert history[0] == "constant() = 3.14159"


# ==================== get_history() - Happy Path ====================


def test_get_history_returns_list():
    """Verify get_history() returns a list."""
    tracker = HistoryTracker()
    tracker.record("add", [1, 2], 3)
    history = tracker.get_history()
    assert isinstance(history, list)


def test_get_history_order_preserved():
    """Verify entries are returned in insertion order."""
    tracker = HistoryTracker()
    tracker.record("op1", [1], 10)
    tracker.record("op2", [2], 20)
    tracker.record("op3", [3], 30)
    history = tracker.get_history()
    assert history[0] == "op1(1) = 10"
    assert history[1] == "op2(2) = 20"
    assert history[2] == "op3(3) = 30"


def test_get_history_immutability():
    """Verify that modifying returned list doesn't affect tracker."""
    tracker = HistoryTracker()
    tracker.record("add", [1, 2], 3)
    history1 = tracker.get_history()
    history1.append("fake entry")
    history2 = tracker.get_history()
    assert len(history2) == 1
    assert history2[0] == "add(1, 2) = 3"


def test_get_history_returns_new_list_each_time():
    """Verify get_history() returns a new list on each call."""
    tracker = HistoryTracker()
    tracker.record("add", [1, 2], 3)
    history1 = tracker.get_history()
    history2 = tracker.get_history()
    assert history1 is not history2  # Different list objects
    assert history1 == history2  # But same content


def test_get_history_on_empty_tracker():
    """Verify get_history() returns empty list for empty tracker."""
    tracker = HistoryTracker()
    history = tracker.get_history()
    assert history == []
    assert isinstance(history, list)


# ==================== display() - Happy Path ====================


def test_display_empty(capsys):
    """Test display on empty tracker prints 'No history' message."""
    tracker = HistoryTracker()
    tracker.display()
    captured = capsys.readouterr()
    assert "No history for this session." in captured.out


def test_display_with_entries(capsys):
    """Test display shows header and each entry."""
    tracker = HistoryTracker()
    tracker.record("add", [2, 3], 5)
    tracker.record("multiply", [4, 5], 20)
    tracker.display()
    captured = capsys.readouterr()
    assert "Session history:" in captured.out
    assert "add(2, 3) = 5" in captured.out
    assert "multiply(4, 5) = 20" in captured.out


def test_display_single_entry(capsys):
    """Test display with a single entry."""
    tracker = HistoryTracker()
    tracker.record("square", [7], 49)
    tracker.display()
    captured = capsys.readouterr()
    assert "Session history:" in captured.out
    assert "square(7) = 49" in captured.out


def test_display_many_entries(capsys):
    """Test display with many entries."""
    tracker = HistoryTracker()
    for i in range(10):
        tracker.record(f"op{i}", [i], i * 10)
    tracker.display()
    captured = capsys.readouterr()
    assert "Session history:" in captured.out
    # Verify several entries are in the output
    assert "op0(0) = 0" in captured.out
    assert "op5(5) = 50" in captured.out
    assert "op9(9) = 90" in captured.out


def test_display_indentation(capsys):
    """Test that display indents entries with two spaces."""
    tracker = HistoryTracker()
    tracker.record("add", [1, 2], 3)
    tracker.display()
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    # Find the entry line (should have 2-space indent)
    entry_lines = [l for l in lines if "add(1, 2)" in l]
    assert len(entry_lines) > 0
    # Check that it starts with two spaces
    assert entry_lines[0].startswith("  ")


# ==================== save_to_file() - Happy Path ====================


def test_save_to_file_creates_file(tmp_path):
    """Test that save_to_file creates a file."""
    tracker = HistoryTracker()
    tracker.record("add", [2, 3], 5)
    filepath = tmp_path / "history.txt"
    tracker.save_to_file(str(filepath))
    assert filepath.exists()


def test_save_to_file_content(tmp_path):
    """Test that saved file contains expected entries."""
    tracker = HistoryTracker()
    tracker.record("add", [2, 3], 5)
    tracker.record("multiply", [4, 5], 20)
    filepath = tmp_path / "history.txt"
    tracker.save_to_file(str(filepath))
    content = filepath.read_text()
    assert "add(2, 3) = 5\n" in content
    assert "multiply(4, 5) = 20\n" in content


def test_save_to_file_empty_history(tmp_path):
    """Test saving empty history creates file with no entries."""
    tracker = HistoryTracker()
    filepath = tmp_path / "history.txt"
    tracker.save_to_file(str(filepath))
    assert filepath.exists()
    content = filepath.read_text()
    assert content == ""


def test_save_to_file_one_per_line(tmp_path):
    """Test that each entry is on its own line."""
    tracker = HistoryTracker()
    tracker.record("add", [1, 2], 3)
    tracker.record("subtract", [5, 3], 2)
    tracker.record("multiply", [4, 5], 20)
    filepath = tmp_path / "history.txt"
    tracker.save_to_file(str(filepath))
    lines = filepath.read_text().split("\n")
    # Should have 3 entries + 1 empty line at end (due to final \n)
    non_empty_lines = [l for l in lines if l.strip()]
    assert len(non_empty_lines) == 3


def test_save_to_file_overwrites_existing(tmp_path):
    """Test that second save overwrites first (not append)."""
    tracker = HistoryTracker()
    filepath = tmp_path / "history.txt"

    # First save
    tracker.record("add", [2, 3], 5)
    tracker.save_to_file(str(filepath))

    # Clear and save again
    tracker.clear()
    tracker.record("multiply", [4, 5], 20)
    tracker.save_to_file(str(filepath))

    content = filepath.read_text()
    assert "add(2, 3) = 5" not in content
    assert "multiply(4, 5) = 20" in content


def test_save_to_file_default_filename(tmp_path):
    """Test save_to_file with default filename (history.txt)."""
    # Change to temp directory temporarily
    original_cwd = os.getcwd()
    try:
        os.chdir(str(tmp_path))
        tracker = HistoryTracker()
        tracker.record("add", [1, 2], 3)
        tracker.save_to_file()  # Use default
        assert Path("history.txt").exists()
        content = Path("history.txt").read_text()
        assert "add(1, 2) = 3" in content
    finally:
        os.chdir(original_cwd)


def test_save_to_file_custom_path(tmp_path):
    """Test save_to_file with custom filepath."""
    tracker = HistoryTracker()
    tracker.record("add", [2, 3], 5)
    filepath = tmp_path / "custom_name.log"
    tracker.save_to_file(str(filepath))
    assert filepath.exists()


def test_save_to_file_nested_directory(tmp_path):
    """Test save_to_file with nested directory path."""
    tracker = HistoryTracker()
    tracker.record("add", [2, 3], 5)
    nested_dir = tmp_path / "subdir" / "nested"
    nested_dir.mkdir(parents=True)
    filepath = nested_dir / "history.txt"
    tracker.save_to_file(str(filepath))
    assert filepath.exists()


def test_save_to_file_special_characters_in_entry(tmp_path):
    """Test saving entries with special characters."""
    tracker = HistoryTracker()
    tracker.record("op_name", [1.5, 2.7], 4.2)
    filepath = tmp_path / "history.txt"
    tracker.save_to_file(str(filepath))
    content = filepath.read_text()
    assert "op_name(1.5, 2.7) = 4.2" in content


def test_save_to_file_unicode_operation_name(tmp_path):
    """Test saving with Unicode in operation name."""
    tracker = HistoryTracker()
    tracker.record("добавить", [2, 3], 5)  # Russian for "add"
    filepath = tmp_path / "history.txt"
    tracker.save_to_file(str(filepath))
    content = filepath.read_text(encoding='utf-8')
    assert "добавить" in content


def test_save_to_file_large_history(tmp_path):
    """Test saving a large history."""
    tracker = HistoryTracker()
    for i in range(1000):
        tracker.record(f"op{i}", [i], i * 2)
    filepath = tmp_path / "history.txt"
    tracker.save_to_file(str(filepath))
    lines = filepath.read_text().strip().split("\n")
    assert len(lines) == 1000


# ==================== save_to_file() - Error Handling ====================


def test_save_to_file_oserror_directory_path(capsys):
    """Test that OSError is caught when filepath is a directory."""
    tracker = HistoryTracker()
    tracker.record("add", [2, 3], 5)
    with tempfile.TemporaryDirectory() as tmpdir:
        # Try to save to a directory path (should fail)
        tracker.save_to_file(str(tmpdir))
        captured = capsys.readouterr()
        # Should print warning to stderr
        assert "Warning" in captured.err
        assert "could not save history" in captured.err


def test_save_to_file_no_exception_raised():
    """Test that OSError doesn't raise an exception (suppressed)."""
    tracker = HistoryTracker()
    tracker.record("add", [2, 3], 5)
    # Try to write to an invalid path that should fail
    # This should NOT raise an exception
    try:
        tracker.save_to_file("/dev/null/this/path/does/not/exist/history.txt")
        # If we reach here, the exception was properly suppressed
        success = True
    except OSError:
        success = False
    assert success


def test_save_to_file_permission_error_message(capsys):
    """Test warning message when save fails."""
    tracker = HistoryTracker()
    tracker.record("add", [2, 3], 5)
    with tempfile.TemporaryDirectory() as tmpdir:
        # Try to save to a directory to trigger OSError
        tracker.save_to_file(str(tmpdir))
        captured = capsys.readouterr()
        assert "Warning:" in captured.err


# ==================== clear() - Happy Path ====================


def test_clear_resets_history():
    """Test that clear removes all entries."""
    tracker = HistoryTracker()
    tracker.record("add", [2, 3], 5)
    tracker.record("multiply", [4, 5], 20)
    assert len(tracker.get_history()) == 2
    tracker.clear()
    assert len(tracker.get_history()) == 0
    assert tracker.get_history() == []


def test_clear_on_empty_tracker():
    """Test that clear on empty tracker doesn't fail."""
    tracker = HistoryTracker()
    tracker.clear()  # Should not raise
    assert tracker.get_history() == []


def test_clear_allows_new_recordings():
    """Test that clear allows new entries after clearing."""
    tracker = HistoryTracker()
    tracker.record("add", [2, 3], 5)
    tracker.clear()
    tracker.record("multiply", [4, 5], 20)
    history = tracker.get_history()
    assert len(history) == 1
    assert history[0] == "multiply(4, 5) = 20"


def test_clear_and_save_creates_empty_file(tmp_path):
    """Test that clear then save creates empty file."""
    tracker = HistoryTracker()
    tracker.record("add", [2, 3], 5)
    tracker.clear()
    filepath = tmp_path / "history.txt"
    tracker.save_to_file(str(filepath))
    content = filepath.read_text()
    assert content == ""


# ==================== Format Specification Tests ====================


def test_format_matches_spec_add():
    """Test that add entry format is exactly 'add(2, 3) = 5'."""
    tracker = HistoryTracker()
    tracker.record("add", [2, 3], 5)
    history = tracker.get_history()
    assert history[0] == "add(2, 3) = 5"


def test_format_matches_spec_factorial():
    """Test that factorial entry format is exactly 'factorial(5) = 120'."""
    tracker = HistoryTracker()
    tracker.record("factorial", [5], 120)
    history = tracker.get_history()
    assert history[0] == "factorial(5) = 120"


def test_format_matches_spec_square_root():
    """Test that square_root entry format matches spec."""
    tracker = HistoryTracker()
    tracker.record("square_root", [9], 3.0)
    history = tracker.get_history()
    assert history[0] == "square_root(9) = 3.0"


def test_format_matches_spec_divide():
    """Test divide operation format."""
    tracker = HistoryTracker()
    tracker.record("divide", [10, 2], 5.0)
    history = tracker.get_history()
    assert history[0] == "divide(10, 2) = 5.0"


def test_format_matches_spec_power():
    """Test power operation format."""
    tracker = HistoryTracker()
    tracker.record("power", [2, 3], 8)
    history = tracker.get_history()
    assert history[0] == "power(2, 3) = 8"


def test_format_matches_spec_subtract():
    """Test subtract operation format."""
    tracker = HistoryTracker()
    tracker.record("subtract", [10, 3], 7)
    history = tracker.get_history()
    assert history[0] == "subtract(10, 3) = 7"


def test_format_matches_spec_multiply():
    """Test multiply operation format."""
    tracker = HistoryTracker()
    tracker.record("multiply", [4, 5], 20)
    history = tracker.get_history()
    assert history[0] == "multiply(4, 5) = 20"


def test_format_matches_spec_square():
    """Test square operation format."""
    tracker = HistoryTracker()
    tracker.record("square", [5], 25)
    history = tracker.get_history()
    assert history[0] == "square(5) = 25"


def test_format_matches_spec_cube():
    """Test cube operation format."""
    tracker = HistoryTracker()
    tracker.record("cube", [3], 27)
    history = tracker.get_history()
    assert history[0] == "cube(3) = 27"


def test_format_matches_spec_cube_root():
    """Test cube_root operation format."""
    tracker = HistoryTracker()
    tracker.record("cube_root", [27], 3.0)
    history = tracker.get_history()
    assert history[0] == "cube_root(27) = 3.0"


def test_format_matches_spec_log():
    """Test log (base-10) operation format."""
    tracker = HistoryTracker()
    tracker.record("log", [100], 2.0)
    history = tracker.get_history()
    assert history[0] == "log(100) = 2.0"


def test_format_matches_spec_ln():
    """Test ln (natural log) operation format."""
    tracker = HistoryTracker()
    tracker.record("ln", [1], 0.0)
    history = tracker.get_history()
    # ln(1) is exactly 0.0
    assert "ln(1)" in history[0]
    assert "= 0" in history[0]


# ==================== Edge Cases - Operand Types ====================


def test_record_with_float_operands():
    """Test recording with float operands."""
    tracker = HistoryTracker()
    tracker.record("add", [1.5, 2.5], 4.0)
    history = tracker.get_history()
    assert "add(1.5, 2.5) = 4.0" in history[0]


def test_record_with_mixed_int_float_operands():
    """Test recording with mixed int and float operands."""
    tracker = HistoryTracker()
    tracker.record("add", [1, 2.5], 3.5)
    history = tracker.get_history()
    assert "add(1, 2.5) = 3.5" in history[0]


def test_record_operand_string_conversion():
    """Test that operands are converted to strings correctly."""
    tracker = HistoryTracker()
    # Record with various types (will be stringified)
    tracker.record("op", [42, 3.14], 45.14)
    history = tracker.get_history()
    assert "42" in history[0]
    assert "3.14" in history[0]


# ==================== Edge Cases - History Operations ====================


def test_multiple_get_history_calls():
    """Test calling get_history multiple times returns consistent results."""
    tracker = HistoryTracker()
    tracker.record("add", [1, 2], 3)
    h1 = tracker.get_history()
    h2 = tracker.get_history()
    h3 = tracker.get_history()
    assert h1 == h2 == h3


def test_record_then_clear_then_record():
    """Test pattern: record, clear, record again."""
    tracker = HistoryTracker()
    tracker.record("add", [1, 2], 3)
    tracker.clear()
    tracker.record("multiply", [4, 5], 20)
    history = tracker.get_history()
    assert len(history) == 1
    assert "multiply" in history[0]


def test_large_operand_list():
    """Test recording with many operands."""
    tracker = HistoryTracker()
    operands = list(range(1, 11))  # [1, 2, 3, ..., 10]
    tracker.record("sum_op", operands, 55)
    history = tracker.get_history()
    assert "sum_op(1, 2, 3, 4, 5, 6, 7, 8, 9, 10) = 55" in history[0]


# ==================== Parametrized Tests ====================


@pytest.mark.parametrize("operation_name,operands,result,expected_entry", [
    ("add", [2, 3], 5, "add(2, 3) = 5"),
    ("subtract", [10, 3], 7, "subtract(10, 3) = 7"),
    ("multiply", [4, 5], 20, "multiply(4, 5) = 20"),
    ("divide", [10, 2], 5.0, "divide(10, 2) = 5.0"),
    ("power", [2, 3], 8, "power(2, 3) = 8"),
    ("factorial", [5], 120, "factorial(5) = 120"),
    ("square", [4], 16, "square(4) = 16"),
    ("cube", [3], 27, "cube(3) = 27"),
    ("square_root", [9], 3.0, "square_root(9) = 3.0"),
    ("cube_root", [27], 3.0, "cube_root(27) = 3.0"),
    ("log", [100], 2.0, "log(100) = 2.0"),
    ("ln", [1], 0.0, "ln(1) = 0.0"),
])
def test_record_various_operations(operation_name, operands, result, expected_entry):
    """Parametrized test for various operation recordings."""
    tracker = HistoryTracker()
    tracker.record(operation_name, operands, result)
    history = tracker.get_history()
    assert history[0] == expected_entry


@pytest.mark.parametrize("entries_count", [1, 5, 10, 50, 100])
def test_get_history_with_various_counts(entries_count):
    """Test get_history with various entry counts."""
    tracker = HistoryTracker()
    for i in range(entries_count):
        tracker.record(f"op{i}", [i], i * 2)
    history = tracker.get_history()
    assert len(history) == entries_count


@pytest.mark.parametrize("operand_count", [0, 1, 2, 3, 5, 10])
def test_record_various_operand_counts(operand_count):
    """Test recording with various operand counts."""
    tracker = HistoryTracker()
    operands = list(range(operand_count))
    tracker.record("test_op", operands, 42)
    history = tracker.get_history()
    assert len(history) == 1
    # Verify format is correct
    assert "test_op(" in history[0]
    assert ") = 42" in history[0]


# ==================== Integration-style Tests ====================


def test_session_simulation():
    """Simulate a calculator session with history."""
    tracker = HistoryTracker()

    # Simulate user operations
    tracker.record("add", [2, 3], 5)
    assert len(tracker.get_history()) == 1

    tracker.record("multiply", [5, 4], 20)
    assert len(tracker.get_history()) == 2

    tracker.record("divide", [20, 2], 10.0)
    assert len(tracker.get_history()) == 3

    history = tracker.get_history()
    assert history[0] == "add(2, 3) = 5"
    assert history[1] == "multiply(5, 4) = 20"
    assert history[2] == "divide(20, 2) = 10.0"


def test_save_and_display_workflow(tmp_path, capsys):
    """Test typical workflow: record, display, save."""
    tracker = HistoryTracker()

    # Record operations
    tracker.record("add", [2, 3], 5)
    tracker.record("multiply", [4, 5], 20)

    # Display
    tracker.display()
    captured = capsys.readouterr()
    assert "add(2, 3) = 5" in captured.out
    assert "multiply(4, 5) = 20" in captured.out

    # Save
    filepath = tmp_path / "history.txt"
    tracker.save_to_file(str(filepath))
    content = filepath.read_text()
    assert "add(2, 3) = 5" in content
    assert "multiply(4, 5) = 20" in content
