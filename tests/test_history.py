"""Comprehensive test suite for OperationHistory class."""

import pytest
import os
import tempfile
from pathlib import Path

from src.history import OperationHistory


class TestOperationHistoryRecording:
    """Test suite for recording operations in OperationHistory."""

    def test_record_single_operand_operation(self):
        """Should successfully record a single operand operation."""
        history = OperationHistory()
        history.record_operation("sqrt", [9], 3)
        entries = history.get_history()
        assert len(entries) == 1
        assert "sqrt(9) = 3" in entries[0]

    def test_record_two_operand_operation(self):
        """Should successfully record a binary operation."""
        history = OperationHistory()
        history.record_operation("add", [2, 3], 5)
        entries = history.get_history()
        assert len(entries) == 1
        assert "add(2, 3) = 5" in entries[0]

    def test_record_multiple_operations_in_sequence(self):
        """Should record and preserve order of multiple operations."""
        history = OperationHistory()
        history.record_operation("add", [2, 3], 5)
        history.record_operation("multiply", [5, 2], 10)
        history.record_operation("subtract", [10, 3], 7)
        entries = history.get_history()
        assert len(entries) == 3
        assert "add(2, 3) = 5" in entries[0]
        assert "multiply(5, 2) = 10" in entries[1]
        assert "subtract(10, 3) = 7" in entries[2]

    @pytest.mark.parametrize("args,result", [
        ([2.5], 6.25),  # square(2.5) = 6.25
        ([2, 0.5], 1.4142135623730951),  # power(2, 0.5) ~= 1.414
        ([7, 2], 3.5),  # divide(7, 2) = 3.5
        ([10.5], 110.25),  # square(10.5) = 110.25
    ])
    def test_record_operations_with_float_results(self, args, result):
        """Should correctly record operations that produce float results."""
        history = OperationHistory()
        op_name = "square" if len(args) == 1 else "divide" if len(args) == 2 and args[0] > args[1] else "power"
        history.record_operation(op_name, args, result)
        entries = history.get_history()
        assert len(entries) == 1
        assert op_name in entries[0]
        assert "=" in entries[0]

    @pytest.mark.parametrize("args,result", [
        ([2, 3], 5),    # add(2, 3) = 5
        ([5], 120),     # factorial(5) = 120
        ([2, 3], 8),    # power(2, 3) = 8
        ([100], 10000), # square(100) = 10000
    ])
    def test_record_operations_with_int_results(self, args, result):
        """Should correctly record operations that produce integer results."""
        history = OperationHistory()
        op_name = "add" if len(args) == 2 and result == 5 else "factorial" if len(args) == 1 else "power" if len(args) == 2 and args[1] == 3 else "square"
        history.record_operation(op_name, args, result)
        entries = history.get_history()
        assert len(entries) == 1
        assert str(result) in entries[0]

    @pytest.mark.parametrize("args,result", [
        ([-5, -3], -2),      # subtract(-5, -3) = -2
        ([-10, 5], -50),     # multiply(-10, 5) = -50
        ([5, -2], 3),        # add(5, -2) = 3
    ])
    def test_record_negative_operands(self, args, result):
        """Should correctly record operations with negative operands."""
        history = OperationHistory()
        op_name = "subtract" if args[0] == -5 else "multiply" if args[0] == -10 else "add"
        history.record_operation(op_name, args, result)
        entries = history.get_history()
        assert len(entries) == 1
        assert op_name in entries[0]

    def test_record_zero_result(self):
        """Should correctly record operation that results in zero."""
        history = OperationHistory()
        history.record_operation("subtract", [5, 5], 0)
        entries = history.get_history()
        assert len(entries) == 1
        assert "subtract(5, 5) = 0" in entries[0]

    def test_record_empty_args_list(self):
        """Should handle operation with empty args list (edge case)."""
        history = OperationHistory()
        history.record_operation("constant", [], 42)
        entries = history.get_history()
        assert len(entries) == 1
        assert "constant() = 42" in entries[0]


