"""Comprehensive pytest tests for CLI mode (CLIHandler and main function).

Tests cover:
- CLIHandler.get_operation_mapping: all operations present
- CLIHandler.parse_args: valid/invalid operations and operands
- CLIHandler.execute: all operations (unary and binary)
- Subprocess integration tests: CLI invocation and exit codes
- Backward compatibility: REPL mode via argv=[] or ["--repl"]
- Edge cases: negative numbers, floats, errors, symbol aliases
"""

import pytest
import subprocess
import sys
import math
from unittest.mock import patch, Mock
from io import StringIO

from src.cli import CLIHandler
from src.calculator import Calculator


# ==============================================================================
# FIXTURES
# ==============================================================================

@pytest.fixture
def calculator():
    """Provide a real Calculator instance."""
    return Calculator()


@pytest.fixture
def handler(calculator):
    """Provide a CLIHandler instance with a real Calculator."""
    return CLIHandler(calculator)


@pytest.fixture
def repo_root():
    """Provide the repository root directory."""
    return "/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team"


# ==============================================================================
# TESTS: CLIHandler.get_operation_mapping
# ==============================================================================

class TestGetOperationMapping:
    """Test suite for get_operation_mapping method."""

    def test_mapping_contains_all_operation_names(self, handler):
        """Test that mapping contains all canonical operation names."""
        mapping = handler.get_operation_mapping()
        expected_names = {
            "add", "subtract", "multiply", "divide", "power",
            "factorial", "square", "cube",
            "square_root", "cube_root",
            "natural_logarithm", "logarithm"
        }
        for name in expected_names:
            assert name in mapping, f"Missing operation name: {name}"

    def test_mapping_contains_all_symbols(self, handler):
        """Test that mapping contains all symbol aliases."""
        mapping = handler.get_operation_mapping()
        expected_symbols = {"+", "-", "*", "/", "^", "sqrt", "cbrt", "ln", "log"}
        for symbol in expected_symbols:
            assert symbol in mapping, f"Missing symbol: {symbol}"

    def test_mapping_returns_correct_method_names(self, handler):
        """Test that mapping values are method names."""
        mapping = handler.get_operation_mapping()
        # Check a few key mappings
        assert mapping["+"] == "add"
        assert mapping["-"] == "subtract"
        assert mapping["*"] == "multiply"
        assert mapping["/"] == "divide"
        assert mapping["^"] == "power"
        assert mapping["sqrt"] == "square_root"
        assert mapping["cbrt"] == "cube_root"
        assert mapping["ln"] == "natural_logarithm"
        assert mapping["log"] == "logarithm"

    def test_mapping_symbol_and_name_map_to_same_method(self, handler):
        """Test that symbols and names for the same operation map to the same method."""
        mapping = handler.get_operation_mapping()
        assert mapping["+"] == mapping["add"]
        assert mapping["-"] == mapping["subtract"]
        assert mapping["*"] == mapping["multiply"]
        assert mapping["/"] == mapping["divide"]
        assert mapping["^"] == mapping["power"]
        assert mapping["sqrt"] == mapping["square_root"]
        assert mapping["cbrt"] == mapping["cube_root"]
        assert mapping["ln"] == mapping["natural_logarithm"]
        assert mapping["log"] == mapping["logarithm"]

    def test_mapping_count(self, handler):
        """Test that mapping has approximately 20 entries (names + symbols)."""
        mapping = handler.get_operation_mapping()
        # 12 operations, some with names and symbols
        assert len(mapping) >= 20


# ==============================================================================
# TESTS: CLIHandler.parse_args - Valid Operations
# ==============================================================================

