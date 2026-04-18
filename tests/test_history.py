"""Tests for src/history.py.

Tests the OperationHistory class for recording, retrieving, and clearing
operation history. File I/O is tested with isolation to avoid polluting
the working directory.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

from src.history import OperationHistory, HISTORY_FILE, _UNARY_OPERATIONS


# ---------------------------------------------------------------------------
# OperationHistory.__init__ and file management
# ---------------------------------------------------------------------------


def test_operation_history_init_creates_empty_list() -> None:
    """OperationHistory() must initialise with an empty in-memory list."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        assert history.get_history() == []


def test_operation_history_init_creates_history_file(tmp_path: Path) -> None:
    """OperationHistory() must create or truncate history.txt in cwd."""
    os.chdir(tmp_path)
    history = OperationHistory()
    history_path = tmp_path / HISTORY_FILE
    assert history_path.exists(), f"history.txt not created at {history_path}"


def test_operation_history_init_clears_previous_file(tmp_path: Path) -> None:
    """Creating a new OperationHistory instance must clear the existing file."""
    os.chdir(tmp_path)
    # Create an instance and record an operation
    history1 = OperationHistory()
    history1.record_operation("add", [1.0, 2.0], 3.0)

    # Create a new instance — file should be cleared
    history2 = OperationHistory()

    # File exists and is empty
    history_file = tmp_path / HISTORY_FILE
    content = history_file.read_text(encoding="utf-8")
    assert content == "", "File should be empty after new OperationHistory()"


def test_operation_history_init_truncates_not_deletes(tmp_path: Path) -> None:
    """File is truncated (cleared) not deleted when OperationHistory is created."""
    os.chdir(tmp_path)
    history_path = tmp_path / HISTORY_FILE

    # Create first instance and record data
    history1 = OperationHistory()
    history1.record_operation("multiply", [5.0, 3.0], 15.0)

    # Create second instance
    history2 = OperationHistory()

    # File must exist (not deleted) and be empty (truncated)
    assert history_path.exists()
    assert history_path.read_text(encoding="utf-8") == ""


# ---------------------------------------------------------------------------
# record_operation – happy path
# ---------------------------------------------------------------------------


def test_record_operation_adds_to_in_memory_history(tmp_path: Path) -> None:
    """record_operation() must append entry to in-memory list."""
    os.chdir(tmp_path)
    history = OperationHistory()
    history.record_operation("add", [2.0, 3.0], 5.0)
    result = history.get_history()
    assert len(result) == 1
    assert "2" in result[0] and "3" in result[0] and "5" in result[0]


def test_record_operation_writes_to_file(tmp_path: Path) -> None:
    """record_operation() must append entry to history.txt on disk."""
    os.chdir(tmp_path)
    history = OperationHistory()
    history.record_operation("add", [10.0, 20.0], 30.0)

    history_file = tmp_path / HISTORY_FILE
    content = history_file.read_text(encoding="utf-8")
    assert "10" in content and "20" in content and "30" in content


def test_record_operation_binary_formats_correctly(tmp_path: Path) -> None:
    """Binary operations must format as 'a operation b = result'."""
    os.chdir(tmp_path)
    history = OperationHistory()
    history.record_operation("add", [2.0, 3.0], 5.0)
    result = history.get_history()[0]
    # Format: 2.0 add 3.0 = 5.0
    assert result == "2.0 add 3.0 = 5.0"


def test_record_operation_unary_formats_correctly(tmp_path: Path) -> None:
    """Unary operations must format as 'operation(a) = result'."""
    os.chdir(tmp_path)
    history = OperationHistory()
    history.record_operation("square", [4.0], 16.0)
    result = history.get_history()[0]
    # Format: square(4.0) = 16.0
    assert result == "square(4.0) = 16.0"


def test_record_operation_multiple_in_order(tmp_path: Path) -> None:
    """Multiple operations must be recorded in chronological order."""
    os.chdir(tmp_path)
    history = OperationHistory()
    history.record_operation("add", [1.0, 2.0], 3.0)
    history.record_operation("multiply", [3.0, 4.0], 12.0)
    history.record_operation("square", [5.0], 25.0)

    result = history.get_history()
    assert len(result) == 3
    assert "1.0 add 2.0 = 3.0" in result[0]
    assert "3.0 multiply 4.0 = 12.0" in result[1]
    assert "square(5.0) = 25.0" in result[2]


