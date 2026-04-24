"""Layer-agnostic operation discovery and invocation registry.

This module is INDEPENDENT of interactive.py, cli.py, history.py, and
error_logger.py.  It sits between the calculation core and any presentation
layer, providing a single, uniform way to discover and call Calculator
operations without coupling callers to the Calculator class directly.

Both the interactive terminal layer (interactive.py) and the command-line
layer (cli.py) use this module to discover available operations and invoke
them by name.

Design pattern: Registry — operations are registered once at construction
time via introspection and looked up by name at call time.
"""

import inspect
from typing import Any, List

from .calculator import Calculator


class OperationRegistry:
    """Discovers and exposes calculator operations via introspection.

    Uses ``inspect.signature`` to enumerate all public callable methods on the
    provided ``Calculator`` instance, retaining only those with arity 1 or 2
    (excluding ``self``).

    Args:
        calculator: A ``Calculator`` instance whose methods are to be registered.
    """

    def __init__(self, calculator: Calculator) -> None:
        self._calculator = calculator
        self._operations: dict[str, int] = {}

        for name, method in inspect.getmembers(calculator, predicate=inspect.ismethod):
            if name.startswith("_"):
                continue
            params = list(inspect.signature(method).parameters.keys())
            arity = len(params)
            if arity in (1, 2):
                self._operations[name] = arity

        # Sorted list is computed once for deterministic ordering.
        self._sorted_names: List[str] = sorted(self._operations.keys())

    def get_operations(self) -> List[str]:
        """Return a sorted list of discovered operation names.

        Returns:
            A list of operation name strings in alphabetical order.
        """
        return list(self._sorted_names)

    def get_arity(self, operation_name: str) -> int:
        """Return the arity (number of operands) for the named operation.

        Args:
            operation_name: The name of a registered operation.

        Returns:
            1 for unary operations, 2 for binary operations.

        Raises:
            KeyError: If ``operation_name`` is not a registered operation.
        """
        return self._operations[operation_name]

    def call(self, operation_name: str, *args: Any) -> Any:
        """Invoke the named operation with the supplied arguments.

        Args:
            operation_name: The name of a registered operation.
            *args: Positional arguments forwarded to the operation.

        Returns:
            The result returned by the calculator method.

        Raises:
            KeyError: If ``operation_name`` is not a registered operation.
            Any exception the underlying calculator method raises.
        """
        method = getattr(self._calculator, operation_name)
        return method(*args)
