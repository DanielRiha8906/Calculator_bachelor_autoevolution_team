"""Entry point.

Routes execution to either GUI mode (--gui flag), CLI mode (interaction
layer — cli.py), or interactive mode (interaction layer — input_loop.py)
based on command-line arguments.
"""

import sys
from typing import Optional

from .cli import run_cli
from .input_loop import run_loop


def main(argv: Optional[list[str]] = None) -> None:
    """Entry point: route to GUI, CLI, or interactive mode.

    Resolution order:

    1. If ``--gui`` is present in *effective_argv*, launch the tkinter GUI
       via :class:`~src.gui.CalculatorGUI` and return immediately after the
       window is closed.
    2. If any other arguments are present, run in non-interactive CLI mode
       via :func:`~src.cli.run_cli`.
    3. Otherwise start the interactive REPL via
       :func:`~src.input_loop.run_loop`.

    Args:
        argv: Explicit argument list used for routing.  When ``None`` (the
            default) the value of ``sys.argv[1:]`` is used.  Pass an explicit
            list to override ``sys.argv`` — useful in tests and embedded use.
    """
    effective_argv = sys.argv[1:] if argv is None else argv

    if "--gui" in effective_argv:
        from .gui import CalculatorGUI
        gui = CalculatorGUI()
        gui.run()
        return

    if effective_argv:
        run_cli()
    else:
        run_loop()


if __name__ == "__main__":
    main()
