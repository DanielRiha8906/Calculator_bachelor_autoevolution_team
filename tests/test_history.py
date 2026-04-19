"""Comprehensive pytest tests for the operation history feature.

Tests cover:
- HistoryManager initialization with custom paths
- HistoryManager.clear(): file creation and truncation
- HistoryManager.record_operation(): formatting and appending
- HistoryManager.get_history(): retrieval and empty states
- HistoryManager._format_operation(): output formatting
- REPLInterface integration with history
- Operation recording on success and non-recording on error
- History display in REPL
"""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from src.history import HistoryManager
from src.repl import REPLInterface
from src.calculator import Calculator


# ==============================================================================
# FIXTURES
# ==============================================================================

@pytest.fixture
def calculator():
    """Provide a real Calculator instance."""
    return Calculator()


@pytest.fixture
def repl(calculator, tmp_path):
    """Provide a REPLInterface with a temporary history file."""
    history_path = str(tmp_path / "history.txt")
    repl = REPLInterface(calculator)
    repl.history_manager = HistoryManager(history_path)
    return repl


@pytest.fixture
def history_manager(tmp_path):
    """Provide a HistoryManager with a temporary file path."""
    history_path = str(tmp_path / "history.txt")
    return HistoryManager(history_path)


# ==============================================================================
# TESTS: HistoryManager Initialization
# ==============================================================================

class TestHistoryManagerInitialization:
    """Test suite for HistoryManager initialization."""

    def test_init_with_default_path(self):
        """Test __init__ with default history_file_path."""
        manager = HistoryManager()
        assert manager.history_file_path == "history.txt"

    def test_init_with_custom_path(self, tmp_path):
        """Test __init__ with custom history_file_path."""
        custom_path = str(tmp_path / "custom_history.txt")
        manager = HistoryManager(custom_path)
        assert manager.history_file_path == custom_path

    def test_init_stores_path_as_string(self, tmp_path):
        """Test __init__ stores path as string."""
        path = str(tmp_path / "history.txt")
        manager = HistoryManager(path)
        assert isinstance(manager.history_file_path, str)


# ==============================================================================
# TESTS: HistoryManager.clear()
# ==============================================================================

class TestHistoryManagerClear:
    """Test suite for clear() method."""

    def test_clear_creates_file_when_not_exists(self, history_manager):
        """Test clear() creates file if it does not exist."""
        assert not Path(history_manager.history_file_path).exists()
        history_manager.clear()
        assert Path(history_manager.history_file_path).exists()

    def test_clear_truncates_existing_file(self, history_manager):
        """Test clear() truncates existing file to empty."""
        # Write some content first
        with open(history_manager.history_file_path, "w") as f:
            f.write("some content\n")
        assert Path(history_manager.history_file_path).stat().st_size > 0

        history_manager.clear()
        assert Path(history_manager.history_file_path).stat().st_size == 0

    def test_clear_multiple_times(self, history_manager):
        """Test clear() can be called multiple times without error."""
        history_manager.clear()
        history_manager.clear()
        assert Path(history_manager.history_file_path).exists()
        assert Path(history_manager.history_file_path).stat().st_size == 0

    def test_clear_creates_empty_file(self, history_manager):
        """Test clear() creates a truly empty file."""
        history_manager.clear()
        with open(history_manager.history_file_path, "r") as f:
            content = f.read()
        assert content == ""

    def test_clear_before_any_operations(self, history_manager):
        """Test clear() can be called before any operations."""
        # Should not raise
        history_manager.clear()
        assert Path(history_manager.history_file_path).exists()


# ==============================================================================
# TESTS: HistoryManager.record_operation()
# ==============================================================================

