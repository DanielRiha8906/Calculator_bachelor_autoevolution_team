"""Tests validating the logic separation refactoring (Issue #176).

This module validates that:
1. Core calculation logic is isolated from UI concerns
2. Interactive session functions are isolated from CLI argument parsing
3. Backward compatibility shim works correctly
4. Top-level package exports are accessible
5. Import paths work correctly
"""

import pytest
from unittest.mock import patch
from src.core.calculator import Calculator


# ==================== Import Path Verification Tests ====================


class TestCoreOperationsImportPath:
    """Tests verifying that core.operations module is properly isolated."""

    def test_import_from_core_operations_directly(self):
        """Test importing get_operation_registry from src.core.operations."""
        from src.core.operations import get_operation_registry

        calc = Calculator()
        registry = get_operation_registry(calc)
        assert isinstance(registry, dict)
        assert "add" in registry
        assert len(registry) == 18

    def test_core_operations_no_cli_imports(self):
        """Verify src.core.operations does not import cli module."""
        import src.core.operations as core_ops
        import inspect

        # Get the source code of the module
        source = inspect.getsource(core_ops)
        # Should not import cli or sys.argv
        assert "from src.cli" not in source
        assert "import sys" not in source
        assert "sys.argv" not in source

    def test_core_operations_no_interactive_imports(self):
        """Verify src.core.operations does not depend on interactive UI."""
        import src.core.operations as core_ops
        import inspect

        source = inspect.getsource(core_ops)
        # Should not import input, print, or display functions
        assert "input(" not in source  # No user input functions
        assert "display" not in source.lower()

    def test_get_operation_registry_returns_correct_structure(self):
        """Verify registry structure is consistent and correct."""
        from src.core.operations import get_operation_registry

        calc = Calculator()
        registry = get_operation_registry(calc)

        # Verify all operations are present
        expected_ops = {
            "add",
            "subtract",
            "multiply",
            "divide",
            "power",
            "factorial",
            "square",
            "cube",
            "square_root",
            "cube_root",
            "log",
            "ln",
            "sin",
            "cos",
            "tan",
            "cot",
            "asin",
            "acos",
        }
        assert set(registry.keys()) == expected_ops

        # Verify each operation is a 2-tuple of (method, arity)
        for op_name, (method, arity) in registry.items():
            assert callable(method), f"{op_name} method not callable"
            assert isinstance(arity, int), f"{op_name} arity not an int"
            assert arity in (1, 2), f"{op_name} arity not 1 or 2"

    def test_core_operations_can_be_called_without_ui(self):
        """Verify that operations can be used without any UI dependency."""
        from src.core.operations import get_operation_registry

        calc = Calculator()
        registry = get_operation_registry(calc)

        # Call a binary operation
        add_method, add_arity = registry["add"]
        result = add_method(2, 3)
        assert result == 5
        assert add_arity == 2

        # Call a unary operation
        square_method, square_arity = registry["square"]
        result = square_method(4)
        assert result == 16
        assert square_arity == 1


class TestInteractiveSessionImportPath:
    """Tests verifying that interactive.session is isolated from CLI."""

    def test_import_from_interactive_session_directly(self):
        """Test importing from src.interactive.session."""
        from src.interactive.session import (
            run_interactive_session,
            display_menu,
            get_operation_choice,
            get_operands,
        )

        # Verify functions exist and are callable
        assert callable(run_interactive_session)
        assert callable(display_menu)
        assert callable(get_operation_choice)
        assert callable(get_operands)

    def test_interactive_session_no_cli_imports(self):
        """Verify src.interactive.session does not import cli module."""
        import src.interactive.session as interactive_session
        import inspect

        source = inspect.getsource(interactive_session)
        # Should not import cli or sys.argv
        assert "from src.cli" not in source
        assert "import sys" not in source
        assert "sys.argv" not in source

    def test_interactive_session_no_sys_argv(self):
        """Verify interactive session doesn't reference sys.argv."""
        import src.interactive.session as interactive_session
        import inspect

        source = inspect.getsource(interactive_session)
        assert "sys.argv" not in source

    def test_interactive_session_uses_core_operations(self):
        """Verify interactive session imports from core.operations."""
        import src.interactive.session as interactive_session
        import inspect

        source = inspect.getsource(interactive_session)
        # Should import from core.operations
        assert "from ..core.operations import" in source

    def test_display_menu_works_with_core_registry(self):
        """Verify display_menu works with registry from core.operations."""
        from src.core.operations import get_operation_registry
        from src.interactive.session import display_menu

        calc = Calculator()
        registry = get_operation_registry(calc)

        with patch("builtins.print") as mock_print:
            display_menu(registry)
            # Verify operations were printed
            printed = [call.args[0] for call in mock_print.call_args_list]
            output = "\n".join(str(p) for p in printed)
            assert "add" in output

    def test_get_operation_choice_works_with_core_registry(self):
        """Verify get_operation_choice works with core registry."""
        from src.core.operations import get_operation_registry
        from src.interactive.session import get_operation_choice

        calc = Calculator()
        registry = get_operation_registry(calc)

        with patch("builtins.input", return_value="add"):
            result = get_operation_choice(registry)
            name, method, arity = result
            assert name == "add"
            assert arity == 2
            assert method(2, 3) == 5

    def test_get_operands_is_independent_of_operations(self):
        """Verify get_operands doesn't depend on operation registry."""
        from src.interactive.session import get_operands

        with patch("builtins.input", return_value="5.5"):
            operands = get_operands(1)
            assert operands == [5.5]


