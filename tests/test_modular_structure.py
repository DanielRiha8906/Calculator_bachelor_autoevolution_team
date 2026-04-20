"""Comprehensive tests for the modularized Calculator structure.

This test module validates:
1. All new module paths are importable
2. OperationRegistry behavior (instantiation, operations, normal/all separation)
3. Interface layer functions (parse_cli_args, convert_operand, format_result)
4. Menu renderer functionality
5. Support package exports
6. Module isolation (core modules don't import from UI modules)
7. Backward compatibility shims
"""

import pytest
from unittest.mock import patch
from src.calculator import Calculator


# ==================== Import Path Tests ====================


class TestCoreLayerImports:
    """Verify core layer modules are importable and properly structured."""

    def test_import_calculator_from_core(self):
        """Test importing Calculator from canonical core location."""
        from src.core.calculator import Calculator as CoreCalc
        calc = CoreCalc()
        assert calc.add(2, 3) == 5

    def test_calculator_backward_compat_shim(self):
        """Test that src.calculator still works as a shim."""
        from src.calculator import Calculator as ShimCalc
        calc = ShimCalc()
        assert calc.subtract(10, 3) == 7

    def test_import_operation_registry(self):
        """Test importing OperationRegistry from core.operations_manager."""
        from src.core.operations_manager import OperationRegistry
        calc = Calculator()
        registry = OperationRegistry(calc)
        assert isinstance(registry, OperationRegistry)

    def test_get_operation_registry_function(self):
        """Test get_operation_registry function from core.operations."""
        from src.core.operations import get_operation_registry
        calc = Calculator()
        registry = get_operation_registry(calc)
        assert isinstance(registry, dict)
        assert "add" in registry


class TestInterfaceLayerImports:
    """Verify interface layer modules are importable."""

    def test_import_parse_cli_args(self):
        """Test importing parse_cli_args from interface.input_parser."""
        from src.interface.input_parser import parse_cli_args
        op_name, operands = parse_cli_args(["add", "3", "4"])
        assert op_name == "add"
        assert operands == ["3", "4"]

    def test_import_convert_operand(self):
        """Test importing convert_operand from interface.input_parser."""
        from src.interface.input_parser import convert_operand
        result = convert_operand("5")
        assert result == 5

    def test_import_format_result(self):
        """Test importing format_result from interface.output_formatter."""
        from src.interface.output_formatter import format_result
        result = format_result(42)
        assert result == "42"

    def test_import_display_menu_from_interface(self):
        """Test importing display_menu from interface.menu_renderer."""
        from src.interface.menu_renderer import display_menu
        assert callable(display_menu)

    def test_import_from_interface_package(self):
        """Test that interface package exports functions."""
        from src.interface import parse_cli_args, convert_operand
        assert callable(parse_cli_args)
        assert callable(convert_operand)


class TestInteractiveLayerImports:
    """Verify interactive layer modules are importable."""

    def test_import_from_interactive_input_handler(self):
        """Test importing from interactive.input_handler."""
        from src.interactive.input_handler import (
            get_operation_choice,
            get_operands,
        )
        assert callable(get_operation_choice)
        assert callable(get_operands)

    def test_import_run_interactive_session(self):
        """Test importing run_interactive_session."""
        from src.interactive.session import run_interactive_session
        assert callable(run_interactive_session)


class TestSupportLayerImports:
    """Verify support layer modules are importable."""

    def test_import_history_tracker_from_canonical(self):
        """Test importing HistoryTracker from canonical location."""
        from src.support.history import HistoryTracker
        tracker = HistoryTracker()
        assert isinstance(tracker, HistoryTracker)

    def test_history_backward_compat_shim(self):
        """Test that src.history still works as a shim."""
        from src.history import HistoryTracker
        tracker = HistoryTracker()
        tracker.record("add", [2, 3], 5)
        assert tracker.get_history() == ["add(2, 3) = 5"]

    def test_import_error_logger_from_canonical(self):
        """Test importing ErrorLogger from canonical location."""
        from src.support.error_logging import ErrorLogger
        assert ErrorLogger is not None

    def test_error_logger_backward_compat_shim(self):
        """Test that src.error_logger still works as canonical."""
        from src.error_logger import ErrorLogger
        assert ErrorLogger is not None


