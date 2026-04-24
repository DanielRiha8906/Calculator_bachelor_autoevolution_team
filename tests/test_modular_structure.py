"""
Test suite for modular refactoring — verify new package structure exists and is importable.

This test suite validates the new modular structure:
- src/core/operations.py contains OperationType and OperationMetadata
- src/ui/interactive.py contains run_interactive_session
- src/ui/cli.py contains run_cli
- src/infrastructure/history.py contains OperationHistory
- src/infrastructure/error_logger.py contains ErrorLogger
- src/session/manager.py contains SessionManager
- src/__init__.py re-exports Calculator, run_interactive_session, run_cli for backward compatibility
"""

import pytest
from enum import Enum


class TestUIInteractiveImport:
    """Test that interactive module is available at new location."""

    def test_import_ui_interactive_new_location(self):
        """Test: from src.ui.interactive import run_interactive_session works."""
        from src.ui.interactive import run_interactive_session
        assert callable(run_interactive_session)

    def test_run_interactive_session_callable(self):
        """Test: run_interactive_session is a callable function."""
        from src.ui.interactive import run_interactive_session
        assert hasattr(run_interactive_session, "__call__")


class TestUICLIImport:
    """Test that CLI module is available at new location."""

    def test_import_ui_cli_new_location(self):
        """Test: from src.ui.cli import run_cli works."""
        from src.ui.cli import run_cli
        assert callable(run_cli)

    def test_run_cli_callable(self):
        """Test: run_cli is a callable function."""
        from src.ui.cli import run_cli
        assert hasattr(run_cli, "__call__")


class TestInfrastructureHistoryImport:
    """Test that history module is available at new location."""

    def test_import_infrastructure_history_new_location(self):
        """Test: from src.infrastructure.history import OperationHistory works."""
        from src.infrastructure.history import OperationHistory
        assert OperationHistory is not None

    def test_operation_history_instantiable(self):
        """Test: OperationHistory class can be instantiated."""
        from src.infrastructure.history import OperationHistory
        history = OperationHistory()
        assert history is not None


class TestInfrastructureErrorLoggerImport:
    """Test that error_logger module is available at new location."""

    def test_import_infrastructure_error_logger_new_location(self):
        """Test: from src.infrastructure.error_logger import ErrorLogger works."""
        from src.infrastructure.error_logger import ErrorLogger
        assert ErrorLogger is not None

    def test_error_logger_instantiable(self):
        """Test: ErrorLogger class can be instantiated."""
        from src.infrastructure.error_logger import ErrorLogger
        error_logger = ErrorLogger()
        assert error_logger is not None


class TestCoreOperationsModule:
    """Test that core/operations module exists with required exports."""

    def test_import_core_operations_module(self):
        """Test: from src.core.operations import OperationType, OperationMetadata works."""
        from src.core.operations import OperationType, OperationMetadata
        assert OperationType is not None
        assert OperationMetadata is not None

    def test_operation_type_is_enum(self):
        """Test: OperationType is an Enum."""
        from src.core.operations import OperationType
        assert issubclass(OperationType, Enum)

    def test_operation_type_unary_member(self):
        """Test: OperationType.UNARY exists."""
        from src.core.operations import OperationType
        assert hasattr(OperationType, "UNARY")
        # Access the member to verify it exists
        _ = OperationType.UNARY

    def test_operation_type_binary_member(self):
        """Test: OperationType.BINARY exists."""
        from src.core.operations import OperationType
        assert hasattr(OperationType, "BINARY")
        # Access the member to verify it exists
        _ = OperationType.BINARY

    def test_operation_metadata_dataclass(self):
        """Test: OperationMetadata can be instantiated with required fields."""
        from src.core.operations import OperationType, OperationMetadata
        metadata = OperationMetadata(
            name="add",
            arity=2,
            op_type=OperationType.BINARY,
            description="Addition"
        )
        assert metadata is not None
        assert metadata.name == "add"
        assert metadata.arity == 2
        assert metadata.op_type == OperationType.BINARY
        assert metadata.description == "Addition"

    def test_operation_metadata_with_unary_type(self):
        """Test: OperationMetadata works with UNARY type."""
        from src.core.operations import OperationType, OperationMetadata
        metadata = OperationMetadata(
            name="factorial",
            arity=1,
            op_type=OperationType.UNARY,
            description="Factorial"
        )
        assert metadata.op_type == OperationType.UNARY
        assert metadata.arity == 1


class TestSessionManagerImport:
    """Test that SessionManager is available at new location."""

    def test_import_session_manager(self):
        """Test: from src.session.manager import SessionManager works."""
        from src.session.manager import SessionManager
        assert SessionManager is not None

    def test_session_manager_instantiable(self):
        """Test: SessionManager can be instantiated with required dependencies."""
        from src.session.manager import SessionManager
        from src.calculator import Calculator
        from src.error_logger import ErrorLogger
        from src.history import OperationHistory

        calculator = Calculator()
        error_logger = ErrorLogger()
        history = OperationHistory()

        manager = SessionManager(calculator, error_logger, history)
        assert manager is not None


class TestSrcInitBackwardCompatibility:
    """Test that src/__init__.py re-exports required symbols for backward compatibility."""

    def test_src_init_reexports_calculator(self):
        """Test: from src import Calculator works."""
        from src import Calculator
        assert Calculator is not None
        # Verify it's the actual Calculator class
        calc = Calculator()
        assert callable(calc.add)

    def test_src_init_reexports_run_interactive_session(self):
        """Test: from src import run_interactive_session works."""
        from src import run_interactive_session
        assert callable(run_interactive_session)

    def test_src_init_reexports_run_cli(self):
        """Test: from src import run_cli works."""
        from src import run_cli
        assert callable(run_cli)

    def test_src_init_reexports_operation_history(self):
        """Test: from src import OperationHistory works."""
        from src import OperationHistory
        history = OperationHistory()
        assert history is not None

    def test_src_init_reexports_error_logger(self):
        """Test: from src import ErrorLogger works."""
        from src import ErrorLogger
        error_logger = ErrorLogger()
        assert error_logger is not None


class TestCoreOperationsPackageStructure:
    """Test that core package is properly structured."""

    def test_core_init_exists_and_imports(self):
        """Test: src/core/__init__.py exists and is importable."""
        import src.core
        assert src.core is not None

    def test_ui_init_exists_and_imports(self):
        """Test: src/ui/__init__.py exists and is importable."""
        import src.ui
        assert src.ui is not None

    def test_infrastructure_init_exists_and_imports(self):
        """Test: src/infrastructure/__init__.py exists and is importable."""
        import src.infrastructure
        assert src.infrastructure is not None

    def test_session_init_exists_and_imports(self):
        """Test: src/session/__init__.py exists and is importable."""
        import src.session
        assert src.session is not None
