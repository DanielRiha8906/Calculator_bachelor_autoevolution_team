"""Comprehensive tests for OperationHistory class."""

import pytest
import tempfile
from pathlib import Path

from src.history import OperationHistory


class TestOperationHistoryFormatting:
    """Test suite for OperationHistory._format_entry formatting logic."""

    @pytest.fixture
    def history(self):
        """Fixture providing a fresh OperationHistory instance."""
        return OperationHistory()

    def test_format_binary_operation(self, history):
        """Test formatting binary operation: add(2, 3) = 5."""
        formatted = history._format_entry("add", [2, 3], 5)
        assert formatted == "add(2, 3) = 5"

    def test_format_unary_operation(self, history):
        """Test formatting unary operation: sqrt(9) = 3."""
        formatted = history._format_entry("square_root", [9], 3.0)
        assert formatted == "square_root(9) = 3"

    def test_format_multi_arg_operation(self, history):
        """Test formatting with multiple arguments: power(2, 3) = 8."""
        formatted = history._format_entry("power", [2, 3], 8.0)
        assert formatted == "power(2, 3) = 8"

    def test_format_with_negative_args(self, history):
        """Test formatting with negative arguments: add(-2, 3) = 1."""
        formatted = history._format_entry("add", [-2, 3], 1)
        assert formatted == "add(-2, 3) = 1"

    def test_format_with_float_results(self, history):
        """Test decimal values preserved: divide(7, 2) = 3.5."""
        formatted = history._format_entry("divide", [7, 2], 3.5)
        assert formatted == "divide(7, 2) = 3.5"

    def test_format_single_int_arg(self, history):
        """Test formatting single int argument: factorial(5) = 120."""
        formatted = history._format_entry("factorial", [5], 120)
        assert formatted == "factorial(5) = 120"

    def test_format_whole_number_float_displayed_as_int(self, history):
        """Test whole-number float 5.0 displayed as 5."""
        formatted = history._format_entry("multiply", [2.0, 2.5], 5.0)
        # Note: 2.0 is also a whole-number float, so it gets displayed as 2
        assert formatted == "multiply(2, 2.5) = 5"

    def test_format_very_small_float_preserved(self, history):
        """Test very small float values are preserved."""
        formatted = history._format_entry("divide", [1, 1000000], 1e-6)
        assert "1e-06" in formatted or "0.000001" in formatted

    def test_format_very_large_float_preserved(self, history):
        """Test very large float values are preserved."""
        formatted = history._format_entry("multiply", [1e10, 1e10], 1e20)
        # Large floats that are whole numbers are displayed as ints
        assert "100000000000000000000" in formatted

    def test_format_negative_whole_float_result(self, history):
        """Test negative whole-number float result displayed as int."""
        formatted = history._format_entry("subtract", [3, 8], -5.0)
        assert formatted == "subtract(3, 8) = -5"

    def test_format_zero_float_result(self, history):
        """Test zero float result displayed as 0 not 0.0."""
        formatted = history._format_entry("subtract", [5, 5], 0.0)
        assert formatted == "subtract(5, 5) = 0"

    def test_format_with_float_args(self, history):
        """Test formatting with float arguments."""
        formatted = history._format_entry("add", [1.5, 2.5], 4.0)
        assert formatted == "add(1.5, 2.5) = 4"

    def test_format_bool_not_treated_as_int(self, history):
        """Test that bool values use repr (not treated as int/float)."""
        formatted = history._format_entry("equal", [1, 1], True)
        assert "True" in formatted


