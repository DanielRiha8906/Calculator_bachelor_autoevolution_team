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
from .core.operations import OperationMetadata, OperationMode, OperationType

# The 12 operations originally available before trigonometric functions were added.
# get_operations() returns exactly these names (backward compatibility with existing tests
# and integrations that relied on a fixed 12-operation set).
_LEGACY_OPERATIONS: frozenset[str] = frozenset({
    "add", "subtract", "multiply", "divide", "square", "sqrt",
    "power", "factorial", "cube", "cbrt", "ln", "log10",
})

_OPERATION_METADATA: dict[str, OperationMetadata] = {
    "add":      OperationMetadata("add",      2, OperationType.BINARY, "Add two numbers", OperationMode.NORMAL),
    "subtract": OperationMetadata("subtract", 2, OperationType.BINARY, "Subtract",        OperationMode.NORMAL),
    "multiply": OperationMetadata("multiply", 2, OperationType.BINARY, "Multiply",        OperationMode.NORMAL),
    "divide":   OperationMetadata("divide",   2, OperationType.BINARY, "Divide",          OperationMode.NORMAL),
    "square":   OperationMetadata("square",   1, OperationType.UNARY,  "Square",          OperationMode.NORMAL),
    "sqrt":     OperationMetadata("sqrt",     1, OperationType.UNARY,  "Square root",     OperationMode.NORMAL),
    "power":    OperationMetadata("power",    2, OperationType.BINARY, "Power",           OperationMode.SCIENTIFIC),
    "factorial":OperationMetadata("factorial",1, OperationType.UNARY,  "Factorial",       OperationMode.SCIENTIFIC),
    "cube":     OperationMetadata("cube",     1, OperationType.UNARY,  "Cube",            OperationMode.SCIENTIFIC),
    "cbrt":     OperationMetadata("cbrt",     1, OperationType.UNARY,  "Cube root",       OperationMode.SCIENTIFIC),
    "ln":       OperationMetadata("ln",       1, OperationType.UNARY,  "Natural log",     OperationMode.SCIENTIFIC),
    "log10":    OperationMetadata("log10",    1, OperationType.UNARY,  "Log base 10",     OperationMode.SCIENTIFIC),
    "sin":      OperationMetadata("sin",      1, OperationType.UNARY,  "Sine",            OperationMode.SCIENTIFIC),
    "cos":      OperationMetadata("cos",      1, OperationType.UNARY,  "Cosine",          OperationMode.SCIENTIFIC),
    "tan":      OperationMetadata("tan",      1, OperationType.UNARY,  "Tangent",         OperationMode.SCIENTIFIC),
    "cot":      OperationMetadata("cot",      1, OperationType.UNARY,  "Cotangent",       OperationMode.SCIENTIFIC),
    "asin":     OperationMetadata("asin",     1, OperationType.UNARY,  "Arcsine",         OperationMode.SCIENTIFIC),
    "acos":     OperationMetadata("acos",     1, OperationType.UNARY,  "Arccosine",       OperationMode.SCIENTIFIC),
}


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
        """Return a sorted list of the 12 core (pre-trigonometric) operation names.

        Returns only the original 12 operations for backward compatibility with
        callers that rely on a fixed operation count and ordering. Use
        ``get_operations_by_mode`` to access the full operation set including
        trigonometric functions.

        Returns:
            A sorted list of 12 operation name strings in alphabetical order.
        """
        return sorted(
            name for name in self._operations if name in _LEGACY_OPERATIONS
        )

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

    def get_operation_metadata(self, operation_name: str) -> OperationMetadata:
        """Return metadata for a named operation.

        Args:
            operation_name: The name of a registered operation.

        Returns:
            The ``OperationMetadata`` for the named operation.

        Raises:
            KeyError: If ``operation_name`` is not in the metadata dictionary.
        """
        return _OPERATION_METADATA[operation_name]

    def get_operation_mode(self, operation_name: str) -> OperationMode:
        """Return the OperationMode for an operation.

        Args:
            operation_name: The name of a registered operation.

        Returns:
            The ``OperationMode`` (NORMAL or SCIENTIFIC) for the named operation.

        Raises:
            KeyError: If ``operation_name`` is not in the metadata dictionary.
        """
        return _OPERATION_METADATA[operation_name].mode

    def get_operations_by_mode(self, mode: OperationMode) -> list[str]:
        """Return sorted list of operation names available in the given mode.

        NORMAL mode returns only the 6 normal operations.
        SCIENTIFIC mode returns all 18 operations (normal + scientific).

        Args:
            mode: The ``OperationMode`` to filter by.

        Returns:
            A sorted list of operation name strings for the requested mode.
        """
        if mode == OperationMode.SCIENTIFIC:
            return sorted(_OPERATION_METADATA.keys())
        return sorted(
            [name for name, meta in _OPERATION_METADATA.items() if meta.mode == mode]
        )
