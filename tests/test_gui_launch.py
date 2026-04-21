"""Smoke tests for GUI module imports and main launcher.

These tests verify that the GUI modules can be imported without errors
and that the main launcher exists and is callable.
"""

import pytest
import sys
from unittest.mock import MagicMock

# Pre-mock tkinter for headless environments
try:
    import tkinter
except ImportError:
    # Create mocks for tkinter modules
    class MockStringVar:
        def __init__(self, value=""):
            self._value = value

        def get(self):
            return self._value

        def set(self, value):
            self._value = value

    tk_mock = MagicMock()
    tk_mock.StringVar = MockStringVar
    tk_mock.Tk = MagicMock
    tkfont_mock = MagicMock()
    sys.modules['tkinter'] = tk_mock
    sys.modules['tkinter.font'] = tkfont_mock


class TestGUIModuleImports:
    """Tests for importing GUI modules."""

    def test_gui_modules_importable(self):
        """Test that src.gui module is importable."""
        try:
            import src.gui
            assert src.gui is not None
        except ImportError as e:
            pytest.fail(f"Failed to import src.gui: {e}")

    def test_gui_modes_importable(self):
        """Test that src.gui.modes module is importable."""
        try:
            import src.gui.modes
            assert src.gui.modes is not None
        except ImportError as e:
            pytest.fail(f"Failed to import src.gui.modes: {e}")

    def test_gui_application_importable(self):
        """Test that src.gui.application module is importable."""
        try:
            import src.gui.application
            assert src.gui.application is not None
        except ImportError as e:
            pytest.fail(f"Failed to import src.gui.application: {e}")

    def test_calc_mode_importable(self):
        """Test that CalcMode class is importable."""
        try:
            from src.gui.modes import CalcMode
            assert CalcMode is not None
        except ImportError as e:
            pytest.fail(f"Failed to import CalcMode: {e}")

    def test_simple_mode_importable(self):
        """Test that SimpleMode class is importable."""
        try:
            from src.gui.modes import SimpleMode
            assert SimpleMode is not None
        except ImportError as e:
            pytest.fail(f"Failed to import SimpleMode: {e}")

    def test_scientific_mode_importable(self):
        """Test that ScientificMode class is importable."""
        try:
            from src.gui.modes import ScientificMode
            assert ScientificMode is not None
        except ImportError as e:
            pytest.fail(f"Failed to import ScientificMode: {e}")

    def test_calculator_gui_importable(self):
        """Test that CalculatorGUI class is importable."""
        try:
            from src.gui.application import CalculatorGUI
            assert CalculatorGUI is not None
        except ImportError as e:
            pytest.fail(f"Failed to import CalculatorGUI: {e}")


class TestGUIMainModuleImports:
    """Tests for importing the main launcher module."""

    def test_gui_main_importable(self):
        """Test that src.gui_main module is importable."""
        try:
            import src.gui_main
            assert src.gui_main is not None
        except ImportError as e:
            pytest.fail(f"Failed to import src.gui_main: {e}")

    def test_main_function_exists(self):
        """Test that main() function exists in src.gui_main."""
        from src.gui_main import main
        assert main is not None

    def test_main_function_callable(self):
        """Test that main() is callable."""
        from src.gui_main import main
        assert callable(main)

    def test_main_function_has_correct_signature(self):
        """Test that main() accepts no required arguments."""
        from src.gui_main import main
        import inspect

        sig = inspect.signature(main)
        # main() should have no required parameters
        assert len(sig.parameters) == 0


class TestDependencyImports:
    """Tests for verifying dependencies are available."""

    def test_calculator_importable(self):
        """Test that Calculator class is importable."""
        try:
            from src.core.calculator import Calculator
            assert Calculator is not None
        except ImportError as e:
            pytest.fail(f"Failed to import Calculator: {e}")

    def test_history_tracker_importable(self):
        """Test that HistoryTracker class is importable."""
        try:
            from src.support.history import HistoryTracker
            assert HistoryTracker is not None
        except ImportError as e:
            pytest.fail(f"Failed to import HistoryTracker: {e}")

    def test_operations_registry_importable(self):
        """Test that OperationRegistry class is importable."""
        try:
            from src.core.operations_manager import OperationRegistry
            assert OperationRegistry is not None
        except ImportError as e:
            pytest.fail(f"Failed to import OperationRegistry: {e}")

    def test_tkinter_available(self):
        """Test that tkinter is available or can be mocked."""
        try:
            import tkinter as tk
            assert tk is not None
        except ImportError:
            # In headless environments, tkinter may not be available
            # but the GUI module should handle this gracefully via mocking
            pass


class TestModuleIntegration:
    """Integration tests for module imports."""

    def test_all_imports_together(self):
        """Test that all GUI components can be imported together."""
        try:
            from src.gui.modes import SimpleMode, ScientificMode
            from src.gui.application import CalculatorGUI
            from src.core.calculator import Calculator
            from src.support.history import HistoryTracker

            assert SimpleMode is not None
            assert ScientificMode is not None
            assert CalculatorGUI is not None
            assert Calculator is not None
            assert HistoryTracker is not None
        except ImportError as e:
            pytest.fail(f"Failed to import all components together: {e}")

    def test_gui_main_imports_all_dependencies(self):
        """Test that gui_main imports all its dependencies."""
        try:
            import src.gui_main
            import inspect

            source = inspect.getsource(src.gui_main)
            # Check that main imports are present
            assert "tkinter" in source or "tk" in source
            assert "Calculator" in source
            assert "HistoryTracker" in source
            assert "SimpleMode" in source
            assert "CalculatorGUI" in source
        except (ImportError, OSError) as e:
            pytest.fail(f"Failed to verify gui_main imports: {e}")
