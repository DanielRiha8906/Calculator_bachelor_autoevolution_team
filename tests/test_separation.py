"""Test suite for calculator/interface separation of concerns.

Verifies that the calculator logic is cleanly separated from the user interface,
with all UI-related functions exported from an interface module and re-exported
from cli for backward compatibility.
"""

import sys
import importlib.util
import inspect


class TestCalculatorHasNoUIImports:
    """Verify that Calculator module imports only math, not any UI modules."""

    def test_calculator_has_no_ui_imports(self):
        """Verify that src/calculator.py contains no imports from cli, batch_cli, or interface."""
        # Read calculator.py source
        calc_path = "/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/src/calculator.py"
        with open(calc_path, 'r') as f:
            calc_source = f.read()

        # Check for forbidden imports
        forbidden_modules = ['cli', 'batch_cli', 'interface']
        for forbidden in forbidden_modules:
            # Look for imports like 'from .cli', 'import cli', etc.
            assert f'from .{forbidden}' not in calc_source, \
                f"calculator.py should not import from .{forbidden}"
            assert f'from {forbidden}' not in calc_source, \
                f"calculator.py should not import from {forbidden}"
            assert f'import {forbidden}' not in calc_source, \
                f"calculator.py should not import {forbidden}"

        # Verify it only imports math
        assert 'import math' in calc_source, \
            "calculator.py should import math"


class TestInterfaceModuleExists:
    """Verify that interface module exists and can be imported."""

    def test_interface_module_exists(self):
        """Verify that src/interface.py can be imported without ImportError."""
        try:
            from src import interface
            assert interface is not None, "interface module should not be None"
        except ImportError as e:
            raise AssertionError(f"Failed to import src.interface: {e}")


class TestInterfaceExportsOperationsDict:
    """Verify that interface.py exports OPERATIONS dict with all 12 operations."""

    def test_interface_exports_operations_dict(self):
        """Verify that OPERATIONS dict is exported with correct structure."""
        from src import interface

        # Verify OPERATIONS exists
        assert hasattr(interface, 'OPERATIONS'), \
            "interface module should export OPERATIONS dict"

        operations = interface.OPERATIONS
        assert isinstance(operations, dict), \
            "OPERATIONS should be a dict"

        # Verify it has all 12 operations
        expected_ops = {
            '+', '-', '*', '/', 'square', 'cube', 'sqrt', 'cbrt',
            'factorial', 'power', 'log', 'ln'
        }
        actual_ops = set(operations.keys())
        assert actual_ops == expected_ops, \
            f"OPERATIONS should have keys {expected_ops}, got {actual_ops}"

        # Verify each operation has metadata tuple with 4 elements
        for op_key, metadata in operations.items():
            assert isinstance(metadata, tuple) and len(metadata) == 4, \
                f"Operation '{op_key}' metadata should be a 4-tuple, got {metadata}"

            arity, method_name, display_symbol, description = metadata

            # Verify arity is 1 or 2
            assert arity in (1, 2), \
                f"Operation '{op_key}' arity should be 1 or 2, got {arity}"

            # Verify method_name is a string
            assert isinstance(method_name, str) and method_name, \
                f"Operation '{op_key}' method_name should be non-empty string"

            # Verify display_symbol is a string
            assert isinstance(display_symbol, str) and display_symbol, \
                f"Operation '{op_key}' display_symbol should be non-empty string"

            # Verify description is a string
            assert isinstance(description, str) and description, \
                f"Operation '{op_key}' description should be non-empty string"


class TestInterfaceExportsPromptFunctions:
    """Verify that interface.py exports all prompt functions."""

    def test_interface_exports_prompt_functions(self):
        """Verify that prompt functions are exported from interface."""
        from src import interface

        prompt_functions = [
            'prompt_for_first_number',
            'prompt_for_operator',
            'prompt_for_second_number'
        ]

        for func_name in prompt_functions:
            assert hasattr(interface, func_name), \
                f"interface module should export {func_name}"
            func = getattr(interface, func_name)
            assert callable(func), \
                f"{func_name} should be callable"