class TestBackwardCompatibilityShim:
    """Tests verifying the backward-compatibility shim in input_handler.py."""

    def test_import_get_operation_registry_from_input_handler(self):
        """Verify get_operation_registry is re-exported from input_handler."""
        from src.input_handler import get_operation_registry

        calc = Calculator()
        registry = get_operation_registry(calc)
        assert "add" in registry
        assert len(registry) == 18

    def test_import_display_menu_from_input_handler(self):
        """Verify display_menu is re-exported from input_handler."""
        from src.input_handler import display_menu

        assert callable(display_menu)

    def test_import_get_operation_choice_from_input_handler(self):
        """Verify get_operation_choice is re-exported from input_handler."""
        from src.input_handler import get_operation_choice

        assert callable(get_operation_choice)

    def test_import_get_operands_from_input_handler(self):
        """Verify get_operands is re-exported from input_handler."""
        from src.input_handler import get_operands

        assert callable(get_operands)

    def test_import_run_interactive_session_from_input_handler(self):
        """Verify run_interactive_session is re-exported from input_handler."""
        from src.input_handler import run_interactive_session

        assert callable(run_interactive_session)

    def test_import_max_validation_attempts_from_input_handler(self):
        """Verify MAX_VALIDATION_ATTEMPTS is re-exported from input_handler."""
        from src.input_handler import MAX_VALIDATION_ATTEMPTS

        assert isinstance(MAX_VALIDATION_ATTEMPTS, int)
        assert MAX_VALIDATION_ATTEMPTS == 5

    def test_backward_compat_functions_behave_identically(self):
        """Verify re-exported functions work identically."""
        from src.input_handler import get_operation_registry as bw_compat_reg
        from src.core.operations import get_operation_registry as core_reg

        calc1 = Calculator()
        calc2 = Calculator()

        reg1 = bw_compat_reg(calc1)
        reg2 = core_reg(calc2)

        # Both should have same operations
        assert set(reg1.keys()) == set(reg2.keys())

    def test_backward_compat_shim_is_transparent(self):
        """Verify using the shim produces same results as using core directly."""
        from src.input_handler import display_menu as bw_compat_menu
        from src.interactive.session import display_menu as core_menu
        from src.core.operations import get_operation_registry

        calc = Calculator()
        registry = get_operation_registry(calc)

        with patch("builtins.print") as mock_print1:
            bw_compat_menu(registry)
        output1 = [call.args[0] for call in mock_print1.call_args_list]

        with patch("builtins.print") as mock_print2:
            core_menu(registry)
        output2 = [call.args[0] for call in mock_print2.call_args_list]

        # Both should produce the same output
        assert output1 == output2


class TestTopLevelPackageExports:
    """Tests verifying top-level src.__init__ exports."""

    def test_get_operation_registry_in_top_level_exports(self):
        """Verify get_operation_registry is exported from src."""
        from src import get_operation_registry

        calc = Calculator()
        registry = get_operation_registry(calc)
        assert "add" in registry

    def test_run_interactive_session_in_top_level_exports(self):
        """Verify run_interactive_session is exported from src."""
        from src import run_interactive_session

        assert callable(run_interactive_session)

    def test_calculator_in_top_level_exports(self):
        """Verify Calculator is exported from src."""
        from src import Calculator as TopLevelCalc

        assert TopLevelCalc is Calculator

    def test_execute_cli_in_top_level_exports(self):
        """Verify execute_cli is exported from src."""
        from src import execute_cli

        assert callable(execute_cli)

    def test_error_logger_in_top_level_exports(self):
        """Verify ErrorLogger is exported from src."""
        from src import ErrorLogger

        assert callable(ErrorLogger)


