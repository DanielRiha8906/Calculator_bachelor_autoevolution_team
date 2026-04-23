"""Tests for gui_main.py entry point.

These tests verify that the main() function properly initializes the GUI
without requiring a display server.
"""

from unittest import mock

import pytest

# Skip all tests in this module if tkinter is unavailable
pytest.importorskip("tkinter")

# Import after checking for tkinter
from src import gui_main


class TestGUIMainEntryPoint:
    """Test suite for gui_main.main() function."""

    def test_gui_main_initializes_without_error(self):
        """Patch tk.Tk and CalculatorGUI to avoid real window; verify main() runs."""
        with mock.patch("src.gui_main.tk.Tk") as mock_tk, \
             mock.patch("src.gui_main.SessionHistory") as mock_history, \
             mock.patch("src.gui_main.CalculatorGUI") as mock_gui:

            mock_root = mock.MagicMock()
            mock_tk.return_value = mock_root
            mock_history_instance = mock.MagicMock()
            mock_history.return_value = mock_history_instance

            # Call main - should not raise an exception
            gui_main.main()

            # Verify tk.Tk was called
            mock_tk.assert_called_once()

    def test_gui_main_creates_session_history(self):
        """Verify that SessionHistory is instantiated in main()."""
        with mock.patch("src.gui_main.tk.Tk") as mock_tk, \
             mock.patch("src.gui_main.SessionHistory") as mock_history, \
             mock.patch("src.gui_main.CalculatorGUI") as mock_gui:

            mock_root = mock.MagicMock()
            mock_tk.return_value = mock_root
            mock_history_instance = mock.MagicMock()
            mock_history.return_value = mock_history_instance

            gui_main.main()

            # Verify SessionHistory was instantiated
            mock_history.assert_called_once()

    def test_gui_main_creates_calculator_gui(self):
        """Verify that CalculatorGUI is created with root and history."""
        with mock.patch("src.gui_main.tk.Tk") as mock_tk, \
             mock.patch("src.gui_main.SessionHistory") as mock_history, \
             mock.patch("src.gui_main.CalculatorGUI") as mock_gui:

            mock_root = mock.MagicMock()
            mock_tk.return_value = mock_root
            mock_history_instance = mock.MagicMock()
            mock_history.return_value = mock_history_instance

            gui_main.main()

            # Verify CalculatorGUI was called with root and history
            mock_gui.assert_called_once_with(mock_root, mock_history_instance)

    def test_gui_main_calls_run(self):
        """Verify that CalculatorGUI.run() is called by main()."""
        with mock.patch("src.gui_main.tk.Tk") as mock_tk, \
             mock.patch("src.gui_main.SessionHistory") as mock_history, \
             mock.patch("src.gui_main.CalculatorGUI") as mock_gui:

            mock_root = mock.MagicMock()
            mock_tk.return_value = mock_root
            mock_history_instance = mock.MagicMock()
            mock_history.return_value = mock_history_instance
            mock_gui_instance = mock.MagicMock()
            mock_gui.return_value = mock_gui_instance

            gui_main.main()

            # Verify run() was called on the GUI instance
            mock_gui_instance.run.assert_called_once()

    def test_gui_main_initialization_order(self):
        """Verify correct initialization order: Tk, History, GUI, run."""
        call_order = []

        def mock_tk_init():
            call_order.append("tk")
            return mock.MagicMock()

        def mock_history_init():
            call_order.append("history")
            return mock.MagicMock()

        def mock_gui_init(root, history):
            call_order.append("gui")
            instance = mock.MagicMock()
            instance.run = lambda: call_order.append("run")
            return instance

        with mock.patch("src.gui_main.tk.Tk", side_effect=mock_tk_init), \
             mock.patch("src.gui_main.SessionHistory", side_effect=mock_history_init), \
             mock.patch("src.gui_main.CalculatorGUI", side_effect=mock_gui_init):

            gui_main.main()

            # Verify order
            assert call_order == ["tk", "history", "gui", "run"]


class TestGUIMainImports:
    """Test suite for gui_main module imports."""

    def test_gui_main_imports_required_modules(self):
        """Verify that gui_main can import all required modules."""
        # This test simply imports gui_main; if imports fail, pytest will catch it
        assert hasattr(gui_main, "main")

    def test_main_is_callable(self):
        """Verify that main is a callable function."""
        assert callable(gui_main.main)
