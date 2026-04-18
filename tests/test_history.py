"""Tests for src/history.py — History session operation tracking.

Comprehensive unit tests for the History class, covering:
- Recording operations with various arities and result types
- Retrieving and copying history entries
- Formatting entries in the expected notation
- File persistence with proper encoding
"""

import pytest
from pathlib import Path
from src.history import History


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def history():
    """Create a fresh History instance for each test."""
    return History()


# ---------------------------------------------------------------------------
# Happy path: add_operation and get_all
# ---------------------------------------------------------------------------

def test_add_operation_single_entry(history):
    """add_operation() should record a single operation."""
    history.add_operation("add", [2, 3], 5.0)
    entries = history.get_all()
    assert len(entries) == 1
    assert entries[0] == "add(2, 3) = 5.0"


def test_add_operation_binary_operation(history):
    """add_operation() should format binary operations correctly."""
    history.add_operation("multiply", [4, 5], 20.0)
    entries = history.get_all()
    assert entries[0] == "multiply(4, 5) = 20.0"


def test_add_operation_unary_operation(history):
    """add_operation() should format unary operations correctly."""
    history.add_operation("square", [7], 49.0)
    entries = history.get_all()
    assert entries[0] == "square(7) = 49.0"


def test_add_operation_multiple_entries_in_order(history):
    """add_operation() should record multiple entries in insertion order."""
    history.add_operation("add", [1, 2], 3.0)
    history.add_operation("multiply", [3, 4], 12.0)
    history.add_operation("subtract", [10, 5], 5.0)

    entries = history.get_all()
    assert len(entries) == 3
    assert entries[0] == "add(1, 2) = 3.0"
    assert entries[1] == "multiply(3, 4) = 12.0"
    assert entries[2] == "subtract(10, 5) = 5.0"


# ---------------------------------------------------------------------------
# get_all() returns a copy, not reference
# ---------------------------------------------------------------------------

def test_get_all_returns_copy(history):
    """get_all() should return a copy; mutations should not affect internal state."""
    history.add_operation("add", [1, 1], 2.0)
    entries = history.get_all()

    # Mutate the returned list
    entries.append("fake_operation() = 999.0")

    # Internal state should be unchanged
    fresh_entries = history.get_all()
    assert len(fresh_entries) == 1
    assert fresh_entries[0] == "add(1, 1) = 2.0"


def test_get_all_multiple_calls_independence(history):
    """Multiple calls to get_all() should return independent lists."""
    history.add_operation("add", [1, 1], 2.0)

    list1 = history.get_all()
    list2 = history.get_all()

    # Modify list1
    list1.append("tampered() = 0")

    # list2 should still be the original
    assert len(list2) == 1
    assert list2[0] == "add(1, 1) = 2.0"


# ---------------------------------------------------------------------------
# _format_entry() — various argument types and result types
# ---------------------------------------------------------------------------

def test_format_entry_unary_with_float_result(history):
    """_format_entry() should format unary operation with float result."""
    entry = history._format_entry("square_root", [9.0], 3.0)
    assert entry == "square_root(9.0) = 3.0"


def test_format_entry_unary_with_int_result(history):
    """_format_entry() should format unary operation with int result."""
    entry = history._format_entry("square", [5], 25)
    assert entry == "square(5) = 25"


def test_format_entry_binary_with_float_operands(history):
    """_format_entry() should format binary operation with float operands."""
    entry = history._format_entry("divide", [10.0, 3.0], 3.3333333)
    assert entry == "divide(10.0, 3.0) = 3.3333333"


def test_format_entry_binary_with_mixed_operand_types(history):
    """_format_entry() should format binary operation with mixed int/float operands."""
    entry = history._format_entry("add", [1, 2.5], 3.5)
    assert entry == "add(1, 2.5) = 3.5"


def test_format_entry_negative_numbers(history):
    """_format_entry() should handle negative operands and results."""
    entry = history._format_entry("subtract", [5, 10], -5)
    assert entry == "subtract(5, 10) = -5"


def test_format_entry_zero_operand(history):
    """_format_entry() should handle zero as an operand."""
    entry = history._format_entry("add", [0, 5], 5)
    assert entry == "add(0, 5) = 5"


