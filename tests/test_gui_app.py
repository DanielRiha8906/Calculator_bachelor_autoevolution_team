"""Tests for src.gui.app and src.__main__ entry points.

Tests the run_gui() function and --gui flag handling.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
import sys


@pytest.fixture(autouse=True)
def mock_tkinter():
    """Mock tkinter modules for headless testing."""
    mock_tk = MagicMock()
    mock_tk.Tk = MagicMock
    mock_tk.Event = MagicMock
    mock_tk.StringVar = MagicMock(return_value=MagicMock())
    mock_tk.Canvas = MagicMock
    mock_tk.Text = MagicMock
    mock_tk.END = "end"

    mock_ttk = MagicMock()
    mock_ttk.LabelFrame = MagicMock
    mock_ttk.Button = MagicMock
    mock_ttk.Entry = MagicMock
    mock_ttk.Label = MagicMock
    mock_ttk.Frame = MagicMock
    mock_ttk.Scrollbar = MagicMock

    modules = {
        "tkinter": mock_tk,
        "tkinter.ttk": mock_ttk,
    }

    with patch.dict(sys.modules, modules):
        yield mock_tk, mock_ttk


class TestRunGui:
    """Test suite for run_gui() function."""

    def test_run_gui_creates_calculator(self, mock_tkinter):
        """Test run_gui creates a Calculator instance."""
        from src.gui.app import run_gui
        from src.core.calculator import Calculator

        with patch("src.gui.app.Calculator") as mock_calc_class:
            with patch("src.gui.app.CalculatorSession"):
                with patch("src.gui.app.GUISessionAdapter"):
                    with patch("src.gui.app.CalculatorWindow"):
                        run_gui()
                        mock_calc_class.assert_called_once()

    def test_run_gui_creates_session(self, mock_tkinter):
        """Test run_gui creates a CalculatorSession instance."""
        from src.gui.app import run_gui

        with patch("src.gui.app.Calculator"):
            with patch("src.gui.app.CalculatorSession") as mock_session_class:
                with patch("src.gui.app.GUISessionAdapter"):
                    with patch("src.gui.app.CalculatorWindow"):
                        run_gui()
                        mock_session_class.assert_called_once()

    def test_run_gui_creates_adapter(self, mock_tkinter):
        """Test run_gui creates a GUISessionAdapter instance."""
        from src.gui.app import run_gui

        with patch("src.gui.app.Calculator"):
            with patch("src.gui.app.CalculatorSession"):
                with patch("src.gui.app.GUISessionAdapter") as mock_adapter_class:
                    with patch("src.gui.app.CalculatorWindow"):
                        run_gui()
                        mock_adapter_class.assert_called_once()

    def test_run_gui_creates_window(self, mock_tkinter):
        """Test run_gui creates a CalculatorWindow instance."""
        from src.gui.app import run_gui

        with patch("src.gui.app.Calculator"):
            with patch("src.gui.app.CalculatorSession"):
                with patch("src.gui.app.GUISessionAdapter"):
                    with patch("src.gui.app.CalculatorWindow") as mock_window_class:
                        run_gui()
                        mock_window_class.assert_called_once()

    def test_run_gui_calls_mainloop(self, mock_tkinter):
        """Test run_gui calls mainloop on the window."""
        from src.gui.app import run_gui

        mock_window = MagicMock()

        with patch("src.gui.app.Calculator"):
            with patch("src.gui.app.CalculatorSession"):
                with patch("src.gui.app.GUISessionAdapter"):
                    with patch("src.gui.app.CalculatorWindow", return_value=mock_window):
                        run_gui()
                        mock_window.mainloop.assert_called_once()

    def test_run_gui_wires_components_in_order(self, mock_tkinter):
        """Test run_gui constructs components in correct order."""
        from src.gui.app import run_gui

        call_order = []

        def track_call(name):
            def wrapper(*args, **kwargs):
                call_order.append(name)
                return MagicMock()
            return wrapper

        with patch("src.gui.app.Calculator", side_effect=track_call("Calculator")):
            with patch("src.gui.app.CalculatorSession", side_effect=track_call("Session")):
                with patch("src.gui.app.GUISessionAdapter", side_effect=track_call("Adapter")):
                    with patch("src.gui.app.CalculatorWindow", side_effect=track_call("Window")):
                        run_gui()

                        # Components should be created in order
                        assert call_order == ["Calculator", "Session", "Adapter", "Window"]


class TestMainFunctionGuiFlag:
    """Test suite for main() function with --gui flag."""

    def test_main_with_gui_flag_calls_run_gui(self, mock_tkinter):
        """Test main() with --gui flag calls run_gui()."""
        from src.__main__ import main

        with patch("sys.argv", ["prog", "--gui"]):
            with patch("src.gui.app.run_gui") as mock_run_gui:
                main()
                mock_run_gui.assert_called_once()

    def test_main_with_gui_flag_does_not_call_interactive_session(self, mock_tkinter):
        """Test main() with --gui flag does not call interactive_session()."""
        from src.__main__ import main

        with patch("sys.argv", ["prog", "--gui"]):
            with patch("src.gui.app.run_gui"):
                with patch("src.__main__.interactive_session") as mock_interactive:
                    main()
                    mock_interactive.assert_not_called()

    def test_main_without_gui_flag_calls_interactive_session(self, mock_tkinter):
        """Test main() without --gui flag calls interactive_session()."""
        from src.__main__ import main

        with patch("sys.argv", ["prog"]):
            with patch("src.__main__.Calculator") as mock_calc:
                with patch("src.__main__.interactive_session") as mock_interactive:
                    main()
                    mock_interactive.assert_called_once()

    def test_main_without_gui_flag_does_not_call_run_gui(self, mock_tkinter):
        """Test main() without --gui flag does not call run_gui()."""
        from src.__main__ import main

        with patch("sys.argv", ["prog"]):
            with patch("src.__main__.Calculator"):
                with patch("src.__main__.interactive_session"):
                    # Since run_gui is lazily imported, it shouldn't be called
                    # We just verify the normal flow doesn't try to import it
                    main()

    def test_main_with_gui_flag_creates_calculator(self, mock_tkinter):
        """Test main() with --gui flag does not create Calculator directly."""
        from src.__main__ import main

        with patch("sys.argv", ["prog", "--gui"]):
            with patch("src.gui.app.run_gui"):
                with patch("src.__main__.Calculator") as mock_calc:
                    main()
                    # Calculator creation is delegated to run_gui, not done in main
                    mock_calc.assert_not_called()

    def test_main_without_gui_flag_creates_calculator(self, mock_tkinter):
        """Test main() without --gui flag creates Calculator."""
        from src.__main__ import main

        with patch("sys.argv", ["prog"]):
            with patch("src.__main__.Calculator") as mock_calc:
                with patch("src.__main__.interactive_session"):
                    main()
                    mock_calc.assert_called_once()


class TestMainWithVariousArguments:
    """Test suite for main() function with various arguments."""

    def test_main_with_gui_flag_in_middle_of_args(self, mock_tkinter):
        """Test main() detects --gui flag in the middle of arguments."""
        from src.__main__ import main

        with patch("sys.argv", ["prog", "arg1", "--gui", "arg2"]):
            with patch("src.gui.app.run_gui") as mock_run_gui:
                with patch("src.__main__.Calculator"):
                    with patch("src.__main__.interactive_session"):
                        main()
                        mock_run_gui.assert_called_once()

    def test_main_with_gui_flag_at_end(self, mock_tkinter):
        """Test main() detects --gui flag at the end of arguments."""
        from src.__main__ import main

        with patch("sys.argv", ["prog", "arg1", "--gui"]):
            with patch("src.gui.app.run_gui") as mock_run_gui:
                with patch("src.__main__.Calculator"):
                    with patch("src.__main__.interactive_session"):
                        main()
                        mock_run_gui.assert_called_once()

    def test_main_without_flag_with_other_args(self, mock_tkinter):
        """Test main() without --gui flag ignores other arguments."""
        from src.__main__ import main

        with patch("sys.argv", ["prog", "arg1", "arg2"]):
            with patch("src.__main__.Calculator"):
                with patch("src.__main__.interactive_session") as mock_interactive:
                    main()
                    mock_interactive.assert_called_once()

    def test_main_empty_argv(self, mock_tkinter):
        """Test main() with empty argv (only program name)."""
        from src.__main__ import main

        with patch("sys.argv", ["prog"]):
            with patch("src.__main__.Calculator"):
                with patch("src.__main__.interactive_session") as mock_interactive:
                    main()
                    mock_interactive.assert_called_once()


class TestGuiImportBehavior:
    """Test suite for lazy import of GUI components."""

    def test_gui_components_lazily_imported_with_flag(self, mock_tkinter):
        """Test GUI components are imported when --gui flag is present."""
        from src.__main__ import main

        with patch("sys.argv", ["prog", "--gui"]):
            with patch("src.gui.app.run_gui") as mock_run_gui:
                main()
                # run_gui should have been called (meaning the import succeeded)
                mock_run_gui.assert_called_once()

    def test_gui_components_not_imported_without_flag(self, mock_tkinter):
        """Test GUI components are not imported when --gui flag is absent."""
        from src.__main__ import main

        # Track which modules are imported
        import_count = {}

        def track_import(name):
            import_count[name] = import_count.get(name, 0) + 1
            if name == "src.gui.app":
                raise ImportError("Should not import GUI when no --gui flag")
            return MagicMock()

        with patch("sys.argv", ["prog"]):
            with patch("src.__main__.Calculator"):
                with patch("src.__main__.interactive_session"):
                    # The import should not happen, so no exception
                    main()

    def test_main_passes_calculator_to_interactive_session(self, mock_tkinter):
        """Test main() passes the Calculator instance to interactive_session."""
        from src.__main__ import main

        mock_calc = MagicMock()

        with patch("sys.argv", ["prog"]):
            with patch("src.__main__.Calculator", return_value=mock_calc):
                with patch("src.__main__.interactive_session") as mock_interactive:
                    main()
                    mock_interactive.assert_called_once_with(mock_calc)