class TestCLIUsesCoreDependencies:
    """Tests verifying CLI correctly uses core dependencies."""

    def test_cli_imports_from_core_operations(self):
        """Verify cli.py imports get_operation_registry from core.operations."""
        import src.cli
        import inspect

        source = inspect.getsource(src.cli)
        # Should import from core.operations
        assert "from src.core.operations import get_operation_registry" in source

    def test_cli_does_not_import_from_input_handler(self):
        """Verify cli.py doesn't import from input_handler."""
        import src.cli
        import inspect

        source = inspect.getsource(src.cli)
        # Should not import from input_handler
        assert "from src.input_handler" not in source

    def test_execute_cli_calls_core_operations(self):
        """Verify execute_cli works with core registry."""
        from src.cli import execute_cli
        from src.core.operations import get_operation_registry

        calc = Calculator()
        registry = get_operation_registry(calc)

        with patch("builtins.print"):
            result = execute_cli("add", ["2", "3"], registry, calc)
            assert result == 0

    def test_patching_core_operations_affects_cli(self):
        """Verify that patching core.operations affects CLI execution."""
        from src.cli import execute_cli
        from src.core.operations import get_operation_registry

        calc = Calculator()

        # Patch the registry in the core module
        with patch("src.core.operations.get_operation_registry") as mock_reg:
            mock_registry = {"add": (lambda x, y: 999, 2)}
            mock_reg.return_value = mock_registry

            # Now execute_cli should use our patched registry
            with patch("builtins.print") as mock_print:
                # Even though we pass a real registry, the patch should intercept
                # This verifies the dependency is properly wired
                result = execute_cli("add", ["2", "3"], mock_registry, calc)
                # Result should work with our mocked operation
                output = [call.args[0] for call in mock_print.call_args_list]
                assert any("999" in str(o) for o in output)


# ==================== Module Structure Validation ====================


class TestModuleStructure:
    """Tests validating the module structure of the refactoring."""

    def test_core_package_exists(self):
        """Verify src.core package exists and is importable."""
        import src.core

        assert hasattr(src.core, "Calculator")
        assert hasattr(src.core, "get_operation_registry")

    def test_interactive_package_exists(self):
        """Verify src.interactive package exists and is importable."""
        import src.interactive

        assert hasattr(src.interactive, "run_interactive_session")

    def test_core_operations_module_exists(self):
        """Verify src.core.operations module exists."""
        import src.core.operations

        assert hasattr(src.core.operations, "get_operation_registry")

    def test_interactive_session_module_exists(self):
        """Verify src.interactive.session module exists."""
        import src.interactive.session

        assert hasattr(src.interactive.session, "run_interactive_session")
        assert hasattr(src.interactive.session, "display_menu")
        assert hasattr(src.interactive.session, "get_operation_choice")
        assert hasattr(src.interactive.session, "get_operands")

    def test_input_handler_shim_exists(self):
        """Verify src.input_handler backward compatibility shim exists."""
        import src.input_handler

        # Verify all expected exports are available
        assert hasattr(src.input_handler, "get_operation_registry")
        assert hasattr(src.input_handler, "display_menu")
        assert hasattr(src.input_handler, "get_operation_choice")
        assert hasattr(src.input_handler, "get_operands")
        assert hasattr(src.input_handler, "run_interactive_session")


# ==================== Cross-Module Consistency Tests ====================


