"""Tests for the modularized calculator structure.

Verifies that the refactoring from a flat src/ structure to a modularized
subpackage structure (core/, operations/, shared/, session/, interface/) works
correctly, including backwards compatibility shims.
"""

import pytest
import sys


# ============================================================================
# Task B.1: Test all new module imports work correctly
# ============================================================================


class TestNewModuleImports:
    """Verify imports from new modularized subpackages."""

    def test_import_calculator_from_core_package(self):
        """Can import Calculator from src.core package."""
        from src.core import Calculator
        assert Calculator is not None
        assert callable(Calculator)

    def test_import_calculator_directly_from_core_module(self):
        """Can import Calculator from src.core.calculator module."""
        from src.core.calculator import Calculator
        assert Calculator is not None
        assert callable(Calculator)

    def test_import_operations_from_operations_package(self):
        """Can import OPERATIONS from src.operations package."""
        from src.operations import OPERATIONS
        assert isinstance(OPERATIONS, dict)
        assert len(OPERATIONS) > 0

    def test_import_normal_operations_from_operations_submodule(self):
        """Can import NORMAL_OPERATIONS from src.operations.normal."""
        from src.operations.normal import NORMAL_OPERATIONS
        assert isinstance(NORMAL_OPERATIONS, dict)
        assert len(NORMAL_OPERATIONS) > 0

    def test_import_scientific_operations_from_operations_submodule(self):
        """Can import SCIENTIFIC_OPERATIONS from src.operations.scientific."""
        from src.operations.scientific import SCIENTIFIC_OPERATIONS
        assert isinstance(SCIENTIFIC_OPERATIONS, dict)

    def test_import_dispatcher_from_shared_package(self):
        """Can import OperationDispatcher from src.shared package."""
        from src.shared import OperationDispatcher
        assert OperationDispatcher is not None
        assert callable(OperationDispatcher)

    def test_import_dispatcher_directly_from_shared_module(self):
        """Can import OperationDispatcher from src.shared.dispatcher."""
        from src.shared.dispatcher import OperationDispatcher
        assert OperationDispatcher is not None
        assert callable(OperationDispatcher)

    def test_import_logger_from_shared_package(self):
        """Can import Logger from src.shared package."""
        from src.shared import Logger
        assert Logger is not None
        assert callable(Logger)

    def test_import_logger_directly_from_shared_module(self):
        """Can import Logger from src.shared.logger."""
        from src.shared.logger import Logger
        assert Logger is not None
        assert callable(Logger)

    def test_import_input_handler_from_session_package(self):
        """Can import InputHandler from src.session package."""
        from src.session import InputHandler
        assert InputHandler is not None
        assert callable(InputHandler)

    def test_import_run_session_from_session_package(self):
        """Can import run_session from src.session package."""
        from src.session import run_session
        assert run_session is not None
        assert callable(run_session)

    def test_import_history_from_session_submodule(self):
        """Can import History from src.session.history."""
        from src.session.history import History
        assert History is not None
        assert callable(History)

    def test_import_input_handler_directly_from_session_module(self):
        """Can import InputHandler directly from src.session.input_handler."""
        from src.session.input_handler import InputHandler
        assert InputHandler is not None
        assert callable(InputHandler)

    def test_import_cli_dispatcher_from_interface_package(self):
        """Can import CliDispatcher from src.interface package."""
        from src.interface import CliDispatcher
        assert CliDispatcher is not None
        assert callable(CliDispatcher)

    def test_import_cli_dispatcher_directly_from_interface_module(self):
        """Can import CliDispatcher directly from src.interface.cli."""
        from src.interface.cli import CliDispatcher
        assert CliDispatcher is not None
        assert callable(CliDispatcher)


# ============================================================================
# Task B.2: Test OPERATIONS dict contains all 12 expected operation keys
# ============================================================================


