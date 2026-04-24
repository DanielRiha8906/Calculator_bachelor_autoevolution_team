"""Tests for interactive input validation and consecutive failure tracking.

Tests the interactive calculator loop's input validation behavior, including
consecutive failure tracking that exits after 3 invalid attempts, and backward
compatibility with the existing interactive behavior.
"""

import sys
import pytest
from unittest.mock import patch
from src.__main__ import _run_interactive_loop, cli_mode, _build_registry
from src.calculator import Calculator


# ============================================================================
# Group A: Consecutive-Failure Tracking (6 tests)
# ============================================================================

class TestConsecutiveFailureTracking:
    """Tests for tracking and exiting on consecutive failures."""

    def test_interactive_consecutive_failures_three_invalid_ops(self, monkeypatch, capsys):
        """Test that three consecutive invalid operations cause exit with message.

        Inputs: stdin = ['invalid_op', 'invalid_op', 'invalid_op']
        Expected: Three error messages "Unknown operation", loop exits, output
        contains "Too many invalid attempts. Exiting.", no SystemExit
        """
        inputs = iter(['invalid_op', 'invalid_op', 'invalid_op'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        calculator = Calculator()
        registry = _build_registry(calculator)

        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Check for 3 error messages about unknown operation
        assert captured.out.count("Unknown operation") >= 3
        # Check for exit message
        assert "Too many invalid attempts" in captured.out

    def test_interactive_consecutive_failures_mixed_invalid_op_and_operand(self, monkeypatch, capsys):
        """Test mixed invalid operand and operation errors trigger exit.

        Inputs: stdin = ['add', 'abc', 'invalid_op', 'invalid_op', 'invalid_op']
        Expected: Error for 'abc' invalid number (counter=1), then 3 unknown-op
        errors (counter increments), loop exits with "Too many invalid attempts. Exiting."
        """
        inputs = iter(['add', 'abc', 'invalid_op', 'invalid_op', 'invalid_op'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        calculator = Calculator()
        registry = _build_registry(calculator)

        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Check for invalid number error
        assert "Invalid number" in captured.out
        # Check for unknown operation errors
        assert "Unknown operation" in captured.out
        # Check for exit message
        assert "Too many invalid attempts" in captured.out

    def test_interactive_consecutive_failures_domain_error_counts(self, monkeypatch, capsys):
        """Test that domain errors (e.g., sqrt(-1)) count as failures.

        Inputs: stdin = ['square_root', '-1', 'square_root', '-1', 'square_root', '-1']
        Expected: Three domain errors, loop exits with "Too many invalid attempts. Exiting."
        """
        inputs = iter(['square_root', '-1', 'square_root', '-1', 'square_root', '-1'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        calculator = Calculator()
        registry = _build_registry(calculator)

        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Check for domain errors (sqrt of negative number)
        assert "Error:" in captured.out
        # Check for exit message
        assert "Too many invalid attempts" in captured.out

    def test_interactive_counter_resets_on_success(self, monkeypatch, capsys):
        """Test that counter resets to 0 after a successful operation.

        Inputs: stdin = ['invalid_op', 'add', '5', '3', 'invalid_op', 'invalid_op', 'invalid_op']
        Expected: Error 1 (counter=1), Success "Result: 8" (counter→0), Error 2
        (counter=1), Error 3 (counter=2), Error 4 (counter=3), exit "Too many invalid attempts. Exiting."
        """
        inputs = iter(['invalid_op', 'add', '5', '3', 'invalid_op', 'invalid_op', 'invalid_op'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        calculator = Calculator()
        registry = _build_registry(calculator)

        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Check for error, then success result
        assert "Unknown operation" in captured.out
        assert "Result: 8" in captured.out
        # Check for more errors
        assert captured.out.count("Unknown operation") >= 3
        # Check for exit message
        assert "Too many invalid attempts" in captured.out

    def test_interactive_success_clears_previous_failures(self, monkeypatch, capsys):
        """Test that a successful operation clears the failure counter.

        Inputs: stdin = ['invalid_op', 'invalid_op', 'square', '4', 'invalid_op', 'invalid_op', 'invalid_op']
        Expected: Two errors (counter=2), success "Result: 16" (counter→0),
        three more errors, exit "Too many invalid attempts. Exiting."
        """
        inputs = iter(['invalid_op', 'invalid_op', 'square', '4', 'invalid_op', 'invalid_op', 'invalid_op'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        calculator = Calculator()
        registry = _build_registry(calculator)

        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Check for errors, then success
        assert "Unknown operation" in captured.out
        assert "Result: 16" in captured.out
        # Check for more errors after success
        assert captured.out.count("Unknown operation") >= 3
        # Check for exit message
        assert "Too many invalid attempts" in captured.out

    def test_interactive_exactly_three_failures_before_exit(self, monkeypatch, capsys):
        """Test that exactly three failures cause exit, not more.

        Inputs: stdin = ['bad', 'bad', 'bad']
        Expected: Exactly three error messages, exit message, no fourth error message
        """
        inputs = iter(['bad', 'bad', 'bad'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        calculator = Calculator()
        registry = _build_registry(calculator)

        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Count unknown operation errors
        error_count = captured.out.count("Unknown operation")
        assert error_count == 3
        # Check for exit message
        assert "Too many invalid attempts" in captured.out


# ============================================================================
# Group B: Backward Compatibility (5 tests)
# ============================================================================

class TestBackwardCompatibility:
    """Tests ensuring backward compatibility with existing behavior."""

    def test_interactive_single_invalid_operation_then_quit(self, monkeypatch, capsys):
        """Test that a single invalid operation does not trigger exit.

        Inputs: stdin = ['invalid_op', 'quit']
        Expected: One error message, loop continues to quit, no "Too many invalid attempts" message
        """
        inputs = iter(['invalid_op', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        calculator = Calculator()
        registry = _build_registry(calculator)

        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Check for error
        assert "Unknown operation" in captured.out
        # Check that NO "Too many invalid attempts" message
        assert "Too many invalid attempts" not in captured.out

    def test_interactive_invalid_operand_reprompts(self, monkeypatch, capsys):
        """Test that invalid operand prompts user to re-enter operation.

        Inputs: stdin = ['add', 'not_a_number', '5', '3', 'quit']
        Expected: Error for invalid number, loop continues from top, then 'add' again
        with '5', '3' → Result: 8, 'quit' ends loop. No "Too many invalid attempts."
        """
        inputs = iter(['add', 'not_a_number', 'add', '5', '3', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        calculator = Calculator()
        registry = _build_registry(calculator)

        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Check for invalid number error
        assert "Invalid number" in captured.out
        # Check for successful result
        assert "Result: 8" in captured.out
        # Check NO exit message
        assert "Too many invalid attempts" not in captured.out

    def test_interactive_successful_operation_output(self, monkeypatch, capsys):
        """Test that successful operations print correctly formatted output.

        Inputs: stdin = ['multiply', '6', '7', 'quit']
        Expected: "Result: 42", loop continues, quit ends it
        """
        inputs = iter(['multiply', '6', '7', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        calculator = Calculator()
        registry = _build_registry(calculator)

        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        assert "Result: 42" in captured.out

    def test_interactive_domain_error_does_not_crash(self, monkeypatch, capsys):
        """Test that domain errors are handled gracefully and loop continues.

        Inputs: stdin = ['ln', '0', 'add', '2', '3', 'quit']
        Expected: Domain error for ln(0) (counter=1), then success "Result: 5"
        (counter→0), quit. No crash.
        """
        inputs = iter(['ln', '0', 'add', '2', '3', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        calculator = Calculator()
        registry = _build_registry(calculator)

        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Check for error handling
        assert "Error:" in captured.out
        # Check for successful result after error
        assert "Result: 5" in captured.out

    def test_interactive_quit_command_ends_loop_normally(self, monkeypatch, capsys):
        """Test that quit command ends loop without exit message.

        Inputs: stdin = ['invalid', 'invalid', 'quit']
        Expected: Two errors (counter=2), quit ends loop, no "Too many invalid attempts" message
        """
        inputs = iter(['invalid', 'invalid', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        calculator = Calculator()
        registry = _build_registry(calculator)

        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Check for errors
        assert "Unknown operation" in captured.out
        # Check error count is exactly 2
        assert captured.out.count("Unknown operation") == 2
        # Check NO exit message
        assert "Too many invalid attempts" not in captured.out


# ============================================================================
# Group C: CLI Mode Regression Tests (2 tests)
# ============================================================================

class TestCLIModeRegression:
    """Tests ensuring CLI mode still rejects invalid input."""

    def test_cli_mode_still_rejects_invalid_operand(self, monkeypatch, capsys):
        """Test that CLI mode rejects invalid operand and exits with code 1.

        Inputs: sys.argv = ['calculator', 'add', '5', 'abc']
        Expected: SystemExit with code 1, error message to stderr
        """
        monkeypatch.setattr(sys, 'argv', ['calculator', 'add', '5', 'abc'])

        with pytest.raises(SystemExit) as exc_info:
            cli_mode()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err or "Error:" in captured.out

    def test_cli_mode_still_rejects_domain_error(self, monkeypatch, capsys):
        """Test that CLI mode rejects domain errors and exits with code 1.

        Inputs: sys.argv = ['calculator', 'square_root', '-1']
        Expected: SystemExit with code 1, error message to stderr
        """
        monkeypatch.setattr(sys, 'argv', ['calculator', 'square_root', '-1'])

        with pytest.raises(SystemExit) as exc_info:
            cli_mode()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err or "Error:" in captured.out


# ============================================================================
# Group D: Edge Cases (1 test)
# ============================================================================

class TestEdgeCases:
    """Tests for edge case scenarios."""

    def test_interactive_consecutive_failures_first_failure(self, monkeypatch, capsys):
        """Test that first failure does not trigger exit.

        Inputs: stdin = ['invalid_op', 'quit']
        Expected: One error (counter=1), loop continues, quit ends it,
        no "Too many invalid attempts"
        """
        inputs = iter(['invalid_op', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        calculator = Calculator()
        registry = _build_registry(calculator)

        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Check for one error
        assert "Unknown operation" in captured.out
        # Check NO exit message
        assert "Too many invalid attempts" not in captured.out
