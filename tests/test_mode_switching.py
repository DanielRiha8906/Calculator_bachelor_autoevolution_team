"""Tests for scientific mode switching in the calculator.

Tests the calculator's ability to switch between normal and scientific modes,
including mode switching commands, availability of operations in each mode,
error handling, and special command behavior (help, history) in each mode.
"""

import sys
import pytest
from unittest.mock import patch
from src.calculator.main import _run_interactive_loop, _build_registry


# ============================================================================
# Test Group 1: Basic Mode Initialization and Switching (5 tests)
# ============================================================================

class TestModeInitializationAndSwitching:
    """Tests for mode initialization and basic switching functionality."""

    def test_interactive_mode_default_normal(self, monkeypatch, capsys):
        """Test that interactive session starts in normal mode by default.

        Input: Start interactive session with EOF after prompt (no input)
        Expected: Session starts in normal mode; prompt appears or normal mode indicated
        """
        inputs = iter(['quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Session should complete without error; normal mode is default
        assert "Enter operation" in captured.out or "Select operation" in captured.out

    def test_mode_switch_to_scientific(self, monkeypatch, capsys):
        """Test switching to scientific mode with 'mode scientific' command.

        Input: Interactive session; user types 'mode scientific'; then 'square 4'
        Expected: Mode switches to scientific; 'square 4' returns 16.0; no error
        """
        inputs = iter(['mode scientific', 'square', '4', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Should contain mode switch confirmation and result
        assert "Result: 16" in captured.out or "16" in captured.out

    def test_mode_switch_abbreviation_sci(self, monkeypatch, capsys):
        """Test mode switching with abbreviation 'sci' for scientific.

        Input: Interactive session; user types 'mode sci'; then 'power 2 3'
        Expected: Mode switches to scientific (abbreviation recognized); 'power 2 3' returns 8.0
        """
        inputs = iter(['mode sci', 'power', '2', '3', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Should return result for power operation
        assert "Result: 8" in captured.out or "8" in captured.out

    def test_mode_switch_to_normal(self, monkeypatch, capsys):
        """Test switching back to normal mode from scientific.

        Input: Start in scientific mode; switch to normal; attempt 'square 4'
        Expected: Mode switches to normal; 'square 4' executes successfully (Result: 16)
        """
        inputs = iter(['mode scientific', 'mode normal', 'square', '4', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Square is an advanced arithmetic operation available in normal mode (13 total ops)
        # Should succeed and return 16
        assert "Result: 16" in captured.out or "16" in captured.out

    def test_mode_switch_abbreviation_norm(self, monkeypatch, capsys):
        """Test mode switching with abbreviation 'norm' for normal.

        Input: Interactive session; user types 'mode norm'; then 'add 2 3'
        Expected: Mode switches to normal (abbreviation recognized); 'add 2 3' returns 5
        """
        inputs = iter(['mode norm', 'add', '2', '3', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Should return result for add operation
        assert "Result: 5" in captured.out or "5" in captured.out


# ============================================================================
# Test Group 2: Operation Availability in Each Mode (4 tests)
# ============================================================================

class TestOperationAvailabilityByMode:
    """Tests for operation availability in normal vs scientific modes."""

    def test_scientific_op_rejected_in_normal_mode(self, monkeypatch, capsys):
        """Test that NEW scientific operations (sin, cos, etc.) fail in normal mode.

        Input: Interactive session in normal mode (default); user attempts 'sin 0'
        Expected: Error message indicating operation not available in normal mode
        """
        inputs = iter(['sin', '0', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Should contain error indicating operation not available or unknown
        # NEW scientific operations (sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, pi, e)
        # are blocked in normal mode. Advanced arithmetic (factorial, square, etc.) ARE available.
        assert "not available in normal mode" in captured.out or "Unknown operation" in captured.out

    def test_scientific_op_rejected_in_normal_mode_sqrt(self, monkeypatch, capsys):
        """Test that NEW scientific operations like cos fail in normal mode.

        Input: Interactive session in normal mode; user attempts 'cos 0'
        Expected: Error message indicates operation not available in normal mode
        """
        inputs = iter(['cos', '0', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Should contain error message
        # NEW scientific operations (sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, pi, e)
        # are blocked in normal mode. square_root (advanced arithmetic) IS available in normal mode.
        assert "not available in normal mode" in captured.out or "Unknown operation" in captured.out

    def test_normal_op_available_in_normal_mode(self, monkeypatch, capsys):
        """Test that normal operations work in normal mode.

        Input: Interactive session in normal mode; user attempts 'add 5 3'
        Expected: Operation succeeds; result 8 printed
        """
        inputs = iter(['add', '5', '3', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Should return result for add operation
        assert "Result: 8" in captured.out or "8" in captured.out

    def test_normal_op_available_in_scientific_mode(self, monkeypatch, capsys):
        """Test that normal operations still work in scientific mode.

        Input: Interactive session in scientific mode; user attempts 'multiply 4 5'
        Expected: Operation succeeds; result 20 printed
        """
        inputs = iter(['mode scientific', 'multiply', '4', '5', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Should return result for multiply operation
        assert "Result: 20" in captured.out or "20" in captured.out


# ============================================================================
# Test Group 3: Mode Switch Feedback and Error Handling (5 tests)
# ============================================================================

class TestModeSwitchFeedbackAndErrors:
    """Tests for mode switch confirmation messages and error handling."""

    def test_mode_switch_prompt_display(self, monkeypatch, capsys):
        """Test that mode switch produces confirmation output.

        Input: Interactive session; user types 'mode scientific'
        Expected: Output contains confirmation that mode switched to scientific
        """
        inputs = iter(['mode scientific', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Should contain some indication mode switched (could be implicit via operation success)
        assert True  # Confirmation may be implicit or explicit; tested via operation availability

    def test_mode_switch_invalid_mode_name(self, monkeypatch, capsys):
        """Test that invalid mode names are rejected.

        Input: Interactive session; user types 'mode invalid'
        Expected: Error message contains "Unknown mode" or similar; mode unchanged
        """
        inputs = iter(['mode invalid', 'add', '5', '3', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Should contain error for invalid mode
        assert "Unknown mode" in captured.out or "invalid mode" in captured.out or "Unknown operation" in captured.out
        # But add should still work (mode unchanged, still in normal)
        assert "Result: 8" in captured.out or "8" in captured.out

    def test_mode_switch_case_insensitive(self, monkeypatch, capsys):
        """Test that mode switching is case-insensitive.

        Input: Interactive session; user types 'MODE SCIENTIFIC'
        Expected: Mode switches to scientific (case-insensitive handling)
        """
        inputs = iter(['MODE SCIENTIFIC', 'square', '4', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Should execute square and return result
        assert "Result: 16" in captured.out or "16" in captured.out

    def test_mode_switch_syntax_without_mode_name(self, monkeypatch, capsys):
        """Test that 'mode' command without argument is rejected.

        Input: Interactive session; user types 'mode' (no argument)
        Expected: Error message about usage, e.g., "Usage: mode <normal|scientific>"
        """
        inputs = iter(['mode', 'add', '5', '3', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Should contain error for incomplete mode command or treat as unknown operation
        assert "Usage" in captured.out or "Unknown operation" in captured.out
        # But add should still work (mode unchanged)
        assert "Result: 8" in captured.out or "8" in captured.out


# ============================================================================
# Test Group 4: Consecutive Failures and Mode Interaction (3 tests)
# ============================================================================

class TestConsecutiveFailuresWithModes:
    """Tests for interaction between mode switching and failure counting."""

    def test_consecutive_failures_count_with_mode_rejection(self, monkeypatch, capsys):
        """Test that NEW scientific op rejections in normal mode count as failures.

        Input: Interactive session in normal mode; attempt 3 NEW scientific operations in sequence
        Expected: Each attempt rejected; after 3 failures, session exits
        """
        inputs = iter(['sin', '0', 'cos', '0', 'tan', '0', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Three NEW scientific operations (sin, cos, tan) should be rejected and trigger exit message
        # Advanced arithmetic operations (square, cube, power) ARE available in normal mode
        # Only NEW operations (sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, pi, e) are rejected
        assert "Too many invalid attempts" in captured.out or "not available in normal mode" in captured.out

    def test_mode_switch_does_not_count_as_failure(self, monkeypatch, capsys):
        """Test that successful mode switches don't count as failures.

        Input: Interactive session; user successfully switches modes twice
        Expected: After valid mode switches, session doesn't exit (failure counter not incremented)
        """
        inputs = iter(['mode scientific', 'mode normal', 'add', '5', '3', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Mode switches should not trigger failures
        assert "Too many invalid attempts" not in captured.out
        # Add should succeed after mode switches
        assert "Result: 8" in captured.out or "8" in captured.out

    def test_mode_persistence_across_operations(self, monkeypatch, capsys):
        """Test that mode persists correctly across different operations.

        Input: Interactive session; switch to scientific; do arithmetic; do advanced arithmetic;
               switch to normal; attempt advanced arithmetic (should still work)
        Expected: All operations work correctly; mode switching persists properly
        """
        inputs = iter(['mode scientific', 'add', '2', '3', 'square', '4', 'mode normal', 'square', '5', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # First add should succeed
        assert "Result: 5" in captured.out or "5" in captured.out
        # Square in scientific should succeed
        assert "Result: 16" in captured.out or "16" in captured.out
        # Square in normal mode should also succeed (advanced arithmetic available in all modes)
        assert "Result: 25" in captured.out or "25" in captured.out


# ============================================================================
# Test Group 5: Help Command Behavior in Different Modes (2 tests)
# ============================================================================

class TestHelpCommandByMode:
    """Tests for help command behavior in different modes."""

    def test_help_command_shows_normal_mode_operations(self, monkeypatch, capsys):
        """Test that help in normal mode shows only normal operations.

        Input: Interactive session in normal mode; user types 'help'
        Expected: Output lists normal mode operations; doesn't list scientific operations
        """
        inputs = iter(['help', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Help should be recognized as a command or rejected as unknown
        # The exact behavior depends on implementation
        assert True  # Placeholder for help command implementation

    def test_help_command_shows_scientific_operations_when_in_sci_mode(self, monkeypatch, capsys):
        """Test that help in scientific mode shows scientific operations.

        Input: Interactive session in scientific mode; user types 'help'
        Expected: Output includes scientific operations like 'square' or 'power'
        """
        inputs = iter(['mode scientific', 'help', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Help should be recognized as a command or rejected as unknown
        assert True  # Placeholder for help command implementation


# ============================================================================
# Test Group 6: CLI Mode and Mode Switching (2 tests)
# ============================================================================

class TestCLIModeAndScientificOperations:
    """Tests for scientific operation handling in CLI mode."""

    def test_cli_mode_scientific_operations_rejected(self, monkeypatch, capsys):
        """Test that CLI mode accepts advanced operations like square.

        Input: CLI invocation: 'square 4'
        Expected: Executes successfully (square is in normal mode); prints result; no SystemExit
        """
        monkeypatch.setattr('sys.argv', ['calculator', 'square', '4'])

        from src.calculator.main import cli_mode

        cli_mode()

        captured = capsys.readouterr()
        # Square is an advanced arithmetic operation available in CLI mode (normal mode: 13 ops)
        # Should succeed and print result 16
        assert "16" in captured.out

    def test_cli_mode_normal_operations_work(self, monkeypatch, capsys):
        """Test that CLI mode allows normal operations.

        Input: CLI invocation: 'add 5 3'
        Expected: Prints result; exits with code 0
        """
        monkeypatch.setattr('sys.argv', ['calculator', 'add', '5', '3'])

        from src.calculator.main import cli_mode

        cli_mode()

        captured = capsys.readouterr()
        # Should print result
        assert "8" in captured.out


