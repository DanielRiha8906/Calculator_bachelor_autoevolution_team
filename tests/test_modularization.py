"""
Comprehensive test suite for calculator modularization refactor (Issue #405).

This module tests the new modular structure for the calculator with separated concerns:
- Core calculation logic in src.calculator.core.Calculator
- Operation registry and abstract base classes in src.calculator.operations
- Specific operation implementations in src.calculator.operations.arithmetic and .scientific
- Input validation in src.calculator.validation
- Input handling in src.calculator.input_handler
- Persistence in src.calculator.persistence
- Main entry point in src.calculator.main

All tests are written before implementation and will fail until the modular structure is created.
"""

import pytest
import math
import sys
import subprocess
from pathlib import Path


# ============================================================================
# GROUP A: Module Imports (8 tests)
# ============================================================================

class TestModuleImports:
    """Test that all new modular components can be imported."""

    def test_calculator_core_imports(self):
        """Verify Calculator can be imported from src.calculator.core."""
        from src.calculator.core import Calculator
        assert Calculator is not None

    def test_operations_base_class_exists(self):
        """Verify Operation and OperationRegistry can be imported."""
        from src.calculator.operations import Operation, OperationRegistry
        assert Operation is not None
        assert OperationRegistry is not None

    def test_arithmetic_operations_module(self):
        """Verify all arithmetic operation classes can be imported."""
        from src.calculator.operations.arithmetic import (
            ArithmeticAdd,
            ArithmeticSubtract,
            ArithmeticMultiply,
            ArithmeticDivide,
            ArithmeticFactorial,
            ArithmeticModulo,
        )
        assert all(
            cls is not None
            for cls in [
                ArithmeticAdd,
                ArithmeticSubtract,
                ArithmeticMultiply,
                ArithmeticDivide,
                ArithmeticFactorial,
                ArithmeticModulo,
            ]
        )

    def test_scientific_operations_module(self):
        """Verify all scientific operation classes can be imported."""
        from src.calculator.operations.scientific import (
            ScientificSquare,
            ScientificCube,
            ScientificSquareRoot,
            ScientificCubeRoot,
            ScientificPower,
            ScientificLog10,
            ScientificLn,
        )
        assert all(
            cls is not None
            for cls in [
                ScientificSquare,
                ScientificCube,
                ScientificSquareRoot,
                ScientificCubeRoot,
                ScientificPower,
                ScientificLog10,
                ScientificLn,
            ]
        )

    def test_validation_module(self):
        """Verify InputValidator can be imported."""
        from src.calculator.validation import InputValidator
        assert InputValidator is not None

    def test_input_handler_module(self):
        """Verify CLIInput and InteractiveInput can be imported."""
        from src.calculator.input_handler import CLIInput, InteractiveInput
        assert CLIInput is not None
        assert InteractiveInput is not None

    def test_persistence_module(self):
        """Verify OperationHistory and ErrorLog can be imported."""
        from src.calculator.persistence import OperationHistory, ErrorLog
        assert OperationHistory is not None
        assert ErrorLog is not None

    def test_main_entry_point(self):
        """Verify main and cli_mode can be imported from src.calculator.main."""
        from src.calculator.main import main, cli_mode
        assert main is not None
        assert cli_mode is not None


# ============================================================================
# GROUP B: Registry Pattern (5 tests)
# ============================================================================

class TestRegistryPattern:
    """Test the OperationRegistry pattern."""

    def test_registry_initialization(self):
        """Verify OperationRegistry can be instantiated and operations registered."""
        from src.calculator.operations import OperationRegistry
        from src.calculator.operations.arithmetic import ArithmeticAdd

        registry = OperationRegistry()
        registry.register(ArithmeticAdd())
        assert registry is not None

    def test_registry_lookup(self):
        """Verify operations can be retrieved from registry."""
        from src.calculator.operations import OperationRegistry
        from src.calculator.operations.arithmetic import ArithmeticAdd

        registry = OperationRegistry()
        registry.register(ArithmeticAdd())
        op = registry.get("add")
        assert op is not None

    def test_registry_arity_validation(self):
        """Verify registry correctly tracks operation arity."""
        from src.calculator.operations import OperationRegistry
        from src.calculator.operations.arithmetic import ArithmeticAdd
        from src.calculator.operations.scientific import ScientificSquareRoot

        registry = OperationRegistry()
        registry.register(ArithmeticAdd())
        registry.register(ScientificSquareRoot())
        assert registry.get("add").arity == 2
        assert registry.get("square_root").arity == 1

    def test_registry_all_operations_registered(self):
        """Verify registry contains all 12+ operations."""
        from src.calculator.main import _build_registry

        registry = _build_registry()
        ops = registry.list_all()
        assert len(ops) >= 12

    def test_registry_operation_execution(self):
        """Verify operations execute correctly through registry."""
        from src.calculator.operations import OperationRegistry
        from src.calculator.operations.arithmetic import ArithmeticAdd

        registry = OperationRegistry()
        registry.register(ArithmeticAdd())
        result = registry.get("add").execute(5, 3)
        assert result == 8