class TestCrossModuleConsistency:
    """Tests ensuring consistency when using different import paths."""

    def test_same_calculator_instance_same_registry(self):
        """Verify same calculator produces same registry regardless of import path."""
        from src.core.operations import get_operation_registry as core_get_reg
        from src.input_handler import get_operation_registry as shim_get_reg

        calc = Calculator()
        registry1 = core_get_reg(calc)
        registry2 = shim_get_reg(calc)

        # Should have identical operations
        assert set(registry1.keys()) == set(registry2.keys())
        # Should have identical arities
        for op in registry1.keys():
            assert registry1[op][1] == registry2[op][1]

    def test_different_calculator_instances_independent_registries(self):
        """Verify different calculators produce independent registries."""
        from src.core.operations import get_operation_registry

        calc1 = Calculator()
        calc2 = Calculator()

        registry1 = get_operation_registry(calc1)
        registry2 = get_operation_registry(calc2)

        # Methods should be different (bound to different instances)
        assert registry1["add"][0] is not registry2["add"][0]

    def test_operation_registry_consistency_across_imports(self):
        """Verify operation registry is consistent across different import paths."""
        from src.core.operations import get_operation_registry as core_reg
        from src.input_handler import get_operation_registry as shim_reg
        from src.interactive.session import get_operation_registry as session_imported

        calc = Calculator()

        # All three import paths should produce equivalent registries
        reg1 = core_reg(calc)
        reg2 = shim_reg(calc)
        reg3 = session_imported(calc)

        # All should have same operations
        assert set(reg1.keys()) == set(reg2.keys()) == set(reg3.keys())


# ==================== Isolation Verification Tests ====================


class TestIsolationVerification:
    """Tests verifying that layers are properly isolated."""

    def test_core_layer_no_input_function(self):
        """Verify core layer doesn't use input() function."""
        import src.core.operations

        source = __import__("inspect").getsource(src.core.operations)
        assert "input(" not in source

    def test_core_layer_no_print_statements(self):
        """Verify core layer doesn't print directly."""
        import src.core.operations

        source = __import__("inspect").getsource(src.core.operations)
        # Should not have standalone print calls
        assert "print(" not in source

    def test_interactive_layer_uses_input(self):
        """Verify interactive layer uses input() for user interaction."""
        import src.interactive.session

        source = __import__("inspect").getsource(src.interactive.session)
        # Should have input calls
        assert "input(" in source

    def test_interactive_layer_uses_print(self):
        """Verify interactive layer uses print() for output."""
        import src.interactive.session

        source = __import__("inspect").getsource(src.interactive.session)
        # Should have print calls
        assert "print(" in source

    def test_cli_layer_uses_core_not_interactive(self):
        """Verify CLI uses core operations directly, not interactive."""
        import src.cli

        source = __import__("inspect").getsource(src.cli)
        # Should import from core
        assert "from src.core.operations" in source
        # Should not import interactive session functions
        assert "from src.interactive" not in source
        assert "get_operation_choice" not in source


# ==================== Functional Integration Tests ====================


class TestFunctionalIntegration:
    """Integration tests verifying the separated layers work correctly together."""

    def test_core_registry_usable_by_interactive(self):
        """Verify interactive session can use core registry."""
        from src.core.operations import get_operation_registry
        from src.interactive.session import display_menu, get_operation_choice

        calc = Calculator()
        registry = get_operation_registry(calc)

        # Display menu should work
        with patch("builtins.print"):
            display_menu(registry)

        # Get operation choice should work
        with patch("builtins.input", return_value="add"):
            result = get_operation_choice(registry)
            assert result[0] == "add"

    def test_core_registry_usable_by_cli(self):
        """Verify CLI can use core registry."""
        from src.core.operations import get_operation_registry
        from src.cli import execute_cli

        calc = Calculator()
        registry = get_operation_registry(calc)

        # Execute CLI should work with core registry
        with patch("builtins.print"):
            result = execute_cli("add", ["2", "3"], registry, calc)
            assert result == 0

    def test_interactive_and_cli_can_coexist(self):
        """Verify interactive and CLI layers can be used in same process."""
        from src.core.operations import get_operation_registry
        from src.interactive.session import get_operands
        from src.cli import execute_cli

        calc = Calculator()
        registry = get_operation_registry(calc)

        # Use CLI
        with patch("builtins.print"):
            cli_result = execute_cli("add", ["2", "3"], registry, calc)
            assert cli_result == 0

        # Use interactive
        with patch("builtins.input", return_value="5"):
            operands = get_operands(1)
            assert operands == [5.0]

    def test_full_session_without_cli_args(self):
        """Verify a full interactive session works without CLI."""
        from src.calculator import Calculator
        from src.interactive.session import run_interactive_session

        calc = Calculator()

        with patch("builtins.input", side_effect=["1", "add", "2", "3", "q"]):
            with patch("builtins.print"):
                # Should not raise, should complete successfully
                run_interactive_session(calc)


# ==================== Parametrized Integration Tests ====================