class TestParseArgsValidBinaryOps:
    """Test suite for parse_args with valid binary operations."""

    def test_parse_add_by_name(self, handler):
        """Test parsing 'add' operation by name."""
        method_name, operands = handler.parse_args(["add", "2", "3"])
        assert method_name == "add"
        assert operands == [2.0, 3.0]

    def test_parse_add_by_symbol(self, handler):
        """Test parsing 'add' operation by symbol."""
        method_name, operands = handler.parse_args(["+", "2", "3"])
        assert method_name == "add"
        assert operands == [2.0, 3.0]

    def test_parse_subtract_by_name(self, handler):
        """Test parsing 'subtract' operation by name."""
        method_name, operands = handler.parse_args(["subtract", "10", "3"])
        assert method_name == "subtract"
        assert operands == [10.0, 3.0]

    def test_parse_subtract_by_symbol(self, handler):
        """Test parsing 'subtract' operation by symbol."""
        method_name, operands = handler.parse_args(["-", "10", "3"])
        assert method_name == "subtract"
        assert operands == [10.0, 3.0]

    def test_parse_multiply_by_name(self, handler):
        """Test parsing 'multiply' operation by name."""
        method_name, operands = handler.parse_args(["multiply", "5", "6"])
        assert method_name == "multiply"
        assert operands == [5.0, 6.0]

    def test_parse_multiply_by_symbol(self, handler):
        """Test parsing 'multiply' operation by symbol."""
        method_name, operands = handler.parse_args(["*", "5", "6"])
        assert method_name == "multiply"
        assert operands == [5.0, 6.0]

    def test_parse_divide_by_name(self, handler):
        """Test parsing 'divide' operation by name."""
        method_name, operands = handler.parse_args(["divide", "12", "3"])
        assert method_name == "divide"
        assert operands == [12.0, 3.0]

    def test_parse_divide_by_symbol(self, handler):
        """Test parsing 'divide' operation by symbol."""
        method_name, operands = handler.parse_args(["/", "12", "3"])
        assert method_name == "divide"
        assert operands == [12.0, 3.0]

    def test_parse_power_by_name(self, handler):
        """Test parsing 'power' operation by name."""
        method_name, operands = handler.parse_args(["power", "2", "3"])
        assert method_name == "power"
        assert operands == [2.0, 3.0]

    def test_parse_power_by_symbol(self, handler):
        """Test parsing 'power' operation by symbol."""
        method_name, operands = handler.parse_args(["^", "2", "3"])
        assert method_name == "power"
        assert operands == [2.0, 3.0]

    def test_parse_logarithm_by_name(self, handler):
        """Test parsing 'logarithm' operation by name."""
        method_name, operands = handler.parse_args(["logarithm", "8", "2"])
        assert method_name == "logarithm"
        assert operands == [8.0, 2.0]

    def test_parse_logarithm_by_symbol(self, handler):
        """Test parsing 'logarithm' operation by symbol."""
        method_name, operands = handler.parse_args(["log", "8", "2"])
        assert method_name == "logarithm"
        assert operands == [8.0, 2.0]


class TestParseArgsValidUnaryOps:
    """Test suite for parse_args with valid unary operations."""

    def test_parse_factorial(self, handler):
        """Test parsing 'factorial' operation."""
        method_name, operands = handler.parse_args(["factorial", "5"])
        assert method_name == "factorial"
        assert operands == [5.0]

    def test_parse_square(self, handler):
        """Test parsing 'square' operation."""
        method_name, operands = handler.parse_args(["square", "4"])
        assert method_name == "square"
        assert operands == [4.0]

    def test_parse_cube(self, handler):
        """Test parsing 'cube' operation."""
        method_name, operands = handler.parse_args(["cube", "3"])
        assert method_name == "cube"
        assert operands == [3.0]

    def test_parse_square_root_by_name(self, handler):
        """Test parsing 'square_root' operation by name."""
        method_name, operands = handler.parse_args(["square_root", "16"])
        assert method_name == "square_root"
        assert operands == [16.0]

    def test_parse_square_root_by_symbol(self, handler):
        """Test parsing 'square_root' operation by symbol."""
        method_name, operands = handler.parse_args(["sqrt", "16"])
        assert method_name == "square_root"
        assert operands == [16.0]

    def test_parse_cube_root_by_name(self, handler):
        """Test parsing 'cube_root' operation by name."""
        method_name, operands = handler.parse_args(["cube_root", "8"])
        assert method_name == "cube_root"
        assert operands == [8.0]

    def test_parse_cube_root_by_symbol(self, handler):
        """Test parsing 'cube_root' operation by symbol."""
        method_name, operands = handler.parse_args(["cbrt", "8"])
        assert method_name == "cube_root"
        assert operands == [8.0]

    def test_parse_natural_logarithm_by_name(self, handler):
        """Test parsing 'natural_logarithm' operation by name."""
        method_name, operands = handler.parse_args(["natural_logarithm", "2.718"])
        assert method_name == "natural_logarithm"
        assert operands == [2.718]

    def test_parse_natural_logarithm_by_symbol(self, handler):
        """Test parsing 'natural_logarithm' operation by symbol."""
        method_name, operands = handler.parse_args(["ln", "2.718"])
        assert method_name == "natural_logarithm"
        assert operands == [2.718]