# ============================================================================
# GROUP C: Operation Class Hierarchy (6 tests)
# ============================================================================

class TestOperationClassHierarchy:
    """Test the Operation base class and implementations."""

    def test_operation_base_class_interface(self):
        """Verify Operation is abstract and cannot be instantiated directly."""
        import inspect
        from src.calculator.operations import Operation

        assert inspect.isabstract(Operation)

    def test_arithmetic_add_instance(self):
        """Verify ArithmeticAdd operation works."""
        from src.calculator.operations.arithmetic import ArithmeticAdd

        assert ArithmeticAdd().execute(5, 3) == 8

    def test_arithmetic_divide_by_zero(self):
        """Verify ArithmeticDivide raises ZeroDivisionError for zero divisor."""
        from src.calculator.operations.arithmetic import ArithmeticDivide

        with pytest.raises(ZeroDivisionError):
            ArithmeticDivide().execute(5, 0)

    def test_scientific_square_root_negative(self):
        """Verify ScientificSquareRoot raises ValueError for negative input."""
        from src.calculator.operations.scientific import ScientificSquareRoot

        with pytest.raises(ValueError):
            ScientificSquareRoot().execute(-4)

    def test_scientific_ln_positive(self):
        """Verify ScientificLn returns correct value for e."""
        from src.calculator.operations.scientific import ScientificLn

        result = ScientificLn().execute(math.e)
        assert result == pytest.approx(1.0)

    def test_operation_arity_property(self):
        """Verify operations have correct arity property."""
        from src.calculator.operations.arithmetic import ArithmeticAdd
        from src.calculator.operations.scientific import ScientificSquareRoot

        assert ArithmeticAdd().arity == 2
        assert ScientificSquareRoot().arity == 1


# ============================================================================
# GROUP D: Validation (4 tests)
# ============================================================================

class TestValidation:
    """Test the InputValidator for parsing and validation."""

    def test_parse_number_integer(self):
        """Verify parsing of integer string."""
        from src.calculator.validation import InputValidator

        result = InputValidator.parse_number("42")
        assert result == 42

    def test_parse_number_float(self):
        """Verify parsing of float string."""
        from src.calculator.validation import InputValidator

        result = InputValidator.parse_number("3.14")
        assert result == pytest.approx(3.14)

    def test_parse_number_negative(self):
        """Verify parsing of negative number string."""
        from src.calculator.validation import InputValidator

        result = InputValidator.parse_number("-25")
        assert result == -25

    def test_parse_number_invalid(self):
        """Verify that invalid strings raise ValueError."""
        from src.calculator.validation import InputValidator

        with pytest.raises(ValueError):
            InputValidator.parse_number("abc")


# ============================================================================
# GROUP E: Input Handlers (6 tests)
# ============================================================================

class TestInputHandlers:
    """Test CLIInput and InteractiveInput handlers."""

    def test_cli_input_init(self):
        """Verify CLIInput can be instantiated."""
        from src.calculator.input_handler import CLIInput

        cli = CLIInput(["prog", "add", "5", "3"])
        assert cli is not None

    def test_cli_input_has_args(self):
        """Verify CLIInput detects when operation args are present."""
        from src.calculator.input_handler import CLIInput

        cli = CLIInput(["prog", "add", "5", "3"])
        assert cli.has_operation_args() == True

    def test_cli_input_no_args(self):
        """Verify CLIInput detects when operation args are absent."""
        from src.calculator.input_handler import CLIInput

        cli = CLIInput(["prog"])
        assert cli.has_operation_args() == False

    def test_cli_input_get_operation_and_operands(self):
        """Verify CLIInput extracts operation name and operands."""
        from src.calculator.input_handler import CLIInput

        cli = CLIInput(["prog", "divide", "10", "2"])
        op, operands = cli.get_operation_and_operands()
        assert op == "divide"
        assert operands == ["10", "2"]

    def test_interactive_input_reads_stdin(self, monkeypatch):
        """Verify InteractiveInput can read operation from input."""
        from src.calculator.input_handler import InteractiveInput

        handler = InteractiveInput()
        with monkeypatch.context() as m:
            m.setattr("builtins.input", lambda _: "add")
            result = handler.read_operation()
        assert result == "add"

    def test_interactive_input_reads_operand(self, monkeypatch):
        """Verify InteractiveInput can read operand from input."""
        from src.calculator.input_handler import InteractiveInput

        handler = InteractiveInput()
        with monkeypatch.context() as m:
            m.setattr("builtins.input", lambda _: "5")
            result = handler.read_operand("First number")
        assert result == "5"