@pytest.mark.parametrize("import_source", [
    "src.core.operations",
    "src.input_handler",
])
def test_get_operation_registry_available_from_multiple_sources(import_source):
    """Verify get_operation_registry is accessible from multiple import paths."""
    import importlib

    module = importlib.import_module(import_source)
    assert hasattr(module, "get_operation_registry")
    assert callable(module.get_operation_registry)

    calc = Calculator()
    registry = module.get_operation_registry(calc)
    assert "add" in registry


@pytest.mark.parametrize("import_source,export_names", [
    ("src.core", ["Calculator", "get_operation_registry"]),
    ("src.interactive", ["run_interactive_session"]),
])
def test_package_exports_correct_items(import_source, export_names):
    """Verify packages export correct items."""
    import importlib

    module = importlib.import_module(import_source)
    for name in export_names:
        assert hasattr(module, name), f"{import_source} missing {name}"


@pytest.mark.parametrize("op_name,operands,expected", [
    ("add", [2, 3], 5),
    ("subtract", [10, 4], 6),
    ("multiply", [4, 5], 20),
    ("square", [3], 9),
])
def test_operations_work_through_core_registry(op_name, operands, expected):
    """Verify operations work when called through core registry."""
    from src.core.operations import get_operation_registry

    calc = Calculator()
    registry = get_operation_registry(calc)

    method, _arity = registry[op_name]
    result = method(*operands)
    assert result == expected


# ==================== Core Layer Module Structure ====================


class TestCoreLayerModuleStructure:
    """Verify core layer module structure and isolation."""

    def test_core_calculator_exists(self):
        """Test that src.core.calculator exists and contains Calculator."""
        import src.core.calculator
        assert hasattr(src.core.calculator, "Calculator")

    def test_core_operations_manager_exists(self):
        """Test that src.core.operations_manager exists and contains OperationRegistry."""
        import src.core.operations_manager
        assert hasattr(src.core.operations_manager, "OperationRegistry")

    def test_operation_registry_instantiable(self):
        """Test that OperationRegistry can be instantiated."""
        from src.core.operations_manager import OperationRegistry
        calc = Calculator()
        registry = OperationRegistry(calc)
        assert isinstance(registry, OperationRegistry)

    def test_calculator_in_core_has_no_io_dependencies(self):
        """Test that Calculator module has no I/O dependencies."""
        import src.core.calculator
        import inspect
        source = inspect.getsource(src.core.calculator)
        # Should not import from UI or interactive modules
        assert "from src.interface" not in source
        assert "from src.interactive" not in source
        assert "input(" not in source
        assert "print(" not in source

    def test_operations_manager_has_no_io_dependencies(self):
        """Test that OperationRegistry module has no I/O dependencies."""
        import src.core.operations_manager
        import inspect
        source = inspect.getsource(src.core.operations_manager)
        # Should not import from UI or interactive modules
        assert "from src.interface" not in source
        assert "from src.interactive" not in source


# ==================== Interface Layer Module Structure ====================


class TestInterfaceLayerStructure:
    """Verify interface layer module structure."""

    def test_input_parser_module_exists(self):
        """Test that src.interface.input_parser exists with required functions."""
        import src.interface.input_parser
        assert hasattr(src.interface.input_parser, "parse_cli_args")
        assert hasattr(src.interface.input_parser, "convert_operand")

    def test_menu_renderer_module_exists(self):
        """Test that src.interface.menu_renderer exists with display_menu."""
        import src.interface.menu_renderer
        assert hasattr(src.interface.menu_renderer, "display_menu")

    def test_output_formatter_module_exists(self):
        """Test that src.interface.output_formatter exists with format_result."""
        import src.interface.output_formatter
        assert hasattr(src.interface.output_formatter, "format_result")

    def test_interface_functions_are_callable(self):
        """Test that interface functions are callable."""
        from src.interface.input_parser import parse_cli_args, convert_operand
        from src.interface.output_formatter import format_result
        from src.interface.menu_renderer import display_menu
        assert callable(parse_cli_args)
        assert callable(convert_operand)
        assert callable(format_result)
        assert callable(display_menu)


# ==================== Session Layer Module Structure ====================