# ==============================================================================
# TESTS: CLIHandler.parse_args - Invalid Operations & Operands
# ==============================================================================

class TestParseArgsErrors:
    """Test suite for parse_args error handling."""

    def test_parse_unknown_operation(self, handler):
        """Test parsing unknown operation raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            handler.parse_args(["foobar", "2", "3"])
        assert "Unknown operation" in str(exc_info.value)

    def test_parse_missing_operand_binary(self, handler):
        """Test parsing binary operation with only one operand raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            handler.parse_args(["add", "2"])
        assert "Missing operand" in str(exc_info.value)

    def test_parse_missing_operand_unary(self, handler):
        """Test parsing unary operation with no operands raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            handler.parse_args(["factorial"])
        assert "Missing operand" in str(exc_info.value)

    def test_parse_extra_operand_unary(self, handler):
        """Test parsing unary operation with too many operands raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            handler.parse_args(["factorial", "5", "6"])
        assert "expected 1 operand" in str(exc_info.value)

    def test_parse_non_numeric_first_operand(self, handler):
        """Test parsing with non-numeric first operand raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            handler.parse_args(["add", "abc", "3"])
        assert "Invalid number" in str(exc_info.value)

    def test_parse_non_numeric_second_operand(self, handler):
        """Test parsing with non-numeric second operand raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            handler.parse_args(["add", "2", "xyz"])
        assert "Invalid number" in str(exc_info.value)

    def test_parse_empty_args(self, handler):
        """Test parsing empty args list raises ValueError."""
        with pytest.raises(ValueError):
            handler.parse_args([])

    def test_parse_special_char_operand(self, handler):
        """Test parsing special characters as operand raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            handler.parse_args(["add", "!@#$", "3"])
        assert "Invalid number" in str(exc_info.value)


# ==============================================================================
# TESTS: CLIHandler.parse_args - Numeric Variants
# ==============================================================================

class TestParseArgsNumericVariants:
    """Test suite for parse_args with various numeric formats."""

    def test_parse_float_operands(self, handler):
        """Test parsing float operands."""
        method_name, operands = handler.parse_args(["add", "1.5", "2.5"])
        assert operands == [1.5, 2.5]

    def test_parse_negative_operands(self, handler):
        """Test parsing negative operands."""
        method_name, operands = handler.parse_args(["add", "-1", "-2"])
        assert operands == [-1.0, -2.0]

    def test_parse_scientific_notation(self, handler):
        """Test parsing scientific notation operands."""
        method_name, operands = handler.parse_args(["add", "1e3", "2e2"])
        assert operands == [1000.0, 200.0]

    def test_parse_zero_operand(self, handler):
        """Test parsing zero as operand."""
        method_name, operands = handler.parse_args(["add", "0", "5"])
        assert operands == [0.0, 5.0]

    def test_parse_very_large_operand(self, handler):
        """Test parsing very large operand."""
        method_name, operands = handler.parse_args(["add", "999999999", "1"])
        assert operands[0] == 999999999.0


# ==============================================================================
# TESTS: CLIHandler.execute - Binary Operations
# ==============================================================================

class TestExecuteBinaryOps:
    """Test suite for execute method with binary operations."""

    def test_execute_add(self, handler):
        """Test execute dispatches add correctly."""
        result = handler.execute(["add", "2", "3"])
        assert result == 5.0

    def test_execute_subtract(self, handler):
        """Test execute dispatches subtract correctly."""
        result = handler.execute(["subtract", "10", "3"])
        assert result == 7.0

    def test_execute_multiply(self, handler):
        """Test execute dispatches multiply correctly."""
        result = handler.execute(["multiply", "5", "6"])
        assert result == 30.0

    def test_execute_divide(self, handler):
        """Test execute dispatches divide correctly."""
        result = handler.execute(["divide", "12", "3"])
        assert result == 4.0

    def test_execute_power(self, handler):
        """Test execute dispatches power correctly."""
        result = handler.execute(["power", "2", "3"])
        assert result == 8.0

    def test_execute_add_symbol(self, handler):
        """Test execute with + symbol."""
        result = handler.execute(["+", "2", "3"])
        assert result == 5.0

    def test_execute_subtract_symbol(self, handler):
        """Test execute with - symbol."""
        result = handler.execute(["-", "10", "3"])
        assert result == 7.0

    def test_execute_multiply_symbol(self, handler):
        """Test execute with * symbol."""
        result = handler.execute(["*", "5", "6"])
        assert result == 30.0

    def test_execute_divide_symbol(self, handler):
        """Test execute with / symbol."""
        result = handler.execute(["/", "12", "3"])
        assert result == 4.0

    def test_execute_power_symbol(self, handler):
        """Test execute with ^ symbol."""
        result = handler.execute(["^", "2", "3"])
        assert result == 8.0


# ==============================================================================
# TESTS: CLIHandler.execute - Unary Operations
# ==============================================================================

class TestExecuteUnaryOps:
    """Test suite for execute method with unary operations."""

    def test_execute_factorial(self, handler):
        """Test execute dispatches factorial correctly."""
        result = handler.execute(["factorial", "5"])
        assert result == 120

    def test_execute_square(self, handler):
        """Test execute dispatches square correctly."""
        result = handler.execute(["square", "4"])
        assert result == 16.0

    def test_execute_cube(self, handler):
        """Test execute dispatches cube correctly."""
        result = handler.execute(["cube", "3"])
        assert result == 27.0

    def test_execute_square_root(self, handler):
        """Test execute dispatches square_root correctly."""
        result = handler.execute(["square_root", "16"])
        assert result == 4.0

    def test_execute_square_root_symbol(self, handler):
        """Test execute with sqrt symbol."""
        result = handler.execute(["sqrt", "16"])
        assert result == 4.0

    def test_execute_cube_root(self, handler):
        """Test execute dispatches cube_root correctly."""
        result = handler.execute(["cube_root", "8"])
        assert result == 2.0

    def test_execute_cube_root_symbol(self, handler):
        """Test execute with cbrt symbol."""
        result = handler.execute(["cbrt", "8"])
        assert result == 2.0

    def test_execute_natural_logarithm(self, handler):
        """Test execute dispatches natural_logarithm correctly."""
        result = handler.execute(["natural_logarithm", "2.718281828"])
        assert abs(result - 1.0) < 0.01

    def test_execute_natural_logarithm_symbol(self, handler):
        """Test execute with ln symbol."""
        result = handler.execute(["ln", "2.718281828"])
        assert abs(result - 1.0) < 0.01


# ==============================================================================
# TESTS: CLIHandler.execute - Logarithm (Special Two-Argument Case)
# ==============================================================================

class TestExecuteLogarithm:
    """Test suite for execute with logarithm (special math.log handling)."""

    def test_execute_logarithm_by_name(self, handler):
        """Test execute logarithm by name."""
        result = handler.execute(["logarithm", "8", "2"])
        assert result == 3.0

    def test_execute_logarithm_by_symbol(self, handler):
        """Test execute logarithm by symbol."""
        result = handler.execute(["log", "8", "2"])
        assert result == 3.0

    def test_execute_logarithm_base_10(self, handler):
        """Test execute logarithm base 10."""
        result = handler.execute(["log", "100", "10"])
        assert result == 2.0

    def test_execute_logarithm_base_e(self, handler):
        """Test execute logarithm base e."""
        result = handler.execute(["log", str(math.e), str(math.e)])
        assert abs(result - 1.0) < 0.001

    def test_execute_logarithm_invalid_base_zero(self, handler):
        """Test execute logarithm with base 0 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            handler.execute(["log", "8", "0"])
        assert "base must be positive and not equal to 1" in str(exc_info.value)

    def test_execute_logarithm_invalid_base_one(self, handler):
        """Test execute logarithm with base 1 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            handler.execute(["log", "8", "1"])
        assert "base must be positive and not equal to 1" in str(exc_info.value)

    def test_execute_logarithm_invalid_base_negative(self, handler):
        """Test execute logarithm with negative base raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            handler.execute(["log", "8", "-2"])
        assert "base must be positive and not equal to 1" in str(exc_info.value)

    def test_execute_logarithm_invalid_x_zero(self, handler):
        """Test execute logarithm with x=0 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            handler.execute(["log", "0", "2"])
        assert "not defined for non-positive values" in str(exc_info.value)

    def test_execute_logarithm_invalid_x_negative(self, handler):
        """Test execute logarithm with negative x raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            handler.execute(["log", "-5", "2"])
        assert "not defined for non-positive values" in str(exc_info.value)