class TestOperationsDictStructure:
    """Verify OPERATIONS dict structure and contents."""

    EXPECTED_KEYS = {
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
        "log10",
        "ln",
    }

    def test_operations_has_all_12_keys(self):
        """OPERATIONS dict contains all 12 normal operation keys (plus scientific)."""
        from src.operations import OPERATIONS
        # OPERATIONS now has 12 normal + 8 scientific = 20 total
        assert len(OPERATIONS) == 20
        # All normal keys must be present
        assert self.EXPECTED_KEYS.issubset(set(OPERATIONS.keys()))

    @pytest.mark.parametrize("key", EXPECTED_KEYS)
    def test_operations_key_exists(self, key):
        """Each expected operation key exists in OPERATIONS."""
        from src.operations import OPERATIONS
        assert key in OPERATIONS

    @pytest.mark.parametrize("key", EXPECTED_KEYS)
    def test_operations_key_is_dict(self, key):
        """Each operation entry is a dict."""
        from src.operations import OPERATIONS
        assert isinstance(OPERATIONS[key], dict)

    @pytest.mark.parametrize("key", EXPECTED_KEYS)
    def test_operations_key_has_method(self, key):
        """Each operation has a 'method' field."""
        from src.operations import OPERATIONS
        assert "method" in OPERATIONS[key]

    @pytest.mark.parametrize("key", EXPECTED_KEYS)
    def test_operations_key_has_arity(self, key):
        """Each operation has an 'arity' field."""
        from src.operations import OPERATIONS
        assert "arity" in OPERATIONS[key]

    @pytest.mark.parametrize("key", EXPECTED_KEYS)
    def test_operations_key_has_label(self, key):
        """Each operation has a 'label' field."""
        from src.operations import OPERATIONS
        assert "label" in OPERATIONS[key]


# ============================================================================
# Task B.3: Test SCIENTIFIC_OPERATIONS is an empty dict
# ============================================================================


class TestScientificOperations:
    """Verify SCIENTIFIC_OPERATIONS structure."""

    def test_scientific_operations_is_dict(self):
        """SCIENTIFIC_OPERATIONS is a dict."""
        from src.operations import SCIENTIFIC_OPERATIONS
        assert isinstance(SCIENTIFIC_OPERATIONS, dict)

    def test_scientific_operations_is_empty(self):
        """SCIENTIFIC_OPERATIONS now has 8 entries (sin, cos, tan, asin, acos, atan, pi, e)."""
        from src.operations import SCIENTIFIC_OPERATIONS
        assert len(SCIENTIFIC_OPERATIONS) == 8
        expected_keys = {"sin", "cos", "tan", "asin", "acos", "atan", "pi", "e"}
        assert set(SCIENTIFIC_OPERATIONS.keys()) == expected_keys


# ============================================================================
# Task B.4: Test NORMAL_OPERATIONS merged correctly
# ============================================================================


class TestOperationsMerge:
    """Verify OPERATIONS is the correct merge of NORMAL + SCIENTIFIC."""

    def test_operations_is_union_of_normal_and_scientific(self):
        """OPERATIONS is the union of NORMAL_OPERATIONS and SCIENTIFIC_OPERATIONS."""
        from src.operations import OPERATIONS, NORMAL_OPERATIONS, SCIENTIFIC_OPERATIONS
        # OPERATIONS should have all normal + all scientific keys
        assert len(SCIENTIFIC_OPERATIONS) == 8
        assert len(OPERATIONS) == len(NORMAL_OPERATIONS) + len(SCIENTIFIC_OPERATIONS)
        assert set(OPERATIONS.keys()) == set(NORMAL_OPERATIONS.keys()) | set(SCIENTIFIC_OPERATIONS.keys())

    def test_normal_operations_has_12_entries(self):
        """NORMAL_OPERATIONS has all 12 operations."""
        from src.operations import NORMAL_OPERATIONS
        assert len(NORMAL_OPERATIONS) == 12

    def test_operations_union_composition(self):
        """OPERATIONS correctly merges NORMAL and SCIENTIFIC entries."""
        from src.operations import OPERATIONS, NORMAL_OPERATIONS, SCIENTIFIC_OPERATIONS
        # All NORMAL_OPERATIONS keys should be in OPERATIONS
        for key in NORMAL_OPERATIONS:
            assert key in OPERATIONS
            assert OPERATIONS[key] == NORMAL_OPERATIONS[key]
        # All SCIENTIFIC_OPERATIONS keys should be in OPERATIONS
        for key in SCIENTIFIC_OPERATIONS:
            assert key in OPERATIONS
            assert OPERATIONS[key] == SCIENTIFIC_OPERATIONS[key]


# ============================================================================
# Task B.5: Test backwards compatibility - main src exports
# ============================================================================


