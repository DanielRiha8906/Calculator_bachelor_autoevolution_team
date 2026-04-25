"""Entry point for ``python -m src``.

Delegates to the modular calculator implementation in src.calculator.main.

The shim exposes its own ``cli_mode()`` that calls the underlying
``cli_mode(MODE_SCIENTIFIC)`` so that all 13 operations remain available
when the calculator is invoked via ``python -m src``.  This preserves
backward compatibility for callers that import ``cli_mode`` from this
module (e.g. existing tests in ``tests/test_cli_mode.py``).

When ``--gui`` is present in ``sys.argv`` the entry point launches the
tkinter-based GUI instead of the CLI/interactive loop.
"""

import sys

from src.calculator.main import cli_mode as _cli_mode_base, MODE_SCIENTIFIC


def cli_mode() -> None:
    """Full-featured CLI mode with all operations available.

    When ``--gui`` is present in ``sys.argv`` the GUI is launched instead
    of the normal CLI/interactive loop.

    Wraps :func:`src.calculator.main.cli_mode` using
    :data:`~src.calculator.main.MODE_SCIENTIFIC` so that scientific
    operations (factorial, square, square_root, power, …) are accessible
    when users invoke the calculator through this entry point.
    """
    if "--gui" in sys.argv:
        sys.argv.remove("--gui")
        from src.calculator.gui.controller import GUIController
        from src.calculator.gui.window import GUIWindow

        controller = GUIController(mode="scientific")
        window = GUIWindow(controller)
        window.run()
        return

    _cli_mode_base(MODE_SCIENTIFIC)


if __name__ == "__main__":
    cli_mode()