# ==============================================================================
# TESTS: CLIHandler.execute - Error Handling
# ==============================================================================

class TestExecuteErrorHandling:
    """Test suite for execute error handling."""

    def test_execute_divide_by_zero(self, handler):
        """Test execute raises ZeroDivisionError on divide by zero."""
        with pytest.raises(ZeroDivisionError):
            handler.execute(["divide", "10", "0"])

    def test_execute_square_root_negative(self, handler):
        """Test execute raises ValueError on square root of negative."""
        with pytest.raises(ValueError) as exc_info:
            handler.execute(["square_root", "-4"])
        assert "not defined for negative values" in str(exc_info.value)

    def test_execute_factorial_non_integer(self, handler):
        """Test execute raises TypeError on factorial of non-integer float."""
        with pytest.raises(TypeError) as exc_info:
            handler.execute(["factorial", "2.5"])
        assert "only accepts integer values" in str(exc_info.value)

    def test_execute_factorial_negative(self, handler):
        """Test execute raises ValueError on factorial of negative."""
        with pytest.raises(ValueError) as exc_info:
            handler.execute(["factorial", "-5"])
        assert "not defined for negative values" in str(exc_info.value)

    def test_execute_natural_logarithm_negative(self, handler):
        """Test execute raises ValueError on ln of negative."""
        with pytest.raises(ValueError):
            handler.execute(["natural_logarithm", "-1"])

    def test_execute_natural_logarithm_zero(self, handler):
        """Test execute raises ValueError on ln of zero."""
        with pytest.raises(ValueError):
            handler.execute(["natural_logarithm", "0"])


