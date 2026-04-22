"""Comprehensive tests for the OperationHistory class."""

import pytest
import os
from src.history import OperationHistory


class TestOperationHistoryRecord:
    """Test suite for OperationHistory.record_operation() method."""

    @pytest.fixture
    def history_with_tmpfile(self, tmp_path):
        """Fixture providing an OperationHistory instance with temp file."""
        history_file = tmp_path / "history.txt"
        return OperationHistory(str(history_file))

    def test_record_operation_single_unary(self, history_with_tmpfile):
        """Record one unary operation and verify file contains formatted line."""
        history_with_tmpfile.record_operation("square", [5], 25)
        with open(history_with_tmpfile.filename, "r") as f:
            content = f.read()
        assert "square(5) = 25" in content

    def test_record_operation_single_binary(self, history_with_tmpfile):
        """Record one binary operation and verify file contains formatted line."""
        history_with_tmpfile.record_operation("add", [3, 5], 8)
        with open(history_with_tmpfile.filename, "r") as f:
            content = f.read()
        assert "add(3, 5) = 8" in content

    def test_record_operation_multiple(self, history_with_tmpfile):
        """Record multiple operations and verify all appear in order."""
        history_with_tmpfile.record_operation("add", [1, 2], 3)
        history_with_tmpfile.record_operation("multiply", [3, 4], 12)
        history_with_tmpfile.record_operation("divide", [10, 2], 5.0)

        with open(history_with_tmpfile.filename, "r") as f:
            content = f.read()

        lines = content.strip().split("\n")
        assert len(lines) == 3
        assert "add(1, 2) = 3" in lines[0]
        assert "multiply(3, 4) = 12" in lines[1]
        assert "divide(10, 2) = 5.0" in lines[2]

    def test_record_operation_creates_file(self, tmp_path):
        """Verify file is created if it doesn't exist."""
        history_file = tmp_path / "new_history.txt"
        assert not history_file.exists()

        history = OperationHistory(str(history_file))
        history.record_operation("sqrt", [16], 4.0)

        assert history_file.exists()

    def test_record_operation_appends(self, tmp_path):
        """Record, close, record again; verify both in file."""
        history_file = tmp_path / "history.txt"

        history = OperationHistory(str(history_file))
        history.record_operation("add", [1, 1], 2)

        # Create a new instance to simulate separate session
        history2 = OperationHistory(str(history_file))
        history2.record_operation("subtract", [5, 2], 3)

        with open(history_file, "r") as f:
            content = f.read()

        assert "add(1, 1) = 2" in content
        assert "subtract(5, 2) = 3" in content

    @pytest.mark.parametrize("operation,operands,result", [
        ("add", [1, 1], 2),
        ("subtract", [10, 5], 5),
        ("multiply", [3, 7], 21),
        ("divide", [8, 2], 4.0),
        ("square", [5], 25),
        ("cube", [2], 8),
        ("factorial", [5], 120),
    ])
    def test_record_operation_various_operations(self, history_with_tmpfile, operation, operands, result):
        """Test recording various operation types produces correct formatting."""
        history_with_tmpfile.record_operation(operation, operands, result)

        with open(history_with_tmpfile.filename, "r") as f:
            content = f.read()

        operands_str = ", ".join(str(o) for o in operands)
        assert f"{operation}({operands_str}) = {result}" in content

    def test_record_operation_float_operands(self, history_with_tmpfile):
        """Record operation with floating-point operands."""
        history_with_tmpfile.record_operation("divide", [5.5, 2.5], 2.2)

        with open(history_with_tmpfile.filename, "r") as f:
            content = f.read()

        assert "divide(5.5, 2.5) = 2.2" in content

    def test_record_operation_negative_values(self, history_with_tmpfile):
        """Record operation with negative operands and results."""
        history_with_tmpfile.record_operation("multiply", [-3, 4], -12)

        with open(history_with_tmpfile.filename, "r") as f:
            content = f.read()

        assert "multiply(-3, 4) = -12" in content

    def test_record_operation_zero_values(self, history_with_tmpfile):
        """Record operation involving zero."""
        history_with_tmpfile.record_operation("add", [0, 5], 5)
        history_with_tmpfile.record_operation("multiply", [10, 0], 0)

        with open(history_with_tmpfile.filename, "r") as f:
            content = f.read()

        assert "add(0, 5) = 5" in content
        assert "multiply(10, 0) = 0" in content

    def test_record_operation_large_numbers(self, history_with_tmpfile):
        """Record operation with very large numbers."""
        history_with_tmpfile.record_operation("add", [1e10, 2e10], 3e10)

        with open(history_with_tmpfile.filename, "r") as f:
            content = f.read()

        assert "add(10000000000.0, 20000000000.0) = 30000000000.0" in content