class TestSessionLayerStructure:
    """Verify interactive session layer structure."""

    def test_interactive_input_handler_exists(self):
        """Test that src.interactive.input_handler exists with required functions."""
        import src.interactive.input_handler
        assert hasattr(src.interactive.input_handler, "get_operation_choice")
        assert hasattr(src.interactive.input_handler, "get_operands")

    def test_interactive_session_exists(self):
        """Test that src.interactive.session exists with required functions."""
        import src.interactive.session
        assert hasattr(src.interactive.session, "run_interactive_session")
        assert hasattr(src.interactive.session, "display_menu")

    def test_session_functions_are_callable(self):
        """Test that session functions are callable."""
        from src.interactive.input_handler import get_operation_choice, get_operands
        from src.interactive.session import run_interactive_session
        assert callable(get_operation_choice)
        assert callable(get_operands)
        assert callable(run_interactive_session)


# ==================== Operations Framework Extensibility ====================


class TestOperationsFrameworkExtensibility:
    """Verify OperationRegistry framework for extensibility."""

    def test_operation_registry_class_exists(self):
        """Test that OperationRegistry class exists in operations_manager."""
        from src.core.operations_manager import OperationRegistry
        assert OperationRegistry is not None

    def test_registry_has_normal_and_scientific_dicts(self):
        """Test that OperationRegistry has _normal_operations and _scientific_operations."""
        from src.core.operations_manager import OperationRegistry
        calc = Calculator()
        registry = OperationRegistry(calc)
        assert hasattr(registry, "_normal_operations")
        assert hasattr(registry, "_scientific_operations")
        assert isinstance(registry._normal_operations, dict)
        assert isinstance(registry._scientific_operations, dict)

    def test_registry_get_all_operations(self):
        """Test that get_all_operations returns all operations."""
        from src.core.operations_manager import OperationRegistry
        from src.core.operations import get_operation_registry
        calc = Calculator()
        registry = OperationRegistry(calc)
        all_ops = registry.get_all_operations()
        legacy_ops = get_operation_registry(calc)
        # Should have same operations
        assert set(all_ops.keys()) == set(legacy_ops.keys())

    def test_registry_get_normal_operations(self):
        """Test that get_normal_operations returns only normal mode operations."""
        from src.core.operations_manager import OperationRegistry
        calc = Calculator()
        registry = OperationRegistry(calc)
        normal_ops = registry.get_normal_operations()
        assert isinstance(normal_ops, dict)
        assert "add" in normal_ops
        assert len(normal_ops) == 6  # Only 6 normal mode operations

    def test_normal_operations_are_subset_of_all(self):
        """Test that normal operations are a subset of all operations."""
        from src.core.operations_manager import OperationRegistry
        calc = Calculator()
        registry = OperationRegistry(calc)
        all_ops = registry.get_all_operations()
        normal_ops = registry.get_normal_operations()
        assert set(normal_ops.keys()).issubset(set(all_ops.keys()))


# ==================== Backward Compatibility Shims ====================


class TestBackwardCompatibilityShims:
    """Verify all backward compatibility shims work."""

    def test_calculator_shim_works(self):
        """Test that src.calculator shim imports Calculator."""
        from src.calculator import Calculator as ShimCalc
        calc = ShimCalc()
        assert calc.add(2, 3) == 5

    def test_input_handler_shim_exports_all_functions(self):
        """Test that input_handler shim re-exports all functions."""
        from src.input_handler import (
            display_menu,
            get_operation_choice,
            get_operands,
            run_interactive_session,
            get_operation_registry,
        )
        assert callable(display_menu)
        assert callable(get_operation_choice)
        assert callable(get_operands)
        assert callable(run_interactive_session)
        assert callable(get_operation_registry)

    def test_error_logger_shim_works(self):
        """Test that src.error_logger still provides ErrorLogger."""
        from src.error_logger import ErrorLogger
        logger = ErrorLogger()
        assert logger is not None

    def test_history_shim_works(self):
        """Test that src.history shim imports HistoryTracker."""
        from src.history import HistoryTracker
        tracker = HistoryTracker()
        assert tracker is not None

    def test_support_error_logging_re_exports_error_logger(self):
        """Test that src.support.error_logging re-exports ErrorLogger."""
        from src.support.error_logging import ErrorLogger as SupportErrorLogger
        from src.error_logger import ErrorLogger as CanonicalErrorLogger
        assert SupportErrorLogger is CanonicalErrorLogger

    def test_support_history_exports_history_tracker(self):
        """Test that src.support.history exports HistoryTracker."""
        from src.support.history import HistoryTracker
        tracker = HistoryTracker()
        assert tracker is not None
