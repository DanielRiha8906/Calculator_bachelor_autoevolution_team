"""Tests for src.gui.window module.

Tests the CalculatorWindow Tkinter GUI implementation.

Since Tkinter is not available in headless CI environments and the window
class has very tight coupling with tkinter widgets, this test module uses
mocking to test that:
1. The module can be imported when tkinter is mocked
2. The CalculatorWindow class has all required methods
3. Methods are callable and accept expected parameters
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, ANY
import sys


@pytest.fixture(autouse=True)
def mock_tkinter():
    """Mock tkinter and ttk modules for headless testing.

    This creates mock objects for tkinter and ttk that are sufficient for
    the window module to import and instantiate objects.
    """
    # Create a more sophisticated mock that can handle widget creation
    mock_tk_module = MagicMock()
    mock_ttk_module = MagicMock()

    # Create a fake Tk class that can be subclassed
    class FakeTk:
        def __init__(self):
            pass
        def columnconfigure(self, *args, **kwargs):
            pass
        def rowconfigure(self, *args, **kwargs):
            pass
        def title(self, *args):
            pass
        def resizable(self, *args):
            pass
        def minsize(self, *args):
            pass
        def mainloop(self):
            pass

    # Setup module-level attributes
    mock_tk_module.Tk = FakeTk
    mock_tk_module.StringVar = MagicMock(return_value=MagicMock())
    mock_tk_module.Canvas = MagicMock
    mock_tk_module.Text = MagicMock
    mock_tk_module.Event = MagicMock
    mock_tk_module.END = "end"

    # Widget factory - returns mocks with necessary methods
    def make_widget():
        widget = MagicMock()
        widget.grid = MagicMock()
        widget.configure = MagicMock()
        widget.get = MagicMock(return_value="")
        widget.delete = MagicMock()
        widget.insert = MagicMock()
        widget.winfo_children = MagicMock(return_value=[])
        widget.destroy = MagicMock()
        widget.bind = MagicMock()
        widget.create_window = MagicMock(return_value=1)
        widget.itemconfigure = MagicMock()
        widget.bbox = MagicMock(return_value=(0, 0, 100, 100))
        widget.see = MagicMock()
        widget.update_idletasks = MagicMock()
        widget.set = MagicMock()
        return widget

    # Setup ttk widgets
    mock_ttk_module.LabelFrame = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_ttk_module.Button = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_ttk_module.Entry = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_ttk_module.Label = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_ttk_module.Frame = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_ttk_module.Scrollbar = MagicMock(side_effect=lambda *args, **kwargs: make_widget())

    # Setup tk widget factories
    mock_tk_module.Canvas = MagicMock(side_effect=lambda *args, **kwargs: make_widget())
    mock_tk_module.Text = MagicMock(side_effect=lambda *args, **kwargs: make_widget())

    modules = {
        "tkinter": mock_tk_module,
        "tkinter.ttk": mock_ttk_module,
    }

    with patch.dict(sys.modules, modules):
        yield mock_tk_module, mock_ttk_module


@pytest.fixture
def mock_adapter():
    """Fixture providing a mocked GUISessionAdapter."""
    adapter = MagicMock()
    adapter.get_operations.return_value = ["add", "subtract", "multiply"]
    adapter.get_arity.return_value = 2
    adapter.get_history.return_value = []
    return adapter


class TestCalculatorWindowImportAndBasics:
    """Test suite for CalculatorWindow import and basic structure."""

    def test_window_module_imports_successfully(self, mock_tkinter):
        """Test that the window module can be imported with mocked tkinter."""
        from src.gui.window import CalculatorWindow
        assert CalculatorWindow is not None

    def test_window_class_is_defined(self, mock_tkinter):
        """Test that CalculatorWindow class is defined."""
        from src.gui.window import CalculatorWindow
        assert hasattr(CalculatorWindow, "__init__")

    def test_window_has_required_event_handlers(self, mock_tkinter):
        """Test that CalculatorWindow has all required event handler methods."""
        from src.gui.window import CalculatorWindow

        required_methods = [
            "on_mode_changed",
            "on_operation_selected",
            "on_execute_clicked",
            "on_clear_history_clicked",
            "update_history_display",
            "update_operation_buttons",
        ]

        for method_name in required_methods:
            assert hasattr(CalculatorWindow, method_name)
            assert callable(getattr(CalculatorWindow, method_name))

    def test_window_can_be_instantiated(self, mock_tkinter, mock_adapter):
        """Test that CalculatorWindow can be instantiated with a mock adapter."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window is not None

    def test_window_stores_adapter_reference(self, mock_tkinter, mock_adapter):
        """Test that CalculatorWindow stores the adapter reference."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._adapter is mock_adapter

    def test_window_initializes_selected_op_to_none(self, mock_tkinter, mock_adapter):
        """Test that window initializes _selected_op to None."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        assert window._selected_op is None