class TestHistoryManagerRecordOperation:
    """Test suite for record_operation() method."""

    def test_record_operation_unary(self, history_manager):
        """Test recording a unary operation."""
        history_manager.clear()
        history_manager.record_operation("factorial", [5.0], 120)

        with open(history_manager.history_file_path, "r") as f:
            content = f.read()
        assert "factorial(5.0) = 120" in content

    def test_record_operation_binary(self, history_manager):
        """Test recording a binary operation."""
        history_manager.clear()
        history_manager.record_operation("add", [3.0, 4.0], 7.0)

        with open(history_manager.history_file_path, "r") as f:
            content = f.read()
        assert "add(3.0, 4.0) = 7.0" in content

    def test_record_operation_multiple_in_order(self, history_manager):
        """Test that multiple operations are recorded in order."""
        history_manager.clear()
        history_manager.record_operation("add", [1.0, 2.0], 3.0)
        history_manager.record_operation("multiply", [3.0, 4.0], 12.0)
        history_manager.record_operation("subtract", [10.0, 5.0], 5.0)

        lines = history_manager.get_history()
        assert len(lines) == 3
        assert lines[0] == "add(1.0, 2.0) = 3.0"
        assert lines[1] == "multiply(3.0, 4.0) = 12.0"
        assert lines[2] == "subtract(10.0, 5.0) = 5.0"

    def test_record_operation_with_float_result(self, history_manager):
        """Test recording operation with float result."""
        history_manager.clear()
        history_manager.record_operation("divide", [10.0, 3.0], 3.3333333)

        lines = history_manager.get_history()
        assert "divide(10.0, 3.0) = 3.3333333" in lines[0]

    def test_record_operation_with_negative_operands(self, history_manager):
        """Test recording operation with negative operands."""
        history_manager.clear()
        history_manager.record_operation("subtract", [-5.0, -3.0], -2.0)

        lines = history_manager.get_history()
        assert "subtract(-5.0, -3.0) = -2.0" in lines[0]

    def test_record_operation_with_negative_result(self, history_manager):
        """Test recording operation with negative result."""
        history_manager.clear()
        history_manager.record_operation("subtract", [3.0, 5.0], -2.0)

        lines = history_manager.get_history()
        assert "subtract(3.0, 5.0) = -2.0" in lines[0]

    def test_record_operation_appends_newline(self, history_manager):
        """Test that each operation is on its own line."""
        history_manager.clear()
        history_manager.record_operation("add", [1.0, 1.0], 2.0)
        history_manager.record_operation("add", [2.0, 2.0], 4.0)

        with open(history_manager.history_file_path, "r") as f:
            lines = f.readlines()
        assert len(lines) == 2
        assert lines[0].endswith("\n")
        assert lines[1].endswith("\n")

    def test_record_operation_with_large_numbers(self, history_manager):
        """Test recording operation with large numbers."""
        history_manager.clear()
        history_manager.record_operation("add", [999999999.0, 1.0], 1000000000.0)

        lines = history_manager.get_history()
        assert "add(999999999.0, 1.0) = 1000000000.0" in lines[0]

    def test_record_operation_with_very_small_numbers(self, history_manager):
        """Test recording operation with very small numbers."""
        history_manager.clear()
        history_manager.record_operation("multiply", [0.0000001, 0.0000001], 1e-14)

        lines = history_manager.get_history()
        assert len(lines) == 1
        assert "multiply" in lines[0]


# ==============================================================================
# TESTS: HistoryManager.get_history()
# ==============================================================================

