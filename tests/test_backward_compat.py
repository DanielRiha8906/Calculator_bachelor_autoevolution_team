"""Tests for backward compatibility re-exports from root-level modules."""

import pytest


class TestOperationsImport:
    """Test importing from src.operations (backward compat wrapper)."""

    def test_operation_registry_import(self):
        """Test importing OperationRegistry from src.operations."""
        from src.operations import OperationRegistry
        assert OperationRegistry is not None
        # Should be the actual class from src.core.operations
        assert hasattr(OperationRegistry, "__init__")

    def test_operation_class_import(self):
        """Test importing Operation from src.operations."""
        from src.operations import Operation
        assert Operation is not None
        assert hasattr(Operation, "__dataclass_fields__")


class TestExceptionsImport:
    """Test importing from src.exceptions (backward compat wrapper)."""

    def test_max_retries_exceeded_import(self):
        """Test importing MaxRetriesExceeded from src.exceptions."""
        from src.exceptions import MaxRetriesExceeded
        assert MaxRetriesExceeded is not None
        # Should be an Exception
        assert issubclass(MaxRetriesExceeded, Exception)

    def test_max_retries_exceeded_instantiate(self):
        """Test instantiating MaxRetriesExceeded from src.exceptions."""
        from src.exceptions import MaxRetriesExceeded
        exc = MaxRetriesExceeded("test message")
        assert str(exc) == "test message"

    def test_max_retries_exceeded_raise_and_catch(self):
        """Test raising and catching MaxRetriesExceeded from src.exceptions."""
        from src.exceptions import MaxRetriesExceeded
        with pytest.raises(MaxRetriesExceeded):
            raise MaxRetriesExceeded("test")


class TestHistoryImport:
    """Test importing from src.history (backward compat wrapper)."""

    def test_operation_history_import(self):
        """Test importing OperationHistory from src.history."""
        from src.history import OperationHistory
        assert OperationHistory is not None
        assert hasattr(OperationHistory, "clear_history")
        assert hasattr(OperationHistory, "record_operation")
        assert hasattr(OperationHistory, "display_history")


class TestErrorLoggerImport:
    """Test importing from src.error_logger (backward compat wrapper)."""

    def test_error_logger_import(self):
        """Test importing ErrorLogger from src.error_logger."""
        from src.error_logger import ErrorLogger
        assert ErrorLogger is not None
        assert hasattr(ErrorLogger, "clear_errors")
        assert hasattr(ErrorLogger, "log_error")
        assert hasattr(ErrorLogger, "get_errors")

    def test_error_logger_constants(self):
        """Test that ErrorLogger constants are accessible."""
        from src.error_logger import ErrorLogger
        assert hasattr(ErrorLogger, "INVALID_INPUT")
        assert hasattr(ErrorLogger, "UNSUPPORTED_OPERATION")
        assert hasattr(ErrorLogger, "CALCULATION_ERROR")


class TestREPLImport:
    """Test importing from src.repl (backward compat wrapper)."""

    def test_max_retries_import(self):
        """Test importing MAX_RETRIES from src.repl."""
        from src.repl import MAX_RETRIES
        assert isinstance(MAX_RETRIES, int)
        assert MAX_RETRIES > 0

    def test_operations_dict_import(self):
        """Test importing OPERATIONS dict from src.repl."""
        from src.repl import OPERATIONS
        assert isinstance(OPERATIONS, dict)
        assert len(OPERATIONS) > 0

    def test_operations_dict_structure(self):
        """Test that OPERATIONS dict has correct structure."""
        from src.repl import OPERATIONS
        # Should have operation names as keys
        assert "add" in OPERATIONS
        assert "multiply" in OPERATIONS
        # Each value should be a dict with arity and name
        for key, value in OPERATIONS.items():
            assert isinstance(value, dict)
            assert "arity" in value
            assert "name" in value

    def test_repl_interface_import(self):
        """Test importing REPLInterface from src.repl."""
        from src.repl import REPLInterface
        assert REPLInterface is not None
        assert hasattr(REPLInterface, "run")


class TestCLIImport:
    """Test importing from src.cli (backward compat wrapper)."""

    def test_cli_handler_import(self):
        """Test importing CLIHandler from src.cli."""
        from src.cli import CLIHandler
        assert CLIHandler is not None
        assert hasattr(CLIHandler, "parse_args")
        assert hasattr(CLIHandler, "execute")


class TestInterfacePackageImport:
    """Test importing from src.interface package (new canonical location)."""

    def test_cli_handler_from_interface(self):
        """Test importing CLIHandler from src.interface."""
        from src.interface import CLIHandler
        assert CLIHandler is not None

    def test_repl_interface_from_interface(self):
        """Test importing REPLInterface from src.interface."""
        from src.interface import REPLInterface
        assert REPLInterface is not None


class TestSupportPackageImport:
    """Test importing from src.support package (new canonical location)."""

    def test_operation_history_from_support(self):
        """Test importing OperationHistory from src.support."""
        from src.support import OperationHistory
        assert OperationHistory is not None

    def test_error_logger_from_support(self):
        """Test importing ErrorLogger from src.support."""
        from src.support import ErrorLogger
        assert ErrorLogger is not None

    def test_max_retries_exceeded_from_support(self):
        """Test importing MaxRetriesExceeded from src.support."""
        from src.support import MaxRetriesExceeded
        assert MaxRetriesExceeded is not None


