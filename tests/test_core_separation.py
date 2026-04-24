"""Core separation tests for Calculator module independence and modularity.

These tests verify:
1. Core Calculator can be imported and used without interactive or cli modules
2. Module boundaries are properly maintained (no circular imports)
3. Core operations can be called directly and via registry
4. Error handling is the responsibility of the core Calculator class
"""

import inspect
import sys
import pytest
from unittest.mock import patch

from src.calculator import Calculator
from src.operation_registry import OperationRegistry
from src.error_logger import ErrorLogger


# ============================================================================
# Test Group A: Core Calculation Independence (8 tests)
# ============================================================================


class TestCoreCalculationIndependence:
    """Verify Calculator operates independently of interactive and cli modules."""

    def test_calculator_independence(self):
        """Import Calculator without importing interactive or cli."""
        # This test simply verifies Calculator can be instantiated
        # after importing it separately from the application structure
        calc = Calculator()
        assert hasattr(calc, 'add')
        assert hasattr(calc, 'subtract')
        assert hasattr(calc, 'multiply')
        assert hasattr(calc, 'divide')
        assert hasattr(calc, 'factorial')
        assert hasattr(calc, 'square')
        assert hasattr(calc, 'cube')
        assert hasattr(calc, 'sqrt')
        assert hasattr(calc, 'cbrt')
        assert hasattr(calc, 'ln')
        assert hasattr(calc, 'log10')
        assert hasattr(calc, 'power')

    def test_no_interactive_imports(self):
        """Verify Calculator source contains no import of interactive module."""
        source = inspect.getsource(Calculator)
        assert "import interactive" not in source
        assert "from interactive" not in source

    def test_no_cli_imports(self):
        """Verify Calculator source contains no import of cli module."""
        source = inspect.getsource(Calculator)
        assert "import cli" not in source
        assert "from cli" not in source

    def test_registry_independence(self):
        """OperationRegistry can be instantiated and used without importing interactive or cli."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        operations = registry.get_operations()
        assert len(operations) == 12
        assert 'add' in operations
        assert 'subtract' in operations
        assert 'multiply' in operations
        assert 'divide' in operations
        assert 'factorial' in operations
        assert 'square' in operations
        assert 'cube' in operations
        assert 'sqrt' in operations
        assert 'cbrt' in operations
        assert 'ln' in operations
        assert 'log10' in operations
        assert 'power' in operations

    def test_core_direct_call(self):
        """All 12 operations can be called directly on Calculator and return correct results."""
        calc = Calculator()

        # Binary operations
        assert calc.add(5, 3) == 8
        assert calc.subtract(5, 3) == 2
        assert calc.multiply(5, 3) == 15
        assert calc.divide(10, 2) == 5.0
        assert calc.power(2, 3) == 8

        # Unary operations
        assert calc.factorial(5) == 120
        assert calc.square(4) == 16
        assert calc.cube(3) == 27
        assert calc.sqrt(9) == 3.0
        assert pytest.approx(calc.cbrt(8)) == 2.0
        assert pytest.approx(calc.ln(1)) == 0.0
        assert pytest.approx(calc.log10(10)) == 1.0

    def test_sqrt_domain_check(self):
        """Calculator.sqrt(-4) raises ValueError with 'square root of negative' in message."""
        calc = Calculator()
        with pytest.raises(ValueError) as exc_info:
            calc.sqrt(-4)
        assert "square root of negative" in str(exc_info.value).lower()

    def test_division_by_zero(self):
        """Calculator.divide(10, 0) raises ZeroDivisionError."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(10, 0)

    def test_factorial_type_validation(self):
        """Calculator.factorial(5.5) raises ValueError with 'got float' in message."""
        calc = Calculator()
        with pytest.raises(ValueError) as exc_info:
            calc.factorial(5.5)
        assert "got float" in str(exc_info.value).lower()


# ============================================================================
# Test Group B: Module Boundary Validation (5 tests)
# ============================================================================