class TestOperationHistoryStorage:
    """Test suite for OperationHistory entry storage."""

    @pytest.fixture
    def history(self):
        """Fixture providing a fresh OperationHistory instance."""
        return OperationHistory()

    def test_add_entry_appends_to_history(self, history):
        """Test that add_entry appends an entry to history."""
        assert len(history.get_entries()) == 0
        history.add_entry("add", [2, 3], 5)
        assert len(history.get_entries()) == 1
        assert history.get_entries()[0] == "add(2, 3) = 5"

    def test_get_entries_returns_copy(self, history):
        """Test that get_entries returns a copy, not a reference."""
        history.add_entry("add", [2, 3], 5)
        entries1 = history.get_entries()
        entries2 = history.get_entries()
        assert entries1 == entries2
        # Mutate one list and verify it doesn't affect internal state
        entries1.append("fake entry")
        assert len(history.get_entries()) == 1

    def test_clear_empties_history(self, history):
        """Test that clear() removes all entries."""
        history.add_entry("add", [2, 3], 5)
        history.add_entry("multiply", [2, 3], 6)
        assert len(history.get_entries()) == 2
        history.clear()
        assert len(history.get_entries()) == 0

    def test_history_initially_empty(self, history):
        """Test that a fresh OperationHistory has no entries."""
        assert history.get_entries() == []

    def test_add_multiple_entries_maintains_order(self, history):
        """Test that multiple entries maintain insertion order."""
        history.add_entry("add", [1, 1], 2)
        history.add_entry("multiply", [2, 3], 6)
        history.add_entry("subtract", [10, 5], 5)
        entries = history.get_entries()
        assert len(entries) == 3
        assert entries[0] == "add(1, 1) = 2"
        assert entries[1] == "multiply(2, 3) = 6"
        assert entries[2] == "subtract(10, 5) = 5"

    def test_add_entry_with_different_result_types(self, history):
        """Test add_entry works with different result types."""
        history.add_entry("add", [1, 2], 3)  # int result
        history.add_entry("divide", [7, 2], 3.5)  # float result
        history.add_entry("factorial", [3], 6)  # int result
        assert len(history.get_entries()) == 3


class TestOperationHistoryPersistence:
    """Test suite for file persistence using tmp_path fixture."""

    @pytest.fixture
    def history(self):
        """Fixture providing a fresh OperationHistory instance."""
        return OperationHistory()

    def test_write_to_file_creates_file(self, history, tmp_path):
        """Test that write_to_file creates a file."""
        history.add_entry("add", [2, 3], 5)
        filepath = tmp_path / "history.txt"
        history.write_to_file(str(filepath))
        assert filepath.exists()

    def test_write_to_file_format(self, history, tmp_path):
        """Test that each line matches expected format: op(args) = result."""
        history.add_entry("add", [2, 3], 5)
        filepath = tmp_path / "history.txt"
        history.write_to_file(str(filepath))
        content = filepath.read_text(encoding="utf-8")
        assert content == "add(2, 3) = 5\n"

    def test_write_to_file_multiple_entries(self, history, tmp_path):
        """Test that multiple entries are written correctly."""
        history.add_entry("add", [2, 3], 5)
        history.add_entry("multiply", [4, 5], 20)
        history.add_entry("divide", [10, 2], 5.0)
        filepath = tmp_path / "history.txt"
        history.write_to_file(str(filepath))
        content = filepath.read_text(encoding="utf-8")
        lines = content.strip().split("\n")
        assert len(lines) == 3
        assert lines[0] == "add(2, 3) = 5"
        assert lines[1] == "multiply(4, 5) = 20"
        assert lines[2] == "divide(10, 2) = 5"

    def test_write_to_file_overwrites_existing(self, history, tmp_path):
        """Test that writing overwrites old content."""
        filepath = tmp_path / "history.txt"
        # Write initial content
        filepath.write_text("old content\n")
        # Write new history
        history.add_entry("add", [1, 1], 2)
        history.write_to_file(str(filepath))
        content = filepath.read_text(encoding="utf-8")
        assert content == "add(1, 1) = 2\n"
        assert "old content" not in content

    def test_write_to_file_empty_history(self, history, tmp_path):
        """Test that writing empty history creates an empty file."""
        filepath = tmp_path / "history.txt"
        history.write_to_file(str(filepath))
        assert filepath.exists()
        content = filepath.read_text(encoding="utf-8")
        assert content == ""

    def test_write_to_file_utf8_encoding(self, history, tmp_path):
        """Test that file is written in UTF-8 encoding."""
        history.add_entry("add", [2, 3], 5)
        filepath = tmp_path / "history.txt"
        history.write_to_file(str(filepath))
        # Read with UTF-8 explicitly
        content = filepath.read_text(encoding="utf-8")
        assert "add(2, 3) = 5" in content

    def test_write_to_file_relative_path(self, history, tmp_path):
        """Test writing to a relative path."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(str(tmp_path))
            history.add_entry("add", [1, 2], 3)
            history.write_to_file("test_history.txt")
            assert Path("test_history.txt").exists()
        finally:
            os.chdir(original_cwd)

    def test_write_to_file_absolute_path(self, history, tmp_path):
        """Test writing to an absolute path."""
        history.add_entry("subtract", [10, 3], 7)
        filepath = tmp_path / "absolute_history.txt"
        history.write_to_file(str(filepath.absolute()))
        assert filepath.exists()
        assert "subtract(10, 3) = 7" in filepath.read_text()