# ==============================================================================
# TESTS: main() - REPL Mode (Backward Compatibility)
# ==============================================================================

class TestMainREPLMode:
    """Test suite for main() function in REPL mode."""

    def test_main_argv_empty_starts_repl(self):
        """Test that main(argv=[]) starts REPL mode."""
        from src.__main__ import main
        with patch("src.repl.REPLInterface.run") as mock_run:
            with patch("src.__main__.Calculator"):
                main(argv=[])
        mock_run.assert_called_once()

    def test_main_argv_repl_flag_starts_repl(self):
        """Test that main(argv=['--repl']) starts REPL mode."""
        from src.__main__ import main
        with patch("src.repl.REPLInterface.run") as mock_run:
            with patch("src.__main__.Calculator"):
                main(argv=["--repl"])
        mock_run.assert_called_once()

    def test_main_catches_eof_in_repl_mode(self):
        """Test that main() catches EOFError from REPL."""
        from src.__main__ import main
        with patch("src.repl.REPLInterface.run", side_effect=EOFError):
            # Should not raise
            main(argv=[])

    def test_main_catches_keyboard_interrupt_in_repl_mode(self):
        """Test that main() catches KeyboardInterrupt from REPL."""
        from src.__main__ import main
        with patch("src.repl.REPLInterface.run", side_effect=KeyboardInterrupt):
            # Should not raise
            main(argv=[])

    def test_main_prints_closed_on_eof(self, capsys):
        """Test that main() prints 'Calculator closed.' on EOFError."""
        from src.__main__ import main
        with patch("src.repl.REPLInterface.run", side_effect=EOFError):
            main(argv=[])
        captured = capsys.readouterr()
        assert "Calculator closed." in captured.out