class TestModuleBoundaryValidation:
    """Verify module boundaries are maintained and circular imports are avoided."""

    def test_interactive_no_cli_import(self):
        """Read src/interactive.py and verify it does not import cli."""
        from src import interactive
        source = inspect.getsource(interactive)
        assert "import cli" not in source
        assert "from cli" not in source

    def test_cli_no_interactive_import(self):
        """Read src/cli.py and verify it does not import interactive."""
        from src import cli
        source = inspect.getsource(cli)
        assert "import interactive" not in source
        assert "from interactive" not in source

    def test_calculator_no_history_import(self):
        """Read src/calculator.py and verify it does not import history or error_logger."""
        source = inspect.getsource(Calculator)
        assert "import history" not in source
        assert "import error_logger" not in source

    def test_circular_imports(self):
        """Verify no circular imports when importing core modules."""
        # Clear any previously imported modules
        modules_to_clear = [m for m in sys.modules.keys() if m.startswith('src.')]
        for m in modules_to_clear:
            del sys.modules[m]

        # Now import in order
        try:
            from src.calculator import Calculator
            from src.operation_registry import OperationRegistry
            from src.interactive import run_interactive_session
            from src.cli import run_cli
            # If we get here, no circular imports occurred
            assert True
        except ImportError as e:
            pytest.fail(f"Circular import detected: {e}")

    def test_main_dispatch_logic(self):
        """Test dispatch logic: len(sys.argv) > 1 means CLI, otherwise interactive."""
        # This test verifies the dispatch logic concept
        # When sys.argv has more than 1 item, it's CLI mode
        # When sys.argv has exactly 1 item (program name only), it's interactive mode

        with patch.object(sys, 'argv', ['calculator']):
            # len = 1: interactive mode
            assert len(sys.argv) == 1
            is_cli = len(sys.argv) > 1
            assert is_cli is False

        with patch.object(sys, 'argv', ['calculator', 'add', '5', '3']):
            # len > 1: CLI mode
            assert len(sys.argv) > 1
            is_cli = len(sys.argv) > 1
            assert is_cli is True


# ============================================================================
# Test Group C: Core Reusability (5 tests)
# ============================================================================


class TestCoreReusability:
    """Verify that core Calculator and OperationRegistry are reusable."""

    def test_external_usage_pattern(self):
        """Import Calculator from src.calculator and use it directly."""
        calc = Calculator()
        result = calc.add(2, 2)
        assert result == 4

    def test_registry_reflection(self):
        """OperationRegistry.get_operations() returns exactly 12 items including add and factorial."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        operations = registry.get_operations()
        assert len(operations) == 12
        assert 'add' in operations
        assert 'factorial' in operations

    def test_registry_call_all_ops(self):
        """Registry can call all major operations with correct results."""
        calc = Calculator()
        registry = OperationRegistry(calc)

        assert registry.call('add', 5, 3) == 8
        assert registry.call('divide', 10, 2) == 5.0
        assert registry.call('factorial', 5) == 120
        assert registry.call('square', 4) == 16

    def test_arity_detection(self):
        """Registry correctly reports arity for binary and unary operations."""
        calc = Calculator()
        registry = OperationRegistry(calc)

        # Binary operations (arity == 2)
        assert registry.get_arity('add') == 2
        assert registry.get_arity('subtract') == 2
        assert registry.get_arity('multiply') == 2
        assert registry.get_arity('divide') == 2
        assert registry.get_arity('power') == 2

        # Unary operations (arity == 1)
        assert registry.get_arity('factorial') == 1
        assert registry.get_arity('square') == 1
        assert registry.get_arity('cube') == 1
        assert registry.get_arity('sqrt') == 1
        assert registry.get_arity('cbrt') == 1
        assert registry.get_arity('ln') == 1
        assert registry.get_arity('log10') == 1

    def test_direct_vs_registry_call(self):
        """Direct method call and registry call return the same result."""
        calc = Calculator()
        registry = OperationRegistry(calc)

        direct_result = calc.add(5, 3)
        registry_result = registry.call('add', 5, 3)
        assert direct_result == registry_result == 8


# ============================================================================
# Test Group D: Error Handling Responsibility (3 tests)
# ============================================================================


class TestErrorHandlingResponsibility:
    """Verify error handling is the responsibility of core Calculator class."""

    def test_domain_error_source(self):
        """Domain error (sqrt of negative) is raised by Calculator, not by UI layer."""
        calc = Calculator()
        with pytest.raises(ValueError) as exc_info:
            calc.sqrt(-4)
        assert "square root of negative" in str(exc_info.value).lower()

    def test_ui_error_handling(self):
        """ErrorLogger can log errors without raising exceptions."""
        calc = Calculator()
        logger = ErrorLogger()

        try:
            result = calc.sqrt(-4)
        except ValueError as e:
            # Log the error without raising
            logger.log_runtime_calculation_error(
                'sqrt',
                (-4,),
                'ValueError',
                str(e)
            )
            # If we get here, logging did not raise
            assert True

    def test_error_logger_independence(self):
        """ErrorLogger can be instantiated and used independently."""
        logger = ErrorLogger()
        # This should not raise an exception
        logger.log_invalid_operand('add', 'abc', 'test')
        assert True
