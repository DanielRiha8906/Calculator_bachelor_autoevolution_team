"""GUI package for the Calculator application (Issue #414).

Exports GUIController (pure Python business-logic layer) and GUIWindow
(tkinter-based user interface).

GUIWindow is imported lazily at runtime to avoid a hard tkinter dependency
at package-import time.  Environments without tkinter (e.g. headless CI)
can still import GUIController without error.
"""

from src.calculator.gui.controller import GUIController

__all__ = ["GUIController", "GUIWindow"]


def __getattr__(name: str):  # type: ignore[override]
    if name == "GUIWindow":
        from src.calculator.gui.window import GUIWindow  # noqa: PLC0415
        return GUIWindow
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