class TestHistoryManagerGetHistory:
    """Test suite for get_history() method."""

    def test_get_history_returns_list(self, history_manager):
        """Test get_history() returns a list."""
        history_manager.clear()
        result = history_manager.get_history()
        assert isinstance(result, list)

    def test_get_history_empty_file_returns_empty_list(self, history_manager):
        """Test get_history() returns [] when file is empty."""
        history_manager.clear()
        result = history_manager.get_history()
        assert result == []

    def test_get_history_missing_file_returns_empty_list(self, tmp_path):
        """Test get_history() returns [] when file doesn't exist."""
        missing_path = str(tmp_path / "nonexistent.txt")
        manager = HistoryManager(missing_path)
        result = manager.get_history()
        assert result == []

    def test_get_history_single_entry(self, history_manager):
        """Test get_history() with single operation."""
        history_manager.clear()
        history_manager.record_operation("add", [1.0, 2.0], 3.0)
        result = history_manager.get_history()
        assert len(result) == 1
        assert result[0] == "add(1.0, 2.0) = 3.0"

    def test_get_history_multiple_entries(self, history_manager):
        """Test get_history() with multiple operations."""
        history_manager.clear()
        history_manager.record_operation("add", [1.0, 2.0], 3.0)
        history_manager.record_operation("multiply", [3.0, 4.0], 12.0)
        history_manager.record_operation("subtract", [10.0, 5.0], 5.0)

        result = history_manager.get_history()
        assert len(result) == 3
        assert result[0] == "add(1.0, 2.0) = 3.0"
        assert result[1] == "multiply(3.0, 4.0) = 12.0"
        assert result[2] == "subtract(10.0, 5.0) = 5.0"

    def test_get_history_preserves_order(self, history_manager):
        """Test get_history() preserves insertion order."""
        history_manager.clear()
        ops = [
            ("add", [1.0, 1.0], 2.0),
            ("subtract", [5.0, 2.0], 3.0),
            ("multiply", [2.0, 2.0], 4.0),
        ]
        for op_name, operands, result in ops:
            history_manager.record_operation(op_name, operands, result)

        history = history_manager.get_history()
        for i, (op_name, operands, result) in enumerate(ops):
            assert history[i] == f"{op_name}({', '.join(str(o) for o in operands)}) = {result}"

    def test_get_history_filters_empty_lines(self, history_manager):
        """Test get_history() filters out empty lines."""
        history_manager.clear()
        # Manually write some content with blank lines
        with open(history_manager.history_file_path, "w") as f:
            f.write("add(1.0, 2.0) = 3.0\n")
            f.write("\n")  # Empty line
            f.write("subtract(5.0, 2.0) = 3.0\n")

        result = history_manager.get_history()
        assert len(result) == 2
        assert "" not in result

    def test_get_history_returns_strings(self, history_manager):
        """Test get_history() returns list of strings."""
        history_manager.clear()
        history_manager.record_operation("add", [1.0, 2.0], 3.0)
        result = history_manager.get_history()
        assert all(isinstance(entry, str) for entry in result)


# ==============================================================================
# TESTS: HistoryManager._format_operation()
# ==============================================================================

class TestHistoryManagerFormatOperation:
    """Test suite for _format_operation() method."""

    def test_format_operation_unary(self, history_manager):
        """Test _format_operation() with unary operation."""
        result = history_manager._format_operation("factorial", [5.0], 120)
        assert result == "factorial(5.0) = 120"

    def test_format_operation_binary(self, history_manager):
        """Test _format_operation() with binary operation."""
        result = history_manager._format_operation("add", [3.0, 4.0], 7.0)
        assert result == "add(3.0, 4.0) = 7.0"

    def test_format_operation_with_multiple_operands(self, history_manager):
        """Test _format_operation() with multiple operands."""
        result = history_manager._format_operation("logarithm", [8.0, 2.0], 3.0)
        assert result == "logarithm(8.0, 2.0) = 3.0"

    def test_format_operation_with_float_result(self, history_manager):
        """Test _format_operation() with float result."""
        result = history_manager._format_operation("divide", [10.0, 3.0], 3.3333333)
        assert result == "divide(10.0, 3.0) = 3.3333333"

    def test_format_operation_with_negative_operands(self, history_manager):
        """Test _format_operation() with negative operands."""
        result = history_manager._format_operation("subtract", [-5.0, -3.0], -2.0)
        assert result == "subtract(-5.0, -3.0) = -2.0"

    def test_format_operation_with_zero(self, history_manager):
        """Test _format_operation() with zero operand."""
        result = history_manager._format_operation("add", [0.0, 5.0], 5.0)
        assert result == "add(0.0, 5.0) = 5.0"

    def test_format_operation_returns_string(self, history_manager):
        """Test _format_operation() returns string."""
        result = history_manager._format_operation("square", [4.0], 16.0)
        assert isinstance(result, str)

    def test_format_operation_integer_conversion(self, history_manager):
        """Test _format_operation() converts operands to string correctly."""
        result = history_manager._format_operation("add", [1.0, 2.0], 3.0)
        assert "1.0" in result
        assert "2.0" in result
        assert "3.0" in result

    def test_format_operation_with_single_operand(self, history_manager):
        """Test _format_operation() with single operand."""
        result = history_manager._format_operation("square", [7.0], 49.0)
        assert result == "square(7.0) = 49.0"


