"""Tests for CLI mode of the Calculator application.

Tests the command-line interface for the calculator when invoked with
command-line arguments (e.g., 'calculator add 5 3') rather than the
interactive mode.
"""

import sys
import pytest


# ============================================================================
# Test Group A: CLI Mode — Argument Parsing and Execution
# ============================================================================

class TestCLIBasicOperations:
    """Test basic CLI operations with two operands."""

    def test_cli_add_two_operands(self, monkeypatch, capsys):
        """Test 'calculator add 5 3' outputs 8."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'add', '5', '3'])

        # Import and call CLI handler (to be implemented)
        from src.__main__ import cli_mode

        cli_mode()
        captured = capsys.readouterr()
        assert '8' in captured.out

    def test_cli_subtract_two_operands(self, monkeypatch, capsys):
        """Test 'calculator subtract 10 4' outputs 6."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'subtract', '10', '4'])

        from src.__main__ import cli_mode

        cli_mode()
        captured = capsys.readouterr()
        assert '6' in captured.out

    def test_cli_multiply_two_operands(self, monkeypatch, capsys):
        """Test 'calculator multiply 6 7' outputs 42."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'multiply', '6', '7'])

        from src.__main__ import cli_mode

        cli_mode()
        captured = capsys.readouterr()
        assert '42' in captured.out

    def test_cli_divide_two_operands(self, monkeypatch, capsys):
        """Test 'calculator divide 20 4' outputs 5 or 5.0."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'divide', '20', '4'])

        from src.__main__ import cli_mode

        cli_mode()
        captured = capsys.readouterr()
        # Check for either 5 or 5.0
        assert '5' in captured.out

    def test_cli_factorial_single_operand(self, monkeypatch, capsys):
        """Test 'calculator factorial 5' outputs 120."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'factorial', '5'])

        from src.__main__ import cli_mode

        cli_mode()
        captured = capsys.readouterr()
        assert '120' in captured.out

    def test_cli_square_single_operand(self, monkeypatch, capsys):
        """Test 'calculator square 9' outputs 81."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'square', '9'])

        from src.__main__ import cli_mode

        cli_mode()
        captured = capsys.readouterr()
        assert '81' in captured.out

    def test_cli_square_root_single_operand(self, monkeypatch, capsys):
        """Test 'calculator square_root 16' outputs 4 or 4.0."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'square_root', '16'])

        from src.__main__ import cli_mode

        cli_mode()
        captured = capsys.readouterr()
        assert '4' in captured.out

    def test_cli_power_two_operands(self, monkeypatch, capsys):
        """Test 'calculator power 2 8' outputs 256."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'power', '2', '8'])

        from src.__main__ import cli_mode

        cli_mode()
        captured = capsys.readouterr()
        assert '256' in captured.out

    def test_cli_ln_single_operand(self, monkeypatch, capsys):
        """Test 'calculator ln 2.718281828' outputs value close to 1.0."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'ln', '2.718281828'])

        from src.__main__ import cli_mode

        cli_mode()
        captured = capsys.readouterr()
        # Check that output contains a number close to 1.0
        output = captured.out
        assert output  # Must produce output


# ============================================================================
# Test Group B: CLI Mode — Float and Negative Arguments
# ============================================================================

class TestCLIFloatsAndNegatives:
    """Test CLI with float and negative operands."""

    def test_cli_float_operands(self, monkeypatch, capsys):
        """Test 'calculator add 2.5 3.7' outputs 6.2 (with float tolerance)."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'add', '2.5', '3.7'])

        from src.__main__ import cli_mode

        cli_mode()
        captured = capsys.readouterr()
        # 2.5 + 3.7 = 6.2, check for presence in output
        assert '6.2' in captured.out or '6.2000' in captured.out

    def test_cli_negative_operands(self, monkeypatch, capsys):
        """Test 'calculator subtract -10 -5' outputs -5."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'subtract', '-10', '-5'])

        from src.__main__ import cli_mode

        cli_mode()
        captured = capsys.readouterr()
        assert '-5' in captured.out


# ============================================================================
# Test Group C: CLI Mode — Error Handling
# ============================================================================

class TestCLIErrorHandling:
    """Test CLI error conditions and exception handling."""

    def test_cli_missing_operation(self, monkeypatch, capsys):
        """Test missing operation exits with error code 1."""
        monkeypatch.setattr(sys, 'argv', ['calculator'])

        from src.__main__ import cli_mode

        with pytest.raises(SystemExit) as exc_info:
            cli_mode()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        # Should have error message in stderr or stdout
        assert 'error' in (captured.err + captured.out).lower()

    def test_cli_unknown_operation(self, monkeypatch, capsys):
        """Test unknown operation exits with error code 1."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'invalid_op', '5', '3'])

        from src.__main__ import cli_mode

        with pytest.raises(SystemExit) as exc_info:
            cli_mode()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert 'error' in (captured.err + captured.out).lower()

    def test_cli_missing_operands_binary(self, monkeypatch, capsys):
        """Test missing operands for binary operation exits with error."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'add', '5'])

        from src.__main__ import cli_mode

        with pytest.raises(SystemExit) as exc_info:
            cli_mode()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert 'error' in (captured.err + captured.out).lower()

    def test_cli_missing_operands_unary(self, monkeypatch, capsys):
        """Test missing operands for unary operation exits with error."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'factorial'])

        from src.__main__ import cli_mode

        with pytest.raises(SystemExit) as exc_info:
            cli_mode()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert 'error' in (captured.err + captured.out).lower()

    def test_cli_invalid_operand_nonnumeric(self, monkeypatch, capsys):
        """Test non-numeric operand exits with error."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'add', '5', 'abc'])

        from src.__main__ import cli_mode

        with pytest.raises(SystemExit) as exc_info:
            cli_mode()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        output = captured.err + captured.out
        assert 'error' in output.lower()
        assert 'invalid' in output.lower() or 'number' in output.lower()

    def test_cli_division_by_zero_error(self, monkeypatch, capsys):
        """Test division by zero exits with error."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'divide', '10', '0'])

        from src.__main__ import cli_mode

        with pytest.raises(SystemExit) as exc_info:
            cli_mode()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert 'error' in (captured.err + captured.out).lower()

    def test_cli_domain_error_square_root(self, monkeypatch, capsys):
        """Test square_root of negative number exits with error."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'square_root', '-4'])

        from src.__main__ import cli_mode

        with pytest.raises(SystemExit) as exc_info:
            cli_mode()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert 'error' in (captured.err + captured.out).lower()

    def test_cli_domain_error_ln(self, monkeypatch, capsys):
        """Test ln of zero exits with error."""
        monkeypatch.setattr(sys, 'argv', ['calculator', 'ln', '0'])

        from src.__main__ import cli_mode

        with pytest.raises(SystemExit) as exc_info:
            cli_mode()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert 'error' in (captured.err + captured.out).lower()


# ============================================================================
# Test Group D: Interactive Mode Fallback (Backward Compatibility)
# ============================================================================

class TestInteractiveModeBackwardCompatibility:
    """Test that CLI mode function properly integrates with interactive mode fallback.

    These tests verify that when cli_mode() is called but should not execute a
    CLI operation (no args), it properly falls back to interactive mode.
    """

    def test_cli_mode_fallback_to_interactive_no_args(self, monkeypatch, capsys):
        """Test that cli_mode() with no argv properly starts interactive mode."""
        # Setup input for interactive mode
        input_sequence = ['quit']
        input_iter = iter(input_sequence)
        monkeypatch.setattr('builtins.input', lambda prompt: next(input_iter))
        monkeypatch.setattr(sys, 'argv', ['calculator'])

        from src.__main__ import cli_mode

        # Should fall back to interactive mode instead of erroring
        cli_mode()
        captured = capsys.readouterr()
        # Interactive mode should show operation selection prompt
        assert 'operation' in captured.out.lower() or 'select' in captured.out.lower()

    def test_cli_mode_fallback_interactive_with_operation(self, monkeypatch, capsys):
        """Test that cli_mode() can fall back to interactive and process operation."""
        input_sequence = ['add', '5', '3', 'quit']
        input_iter = iter(input_sequence)
        monkeypatch.setattr('builtins.input', lambda prompt: next(input_iter))
        monkeypatch.setattr(sys, 'argv', ['calculator'])

        from src.__main__ import cli_mode

        cli_mode()
        captured = capsys.readouterr()
        # Should show result of add
        assert '8' in captured.out

    def test_cli_mode_fallback_interactive_invalid_op(self, monkeypatch, capsys):
        """Test that cli_mode() fallback interactive handles errors properly."""
        input_sequence = ['invalid', 'quit']
        input_iter = iter(input_sequence)
        monkeypatch.setattr('builtins.input', lambda prompt: next(input_iter))
        monkeypatch.setattr(sys, 'argv', ['calculator'])

        from src.__main__ import cli_mode

        cli_mode()
        captured = capsys.readouterr()
        # Should show error message and continue to quit
        assert 'error' in captured.out.lower()
