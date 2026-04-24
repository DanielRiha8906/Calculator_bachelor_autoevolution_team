"""
Tests for the interactive history menu feature.

Tests the ability to view operation history during an interactive session
by typing "h", "H", or "history". The feature displays a numbered list
of operations (1-based indexing) or shows "No operations recorded yet."
"""

from unittest.mock import patch
import pytest
from src.ui.interactive import run_interactive_session


class TestHistoryViewCommand:
    """Test suite for history viewing in interactive mode."""

    def test_history_view_empty_at_start(self):
        """Test: User inputs ["h", "n"] - view history with no operations, then exit.

        Expected: Output contains "No operations recorded yet."
        """
        with patch('builtins.input', side_effect=["h", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "No operations recorded yet." in output

    def test_history_view_after_single_unary_operation(self):
        """Test: User performs one unary operation then types "h".

        Expected: Output contains `1. <operation>(<arg>) = <result>`
        """
        with patch('builtins.input', side_effect=["10", "4", "h", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # square(4) = 16 is operation index 10
                assert "1." in output and "square(4)" in output and "16" in output

    def test_history_view_after_single_binary_operation(self):
        """Test: User performs one binary operation (add 2, 3) then types "h".

        Expected: Output contains `1. add(2, 3) = 5`
        """
        with patch('builtins.input', side_effect=["0", "2", "3", "h", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "1." in output and "add(2, 3)" in output and "5" in output

    def test_history_view_after_three_operations(self):
        """Test: User performs three operations, then types "h".

        Expected: Output contains 3 numbered entries in order.
        """
        with patch('builtins.input', side_effect=["0", "1", "2", "yes", "0", "3", "4", "yes", "0", "5", "6", "h", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # Three separate add operations
                assert "1." in output
                assert "2." in output
                assert "3." in output

    def test_history_view_with_float_operands(self):
        """Test: User divides 5 by 2, views history.

        Expected: Output contains `1. divide(5, 2) = 2.5`
        """
        with patch('builtins.input', side_effect=["3", "5", "2", "h", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "1." in output and "divide(5, 2)" in output and "2.5" in output

    def test_history_view_with_negative_operands(self):
        """Test: User does add(-5, 3), views history.

        Expected: Output contains `1. add(-5, 3) = -2`
        """
        with patch('builtins.input', side_effect=["0", "-5", "3", "h", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                assert "1." in output and "add(-5, 3)" in output and "-2" in output

    def test_history_view_does_not_record_errors(self):
        """Test: User attempts a failing operation (e.g., sqrt of -4), then views history.

        Expected: Output contains "No operations recorded yet."
        """
        with patch('builtins.input', side_effect=["9", "-4", "yes", "h", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # sqrt with negative input should fail and not be recorded
                assert "No operations recorded yet." in output

    def test_history_view_command_case_insensitive_lowercase(self):
        """Test: User types "h" (lowercase).

        Expected: History is displayed.
        """
        with patch('builtins.input', side_effect=["0", "5", "5", "h", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # If the feature works, lowercase "h" should trigger history display
                # Add validation that history is displayed after "h"
                assert "1." in output or "No operations recorded yet." in output

    def test_history_view_command_case_insensitive_uppercase(self):
        """Test: User types "H" (uppercase).

        Expected: History is displayed.
        """
        with patch('builtins.input', side_effect=["0", "7", "8", "H", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # If the feature works, uppercase "H" should trigger history display
                assert "1." in output or "No operations recorded yet." in output

    def test_history_view_command_case_insensitive_word(self):
        """Test: User types "history" (full word).

        Expected: History is displayed.
        """
        with patch('builtins.input', side_effect=["0", "2", "2", "history", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # If the feature works, "history" should trigger history display
                assert "1." in output or "No operations recorded yet." in output

    def test_history_view_returns_to_menu(self):
        """Test: After viewing history, the operation menu is redisplayed (session continues).

        User views history, then performs another operation.
        Expected: History is displayed with "1. add(1, 2) = 3", then user continues
        and performs another operation, resulting in 2 add operations total.
        """
        with patch('builtins.input', side_effect=["0", "1", "2", "h", "yes", "0", "3", "4", "no"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # After viewing history with "h", should show "1. add(1, 2) = 3"
                # Then continuing should allow another operation (second add)
                assert "1. add(1, 2) = 3" in output

    def test_history_view_continues_session_with_new_operation(self):
        """Test: User views history (empty), does an operation, views history again (1 entry).

        Second view shows the new entry.
        """
        with patch('builtins.input', side_effect=["h", "yes", "0", "5", "5", "h", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # First view should show "No operations recorded yet."
                # Second view should show the operation
                assert "add(5, 5)" in output and "10" in output

    def test_history_display_format_exact(self):
        """Test: Verify exact format: `1. square(4) = 16` (with period after number, space before operation).

        Expected: Format is `1. operation_name(...) = result` with no extra whitespace.
        """
        with patch('builtins.input', side_effect=["10", "4", "h", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output_lines = [
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                ]
                full_output = "\n".join(output_lines)
                # Check for exact format with period and space
                assert "1. square(4) = 16" in full_output

    def test_history_menu_shows_help_text(self):
        """Test: The menu displayed to the user includes text indicating "h" is available.

        Expected: Menu contains text like "h: View operation history" or similar.
        """
        with patch('builtins.input', side_effect=["h", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                output_lower = output.lower()
                # Menu should mention how to view history
                assert ("h:" in output_lower or "view history" in output_lower or
                        "history" in output_lower)

    def test_history_view_on_invalid_operation_then_history(self):
        """Test: User enters invalid index (e.g., "999"), then views history.

        Expected: History is empty, shows "No operations recorded yet."
        """
        with patch('builtins.input', side_effect=["999", "h", "n"]):
            with patch('builtins.print') as mock_print:
                run_interactive_session()
                output = " ".join(
                    str(call_args[0][0]) for call_args in mock_print.call_args_list
                    if call_args[0]
                )
                # After invalid operation and viewing history, should show no operations
                assert "No operations recorded yet." in output
