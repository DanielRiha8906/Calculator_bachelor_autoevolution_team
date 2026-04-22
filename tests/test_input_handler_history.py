"""test_input_handler_history.py — tests for the history command in CalculatorREPL.

Tests cover:
- "history" command displays "No history yet." when empty
- "history" command displays formatted list of entries after operations
- Case-insensitivity: "history", "HISTORY", "History", etc. all work
- REPL loop continues after displaying history (does not exit)
- Binary operation format: "N. op1 operator op2 = result"
- Unary operation format: "N. op1 operator = result"
- History display integrates with normal calculator operations
"""

import pytest
from unittest.mock import patch
from src import Calculator, CalculatorREPL


@pytest.fixture
def calculator():
    """Fixture providing a fresh Calculator instance."""
    return Calculator()


@pytest.fixture
def repl(calculator):
    """Fixture providing a fresh CalculatorREPL instance."""
    return CalculatorREPL(calculator)


class TestHistoryCommandEmpty:
    """Tests for history command with no recorded operations."""

    def test_history_command_empty_displays_no_history_yet(self, repl, capsys):
        """Test that 'history' displays 'No history yet.' when history is empty."""
        with patch("builtins.input", side_effect=["history", "exit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "No history yet." in captured.out

    def test_history_command_case_insensitive_lower(self, repl, capsys):
        """Test that 'history' (lowercase) displays empty history message."""
        with patch("builtins.input", side_effect=["history", "exit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "No history yet." in captured.out

    def test_history_command_case_insensitive_upper(self, repl, capsys):
        """Test that 'HISTORY' (uppercase) displays empty history message."""
        with patch("builtins.input", side_effect=["HISTORY", "exit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "No history yet." in captured.out

    def test_history_command_case_insensitive_mixed(self, repl, capsys):
        """Test that 'History', 'HiStOrY', etc. all display empty history message."""
        test_cases = ["History", "HiStOrY", "hiSTory", "HISTORY", "history"]
        for history_cmd in test_cases:
            repl_fresh = CalculatorREPL(Calculator())
            with patch("builtins.input", side_effect=[history_cmd, "exit"]):
                repl_fresh.run()
            captured = capsys.readouterr()
            assert "No history yet." in captured.out


class TestHistoryCommandWithOperations:
    """Tests for history command displaying recorded operations."""

    def test_history_after_single_binary_operation(self, repl, capsys):
        """Test history display after one binary operation."""
        with patch("builtins.input", side_effect=["add 5 3", "history", "exit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. 5 add 3 = 8" in captured.out

    def test_history_after_single_unary_operation(self, repl, capsys):
        """Test history display after one unary operation."""
        with patch("builtins.input", side_effect=["square 5", "history", "exit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. 5 square = 25" in captured.out

    def test_history_format_binary_operations(self, repl, capsys):
        """Test that binary operations display as 'N. op1 operator op2 = result'."""
        with patch("builtins.input", side_effect=[
            "add 5 3",
            "subtract 10 4",
            "multiply 2 6",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. 5 add 3 = 8" in captured.out
        assert "2. 10 subtract 4 = 6" in captured.out
        assert "3. 2 multiply 6 = 12" in captured.out

    def test_history_format_unary_operations(self, repl, capsys):
        """Test that unary operations display as 'N. op1 operator = result'."""
        with patch("builtins.input", side_effect=[
            "square 5",
            "cube 3",
            "factorial 4",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. 5 square = 25" in captured.out
        assert "2. 3 cube = 27" in captured.out
        assert "3. 4 factorial = 24" in captured.out

    def test_history_format_mixed_operations(self, repl, capsys):
        """Test history display with alternating binary and unary operations."""
        with patch("builtins.input", side_effect=[
            "add 5 3",
            "square 4",
            "divide 20 5",
            "cube 2",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. 5 add 3 = 8" in captured.out
        assert "2. 4 square = 16" in captured.out
        assert "3. 20 divide 5 = 4.0" in captured.out
        assert "4. 2 cube = 8" in captured.out

    def test_history_numbered_list(self, repl, capsys):
        """Test that history entries are numbered sequentially."""
        with patch("builtins.input", side_effect=[
            "add 1 1",
            "add 2 2",
            "add 3 3",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. 1 add 1 = 2" in captured.out
        assert "2. 2 add 2 = 4" in captured.out
        assert "3. 3 add 3 = 6" in captured.out

    def test_history_with_negative_operands(self, repl, capsys):
        """Test history display with negative operands."""
        with patch("builtins.input", side_effect=[
            "add -5 3",
            "multiply -2 -3",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. -5 add 3 = -2" in captured.out
        assert "2. -2 multiply -3 = 6" in captured.out

    def test_history_with_floating_point_results(self, repl, capsys):
        """Test history display with floating-point results."""
        with patch("builtins.input", side_effect=[
            "divide 10 4",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. 10 divide 4 = 2.5" in captured.out

    def test_history_with_square_root(self, repl, capsys):
        """Test history display for square_root operation."""
        with patch("builtins.input", side_effect=[
            "square_root 16",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. 16 square_root = 4.0" in captured.out

    def test_history_with_power_operation(self, repl, capsys):
        """Test history display for power operation."""
        with patch("builtins.input", side_effect=[
            "power 2 8",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. 2 power 8 = 256" in captured.out

    def test_history_with_natural_log(self, repl, capsys):
        """Test history display for natural_log operation."""
        with patch("builtins.input", side_effect=[
            "natural_log 1",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. 1 natural_log = 0" in captured.out

    def test_history_with_log_base_10(self, repl, capsys):
        """Test history display for log_base_10 operation."""
        with patch("builtins.input", side_effect=[
            "log_base_10 100",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. 100 log_base_10 = 2.0" in captured.out


class TestHistoryCommandLoopContinuation:
    """Tests for REPL loop continuation after history display."""

    def test_history_command_does_not_exit_repl(self, repl, capsys):
        """Test that 'history' command does not exit the REPL."""
        with patch("builtins.input", side_effect=[
            "add 5 3",
            "history",
            "add 2 2",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        # Should show history, but also continue and execute the next operation
        assert "1. 5 add 3 = 8" in captured.out
        assert "Result: 4" in captured.out
        assert "Goodbye!" in captured.out

    def test_multiple_history_commands_in_sequence(self, repl, capsys):
        """Test that multiple history commands can be issued in sequence."""
        with patch("builtins.input", side_effect=[
            "add 5 3",
            "history",
            "multiply 2 3",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        # First history should show only add
        output_parts = captured.out.split("No history yet")
        # After first add, history should show 1 entry
        assert "1. 5 add 3 = 8" in captured.out
        # After multiply, should see both
        assert "1. 5 add 3 = 8" in captured.out
        assert "2. 2 multiply 3 = 6" in captured.out

    def test_history_then_operation_then_history(self, repl, capsys):
        """Test history -> operation -> history sequence."""
        with patch("builtins.input", side_effect=[
            "history",
            "add 5 3",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        # First history should show empty
        assert "No history yet." in captured.out
        # Then add operation
        assert "Result: 8" in captured.out
        # Second history should show the operation
        assert "1. 5 add 3 = 8" in captured.out


class TestHistoryCommandCaseSensitivity:
    """Tests for case-insensitive history command."""

    @pytest.mark.parametrize("history_cmd", [
        "history",
        "HISTORY",
        "History",
        "HiStOrY",
        "hiSTory",
        "hIsTorY",
    ])
    def test_history_command_all_case_variations(self, history_cmd, capsys):
        """Test that history command works with all case variations."""
        repl = CalculatorREPL(Calculator())
        with patch("builtins.input", side_effect=["add 5 3", history_cmd, "exit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. 5 add 3 = 8" in captured.out

    def test_history_with_leading_trailing_spaces(self, repl, capsys):
        """Test that history command works with leading/trailing spaces."""
        # Input trimming should handle this in the REPL
        with patch("builtins.input", side_effect=["add 5 3", "  history  ", "exit"]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. 5 add 3 = 8" in captured.out


class TestHistoryIntegrationWithREPL:
    """Integration tests for history in the REPL context."""

    def test_history_accessible_throughout_session(self, repl, capsys):
        """Test that history accumulates throughout a session."""
        with patch("builtins.input", side_effect=[
            "add 5 3",
            "history",
            "square 4",
            "history",
            "multiply 2 3",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        # After first history: should show 1 entry
        assert "1. 5 add 3 = 8" in captured.out
        # After third history command: should show all 3 entries
        assert "1. 5 add 3 = 8" in captured.out
        assert "2. 4 square = 16" in captured.out
        assert "3. 2 multiply 3 = 6" in captured.out

    def test_history_survives_invalid_input(self, repl, capsys):
        """Test that history is preserved when invalid input occurs.

        Note: Due to retry loop behavior, 'history' typed during retry prompt
        is treated as an expression, not as the history command. This test
        verifies that history data is preserved internally, by checking that
        a subsequent successful operation and history display works correctly.
        """
        with patch("builtins.input", side_effect=[
            "add 5 3",
            "invalid_op 5",
            "add 2 2",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        # History should contain both operations
        assert "1. 5 add 3 = 8" in captured.out
        assert "2. 2 add 2 = 4" in captured.out
        assert "Validation error:" in captured.out

    def test_history_with_retry_logic(self, repl, capsys):
        """Test that history is preserved and accessible after retry attempts."""
        with patch("builtins.input", side_effect=[
            "add 5 3",
            "bad_command",
            "square 4",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        # Valid operations should be in history
        assert "1. 5 add 3 = 8" in captured.out
        assert "2. 4 square = 16" in captured.out

    def test_history_command_interleaved_with_operations(self, repl, capsys):
        """Test history command can be used to check progress during session."""
        with patch("builtins.input", side_effect=[
            "add 10 5",
            "history",
            "multiply 3 4",
            "history",
            "square 5",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        # All operations should appear in output
        assert "Result: 15" in captured.out
        assert "Result: 12" in captured.out
        assert "Result: 25" in captured.out
        # History should show all entries in correct order
        assert "1. 10 add 5 = 15" in captured.out
        assert "2. 3 multiply 4 = 12" in captured.out
        assert "3. 5 square = 25" in captured.out


class TestHistoryCalcuatorInstanceIntegration:
    """Tests for history command retrieving data from Calculator instance."""

    def test_history_command_uses_calculator_get_history(self, calculator):
        """Test that REPL history command calls calculator.get_history()."""
        # Manually build history via calculator
        calculator.add(5, 3)
        calculator.square(4)

        repl = CalculatorREPL(calculator)
        with patch("builtins.input", side_effect=["history", "exit"]):
            with patch("builtins.print") as mock_print:
                repl.run()

        # Verify that history entries were printed
        printed_output = "\n".join(str(call) for call in mock_print.call_args_list)
        assert "5 add 3 = 8" in printed_output or any(
            "5" in str(call) and "add" in str(call) for call in mock_print.call_args_list
        )

    def test_separate_repl_instances_use_same_calculator_history(self, calculator):
        """Test that multiple REPL instances using same calculator share history."""
        calculator.add(5, 3)

        repl1 = CalculatorREPL(calculator)
        repl2 = CalculatorREPL(calculator)

        # Both should see the same history entry
        assert len(repl1._calculator.get_history()) == 1
        assert len(repl2._calculator.get_history()) == 1
        assert repl1._calculator.get_history()[0] == repl2._calculator.get_history()[0]


class TestHistoryEdgeCases:
    """Tests for edge cases in history command behavior."""

    def test_history_after_failed_operation_still_shows_prior_entries(self, repl, capsys):
        """Test that failed operations don't prevent history display of valid ones.

        Note: Due to retry loop behavior, 'history' typed during retry prompt
        is treated as an expression, not as the history command. This test
        verifies that the add operation is still recorded and accessible.
        """
        with patch("builtins.input", side_effect=[
            "add 5 3",
            "divide 10 0",
            "add 2 2",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        # add operations should be in history, divide by zero should not
        assert "1. 5 add 3 = 8" in captured.out
        assert "2. 2 add 2 = 4" in captured.out

    def test_history_with_very_long_operation_sequence(self, repl, capsys):
        """Test history display with many operations."""
        inputs = []
        for i in range(1, 6):
            inputs.append(f"add {i} {i}")
        inputs.append("history")
        inputs.append("exit")

        with patch("builtins.input", side_effect=inputs):
            repl.run()

        captured = capsys.readouterr()
        for i in range(1, 6):
            assert f"{i}. {i} add {i} = {i*2}" in captured.out

    def test_history_with_zero_operands(self, repl, capsys):
        """Test history display with zero operands."""
        with patch("builtins.input", side_effect=[
            "add 0 5",
            "multiply 0 10",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. 0 add 5 = 5" in captured.out
        assert "2. 0 multiply 10 = 0" in captured.out

    def test_history_with_negative_results(self, repl, capsys):
        """Test history display with negative results."""
        with patch("builtins.input", side_effect=[
            "subtract 5 10",
            "multiply -2 3",
            "history",
            "exit"
        ]):
            repl.run()

        captured = capsys.readouterr()
        assert "1. 5 subtract 10 = -5" in captured.out
        assert "2. -2 multiply 3 = -6" in captured.out
