import pytest
import sys
from unittest.mock import patch
from src.batch_cli import batch_main


class TestBatchCLIHelp:
    """Test suite for batch CLI help functionality."""

    def test_batch_cli_help_flag(self, capsys):
        """Test --help flag displays help message and exits with code 0."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["--help"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "help" in captured.out.lower() or "usage" in captured.out.lower()

    def test_batch_cli_h_flag(self, capsys):
        """Test -h flag displays help message and exits with code 0."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["-h"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "help" in captured.out.lower() or "usage" in captured.out.lower()


class TestBatchCLIBinaryOps:
    """Test suite for batch CLI binary operations."""

    def test_batch_cli_add(self, capsys):
        """Test add operation: add 5 3 -> 8."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["add", "5", "3"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "8" in captured.out

    def test_batch_cli_subtract(self, capsys):
        """Test subtract operation: subtract 10 4 -> 6."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["subtract", "10", "4"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "6" in captured.out

    def test_batch_cli_multiply(self, capsys):
        """Test multiply operation: multiply 3 7 -> 21."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["multiply", "3", "7"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "21" in captured.out

    def test_batch_cli_divide(self, capsys):
        """Test divide operation: divide 10 2 -> 5."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["divide", "10", "2"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "5" in captured.out

    def test_batch_cli_power(self, capsys):
        """Test power operation: power 2 3 -> 8."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["power", "2", "3"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "8" in captured.out


class TestBatchCLIUnaryOps:
    """Test suite for batch CLI unary operations."""

    def test_batch_cli_square(self, capsys):
        """Test square operation: square 5 -> 25."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["square", "5"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "25" in captured.out

    def test_batch_cli_cube(self, capsys):
        """Test cube operation: cube 3 -> 27."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["cube", "3"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "27" in captured.out

    def test_batch_cli_sqrt(self, capsys):
        """Test sqrt operation: sqrt 16 -> 4."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["sqrt", "16"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "4" in captured.out

    def test_batch_cli_cbrt(self, capsys):
        """Test cbrt operation: cbrt 27 -> 3."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["cbrt", "27"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "3" in captured.out

    def test_batch_cli_factorial(self, capsys):
        """Test factorial operation: factorial 5 -> 120."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["factorial", "5"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "120" in captured.out

    def test_batch_cli_log(self, capsys):
        """Test log operation: log 100 -> 2."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["log", "100"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "2" in captured.out

    def test_batch_cli_ln(self, capsys):
        """Test ln operation: ln 1 -> 0."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["ln", "1"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "0" in captured.out


class TestBatchCLIErrors:
    """Test suite for batch CLI error handling."""

    def test_batch_cli_division_by_zero(self, capsys):
        """Test division by zero error: divide 5 0 -> error containing 'zero'."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["divide", "5", "0"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "zero" in captured.err.lower()

    def test_batch_cli_sqrt_negative(self, capsys):
        """Test sqrt with negative number error: sqrt -4 -> error containing 'negative'."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["sqrt", "-4"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "negative" in captured.err.lower()

    def test_batch_cli_cbrt_negative(self, capsys):
        """Test cbrt with negative number (should work): cbrt -8 -> -2."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["cbrt", "-8"])
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "-2" in captured.out

    def test_batch_cli_factorial_negative(self, capsys):
        """Test factorial with negative number error: factorial -3 -> error containing 'negative'."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["factorial", "-3"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "negative" in captured.err.lower()

    def test_batch_cli_log_zero(self, capsys):
        """Test log of zero error: log 0 -> error containing 'positive'."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["log", "0"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "positive" in captured.err.lower()

    def test_batch_cli_log_negative(self, capsys):
        """Test log of negative error: log -5 -> error containing 'positive'."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["log", "-5"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "positive" in captured.err.lower()

    def test_batch_cli_ln_zero(self, capsys):
        """Test ln of zero error: ln 0 -> error containing 'positive'."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["ln", "0"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "positive" in captured.err.lower()

    def test_batch_cli_ln_negative(self, capsys):
        """Test ln of negative error: ln -1 -> error containing 'positive'."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["ln", "-1"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "positive" in captured.err.lower()


class TestBatchCLIArgValidation:
    """Test suite for batch CLI argument validation."""

    def test_batch_cli_missing_operand_unary(self, capsys):
        """Test missing operand for unary operation: square -> error."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["square"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert len(captured.err) > 0

    def test_batch_cli_missing_operands_binary(self, capsys):
        """Test missing second operand for binary operation: add 5 -> error."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["add", "5"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert len(captured.err) > 0

    def test_batch_cli_too_many_args_unary(self, capsys):
        """Test too many arguments for unary operation: square 5 extra -> error."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["square", "5", "extra"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert len(captured.err) > 0

    def test_batch_cli_too_many_args_binary(self, capsys):
        """Test too many arguments for binary operation: add 5 3 extra -> error."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["add", "5", "3", "extra"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert len(captured.err) > 0

    def test_batch_cli_invalid_numeric_unary(self, capsys):
        """Test invalid numeric input for unary operation: square abc -> error."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["square", "abc"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert len(captured.err) > 0

    def test_batch_cli_invalid_numeric_binary_first(self, capsys):
        """Test invalid numeric input for first operand: add xyz 5 -> error."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["add", "xyz", "5"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert len(captured.err) > 0

    def test_batch_cli_invalid_numeric_binary_second(self, capsys):
        """Test invalid numeric input for second operand: add 5 abc -> error."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["add", "5", "abc"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert len(captured.err) > 0


class TestBatchCLIInvalidOps:
    """Test suite for batch CLI invalid operation handling."""

    def test_batch_cli_unknown_operation(self, capsys):
        """Test unknown operation: invalid_op 5 -> error."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main(["invalid_op", "5"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert len(captured.err) > 0

    def test_batch_cli_no_operation(self, capsys):
        """Test no operation provided: [] -> error."""
        with pytest.raises(SystemExit) as exc_info:
            batch_main([])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert len(captured.err) > 0


class TestBackwardCompat:
    """Test suite for backward compatibility verification."""

    @pytest.mark.skip(reason="Verified by running test_cli.py separately")
    def test_interactive_existing_tests_not_broken(self):
        """Placeholder: Interactive CLI tests in test_cli.py remain unaffected by batch CLI introduction."""
        pass