# ==============================================================================
# TESTS: main() - CLI Mode / Argument Parsing
# ==============================================================================

class TestMainCLIMode:
    """Test suite for main() function in CLI mode."""

    def test_main_single_arg_prints_usage_and_exits_1(self, capsys):
        """Test that single arg (non-repl) prints usage and exits with code 1."""
        from src.__main__ import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv=["add"])
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Usage" in captured.err

    def test_main_two_args_cli_mode(self):
        """Test that two or more args triggers CLI mode."""
        from src.__main__ import main
        with patch("src.cli.CLIHandler.execute") as mock_execute:
            mock_execute.return_value = 5.0
            with pytest.raises(SystemExit) as exc_info:
                main(argv=["add", "2", "3"])
            assert exc_info.value.code == 0
            mock_execute.assert_called_once_with(["add", "2", "3"])


# ==============================================================================
# TESTS: main() - CLI Exit Codes
# ==============================================================================

class TestMainCLIExitCodes:
    """Test suite for main() exit codes in CLI mode."""

    def test_main_cli_success_exit_code_0(self, capsys):
        """Test CLI mode exits with code 0 on success."""
        from src.__main__ import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv=["add", "2", "3"])
        assert exc_info.value.code == 0

    def test_main_cli_unknown_operation_exit_code_2(self, capsys):
        """Test CLI mode exits with code 2 on unknown operation."""
        from src.__main__ import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv=["foobar", "2", "3"])
        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "Unknown operation" in captured.err

    def test_main_cli_invalid_operand_exit_code_3(self, capsys):
        """Test CLI mode exits with code 3 on invalid operands."""
        from src.__main__ import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv=["add", "abc", "3"])
        assert exc_info.value.code == 3
        captured = capsys.readouterr()
        assert "Invalid number" in captured.err

    def test_main_cli_missing_operand_exit_code_3(self, capsys):
        """Test CLI mode exits with code 3 on missing operands."""
        from src.__main__ import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv=["add", "2"])
        assert exc_info.value.code == 3
        captured = capsys.readouterr()
        assert "Missing operand" in captured.err

    def test_main_cli_divide_by_zero_exit_code_4(self, capsys):
        """Test CLI mode exits with code 4 on divide by zero."""
        from src.__main__ import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv=["divide", "10", "0"])
        assert exc_info.value.code == 4
        captured = capsys.readouterr()
        assert "Error" in captured.err

    def test_main_cli_math_domain_error_exit_code_3(self, capsys):
        """Test CLI mode exits with code 3 on math domain error from Calculator."""
        from src.__main__ import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv=["square_root", "-4"])
        # ValueError from Calculator (domain error) exits with code 3
        assert exc_info.value.code == 3
        captured = capsys.readouterr()
        assert "Error" in captured.err


# ==============================================================================
# TESTS: Subprocess Integration (Full End-to-End CLI)
# ==============================================================================