class TestCorePackageImport:
    """Test importing from src.core package (new canonical location)."""

    def test_calculation_engine_import(self):
        """Test importing CalculationEngine from src.core."""
        from src.core import CalculationEngine
        assert CalculationEngine is not None
        assert hasattr(CalculationEngine, "add")
        assert hasattr(CalculationEngine, "subtract")
        assert hasattr(CalculationEngine, "multiply")
        assert hasattr(CalculationEngine, "divide")

    def test_operation_registry_from_core(self):
        """Test importing OperationRegistry from src.core."""
        from src.core import OperationRegistry
        assert OperationRegistry is not None

    def test_operation_from_core(self):
        """Test importing Operation from src.core."""
        from src.core import Operation
        assert Operation is not None

    def test_catalog_from_core(self):
        """Test importing _CATALOG from src.core."""
        from src.core import _CATALOG
        assert isinstance(_CATALOG, list)
        assert len(_CATALOG) > 0


class TestOperationsPackageImport:
    """Test importing from src.operations package (new canonical location)."""

    def test_arithmetic_functions(self):
        """Test importing arithmetic functions."""
        from src.operations.arithmetic import add, subtract, multiply, divide
        assert callable(add)
        assert callable(subtract)
        assert callable(multiply)
        assert callable(divide)

    def test_scientific_functions(self):
        """Test importing scientific functions."""
        from src.operations.scientific import power, logarithm, natural_logarithm
        assert callable(power)
        assert callable(logarithm)
        assert callable(natural_logarithm)

    def test_roots_functions(self):
        """Test importing roots functions."""
        from src.operations.roots import factorial, square, cube, square_root, cube_root
        assert callable(factorial)
        assert callable(square)
        assert callable(cube)
        assert callable(square_root)
        assert callable(cube_root)


class TestImportEquivalence:
    """Test that old and new import paths yield the same objects."""

    def test_operation_history_equivalence(self):
        """Test that OperationHistory imports are equivalent."""
        from src.history import OperationHistory as OldImport
        from src.support.history import OperationHistory as NewImport
        assert OldImport is NewImport

    def test_error_logger_equivalence(self):
        """Test that ErrorLogger imports are equivalent."""
        from src.error_logger import ErrorLogger as OldImport
        from src.support.error_logger import ErrorLogger as NewImport
        assert OldImport is NewImport

    def test_max_retries_exceeded_equivalence(self):
        """Test that MaxRetriesExceeded imports are equivalent."""
        from src.exceptions import MaxRetriesExceeded as OldImport
        from src.support.exceptions import MaxRetriesExceeded as NewImport
        assert OldImport is NewImport

    def test_operation_registry_equivalence(self):
        """Test that OperationRegistry imports are equivalent."""
        from src.operations import OperationRegistry as OldImport
        from src.core.operations import OperationRegistry as NewImport
        assert OldImport is NewImport

    def test_operation_equivalence(self):
        """Test that Operation imports are equivalent."""
        from src.operations import Operation as OldImport
        from src.core.operations import Operation as NewImport
        assert OldImport is NewImport

    def test_cli_handler_equivalence(self):
        """Test that CLIHandler imports are equivalent."""
        from src.cli import CLIHandler as OldImport
        from src.interface.cli import CLIHandler as NewImport
        assert OldImport is NewImport

    def test_repl_interface_equivalence(self):
        """Test that REPLInterface imports are equivalent."""
        from src.repl import REPLInterface as OldImport
        from src.interface.repl import REPLInterface as NewImport
        assert OldImport is NewImport


class TestComplexBackwardCompatScenarios:
    """Test complex scenarios using backward compat imports."""

    def test_mixed_old_and_new_imports(self):
        """Test using mixed old and new imports together."""
        from src.operations import OperationRegistry  # Old import
        from src.core.engine import CalculationEngine  # New import

        engine = CalculationEngine()
        registry = OperationRegistry(engine)

        # Should work seamlessly
        assert registry.arity("add") == 2
        assert registry.dispatch("add", [2, 3]) == 5

    def test_legacy_code_path(self):
        """Test a legacy code path using old imports."""
        from src.error_logger import ErrorLogger  # Old import
        from src.history import OperationHistory  # Old import
        from src.exceptions import MaxRetriesExceeded  # Old import

        # Should all be functional
        error_logger = ErrorLogger()
        history = OperationHistory()
        exc = MaxRetriesExceeded("test")

        assert isinstance(error_logger, ErrorLogger)
        assert isinstance(history, OperationHistory)
        assert isinstance(exc, Exception)

    def test_repl_module_compatibility(self):
        """Test REPL module backward compatibility."""
        from src.repl import MAX_RETRIES, OPERATIONS, REPLInterface
        from src.interface.repl import MAX_RETRIES as new_max_retries
        from src.interface.repl import OPERATIONS as new_operations

        # Should be the same objects
        assert MAX_RETRIES == new_max_retries
        assert OPERATIONS == new_operations
