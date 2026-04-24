"""Comprehensive test suite for Calculator history feature.

Tests cover:
1. History recording and storage (24 tests)
2. CLI history display functionality (5 tests)
3. Integration with batch mode (1 test)
"""

import pytest
from unittest.mock import patch, MagicMock
from src.calculator import Calculator


# ===== HISTORY RECORDING & STORAGE TESTS (Tests 1-24) =====

class TestHistoryInitialization:
    """Test that Calculator initializes with empty history."""

    def test_history_initialized(self):
        """New Calculator instance has empty history list."""
        calc = Calculator()
        assert len(calc.get_history()) == 0
        assert calc.get_history() == []


class TestHistoryRecording:
    """Test that operations are recorded in history with correct structure."""

    def test_history_record_add(self):
        """After add(5, 3), history contains entry with operation='add', operands=[5, 3], result=8."""
        calc = Calculator()
        result = calc.add(5, 3)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0]['operation'] == 'add'
        assert history[0]['operands'] == [5, 3]
        assert history[0]['result'] == 8

    def test_history_record_subtract(self):
        """After subtract(10, 3), history contains entry with operation='subtract', operands=[10, 3], result=7."""
        calc = Calculator()
        result = calc.subtract(10, 3)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0]['operation'] == 'subtract'
        assert history[0]['operands'] == [10, 3]
        assert history[0]['result'] == 7

    def test_history_record_multiply(self):
        """After multiply(6, 7), history contains entry with operation='multiply', operands=[6, 7], result=42."""
        calc = Calculator()
        result = calc.multiply(6, 7)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0]['operation'] == 'multiply'
        assert history[0]['operands'] == [6, 7]
        assert history[0]['result'] == 42

    def test_history_record_divide(self):
        """After divide(15, 3), history contains entry with operation='divide', operands=[15, 3], result=5.0."""
        calc = Calculator()
        result = calc.divide(15, 3)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0]['operation'] == 'divide'
        assert history[0]['operands'] == [15, 3]
        assert history[0]['result'] == pytest.approx(5.0)

    def test_history_record_square(self):
        """After square(4), history records operation='square', operands=[4], result=16."""
        calc = Calculator()
        result = calc.square(4)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0]['operation'] == 'square'
        assert history[0]['operands'] == [4]
        assert history[0]['result'] == 16

    def test_history_record_cube(self):
        """After cube(3), history records operation='cube', operands=[3], result=27."""
        calc = Calculator()
        result = calc.cube(3)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0]['operation'] == 'cube'
        assert history[0]['operands'] == [3]
        assert history[0]['result'] == 27

    def test_history_record_sqrt(self):
        """After square_root(9), history records operation='square_root', operands=[9], result=3.0."""
        calc = Calculator()
        result = calc.square_root(9)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0]['operation'] == 'square_root'
        assert history[0]['operands'] == [9]
        assert history[0]['result'] == pytest.approx(3.0)

    def test_history_record_cbrt(self):
        """After cube_root(8), history records operation='cube_root', operands=[8], result=2.0."""
        calc = Calculator()
        result = calc.cube_root(8)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0]['operation'] == 'cube_root'
        assert history[0]['operands'] == [8]
        assert history[0]['result'] == pytest.approx(2.0)

    def test_history_record_factorial(self):
        """After factorial(5), history records operation='factorial', operands=[5], result=120."""
        calc = Calculator()
        result = calc.factorial(5)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0]['operation'] == 'factorial'
        assert history[0]['operands'] == [5]
        assert history[0]['result'] == 120

    def test_history_record_power(self):
        """After power(2, 8), history records operation='power', operands=[2, 8], result=256."""
        calc = Calculator()
        result = calc.power(2, 8)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0]['operation'] == 'power'
        assert history[0]['operands'] == [2, 8]
        assert history[0]['result'] == 256

    def test_history_record_log(self):
        """After log(100), history records operation='log', operands=[100], result approx 2.0."""
        calc = Calculator()
        result = calc.log(100)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0]['operation'] == 'log'
        assert history[0]['operands'] == [100]
        assert history[0]['result'] == pytest.approx(2.0)

    def test_history_record_ln(self):
        """After ln(e), history records operation='ln', operands=[e], result approx 1.0."""
        import math
        calc = Calculator()
        e = math.e
        result = calc.ln(e)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0]['operation'] == 'ln'
        assert history[0]['operands'] == [e]
        assert history[0]['result'] == pytest.approx(1.0)


class TestHistoryOrdering:
    """Test that history maintains chronological order."""

    def test_history_chronological_order(self):
        """Execute add, multiply, divide sequentially → history has 3 entries in exact order."""
        calc = Calculator()
        calc.add(1, 2)
        calc.multiply(3, 4)
        calc.divide(10, 2)
        history = calc.get_history()
        assert len(history) == 3
        assert history[0]['operation'] == 'add'
        assert history[1]['operation'] == 'multiply'
        assert history[2]['operation'] == 'divide'

    def test_history_multiple_same_operation(self):
        """Execute add(1, 1) twice on same instance → history has 2 entries, both add."""
        calc = Calculator()
        calc.add(1, 1)
        calc.add(1, 1)
        history = calc.get_history()
        assert len(history) == 2
        assert history[0]['operation'] == 'add'
        assert history[1]['operation'] == 'add'