def test_format_entry_zero_result(history):
    """_format_entry() should handle zero as a result."""
    entry = history._format_entry("subtract", [5, 5], 0)
    assert entry == "subtract(5, 5) = 0"


def test_format_entry_negative_result(history):
    """_format_entry() should handle negative results."""
    entry = history._format_entry("subtract", [3, 7], -4)
    assert entry == "subtract(3, 7) = -4"


def test_format_entry_large_numbers(history):
    """_format_entry() should handle very large numbers."""
    entry = history._format_entry("power", [2, 100], 2**100)
    assert entry == f"power(2, 100) = {2**100}"


def test_format_entry_very_small_floats(history):
    """_format_entry() should handle very small floating-point numbers."""
    entry = history._format_entry("divide", [1, 1000000], 1e-6)
    assert entry == "divide(1, 1000000) = 1e-06"


def test_format_entry_empty_operands_list(history):
    """_format_entry() should handle empty operands list."""
    entry = history._format_entry("constant", [], 42)
    assert entry == "constant() = 42"


def test_format_entry_three_operands(history):
    """_format_entry() should handle operations with more than 2 operands."""
    entry = history._format_entry("sum_three", [1, 2, 3], 6)
    assert entry == "sum_three(1, 2, 3) = 6"


def test_format_entry_operation_name_variations(history):
    """_format_entry() should preserve operation name as given."""
    entry1 = history._format_entry("add", [1, 1], 2)
    entry2 = history._format_entry("ADD", [1, 1], 2)

    assert entry1 == "add(1, 1) = 2"
    assert entry2 == "ADD(1, 1) = 2"


# ---------------------------------------------------------------------------
# save_to_file() — file I/O and persistence
# ---------------------------------------------------------------------------

def test_save_to_file_single_entry(tmp_path):
    """save_to_file() should write a single entry to file."""
    history = History()
    history.add_operation("add", [2, 3], 5.0)

    filepath = tmp_path / "history.txt"
    history.save_to_file(str(filepath))

    content = filepath.read_text(encoding="utf-8")
    assert content == "add(2, 3) = 5.0\n"


def test_save_to_file_multiple_entries(tmp_path):
    """save_to_file() should write multiple entries, one per line."""
    history = History()
    history.add_operation("add", [1, 2], 3.0)
    history.add_operation("multiply", [3, 4], 12.0)
    history.add_operation("subtract", [10, 5], 5.0)

    filepath = tmp_path / "history.txt"
    history.save_to_file(str(filepath))

    content = filepath.read_text(encoding="utf-8")
    lines = content.strip().split("\n")

    assert len(lines) == 3
    assert lines[0] == "add(1, 2) = 3.0"
    assert lines[1] == "multiply(3, 4) = 12.0"
    assert lines[2] == "subtract(10, 5) = 5.0"


def test_save_to_file_empty_history(tmp_path):
    """save_to_file() should create an empty file if no operations recorded."""
    history = History()

    filepath = tmp_path / "history.txt"
    history.save_to_file(str(filepath))

    assert filepath.exists()
    content = filepath.read_text(encoding="utf-8")
    assert content == ""


def test_save_to_file_overwrites_existing(tmp_path):
    """save_to_file() should overwrite an existing file."""
    history1 = History()
    history1.add_operation("add", [1, 1], 2.0)

    filepath = tmp_path / "history.txt"
    history1.save_to_file(str(filepath))

    # Create a new history and write to same file
    history2 = History()
    history2.add_operation("multiply", [5, 5], 25.0)
    history2.save_to_file(str(filepath))

    content = filepath.read_text(encoding="utf-8")
    assert "add" not in content
    assert "multiply(5, 5) = 25.0" in content


def test_save_to_file_utf8_encoding(tmp_path):
    """save_to_file() should write in UTF-8 encoding."""
    history = History()
    # Add entries with special characters (though operation names typically are ASCII)
    history.add_operation("op", [1.5, 2.5], 4.0)

    filepath = tmp_path / "history.txt"
    history.save_to_file(str(filepath))

    # Read back as UTF-8 explicitly
    content = filepath.read_text(encoding="utf-8")
    assert "op(1.5, 2.5) = 4.0" in content