def test_record_operation_persists_to_file(tmp_path: Path) -> None:
    """Operations recorded to file must persist across instances."""
    os.chdir(tmp_path)
    history1 = OperationHistory()
    history1.record_operation("add", [5.0, 10.0], 15.0)

    # Read file directly
    history_file = tmp_path / HISTORY_FILE
    content = history_file.read_text(encoding="utf-8")
    assert "5.0 add 10.0 = 15.0" in content


# ---------------------------------------------------------------------------
# get_history
# ---------------------------------------------------------------------------


def test_get_history_empty_returns_empty_list(tmp_path: Path) -> None:
    """get_history() on a new instance must return an empty list."""
    os.chdir(tmp_path)
    history = OperationHistory()
    assert history.get_history() == []


def test_get_history_returns_list_of_formatted_strings(tmp_path: Path) -> None:
    """get_history() must return a list of formatted operation strings."""
    os.chdir(tmp_path)
    history = OperationHistory()
    history.record_operation("subtract", [10.0, 3.0], 7.0)
    history.record_operation("divide", [20.0, 4.0], 5.0)

    result = history.get_history()
    assert isinstance(result, list)
    assert all(isinstance(entry, str) for entry in result)
    assert len(result) == 2


def test_get_history_returns_copy_not_reference(tmp_path: Path) -> None:
    """get_history() must return a copy, not the internal list reference."""
    os.chdir(tmp_path)
    history = OperationHistory()
    history.record_operation("add", [1.0, 1.0], 2.0)

    result1 = history.get_history()
    result1.append("fake_entry")  # Mutate the returned list

    result2 = history.get_history()
    assert len(result2) == 1, "Mutation of returned list must not affect history"


def test_get_history_preserves_order(tmp_path: Path) -> None:
    """get_history() must return entries in chronological order."""
    os.chdir(tmp_path)
    history = OperationHistory()

    operations = [
        ("add", [1.0, 1.0], 2.0),
        ("subtract", [5.0, 2.0], 3.0),
        ("multiply", [2.0, 3.0], 6.0),
    ]
    for op, operands, result in operations:
        history.record_operation(op, operands, result)

    retrieved = history.get_history()
    for i, (op, operands, result) in enumerate(operations):
        # Verify order by checking operation names appear in the right sequence
        assert op in retrieved[i]


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


def test_clear_empties_in_memory_list(tmp_path: Path) -> None:
    """clear() must reset the in-memory list to empty."""
    os.chdir(tmp_path)
    history = OperationHistory()
    history.record_operation("add", [1.0, 2.0], 3.0)
    assert len(history.get_history()) == 1

    history.clear()
    assert history.get_history() == []


def test_clear_does_not_truncate_file(tmp_path: Path) -> None:
    """clear() must NOT modify the history.txt file."""
    os.chdir(tmp_path)
    history = OperationHistory()
    history.record_operation("add", [10.0, 20.0], 30.0)

    history_file = tmp_path / HISTORY_FILE
    content_before = history_file.read_text(encoding="utf-8")

    history.clear()

    content_after = history_file.read_text(encoding="utf-8")
    assert content_before == content_after, "File should not be modified by clear()"
    assert len(content_after) > 0, "File should still contain the previous entry"


def test_clear_then_record_appends_to_file(tmp_path: Path) -> None:
    """After clear(), recording new operations appends to file (does not overwrite)."""
    os.chdir(tmp_path)
    history = OperationHistory()
    history.record_operation("add", [1.0, 1.0], 2.0)

    history.clear()
    assert history.get_history() == []

    history.record_operation("subtract", [5.0, 2.0], 3.0)

    # File should have both entries
    history_file = tmp_path / HISTORY_FILE
    content = history_file.read_text(encoding="utf-8")
    assert "1.0 add 1.0 = 2.0" in content
    assert "5.0 subtract 2.0 = 3.0" in content


# ---------------------------------------------------------------------------
# _format_entry – binary operations
# ---------------------------------------------------------------------------


def test_format_entry_binary_add(tmp_path: Path) -> None:
    """_format_entry for 'add' must format as 'a add b = result'."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("add", [2.0, 3.0], 5.0)
    assert result == "2.0 add 3.0 = 5.0"


def test_format_entry_binary_subtract(tmp_path: Path) -> None:
    """_format_entry for 'subtract' must format correctly."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("subtract", [10.0, 3.0], 7.0)
    assert result == "10.0 subtract 3.0 = 7.0"


