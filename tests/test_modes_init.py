"""test_modes_init.py — tests for src.modes and src package exports.

Tests cover:
- src.modes.__init__ exports
- src.__init__ exports
- Public API completeness
"""

import pytest


class TestModesPackageExports:
    """Tests for exports from src.modes package."""

    def test_import_basicoperations_from_modes(self):
        """Test that BasicOperations can be imported from src.modes."""
        from src.modes import BasicOperations
        assert BasicOperations is not None

    def test_import_advancedoperations_from_modes(self):
        """Test that AdvancedOperations can be imported from src.modes."""
        from src.modes import AdvancedOperations
        assert AdvancedOperations is not None

    def test_import_operationregistry_from_modes(self):
        """Test that OperationRegistry can be imported from src.modes."""
        from src.modes import OperationRegistry
        assert OperationRegistry is not None

    def test_modes_all_attribute(self):
        """Test that src.modes has __all__ attribute if needed."""
        import src.modes
        # Check that the key classes are accessible
        assert hasattr(src.modes, "BasicOperations")
        assert hasattr(src.modes, "AdvancedOperations")
        assert hasattr(src.modes, "OperationRegistry")


class TestSrcPackageExports:
    """Tests for exports from src package main __init__.py."""

    def test_import_basicoperations_from_src(self):
        """Test that BasicOperations can be imported from src."""
        from src import BasicOperations
        assert BasicOperations is not None

    def test_import_advancedoperations_from_src(self):
        """Test that AdvancedOperations can be imported from src."""
        from src import AdvancedOperations
        assert AdvancedOperations is not None

    def test_import_operationregistry_from_src(self):
        """Test that OperationRegistry can be imported from src."""
        from src import OperationRegistry
        assert OperationRegistry is not None

    def test_import_calculator_from_src(self):
        """Test that Calculator can be imported from src."""
        from src import Calculator
        assert Calculator is not None

    def test_import_inputvalidator_from_src(self):
        """Test that InputValidator can be imported from src."""
        from src import InputValidator
        assert InputValidator is not None

    def test_import_expressionparser_from_src(self):
        """Test that ExpressionParser can be imported from src."""
        from src import ExpressionParser
        assert ExpressionParser is not None

    def test_import_calculatorreplen_from_src(self):
        """Test that CalculatorREPL can be imported from src."""
        from src import CalculatorREPL
        assert CalculatorREPL is not None

    def test_import_clihandler_from_src(self):
        """Test that CLIHandler can be imported from src."""
        from src import CLIHandler
        assert CLIHandler is not None

    def test_src_all_attribute(self):
        """Test that src has __all__ attribute with expected exports."""
        from src import __all__
        expected_exports = {
            "Calculator",
            "InputValidator",
            "ExpressionParser",
            "CalculatorREPL",
            "CLIHandler",
            "OperationRegistry",
            "BasicOperations",
            "AdvancedOperations",
        }
        assert set(__all__) == expected_exports


class TestClassInstantiation:
    """Tests that exported classes can be instantiated."""

    def test_basicoperations_instantiation(self):
        """Test that BasicOperations can be instantiated."""
        from src import BasicOperations
        ops = BasicOperations()
        assert ops is not None
        assert hasattr(ops, "get_operations")

    def test_advancedoperations_instantiation(self):
        """Test that AdvancedOperations can be instantiated."""
        from src import AdvancedOperations
        ops = AdvancedOperations()
        assert ops is not None
        assert hasattr(ops, "get_operations")

    def test_operationregistry_instantiation(self):
        """Test that OperationRegistry can be instantiated."""
        from src import OperationRegistry
        registry = OperationRegistry()
        assert registry is not None
        assert hasattr(registry, "register_mode")
        assert hasattr(registry, "get")
        assert hasattr(registry, "get_mode")
        assert hasattr(registry, "all_names")

    def test_calculator_instantiation(self):
        """Test that Calculator can be instantiated."""
        from src import Calculator
        calc = Calculator()
        assert calc is not None
        assert hasattr(calc, "add")
        assert hasattr(calc, "get_history")

    def test_inputvalidator_instantiation(self):
        """Test that InputValidator can be instantiated."""
        from src import InputValidator
        validator = InputValidator()
        assert validator is not None
        assert hasattr(validator, "validate")


class TestBasicOperationsInterface:
    """Tests for BasicOperations interface through public imports."""

    def test_basicoperations_has_all_operations(self):
        """Test that BasicOperations has all expected operation methods."""
        from src import BasicOperations
        ops = BasicOperations()
        assert hasattr(ops, "add")
        assert hasattr(ops, "subtract")
        assert hasattr(ops, "multiply")
        assert hasattr(ops, "divide")
        assert callable(ops.add)
        assert callable(ops.subtract)
        assert callable(ops.multiply)
        assert callable(ops.divide)

    def test_basicoperations_get_operations_returns_dict(self):
        """Test that BasicOperations.get_operations() returns correct dict."""
        from src import BasicOperations
        ops = BasicOperations()
        ops_dict = ops.get_operations()
        assert isinstance(ops_dict, dict)
        assert set(ops_dict.keys()) == {"add", "subtract", "multiply", "divide"}


class TestAdvancedOperationsInterface:
    """Tests for AdvancedOperations interface through public imports."""

    def test_advancedoperations_has_all_operations(self):
        """Test that AdvancedOperations has all expected operation methods."""
        from src import AdvancedOperations
        ops = AdvancedOperations()
        expected_methods = {
            "factorial", "square", "cube", "square_root", "cube_root",
            "power", "natural_log", "log_base_10",
        }
        for method in expected_methods:
            assert hasattr(ops, method)
            assert callable(getattr(ops, method))

    def test_advancedoperations_get_operations_returns_dict(self):
        """Test that AdvancedOperations.get_operations() returns correct dict."""
        from src import AdvancedOperations
        ops = AdvancedOperations()
        ops_dict = ops.get_operations()
        assert isinstance(ops_dict, dict)
        expected_keys = {
            "factorial", "square", "cube", "square_root", "cube_root",
            "power", "natural_log", "log_base_10",
        }
        assert set(ops_dict.keys()) == expected_keys