def test_save_to_file_large_history(tmp_path):
    """save_to_file() should handle a large number of operations."""
    history = History()
    for i in range(1000):
        history.add_operation("op", [i, i + 1], i + i + 1)

    filepath = tmp_path / "history.txt"
    history.save_to_file(str(filepath))

    lines = filepath.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 1000


def test_save_to_file_path_does_not_exist(tmp_path):
    """save_to_file() should create a file in a directory that exists."""
    history = History()
    history.add_operation("add", [1, 1], 2.0)

    # Use a valid directory but non-existent file
    filepath = tmp_path / "subdir" / "history.txt"
    filepath.parent.mkdir()

    history.save_to_file(str(filepath))
    assert filepath.exists()


def test_save_to_file_oserror_propagates(tmp_path):
    """save_to_file() should propagate OSError if the write fails."""
    history = History()
    history.add_operation("add", [1, 1], 2.0)

    # Create a directory where a file should be
    filepath = tmp_path / "history_dir"
    filepath.mkdir()

    # Attempting to write to a directory should raise OSError
    with pytest.raises(OSError):
        history.save_to_file(str(filepath))


def test_save_to_file_read_back_consistency(tmp_path):
    """Entries written to file should be readable and match original."""
    history = History()
    history.add_operation("add", [2, 3], 5.0)
    history.add_operation("divide", [10.0, 3.0], 3.3333333)
    history.add_operation("square", [4], 16)

    filepath = tmp_path / "history.txt"
    history.save_to_file(str(filepath))

    # Read back and verify line-by-line
    with open(filepath, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    original_entries = history.get_all()
    assert len(lines) == len(original_entries)
    for line, entry in zip(lines, original_entries):
        assert line == entry


# ---------------------------------------------------------------------------
# Integration: full workflow
# ---------------------------------------------------------------------------

def test_full_workflow_add_get_save(tmp_path):
    """Full workflow: add operations, retrieve, and save to file."""
    history = History()

    # Add several operations
    history.add_operation("add", [1, 2], 3.0)
    history.add_operation("multiply", [3, 4], 12.0)

    # Retrieve all
    entries = history.get_all()
    assert len(entries) == 2

    # Save to file
    filepath = tmp_path / "history.txt"
    history.save_to_file(str(filepath))

    # Verify file contents
    content = filepath.read_text(encoding="utf-8")
    assert "add(1, 2) = 3.0" in content
    assert "multiply(3, 4) = 12.0" in content


def test_empty_history_workflow(tmp_path):
    """Empty history should save as empty file and return empty list."""
    history = History()

    entries = history.get_all()
    assert entries == []

    filepath = tmp_path / "history.txt"
    history.save_to_file(str(filepath))

    content = filepath.read_text(encoding="utf-8")
    assert content == ""


# ---------------------------------------------------------------------------
# Edge cases: special numeric values
# ---------------------------------------------------------------------------

def test_format_entry_float_infinity(history):
    """_format_entry() should handle float('inf') as a result."""
    entry = history._format_entry("divide", [1.0, 0.0], float('inf'))
    # Python represents infinity as 'inf'
    assert "inf" in entry.lower()
    assert "divide(1.0, 0.0)" in entry


def test_format_entry_negative_infinity(history):
    """_format_entry() should handle float('-inf') as a result."""
    entry = history._format_entry("negate", [1.0], float('-inf'))
    assert "inf" in entry.lower()
    assert "-inf" in entry.lower()


def test_format_entry_nan(history):
    """_format_entry() should handle NaN values."""
    entry = history._format_entry("sqrt", [-1.0], float('nan'))
    # NaN is represented as 'nan'
    assert "nan" in entry.lower()


def test_format_entry_scientific_notation(history):
    """_format_entry() should handle results in scientific notation."""
    entry = history._format_entry("power", [10, 20], 1e20)
    assert "1e" in entry


# ---------------------------------------------------------------------------
# Edge cases: operand types and coercion
# ---------------------------------------------------------------------------

def test_format_entry_string_operands(history):
    """_format_entry() should stringify operands as given."""
    # While unusual, str() should work on any operand
    entry = history._format_entry("op", ["10", "20"], 30)
    assert entry == "op(10, 20) = 30"


def test_format_entry_mixed_string_and_numeric(history):
    """_format_entry() should stringify mixed types."""
    entry = history._format_entry("op", [1, "2"], 3)
    assert entry == "op(1, 2) = 3"
