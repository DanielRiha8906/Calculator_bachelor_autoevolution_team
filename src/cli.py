"""cli.py — non-interactive CLI mode for the Calculator.

Provides argument parsing and single-expression execution without launching
the interactive REPL.  Intended for use in scripts and pipelines::

    python -m src.main "add 5 3"
    python -m src.main "factorial 7"
"""

from __future__ import annotations

import argparse
import sys
from typing import Union

from .calculator import Calculator
from .input_handler import ExpressionParser, InputValidator

# Numeric type alias, consistent with input_handler.py.
Numeric = Union[int, float]


class CLIHandler:
    """Execute a single calculator expression in non-interactive mode.

    Parses and validates the expression using the shared ``ExpressionParser``
    and ``InputValidator``, dispatches to the appropriate ``Calculator``
    method, and writes the result to *stdout*.  All error messages are
    written to *stderr* so the output stream stays clean for pipelines.

    Args:
        expression: A whitespace-separated expression string, e.g.
            ``"add 5 3"`` or ``"factorial 7"``.

    Example::

        handler = CLIHandler("power 2 10")
        exit_code = handler.run()
        # prints "1024" to stdout; exit_code == 0
    """

    def __init__(self, expression: str) -> None:
        self._expression = expression
        self._calculator = Calculator()
        self._parser = ExpressionParser()
        self._validator = InputValidator()

    def _dispatch(self, operation: str, operands: list[Numeric]) -> Numeric:
        """Call the appropriate Calculator method.

        Args:
            operation: A validated, lowercased operation name.
            operands: A list of numeric operands.

        Returns:
            The numeric result from the Calculator.

        Raises:
            ZeroDivisionError: Propagated from Calculator.divide.
            ValueError: Propagated from Calculator methods.
            TypeError: Propagated from Calculator methods.
        """
        method = getattr(self._calculator, operation)
        return method(*operands)

    def run(self) -> int:
        """Parse, validate, and execute the expression.

        Prints the numeric result to *stdout* on success.  Prints a
        descriptive error message to *stderr* on any failure.

        Returns:
            ``0`` on success, ``1`` on any error (parse, validation, or
            math error).
        """
        try:
            operation, operands = self._parser.parse(self._expression)
        except ValueError as exc:
            print(f"Input error: {exc}", file=sys.stderr)
            return 1

        try:
            self._validator.validate(operation, operands)
        except ValueError as exc:
            print(f"Validation error: {exc}", file=sys.stderr)
            return 1

        try:
            result = self._dispatch(operation, operands)
        except ZeroDivisionError:
            print("Math error: division by zero.", file=sys.stderr)
            return 1
        except ValueError as exc:
            print(f"Math error: {exc}", file=sys.stderr)
            return 1
        except TypeError as exc:
            print(f"Type error: {exc}", file=sys.stderr)
            return 1

        self._calculator._history.append(operation, operands, result)
        print(result)
        return 0


def main_cli() -> None:
    """Entry point for CLI mode.

    Sets up argument parsing for a single positional ``expression`` argument,
    instantiates a ``CLIHandler``, runs it, and exits with the returned code.

    This function is called by ``src.main`` when command-line arguments are
    present.  It may also be used directly as a standalone entry point.
    """
    parser = argparse.ArgumentParser(
        prog="calculator",
        description=(
            "Evaluate a single calculator expression and print the result. "
            "Example: calculator 'add 5 3'"
        ),
    )
    parser.add_argument(
        "expression",
        help=(
            "The expression to evaluate, as a quoted string. "
            "Format: OPERATION OPERAND1 [OPERAND2]. "
            "Example: 'multiply 6 7'"
        ),
    )

    args = parser.parse_args()
    handler = CLIHandler(args.expression)
    sys.exit(handler.run())