# ==================== OperationRegistry Tests ====================


class TestOperationRegistry:
    """Comprehensive tests for the OperationRegistry class."""

    def test_registry_instantiation(self):
        """Test that OperationRegistry can be instantiated."""
        from src.core.operations_manager import OperationRegistry
        calc = Calculator()
        registry = OperationRegistry(calc)
        assert isinstance(registry, OperationRegistry)

    def test_registry_has_normal_operations_dict(self):
        """Test that registry has _normal_operations dict."""
        from src.core.operations_manager import OperationRegistry
        calc = Calculator()
        registry = OperationRegistry(calc)
        assert hasattr(registry, "_normal_operations")
        assert isinstance(registry._normal_operations, dict)

    def test_registry_has_scientific_operations_dict(self):
        """Test that registry has _scientific_operations dict."""
        from src.core.operations_manager import OperationRegistry
        calc = Calculator()
        registry = OperationRegistry(calc)
        assert hasattr(registry, "_scientific_operations")
        assert isinstance(registry._scientific_operations, dict)

    def test_get_all_operations_returns_dict(self):
        """Test that get_all_operations returns a dict."""
        from src.core.operations_manager import OperationRegistry
        calc = Calculator()
        registry = OperationRegistry(calc)
        all_ops = registry.get_all_operations()
        assert isinstance(all_ops, dict)

    def test_get_all_operations_contains_expected_ops(self):
        """Test that get_all_operations contains 18 operations."""
        from src.core.operations_manager import OperationRegistry
        calc = Calculator()
        registry = OperationRegistry(calc)
        all_ops = registry.get_all_operations()
        expected_ops = {
            "add", "subtract", "multiply", "divide", "power",
            "factorial", "square", "cube", "square_root", "cube_root",
            "log", "ln", "sin", "cos", "tan", "cot", "asin", "acos"
        }
        assert set(all_ops.keys()) == expected_ops
        assert len(all_ops) == 18

    def test_get_normal_operations_returns_dict(self):
        """Test that get_normal_operations returns a dict."""
        from src.core.operations_manager import OperationRegistry
        calc = Calculator()
        registry = OperationRegistry(calc)
        normal_ops = registry.get_normal_operations()
        assert isinstance(normal_ops, dict)

    def test_get_normal_operations_is_subset_of_all(self):
        """Test that normal operations is a subset of all operations."""
        from src.core.operations_manager import OperationRegistry
        calc = Calculator()
        registry = OperationRegistry(calc)
        all_ops = registry.get_all_operations()
        normal_ops = registry.get_normal_operations()
        assert set(normal_ops.keys()).issubset(set(all_ops.keys()))

    def test_operations_are_tuples_with_arity(self):
        """Test that each operation is a 2-tuple (method, arity)."""
        from src.core.operations_manager import OperationRegistry
        calc = Calculator()
        registry = OperationRegistry(calc)
        for op_name, (method, arity) in registry.get_all_operations().items():
            assert isinstance(method, object), f"{op_name} method not callable"
            assert isinstance(arity, int), f"{op_name} arity not int"
            assert arity in (1, 2), f"{op_name} arity not 1 or 2"

    def test_registry_matches_get_operation_registry(self):
        """Test that OperationRegistry.get_all_operations() matches get_operation_registry()."""
        from src.core.operations_manager import OperationRegistry
        from src.core.operations import get_operation_registry
        calc = Calculator()
        registry = OperationRegistry(calc)
        legacy_registry = get_operation_registry(calc)
        # Should have same keys
        assert set(registry.get_all_operations().keys()) == set(legacy_registry.keys())


# ==================== Interface Layer Function Tests ====================