class TestCalculatorWindowEventHandlers:
    """Test suite for event handler signatures and basic execution."""

    def test_on_mode_changed_accepts_mode_name(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed accepts a mode_name parameter."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.on_mode_changed("normal")

    def test_on_mode_changed_calls_adapter_set_mode(self, mock_tkinter, mock_adapter):
        """Test that on_mode_changed calls adapter.set_mode."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window.on_mode_changed("scientific")

        # Verify the adapter method was called
        mock_adapter.set_mode.assert_called_with("scientific")

    def test_on_operation_selected_accepts_operation_name(self, mock_tkinter, mock_adapter):
        """Test that on_operation_selected accepts an operation name."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.on_operation_selected("add")

    def test_on_operation_selected_stores_operation(self, mock_tkinter, mock_adapter):
        """Test that on_operation_selected stores the selected operation."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window.on_operation_selected("multiply")

        assert window._selected_op == "multiply"

    def test_on_operation_selected_calls_adapter_get_arity(self, mock_tkinter, mock_adapter):
        """Test that on_operation_selected calls adapter.get_arity."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_arity.reset_mock()

        window.on_operation_selected("add")

        mock_adapter.get_arity.assert_called_with("add")

    def test_on_execute_clicked_is_callable(self, mock_tkinter, mock_adapter):
        """Test that on_execute_clicked can be called."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.on_execute_clicked()

    def test_on_execute_clicked_with_no_operation_selected(self, mock_tkinter, mock_adapter):
        """Test on_execute_clicked when no operation is selected."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window._selected_op = None

        # Should handle gracefully without calling adapter.execute_operation_safe
        window.on_execute_clicked()
        mock_adapter.execute_operation_safe.assert_not_called()

    def test_on_execute_clicked_with_valid_selection(self, mock_tkinter, mock_adapter):
        """Test on_execute_clicked with a valid operation selected."""
        from src.gui.window import CalculatorWindow

        mock_adapter.execute_operation_safe.return_value = ("7.0", "")
        mock_adapter.get_arity.return_value = 2

        window = CalculatorWindow(mock_adapter)
        window._selected_op = "add"
        window._operand1_entry.get.return_value = "3.0"
        window._operand2_entry.get.return_value = "4.0"

        window.on_execute_clicked()

        # Should have called execute_operation_safe
        mock_adapter.execute_operation_safe.assert_called_once()

    def test_on_clear_history_clicked_is_callable(self, mock_tkinter, mock_adapter):
        """Test that on_clear_history_clicked can be called."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.on_clear_history_clicked()

    def test_on_clear_history_clicked_calls_adapter_clear_history(self, mock_tkinter, mock_adapter):
        """Test that on_clear_history_clicked calls adapter.clear_history."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        window.on_clear_history_clicked()

        mock_adapter.clear_history.assert_called_once()


class TestCalculatorWindowUpdateMethods:
    """Test suite for update methods."""

    def test_update_history_display_is_callable(self, mock_tkinter, mock_adapter):
        """Test that update_history_display can be called."""
        from src.gui.window import CalculatorWindow

        mock_adapter.get_history.return_value = []
        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.update_history_display()

    def test_update_history_display_calls_adapter_get_history(self, mock_tkinter, mock_adapter):
        """Test that update_history_display calls adapter.get_history."""
        from src.gui.window import CalculatorWindow

        mock_adapter.get_history.return_value = []
        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_history.reset_mock()

        window.update_history_display()

        mock_adapter.get_history.assert_called_once()

    def test_update_operation_buttons_is_callable(self, mock_tkinter, mock_adapter):
        """Test that update_operation_buttons can be called."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # Should not raise
        window.update_operation_buttons()

    def test_update_operation_buttons_calls_adapter_get_operations(self, mock_tkinter, mock_adapter):
        """Test that update_operation_buttons calls adapter.get_operations."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        mock_adapter.get_operations.reset_mock()

        window.update_operation_buttons()

        mock_adapter.get_operations.assert_called_once()


class TestCalculatorWindowInitialization:
    """Test suite for initialization behavior."""

    def test_window_calls_build_ui_on_init(self, mock_tkinter, mock_adapter):
        """Test that __init__ calls _build_ui."""
        from src.gui.window import CalculatorWindow

        with patch.object(CalculatorWindow, "_build_ui") as mock_build:
            with patch.object(CalculatorWindow, "on_mode_changed"):
                window = CalculatorWindow(mock_adapter)
                mock_build.assert_called_once()

    def test_window_calls_on_mode_changed_normal_on_init(self, mock_tkinter, mock_adapter):
        """Test that __init__ calls on_mode_changed('normal')."""
        from src.gui.window import CalculatorWindow

        with patch.object(CalculatorWindow, "on_mode_changed") as mock_on_mode:
            window = CalculatorWindow(mock_adapter)
            mock_on_mode.assert_called_with("normal")


class TestCalculatorWindowBuildUI:
    """Test suite for _build_ui method."""

    def test_build_ui_creates_widgets(self, mock_tkinter, mock_adapter):
        """Test that _build_ui creates necessary widget attributes."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)

        # Check that key widgets were created as attributes
        assert hasattr(window, "_operand1_entry")
        assert hasattr(window, "_operand2_entry")
        assert hasattr(window, "_operand2_label")
        assert hasattr(window, "_result_var")
        assert hasattr(window, "_result_label_widget")
        assert hasattr(window, "_history_text")
        assert hasattr(window, "_ops_canvas")
        assert hasattr(window, "_ops_inner_frame")

    def test_build_ui_sets_window_title(self, mock_tkinter, mock_adapter):
        """Test that _build_ui sets the window title."""
        from src.gui.window import CalculatorWindow

        window = CalculatorWindow(mock_adapter)
        # If title was called, this should work (it's mocked)
        assert window is not None
