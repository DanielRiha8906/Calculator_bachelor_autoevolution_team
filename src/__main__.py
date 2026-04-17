import sys

from .cli import run_cli
from .input_loop import OPERATIONS, run_loop


def main() -> None:
    """Entry point: start the interactive calculator session or run CLI mode.

    If the first command-line argument is a recognised calculator operation,
    delegates to :func:`~src.cli.run_cli` for non-interactive single-operation
    mode.  Otherwise falls back to the interactive
    :func:`~src.input_loop.run_loop`.

    Checking the first argument against ``OPERATIONS`` (rather than merely
    testing ``len(sys.argv) > 1``) ensures that the module remains safe to
    call in test harnesses where ``sys.argv`` already contains the test
    runner's own arguments.
    """
    if len(sys.argv) > 1 and sys.argv[1] in OPERATIONS:
        run_cli()
    else:
        run_loop()


if __name__ == "__main__":
    main()