class TestHistoryErrorHandling:
    """Test that failed operations are not recorded in history."""

    def test_history_not_recorded_divide_by_zero(self):
        """Call divide(5, 0) raises ZeroDivisionError → history remains empty."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(5, 0)
        assert len(calc.get_history()) == 0

    def test_history_not_recorded_sqrt_negative(self):
        """Call square_root(-1) raises ValueError → history remains empty."""
        calc = Calculator()
        with pytest.raises(ValueError):
            calc.square_root(-1)
        assert len(calc.get_history()) == 0

    def test_history_not_recorded_log_nonpositive(self):
        """Call log(-5) raises ValueError → history remains empty."""
        calc = Calculator()
        with pytest.raises(ValueError):
            calc.log(-5)
        assert len(calc.get_history()) == 0

    def test_history_not_recorded_factorial_negative(self):
        """Call factorial(-3) raises ValueError → history remains empty."""
        calc = Calculator()
        with pytest.raises(ValueError):
            calc.factorial(-3)
        assert len(calc.get_history()) == 0

    def test_history_success_after_error(self):
        """Call log(0) (fails), then add(1, 1) (succeeds) → history contains only 1 entry."""
        calc = Calculator()
        with pytest.raises(ValueError):
            calc.log(0)
        result = calc.add(1, 1)
        history = calc.get_history()
        assert len(history) == 1
        assert history[0]['operation'] == 'add'


class TestHistoryRetrieval:
    """Test get_history() and clear_history() methods."""

    def test_get_history_empty(self):
        """New Calculator, get_history() returns [] (empty list)."""
        calc = Calculator()
        assert calc.get_history() == []

    def test_get_history_returns_copy(self):
        """Record operation, get history, modify returned list → original unmodified."""
        calc = Calculator()
        calc.add(1, 1)
        history = calc.get_history()
        history.clear()  # Modify the returned list
        assert len(calc.get_history()) == 1  # Original should still have 1 entry

    def test_clear_history(self):
        """Record 3 operations, call clear_history() → get_history() is empty."""
        calc = Calculator()
        calc.add(1, 1)
        calc.subtract(5, 3)
        calc.multiply(2, 3)
        assert len(calc.get_history()) == 3
        calc.clear_history()
        assert len(calc.get_history()) == 0

    def test_clear_history_idempotent(self):
        """Call clear_history() twice → no error, history remains empty."""
        calc = Calculator()
        calc.add(1, 1)
        calc.clear_history()
        calc.clear_history()  # Second call should not raise
        assert len(calc.get_history()) == 0


# ===== CLI HISTORY DISPLAY TESTS (Tests 25-29) =====

class TestCLIDisplayHistory:
    """Test display_history() function for CLI output."""

    def test_cli_display_history_empty(self, capsys):
        """Call display_history(calc) with empty calc → output shows 'No operations recorded.'."""
        from src.cli import display_history
        calc = Calculator()
        display_history(calc)
        captured = capsys.readouterr()
        assert 'No operations recorded' in captured.out or 'No operations recorded.' in captured.out

    def test_cli_display_history_single_operation(self, capsys):
        """After add(5, 3), call display_history(calc) → output contains add, 5, 3, 8."""
        from src.cli import display_history
        calc = Calculator()
        calc.add(5, 3)
        display_history(calc)
        captured = capsys.readouterr()
        output = captured.out
        assert 'add' in output or '+' in output
        assert '5' in output
        assert '3' in output
        assert '8' in output

    def test_cli_display_history_multiple_operations(self, capsys):
        """After 3 operations (add, multiply, divide), call display_history(calc) → output shows 3 numbered lines in order."""
        from src.cli import display_history
        calc = Calculator()
        calc.add(2, 3)
        calc.multiply(4, 5)
        calc.divide(20, 4)
        display_history(calc)
        captured = capsys.readouterr()
        output = captured.out
        lines = output.strip().split('\n')
        # Should have at least 3 lines (one per operation)
        assert len(lines) >= 3
        # Check that all operations appear in output
        assert 'add' in output or '+' in output
        assert 'multiply' in output or '*' in output
        assert 'divide' in output or '/' in output

    def test_cli_display_history_unary_format(self, capsys):
        """After square(4), call display_history(calc) → output shows unary operation format."""
        from src.cli import display_history
        calc = Calculator()
        calc.square(4)
        display_history(calc)
        captured = capsys.readouterr()
        output = captured.out
        assert 'square' in output or '2' in output  # Either the word or exponent notation
        assert '4' in output
        assert '16' in output

    def test_cli_display_history_binary_format(self, capsys):
        """After add(5, 3), call display_history(calc) → output shows binary operation format."""
        from src.cli import display_history
        calc = Calculator()
        calc.add(5, 3)
        display_history(calc)
        captured = capsys.readouterr()
        output = captured.out
        # Should show: 5 [operator] 3 = 8
        assert '5' in output
        assert '3' in output
        assert '8' in output


# ===== INTEGRATION TESTS (Test 30) =====

class TestBatchModeIntegration:
    """Test that batch mode is stateless and doesn't expose history."""

    def test_batch_cli_stateless(self):
        """Batch mode execution produces result without history display.

        Verifies that batch mode operates independently: executing a batch operation
        produces a result without exposing or displaying operation history.
        Backward compatibility: existing batch_cli behavior unchanged.
        """
        from src.batch_cli import batch_main
        from io import StringIO

        # Execute batch add operation
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                try:
                    batch_main(['add', '5', '3'])
                except SystemExit as e:
                    # batch_main calls sys.exit(0) on success
                    assert e.code == 0
                output = mock_stdout.getvalue()
                # Result should be printed
                assert '8' in output
                # History should NOT be automatically displayed in batch mode
                # (if History feature exists, batch mode shouldn't expose it)
                assert output.count('\n') <= 2  # At most one or two lines (result + maybe newline)