class TestSubprocessCLI:
    """Test suite for CLI invocation via subprocess."""

    def test_cli_subprocess_add(self, repo_root):
        """Test CLI via subprocess: add 2 3."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "add", "2", "3"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 5.0

    def test_cli_subprocess_subtract(self, repo_root):
        """Test CLI via subprocess: subtract 10 3."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "subtract", "10", "3"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 7.0

    def test_cli_subprocess_multiply(self, repo_root):
        """Test CLI via subprocess: multiply 5 6."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "multiply", "5", "6"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 30.0

    def test_cli_subprocess_divide(self, repo_root):
        """Test CLI via subprocess: divide 12 3."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "divide", "12", "3"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 4.0

    def test_cli_subprocess_power(self, repo_root):
        """Test CLI via subprocess: power 2 3."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "power", "2", "3"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 8.0

    def test_cli_subprocess_factorial(self, repo_root):
        """Test CLI via subprocess: factorial 5."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "factorial", "5"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 120.0

    def test_cli_subprocess_square(self, repo_root):
        """Test CLI via subprocess: square 4."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "square", "4"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 16.0

    def test_cli_subprocess_cube(self, repo_root):
        """Test CLI via subprocess: cube 3."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "cube", "3"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 27.0

    def test_cli_subprocess_square_root(self, repo_root):
        """Test CLI via subprocess: square_root 16."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "square_root", "16"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 4.0

    def test_cli_subprocess_square_root_symbol(self, repo_root):
        """Test CLI via subprocess: sqrt 16."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "sqrt", "16"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 4.0

    def test_cli_subprocess_cube_root(self, repo_root):
        """Test CLI via subprocess: cube_root 8."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "cube_root", "8"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 2.0

    def test_cli_subprocess_cube_root_symbol(self, repo_root):
        """Test CLI via subprocess: cbrt 8."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "cbrt", "8"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 2.0

    def test_cli_subprocess_natural_logarithm(self, repo_root):
        """Test CLI via subprocess: natural_logarithm 2.718281828."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "natural_logarithm", "2.718281828"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        output = float(result.stdout.strip())
        assert abs(output - 1.0) < 0.01

    def test_cli_subprocess_natural_logarithm_symbol(self, repo_root):
        """Test CLI via subprocess: ln 2.718281828."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "ln", "2.718281828"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        output = float(result.stdout.strip())
        assert abs(output - 1.0) < 0.01

    def test_cli_subprocess_logarithm(self, repo_root):
        """Test CLI via subprocess: logarithm 8 2."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "logarithm", "8", "2"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 3.0

    def test_cli_subprocess_logarithm_symbol(self, repo_root):
        """Test CLI via subprocess: log 8 2."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "log", "8", "2"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 3.0


# ==============================================================================
# TESTS: Subprocess Symbol Aliases
# ==============================================================================

