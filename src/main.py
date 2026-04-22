"""main.py — entry point for the interactive calculator application.

Run this module directly to start a REPL session::

    python -m src.main
"""

from .calculator import Calculator
from .input_handler import CalculatorREPL


def main() -> None:
    """Start the interactive calculator REPL.

    Creates a ``Calculator`` instance, wraps it in a ``CalculatorREPL``,
    and starts the read-eval-print loop.  A ``KeyboardInterrupt`` is
    handled gracefully inside ``CalculatorREPL.run``; this function
    itself will not propagate it.
    """
    calculator = Calculator()
    repl = CalculatorREPL(calculator)
    repl.run()


if __name__ == "__main__":
    main()