def test_format_entry_binary_multiply(tmp_path: Path) -> None:
    """_format_entry for 'multiply' must format correctly."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("multiply", [4.0, 5.0], 20.0)
    assert result == "4.0 multiply 5.0 = 20.0"


def test_format_entry_binary_divide(tmp_path: Path) -> None:
    """_format_entry for 'divide' must format correctly."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("divide", [20.0, 4.0], 5.0)
    assert result == "20.0 divide 4.0 = 5.0"


def test_format_entry_binary_power(tmp_path: Path) -> None:
    """_format_entry for 'power' must format correctly."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("power", [2.0, 8.0], 256.0)
    assert result == "2.0 power 8.0 = 256.0"


# ---------------------------------------------------------------------------
# _format_entry – unary operations
# ---------------------------------------------------------------------------


def test_format_entry_unary_square(tmp_path: Path) -> None:
    """_format_entry for 'square' must format as 'square(a) = result'."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("square", [5.0], 25.0)
    assert result == "square(5.0) = 25.0"


def test_format_entry_unary_cube(tmp_path: Path) -> None:
    """_format_entry for 'cube' must format as 'cube(a) = result'."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("cube", [3.0], 27.0)
    assert result == "cube(3.0) = 27.0"


def test_format_entry_unary_square_root(tmp_path: Path) -> None:
    """_format_entry for 'square_root' must format as 'square_root(a) = result'."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("square_root", [9.0], 3.0)
    assert result == "square_root(9.0) = 3.0"


def test_format_entry_unary_cube_root(tmp_path: Path) -> None:
    """_format_entry for 'cube_root' must format as 'cube_root(a) = result'."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("cube_root", [8.0], 2.0)
    assert result == "cube_root(8.0) = 2.0"


def test_format_entry_unary_factorial(tmp_path: Path) -> None:
    """_format_entry for 'factorial' must format as 'factorial(a) = result'."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("factorial", [5.0], 120.0)
    assert result == "factorial(5.0) = 120.0"


def test_format_entry_unary_log(tmp_path: Path) -> None:
    """_format_entry for 'log' must format as 'log(a) = result'."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("log", [100.0], 2.0)
    assert result == "log(100.0) = 2.0"


def test_format_entry_unary_ln(tmp_path: Path) -> None:
    """_format_entry for 'ln' must format as 'ln(a) = result'."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("ln", [2.718], 1.0)
    assert result == "ln(2.718) = 1.0"


# ---------------------------------------------------------------------------
# _format_entry – edge cases
# ---------------------------------------------------------------------------


def test_format_entry_zero_operand(tmp_path: Path) -> None:
    """_format_entry must handle zero as operand."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("add", [0.0, 5.0], 5.0)
    assert result == "0.0 add 5.0 = 5.0"


def test_format_entry_negative_operand(tmp_path: Path) -> None:
    """_format_entry must handle negative operands."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("add", [-3.0, 5.0], 2.0)
    assert result == "-3.0 add 5.0 = 2.0"


def test_format_entry_negative_result(tmp_path: Path) -> None:
    """_format_entry must handle negative results."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("subtract", [2.0, 5.0], -3.0)
    assert result == "2.0 subtract 5.0 = -3.0"


def test_format_entry_large_numbers(tmp_path: Path) -> None:
    """_format_entry must handle very large numbers."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("multiply", [1e100, 2.0], 2e100)
    assert "1e+100" in result and "2e+100" in result