class TestSubprocessSymbolAliases:
    """Test suite for symbol aliases via subprocess."""

    def test_cli_subprocess_symbol_plus(self, repo_root):
        """Test CLI via subprocess: + 1 1."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "+", "1", "1"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 2.0

    def test_cli_subprocess_symbol_minus(self, repo_root):
        """Test CLI via subprocess: - 10 3."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "-", "10", "3"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 7.0

    def test_cli_subprocess_symbol_star(self, repo_root):
        """Test CLI via subprocess: * 5 6."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "*", "5", "6"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 30.0

    def test_cli_subprocess_symbol_slash(self, repo_root):
        """Test CLI via subprocess: / 12 3."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "/", "12", "3"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 4.0

    def test_cli_subprocess_symbol_caret(self, repo_root):
        """Test CLI via subprocess: ^ 2 3."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "^", "2", "3"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 8.0


# ==============================================================================
# TESTS: Subprocess Numeric Variants
# ==============================================================================

class TestSubprocessNumericVariants:
    """Test suite for numeric variants via subprocess."""

    def test_cli_subprocess_float_operands(self, repo_root):
        """Test CLI via subprocess with float operands."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "add", "1.5", "2.5"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == 4.0

    def test_cli_subprocess_negative_operands(self, repo_root):
        """Test CLI via subprocess with negative operands."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "add", "-1", "-2"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert float(result.stdout.strip()) == -3.0


# ==============================================================================
# TESTS: Subprocess Error Handling
# ==============================================================================

class TestSubprocessErrorHandling:
    """Test suite for error handling via subprocess."""

    def test_cli_subprocess_divide_by_zero_exit_4(self, repo_root):
        """Test CLI via subprocess: divide by zero exits with code 4."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "divide", "10", "0"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 4
        assert "Error" in result.stderr

    def test_cli_subprocess_unknown_operation_exit_2(self, repo_root):
        """Test CLI via subprocess: unknown operation exits with code 2."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "foobar", "2", "3"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 2
        assert "Unknown operation" in result.stderr

    def test_cli_subprocess_invalid_operand_exit_3(self, repo_root):
        """Test CLI via subprocess: invalid operand exits with code 3."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "add", "abc", "3"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 3
        assert "Invalid number" in result.stderr

    def test_cli_subprocess_missing_operand_exit_code(self, repo_root):
        """Test CLI via subprocess: missing operand exits with code 3."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "add", "2"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 3
        assert "Missing operand" in result.stderr

    def test_cli_subprocess_square_root_negative_exit_3(self, repo_root):
        """Test CLI via subprocess: square root of negative exits with code 3."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "square_root", "-4"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        # ValueError from Calculator (domain error) exits with code 3
        assert result.returncode == 3
        assert "Error" in result.stderr

    def test_cli_subprocess_error_to_stderr(self, repo_root):
        """Test CLI via subprocess: error messages go to stderr."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "divide", "10", "0"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 4
        assert result.stderr != ""
        assert "Error" in result.stderr

    def test_cli_subprocess_success_to_stdout(self, repo_root):
        """Test CLI via subprocess: successful result goes to stdout."""
        result = subprocess.run(
            [sys.executable, "-m", "src", "add", "2", "3"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "5.0"
        assert result.stderr == ""


# ==============================================================================
# TESTS: Edge Cases and Special Scenarios
# ==============================================================================

class TestEdgeCasesAndSpecial:
    """Test suite for edge cases and special scenarios."""

    def test_parse_args_with_spaces_in_operands(self, handler):
        """Test that spaces around operands are handled correctly."""
        # Spaces in the operand strings should be stripped when parsed as floats
        method_name, operands = handler.parse_args(["add", " 2 ", " 3 "])
        assert operands == [2.0, 3.0]

    def test_execute_with_very_large_numbers(self, handler):
        """Test execute with very large numbers."""
        result = handler.execute(["add", "999999999", "1"])
        assert result == 1000000000.0

    def test_execute_power_with_fractional_exponent(self, handler):
        """Test power with fractional exponent."""
        result = handler.execute(["power", "4", "0.5"])
        assert abs(result - 2.0) < 0.0001

    def test_execute_cube_root_negative(self, handler):
        """Test cube root of negative number."""
        result = handler.execute(["cube_root", "-8"])
        assert abs(result - (-2.0)) < 0.0001

    def test_execute_factorial_zero(self, handler):
        """Test factorial of zero."""
        result = handler.execute(["factorial", "0"])
        assert result == 1

    def test_execute_factorial_one(self, handler):
        """Test factorial of one."""
        result = handler.execute(["factorial", "1"])
        assert result == 1

    def test_execute_square_zero(self, handler):
        """Test square of zero."""
        result = handler.execute(["square", "0"])
        assert result == 0.0

    def test_execute_divide_fractional_result(self, handler):
        """Test division with fractional result."""
        result = handler.execute(["divide", "10", "3"])
        assert abs(result - (10/3)) < 0.0001


# ==============================================================================
# TESTS: Main function with None argv (default sys.argv)
# ==============================================================================

class TestMainWithNoneArgv:
    """Test suite for main() with argv=None."""

    def test_main_none_argv_uses_sys_argv(self):
        """Test that main(argv=None) uses sys.argv[1:]."""
        from src.__main__ import main
        # Patch sys.argv to simulate command-line args
        with patch("sys.argv", ["prog", "add", "2", "3"]):
            with patch("src.cli.CLIHandler.execute") as mock_execute:
                mock_execute.return_value = 5.0
                with pytest.raises(SystemExit) as exc_info:
                    main(argv=None)
                assert exc_info.value.code == 0
                mock_execute.assert_called_once_with(["add", "2", "3"])

    def test_main_none_argv_empty_sys_argv_starts_repl(self):
        """Test that main(argv=None) starts REPL when sys.argv has no extra args."""
        from src.__main__ import main
        with patch("sys.argv", ["prog"]):
            with patch("src.repl.REPLInterface.run") as mock_run:
                with patch("src.__main__.Calculator"):
                    main(argv=None)
            mock_run.assert_called_once()
