"""Entry point for ``python -m src``.

Delegates to the modular calculator implementation in src.calculator.main.

The shim exposes its own ``cli_mode()`` that calls the underlying
``cli_mode(MODE_SCIENTIFIC)`` so that all 13 operations remain available
when the calculator is invoked via ``python -m src``.  This preserves
backward compatibility for callers that import ``cli_mode`` from this
module (e.g. existing tests in ``tests/test_cli_mode.py``).
"""

from src.calculator.main import cli_mode as _cli_mode_base, MODE_SCIENTIFIC


def cli_mode() -> None:
    """Full-featured CLI mode with all operations available.

    Wraps :func:`src.calculator.main.cli_mode` using
    :data:`~src.calculator.main.MODE_SCIENTIFIC` so that scientific
    operations (factorial, square, square_root, power, …) are accessible
    when users invoke the calculator through this entry point.
    """
    _cli_mode_base(MODE_SCIENTIFIC)


if __name__ == "__main__":
    cli_mode()