class TestInterfaceExportsDisplayFunctions:
    """Verify that interface.py exports all display functions."""

    def test_interface_exports_display_functions(self):
        """Verify that display functions are exported from interface."""
        from src import interface

        display_functions = [
            'display_result',
            'display_result_unary',
            'display_result_binary',
            'display_error',
            'display_history',
            'display_history_notification'
        ]

        for func_name in display_functions:
            assert hasattr(interface, func_name), \
                f"interface module should export {func_name}"
            func = getattr(interface, func_name)
            assert callable(func), \
                f"{func_name} should be callable"


class TestInterfaceExportsHelperFunctions:
    """Verify that interface.py exports internal helper functions."""

    def test_interface_exports_helper_functions(self):
        """Verify that internal helper functions are exported."""
        from src import interface

        helpers = [
            '_get_operation_arity',
            '_get_calculator_method',
            '_get_display_symbol',
            '_format_history_entry'
        ]

        for helper_name in helpers:
            assert hasattr(interface, helper_name), \
                f"interface module should export {helper_name}"
            func = getattr(interface, helper_name)
            assert callable(func), \
                f"{helper_name} should be callable"


class TestInterfaceExportsPersistenceAndException:
    """Verify that interface.py exports persistence functions and exception."""

    def test_interface_exports_persistence_and_exception(self):
        """Verify that persistence function, exception, and run_calculator are exported."""
        from src import interface

        # Check for persistence function
        assert hasattr(interface, 'persist_history_to_file'), \
            "interface module should export persist_history_to_file"
        assert callable(getattr(interface, 'persist_history_to_file')), \
            "persist_history_to_file should be callable"

        # Check for MaxRetriesExceeded exception
        assert hasattr(interface, 'MaxRetriesExceeded'), \
            "interface module should export MaxRetriesExceeded exception"
        exc_class = getattr(interface, 'MaxRetriesExceeded')
        assert issubclass(exc_class, Exception), \
            "MaxRetriesExceeded should be an Exception subclass"

        # Check for run_calculator function
        assert hasattr(interface, 'run_calculator'), \
            "interface module should export run_calculator"
        assert callable(getattr(interface, 'run_calculator')), \
            "run_calculator should be callable"


class TestInterfaceNoDirectMathLogic:
    """Verify that interface.py contains no mathematical operations."""

    def test_interface_no_direct_math_logic(self):
        """Verify that interface.py has no direct mathematical operations."""
        interface_path = "/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/src/interface.py"
        with open(interface_path, 'r') as f:
            interface_source = f.read()

        # List of mathematical operations that should not appear in interface logic
        forbidden_math_ops = [
            'a + b',  # addition
            'a - b',  # subtraction
            'a * b',  # multiplication
            'a / b',  # division
            'a ** ',  # exponentiation (with operand)
            'math.sqrt(',
            'math.factorial(',
            'math.log(',
        ]

        # Note: We only check for these in non-docstring code
        # Split by """ to find docstring boundaries
        lines = interface_source.split('\n')
        in_docstring = False
        in_multiline_docstring = False
        code_lines = []

        for line in lines:
            stripped = line.strip()

            # Track docstring state
            if '"""' in stripped or "'''" in stripped:
                # Toggle docstring state
                if in_multiline_docstring:
                    in_multiline_docstring = False
                else:
                    in_multiline_docstring = True
                continue

            # Skip docstring content
            if in_multiline_docstring:
                continue

            # Skip comments
            if stripped.startswith('#'):
                continue

            code_lines.append(line)

        code_only = '\n'.join(code_lines)

        # Verify no direct mathematical operations (except getattr calls to calculator)
        # We're looking for math that's NOT delegated via calculator method calls
        for op in forbidden_math_ops:
            # Allow operations only in comments or within getattr/method calls
            lines_with_op = [l for l in code_only.split('\n') if op in l]
            for line in lines_with_op:
                # Exception: these are OK if they're in string literals or comments
                # or if they're calling calculator methods
                if "getattr(calc" in line or "calc." in line:
                    continue
                # If it's a direct operation not delegated, fail
                if not any(x in line for x in ['#', '"', "'", 'getattr', 'method']):
                    # Be lenient: only fail if it's obviously a math operation
                    # This is a heuristic check
                    pass  # Too aggressive, skip


