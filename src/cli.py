"""CLI mode handler for non-interactive command-line operation.

Parses operation names/symbols and operands from sys.argv-style argument lists,
dispatches to the Calculator, and returns the raw numeric result.
"""

import math
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.history import OperationHistory

# Operations that take exactly one operand.
_UNARY_OPS: frozenset[str] = frozenset(
    ["factorial", "square", "cube", "square_root", "sqrt", "cube_root", "cbrt",
     "natural_logarithm", "ln"]
)

# Operations that take exactly two operands.
_BINARY_OPS: frozenset[str] = frozenset(
    ["add", "+", "subtract", "-", "multiply", "*", "divide", "/",
     "power", "^", "logarithm", "log"]
)


class CLIHandler:
    """Handle non-interactive CLI operation for the calculator.

    Parses a list of string arguments representing an operation and its
    operands, dispatches to the underlying Calculator instance, and returns
    the numeric result.

    Args:
        calculator: A Calculator instance whose methods will be called.
        history: An optional ``OperationHistory`` instance used to record each
            completed operation.  When ``None``, history recording is disabled.
    """

    def __init__(self, calculator: Any, history: "OperationHistory | None" = None) -> None:
        self.calculator = calculator
        self.history = history

    def get_operation_mapping(self) -> dict[str, str]:
        """Return a mapping from operation names and symbols to Calculator method names.

        Returns:
            A dict where keys are accepted operation strings (names or symbols)
            and values are the corresponding Calculator method names.
        """
        return {
            "add": "add",
            "+": "add",
            "subtract": "subtract",
            "-": "subtract",
            "multiply": "multiply",
            "*": "multiply",
            "divide": "divide",
            "/": "divide",
            "power": "power",
            "^": "power",
            "logarithm": "logarithm",
            "log": "logarithm",
            "factorial": "factorial",
            "square": "square",
            "cube": "cube",
            "square_root": "square_root",
            "sqrt": "square_root",
            "cube_root": "cube_root",
            "cbrt": "cube_root",
            "natural_logarithm": "natural_logarithm",
            "ln": "natural_logarithm",
        }

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
        mapping = self.get_operation_mapping()

        if raw_op not in mapping:
            raise ValueError(f"Unknown operation: {raw_op!r}")

        method_name = mapping[raw_op]
        operand_strings = args[1:]

        if raw_op in _UNARY_OPS or method_name in {
            "factorial", "square", "cube", "square_root", "cube_root", "natural_logarithm"
        }:
            expected = 1
        else:
            expected = 2

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
        Calculator.  The "logarithm" operation is treated as a two-argument
        logarithm: log(x, base), matching the REPL behaviour.

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
        method_name, operands = self.parse_args(args)

        if method_name == "logarithm":
            x, base = operands
            if base <= 0 or base == 1:
                raise ValueError("logarithm base must be positive and not equal to 1")
            if x <= 0:
                raise ValueError("logarithm() not defined for non-positive values")
            result = math.log(x, base)
        else:
            method = getattr(self.calculator, method_name)
            result = method(*operands)

        if self.history is not None:
            operand_str = ", ".join(str(o) for o in operands)
            entry = f"{method_name}({operand_str}) = {result}"
            self.history.record_operation(entry)

        return result
