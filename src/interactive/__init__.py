"""Interactive CLI session handling for the Calculator application.

This package manages the interactive command-line session: displaying menus,
reading and validating user input, executing operations, and persisting session
history.  It depends on the core layer for the operation registry and has no
knowledge of non-interactive CLI argument parsing.
"""

from .session import run_interactive_session

__all__ = ["run_interactive_session"]