class TestParseCliArgs:
    """Comprehensive tests for parse_cli_args function."""

    def test_parse_cli_args_basic(self):
        """Test basic argument parsing."""
        from src.interface.input_parser import parse_cli_args
        op_name, operands = parse_cli_args(["add", "3", "4"])
        assert op_name == "add"
        assert operands == ["3", "4"]

    def test_parse_cli_args_single_operand(self):
        """Test parsing with single operand."""
        from src.interface.input_parser import parse_cli_args
        op_name, operands = parse_cli_args(["factorial", "5"])
        assert op_name == "factorial"
        assert operands == ["5"]

    def test_parse_cli_args_no_operands(self):
        """Test parsing with no operands."""
        from src.interface.input_parser import parse_cli_args
        op_name, operands = parse_cli_args(["operation"])
        assert op_name == "operation"
        assert operands == []

    def test_parse_cli_args_multiple_operands(self):
        """Test parsing with multiple operands."""
        from src.interface.input_parser import parse_cli_args
        op_name, operands = parse_cli_args(["op", "1", "2", "3"])
        assert op_name == "op"
        assert operands == ["1", "2", "3"]

    def test_parse_cli_args_preserves_operand_order(self):
        """Test that operand order is preserved."""
        from src.interface.input_parser import parse_cli_args
        op_name, operands = parse_cli_args(["subtract", "10", "3"])
        assert operands == ["10", "3"]

    def test_parse_cli_args_with_float_strings(self):
        """Test parsing float string operands."""
        from src.interface.input_parser import parse_cli_args
        op_name, operands = parse_cli_args(["add", "3.5", "2.1"])
        assert operands == ["3.5", "2.1"]

    def test_parse_cli_args_with_negative_operands(self):
        """Test parsing negative operand strings."""
        from src.interface.input_parser import parse_cli_args
        op_name, operands = parse_cli_args(["add", "-5", "10"])
        assert operands == ["-5", "10"]


class TestConvertOperand:
    """Comprehensive tests for convert_operand function."""

    def test_convert_operand_integer_string(self):
        """Test converting integer string."""
        from src.interface.input_parser import convert_operand
        result = convert_operand("42")
        assert result == 42
        assert isinstance(result, int)

    def test_convert_operand_float_string_whole_number(self):
        """Test converting float string representing whole number."""
        from src.interface.input_parser import convert_operand
        result = convert_operand("3.0")
        assert result == 3
        assert isinstance(result, int)

    def test_convert_operand_float_string(self):
        """Test converting true float string."""
        from src.interface.input_parser import convert_operand
        result = convert_operand("3.5")
        assert result == 3.5
        assert isinstance(result, float)

    def test_convert_operand_negative_integer(self):
        """Test converting negative integer string."""
        from src.interface.input_parser import convert_operand
        result = convert_operand("-42")
        assert result == -42
        assert isinstance(result, int)

    def test_convert_operand_negative_float(self):
        """Test converting negative float string."""
        from src.interface.input_parser import convert_operand
        result = convert_operand("-3.5")
        assert result == -3.5
        assert isinstance(result, float)

    def test_convert_operand_zero(self):
        """Test converting zero."""
        from src.interface.input_parser import convert_operand
        result = convert_operand("0")
        assert result == 0
        assert isinstance(result, int)

    def test_convert_operand_zero_float(self):
        """Test converting 0.0."""
        from src.interface.input_parser import convert_operand
        result = convert_operand("0.0")
        assert result == 0
        assert isinstance(result, int)

    def test_convert_operand_invalid_string(self):
        """Test that invalid string raises ValueError."""
        from src.interface.input_parser import convert_operand
        with pytest.raises(ValueError):
            convert_operand("abc")

    def test_convert_operand_empty_string(self):
        """Test that empty string raises ValueError."""
        from src.interface.input_parser import convert_operand
        with pytest.raises(ValueError):
            convert_operand("")

    def test_convert_operand_large_number(self):
        """Test converting large numbers."""
        from src.interface.input_parser import convert_operand
        result = convert_operand("999999999")
        assert result == 999999999
        assert isinstance(result, int)

    def test_convert_operand_scientific_notation(self):
        """Test converting scientific notation."""
        from src.interface.input_parser import convert_operand
        result = convert_operand("1e3")
        assert result == 1000
        assert isinstance(result, int)

    def test_convert_operand_scientific_notation_float(self):
        """Test converting scientific notation float."""
        from src.interface.input_parser import convert_operand
        result = convert_operand("1.5e2")
        assert result == 150  # 1.5e2 = 150.0 which converts to int 150
        assert isinstance(result, int)


