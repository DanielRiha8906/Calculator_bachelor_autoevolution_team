"""input_handler.py — user-facing input layer for the Calculator.

Provides three cooperating classes:

- ``InputValidator``: validates expression format and operand types before
  any Calculator method is invoked.
- ``ExpressionParser``: converts a raw input string into an
  ``(operation, operands)`` tuple ready for dispatch.
- ``CalculatorREPL``: wraps a ``Calculator`` instance in a
  read-eval-print loop that runs until the user exits.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union

from .calculator import Calculator


# ---------------------------------------------------------------------------
# RetryConfig
# ---------------------------------------------------------------------------


@dataclass
class RetryConfig:
    """Configuration for the bad-input retry behaviour in ``CalculatorREPL``.

    Attributes:
        max_retries: Maximum number of times the REPL re-prompts the user
            after an invalid expression before returning to the main prompt.
            Must be a positive integer.  Defaults to ``3``.
    """

    max_retries: int = field(default=3)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Maps operation name → expected number of operands.
_ONE_OPERAND_OPS: frozenset[str] = frozenset(
    {
        "factorial",
        "square",
        "cube",
        "square_root",
        "cube_root",
        "natural_log",
        "log_base_10",
    }
)

_TWO_OPERAND_OPS: frozenset[str] = frozenset(
    {
        "add",
        "subtract",
        "multiply",
        "divide",
        "power",
    }
)

SUPPORTED_OPERATIONS: frozenset[str] = _ONE_OPERAND_OPS | _TWO_OPERAND_OPS

# Numeric type alias used throughout this module.
Numeric = Union[int, float]


# ---------------------------------------------------------------------------
# InputValidator
# ---------------------------------------------------------------------------


class InputValidator:
    """Validate a parsed expression before it reaches the Calculator.

    All validation methods raise ``ValueError`` with a human-readable
    message on failure and return ``None`` on success.
    """

    def validate_operation(self, operation: str) -> None:
        """Check that *operation* is a supported Calculator method name.

        Args:
            operation: The lowercased operation token from user input.

        Raises:
            ValueError: If the operation is not recognised.
        """
        if operation not in SUPPORTED_OPERATIONS:
            raise ValueError(
                f"Unknown operation '{operation}'. "
                f"Supported operations: {', '.join(sorted(SUPPORTED_OPERATIONS))}"
            )

    def validate_operand_count(self, operation: str, operands: list[Numeric]) -> None:
        """Check that the number of operands matches what *operation* expects.

        Args:
            operation: The validated operation name.
            operands: The list of already-parsed numeric operands.

        Raises:
            ValueError: If the operand count is wrong.
        """
        if operation in _ONE_OPERAND_OPS:
            expected = 1
        else:
            expected = 2

        if len(operands) != expected:
            raise ValueError(
                f"Operation '{operation}' expects {expected} operand(s), "
                f"got {len(operands)}."
            )

    def validate(self, operation: str, operands: list[Numeric]) -> None:
        """Run all validation checks for an expression.

        Args:
            operation: The lowercased operation token.
            operands: The list of numeric operands.

        Raises:
            ValueError: If any check fails.
        """
        self.validate_operation(operation)
        self.validate_operand_count(operation, operands)


# ---------------------------------------------------------------------------
# ExpressionParser
# ---------------------------------------------------------------------------


class ExpressionParser:
    """Parse a raw input string into a validated (operation, operands) tuple.

    Expected input format::

        OPERATION OPERAND1 [OPERAND2]

    Examples::

        "add 5 3"
        "square 7"
        "power 2 3"
        "factorial 5"

    Operation names are case-insensitive.
    """

    def _coerce_numeric(self, token: str) -> Numeric:
        """Convert a string token to int or float.

        Tries ``int`` first so that integer-valued inputs (e.g. ``"5"``)
        keep their type, which matters for ``factorial``.

        Args:
            token: A raw string that should represent a number.

        Returns:
            The value as ``int`` if it represents a whole number, else
            ``float``.

        Raises:
            ValueError: If the token cannot be parsed as a number.
        """
        try:
            return int(token)
        except ValueError:
            pass
        try:
            return float(token)
        except ValueError:
            raise ValueError(
                f"'{token}' is not a valid number. "
                "Operands must be integers or decimal numbers."
            )

    def parse(self, raw_input: str) -> tuple[str, list[Numeric]]:
        """Parse *raw_input* into an ``(operation, operands)`` tuple.

        Args:
            raw_input: A whitespace-separated expression string from the
                user, e.g. ``"add 5 3"`` or ``"SQUARE 7"``.

        Returns:
            A 2-tuple of ``(operation_name, [operand, ...])``.  The
            operation name is lowercased.

        Raises:
            ValueError: If the input is empty or the operands cannot be
                parsed as numbers.
        """
        tokens = raw_input.strip().split()
        if not tokens:
            raise ValueError("Empty input. Please enter an expression.")

        operation = tokens[0].lower()
        operands: list[Numeric] = [
            self._coerce_numeric(tok) for tok in tokens[1:]
        ]
        return operation, operands


# ---------------------------------------------------------------------------
# CalculatorREPL
# ---------------------------------------------------------------------------


class CalculatorREPL:
    """Interactive read-eval-print loop for the Calculator.

    Wraps a ``Calculator`` instance and repeatedly reads one expression
    per line from *stdin*, evaluates it, and prints the result.  The
    loop exits cleanly on ``KeyboardInterrupt`` or when the user types
    ``exit`` / ``quit``.

    Args:
        calculator: A ``Calculator`` instance to delegate computation to.
    """

    _EXIT_COMMANDS: frozenset[str] = frozenset({"exit", "quit"})

    def __init__(
        self,
        calculator: Calculator,
        retry_config: RetryConfig | None = None,
    ) -> None:
        self._calculator = calculator
        self._parser = ExpressionParser()
        self._validator = InputValidator()
        self._retry_config: RetryConfig = retry_config or RetryConfig()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _dispatch(self, operation: str, operands: list[Numeric]) -> Numeric:
        """Call the appropriate Calculator method.

        Args:
            operation: A validated, lowercased operation name.
            operands: A list of numeric operands.

        Returns:
            The numeric result from the Calculator.

        Raises:
            AttributeError: Should not happen for validated operations, but
                propagated if it does.
            ZeroDivisionError: Propagated from Calculator.divide.
            ValueError: Propagated from Calculator methods.
            TypeError: Propagated from Calculator methods.
        """
        method = getattr(self._calculator, operation)
        return method(*operands)

    def _evaluate(self, raw_input: str) -> str:
        """Parse, validate, execute one expression, and format the result.

        Args:
            raw_input: The raw string entered by the user.

        Returns:
            A human-readable result string (either the answer or an error
            message).
        """
        try:
            operation, operands = self._parser.parse(raw_input)
        except ValueError as exc:
            return f"Input error: {exc}"

        try:
            self._validator.validate(operation, operands)
        except ValueError as exc:
            return f"Validation error: {exc}"

        try:
            result = self._dispatch(operation, operands)
        except ZeroDivisionError:
            return "Math error: division by zero."
        except ValueError as exc:
            return f"Math error: {exc}"
        except TypeError as exc:
            return f"Type error: {exc}"

        self._calculator._history.append(operation, operands, result)
        return f"Result: {result}"

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the interactive REPL.

        Reads expressions from *stdin* in a loop, prints results, and
        stops on ``KeyboardInterrupt`` or when the user types ``exit`` /
        ``quit``.

        The loop never raises; all errors are printed as messages so the
        session continues until the user explicitly exits.
        """
        print("Calculator REPL — type an expression (e.g. 'add 5 3') or 'exit' to quit.")
        print(f"Supported operations: {', '.join(sorted(SUPPORTED_OPERATIONS))}")

        while True:
            try:
                raw = input("> ").strip()
            except KeyboardInterrupt:
                print("\nInterrupted. Goodbye!")
                break
            except EOFError:
                # Non-interactive stdin (e.g. piped input) is exhausted.
                break

            if not raw:
                continue

            if raw.lower() in self._EXIT_COMMANDS:
                print("Goodbye!")
                break

            response = self._evaluate(raw)
            if response.startswith("Result:"):
                print(response)
                continue

            # Bad input — enter retry loop.
            print(response)
            max_retries = self._retry_config.max_retries
            for attempt in range(1, max_retries + 1):
                try:
                    raw = input(
                        f"Invalid input. Attempt {attempt}/{max_retries}."
                        " Please try again: "
                    ).strip()
                except KeyboardInterrupt:
                    print("\nInterrupted. Goodbye!")
                    return
                except EOFError:
                    return

                if raw.lower() in self._EXIT_COMMANDS:
                    print("Goodbye!")
                    return

                response = self._evaluate(raw)
                if response.startswith("Result:"):
                    print(response)
                    break
                print(response)
            else:
                print("Too many invalid attempts. Returning to main prompt.")