class TestBackwardsCompatibilityMainExports:
    """Verify backwards compat: src.__init__ exports all key classes."""

    def test_calculator_importable_from_src(self):
        """Calculator importable from src."""
        from src import Calculator
        assert Calculator is not None
        assert callable(Calculator)

    def test_operations_importable_from_src(self):
        """OPERATIONS importable from src."""
        from src import OPERATIONS
        assert isinstance(OPERATIONS, dict)
        assert len(OPERATIONS) == 20

    def test_cli_dispatcher_importable_from_src(self):
        """CliDispatcher importable from src."""
        from src import CliDispatcher
        assert CliDispatcher is not None
        assert callable(CliDispatcher)

    def test_logger_importable_from_src(self):
        """Logger importable from src."""
        from src import Logger
        assert Logger is not None
        assert callable(Logger)

    def test_operation_dispatcher_importable_from_src(self):
        """OperationDispatcher importable from src."""
        from src import OperationDispatcher
        assert OperationDispatcher is not None
        assert callable(OperationDispatcher)

    def test_src_all_exports_all_five_classes(self):
        """src.__all__ includes all 5 key exports."""
        import src
        expected = {"Calculator", "CliDispatcher", "Logger", "OperationDispatcher", "OPERATIONS"}
        assert set(src.__all__) == expected


# ============================================================================
# Task B.6: Test backwards compatibility shims
# ============================================================================


class TestBackwardsCompatibilityShims:
    """Verify backwards compat shims resolve correctly."""

    def test_calculator_from_old_location(self):
        """Can still import Calculator from src.calculator (shim)."""
        from src.calculator import Calculator
        assert Calculator is not None
        assert callable(Calculator)

    def test_cli_dispatcher_from_old_location(self):
        """Can still import CliDispatcher from src.cli (shim)."""
        from src.cli import CliDispatcher
        assert CliDispatcher is not None
        assert callable(CliDispatcher)

    def test_input_handler_from_old_location(self):
        """Can still import InputHandler from src.input_handler (shim)."""
        from src.input_handler import InputHandler
        assert InputHandler is not None
        assert callable(InputHandler)

    def test_run_session_from_old_location(self):
        """Can still import run_session from src.input_handler (shim)."""
        from src.input_handler import run_session
        assert run_session is not None
        assert callable(run_session)

    def test_operations_from_old_location(self):
        """Can still import OPERATIONS from src.input_handler (shim)."""
        from src.input_handler import OPERATIONS
        assert isinstance(OPERATIONS, dict)
        assert len(OPERATIONS) == 20

    def test_max_retries_from_old_location(self):
        """Can still import MAX_RETRIES from src.input_handler (shim)."""
        from src.input_handler import MAX_RETRIES
        assert isinstance(MAX_RETRIES, int)
        assert MAX_RETRIES > 0

    def test_dispatcher_from_old_location(self):
        """Can still import OperationDispatcher from src.dispatcher (shim)."""
        from src.dispatcher import OperationDispatcher
        assert OperationDispatcher is not None
        assert callable(OperationDispatcher)

    def test_logger_from_old_location(self):
        """Can still import Logger from src.logger (shim)."""
        from src.logger import Logger
        assert Logger is not None
        assert callable(Logger)

    def test_history_from_old_location(self):
        """Can still import History from src.history (shim)."""
        from src.history import History
        assert History is not None
        assert callable(History)


# ============================================================================
# Task B.7: Test Calculator methods work from new location
# ============================================================================


