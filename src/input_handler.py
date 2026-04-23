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
from .logger import get_logger
from .modes.operations import BASIC_OPERATIONS, ADVANCED_OPERATIONS, SCIENTIFIC_OPERATIONS

logger = get_logger(__name__)


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
# Exceptions
# ---------------------------------------------------------------------------


class OperationNotAvailableInModeError(ValueError):
    """Raised when an operation is invoked in a mode that does not support it.

    Attributes:
        operation: The operation name that was attempted.
        current_mode: The mode the calculator was in when the error occurred.
        available_modes: Sorted list of modes that do support the operation.
    """

    def __init__(
        self,
        operation: str,
        current_mode: str,
        available_modes: list[str],
    ) -> None:
        """Initialise with details about the unsupported operation.

        Args:
            operation: The operation name that was attempted.
            current_mode: The mode the calculator was in.
            available_modes: Sorted list of modes that do support the operation.
        """
        self.operation = operation
        self.current_mode = current_mode
        self.available_modes = available_modes
        super().__init__(str(self))

    def __str__(self) -> str:
        if not self.available_modes:
            return (
                f"Operation '{self.operation}' is not available in "
                f"'{self.current_mode}' mode."
            )
        switch_hint = f"Type 'mode {self.available_modes[0]}' to switch."
        modes_str = ", ".join(self.available_modes)
        return (
            f"Operation '{self.operation}' is not available in "
            f"'{self.current_mode}' mode. "
            f"Available in: {modes_str}. "
            f"{switch_hint}"
        )


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Maps operation name → expected number of operands.
# Populated from the canonical sets in modes.operations so that any future
# addition to those sets is automatically reflected here.
_ONE_OPERAND_OPS: frozenset[str] = frozenset(
    (ADVANCED_OPERATIONS - {"power"}) | SCIENTIFIC_OPERATIONS
)

_TWO_OPERAND_OPS: frozenset[str] = frozenset(
    BASIC_OPERATIONS | {"power"}
)

SUPPORTED_OPERATIONS: frozenset[str] = (
    BASIC_OPERATIONS | ADVANCED_OPERATIONS | SCIENTIFIC_OPERATIONS
)

