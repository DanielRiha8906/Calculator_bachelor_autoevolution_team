"""Tests for scientific mode UI behaviors.

This module tests the new UI features added in Issue #410:
1. display_welcome() function and its output
2. display_mode_change() auto-derivation of operations
3. prompt_for_operator() mode toggle hint in prompt text
4. Re-exports from src.cli module (backward compatibility)
5. Scientific vs. normal mode operation filtering in display_mode_change()
"""

import pytest
from unittest.mock import patch
from src.interface import display_welcome, display_mode_change, prompt_for_operator


# ==============================================================================
# Test 1: display_welcome exists and prints mode toggle hint
# ==============================================================================

class TestDisplayWelcome:
    """Test suite for the display_welcome function."""

    def test_display_welcome_prints_message(self, capsys):
        """Test that display_welcome prints a welcome message containing 'Welcome'.

        Calls display_welcome() and verifies that stdout contains the word 'Welcome'.
        """
        display_welcome()
        captured = capsys.readouterr()
        assert "Welcome" in captured.out, (
            "display_welcome() should print a message containing 'Welcome' to stdout"
        )

    def test_display_welcome_prints_mode_toggle_hint(self, capsys):
        """Test that display_welcome prints hint about mode toggle.

        Calls display_welcome() and verifies that stdout contains either 'mode' or 'sci'
        to inform the user how to toggle modes.
        """
        display_welcome()
        captured = capsys.readouterr()
        output_lower = captured.out.lower()
        has_mode_hint = "mode" in output_lower or "sci" in output_lower
        assert has_mode_hint, (
            "display_welcome() should print a hint about mode toggling "
            "(should contain 'mode' or 'sci')"
        )


# ==============================================================================
# Test 2: display_mode_change auto-derives scientific ops when available_ops=None
# ==============================================================================

class TestDisplayModeChangeScientificAutoDerive:
    """Test suite for display_mode_change with scientific mode auto-derivation."""

    def test_display_mode_change_scientific_auto_derives_ops(self, capsys):
        """Test that display_mode_change('scientific') auto-derives and lists scientific ops.

        Calls display_mode_change('scientific') without providing available_ops,
        and verifies that output contains 'Switched to scientific mode' and 'sin'
        (one of the scientific operations).
        """
        display_mode_change("scientific")
        captured = capsys.readouterr()
        output_lower = captured.out.lower()
        assert "scientific" in output_lower, (
            "display_mode_change('scientific') should print a message "
            "containing 'scientific'"
        )
        assert "sin" in output_lower, (
            "display_mode_change('scientific') should list 'sin' "
            "(one of the scientific operations)"
        )


# ==============================================================================
# Test 3: display_mode_change auto-derives normal ops when available_ops=None
# ==============================================================================

class TestDisplayModeChangeNormalAutoDerive:
    """Test suite for display_mode_change with normal mode auto-derivation."""

    def test_display_mode_change_normal_auto_derives_ops(self, capsys):
        """Test that display_mode_change('normal') auto-derives and lists normal ops.

        Calls display_mode_change('normal') without providing available_ops,
        and verifies that output contains 'Switched to normal mode' and '+' (addition).
        """
        display_mode_change("normal")
        captured = capsys.readouterr()
        output_lower = captured.out.lower()
        assert "normal" in output_lower, (
            "display_mode_change('normal') should print a message "
            "containing 'normal'"
        )
        assert "+" in captured.out, (
            "display_mode_change('normal') should list '+' "
            "(one of the normal operations)"
        )


# ==============================================================================
# Test 4: display_mode_change uses explicit list when available_ops provided
# ==============================================================================