class TestCalculatorMethodsFromNewLocation:
    """Verify Calculator class methods work correctly from new location."""

    def test_calculator_add(self):
        """Calculator.add works correctly from new location."""
        from src.core import Calculator
        calc = Calculator()
        assert calc.add(2, 3) == 5
        assert calc.add(-1, 1) == 0
        assert calc.add(0.5, 0.5) == 1.0

    def test_calculator_subtract(self):
        """Calculator.subtract works correctly."""
        from src.core import Calculator
        calc = Calculator()
        assert calc.subtract(5, 3) == 2
        assert calc.subtract(0, 0) == 0

    def test_calculator_multiply(self):
        """Calculator.multiply works correctly."""
        from src.core import Calculator
        calc = Calculator()
        assert calc.multiply(3, 4) == 12
        assert calc.multiply(0, 100) == 0

    def test_calculator_divide(self):
        """Calculator.divide works correctly."""
        from src.core import Calculator
        calc = Calculator()
        assert calc.divide(10, 2) == 5.0
        assert calc.divide(1, 2) == 0.5

    def test_calculator_divide_by_zero_raises_exception(self):
        """Calculator.divide raises ZeroDivisionError on division by zero."""
        from src.core import Calculator
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(10, 0)

    def test_calculator_factorial(self):
        """Calculator.factorial works correctly."""
        from src.core import Calculator
        calc = Calculator()
        assert calc.factorial(0) == 1
        assert calc.factorial(1) == 1
        assert calc.factorial(5) == 120
        assert calc.factorial(10) == 3628800

    def test_calculator_factorial_negative_raises_error(self):
        """Calculator.factorial raises ValueError for negative input."""
        from src.core import Calculator
        calc = Calculator()
        with pytest.raises(ValueError):
            calc.factorial(-1)

    def test_calculator_factorial_boolean_raises_error(self):
        """Calculator.factorial raises TypeError for boolean input."""
        from src.core import Calculator
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.factorial(True)

    def test_calculator_square(self):
        """Calculator.square works correctly."""
        from src.core import Calculator
        calc = Calculator()
        assert calc.square(2) == 4
        assert calc.square(0) == 0
        assert calc.square(-3) == 9

    def test_calculator_cube(self):
        """Calculator.cube works correctly."""
        from src.core import Calculator
        calc = Calculator()
        assert calc.cube(2) == 8
        assert calc.cube(0) == 0
        assert calc.cube(-2) == -8

    def test_calculator_square_root(self):
        """Calculator.square_root works correctly."""
        from src.core import Calculator
        calc = Calculator()
        assert calc.square_root(4) == 2.0
        assert calc.square_root(0) == 0.0
        assert calc.square_root(1) == 1.0

    def test_calculator_cube_root(self):
        """Calculator.cube_root works correctly."""
        from src.core import Calculator
        calc = Calculator()
        assert calc.cube_root(8) == 2.0
        assert calc.cube_root(0) == 0.0

    def test_calculator_power(self):
        """Calculator.power works correctly."""
        from src.core import Calculator
        calc = Calculator()
        assert calc.power(2, 3) == 8
        assert calc.power(5, 0) == 1

    def test_calculator_log10(self):
        """Calculator.log10 works correctly."""
        from src.core import Calculator
        calc = Calculator()
        assert calc.log10(10) == 1.0
        assert calc.log10(100) == 2.0

    def test_calculator_ln(self):
        """Calculator.ln (natural log) works correctly."""
        from src.core import Calculator
        calc = Calculator()
        assert abs(calc.ln(2.718281828) - 1.0) < 0.0001


# ============================================================================
# Task B.8: Test module identity - same class from different imports
# ============================================================================


class TestModuleIdentity:
    """Verify module identity: same class from different import paths."""

    def test_calculator_identity_new_vs_shim(self):
        """Calculator from new location is same class as from shim."""
        from src.core.calculator import Calculator as CalcNewLocation
        from src.calculator import Calculator as CalcShim
        assert CalcNewLocation is CalcShim

    def test_calculator_identity_package_vs_direct(self):
        """Calculator from package is same as from direct module import."""
        from src.core import Calculator as CalcPackage
        from src.core.calculator import Calculator as CalcDirect
        assert CalcPackage is CalcDirect

    def test_calculator_identity_main_vs_new(self):
        """Calculator from src is same as from src.core."""
        from src import Calculator as CalcMain
        from src.core import Calculator as CalcNew
        assert CalcMain is CalcNew

    def test_dispatcher_identity_new_vs_shim(self):
        """OperationDispatcher from new location is same as from shim."""
        from src.shared.dispatcher import OperationDispatcher as DispatcherNew
        from src.dispatcher import OperationDispatcher as DispatcherShim
        assert DispatcherNew is DispatcherShim

    def test_dispatcher_identity_package_vs_direct(self):
        """OperationDispatcher from package is same as from direct module."""
        from src.shared import OperationDispatcher as DispatcherPackage
        from src.shared.dispatcher import OperationDispatcher as DispatcherDirect
        assert DispatcherPackage is DispatcherDirect

    def test_logger_identity_new_vs_shim(self):
        """Logger from new location is same as from shim."""
        from src.shared.logger import Logger as LoggerNew
        from src.logger import Logger as LoggerShim
        assert LoggerNew is LoggerShim

    def test_logger_identity_package_vs_direct(self):
        """Logger from package is same as from direct module."""
        from src.shared import Logger as LoggerPackage
        from src.shared.logger import Logger as LoggerDirect
        assert LoggerPackage is LoggerDirect

    def test_cli_dispatcher_identity_new_vs_shim(self):
        """CliDispatcher from new location is same as from shim."""
        from src.interface.cli import CliDispatcher as CliNew
        from src.cli import CliDispatcher as CliShim
        assert CliNew is CliShim

    def test_cli_dispatcher_identity_package_vs_direct(self):
        """CliDispatcher from package is same as from direct module."""
        from src.interface import CliDispatcher as CliPackage
        from src.interface.cli import CliDispatcher as CliDirect
        assert CliPackage is CliDirect

    def test_input_handler_identity_new_vs_shim(self):
        """InputHandler from new location is same as from shim."""
        from src.session.input_handler import InputHandler as HandlerNew
        from src.input_handler import InputHandler as HandlerShim
        assert HandlerNew is HandlerShim

    def test_input_handler_identity_package_vs_direct(self):
        """InputHandler from package is same as from direct module."""
        from src.session import InputHandler as HandlerPackage
        from src.session.input_handler import InputHandler as HandlerDirect
        assert HandlerPackage is HandlerDirect

    def test_history_identity_new_vs_shim(self):
        """History from new location is same as from shim."""
        from src.session.history import History as HistoryNew
        from src.history import History as HistoryShim
        assert HistoryNew is HistoryShim

    def test_run_session_identity_new_vs_shim(self):
        """run_session function from new location is same as from shim."""
        from src.session.input_handler import run_session as RunNew
        from src.input_handler import run_session as RunShim
        assert RunNew is RunShim


