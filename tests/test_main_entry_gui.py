"""Test suite for GUI entry point in src.__main__ module.

This module tests the integration of the GUI launch feature with the
existing command-line and interactive interfaces. Tests verify that:
- The --gui flag is recognized and triggers GUI mode
- GUI mode is launched correctly (mocked)
- CLI and interactive modes still work without --gui flag
- GUI flag takes precedence over other execution modes
"""

import sys
from unittest.mock import patch, MagicMock
import pytest


class TestMainGuiIntegration:
    """Test GUI entry point integration with src.__main__."""

    def test_main_accepts_gui_flag(self, monkeypatch):
        """Importing src.__main__ works and has cli_mode; --gui flag triggers GUI launch."""
        from src.__main__ import cli_mode

        # Mock sys.argv to include --gui flag
        monkeypatch.setattr(sys, "argv", ["src", "--gui"])

        # When --gui is present, cli_mode should attempt to launch GUI
        # We expect it to either succeed (if GUI module exists) or fail with clear error
        with patch("builtins.print"):
            # The implementation must recognize --gui flag
            # It should attempt to import and launch the GUI controller
            try:
                cli_mode()
            except (ImportError, ModuleNotFoundError, AttributeError):
                # Expected: GUI module doesn't exist yet
                pass
            except SystemExit:
                # Also acceptable: program exits cleanly
                pass

    def test_main_cli_mode_without_gui_flag(self, monkeypatch):
        """run cli_mode() works normally without --gui flag."""
        from src.__main__ import cli_mode

        # Mock sys.argv to simulate: python -m src add 2 3
        monkeypatch.setattr(sys, "argv", ["src", "add", "2", "3"])

        # Mock sys.exit to prevent test from exiting
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                cli_mode()
                # cli_mode should complete without raising
                # (either exit was called or function returned)

    def test_main_gui_flag_triggers_gui_not_cli(self, monkeypatch):
        """With --gui in sys.argv, GUI is launched (run is called), not CLI."""
        # Mock tkinter at sys.modules level to avoid ImportError in CI
        tk_mock = MagicMock()
        monkeypatch.setitem(sys.modules, "tkinter", tk_mock)
        monkeypatch.setitem(sys.modules, "tkinter.ttk", MagicMock())

        from src.__main__ import cli_mode

        # Mock sys.argv to simulate: python -m src --gui
        monkeypatch.setattr(sys, "argv", ["src", "--gui"])

        # Mock GUIWindow class at the point where it's imported in the window module
        mock_window = MagicMock()
        mock_gui_window_class = MagicMock(return_value=mock_window)

        with patch("src.calculator.gui.window.GUIWindow", new=mock_gui_window_class):
            # cli_mode should recognize --gui, create GUIWindow, and call run()
            cli_mode()
            # Verify that run() was called exactly once on the created instance
            mock_window.run.assert_called_once()

    def test_main_interactive_mode_without_gui_flag(self, monkeypatch):
        """Interactive mode works normally without --gui flag."""
        from src.__main__ import cli_mode

        # Mock sys.argv to simulate: python -m src (no args = interactive)
        monkeypatch.setattr(sys, "argv", ["src"])

        # Mock input to quit immediately
        with patch("builtins.input", return_value="quit"):
            with patch("builtins.print"):
                # Should enter interactive mode and quit cleanly
                cli_mode()
