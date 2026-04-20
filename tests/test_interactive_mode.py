"""Comprehensive tests for interactive mode with scientific mode support.

Tests cover:
- Mode switching commands (mode scientific, mode normal)
- Mode indicator in prompt
- Scientific operation blocking in normal mode
- Scientific operation execution in scientific mode
- Mode persistence through operations
"""

import pytest
import math
from unittest.mock import patch, call
from src.presentation.interactive import run_interactive, OPERATIONS, SCIENTIFIC_OPERATIONS


# ============================================================================
# MODE SWITCHING TESTS
# ============================================================================


class TestModeSwitch:
    """Test suite for mode switching in interactive mode."""

    @patch("builtins.input", side_effect=["mode scientific", "quit"])
    @patch("builtins.print")
    def test_mode_switch_to_scientific(self, mock_print, mock_input):
        """Test switching to scientific mode prints confirmation."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        mode_set_printed = any("Mode set to scientific" in str(call_obj) for call_obj in print_calls)
        assert mode_set_printed

    @patch("builtins.input", side_effect=["mode scientific", "mode normal", "quit"])
    @patch("builtins.print")
    def test_mode_switch_to_normal(self, mock_print, mock_input):
        """Test switching to normal mode prints confirmation."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        mode_set_printed = any("Mode set to normal" in str(call_obj) for call_obj in print_calls)
        assert mode_set_printed

    @patch("builtins.input", side_effect=["mode scientific", "mode normal", "mode scientific", "quit"])
    @patch("builtins.print")
    def test_mode_toggle_multiple_times(self, mock_print, mock_input):
        """Test toggling modes multiple times."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        mode_set_count = sum(1 for call_obj in print_calls if "Mode set to" in str(call_obj))
        assert mode_set_count >= 3


# ============================================================================
# MODE INDICATOR TESTS
# ============================================================================


class TestModeIndicator:
    """Test suite for mode indicator in interactive prompt."""

    @patch("builtins.input", side_effect=["quit"])
    @patch("builtins.print")
    def test_default_mode_indicator_normal(self, mock_print, mock_input):
        """Test that default prompt shows [Normal Mode]."""
        run_interactive()
        input_calls = [str(call_obj) for call_obj in mock_input.call_args_list]
        normal_mode_shown = any("[Normal Mode]" in str(call_obj) for call_obj in input_calls)
        assert normal_mode_shown

    @patch("builtins.input", side_effect=["mode scientific", "quit"])
    @patch("builtins.print")
    def test_mode_indicator_scientific_after_switch(self, mock_print, mock_input):
        """Test that prompt shows [Scientific Mode] after switching."""
        run_interactive()
        input_calls = [str(call_obj) for call_obj in mock_input.call_args_list]
        scientific_mode_shown = any("[Scientific Mode]" in str(call_obj) for call_obj in input_calls)
        assert scientific_mode_shown


# ============================================================================
# SCIENTIFIC OPERATION BLOCKING TESTS
# ============================================================================


class TestScientificOperationBlocking:
    """Test suite for blocking scientific operations in normal mode."""

    @patch("builtins.input", side_effect=["sin", "quit"])
    @patch("builtins.print")
    def test_sin_blocked_in_normal_mode(self, mock_print, mock_input):
        """Test that sin operation is blocked in normal mode."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        error_printed = any("not available in normal mode" in str(call_obj) or "Error" in str(call_obj) for call_obj in print_calls)
        assert error_printed

    @patch("builtins.input", side_effect=["cos", "quit"])
    @patch("builtins.print")
    def test_cos_blocked_in_normal_mode(self, mock_print, mock_input):
        """Test that cos operation is blocked in normal mode."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        error_printed = any("not available in normal mode" in str(call_obj) or "Error" in str(call_obj) for call_obj in print_calls)
        assert error_printed

    @patch("builtins.input", side_effect=["tan", "quit"])
    @patch("builtins.print")
    def test_tan_blocked_in_normal_mode(self, mock_print, mock_input):
        """Test that tan operation is blocked in normal mode."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        error_printed = any("not available in normal mode" in str(call_obj) or "Error" in str(call_obj) for call_obj in print_calls)
        assert error_printed

    @patch("builtins.input", side_effect=["exp", "quit"])
    @patch("builtins.print")
    def test_exp_blocked_in_normal_mode(self, mock_print, mock_input):
        """Test that exp operation is blocked in normal mode."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        error_printed = any("not available in normal mode" in str(call_obj) or "Error" in str(call_obj) for call_obj in print_calls)
        assert error_printed

    @patch("builtins.input", side_effect=["sin", "quit"])
    @patch("builtins.print")
    def test_scientific_op_blocked_error_message_mentions_operation(self, mock_print, mock_input):
        """Test that blocking message mentions the operation name."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        error_with_sin = any("sin" in str(call_obj) and ("not available" in str(call_obj) or "Error" in str(call_obj)) for call_obj in print_calls)
        assert error_with_sin


