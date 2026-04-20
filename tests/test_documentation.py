"""Comprehensive tests validating documentation accuracy for the Calculator application.

This test suite verifies that:
1. README quick-start examples produce expected outputs via CLI
2. Operation table examples are correct
3. Documented error conditions actually occur
4. Module structure and imports work as documented
5. HistoryTracker and ErrorLogger APIs function as documented
6. All documentation files exist
7. MAX_VALIDATION_ATTEMPTS behavior is correct
8. history.txt and error.log files are created/managed as documented
"""

import subprocess
import sys
import os
import math
import tempfile
from pathlib import Path
from io import StringIO

import pytest

from src.core.calculator import Calculator
from src.support.history import HistoryTracker
from src.error_logger import ErrorLogger
from src.core.operations import get_operation_registry


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def calculator():
    """Provide a fresh Calculator instance for each test."""
    return Calculator()


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for file-based tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        old_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            yield Path(tmpdir)
        finally:
            os.chdir(old_cwd)


# ============================================================================
# 1. Quick Start Examples from README
# ============================================================================


class TestReadmeQuickStartExamples:
    """Test examples from the README quick-start section."""

    def test_readme_add_example(self):
        """Test: python main.py add 3 4 → outputs 7"""
        result = subprocess.run(
            [sys.executable, "main.py", "add", "3", "4"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "7" in result.stdout
        # Output should be the bare result
        assert result.stdout.strip() == "7"

    def test_readme_factorial_example(self):
        """Test: python main.py factorial 5 → outputs 120"""
        result = subprocess.run(
            [sys.executable, "main.py", "factorial", "5"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "120" in result.stdout

    def test_readme_square_root_example(self):
        """Test: python main.py square_root 9 → outputs 3.0"""
        result = subprocess.run(
            [sys.executable, "main.py", "square_root", "9"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "3" in result.stdout

    def test_readme_power_example(self):
        """Test: python main.py power 2 10 → outputs 1024"""
        result = subprocess.run(
            [sys.executable, "main.py", "power", "2", "10"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "1024" in result.stdout

    def test_readme_log_example(self):
        """Test: python main.py log 100 → outputs 2.0"""
        result = subprocess.run(
            [sys.executable, "main.py", "log", "100"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "2" in result.stdout


# ============================================================================
# 2. Operation Table Examples - All 12 Operations
# ============================================================================


class TestOperationTableExamples:
    """Test all examples from the Supported Operations table in README."""

    def test_add_3_4_equals_7(self):
        """add 3 4 → 7"""
        result = subprocess.run(
            [sys.executable, "main.py", "add", "3", "4"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0
        assert "7" in result.stdout

    def test_subtract_10_3_equals_7(self):
        """subtract 10 3 → 7"""
        result = subprocess.run(
            [sys.executable, "main.py", "subtract", "10", "3"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0
        assert "7" in result.stdout

    def test_multiply_3_4_equals_12(self):
        """multiply 3 4 → 12"""
        result = subprocess.run(
            [sys.executable, "main.py", "multiply", "3", "4"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0
        assert "12" in result.stdout

    def test_divide_10_2_equals_5(self):
        """divide 10 2 → 5.0"""
        result = subprocess.run(
            [sys.executable, "main.py", "divide", "10", "2"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0
        assert "5" in result.stdout

    def test_power_2_10_equals_1024(self):
        """power 2 10 → 1024"""
        result = subprocess.run(
            [sys.executable, "main.py", "power", "2", "10"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0
        assert "1024" in result.stdout

    def test_factorial_5_equals_120(self):
        """factorial 5 → 120"""
        result = subprocess.run(
            [sys.executable, "main.py", "factorial", "5"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0
        assert "120" in result.stdout

    def test_square_4_equals_16(self):
        """square 4 → 16"""
        result = subprocess.run(
            [sys.executable, "main.py", "square", "4"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0
        assert "16" in result.stdout

    def test_cube_3_equals_27(self):
        """cube 3 → 27"""
        result = subprocess.run(
            [sys.executable, "main.py", "cube", "3"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0
        assert "27" in result.stdout

    def test_square_root_9_equals_3(self):
        """square_root 9 → 3.0"""
        result = subprocess.run(
            [sys.executable, "main.py", "square_root", "9"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0
        assert "3" in result.stdout

    def test_cube_root_8_equals_2(self):
        """cube_root 8 → 2.0"""
        result = subprocess.run(
            [sys.executable, "main.py", "cube_root", "8"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0
        assert "2" in result.stdout

    def test_cube_root_negative_8_equals_negative_2(self):
        """cube_root -8 → -2.0 (from README table)"""
        result = subprocess.run(
            [sys.executable, "main.py", "cube_root", "-8"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0
        assert "-2" in result.stdout

    def test_log_100_equals_2(self):
        """log 100 → 2.0"""
        result = subprocess.run(
            [sys.executable, "main.py", "log", "100"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0
        assert "2" in result.stdout

    def test_ln_1_equals_0(self):
        """ln 1 → 0.0"""
        result = subprocess.run(
            [sys.executable, "main.py", "ln", "1"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 0
        assert "0" in result.stdout


# ============================================================================
# 3. Domain Constraint Error Conditions
# ============================================================================


class TestErrorDomainConditions:
    """Test that documented domain constraint errors actually occur."""

    def test_divide_by_zero_error(self):
        """divide 10 0 → exit code 1 with error message"""
        result = subprocess.run(
            [sys.executable, "main.py", "divide", "10", "0"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 1
        assert "Error" in result.stderr or "division" in result.stderr.lower()

    def test_square_root_negative_error(self):
        """square_root -1 → exit code 1"""
        result = subprocess.run(
            [sys.executable, "main.py", "square_root", "-1"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 1
        assert "Error" in result.stderr

    def test_factorial_negative_error(self):
        """factorial -1 → exit code 1"""
        result = subprocess.run(
            [sys.executable, "main.py", "factorial", "-1"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 1
        assert "Error" in result.stderr

    def test_log_zero_error(self):
        """log 0 → exit code 1"""
        result = subprocess.run(
            [sys.executable, "main.py", "log", "0"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 1
        assert "Error" in result.stderr

    def test_ln_negative_error(self):
        """ln -1 → exit code 1"""
        result = subprocess.run(
            [sys.executable, "main.py", "ln", "-1"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 1
        assert "Error" in result.stderr

    def test_ln_zero_error(self):
        """ln 0 → exit code 1"""
        result = subprocess.run(
            [sys.executable, "main.py", "ln", "0"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 1
        assert "Error" in result.stderr


# ============================================================================
# 4. Calculator Class API - Direct Import Tests
# ============================================================================


class TestCalculatorClassAPI:
    """Test Calculator API by direct import and instantiation."""

    def test_add_direct(self, calculator):
        """Calculator.add() works directly."""
        assert calculator.add(3, 4) == 7

    def test_subtract_direct(self, calculator):
        """Calculator.subtract() works directly."""
        assert calculator.subtract(10, 3) == 7

    def test_multiply_direct(self, calculator):
        """Calculator.multiply() works directly."""
        assert calculator.multiply(3, 4) == 12

    def test_divide_direct(self, calculator):
        """Calculator.divide() works directly."""
        assert calculator.divide(10, 2) == 5.0

    def test_factorial_direct(self, calculator):
        """Calculator.factorial() works directly."""
        assert calculator.factorial(5) == 120

    def test_square_direct(self, calculator):
        """Calculator.square() works directly."""
        assert calculator.square(4) == 16

    def test_cube_direct(self, calculator):
        """Calculator.cube() works directly."""
        assert calculator.cube(3) == 27

    def test_square_root_direct(self, calculator):
        """Calculator.square_root() works directly."""
        assert calculator.square_root(9) == 3.0

    def test_cube_root_direct(self, calculator):
        """Calculator.cube_root() works directly."""
        result = calculator.cube_root(8)
        assert abs(result - 2.0) < 1e-9

    def test_cube_root_negative_direct(self, calculator):
        """Calculator.cube_root() handles negative inputs."""
        result = calculator.cube_root(-8)
        assert abs(result - (-2.0)) < 1e-9

    def test_power_direct(self, calculator):
        """Calculator.power() works directly."""
        assert calculator.power(2, 10) == 1024

    def test_log_direct(self, calculator):
        """Calculator.log() works directly."""
        assert calculator.log(100) == 2.0

    def test_ln_direct(self, calculator):
        """Calculator.ln() works directly."""
        assert calculator.ln(1) == 0.0

    def test_divide_by_zero_exception(self, calculator):
        """Calculator.divide(a, 0) raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)

    def test_square_root_negative_exception(self, calculator):
        """Calculator.square_root(-1) raises ValueError."""
        with pytest.raises(ValueError):
            calculator.square_root(-1)

    def test_factorial_negative_exception(self, calculator):
        """Calculator.factorial(-1) raises ValueError."""
        with pytest.raises(ValueError):
            calculator.factorial(-1)

    def test_log_zero_exception(self, calculator):
        """Calculator.log(0) raises ValueError."""
        with pytest.raises(ValueError):
            calculator.log(0)

    def test_ln_zero_exception(self, calculator):
        """Calculator.ln(0) raises ValueError."""
        with pytest.raises(ValueError):
            calculator.ln(0)

    def test_factorial_float_exception(self, calculator):
        """Calculator.factorial(5.5) raises TypeError."""
        with pytest.raises(TypeError):
            calculator.factorial(5.5)

    def test_square_string_exception(self, calculator):
        """Calculator.square('5') raises TypeError."""
        with pytest.raises(TypeError):
            calculator.square("5")

    def test_ln_string_exception(self, calculator):
        """Calculator.ln('5') raises TypeError."""
        with pytest.raises(TypeError):
            calculator.ln("5")


# ============================================================================
# 5. Module Structure and Imports
# ============================================================================


class TestModuleStructure:
    """Test that documented module structure and imports work."""

    def test_import_calculator_from_core(self):
        """Can import Calculator from src.core.calculator."""
        from src.core.calculator import Calculator as CalcCore
        assert CalcCore is not None
        calc = CalcCore()
        assert calc.add(1, 2) == 3

    def test_import_calculator_from_root_shim(self):
        """Can import Calculator from src.calculator (backward-compat shim)."""
        from src.calculator import Calculator as CalcShim
        assert CalcShim is not None
        calc = CalcShim()
        assert calc.add(1, 2) == 3

    def test_import_operations_manager(self):
        """Can import OperationRegistry from src.core.operations_manager."""
        from src.core.operations_manager import OperationRegistry
        assert OperationRegistry is not None

    def test_import_operations_factory(self):
        """Can import get_operation_registry from src.core.operations."""
        from src.core.operations import get_operation_registry
        assert get_operation_registry is not None

    def test_import_input_parser(self):
        """Can import parse_cli_args and convert_operand from src.interface.input_parser."""
        from src.interface.input_parser import parse_cli_args, convert_operand
        assert parse_cli_args is not None
        assert convert_operand is not None

    def test_import_output_formatter(self):
        """Can import format_result from src.interface.output_formatter."""
        from src.interface.output_formatter import format_result
        assert format_result is not None

    def test_import_menu_renderer(self):
        """Can import display_menu from src.interface.menu_renderer."""
        from src.interface.menu_renderer import display_menu
        assert display_menu is not None

    def test_import_session(self):
        """Can import run_interactive_session from src.interactive.session."""
        from src.interactive.session import run_interactive_session
        assert run_interactive_session is not None

    def test_import_history_tracker_from_support(self):
        """Can import HistoryTracker from src.support.history."""
        from src.support.history import HistoryTracker
        assert HistoryTracker is not None

    def test_import_history_tracker_from_shim(self):
        """Can import HistoryTracker from src.history (backward-compat shim)."""
        from src.history import HistoryTracker
        assert HistoryTracker is not None

    def test_import_error_logger(self):
        """Can import ErrorLogger from src.error_logger."""
        from src.error_logger import ErrorLogger
        assert ErrorLogger is not None

    def test_import_cli_functions(self):
        """Can import parse_arguments and execute_cli from src.cli."""
        from src.cli import parse_arguments, execute_cli
        assert parse_arguments is not None
        assert execute_cli is not None


# ============================================================================
# 6. HistoryTracker API Tests
# ============================================================================


class TestHistoryTrackerAPI:
    """Test HistoryTracker functionality as documented."""

    def test_history_tracker_record(self):
        """HistoryTracker.record() works."""
        tracker = HistoryTracker()
        tracker.record("add", [1, 2], 3)
        history = tracker.get_history()
        assert len(history) == 1
        assert "add(1, 2) = 3" in history

    def test_history_tracker_get_history(self):
        """HistoryTracker.get_history() returns a list copy."""
        tracker = HistoryTracker()
        tracker.record("factorial", [5], 120)
        history = tracker.get_history()
        assert isinstance(history, list)
        assert "factorial(5) = 120" in history

    def test_history_tracker_display_with_entries(self, capsys):
        """HistoryTracker.display() prints entries correctly."""
        tracker = HistoryTracker()
        tracker.record("add", [3, 4], 7)
        tracker.record("multiply", [2, 5], 10)
        tracker.display()
        captured = capsys.readouterr()
        assert "Session history:" in captured.out
        assert "add(3, 4) = 7" in captured.out
        assert "multiply(2, 5) = 10" in captured.out

    def test_history_tracker_display_empty(self, capsys):
        """HistoryTracker.display() handles empty history."""
        tracker = HistoryTracker()
        tracker.display()
        captured = capsys.readouterr()
        assert "No history for this session." in captured.out

    def test_history_tracker_save_to_file(self, temp_dir):
        """HistoryTracker.save_to_file() creates history.txt."""
        tracker = HistoryTracker()
        tracker.record("add", [3, 4], 7)
        tracker.record("factorial", [5], 120)
        tracker.save_to_file(str(temp_dir / "history.txt"))

        assert (temp_dir / "history.txt").exists()
        content = (temp_dir / "history.txt").read_text()
        assert "add(3, 4) = 7\n" in content
        assert "factorial(5) = 120\n" in content

    def test_history_tracker_save_to_file_default_path(self, temp_dir):
        """HistoryTracker.save_to_file() uses history.txt by default."""
        tracker = HistoryTracker()
        tracker.record("square", [4], 16)
        tracker.save_to_file()

        assert (temp_dir / "history.txt").exists()
        content = (temp_dir / "history.txt").read_text()
        assert "square(4) = 16" in content

    def test_history_tracker_clear(self):
        """HistoryTracker.clear() removes all entries."""
        tracker = HistoryTracker()
        tracker.record("add", [1, 2], 3)
        assert len(tracker.get_history()) == 1
        tracker.clear()
        assert len(tracker.get_history()) == 0

    def test_history_tracker_multiple_records(self):
        """HistoryTracker.record() accumulates multiple entries."""
        tracker = HistoryTracker()
        tracker.record("add", [1, 2], 3)
        tracker.record("subtract", [5, 3], 2)
        tracker.record("multiply", [2, 3], 6)
        history = tracker.get_history()
        assert len(history) == 3
        assert history[0] == "add(1, 2) = 3"
        assert history[1] == "subtract(5, 3) = 2"
        assert history[2] == "multiply(2, 3) = 6"


# ============================================================================
# 7. ErrorLogger API Tests
# ============================================================================


class TestErrorLoggerAPI:
    """Test ErrorLogger functionality as documented.

    Note: ErrorLogger is a singleton with module-level state. We test the
    core functionality but note that the file-writing behavior depends on
    module initialization state and CWD.
    """

    def test_error_logger_exists(self):
        """ErrorLogger class can be instantiated."""
        logger = ErrorLogger()
        assert logger is not None

    def test_error_logger_log_error_accepts_context(self):
        """ErrorLogger.log_error() accepts error type and context dict."""
        logger = ErrorLogger()
        # This should not raise an error
        logger.log_error(
            "TEST_ERROR",
            {
                "operation": "add",
                "operands": "1, 2",
                "message": "test error message",
            },
        )

    def test_error_logger_handles_sparse_context(self):
        """ErrorLogger.log_error() handles partial context dict."""
        logger = ErrorLogger()
        # Should not raise an error even with partial context
        logger.log_error("SPARSE_ERROR", {"message": "only message"})

    def test_error_logger_via_cli_creates_error_log(self):
        """Running CLI with an error creates error.log file."""
        # Use subprocess to test actual error logging behavior
        result = subprocess.run(
            [sys.executable, "main.py", "divide", "10", "0"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 1
        # Check that error.log was created
        error_log = Path("/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/error.log")
        assert error_log.exists(), "error.log should be created after CLI error"

    def test_error_log_contains_structured_entries(self):
        """error.log contains structured error entries."""
        # Trigger another error to append to the log
        result = subprocess.run(
            [sys.executable, "main.py", "factorial", "-1"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 1

        # Read the error log
        error_log = Path("/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/error.log")
        if error_log.exists():
            content = error_log.read_text()
            # Should contain pipe-separated structured format
            assert "|" in content


# ============================================================================
# 8. Documentation Files Existence
# ============================================================================


class TestDocumentationFilesExist:
    """Test that all documented documentation files exist."""

    def test_readme_exists(self):
        """README.md exists in project root."""
        readme = Path("/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/README.md")
        assert readme.exists(), "README.md not found"

    def test_user_guide_exists(self):
        """docs/USER_GUIDE.md exists."""
        user_guide = Path("/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/docs/USER_GUIDE.md")
        assert user_guide.exists(), "docs/USER_GUIDE.md not found"

    def test_developer_guide_exists(self):
        """docs/DEVELOPER_GUIDE.md exists."""
        dev_guide = Path("/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/docs/DEVELOPER_GUIDE.md")
        assert dev_guide.exists(), "docs/DEVELOPER_GUIDE.md not found"

    def test_architecture_guide_exists(self):
        """docs/ARCHITECTURE.md exists."""
        arch_guide = Path("/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/docs/ARCHITECTURE.md")
        assert arch_guide.exists(), "docs/ARCHITECTURE.md not found"

    def test_api_reference_exists(self):
        """docs/API_REFERENCE.md exists."""
        api_ref = Path("/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/docs/API_REFERENCE.md")
        assert api_ref.exists(), "docs/API_REFERENCE.md not found"


# ============================================================================
# 9. CLI Error Handling
# ============================================================================


class TestCLIErrorHandling:
    """Test documented CLI error handling behavior."""

    def test_no_arguments_exit_code_1(self):
        """main.py with no arguments exits with code 1."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 1

    def test_unknown_operation_exit_code_1(self):
        """main.py with unknown operation exits with code 1."""
        result = subprocess.run(
            [sys.executable, "main.py", "unknown_op", "5"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 1
        assert "Error" in result.stderr or "unknown" in result.stderr.lower()

    def test_invalid_operand_exit_code_1(self):
        """main.py with non-numeric operand exits with code 1."""
        result = subprocess.run(
            [sys.executable, "main.py", "add", "abc", "5"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 1
        assert "Error" in result.stderr

    def test_wrong_operand_count_exit_code_1(self):
        """main.py with wrong operand count exits with code 1."""
        result = subprocess.run(
            [sys.executable, "main.py", "add", "5"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team",
        )
        assert result.returncode == 1
        assert "Error" in result.stderr


# ============================================================================
# 10. Operation Registry
# ============================================================================


class TestOperationRegistry:
    """Test the operation registry as documented."""

    def test_registry_contains_all_operations(self):
        """Operation registry contains all 18 documented operations."""
        calc = Calculator()
        registry = get_operation_registry(calc)

        expected_ops = {
            "add", "subtract", "multiply", "divide",
            "factorial", "square", "cube",
            "square_root", "cube_root",
            "power", "log", "ln",
            "sin", "cos", "tan", "cot", "asin", "acos"
        }
        assert set(registry.keys()) == expected_ops

    def test_registry_operation_arity(self):
        """Operation registry returns correct arity for each operation."""
        calc = Calculator()
        registry = get_operation_registry(calc)

        # Binary operations
        binary_ops = {"add", "subtract", "multiply", "divide", "power"}
        for op in binary_ops:
            method, arity = registry[op]
            assert arity == 2, f"{op} should have arity 2, got {arity}"

        # Unary operations
        unary_ops = {"factorial", "square", "cube", "square_root", "cube_root", "log", "ln",
                     "sin", "cos", "tan", "cot", "asin", "acos"}
        for op in unary_ops:
            method, arity = registry[op]
            assert arity == 1, f"{op} should have arity 1, got {arity}"

    def test_registry_methods_are_callable(self):
        """Registry operations are callable calculator methods."""
        calc = Calculator()
        registry = get_operation_registry(calc)

        method, arity = registry["add"]
        result = method(3, 4)
        assert result == 7

    def test_registry_is_dict(self):
        """Operation registry is a dict."""
        calc = Calculator()
        registry = get_operation_registry(calc)
        assert isinstance(registry, dict)


# ============================================================================
# 11. Input/Output Handling
# ============================================================================


class TestInputOutputHandling:
    """Test documented input parsing and output formatting."""

    def test_convert_operand_integer_string(self):
        """convert_operand('3') returns int 3."""
        from src.interface.input_parser import convert_operand
        result = convert_operand("3")
        assert result == 3
        assert isinstance(result, int)

    def test_convert_operand_float_string(self):
        """convert_operand('3.5') returns float 3.5."""
        from src.interface.input_parser import convert_operand
        result = convert_operand("3.5")
        assert result == 3.5
        assert isinstance(result, float)

    def test_convert_operand_whole_number_float_string(self):
        """convert_operand('3.0') returns int 3."""
        from src.interface.input_parser import convert_operand
        result = convert_operand("3.0")
        assert result == 3
        assert isinstance(result, int)

    def test_convert_operand_invalid_raises_error(self):
        """convert_operand('abc') raises ValueError."""
        from src.interface.input_parser import convert_operand
        with pytest.raises(ValueError):
            convert_operand("abc")

    def test_parse_cli_args(self):
        """parse_cli_args() parses correctly."""
        from src.interface.input_parser import parse_cli_args
        op, operands = parse_cli_args(["add", "3", "4"])
        assert op == "add"
        assert operands == ["3", "4"]

    def test_format_result_integer(self):
        """format_result(7) formats integer correctly."""
        from src.interface.output_formatter import format_result
        result = format_result(7)
        assert "7" in str(result)

    def test_format_result_float(self):
        """format_result(3.5) formats float correctly."""
        from src.interface.output_formatter import format_result
        result = format_result(3.5)
        assert "3.5" in str(result)


# ============================================================================
# 12. Max Validation Attempts (from documentation)
# ============================================================================


class TestMaxValidationAttempts:
    """Test MAX_VALIDATION_ATTEMPTS constant."""

    def test_max_validation_attempts_constant_exists(self):
        """MAX_VALIDATION_ATTEMPTS is defined and equals 5."""
        from src.interactive.session import MAX_VALIDATION_ATTEMPTS
        assert MAX_VALIDATION_ATTEMPTS == 5

    def test_max_validation_attempts_imported_from_input_handler(self):
        """MAX_VALIDATION_ATTEMPTS can be imported from input_handler shim."""
        from src.input_handler import MAX_VALIDATION_ATTEMPTS
        assert MAX_VALIDATION_ATTEMPTS == 5


# ============================================================================
# 13. Edge Cases and Special Scenarios
# ============================================================================


class TestEdgeCasesAndSpecialScenarios:
    """Test edge cases and scenarios mentioned in documentation."""

    def test_factorial_zero(self, calculator):
        """factorial(0) returns 1."""
        assert calculator.factorial(0) == 1

    def test_factorial_one(self, calculator):
        """factorial(1) returns 1."""
        assert calculator.factorial(1) == 1

    def test_log_one(self, calculator):
        """log(1) returns 0.0."""
        assert calculator.log(1) == 0.0

    def test_ln_math_e(self, calculator):
        """ln(e) returns approximately 1.0."""
        result = calculator.ln(math.e)
        assert abs(result - 1.0) < 1e-9

    def test_power_zero_exponent(self, calculator):
        """power(5, 0) returns 1."""
        assert calculator.power(5, 0) == 1

    def test_power_one_exponent(self, calculator):
        """power(5, 1) returns 5."""
        assert calculator.power(5, 1) == 5

    def test_square_root_zero(self, calculator):
        """square_root(0) returns 0.0."""
        assert calculator.square_root(0) == 0.0

    def test_cube_root_zero(self, calculator):
        """cube_root(0) returns 0.0."""
        result = calculator.cube_root(0)
        assert abs(result) < 1e-9

    def test_square_negative(self, calculator):
        """square(-3) returns 9."""
        assert calculator.square(-3) == 9

    def test_cube_negative(self, calculator):
        """cube(-2) returns -8."""
        assert calculator.cube(-2) == -8

    def test_add_floats(self, calculator):
        """add(1.5, 2.5) returns 4.0."""
        result = calculator.add(1.5, 2.5)
        assert result == 4.0

    def test_divide_floats(self, calculator):
        """divide(10.0, 3.0) returns approximately 3.333..."""
        result = calculator.divide(10.0, 3.0)
        assert abs(result - (10.0 / 3.0)) < 1e-9

    def test_power_fractional_exponent(self, calculator):
        """power(9.0, 0.5) returns 3.0."""
        result = calculator.power(9.0, 0.5)
        assert abs(result - 3.0) < 1e-9

    def test_power_negative_base_integer_exponent(self, calculator):
        """power(-2, 3) returns -8."""
        assert calculator.power(-2, 3) == -8

    def test_power_negative_base_fractional_exponent_raises(self, calculator):
        """power(-2, 0.5) raises ValueError."""
        with pytest.raises(ValueError):
            calculator.power(-2, 0.5)

    def test_factorial_of_bool_true(self, calculator):
        """factorial(True) is accepted (True == 1)."""
        # Note: bool is subclass of int, so True == 1
        result = calculator.factorial(True)
        assert result == 1

    def test_factorial_of_bool_false(self, calculator):
        """factorial(False) is accepted (False == 0)."""
        # Note: bool is subclass of int, so False == 0
        result = calculator.factorial(False)
        assert result == 1  # 0! = 1
