"""Interface package for the Calculator application.

Exports CLIHandler and REPLInterface from their respective submodules.
GUICalculator is also exported when tkinter is available; the import is
guarded so that headless environments (e.g. CI) can still use the
CLI and REPL modes without error.
"""

from .cli import CLIHandler
from .repl import REPLInterface

__all__ = ["CLIHandler", "REPLInterface", "GUICalculator"]

# GUICalculator requires tkinter, which may not be present in headless
# environments.  Export it only when the import succeeds.
try:
    from .gui import GUICalculator
except ImportError:
    pass