class TestOperationHistoryDisplay:
    """Test suite for OperationHistory.display_history() method."""

    @pytest.fixture
    def history_with_tmpfile(self, tmp_path):
        """Fixture providing an OperationHistory instance with temp file."""
        history_file = tmp_path / "history.txt"
        return OperationHistory(str(history_file))

    def test_display_history_empty(self, history_with_tmpfile):
        """Call display on non-existent file, returns 'No history yet.' message."""
        result = history_with_tmpfile.display_history()
        assert result == "No history yet."

    def test_display_history_single(self, history_with_tmpfile):
        """Record one operation, display returns formatted string."""
        history_with_tmpfile.record_operation("add", [3, 5], 8)
        result = history_with_tmpfile.display_history()
        assert "1. add(3, 5) = 8" in result

    def test_display_history_multiple(self, history_with_tmpfile):
        """Record multiple operations, display returns all in order with numbering."""
        history_with_tmpfile.record_operation("add", [1, 2], 3)
        history_with_tmpfile.record_operation("multiply", [3, 4], 12)
        history_with_tmpfile.record_operation("divide", [10, 2], 5.0)

        result = history_with_tmpfile.display_history()

        assert "1. add(1, 2) = 3" in result
        assert "2. multiply(3, 4) = 12" in result
        assert "3. divide(10, 2) = 5.0" in result

    def test_display_history_formatting(self, history_with_tmpfile):
        """Verify format is human-readable with numbering."""
        history_with_tmpfile.record_operation("square", [5], 25)
        history_with_tmpfile.record_operation("cube", [3], 27)

        result = history_with_tmpfile.display_history()

        # Verify numbering format
        lines = result.split("\n")
        assert lines[0].startswith("1. ")
        assert lines[1].startswith("2. ")
        # Verify content
        assert "square(5) = 25" in lines[0]
        assert "cube(3) = 27" in lines[1]

    def test_display_history_after_clear_and_new_record(self, history_with_tmpfile):
        """Display after clearing and recording new operations."""
        history_with_tmpfile.record_operation("add", [1, 1], 2)
        history_with_tmpfile.clear()
        history_with_tmpfile.record_operation("subtract", [5, 3], 2)

        result = history_with_tmpfile.display_history()
        assert "1. subtract(5, 3) = 2" in result
        # Old operation should not appear
        assert "add" not in result

    def test_display_history_preserves_order(self, history_with_tmpfile):
        """Verify operations are displayed in the order they were recorded."""
        operations = [
            ("op1", [1], 1),
            ("op2", [2], 2),
            ("op3", [3], 3),
            ("op4", [4], 4),
            ("op5", [5], 5),
        ]

        for op, operands, result in operations:
            history_with_tmpfile.record_operation(op, operands, result)

        result = history_with_tmpfile.display_history()
        lines = result.split("\n")

        assert len(lines) == 5
        for i, (op, _, _) in enumerate(operations, start=1):
            assert f"{i}. {op}(" in lines[i-1]

    def test_display_history_with_empty_file(self, tmp_path):
        """Create an empty file and verify display returns 'No history yet.'"""
        history_file = tmp_path / "empty.txt"
        history_file.write_text("")

        history = OperationHistory(str(history_file))
        result = history.display_history()
        assert result == "No history yet."


class TestOperationHistoryClear:
    """Test suite for OperationHistory.clear() method."""

    @pytest.fixture
    def history_with_tmpfile(self, tmp_path):
        """Fixture providing an OperationHistory instance with temp file."""
        history_file = tmp_path / "history.txt"
        return OperationHistory(str(history_file))

    def test_clear_removes_file(self, history_with_tmpfile):
        """Create file with content, call clear(), file no longer exists."""
        history_with_tmpfile.record_operation("add", [1, 2], 3)
        assert os.path.exists(history_with_tmpfile.filename)

        history_with_tmpfile.clear()

        assert not os.path.exists(history_with_tmpfile.filename)

    def test_clear_idempotent(self, history_with_tmpfile):
        """Call clear() twice, second succeeds without error."""
        history_with_tmpfile.record_operation("add", [1, 2], 3)
        history_with_tmpfile.clear()

        # Second call should not raise an error
        history_with_tmpfile.clear()

        assert not os.path.exists(history_with_tmpfile.filename)

    def test_clear_non_existent_file(self, tmp_path):
        """Call clear() when file doesn't exist — no exception."""
        history_file = tmp_path / "nonexistent.txt"
        history = OperationHistory(str(history_file))

        # Should not raise FileNotFoundError
        history.clear()

        assert not os.path.exists(history_file)

    def test_clear_then_display_returns_empty_message(self, history_with_tmpfile):
        """After clearing, display_history returns 'No history yet.'"""
        history_with_tmpfile.record_operation("add", [1, 2], 3)
        history_with_tmpfile.clear()

        result = history_with_tmpfile.display_history()
        assert result == "No history yet."

    def test_clear_then_record_creates_new_file(self, history_with_tmpfile):
        """After clearing, record_operation creates a new file with new content."""
        history_with_tmpfile.record_operation("add", [1, 2], 3)
        first_mtime = os.path.getmtime(history_with_tmpfile.filename)

        history_with_tmpfile.clear()
        history_with_tmpfile.record_operation("subtract", [5, 3], 2)

        assert os.path.exists(history_with_tmpfile.filename)
        with open(history_with_tmpfile.filename, "r") as f:
            content = f.read()
        assert "add" not in content
        assert "subtract(5, 3) = 2" in content


