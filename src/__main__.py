import sys
from typing import Optional

from .cli import run_cli
from .input_loop import run_loop


def main(argv: Optional[list[str]] = None) -> None:
    """Entry point: route to CLI mode or interactive mode.

    If command-line arguments are present (beyond the module name), the
    calculator runs in non-interactive CLI mode via :func:`~src.cli.run_cli`.
    Otherwise the interactive REPL is started via
    :func:`~src.input_loop.run_loop`.

    Args:
        argv: Explicit argument list used for routing.  When ``None`` (the
            default) the value of ``sys.argv[1:]`` is used.  Pass an explicit
            list to override ``sys.argv`` — useful in tests and embedded use.
    """
    effective_argv = sys.argv[1:] if argv is None else argv
    if effective_argv:
        run_cli()
    else:
        run_loop()


if __name__ == "__main__":
    main()