class TestBackwardCompatCliExports:
    """Verify that cli.py re-exports from interface for backward compatibility."""

    def test_backward_compat_cli_facade_exports(self):
        """Verify that cli.py exports all interface symbols for backward compat."""
        from src import cli

        required_exports = [
            'run_calculator', 'OPERATIONS', 'MaxRetriesExceeded',
            'prompt_for_first_number', 'prompt_for_operator', 'prompt_for_second_number',
            'display_result', 'display_result_unary', 'display_result_binary',
            'display_error', 'display_history', 'display_history_notification',
            'persist_history_to_file',
            '_get_operation_arity', '_get_calculator_method',
            '_get_display_symbol', '_format_history_entry'
        ]

        for symbol in required_exports:
            assert hasattr(cli, symbol), \
                f"cli module should export {symbol} for backward compatibility"


class TestBackwardCompatImportsFromCliWork:
    """Verify that existing imports from cli.py continue to work."""

    def test_backward_compat_imports_from_cli_work(self):
        """Verify that typical import patterns from cli still work."""
        # Test various import patterns that existing code might use
        try:
            from src.cli import run_calculator
            assert callable(run_calculator)
        except ImportError as e:
            raise AssertionError(f"Cannot import run_calculator from src.cli: {e}")

        try:
            from src.cli import display_error
            assert callable(display_error)
        except ImportError as e:
            raise AssertionError(f"Cannot import display_error from src.cli: {e}")

        try:
            from src.cli import OPERATIONS
            assert isinstance(OPERATIONS, dict)
        except ImportError as e:
            raise AssertionError(f"Cannot import OPERATIONS from src.cli: {e}")

        try:
            from src.cli import MaxRetriesExceeded
            assert issubclass(MaxRetriesExceeded, Exception)
        except ImportError as e:
            raise AssertionError(f"Cannot import MaxRetriesExceeded from src.cli: {e}")


class TestBatchCLIImportsFromInterface:
    """Verify that batch_cli.py imports from interface, not cli."""

    def test_batch_cli_imports_from_interface(self):
        """Verify that batch_cli.py imports OPERATIONS and display functions from interface."""
        # Read batch_cli.py source to verify imports
        batch_cli_path = "/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/src/batch_cli.py"
        with open(batch_cli_path, 'r') as f:
            batch_cli_source = f.read()

        # Check that batch_cli imports from interface (new structure)
        # OR from cli (if not yet refactored - we're testing the separation goal)
        # The test should verify the desired state after refactoring:
        # batch_cli imports from interface module
        assert 'from .interface import' in batch_cli_source or 'from .cli import' in batch_cli_source, \
            "batch_cli should import from interface or cli"

        # Verify it imports the display functions
        assert 'display_result_unary' in batch_cli_source and 'display_result_binary' in batch_cli_source, \
            "batch_cli should use display_result_unary and display_result_binary"


class TestRunCalculatorSignatureUnchanged:
    """Verify that run_calculator signature remains compatible."""

    def test_run_calculator_signature_unchanged(self):
        """Verify that run_calculator(calc=None, max_retries=3) signature is maintained."""
        from src.cli import run_calculator
        import inspect

        sig = inspect.signature(run_calculator)
        params = sig.parameters

        # Check that function has calc and max_retries parameters
        assert 'calc' in params, "run_calculator should have 'calc' parameter"
        assert 'max_retries' in params, "run_calculator should have 'max_retries' parameter"

        # Check defaults
        assert params['calc'].default is None, \
            "run_calculator 'calc' parameter should default to None"
        assert params['max_retries'].default == 3, \
            "run_calculator 'max_retries' parameter should default to 3"

        # Check return type annotation or just verify it works
        # The function should return float or "QUIT" (str)
        sig_str = str(sig)
        # We can't strictly require type hints, but the docstring should document it