# ============================================================================
# GROUP F: Persistence (2 tests)
# ============================================================================

class TestPersistence:
    """Test persistence modules."""

    def test_operation_history_imported(self):
        """Verify OperationHistory can be imported."""
        from src.calculator.persistence import OperationHistory

        assert OperationHistory is not None

    def test_error_log_imported(self):
        """Verify ErrorLog can be imported."""
        from src.calculator.persistence import ErrorLog

        assert ErrorLog is not None


# ============================================================================
# GROUP G: Core Calculator (4 tests)
# ============================================================================

class TestCoreCalculator:
    """Test that the core Calculator has all required methods."""

    def test_core_calculator_has_methods(self):
        """Verify Calculator has all 12 operation methods."""
        from src.calculator.core import Calculator

        calc = Calculator()
        methods = [
            "add",
            "subtract",
            "multiply",
            "divide",
            "factorial",
            "square",
            "cube",
            "square_root",
            "cube_root",
            "power",
            "log10",
            "ln",
        ]
        for method in methods:
            assert hasattr(calc, method), f"Missing method: {method}"

    def test_core_calculator_add_still_works(self):
        """Verify Calculator.add() still works correctly."""
        from src.calculator.core import Calculator

        assert Calculator().add(2, 3) == 5

    def test_core_calculator_square_root_still_works(self):
        """Verify Calculator.square_root() still works correctly."""
        from src.calculator.core import Calculator

        assert Calculator().square_root(9) == 3.0

    def test_core_calculator_factorial_still_works(self):
        """Verify Calculator.factorial() still works correctly."""
        from src.calculator.core import Calculator

        assert Calculator().factorial(5) == 120


# ============================================================================
# GROUP H: End-to-End (4 tests)
# ============================================================================

class TestEndToEnd:
    """Test end-to-end CLI execution."""

    @pytest.mark.skip(
        reason="Subprocess test requires proper module installation"
    )
    def test_modular_cli_execution(self):
        """Verify CLI execution works with new modular structure."""
        repo_root = Path(__file__).parent.parent
        result = subprocess.run(
            [sys.executable, "-m", "src", "add", "10", "5"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
        )
        assert result.returncode == 0
        assert "15" in result.stdout

    @pytest.mark.skip(
        reason="Subprocess test requires proper module installation"
    )
    def test_modular_cli_domain_error(self):
        """Verify CLI rejects domain errors (e.g., sqrt(-1))."""
        repo_root = Path(__file__).parent.parent
        result = subprocess.run(
            [sys.executable, "-m", "src", "square_root", "-1"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
        )
        assert result.returncode != 0

    @pytest.mark.skip(
        reason="Subprocess test requires proper module installation"
    )
    def test_modular_interactive_sequence(self):
        """Verify interactive mode works with new modular structure."""
        repo_root = Path(__file__).parent.parent
        result = subprocess.run(
            [sys.executable, "-m", "src"],
            input="add\n5\n3\nquit\n",
            capture_output=True,
            text=True,
            cwd=str(repo_root),
        )
        assert "8" in result.stdout

    def test_modular_registry_all_12_operations(self):
        """Verify registry contains all 12 required operations."""
        from src.calculator.main import _build_registry

        registry = _build_registry()
        ops = registry.list_all()
        assert len(ops) >= 12
        required_ops = [
            "add",
            "subtract",
            "multiply",
            "divide",
            "factorial",
            "square",
            "cube",
            "square_root",
            "cube_root",
            "power",
            "log10",
            "ln",
        ]
        for name in required_ops:
            assert name in ops


# ============================================================================
# GROUP I: Backward Compatibility (2 tests)
# ============================================================================

class TestBackwardCompatibility:
    """Test that old import paths still work (backward compatibility)."""

    def test_old_import_calculator_still_works(self):
        """Verify Calculator can still be imported from src.calculator."""
        from src.calculator import Calculator

        assert Calculator is not None

    def test_old_import_main_from_src_still_works(self):
        """Verify main can still be imported from src.__main__."""
        from src.__main__ import main

        assert main is not None