class TestDisplayModeChangeExplicitOps:
    """Test suite for display_mode_change with explicit operation list."""

    def test_display_mode_change_uses_explicit_ops_list(self, capsys):
        """Test that display_mode_change uses the provided available_ops list.

        Calls display_mode_change('scientific', ['sin', 'cos']),
        and verifies that output contains both 'sin' and 'cos'.
        """
        display_mode_change("scientific", ["sin", "cos"])
        captured = capsys.readouterr()
        assert "sin" in captured.out.lower(), (
            "display_mode_change should include 'sin' when provided in available_ops"
        )
        assert "cos" in captured.out.lower(), (
            "display_mode_change should include 'cos' when provided in available_ops"
        )


# ==============================================================================
# Test 5: prompt_for_operator prompt text contains mode toggle hint
# ==============================================================================

class TestPromptForOperatorModeHint:
    """Test suite for mode toggle hint in prompt_for_operator prompt text."""

    @patch("builtins.input", return_value="+")
    def test_prompt_for_operator_contains_mode_hint(self, mock_input):
        """Test that prompt_for_operator's input prompt contains 'mode'.

        Mocks input to return '+' and verifies that the prompt string passed to
        input() contains 'mode' to hint the user about mode toggling.
        """
        result = prompt_for_operator(mode="normal")
        assert result == "+", "Should accept '+' as a valid operator"

        # Verify the prompt string passed to input() contains 'mode'
        assert mock_input.called, "input() should have been called"
        call_args = mock_input.call_args
        if call_args:
            prompt_text = call_args[0][0] if call_args[0] else ""
            assert "mode" in prompt_text.lower(), (
                "The prompt string passed to input() should contain 'mode' "
                "to hint about mode toggling"
            )


# ==============================================================================
# Test 6: display_welcome is importable from src.cli
# ==============================================================================

class TestDisplayWelcomeImportFromCli:
    """Test suite for backward compatibility: display_welcome importable from src.cli."""

    def test_display_welcome_importable_from_cli(self):
        """Test that display_welcome can be imported from src.cli (backward compat).

        Attempts to import display_welcome from src.cli and verifies it is callable.
        This ensures backward compatibility with code that expects display_welcome
        to be re-exported from the cli module.
        """
        from src.cli import display_welcome
        assert callable(display_welcome), (
            "display_welcome should be importable from src.cli and callable"
        )


# ==============================================================================
# Test 7: display_mode_change with scientific mode lists at least 3 scientific ops
# ==============================================================================

class TestDisplayModeChangeScientificOpsCount:
    """Test suite for comprehensive scientific operations list."""

    def test_display_mode_change_scientific_lists_multiple_scientific_ops(self, capsys):
        """Test that display_mode_change('scientific') lists at least 3 scientific ops.

        Calls display_mode_change('scientific') and verifies that output contains
        at least 3 of: sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, pi, e
        """
        display_mode_change("scientific")
        captured = capsys.readouterr()
        output_lower = captured.out.lower()

        scientific_ops = ["sin", "cos", "tan", "asin", "acos", "atan",
                         "sinh", "cosh", "tanh", "exp", "pi", "e"]
        found_ops = [op for op in scientific_ops if op in output_lower]

        assert len(found_ops) >= 3, (
            f"display_mode_change('scientific') should list at least 3 scientific ops. "
            f"Found: {found_ops}"
        )


# ==============================================================================
# Test 8: display_mode_change with normal mode does NOT list scientific ops
# ==============================================================================

class TestDisplayModeChangeNormalExcludesScientificOps:
    """Test suite for normal mode operation filtering."""

    def test_display_mode_change_normal_does_not_list_scientific_ops(self, capsys):
        """Test that display_mode_change('normal') does NOT list 'sin'.

        Calls display_mode_change('normal') and verifies that output does NOT
        contain 'sin' (a scientific operation). This ensures normal mode only
        shows the basic 12 operations, not the additional scientific operations.
        """
        display_mode_change("normal")
        captured = capsys.readouterr()
        output_lower = captured.out.lower()

        assert "sin" not in output_lower, (
            "display_mode_change('normal') should NOT list 'sin' "
            "(a scientific operation exclusive to scientific mode)"
        )