class TestFormatResult:
    """Comprehensive tests for format_result function."""

    def test_format_result_integer(self):
        """Test formatting integer result."""
        from src.interface.output_formatter import format_result
        result = format_result(42)
        assert result == "42"
        assert isinstance(result, str)

    def test_format_result_float(self):
        """Test formatting float result."""
        from src.interface.output_formatter import format_result
        result = format_result(3.14)
        assert result == "3.14"
        assert isinstance(result, str)

    def test_format_result_zero(self):
        """Test formatting zero."""
        from src.interface.output_formatter import format_result
        result = format_result(0)
        assert result == "0"

    def test_format_result_negative_integer(self):
        """Test formatting negative integer."""
        from src.interface.output_formatter import format_result
        result = format_result(-42)
        assert result == "-42"

    def test_format_result_negative_float(self):
        """Test formatting negative float."""
        from src.interface.output_formatter import format_result
        result = format_result(-3.5)
        assert result == "-3.5"

    def test_format_result_large_number(self):
        """Test formatting large number."""
        from src.interface.output_formatter import format_result
        result = format_result(999999999)
        assert result == "999999999"

    def test_format_result_small_decimal(self):
        """Test formatting small decimal."""
        from src.interface.output_formatter import format_result
        result = format_result(0.001)
        assert result == "0.001"

    def test_format_result_float_whole_number(self):
        """Test formatting float that represents whole number."""
        from src.interface.output_formatter import format_result
        result = format_result(5.0)
        assert result == "5.0"


class TestDisplayMenu:
    """Tests for display_menu function."""

    def test_display_menu_with_registry(self):
        """Test that display_menu can be called with a registry."""
        from src.interface.menu_renderer import display_menu
        from src.core.operations import get_operation_registry
        calc = Calculator()
        registry = get_operation_registry(calc)
        with patch("builtins.print") as mock_print:
            display_menu(registry)
            assert mock_print.called

    def test_display_menu_prints_operations(self):
        """Test that display_menu prints operation names."""
        from src.interface.menu_renderer import display_menu
        from src.core.operations import get_operation_registry
        calc = Calculator()
        registry = get_operation_registry(calc)
        with patch("builtins.print") as mock_print:
            display_menu(registry)
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "add" in output
            assert "Available operations" in output

    def test_display_menu_with_empty_registry(self):
        """Test display_menu with empty registry."""
        from src.interface.menu_renderer import display_menu
        with patch("builtins.print") as mock_print:
            display_menu({})
            # Should still print header
            assert mock_print.called


# ==================== Support Package Tests ====================


class TestSupportPackageExports:
    """Tests for support package structure and exports."""

    def test_support_history_contains_history_tracker(self):
        """Test that src.support.history exports HistoryTracker."""
        from src.support import history
        assert hasattr(history, "HistoryTracker")

    def test_history_tracker_has_required_methods(self):
        """Test that HistoryTracker has required methods."""
        from src.support.history import HistoryTracker
        tracker = HistoryTracker()
        assert hasattr(tracker, "record")
        assert hasattr(tracker, "get_history")
        assert callable(tracker.record)
        assert callable(tracker.get_history)

    def test_history_tracker_record_and_get(self):
        """Test HistoryTracker record and get_history."""
        from src.support.history import HistoryTracker
        tracker = HistoryTracker()
        tracker.record("add", [2, 3], 5)
        history = tracker.get_history()
        assert len(history) == 1
        assert "add(2, 3) = 5" in history[0]


# ==================== Interface Package Tests ====================


class TestInterfacePackageExports:
    """Tests for interface package structure and exports."""

    def test_interface_package_has_input_parser(self):
        """Test that interface package has input_parser module."""
        from src.interface import input_parser
        assert hasattr(input_parser, "parse_cli_args")
        assert hasattr(input_parser, "convert_operand")

    def test_interface_package_has_output_formatter(self):
        """Test that interface package has output_formatter module."""
        from src.interface import output_formatter
        assert hasattr(output_formatter, "format_result")

    def test_interface_package_has_menu_renderer(self):
        """Test that interface package has menu_renderer module."""
        from src.interface import menu_renderer
        assert hasattr(menu_renderer, "display_menu")