def test_format_entry_very_small_numbers(tmp_path: Path) -> None:
    """_format_entry must handle very small numbers."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("multiply", [1e-100, 1e-100], 1e-200)
    # Small floats are represented in scientific notation
    assert "1e-100" in result or "0.0" in result


def test_format_entry_float_precision(tmp_path: Path) -> None:
    """_format_entry must preserve float precision in output."""
    os.chdir(tmp_path)
    history = OperationHistory()
    result = history._format_entry("divide", [1.0, 3.0], 0.3333333333333333)
    assert "0.3333333333333333" in result


# ---------------------------------------------------------------------------
# Edge cases – multiple instances and session isolation
# ---------------------------------------------------------------------------


def test_multiple_instances_isolated(tmp_path: Path) -> None:
    """Two OperationHistory instances in same session must be independent."""
    os.chdir(tmp_path)
    history1 = OperationHistory()
    history2 = OperationHistory()  # This clears the file

    history1.record_operation("add", [1.0, 1.0], 2.0)
    history2.record_operation("subtract", [5.0, 2.0], 3.0)

    # history1 and history2 are independent in memory
    assert len(history1.get_history()) == 1
    assert len(history2.get_history()) == 1

    # File contains only history2's entry (because history2's __init__ cleared it)
    history_file = tmp_path / HISTORY_FILE
    content = history_file.read_text(encoding="utf-8")
    assert "5.0 subtract 2.0 = 3.0" in content


def test_record_after_clear_increases_count(tmp_path: Path) -> None:
    """After clear(), new records append to both in-memory and file."""
    os.chdir(tmp_path)
    history = OperationHistory()
    history.record_operation("add", [1.0, 1.0], 2.0)
    history.clear()
    history.record_operation("multiply", [3.0, 3.0], 9.0)

    # In-memory has only the new entry
    assert len(history.get_history()) == 1
    assert "multiply" in history.get_history()[0]

    # File has both entries
    history_file = tmp_path / HISTORY_FILE
    content = history_file.read_text(encoding="utf-8")
    assert "1.0 add 1.0 = 2.0" in content
    assert "3.0 multiply 3.0 = 9.0" in content


# ---------------------------------------------------------------------------
# Unary operations set verification
# ---------------------------------------------------------------------------


def test_unary_operations_set_includes_expected_operations() -> None:
    """_UNARY_OPERATIONS frozenset must include all unary operation keys."""
    expected = {"factorial", "square", "cube", "square_root", "cube_root", "log", "ln"}
    assert _UNARY_OPERATIONS == expected


def test_all_unary_operations_format_correctly(tmp_path: Path) -> None:
    """All operations in _UNARY_OPERATIONS must use unary format."""
    os.chdir(tmp_path)
    history = OperationHistory()

    for op in _UNARY_OPERATIONS:
        result = history._format_entry(op, [5.0], 10.0)
        # Unary format is "op(operand) = result"
        assert f"{op}(5.0) = 10.0" == result


@pytest.mark.parametrize("op", ["add", "subtract", "multiply", "divide", "power"])
def test_binary_operations_format_correctly(tmp_path: Path, op: str) -> None:
    """All binary operations must use binary format."""
    os.chdir(tmp_path)
    history = OperationHistory()

    result = history._format_entry(op, [2.0, 3.0], 5.0)
    # Binary format is "a op b = result"
    assert f"2.0 {op} 3.0 = 5.0" == result


# ---------------------------------------------------------------------------
# File encoding and newline handling
# ---------------------------------------------------------------------------


def test_record_operation_writes_with_newline(tmp_path: Path) -> None:
    """Each record_operation call must append a newline to the file."""
    os.chdir(tmp_path)
    history = OperationHistory()
    history.record_operation("add", [1.0, 2.0], 3.0)
    history.record_operation("multiply", [3.0, 4.0], 12.0)

    history_file = tmp_path / HISTORY_FILE
    content = history_file.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Should have at least 2 non-empty lines (entries) + possibly empty last
    assert len([l for l in lines if l]) == 2


def test_file_uses_utf8_encoding(tmp_path: Path) -> None:
    """History file must be written and read using UTF-8 encoding."""
    os.chdir(tmp_path)
    history = OperationHistory()
    history.record_operation("add", [1.5, 2.5], 4.0)

    history_file = tmp_path / HISTORY_FILE
    # Reading with UTF-8 must work without error
    content = history_file.read_text(encoding="utf-8")
    assert "1.5" in content


def test_multiple_operations_readable_from_file(tmp_path: Path) -> None:
    """Multiple operations in file must be readable as separate lines."""
    os.chdir(tmp_path)
    history = OperationHistory()

    ops = [
        ("add", [1.0, 2.0], 3.0),
        ("multiply", [3.0, 4.0], 12.0),
        ("square", [5.0], 25.0),
    ]
    for op, operands, result in ops:
        history.record_operation(op, operands, result)

    history_file = tmp_path / HISTORY_FILE
    lines = history_file.read_text(encoding="utf-8").strip().split("\n")

    assert len(lines) == 3
    assert "1.0 add 2.0 = 3.0" in lines[0]
    assert "3.0 multiply 4.0 = 12.0" in lines[1]
    assert "square(5.0) = 25.0" in lines[2]