class TestOperationHistoryFormatting:
    """Test suite for _format_entry static method."""

    def test_format_entry_single_operand(self):
        """Should format single operand operation correctly."""
        result = OperationHistory._format_entry("factorial", [5], 120)
        assert result == "factorial(5) = 120"

    def test_format_entry_two_operands(self):
        """Should format binary operation correctly."""
        result = OperationHistory._format_entry("power", [2, 3], 8)
        assert result == "power(2, 3) = 8"

    def test_format_entry_float_operands(self):
        """Should format float operands correctly."""
        result = OperationHistory._format_entry("divide", [7, 2], 3.5)
        assert result == "divide(7, 2) = 3.5"

    def test_format_entry_whole_float_collapses_operands(self):
        """Should collapse whole-number float operands to int form."""
        result = OperationHistory._format_entry("sqrt", [9.0], 3.0)
        assert result == "sqrt(9) = 3"

    def test_format_entry_whole_float_collapses_result(self):
        """Should collapse whole-number float result to int form."""
        result = OperationHistory._format_entry("add", [2.0, 3.0], 5.0)
        assert result == "add(2, 3) = 5"

    def test_format_entry_mixed_float_int_operands(self):
        """Should correctly format mixed int and float operands."""
        result = OperationHistory._format_entry("multiply", [2.5, 4], 10.0)
        assert result == "multiply(2.5, 4) = 10"

    def test_format_entry_preserves_operation_name(self):
        """Should preserve the operation name as provided."""
        result = OperationHistory._format_entry("MyOperation", [1], 2)
        assert result.startswith("MyOperation(")

    def test_format_entry_lowercase_operation_name(self):
        """Should handle operation names as provided (case-sensitive)."""
        result = OperationHistory._format_entry("add", [1, 2], 3)
        assert result == "add(1, 2) = 3"

    def test_format_entry_negative_operands_in_format(self):
        """Should correctly format negative operands."""
        result = OperationHistory._format_entry("subtract", [-5, -3], -2)
        assert result == "subtract(-5, -3) = -2"

    def test_format_entry_large_numbers(self):
        """Should handle very large numbers without error."""
        result = OperationHistory._format_entry("add", [1e100, 2e100], 3e100)
        # Result should be a valid string with operation format
        assert "add" in result
        assert "=" in result
        assert isinstance(result, str)

    @pytest.mark.parametrize("operands,result,expected", [
        ([1.5, 2.5], 4.0, "add(1.5, 2.5) = 4"),
        ([10.0], 100.0, "square(10) = 100"),
        ([7], 49.0, "square(7) = 49"),
        ([2, 3], 5.0, "add(2, 3) = 5"),
    ])
    def test_format_entry_various_combinations(self, operands, result, expected):
        """Should correctly format various operand and result combinations."""
        op_name = "add" if len(operands) == 2 and operands[0] in [1.5, 2, 10.0] else "square"
        actual = OperationHistory._format_entry(op_name, operands, result)
        assert actual == expected


class TestOperationHistoryRetrieval:
    """Test suite for get_history method."""

    def test_get_history_empty(self):
        """Should return empty list for new history."""
        history = OperationHistory()
        assert history.get_history() == []

    def test_get_history_after_recordings(self):
        """Should return all recorded operations in order."""
        history = OperationHistory()
        history.record_operation("add", [2, 3], 5)
        history.record_operation("multiply", [5, 2], 10)
        entries = history.get_history()
        assert len(entries) == 2
        assert entries[0] == "add(2, 3) = 5"
        assert entries[1] == "multiply(5, 2) = 10"

    def test_get_history_returns_copy(self):
        """Should return a shallow copy, not the internal list."""
        history = OperationHistory()
        history.record_operation("add", [2, 3], 5)
        entries1 = history.get_history()
        entries1.append("fake_entry")
        entries2 = history.get_history()
        # Modifying returned list should not affect internal state
        assert len(entries2) == 1
        assert entries2[0] == "add(2, 3) = 5"

    def test_get_history_maintains_order(self):
        """Should maintain insertion order of operations."""
        history = OperationHistory()
        for i in range(5):
            history.record_operation(f"op{i}", [i], i * 2)
        entries = history.get_history()
        assert len(entries) == 5
        for i, entry in enumerate(entries):
            assert f"op{i}" in entry