# ============================================================================
# Task B.9: Test __main__ module still works
# ============================================================================


class TestMainModule:
    """Verify src.__main__ module works with updated imports."""

    def test_main_module_has_main_function(self):
        """src.__main__ has a main() function."""
        from src.__main__ import main
        assert callable(main)

    def test_main_module_importable(self):
        """src.__main__ module is importable without errors."""
        import src.__main__
        assert src.__main__ is not None


# ============================================================================
# Task B.10: Integration tests - mix new and old imports in same code
# ============================================================================


class TestMixedImportIntegration:
    """Test that old and new import paths work together in same code."""

    def test_mixed_calculator_imports_same_instance(self):
        """Calculator from old and new paths work together."""
        from src.core import Calculator as NewCalc
        from src.calculator import Calculator as OldCalc

        new_calc = NewCalc()
        old_calc = OldCalc()

        # Both should work and produce same results
        assert new_calc.add(2, 3) == old_calc.add(2, 3) == 5

    def test_mixed_operations_imports_same_dict(self):
        """OPERATIONS from old and new paths are identical."""
        from src.operations import OPERATIONS as NewOps
        from src.input_handler import OPERATIONS as OldOps

        assert NewOps is OldOps
        assert len(NewOps) == 20
        assert len(OldOps) == 20

    def test_mixed_dispatcher_imports_same_class(self):
        """OperationDispatcher from old and new paths work together."""
        from src.shared import OperationDispatcher as NewDispatcher
        from src.dispatcher import OperationDispatcher as OldDispatcher

        # Both should be the same class
        assert NewDispatcher is OldDispatcher


# ============================================================================
# Task B.11: Edge cases - circular imports, lazy evaluation
# ============================================================================


class TestEdgeCasesAndCircularImports:
    """Test edge cases like circular imports and lazy evaluation."""

    def test_all_main_imports_dont_raise(self):
        """Importing all main classes together doesn't raise ImportError."""
        try:
            from src import Calculator, CliDispatcher, Logger, OperationDispatcher, OPERATIONS
            assert all([Calculator, CliDispatcher, Logger, OperationDispatcher, OPERATIONS])
        except ImportError as e:
            pytest.fail(f"Importing all main classes raised ImportError: {e}")

    def test_all_new_subpackage_imports_dont_raise(self):
        """Importing from all new subpackages doesn't raise ImportError."""
        try:
            from src.core import Calculator
            from src.operations import OPERATIONS
            from src.shared import OperationDispatcher, Logger
            from src.session import InputHandler, run_session
            from src.interface import CliDispatcher
            assert all([Calculator, OPERATIONS, OperationDispatcher, Logger, InputHandler, run_session, CliDispatcher])
        except ImportError as e:
            pytest.fail(f"Importing from all subpackages raised ImportError: {e}")

    def test_all_old_shim_imports_dont_raise(self):
        """Importing from all old shim locations doesn't raise ImportError."""
        try:
            from src.calculator import Calculator
            from src.cli import CliDispatcher
            from src.input_handler import InputHandler, run_session, OPERATIONS
            from src.dispatcher import OperationDispatcher
            from src.logger import Logger
            from src.history import History
            assert all([Calculator, CliDispatcher, InputHandler, run_session, OPERATIONS, OperationDispatcher, Logger, History])
        except ImportError as e:
            pytest.fail(f"Importing from all shims raised ImportError: {e}")


