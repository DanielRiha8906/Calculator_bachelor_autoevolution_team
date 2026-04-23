"""main.py — entry point for the interactive calculator application.

Run without arguments to start an interactive REPL session::

    python -m src.main

Run with an expression argument to evaluate it non-interactively::

    python -m src.main "add 5 3"
"""

import sys

from .calculator import Calculator
from .cli import CLIHandler
from .input_handler import CalculatorREPL


def _is_calculator_expression(arg: str) -> bool:
    """Return True if *arg* looks like a bare calculator expression.

    Guards against accidental CLI-mode activation when ``main()`` is called
    from pytest or other test runners that populate ``sys.argv`` with file
    paths and flags.

    An argument is considered a calculator expression when it:
    - does not start with ``-`` (rules out CLI flags such as ``--verbose``)
    - does not contain ``/`` (rules out UNIX file paths)
    - does not end with ``.py`` (rules out Python module paths)

    Args:
        arg: The first positional command-line argument to inspect.

    Returns:
        ``True`` when the argument is likely a calculator expression,
        ``False`` otherwise.
    """
    return (
        not arg.startswith("-")
        and "/" not in arg
        and not arg.endswith(".py")
    )


def main() -> None:
    """Start the calculator in GUI, REPL, or CLI mode depending on arguments.

    If ``--gui`` or ``-g`` is present in the arguments, launches the
    Tkinter-based :class:`~src.gui.CalculatorGUI`.  ``CalculatorGUI`` is
    imported lazily inside this branch so that the module remains usable
    in environments where ``tkinter`` is not available (e.g. headless CI).

    If a command-line argument is present (beyond the script name) **and**
    that argument looks like a calculator expression (not a file path or a
    flag), delegates to ``CLIHandler`` for non-interactive single-expression
    evaluation.  Otherwise falls through to the interactive
    ``CalculatorREPL``.

    This guard prevents pytest from accidentally activating CLI mode when it
    populates ``sys.argv`` with test-file paths.

    A ``KeyboardInterrupt`` is handled gracefully inside
    ``CalculatorREPL.run``; this function itself will not propagate it.
    """
    if "--gui" in sys.argv or "-g" in sys.argv:
        # Lazy import so that missing tkinter does not break CLI/REPL usage.
        from .gui import CalculatorGUI  # noqa: PLC0415
        calculator = Calculator()
        app = CalculatorGUI(calculator)
        app.mainloop()
        return

    if len(sys.argv) > 1 and _is_calculator_expression(sys.argv[1]):
        handler = CLIHandler(sys.argv[1])
        sys.exit(handler.run())

    calculator = Calculator()
    repl = CalculatorREPL(calculator)
    repl.run()


if __name__ == "__main__":
    main()
