"""operations.py — base abstractions and operation registry for calculator modes.

Provides :class:`BaseOperationSet` as an abstract contract for operation
classes, :class:`OperationRegistry` as a runtime registry that maps operation
names to implementations, and the three canonical constant sets
:data:`BASIC_OPERATIONS`, :data:`ADVANCED_OPERATIONS`, and
:data:`SCIENTIFIC_OPERATIONS`.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Optional


# ---------------------------------------------------------------------------
# Canonical operation name sets
# ---------------------------------------------------------------------------

BASIC_OPERATIONS: frozenset[str] = frozenset(
    {"add", "subtract", "multiply", "divide"}
)

ADVANCED_OPERATIONS: frozenset[str] = frozenset(
    {
        "factorial",
        "square",
        "cube",
        "square_root",
        "cube_root",
        "power",
        "natural_log",
        "log_base_10",
    }
)

SCIENTIFIC_OPERATIONS: frozenset[str] = frozenset(
    {
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "sinh",
        "cosh",
        "tanh",
        "degrees",
        "radians",
        "exp",
        "ln",
    }
)


# ---------------------------------------------------------------------------
# BaseOperationSet
# ---------------------------------------------------------------------------


class BaseOperationSet(ABC):
    """Abstract base class that defines the contract for operation classes.

    Concrete subclasses must implement :meth:`get_operations`, which returns
    a mapping from operation name to callable.  The optional
    ``record_callback`` is injected at construction time and, when provided,
    is called with the result of every operation.

    Args:
        record_callback: An optional callable that accepts a single positional
            argument (the numeric result).  Intended for history recording.
    """

    def __init__(
        self, record_callback: Optional[Callable] = None
    ) -> None:
        self._record_callback = record_callback

    def _record(self, result) -> None:
        """Invoke the record callback if one was provided.

        Args:
            result: The numeric result to pass to the callback.
        """
        if self._record_callback is not None:
            self._record_callback(result)

    @abstractmethod
    def get_operations(self) -> dict[str, Callable]:
        """Return a mapping of operation name to callable.

        Returns:
            A dict whose keys are operation name strings and whose values
            are the bound methods implementing those operations.
        """


# ---------------------------------------------------------------------------
# OperationRegistry
# ---------------------------------------------------------------------------


class OperationRegistry:
    """Maps operation names to their implementations and owning mode.

    Operations are registered per-mode.  Multiple modes may register
    overlapping names; the last registration wins (modes are meant to be
    mutually exclusive in practice).

    Typical usage::

        registry = OperationRegistry()
        basic = BasicOperations()
        registry.register_mode("basic", basic.get_operations())
        fn = registry.get("add")
        result = fn(1, 2)
    """

    def __init__(self) -> None:
        """Initialise an empty registry."""
        self._operations: dict[str, Callable] = {}
        self._operation_mode: dict[str, str] = {}

    def register_mode(self, mode: str, operations: dict[str, Callable]) -> None:
        """Register all operations belonging to a named mode.

        Args:
            mode: A short identifier for the mode (e.g. ``"basic"``).
            operations: A mapping of operation name to callable, as returned
                by :meth:`BaseOperationSet.get_operations`.
        """
        for name, fn in operations.items():
            self._operations[name] = fn
            self._operation_mode[name] = mode

    def get(self, name: str) -> Callable:
        """Look up an operation by name.

        Args:
            name: The operation name (e.g. ``"add"``).

        Returns:
            The callable registered under *name*.

        Raises:
            KeyError: If *name* has not been registered.
        """
        if name not in self._operations:
            raise KeyError(f"Operation '{name}' is not registered.")
        return self._operations[name]

    def get_mode(self, name: str) -> str:
        """Return the mode that registered *name*.

        Args:
            name: The operation name.

        Returns:
            The mode string (e.g. ``"basic"`` or ``"advanced"``).

        Raises:
            KeyError: If *name* has not been registered.
        """
        if name not in self._operation_mode:
            raise KeyError(f"Operation '{name}' is not registered.")
        return self._operation_mode[name]

    def all_names(self) -> frozenset[str]:
        """Return the set of all registered operation names.

        Returns:
            A :class:`frozenset` of operation name strings.
        """
        return frozenset(self._operations.keys())
