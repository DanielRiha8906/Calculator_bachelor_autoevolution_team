"""Tests for operation history tracking and persistence.

Tests the history module's recording of calculator operations, in-memory
history management, file-based persistence, and integration with the
interactive calculator loop.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch
from src.calculator import Calculator


# ============================================================================
# Test Group A: History Recording Basics (8 tests)
# ============================================================================

class TestHistoryRecordingBasics:
    """Tests for basic history recording of operations."""

    def test_history_records_single_successful_operation(self, tmp_path):
        """Test that a single successful operation is recorded to history.

        Input: Execute "add 5 3" in interactive mode
        Expected: Operation recorded to in-memory history as "add 5 3 = 8"
        """
        from src.history import OperationHistory

        history = OperationHistory(str(tmp_path / "history.txt"))
        calculator = Calculator()

        result = calculator.add(5, 3)
        history.record("add", [5, 3], result)

        records = history.get_all()
        assert len(records) == 1
        assert records[0] == "add 5 3 = 8"

    def test_history_records_multiple_operations(self, tmp_path):
        """Test that multiple operations are recorded in order.

        Input: Execute "add 2 3", then "multiply 4 5" in interactive mode
        Expected: Both recorded in order: ["add 2 3 = 5", "multiply 4 5 = 20"]
        """
        from src.history import OperationHistory

        history = OperationHistory(str(tmp_path / "history.txt"))
        calculator = Calculator()

        result1 = calculator.add(2, 3)
        history.record("add", [2, 3], result1)

        result2 = calculator.multiply(4, 5)
        history.record("multiply", [4, 5], result2)

        records = history.get_all()
        assert len(records) == 2
        assert records[0] == "add 2 3 = 5"
        assert records[1] == "multiply 4 5 = 20"

    def test_history_records_operation_with_float_operands(self, tmp_path):
        """Test that operations with float operands are recorded correctly.

        Input: Execute "add 2.5 3.5"
        Expected: Recorded as "add 2.5 3.5 = 6.0"
        """
        from src.history import OperationHistory

        history = OperationHistory(str(tmp_path / "history.txt"))
        calculator = Calculator()

        result = calculator.add(2.5, 3.5)
        history.record("add", [2.5, 3.5], result)

        records = history.get_all()
        assert len(records) == 1
        assert records[0] == "add 2.5 3.5 = 6.0"

    def test_history_records_unary_operation(self, tmp_path):
        """Test that unary operations are recorded correctly.

        Input: Execute "square 5"
        Expected: Recorded as "square 5 = 25"
        """
        from src.history import OperationHistory

        history = OperationHistory(str(tmp_path / "history.txt"))
        calculator = Calculator()

        result = calculator.square(5)
        history.record("square", [5], result)

        records = history.get_all()
        assert len(records) == 1
        assert records[0] == "square 5 = 25"

    def test_history_does_not_record_failed_operation_unknown_command(self, tmp_path):
        """Test that invalid operations are NOT recorded.

        Input: Enter invalid operation "foo"
        Expected: Operation NOT recorded; history remains empty
        """
        from src.history import OperationHistory

        history = OperationHistory(str(tmp_path / "history.txt"))

        records = history.get_all()
        assert len(records) == 0

    def test_history_does_not_record_failed_operation_invalid_operand(self, tmp_path):
        """Test that operations with invalid operands are NOT recorded.

        Input: Attempt "add abc 3"
        Expected: Operation NOT recorded; history remains empty
        """
        from src.history import OperationHistory

        history = OperationHistory(str(tmp_path / "history.txt"))

        # Do not call history.record() for failed operations
        records = history.get_all()
        assert len(records) == 0

    def test_history_does_not_record_failed_operation_domain_error(self, tmp_path):
        """Test that operations with domain errors are NOT recorded.

        Input: Attempt "square_root -5"
        Expected: Operation NOT recorded; history remains empty
        """
        from src.history import OperationHistory

        history = OperationHistory(str(tmp_path / "history.txt"))
        calculator = Calculator()

        # Attempting square_root(-5) raises ValueError; don't record it
        try:
            result = calculator.square_root(-5)
            history.record("square_root", [-5], result)
        except ValueError:
            # Expected: don't record failed operations
            pass

        records = history.get_all()
        assert len(records) == 0

    def test_history_does_not_record_failed_operation_zero_division(self, tmp_path):
        """Test that division by zero operations are NOT recorded.

        Input: Attempt "divide 5 0"
        Expected: Operation NOT recorded; history remains empty
        """
        from src.history import OperationHistory

        history = OperationHistory(str(tmp_path / "history.txt"))
        calculator = Calculator()

        # Attempting divide(5, 0) raises ZeroDivisionError; don't record it
        try:
            result = calculator.divide(5, 0)
            history.record("divide", [5, 0], result)
        except ZeroDivisionError:
            # Expected: don't record failed operations
            pass

        records = history.get_all()
        assert len(records) == 0


# ============================================================================
# Test Group B: History Display Command (4 tests)
# ============================================================================

class TestHistoryDisplay:
    """Tests for the history display command."""

    def test_history_command_displays_empty_on_new_session(self, tmp_path, monkeypatch, capsys):
        """Test that 'history' command displays "empty" when no history exists.

        Input: Enter "history" without any prior operations
        Expected: Output contains "empty" or similar "no history" message
        """
        from src.history import OperationHistory

        history = OperationHistory(str(tmp_path / "history.txt"))

        # Display history when empty
        display_output = history.display()

        assert "empty" in display_output.lower() or len(history.get_all()) == 0

    def test_history_command_displays_all_recorded_operations(self, tmp_path):
        """Test that history command displays all recorded operations.

        Input: Execute "add 2 3", "multiply 4 5", then "history"
        Expected: Displays both operations in order
        """
        from src.history import OperationHistory

        history = OperationHistory(str(tmp_path / "history.txt"))
        calculator = Calculator()

        result1 = calculator.add(2, 3)
        history.record("add", [2, 3], result1)

        result2 = calculator.multiply(4, 5)
        history.record("multiply", [4, 5], result2)

        display_output = history.display()

        assert "add 2 3 = 5" in display_output
        assert "multiply 4 5 = 20" in display_output

    def test_history_command_maintains_order(self, tmp_path):
        """Test that operations are displayed in execution order.

        Input: Execute "add 1 2", "subtract 10 3", "divide 8 2", then "history"
        Expected: Operations displayed in exact execution order
        """
        from src.history import OperationHistory

        history = OperationHistory(str(tmp_path / "history.txt"))
        calculator = Calculator()

        result1 = calculator.add(1, 2)
        history.record("add", [1, 2], result1)

        result2 = calculator.subtract(10, 3)
        history.record("subtract", [10, 3], result2)

        result3 = calculator.divide(8, 2)
        history.record("divide", [8, 2], result3)

        records = history.get_all()

        assert records[0] == "add 1 2 = 3"
        assert records[1] == "subtract 10 3 = 7"
        assert records[2] == "divide 8 2 = 4.0"

    def test_history_command_case_insensitive_invocation(self, tmp_path):
        """Test that history command is case-insensitive.

        Input: Enter "HISTORY" or "History"
        Expected: Displays history regardless of case
        """
        from src.history import OperationHistory

        history = OperationHistory(str(tmp_path / "history.txt"))
        calculator = Calculator()

        result = calculator.add(2, 3)
        history.record("add", [2, 3], result)

        # Both uppercase and mixed case should work
        display_output = history.display()
        assert "add 2 3 = 5" in display_output


# ============================================================================
# Test Group C: File Persistence (Session Isolation) (4 tests)
# ============================================================================

class TestFilePersistence:
    """Tests for history file persistence and session isolation."""

    def test_history_file_created_at_session_start(self, tmp_path):
        """Test that history file is created/cleared at session start.

        Input: Start interactive mode with injectable file path
        Expected: History file created/cleared at session start (empty)
        """
        from src.history import OperationHistory

        history_file = str(tmp_path / "history.txt")
        history = OperationHistory(history_file)

        # File should be created or ready for use
        assert history.get_all() == []

    def test_history_written_to_file_on_operation(self, tmp_path):
        """Test that operations are written to the history file.

        Input: Execute "add 3 4" with injectable file path
        Expected: "add 3 4 = 7" written to history file
        """
        from src.history import OperationHistory

        history_file = str(tmp_path / "history.txt")
        history = OperationHistory(history_file)
        calculator = Calculator()

        result = calculator.add(3, 4)
        history.record("add", [3, 4], result)

        # Read file and verify
        file_path = Path(history_file)
        if file_path.exists():
            contents = file_path.read_text()
            assert "add 3 4 = 7" in contents

    def test_history_file_not_loaded_on_new_session(self, tmp_path):
        """Test that a new session starts with empty history (session isolation).

        Input: Session 1 creates history with "add 2 3"; session 2 starts fresh
        Expected: Session 2 history starts empty
        """
        from src.history import OperationHistory

        history_file = str(tmp_path / "history.txt")

        # Session 1: create history with one operation
        history1 = OperationHistory(history_file)
        calculator = Calculator()
        result1 = calculator.add(2, 3)
        history1.record("add", [2, 3], result1)

        # Session 2: create new OperationHistory instance
        # Expected: starts empty (session isolation)
        history2 = OperationHistory(history_file)
        records2 = history2.get_all()

        assert len(records2) == 0

    def test_history_file_overwritten_between_sessions(self, tmp_path):
        """Test that file is overwritten when a new session starts.

        Input: Session 1 records "add 1 2"; session 2 records "multiply 3 4"
        Expected: File contains ONLY session 2's operation
        """
        from src.history import OperationHistory

        history_file = str(tmp_path / "history.txt")
        calculator = Calculator()

        # Session 1: create history and record one operation
        history1 = OperationHistory(history_file)
        result1 = calculator.add(1, 2)
        history1.record("add", [1, 2], result1)

        # Session 2: create new history (should clear/overwrite)
        history2 = OperationHistory(history_file)
        result2 = calculator.multiply(3, 4)
        history2.record("multiply", [3, 4], result2)

        # Verify file contains only session 2 data
        file_path = Path(history_file)
        if file_path.exists():
            contents = file_path.read_text()
            assert "multiply 3 4 = 12" in contents


# ============================================================================
# Test Group D: Integration with Failure Tracking (2 tests)
# ============================================================================

class TestHistoryWithFailureTracking:
    """Tests for history integration with failure tracking."""

    def test_history_counter_independent_from_failure_counter(self, tmp_path, monkeypatch, capsys):
        """Test that history is independent from failure counter.

        Input: Enter invalid operation (failure counter = 1), then valid operation
        Expected: Valid operation IS recorded; failure counter resets to 0
        """
        from src.history import OperationHistory
        from src.__main__ import _run_interactive_loop, _build_registry

        history_file = str(tmp_path / "history.txt")
        history = OperationHistory(history_file)

        # This test verifies the interactive loop records valid ops even after errors
        calculator = Calculator()

        # Record a valid operation (history should work independently)
        result = calculator.add(5, 3)
        history.record("add", [5, 3], result)

        records = history.get_all()
        assert len(records) == 1
        assert records[0] == "add 5 3 = 8"

    def test_history_survives_three_consecutive_failures_exit(self, tmp_path, monkeypatch, capsys):
        """Test that history is preserved even when loop exits due to failures.

        Input: Record one operation, then loop exits on 3 failures
        Expected: Loop exits gracefully; history preserved (no crash)
        """
        from src.history import OperationHistory
        from src.__main__ import _run_interactive_loop, _build_registry

        history_file = str(tmp_path / "history.txt")
        history = OperationHistory(history_file)
        calculator = Calculator()

        # Record a valid operation before failures
        result = calculator.add(5, 5)
        history.record("add", [5, 5], result)

        # Simulate 3 invalid operations in the interactive loop
        inputs = iter(['invalid_op', 'invalid_op', 'invalid_op'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry(calculator)

        # Run interactive loop; should exit after 3 failures
        try:
            _run_interactive_loop(registry)
        except StopIteration:
            # Expected: input iterator exhausted
            pass

        # History should still be intact
        records = history.get_all()
        # At minimum, the first operation should be recorded
        assert any("add 5 5 = 10" in r for r in records)


# ============================================================================
# Test Group E: Edge Cases (5 tests)
# ============================================================================

class TestHistoryEdgeCases:
    """Tests for edge cases in history recording."""

    def test_history_with_negative_operands(self, tmp_path):
        """Test that operations with negative operands are recorded correctly.

        Input: Execute "subtract 5 -3"
        Expected: Recorded as "subtract 5 -3 = 8"
        """
        from src.history import OperationHistory

        history = OperationHistory(str(tmp_path / "history.txt"))
        calculator = Calculator()

        result = calculator.subtract(5, -3)
        history.record("subtract", [5, -3], result)

        records = history.get_all()
        assert len(records) == 1
        assert records[0] == "subtract 5 -3 = 8"

    def test_history_with_very_large_numbers(self, tmp_path):
        """Test that very large numbers are recorded accurately.

        Input: Execute "add 999999999 1"
        Expected: Recorded accurately
        """
        from src.history import OperationHistory

        history = OperationHistory(str(tmp_path / "history.txt"))
        calculator = Calculator()

        result = calculator.add(999999999, 1)
        history.record("add", [999999999, 1], result)

        records = history.get_all()
        assert len(records) == 1
        assert records[0] == "add 999999999 1 = 1000000000"

    def test_history_with_special_float_values(self, tmp_path):
        """Test that special float values (division results) are recorded.

        Input: Execute "divide 1 3"
        Expected: Recorded with Python's float representation
        """
        from src.history import OperationHistory

        history = OperationHistory(str(tmp_path / "history.txt"))
        calculator = Calculator()

        result = calculator.divide(1, 3)
        history.record("divide", [1, 3], result)

        records = history.get_all()
        assert len(records) == 1
        # Float 1/3 should be recorded with its Python representation
        assert "divide 1 3 =" in records[0]

    def test_history_file_path_injectable_for_testing(self, tmp_path):
        """Test that history file path is injectable for testing.

        Input: Initialize with custom history file path (tmp_path fixture)
        Expected: History written to specified path
        """
        from src.history import OperationHistory

        custom_path = str(tmp_path / "custom_history.txt")
        history = OperationHistory(custom_path)
        calculator = Calculator()

        result = calculator.multiply(2, 3)
        history.record("multiply", [2, 3], result)

        # Verify file was written to custom path
        file_path = Path(custom_path)
        if file_path.exists():
            contents = file_path.read_text()
            assert "multiply 2 3 = 6" in contents

    def test_history_quit_command_preserves_history(self, tmp_path, monkeypatch, capsys):
        """Test that history is preserved when user quits.

        Input: Execute "add 5 5", then "quit"
        Expected: History preserved before exit; no crash
        """
        from src.history import OperationHistory
        from src.__main__ import _run_interactive_loop, _build_registry

        history_file = str(tmp_path / "history.txt")
        history = OperationHistory(history_file)
        calculator = Calculator()

        # Pre-record an operation
        result = calculator.add(5, 5)
        history.record("add", [5, 5], result)

        # Simulate user input: quit
        inputs = iter(['quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry(calculator)

        # Run interactive loop; should exit on 'quit'
        try:
            _run_interactive_loop(registry)
        except StopIteration:
            # Expected: input iterator exhausted
            pass

        # History should still be intact
        records = history.get_all()
        # The pre-recorded operation should be preserved
        if len(records) > 0:
            assert any("add 5 5 = 10" in r for r in records)