class TestOperationHistoryClear:
    """Test suite for clear method."""

    def test_clear_empties_history(self):
        """Should empty history after clear."""
        history = OperationHistory()
        history.record_operation("add", [2, 3], 5)
        history.clear()
        assert history.get_history() == []

    def test_clear_after_recordings(self):
        """Should reset state completely after clear."""
        history = OperationHistory()
        history.record_operation("add", [2, 3], 5)
        history.record_operation("multiply", [5, 2], 10)
        history.clear()
        assert len(history.get_history()) == 0

    def test_clear_allows_new_recordings(self):
        """Should allow recording new operations after clear."""
        history = OperationHistory()
        history.record_operation("add", [2, 3], 5)
        history.clear()
        history.record_operation("subtract", [10, 3], 7)
        entries = history.get_history()
        assert len(entries) == 1
        assert "subtract(10, 3) = 7" in entries[0]

    def test_clear_on_empty_history(self):
        """Should handle clear on already empty history."""
        history = OperationHistory()
        history.clear()
        assert history.get_history() == []


class TestOperationHistoryFilePersistence:
    """Test suite for save_to_file method using temporary files."""

    def test_save_to_file_creates_file(self, tmp_path):
        """Should create file at specified path."""
        history = OperationHistory()
        history.record_operation("add", [2, 3], 5)
        filepath = tmp_path / "history.txt"
        history.save_to_file(str(filepath))
        assert filepath.exists()

    def test_save_to_file_writes_history_entries(self, tmp_path):
        """Should write recorded operations to file."""
        history = OperationHistory()
        history.record_operation("add", [2, 3], 5)
        history.record_operation("multiply", [5, 2], 10)
        filepath = tmp_path / "history.txt"
        history.save_to_file(str(filepath))
        content = filepath.read_text()
        assert "add(2, 3) = 5" in content
        assert "multiply(5, 2) = 10" in content

    def test_save_to_file_one_entry_per_line(self, tmp_path):
        """Should write each entry on a separate line."""
        history = OperationHistory()
        history.record_operation("add", [2, 3], 5)
        history.record_operation("multiply", [5, 2], 10)
        history.record_operation("subtract", [10, 3], 7)
        filepath = tmp_path / "history.txt"
        history.save_to_file(str(filepath))
        lines = filepath.read_text().strip().split("\n")
        assert len(lines) == 3
        assert lines[0] == "add(2, 3) = 5"
        assert lines[1] == "multiply(5, 2) = 10"
        assert lines[2] == "subtract(10, 3) = 7"

    def test_save_to_file_with_empty_history(self, tmp_path):
        """Should create empty file when saving empty history."""
        history = OperationHistory()
        filepath = tmp_path / "history.txt"
        history.save_to_file(str(filepath))
        assert filepath.exists()
        assert filepath.read_text() == ""

    def test_save_to_file_overwrites_existing(self, tmp_path):
        """Should overwrite existing file content."""
        filepath = tmp_path / "history.txt"
        # Write initial content
        filepath.write_text("old content\nmore old\n")
        # Save new history
        history = OperationHistory()
        history.record_operation("add", [1, 1], 2)
        history.save_to_file(str(filepath))
        content = filepath.read_text()
        assert "old content" not in content
        assert "add(1, 1) = 2" in content

    def test_save_to_file_default_filename(self, tmp_path, monkeypatch):
        """Should save to 'history.txt' by default in current directory."""
        monkeypatch.chdir(tmp_path)
        history = OperationHistory()
        history.record_operation("add", [2, 3], 5)
        history.save_to_file()
        filepath = tmp_path / "history.txt"
        assert filepath.exists()

    def test_save_to_file_with_special_characters(self, tmp_path):
        """Should correctly handle entries with special characters."""
        history = OperationHistory()
        history.record_operation("op_with_underscore", [1, 2], 3)
        filepath = tmp_path / "history.txt"
        history.save_to_file(str(filepath))
        content = filepath.read_text()
        assert "op_with_underscore(1, 2) = 3" in content

    def test_save_to_file_preserves_all_entries(self, tmp_path):
        """Should preserve all entries without loss or modification."""
        history = OperationHistory()
        for i in range(10):
            history.record_operation("op", [i], i * 2)
        filepath = tmp_path / "history.txt"
        history.save_to_file(str(filepath))
        lines = filepath.read_text().strip().split("\n")
        assert len(lines) == 10

    def test_save_to_file_with_float_results(self, tmp_path):
        """Should correctly save entries with float results."""
        history = OperationHistory()
        history.record_operation("divide", [7, 2], 3.5)
        filepath = tmp_path / "history.txt"
        history.save_to_file(str(filepath))
        content = filepath.read_text()
        assert "3.5" in content


