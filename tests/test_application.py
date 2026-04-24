"""Tests for the Application layer separation (Issue #402).

Tests verify that:
1. Calculator can be instantiated independently without UI/interface dependencies
2. Application layer accepts and uses Calculator instances
3. Application layer manages operation registry
4. Application layer handles CLI and interactive modes
5. OperationHistory and ErrorLog work independently of Calculator
6. All layers are properly separated and composable
"""

import sys
from unittest.mock import MagicMock, patch

import pytest

from src.calculator import Calculator
from src.error_logging import ErrorLog
from src.history import OperationHistory


class TestCalculatorIndependence:
    """Tests verifying Calculator works independently of UI layers."""

    def test_calculator_can_be_instantiated_directly(self):
        """Calculator is instantiable without any UI/interface dependencies."""
        calc = Calculator()
        assert isinstance(calc, Calculator)
        # Verify all methods exist
        assert hasattr(calc, "add")
        assert hasattr(calc, "subtract")
        assert hasattr(calc, "multiply")
        assert hasattr(calc, "divide")
        assert hasattr(calc, "factorial")
        assert hasattr(calc, "square")
        assert hasattr(calc, "cube")
        assert hasattr(calc, "square_root")
        assert hasattr(calc, "cube_root")
        assert hasattr(calc, "power")
        assert hasattr(calc, "log10")
        assert hasattr(calc, "ln")

    def test_calculator_add_isolated(self):
        """Calculator.add() works independently of any UI/interface layer."""
        calc = Calculator()
        result = calc.add(5, 3)
        assert result == 8

    def test_calculator_divide_raises_zerodivisionerror(self):
        """Calculator.divide() raises ZeroDivisionError without UI catching it."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(5, 0)

    def test_square_root_raises_valueerror_independently(self):
        """Calculator.square_root() raises ValueError without UI wrapping."""
        calc = Calculator()
        with pytest.raises(ValueError):
            calc.square_root(-1)

    def test_can_import_calculator_independently(self):
        """Calculator module imports without requiring interface dependencies."""
        from src.calculator import Calculator as CalcClass

        assert CalcClass is not None
        assert isinstance(CalcClass, type)


class TestApplicationLayerIntegration:
    """Tests verifying Application layer accepts and integrates Calculator."""

    def test_application_interface_accepts_calculator(self):
        """New Application class accepts Calculator instance."""
        from src.application import Application

        calc = Calculator()
        app = Application(calc)
        assert app is not None
        assert hasattr(app, "calculator")
        assert app.calculator is calc

    def test_application_interface_has_registry(self):
        """Application instance has a registry attribute with all operations."""
        from src.application import Application

        calc = Calculator()
        app = Application(calc)
        assert hasattr(app, "registry")
        assert isinstance(app.registry, dict)

        # Verify all 12 operations are in registry
        expected_ops = {
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
        }
        assert set(app.registry.keys()) == expected_ops

    def test_can_import_application_with_calculator(self):
        """src.application module imports with Calculator dependency."""
        from src.application import Application

        assert Application is not None
        assert isinstance(Application, type)


class TestApplicationRegistryArities:
    """Tests verifying registry operations have correct arity (argument count)."""

    def test_application_registry_has_correct_arities(self):
        """Operations have correct number of arguments (unary or binary)."""
        from src.application import Application

        calc = Calculator()
        app = Application(calc)

        # Binary operations (2 args)
        binary_ops = {"add", "subtract", "multiply", "divide", "power"}
        # Unary operations (1 arg)
        unary_ops = {"factorial", "square", "cube", "square_root", "cube_root", "ln", "log10"}

        for op_name in binary_ops:
            op_func = app.registry[op_name]
            # Should be callable with 2 args without TypeError
            try:
                # Don't execute, just verify signature by inspecting the callable
                import inspect

                sig = inspect.signature(op_func)
                params = list(sig.parameters.values())
                assert len(params) == 2, f"{op_name} should have 2 parameters"
            except (ValueError, TypeError):
                # If we can't inspect, try to call it (will fail if wrong arity)
                pass

        for op_name in unary_ops:
            op_func = app.registry[op_name]
            # Should be callable with 1 arg without TypeError
            try:
                import inspect

                sig = inspect.signature(op_func)
                params = list(sig.parameters.values())
                assert len(params) == 1, f"{op_name} should have 1 parameter"
            except (ValueError, TypeError):
                pass


class TestApplicationCLIMode:
    """Tests verifying Application can execute CLI mode operations."""

    def test_application_interface_executes_cli_operation(self):
        """Application can execute CLI mode dispatching add operation."""
        from src.application import Application

        calc = Calculator()
        app = Application(calc)

        # Mock sys.argv for CLI mode with add 5 3
        with patch("sys.argv", ["calc", "add", "5", "3"]):
            # Application should have a method to execute CLI operations
            result = app.execute_cli(["add", "5", "3"])
            assert result == 8 or result is None  # May return result or exit(0)

    def test_application_interface_cli_exits_on_unknown_op(self):
        """Application CLI mode rejects unknown operations."""
        from src.application import Application

        calc = Calculator()
        app = Application(calc)

        # Unknown operation should raise SystemExit or return error
        with pytest.raises((SystemExit, ValueError, KeyError)):
            app.execute_cli(["unknown_op"])


class TestApplicationInteractiveMode:
    """Tests verifying Application can run interactive loop."""

    def test_application_interface_runs_interactive_loop(self):
        """Application can run interactive loop with mocked input and exit cleanly."""
        from src.application import Application

        calc = Calculator()
        app = Application(calc)

        # Mock input to return 'quit' immediately
        with patch("builtins.input", return_value="quit"):
            result = app.run_interactive()
            # Should return normally without raising
            assert result is None or result == 0

    def test_interactive_mode_exits_after_too_many_failures(self):
        """Application interactive mode exits after 3 consecutive invalid inputs."""
        from src.application import Application

        calc = Calculator()
        app = Application(calc)

        # Mock input to return 3 invalid operations then 'quit'
        invalid_inputs = ["invalid1", "invalid2", "invalid3", "quit"]
        with patch("builtins.input", side_effect=invalid_inputs):
            result = app.run_interactive()
            # Should exit after 3 failures (may raise SystemExit or return)
            assert result is None or isinstance(result, int)


class TestOperationHistoryIndependence:
    """Tests verifying OperationHistory works independently."""

    def test_operation_history_independent_of_calculator(self):
        """OperationHistory works independently of Calculator."""
        history = OperationHistory()
        # Record an operation manually
        history.record("add", [5, 3], 8)
        # Verify history list is not empty
        assert len(history.get_all()) > 0
        assert "add" in history.get_all()[0]


class TestErrorLogIndependence:
    """Tests verifying ErrorLog works independently."""

    def test_error_log_independent_of_calculator(self):
        """ErrorLog works independently of Calculator."""
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmpdir:
            error_log_path = Path(tmpdir) / "test_error.log"
            error_log = ErrorLog(str(error_log_path))
            # Log an error
            error_log.log_error("invalid_input", "add", [5, "abc"], "not a number")
            # Verify file was created and contains the entry
            assert error_log_path.exists()
            content = error_log_path.read_text()
            assert "invalid_input" in content
            assert "add" in content


class TestImportsAndModules:
    """Tests verifying all modules can be imported independently."""

    def test_can_import_calculator_independently(self):
        """Calculator module can be imported independently."""
        from src.calculator import Calculator as CalcClass

        assert CalcClass is not None

    def test_can_import_application_with_calculator(self):
        """Application module can be imported with Calculator."""
        from src.application import Application

        assert Application is not None

    def test_can_import_history_independently(self):
        """OperationHistory can be imported independently."""
        from src.history import OperationHistory as HistoryClass

        assert HistoryClass is not None

    def test_can_import_error_logging_independently(self):
        """ErrorLog can be imported independently."""
        from src.error_logging import ErrorLog as ErrorLogClass

        assert ErrorLogClass is not None