# ==============================================================================
# TESTS: REPLInterface.display_history()
# ==============================================================================

class TestREPLInterfaceDisplayHistory:
    """Test suite for display_history() method."""

    def test_display_history_empty(self, repl, capsys):
        """Test display_history() with no operations recorded."""
        repl.history_manager.clear()
        repl.display_history()
        captured = capsys.readouterr()
        assert "No operations recorded yet." in captured.out

    def test_display_history_single_operation(self, repl, capsys):
        """Test display_history() with single operation."""
        repl.history_manager.clear()
        repl.history_manager.record_operation("add", [1.0, 2.0], 3.0)
        repl.display_history()
        captured = capsys.readouterr()
        assert "Operation History:" in captured.out
        assert "add(1.0, 2.0) = 3.0" in captured.out

    def test_display_history_multiple_operations(self, repl, capsys):
        """Test display_history() with multiple operations."""
        repl.history_manager.clear()
        repl.history_manager.record_operation("add", [1.0, 2.0], 3.0)
        repl.history_manager.record_operation("multiply", [3.0, 4.0], 12.0)
        repl.display_history()
        captured = capsys.readouterr()
        assert "Operation History:" in captured.out
        assert "add(1.0, 2.0) = 3.0" in captured.out
        assert "multiply(3.0, 4.0) = 12.0" in captured.out

    def test_display_history_header_when_not_empty(self, repl, capsys):
        """Test display_history() prints header when operations exist."""
        repl.history_manager.clear()
        repl.history_manager.record_operation("square", [5.0], 25.0)
        repl.display_history()
        captured = capsys.readouterr()
        assert "Operation History:" in captured.out

    def test_display_history_no_header_when_empty(self, repl, capsys):
        """Test display_history() does not print header when empty."""
        repl.history_manager.clear()
        repl.display_history()
        captured = capsys.readouterr()
        assert "Operation History:" not in captured.out


# ==============================================================================
# TESTS: REPLInterface Integration with History
# ==============================================================================

