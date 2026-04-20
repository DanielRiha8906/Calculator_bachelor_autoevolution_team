"""CLI mode handler for non-interactive command-line operation.

Parses operation names/symbols and operands from sys.argv-style argument lists,
dispatches to the Calculator via :class:`~src.core.operations.OperationRegistry`,
and returns the raw numeric result.
"""

from typing import TYPE_CHECKING, Any, Optional

from src.support.error_logger import ErrorLogger
from src.core.operations import OperationRegistry
from src.context import CalculatorContext

if TYPE_CHECKING:
    from src.support.history import OperationHistory


class CLIHandler:
    """Handle non-interactive CLI operation for the calculator.

    Parses a list of string arguments representing an operation and its
    operands, dispatches to the underlying Calculator instance via the
    :class:`~src.core.operations.OperationRegistry`, and returns the numeric result.

    Args:
        calculator: A Calculator instance whose methods will be called.
        history: An optional ``OperationHistory`` instance used to record each
            completed operation.  When ``None``, history recording is disabled.
        error_logger: An optional ``ErrorLogger`` instance used to record
            errors encountered during execution.  When ``None``, error
            logging is disabled.
        context: An optional :class:`~src.context.CalculatorContext` instance
            used to determine the active operating mode.  When ``None``, a
            fresh context (default ``"normal"`` mode) is created internally.
    """

    def __init__(
        self,
        calculator: Any,
        history: "OperationHistory | None" = None,
        error_logger: ErrorLogger | None = None,
        context: Optional[CalculatorContext] = None,
    ) -> None:
        self.calculator = calculator
        self.history = history
        self.error_logger = error_logger
        self._context: CalculatorContext = context if context is not None else CalculatorContext()
        self._registry = OperationRegistry(calculator)
        # Sync registry mode with the context at construction time.
        self._registry.set_mode(self._context.get_mode())

    def get_operation_mapping(self) -> dict[str, str]:
        """Return a mapping from operation names and symbols to Calculator method names.

        Delegates to :class:`~src.core.operations.OperationRegistry` so that the
        operation catalog is defined in a single place.

        Returns:
            A dict where keys are accepted operation strings (names or symbols)
            and values are the corresponding canonical Calculator method names.
        """
        return self._registry.get_operation_mapping()

    def parse_args(self, args: list[str]) -> tuple[str, list[float]]:
        """Parse a list of argument strings into an operation name and operands.

        The first element of args is expected to be the operation name or symbol.
        Subsequent elements are expected to be numeric operand strings.

        Args:
            args: A list of strings, e.g. ["add", "3", "4"] or ["+", "3", "4"].

        Returns:
            A tuple of (canonical_operation_name, [operand, ...]).

        Raises:
            ValueError: If the operation is unknown, operand count is wrong,
                        or any operand cannot be parsed as a number.
        """
        if not args:
            raise ValueError("Missing operand(s) for operation: no arguments provided")

        raw_op = args[0]

        try:
            method_name = self._registry.resolve(raw_op)
        except ValueError:
            raise ValueError(f"Unknown operation: {raw_op!r}")

        expected = self._registry.arity(raw_op)
        operand_strings = args[1:]

        if len(operand_strings) != expected:
            raise ValueError(
                f"Missing operand(s) for {raw_op!r}: "
                f"expected {expected} operand(s), got {len(operand_strings)}"
            )

        operands: list[float] = []
        for token in operand_strings:
            try:
                operands.append(float(token))
            except ValueError:
                raise ValueError(f"Invalid number: {token!r}")

        return method_name, operands

    def execute(self, args: list[str]) -> float:
        """Execute the operation described by args and return the numeric result.

        Parses the operation and operands from args, then dispatches to the
        Calculator via the :class:`~src.core.operations.OperationRegistry`.  The
        ``logarithm`` operation is treated as a two-argument logarithm:
        ``log(x, base)``, matching the REPL behaviour.

        Errors are logged via ``self.error_logger`` (if set) before being
        re-raised:

        - ``UNSUPPORTED_OPERATION`` when the operation name is not recognised.
        - ``INVALID_INPUT`` when operand count or format is wrong.
        - ``CALCULATION_ERROR`` when the calculator raises a numeric error.

        Args:
            args: A list of strings in the form [operation, operand, ...].

        Returns:
            The numeric result of the operation.

        Raises:
            ValueError: If the operation is unknown, operands are invalid, or
                        the calculator raises a domain error.
            ZeroDivisionError: If the calculator raises a division-by-zero error.
            TypeError: Propagated from Calculator (e.g. factorial of a float).
        """
        raw_op = args[0] if args else ""
        user_input = " ".join(args)

        try:
            method_name, operands = self.parse_args(args)
        except ValueError as exc:
            if self.error_logger is not None:
                error_message = str(exc)
                if "Unknown operation" in error_message:
                    self.error_logger.log_error(
                        ErrorLogger.UNSUPPORTED_OPERATION, user_input, exc
                    )
                else:
                    self.error_logger.log_error(
                        ErrorLogger.INVALID_INPUT, user_input, exc
                    )
            raise

        try:
            result = self._registry.dispatch(method_name, operands)
        except (ValueError, ZeroDivisionError, TypeError) as exc:
            if self.error_logger is not None:
                self.error_logger.log_error(
                    ErrorLogger.CALCULATION_ERROR, user_input, exc
                )
            raise

        if self.history is not None:
            operand_str = ", ".join(str(o) for o in operands)
            entry = f"{method_name}({operand_str}) = {result}"
            self.history.record_operation(entry)

        return result