class TestOperationHistoryIsEmpty:
    """Test suite for OperationHistory.is_empty() method."""

    @pytest.fixture
    def history_with_tmpfile(self, tmp_path):
        """Fixture providing an OperationHistory instance with temp file."""
        history_file = tmp_path / "history.txt"
        return OperationHistory(str(history_file))

    def test_is_empty_when_file_not_created(self, history_with_tmpfile):
        """Returns True before any operations."""
        result = history_with_tmpfile.is_empty()
        assert result is True

    def test_is_empty_after_clear(self, history_with_tmpfile):
        """Returns True after clearing."""
        history_with_tmpfile.record_operation("add", [1, 2], 3)
        history_with_tmpfile.clear()

        result = history_with_tmpfile.is_empty()
        assert result is True

    def test_is_empty_after_record(self, history_with_tmpfile):
        """Returns False after recording operation."""
        history_with_tmpfile.record_operation("add", [1, 2], 3)

        result = history_with_tmpfile.is_empty()
        assert result is False

    def test_is_empty_with_empty_file(self, tmp_path):
        """Returns True for empty file."""
        history_file = tmp_path / "empty.txt"
        history_file.write_text("")

        history = OperationHistory(str(history_file))
        result = history.is_empty()
        assert result is True

    def test_is_empty_with_single_operation(self, history_with_tmpfile):
        """Returns False after single operation."""
        history_with_tmpfile.record_operation("square", [5], 25)
        result = history_with_tmpfile.is_empty()
        assert result is False

    def test_is_empty_with_multiple_operations(self, history_with_tmpfile):
        """Returns False with multiple operations."""
        history_with_tmpfile.record_operation("add", [1, 2], 3)
        history_with_tmpfile.record_operation("multiply", [3, 4], 12)
        history_with_tmpfile.record_operation("divide", [10, 2], 5.0)

        result = history_with_tmpfile.is_empty()
        assert result is False


class TestOperationHistoryEdgeCases:
    """Edge case tests for OperationHistory."""

    @pytest.fixture
    def history_with_tmpfile(self, tmp_path):
        """Fixture providing an OperationHistory instance with temp file."""
        history_file = tmp_path / "history.txt"
        return OperationHistory(str(history_file))

    def test_record_operation_with_special_characters_in_operation_name(self, history_with_tmpfile):
        """Record operation with special characters (underscores, etc)."""
        history_with_tmpfile.record_operation("square_root", [16], 4.0)

        result = history_with_tmpfile.display_history()
        assert "square_root(16) = 4.0" in result

    def test_record_operation_single_large_operand_list(self, history_with_tmpfile):
        """Record with many operands (though operations typically use 1-2)."""
        history_with_tmpfile.record_operation("sum", [1, 2, 3, 4, 5], 15)

        result = history_with_tmpfile.display_history()
        assert "sum(1, 2, 3, 4, 5) = 15" in result

    def test_filename_initialization(self, tmp_path):
        """Verify OperationHistory respects custom filename."""
        custom_file = tmp_path / "custom_history.txt"
        history = OperationHistory(str(custom_file))

        history.record_operation("add", [1, 1], 2)

        assert str(custom_file) == history.filename
        assert custom_file.exists()

    def test_default_filename(self, tmp_path):
        """Verify default filename is 'history.txt'."""
        # Change to temp directory to avoid creating file in repo
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(str(tmp_path))
            history = OperationHistory()
            assert history.filename == "history.txt"
        finally:
            os.chdir(original_cwd)

    def test_display_history_numbering_consistency(self, history_with_tmpfile):
        """Verify numbering is always sequential 1, 2, 3, ..."""
        for i in range(1, 11):
            history_with_tmpfile.record_operation(f"op{i}", [i], i)

        result = history_with_tmpfile.display_history()
        lines = result.split("\n")

        for i, line in enumerate(lines, start=1):
            assert line.startswith(f"{i}. ")

    def test_record_and_display_with_scientific_notation_result(self, history_with_tmpfile):
        """Record result with scientific notation."""
        history_with_tmpfile.record_operation("power", [10, 20], 1e20)

        result = history_with_tmpfile.display_history()
        assert "power(10, 20) = 1e+20" in result or "power(10, 20) = 1e20" in result