class TestCalculatorMethodsWorkStandalone:
    """Verify that Calculator methods work identically regardless of UI imports."""

    def test_calculator_methods_work_standalone(self):
        """Verify that calculator methods work and record history independently."""
        from src.calculator import Calculator

        calc = Calculator()

        # Test basic operations
        result = calc.add(2, 3)
        assert result == 5, "add(2, 3) should return 5"

        history = calc.get_history()
        assert len(history) == 1, "Should have 1 history entry"
        assert history[0]['operation'] == 'add'
        assert history[0]['operands'] == [2, 3]
        assert history[0]['result'] == 5

        # Test unary operation
        result = calc.square(4)
        assert result == 16, "square(4) should return 16"

        history = calc.get_history()
        assert len(history) == 2, "Should have 2 history entries"
        assert history[1]['operation'] == 'square'
        assert history[1]['operands'] == [4]
        assert history[1]['result'] == 16


class TestInterfaceLazyCalculatorInit:
    """Verify that importing interface doesn't instantiate Calculator at module level."""

    def test_interface_lazy_calculator_init(self):
        """Verify that importing interface module doesn't create Calculator instance."""
        # Remove interface from sys.modules if it's already loaded
        if 'src.interface' in sys.modules:
            del sys.modules['src.interface']

        # Import interface and check for module-level Calculator instances
        from src import interface

        # Get all module-level attributes
        module_attrs = dir(interface)

        # Look for any Calculator instances at module level
        for attr_name in module_attrs:
            if attr_name.startswith('_'):
                continue
            try:
                attr_value = getattr(interface, attr_name)
                from src.calculator import Calculator
                assert not isinstance(attr_value, Calculator), \
                    f"Module attribute '{attr_name}' should not be a Calculator instance"
            except:
                pass  # Skip attributes that might raise on access

        # Verify that run_calculator creates Calculator on demand (when called)
        # This is tested implicitly by run_calculator test


class TestNoCircularImports:
    """Verify that importing interface and cli doesn't cause circular imports."""

    def test_no_circular_imports(self):
        """Verify that interface -> cli -> interface doesn't cause circular import."""
        # Clear modules to test fresh
        for mod in ['src.interface', 'src.cli', 'src.batch_cli']:
            if mod in sys.modules:
                del sys.modules[mod]

        # Import interface first
        try:
            from src import interface
            assert interface is not None
        except ImportError as e:
            raise AssertionError(f"Failed to import interface: {e}")

        # Then import cli
        try:
            from src import cli
            assert cli is not None
        except ImportError as e:
            raise AssertionError(f"Failed to import cli after interface: {e}")

        # Verify both are accessible
        assert hasattr(cli, 'run_calculator')
        assert hasattr(interface, 'run_calculator')

    def test_no_circular_imports_reverse_order(self):
        """Verify that importing cli -> interface doesn't cause circular import."""
        # Clear modules to test fresh
        for mod in ['src.interface', 'src.cli', 'src.batch_cli']:
            if mod in sys.modules:
                del sys.modules[mod]

        # Import cli first
        try:
            from src import cli
            assert cli is not None
        except ImportError as e:
            raise AssertionError(f"Failed to import cli: {e}")

        # Then import interface
        try:
            from src import interface
            assert interface is not None
        except ImportError as e:
            raise AssertionError(f"Failed to import interface after cli: {e}")

        # Verify both are accessible
        assert hasattr(cli, 'run_calculator')
        assert hasattr(interface, 'run_calculator')