# ============================================================================
# Task B.12: OPERATIONS dict completeness and validity
# ============================================================================


class TestOperationsDictValidity:
    """Test OPERATIONS dict is complete and valid."""

    def test_operations_all_values_are_dicts(self):
        """All values in OPERATIONS are dicts."""
        from src.operations import OPERATIONS
        for key, value in OPERATIONS.items():
            assert isinstance(value, dict), f"OPERATIONS[{key!r}] is not a dict"

    def test_operations_all_have_method_field(self):
        """All OPERATIONS entries have 'method' field."""
        from src.operations import OPERATIONS
        for key in OPERATIONS:
            assert "method" in OPERATIONS[key], f"OPERATIONS[{key!r}] missing 'method' field"

    def test_operations_all_have_arity_field(self):
        """All OPERATIONS entries have 'arity' field."""
        from src.operations import OPERATIONS
        for key in OPERATIONS:
            assert "arity" in OPERATIONS[key], f"OPERATIONS[{key!r}] missing 'arity' field"

    def test_operations_all_have_label_field(self):
        """All OPERATIONS entries have 'label' field."""
        from src.operations import OPERATIONS
        for key in OPERATIONS:
            assert "label" in OPERATIONS[key], f"OPERATIONS[{key!r}] missing 'label' field"

    def test_operations_arity_values_are_positive_integers(self):
        """All arity values in OPERATIONS are non-negative integers (0 or 1 or 2)."""
        from src.operations import OPERATIONS
        for key in OPERATIONS:
            arity = OPERATIONS[key]["arity"]
            assert isinstance(arity, int), f"OPERATIONS[{key!r}]['arity'] is not int"
            assert arity >= 0, f"OPERATIONS[{key!r}]['arity'] is not >= 0"
            assert arity in (0, 1, 2), f"OPERATIONS[{key!r}]['arity'] has unexpected value {arity}"

    def test_operations_method_values_are_strings(self):
        """All method values in OPERATIONS are strings."""
        from src.operations import OPERATIONS
        for key in OPERATIONS:
            method = OPERATIONS[key]["method"]
            assert isinstance(method, str), f"OPERATIONS[{key!r}]['method'] is not str"

    def test_operations_label_values_are_strings(self):
        """All label values in OPERATIONS are strings."""
        from src.operations import OPERATIONS
        for key in OPERATIONS:
            label = OPERATIONS[key]["label"]
            assert isinstance(label, str), f"OPERATIONS[{key!r}]['label'] is not str"

    def test_operations_coerce_is_optional_and_callable(self):
        """If 'coerce' field exists in OPERATIONS, it's callable."""
        from src.operations import OPERATIONS
        for key in OPERATIONS:
            if "coerce" in OPERATIONS[key]:
                coerce = OPERATIONS[key]["coerce"]
                assert callable(coerce), f"OPERATIONS[{key!r}]['coerce'] is not callable"


# ============================================================================
# Task B.13: Test __all__ exports are consistent across modules
# ============================================================================


class TestAllExports:
    """Verify __all__ exports are properly defined and consistent."""

    def test_core_all_exports_calculator(self):
        """src.core.__all__ includes Calculator."""
        from src import core
        assert "Calculator" in core.__all__

    def test_operations_all_exports_operations(self):
        """src.operations.__all__ includes OPERATIONS."""
        from src import operations
        assert "OPERATIONS" in operations.__all__

    def test_operations_all_exports_normal_and_scientific(self):
        """src.operations.__all__ includes NORMAL and SCIENTIFIC."""
        from src import operations
        assert "NORMAL_OPERATIONS" in operations.__all__
        assert "SCIENTIFIC_OPERATIONS" in operations.__all__

    def test_shared_all_exports_dispatcher_and_logger(self):
        """src.shared.__all__ includes OperationDispatcher and Logger."""
        from src import shared
        assert "OperationDispatcher" in shared.__all__
        assert "Logger" in shared.__all__

    def test_session_all_exports_input_handler_and_run_session(self):
        """src.session.__all__ includes InputHandler and run_session."""
        from src import session
        assert "InputHandler" in session.__all__
        assert "run_session" in session.__all__

    def test_interface_all_exports_cli_dispatcher(self):
        """src.interface.__all__ includes CliDispatcher."""
        from src import interface
        assert "CliDispatcher" in interface.__all__