# ============================================================================
# SCIENTIFIC OPERATION EXECUTION TESTS
# ============================================================================


class TestScientificOperationExecution:
    """Test suite for executing scientific operations in scientific mode."""

    @patch("builtins.input", side_effect=["mode scientific", "sin", "0", "quit"])
    @patch("builtins.print")
    def test_sin_works_in_scientific_mode(self, mock_print, mock_input):
        """Test that sin can be executed in scientific mode."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        result_printed = any("Result" in str(call_obj) or "0" in str(call_obj) for call_obj in print_calls)
        assert result_printed

    @patch("builtins.input", side_effect=["mode scientific", "cos", "0", "quit"])
    @patch("builtins.print")
    def test_cos_works_in_scientific_mode(self, mock_print, mock_input):
        """Test that cos can be executed in scientific mode."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        result_printed = any("Result" in str(call_obj) or "1" in str(call_obj) for call_obj in print_calls)
        assert result_printed

    @patch("builtins.input", side_effect=["mode scientific", "tan", "0", "quit"])
    @patch("builtins.print")
    def test_tan_works_in_scientific_mode(self, mock_print, mock_input):
        """Test that tan can be executed in scientific mode."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        result_printed = any("Result" in str(call_obj) for call_obj in print_calls)
        assert result_printed

    @patch("builtins.input", side_effect=["mode scientific", "exp", "0", "quit"])
    @patch("builtins.print")
    def test_exp_works_in_scientific_mode(self, mock_print, mock_input):
        """Test that exp can be executed in scientific mode."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        result_printed = any("Result" in str(call_obj) or "1" in str(call_obj) for call_obj in print_calls)
        assert result_printed

    @patch("builtins.input", side_effect=["mode scientific", "sin", str(math.pi / 2), "quit"])
    @patch("builtins.print")
    def test_sin_with_pi_over_2_in_scientific_mode(self, mock_print, mock_input):
        """Test sin(π/2) ≈ 1 in scientific mode."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        result_printed = any("Result" in str(call_obj) for call_obj in print_calls)
        assert result_printed


# ============================================================================
# MODE PERSISTENCE TESTS
# ============================================================================


class TestModePersistence:
    """Test suite for mode persistence across operations."""

    @patch("builtins.input", side_effect=["mode scientific", "add", "2", "3", "sin", "0", "quit"])
    @patch("builtins.print")
    def test_mode_persists_after_basic_operation(self, mock_print, mock_input):
        """Test that scientific mode persists after executing basic operation."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        result_count = sum(1 for call_obj in print_calls if "Result" in str(call_obj))
        # Should have two results: add result and sin result
        assert result_count >= 2

    @patch("builtins.input", side_effect=["mode scientific", "sin", "0", "add", "1", "2", "quit"])
    @patch("builtins.print")
    def test_mode_persists_across_mixed_operations(self, mock_print, mock_input):
        """Test that mode persists when mixing scientific and basic operations."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        result_count = sum(1 for call_obj in print_calls if "Result" in str(call_obj))
        # Should have two results: sin result and add result
        assert result_count >= 2


# ============================================================================
# OPERATIONS DICT TESTS
# ============================================================================


class TestOperationsDictStructure:
    """Test the structure of OPERATIONS dict with scientific operations."""

    def test_operations_dict_includes_scientific_operations(self):
        """Test that OPERATIONS dict includes sin, cos, tan, exp."""
        assert "sin" in OPERATIONS
        assert "cos" in OPERATIONS
        assert "tan" in OPERATIONS
        assert "exp" in OPERATIONS

    def test_scientific_operations_frozenset_is_defined(self):
        """Test that SCIENTIFIC_OPERATIONS frozenset exists."""
        assert isinstance(SCIENTIFIC_OPERATIONS, frozenset)

    def test_scientific_operations_contains_four_operations(self):
        """Test that SCIENTIFIC_OPERATIONS contains exactly 4 operations."""
        assert len(SCIENTIFIC_OPERATIONS) == 4

    def test_scientific_operations_contains_correct_names(self):
        """Test that SCIENTIFIC_OPERATIONS contains sin, cos, tan, exp."""
        assert "sin" in SCIENTIFIC_OPERATIONS
        assert "cos" in SCIENTIFIC_OPERATIONS
        assert "tan" in SCIENTIFIC_OPERATIONS
        assert "exp" in SCIENTIFIC_OPERATIONS

    def test_operations_dict_has_16_total_entries(self):
        """Test that OPERATIONS dict has 16 entries total."""
        assert len(OPERATIONS) == 16

    def test_scientific_operations_map_to_correct_methods(self):
        """Test that scientific operations map to correct Calculator methods."""
        assert OPERATIONS["sin"][0] == "sin"
        assert OPERATIONS["cos"][0] == "cos"
        assert OPERATIONS["tan"][0] == "tan"
        assert OPERATIONS["exp"][0] == "exp"

    def test_scientific_operations_have_one_operand(self):
        """Test that scientific operations require 1 operand."""
        assert OPERATIONS["sin"][1] == 1
        assert OPERATIONS["cos"][1] == 1
        assert OPERATIONS["tan"][1] == 1
        assert OPERATIONS["exp"][1] == 1

    def test_basic_operations_still_in_dict(self):
        """Test that basic operations are still present."""
        assert "add" in OPERATIONS
        assert "subtract" in OPERATIONS
        assert "multiply" in OPERATIONS
        assert "divide" in OPERATIONS
        assert "square" in OPERATIONS
        assert "factorial" in OPERATIONS


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


class TestScientificModeIntegration:
    """Integration tests for scientific mode feature."""

    @patch("builtins.input", side_effect=["sin", "mode scientific", "sin", "0", "quit"])
    @patch("builtins.print")
    def test_switch_to_scientific_after_failed_sin_attempt(self, mock_print, mock_input):
        """Test switching to scientific mode after sin is blocked."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        # Should have error for first sin (blocked), then valid result for second sin (in scientific mode)
        error_count = sum(1 for call_obj in print_calls if "not available in normal mode" in str(call_obj))
        result_count = sum(1 for call_obj in print_calls if "Result" in str(call_obj))
        assert error_count >= 1
        assert result_count >= 1

    @patch("builtins.input", side_effect=["mode scientific", "sin", "0", "mode normal", "add", "1", "2", "quit"])
    @patch("builtins.print")
    def test_switch_from_scientific_back_to_normal(self, mock_print, mock_input):
        """Test switching from scientific back to normal mode."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        result_count = sum(1 for call_obj in print_calls if "Result" in str(call_obj))
        # Should have sin result and add result
        assert result_count >= 2

    @patch("builtins.input", side_effect=["mode scientific", "sin", "0", "cos", "0", "tan", "0", "exp", "0", "quit"])
    @patch("builtins.print")
    def test_all_scientific_operations_in_sequence(self, mock_print, mock_input):
        """Test executing all scientific operations in sequence."""
        run_interactive()
        print_calls = [str(call_obj) for call_obj in mock_print.call_args_list]
        result_count = sum(1 for call_obj in print_calls if "Result" in str(call_obj))
        # Should have 4 results: sin, cos, tan, exp
        assert result_count >= 4