# ==================== Backward Compatibility Tests ====================


class TestBackwardCompatibilityShims:
    """Tests verifying all backward compatibility shims work."""

    def test_calculator_shim_works(self):
        """Test that src.calculator shim works."""
        from src.calculator import Calculator
        calc = Calculator()
        assert calc.add(2, 3) == 5

    def test_history_shim_works(self):
        """Test that src.history shim works."""
        from src.history import HistoryTracker
        tracker = HistoryTracker()
        tracker.record("test", [1], 1)
        assert len(tracker.get_history()) == 1

    def test_error_logger_direct_access(self):
        """Test that ErrorLogger is still accessible from error_logger."""
        from src.error_logger import ErrorLogger
        assert ErrorLogger is not None

    def test_input_handler_display_menu_shim(self):
        """Test that display_menu is re-exported from input_handler."""
        from src.input_handler import display_menu
        assert callable(display_menu)

    def test_input_handler_get_operation_choice_shim(self):
        """Test that get_operation_choice is re-exported from input_handler."""
        from src.input_handler import get_operation_choice
        assert callable(get_operation_choice)

    def test_input_handler_get_operands_shim(self):
        """Test that get_operands is re-exported from input_handler."""
        from src.input_handler import get_operands
        assert callable(get_operands)

    def test_input_handler_run_interactive_session_shim(self):
        """Test that run_interactive_session is re-exported from input_handler."""
        from src.input_handler import run_interactive_session
        assert callable(run_interactive_session)

    def test_input_handler_get_operation_registry_shim(self):
        """Test that get_operation_registry is re-exported from input_handler."""
        from src.input_handler import get_operation_registry
        calc = Calculator()
        registry = get_operation_registry(calc)
        assert isinstance(registry, dict)
        assert "add" in registry


# ==================== Module Isolation Tests ====================


class TestModuleIsolation:
    """Tests verifying that core modules don't import from UI modules."""

    def test_calculator_has_no_ui_imports(self):
        """Test that Calculator module has no I/O dependencies."""
        import src.core.calculator
        import inspect
        source = inspect.getsource(src.core.calculator)
        # Should not import UI modules
        assert "from src.interface" not in source
        assert "from src.interactive" not in source
        assert "input(" not in source

    def test_operations_manager_has_no_ui_imports(self):
        """Test that operations_manager has no I/O dependencies."""
        import src.core.operations_manager
        import inspect
        source = inspect.getsource(src.core.operations_manager)
        # Should not import UI modules
        assert "from src.interface" not in source
        assert "from src.interactive" not in source
        assert "print(" not in source

    def test_interface_modules_are_stateless(self):
        """Test that interface modules have no session/state imports."""
        import src.interface.input_parser
        import inspect
        source = inspect.getsource(src.interface.input_parser)
        # Should not import interactive session
        assert "from src.interactive" not in source


# ==================== Integration Tests ====================


class TestModularIntegration:
    """Integration tests verifying the modular structure works together."""

    def test_parse_convert_format_pipeline(self):
        """Test the pipeline: parse -> convert -> calculate -> format."""
        from src.interface.input_parser import parse_cli_args, convert_operand
        from src.interface.output_formatter import format_result
        from src.core.calculator import Calculator
        from src.core.operations import get_operation_registry

        # Parse
        op_name, operand_strs = parse_cli_args(["add", "3", "4"])

        # Convert
        operands = [convert_operand(s) for s in operand_strs]

        # Calculate
        calc = Calculator()
        result = calc.add(*operands)

        # Format
        output = format_result(result)
        assert output == "7"

    def test_operation_registry_pipeline(self):
        """Test using OperationRegistry through the pipeline."""
        from src.core.operations_manager import OperationRegistry
        from src.core.calculator import Calculator
        from src.interface.menu_renderer import display_menu

        calc = Calculator()
        registry = OperationRegistry(calc)

        # Should be able to display the menu
        with patch("builtins.print") as mock_print:
            display_menu(registry.get_all_operations())
            assert mock_print.called