_VALID_MODES: frozenset[str] = frozenset({"basic", "advanced", "scientific"})

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
            exc = ValueError(
                f"Unknown operation '{operation}'. "
                f"Supported operations: {', '.join(sorted(SUPPORTED_OPERATIONS))}"
            )
            logger.warning(
                "validate_operation() failed: operation=%r %s: %s",
                operation,
                type(exc).__name__,
                exc,
            )
            raise exc

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
            exc = ValueError(
                f"Operation '{operation}' expects {expected} operand(s), "
                f"got {len(operands)}."
            )
            logger.warning(
                "validate_operand_count() failed: operation=%r operands=%r %s: %s",
                operation,
                operands,
                type(exc).__name__,
                exc,
            )
            raise exc

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
        "sin 1.5708"

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
            exc = ValueError(
                f"'{token}' is not a valid number. "
                "Operands must be integers or decimal numbers."
            )
            logger.warning(
                "_coerce_numeric() failed: value=%r %s: %s",
                token,
                type(exc).__name__,
                exc,
            )
            raise exc

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
            exc = ValueError("Empty input. Please enter an expression.")
            logger.warning("parse() failed: empty raw_input %s: %s", type(exc).__name__, exc)
            raise exc

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

    Special commands available during the session:

    - ``history`` — display the operation history.
    - ``mode`` — display the current mode and list available modes.
    - ``mode <name>`` — switch to the named mode (basic, advanced, scientific).
    - ``exit`` / ``quit`` — terminate the session.

    Args:
        calculator: A ``Calculator`` instance to delegate computation to.
        retry_config: Optional retry configuration.  Defaults to
            :class:`RetryConfig` with ``max_retries=3``.
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

    def _get_available_modes_for_operation(self, operation: str) -> list[str]:
        """Return which modes support a given operation.

        Delegates to :meth:`~src.calculator.Calculator.get_available_modes_for_operation`.

        Args:
            operation: The operation name to look up.

        Returns:
            A sorted list of mode name strings that support the operation.
        """
        return self._calculator.get_available_modes_for_operation(operation)

    def _dispatch(self, operation: str, operands: list[Numeric]) -> Numeric:
        """Call the appropriate Calculator method.

        Args:
            operation: A validated, lowercased operation name.
            operands: A list of numeric operands.

        Returns:
            The numeric result from the Calculator.

        Raises:
            OperationNotAvailableInModeError: If the operation is not
                supported in the current calculator mode.
            ZeroDivisionError: Propagated from Calculator.divide.
            ValueError: Propagated from Calculator methods for non-mode errors.
            TypeError: Propagated from Calculator methods.
        """
        try:
            method = getattr(self._calculator, operation)
            return method(*operands)
        except ValueError as exc:
            # Re-raise as OperationNotAvailableInModeError when the engine
            # signals that the current mode does not support this operation.
            if "not available in" in str(exc):
                current_mode = self._calculator._engine._mode
                available = self._get_available_modes_for_operation(operation)
                raise OperationNotAvailableInModeError(
                    operation, current_mode, available
                ) from exc
            raise

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
        except OperationNotAvailableInModeError as exc:
            logger.warning(
                "_evaluate() mode error: raw_input=%r operation=%r current_mode=%r"
                " available_modes=%r",
                raw_input,
                operation,
                exc.current_mode,
                exc.available_modes,
            )
            if exc.available_modes:
                modes_str = ", ".join(exc.available_modes)
                switch_cmd = f"mode {exc.available_modes[0]}"
                return (
                    f"'{exc.operation}' is not available in {exc.current_mode} mode.\n"
                    f"Available in: {modes_str}.\n"
                    f"To switch: type '{switch_cmd}'"
                )
            return (
                f"'{exc.operation}' is not available in {exc.current_mode} mode."
            )
        except ZeroDivisionError as exc:
            logger.error(
                "_evaluate() dispatch error: raw_input=%r operation=%r operands=%r"
                " %s: %s",
                raw_input,
                operation,
                operands,
                type(exc).__name__,
                exc,
            )
            return "Math error: division by zero."
        except ValueError as exc:
            logger.error(
                "_evaluate() dispatch error: raw_input=%r operation=%r operands=%r"
                " %s: %s",
                raw_input,
                operation,
                operands,
                type(exc).__name__,
                exc,
            )
            return f"Math error: {exc}"
        except TypeError as exc:
            logger.error(
                "_evaluate() dispatch error: raw_input=%r operation=%r operands=%r"
                " %s: %s",
                raw_input,
                operation,
                operands,
                type(exc).__name__,
                exc,
            )
            return f"Type error: {exc}"

        return f"Result: {result}"

    def _handle_mode_command(self, args: str) -> None:
        """Handle the ``mode`` REPL command.

        With no argument, prints the current mode and the list of valid
        modes.  With a valid mode name as argument, switches the calculator
        to that mode and confirms to the user.  With an invalid argument,
        prints an error and lists the valid modes.

        Args:
            args: The portion of the user's input after the ``"mode"``
                keyword, stripped of surrounding whitespace.  An empty
                string means no argument was provided.
        """
        if not args:
            engine_mode = self._calculator._engine._mode
            print(f"Current mode: {engine_mode}")
            print(f"Available modes: {', '.join(sorted(_VALID_MODES))}")
            return

        requested = args.strip().lower()
        if requested not in _VALID_MODES:
            print(
                f"Unknown mode '{requested}'. "
                f"Valid modes: {', '.join(sorted(_VALID_MODES))}"
            )
            return

        try:
            self._calculator.set_mode(requested)
        except ValueError as exc:
            print(f"Mode error: {exc}")
            return

        print(f"Mode switched to '{requested}'.")

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
        print("Calculator — type 'exit' to quit.")
        print("Switch modes with: mode basic | mode advanced | mode scientific")
        print("  basic: +, -, *, /")
        print("  advanced: + factorial, power, square, cube, roots, natural_log, log_base_10")
        print("  scientific: + sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, ln, ...")
        print("Type 'history' to view past operations.")
        print("Type 'mode' to see current mode.")

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

            if raw.lower() == "history":
                history = self._calculator.get_history()
                if not history:
                    print("No history yet.")
                else:
                    for idx, entry in enumerate(history, start=1):
                        op1 = entry["operand1"]
                        operator = entry["operator"]
                        op2 = entry["operand2"]
                        res = entry["result"]
                        if op2 is None:
                            line = f"{idx}. {op1} {operator} = {res}"
                        else:
                            line = f"{idx}. {op1} {operator} {op2} = {res}"
                        print(line)
                continue

            if raw.lower() in self._EXIT_COMMANDS:
                print("Goodbye!")
                break

            # Handle "mode" and "mode <name>" commands.
            lowered = raw.lower()
            if lowered == "mode" or lowered.startswith("mode "):
                # Strip the leading keyword and any surrounding whitespace.
                remainder = raw[4:].strip()
                self._handle_mode_command(remainder)
                continue

            response = self._evaluate(raw)
            if response.startswith("Result:"):
                print(response)
                continue

            # Mode-not-available messages are informational; do not retry.
            if "is not available in" in response and "To switch:" in response:
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