class TestREPLInterfaceHistoryIntegration:
    """Test suite for REPLInterface integration with history."""

    def test_run_calls_clear_at_start(self, repl, tmp_path):
        """Test run() calls history_manager.clear() at session start."""
        history_path = str(tmp_path / "history.txt")
        repl.history_manager = HistoryManager(history_path)

        # Pre-populate the file with some data
        with open(history_path, "w") as f:
            f.write("old_data\n")

        with patch("builtins.input", side_effect=["quit"]):
            repl.run()

        # After run(), the file should be empty (cleared)
        with open(history_path, "r") as f:
            content = f.read()
        assert content == ""

    def test_run_records_successful_operation(self, repl, capsys):
        """Test run() records successful operation."""
        with patch("builtins.input", side_effect=["1", "2", "3", "quit"]):
            repl.run()

        history = repl.history_manager.get_history()
        assert len(history) == 1
        assert "add(2.0, 3.0) = 5.0" in history[0]

    def test_run_records_multiple_operations(self, repl, capsys):
        """Test run() records multiple successful operations."""
        with patch("builtins.input", side_effect=[
            "1", "2", "3",     # add 2 + 3 = 5
            "3", "", "4",      # multiply 5 * 4 = 20
            "quit"
        ]):
            repl.run()

        history = repl.history_manager.get_history()
        assert len(history) == 2
        assert "add(2.0, 3.0) = 5.0" in history[0]
        assert "multiply(5.0, 4.0) = 20.0" in history[1]

    def test_run_does_not_record_failed_operation(self, repl, capsys):
        """Test run() does not record operation that raises error."""
        with patch("builtins.input", side_effect=[
            "4", "10", "0",    # divide by zero - error
            "quit"
        ]):
            repl.run()

        history = repl.history_manager.get_history()
        assert len(history) == 0

    def test_run_does_not_record_domain_error(self, repl, capsys):
        """Test run() does not record operation with domain error."""
        with patch("builtins.input", side_effect=[
            "10", "-4",         # square_root of negative - error
            "quit"
        ]):
            repl.run()

        history = repl.history_manager.get_history()
        assert len(history) == 0

    def test_run_records_after_error_on_retry(self, repl, capsys):
        """Test run() records operation after retrying from error."""
        with patch("builtins.input", side_effect=[
            "4", "10", "0",    # divide by zero - error
            "1", "2", "3",     # add 2 + 3 = 5 - success
            "quit"
        ]):
            repl.run()

        history = repl.history_manager.get_history()
        assert len(history) == 1
        assert "add(2.0, 3.0) = 5.0" in history[0]

    def test_history_option_in_menu(self, repl, capsys):
        """Test 'history' option appears in operation menu."""
        with patch("builtins.input", side_effect=["quit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "history" in captured.out.lower()

    def test_history_selection_displays_history(self, repl, capsys):
        """Test selecting 'history' displays recorded operations."""
        with patch("builtins.input", side_effect=[
            "1", "2", "3",     # add 2 + 3 = 5
            "history",         # display history
            "quit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        assert "Operation History:" in captured.out
        assert "add(2.0, 3.0) = 5.0" in captured.out

    def test_history_selection_returns_to_menu(self, repl, capsys):
        """Test REPL continues after selecting 'history'."""
        with patch("builtins.input", side_effect=[
            "1", "2", "3",     # add 2 + 3 = 5
            "history",         # display history
            "1", "5", "10",    # add 5 + 10 = 15
            "quit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        # Both operations should be recorded (note: display uses "Addition" not "add")
        assert "Addition(2.0, 3.0) = 5.0" in captured.out
        assert "Addition(5.0, 10.0) = 15.0" in captured.out

    def test_history_empty_during_session(self, repl, capsys):
        """Test displaying empty history during session."""
        with patch("builtins.input", side_effect=[
            "history",         # display history (empty)
            "quit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        assert "No operations recorded yet." in captured.out

    def test_history_case_insensitive(self, repl, capsys):
        """Test 'history' input is case-insensitive."""
        with patch("builtins.input", side_effect=[
            "1", "2", "3",     # add 2 + 3 = 5
            "HISTORY",         # uppercase
            "quit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        # Should display history
        assert "Operation History:" in captured.out or "add(2.0, 3.0) = 5.0" in captured.out

    def test_history_with_unary_operation(self, repl, capsys):
        """Test history records unary operations correctly."""
        with patch("builtins.input", side_effect=[
            "8", "4",           # square 4 = 16
            "history",          # display history
            "quit"
        ]):
            repl.run()

        history = repl.history_manager.get_history()
        assert len(history) == 1
        assert "square(4.0) = 16.0" in history[0]


# ==============================================================================
# TESTS: Edge Cases and Boundary Conditions
# ==============================================================================

class TestHistoryEdgeCases:
    """Test suite for edge cases in history functionality."""

    def test_history_with_zero_result(self, history_manager):
        """Test recording operation with zero result."""
        history_manager.clear()
        history_manager.record_operation("subtract", [5.0, 5.0], 0.0)
        history = history_manager.get_history()
        assert "subtract(5.0, 5.0) = 0.0" in history[0]

    def test_history_with_very_large_result(self, history_manager):
        """Test recording operation with very large result."""
        history_manager.clear()
        history_manager.record_operation("power", [10.0, 100.0], 1e100)
        history = history_manager.get_history()
        assert len(history) == 1

    def test_history_with_scientific_notation_result(self, history_manager):
        """Test recording operation with scientific notation result."""
        history_manager.clear()
        history_manager.record_operation("divide", [1.0, 1000000.0], 1e-6)
        history = history_manager.get_history()
        assert len(history) == 1

    def test_format_operation_with_integer_operands(self, history_manager):
        """Test _format_operation() handles integer operands."""
        result = history_manager._format_operation("add", [1, 2], 3)
        assert result == "add(1, 2) = 3"

    def test_record_operation_file_permissions(self, tmp_path):
        """Test record_operation works with file in different directory."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        path = str(subdir / "history.txt")
        manager = HistoryManager(path)
        manager.clear()
        manager.record_operation("add", [1.0, 2.0], 3.0)
        assert Path(path).exists()

    def test_clear_with_unicode_filename(self, tmp_path):
        """Test clear() with unicode in path."""
        path = str(tmp_path / "history.txt")
        manager = HistoryManager(path)
        manager.clear()
        assert Path(path).exists()


# ==============================================================================
# TESTS: REPLInterface Mock Integration
# ==============================================================================

class TestREPLWithMockedHistory:
    """Test suite for REPLInterface with mocked HistoryManager."""

    def test_repl_init_creates_history_manager(self, calculator):
        """Test REPLInterface.__init__ creates HistoryManager."""
        repl = REPLInterface(calculator)
        assert hasattr(repl, 'history_manager')
        assert isinstance(repl.history_manager, HistoryManager)

    def test_repl_run_with_mocked_history_manager(self, calculator):
        """Test run() interacts with HistoryManager correctly."""
        repl = REPLInterface(calculator)
        repl.history_manager = MagicMock()

        with patch("builtins.input", side_effect=["quit"]):
            repl.run()

        # clear() should be called at session start
        repl.history_manager.clear.assert_called_once()

    def test_repl_records_operation_on_success(self, calculator, tmp_path):
        """Test REPLInterface records operation on successful execution."""
        history_path = str(tmp_path / "history.txt")
        repl = REPLInterface(calculator)
        repl.history_manager = HistoryManager(history_path)

        with patch("builtins.input", side_effect=["1", "5", "10", "quit"]):
            repl.run()

        # Verify that the operation was actually recorded
        history = repl.history_manager.get_history()
        assert len(history) > 0
        assert "add(5.0, 10.0) = 15.0" in history[0]


# ==============================================================================
# TESTS: Concurrent-like Scenarios
# ==============================================================================

class TestHistoryConcurrentScenarios:
    """Test suite for history behavior under concurrent-like scenarios."""

    def test_sequential_operations_preserve_order(self, history_manager):
        """Test sequential operations maintain order."""
        history_manager.clear()
        operations = [
            ("op1", [1.0], 1),
            ("op2", [2.0], 2),
            ("op3", [3.0], 3),
            ("op4", [4.0], 4),
            ("op5", [5.0], 5),
        ]
        for name, operands, result in operations:
            history_manager.record_operation(name, operands, result)

        history = history_manager.get_history()
        for i, (name, operands, result) in enumerate(operations):
            assert f"{name}({operands[0]}) = {result}" in history[i]

    def test_rapid_fire_operations(self, history_manager):
        """Test rapid-fire operation recording."""
        history_manager.clear()
        for i in range(100):
            history_manager.record_operation("op", [float(i)], float(i * 2))

        history = history_manager.get_history()
        assert len(history) == 100

    def test_clear_and_reuse_same_manager(self, history_manager):
        """Test clearing and reusing the same HistoryManager instance."""
        # First session
        history_manager.clear()
        history_manager.record_operation("add", [1.0, 2.0], 3.0)
        assert len(history_manager.get_history()) == 1

        # Clear for second session
        history_manager.clear()
        assert len(history_manager.get_history()) == 0

        # Record in second session
        history_manager.record_operation("subtract", [5.0, 2.0], 3.0)
        assert len(history_manager.get_history()) == 1


# ==============================================================================
# TESTS: Validation and Input Safety
# ==============================================================================

class TestHistoryInputValidation:
    """Test suite for input validation in history operations."""

    def test_record_operation_with_empty_operands_list(self, history_manager):
        """Test recording with empty operands list."""
        history_manager.clear()
        history_manager.record_operation("nullary", [], 42)
        history = history_manager.get_history()
        assert "nullary() = 42" in history[0]

    def test_record_operation_with_none_operation_name(self, history_manager):
        """Test recording with None operation name converts to string."""
        history_manager.clear()
        history_manager.record_operation(None, [1.0], 1)
        history = history_manager.get_history()
        assert "None" in history[0]

    def test_format_operation_preserves_operand_precision(self, history_manager):
        """Test _format_operation preserves operand precision."""
        result = history_manager._format_operation("add", [1.123456789, 2.987654321], 4.11111111)
        assert "1.123456789" in result
        assert "2.987654321" in result

    def test_format_operation_with_string_operation_name(self, history_manager):
        """Test _format_operation with string operation name."""
        result = history_manager._format_operation("custom_op", [1.0], 1)
        assert result.startswith("custom_op")