class TestOperationHistoryEdgeCases:
    """Test suite for edge cases and boundary conditions."""

    def test_record_with_large_numbers(self):
        """Should handle very large numbers without error."""
        history = OperationHistory()
        history.record_operation("add", [1e100, 2e100], 3e100)
        entries = history.get_history()
        assert len(entries) == 1
        assert "add" in entries[0]

    def test_record_with_very_small_numbers(self):
        """Should handle very small numbers without error."""
        history = OperationHistory()
        history.record_operation("multiply", [1e-100, 2e-100], 2e-200)
        entries = history.get_history()
        assert len(entries) == 1
        assert "multiply" in entries[0]

    def test_record_factorial_result(self):
        """Should correctly format factorial results as integers."""
        history = OperationHistory()
        history.record_operation("factorial", [5], 120)
        entries = history.get_history()
        assert entries[0] == "factorial(5) = 120"

    def test_record_with_many_operands(self):
        """Should handle operations with many operands."""
        history = OperationHistory()
        history.record_operation("sum_all", [1, 2, 3, 4, 5], 15)
        entries = history.get_history()
        assert "1, 2, 3, 4, 5" in entries[0]

    def test_format_entry_with_very_precise_float(self):
        """Should preserve float precision in formatting."""
        result = OperationHistory._format_entry("divide", [1, 3], 0.3333333333333333)
        assert "0.333" in result

    def test_history_thread_safety_sequential(self):
        """Should maintain correctness with sequential operations."""
        history = OperationHistory()
        for i in range(100):
            history.record_operation(f"op{i % 10}", [i], i * 2)
        entries = history.get_history()
        assert len(entries) == 100

    def test_format_entry_negative_zero(self):
        """Should correctly handle negative zero."""
        result = OperationHistory._format_entry("subtract", [0.0, 0.0], -0.0)
        assert "0" in result  # -0.0 should display as "0"

    def test_format_entry_scientific_notation_input(self):
        """Should handle operands in scientific notation."""
        result = OperationHistory._format_entry("multiply", [1e5, 2e5], 2e10)
        assert "=" in result

    def test_record_string_representation_of_numbers(self):
        """Should handle numeric operands correctly."""
        history = OperationHistory()
        history.record_operation("add", [2, 3], 5)
        entries = history.get_history()
        assert all(isinstance(e, str) for e in entries)

    def test_clear_and_save_creates_empty_file(self, tmp_path):
        """Should create empty file after clear and save."""
        history = OperationHistory()
        history.record_operation("add", [1, 2], 3)
        history.clear()
        filepath = tmp_path / "history.txt"
        history.save_to_file(str(filepath))
        assert filepath.read_text() == ""
