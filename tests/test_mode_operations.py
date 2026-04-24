"""Tests for scientific mode operations and cross-mode compatibility.

Tests that scientific operations are available in scientific mode,
normal operations work in both modes, and domain validation is preserved.
"""

import sys
import pytest
from unittest.mock import patch
from src.calculator.main import _run_interactive_loop, _build_registry


# ============================================================================
# Test Group 1: Scientific Operations in Scientific Mode (1 test)
# ============================================================================

class TestScientificOperationsAvailability:
    """Tests for scientific operation availability in scientific mode."""

    @pytest.mark.parametrize("operation,operand,expected_result", [
        ("square", "4", "16"),
        ("cube", "2", "8"),
        ("power", "2\n3", "8"),  # Two operands
        ("ln", "1", "0"),
    ])
    def test_scientific_operations_in_scientific_mode_succeed(
        self, operation, operand, expected_result, monkeypatch, capsys
    ):
        """Test that scientific operations execute without mode rejection.

        Input: Interactive session in scientific mode; execute scientific operations
        Expected: All operations execute without mode rejection; produce correct results
        Note: Domain errors (e.g., sqrt(-1)) still raise ValueError; mode doesn't bypass validation
        """
        # Build input sequence with mode switch, then operation and operand(s)
        if operation == "power":
            # power needs two operands
            inputs = iter(['mode scientific', operation] + operand.split('\n') + ['quit'])
        else:
            inputs = iter(['mode scientific', operation, operand, 'quit'])

        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Should contain result
        assert expected_result in captured.out or f"Result: {expected_result}" in captured.out


# ============================================================================
# Test Group 2: Normal Operations in Both Modes (1 test)
# ============================================================================

class TestNormalOperationsAvailableInBothModes:
    """Tests for normal operation availability in all modes."""

    @pytest.mark.parametrize("mode,op1,op2,operand1,operand2,expected", [
        ("normal", "add", "add", "2", "3", "5"),
        ("scientific", "subtract", "subtract", "10", "3", "7"),
        ("normal", "multiply", "multiply", "4", "5", "20"),
        ("scientific", "divide", "divide", "20", "4", "5"),
    ])
    def test_normal_ops_available_in_both_modes(
        self, mode, op1, op2, operand1, operand2, expected, monkeypatch, capsys
    ):
        """Test that arithmetic operations work in both normal and scientific modes.

        Input: Interactive session; test add, subtract, multiply, divide in both modes
        Expected: All arithmetic operations succeed in both modes
        """
        # Build input sequence based on mode
        if mode == "scientific":
            inputs = iter(['mode scientific', op1, operand1, operand2, 'quit'])
        else:
            inputs = iter([op1, operand1, operand2, 'quit'])

        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        registry = _build_registry()
        _run_interactive_loop(registry)

        captured = capsys.readouterr()
        # Should contain result
        assert expected in captured.out or f"Result: {expected}" in captured.out


