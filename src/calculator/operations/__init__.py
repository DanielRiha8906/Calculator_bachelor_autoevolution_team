"""Operation abstract base class and registry for the modular calculator.

Provides the Operation ABC and OperationRegistry class used to register
and retrieve calculator operations by name (Issue #405).
"""

from abc import ABC, abstractmethod


class Operation(ABC):
    """Abstract base class for all calculator operations.

    Subclasses must implement the ``name``, ``arity``, and ``execute``
    members.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The unique string identifier for this operation."""

    @property
    @abstractmethod
    def arity(self) -> int:
        """The number of operands this operation accepts."""

    @abstractmethod
    def execute(self, *args: float) -> float:
        """Execute the operation on the supplied arguments.

        Args:
            *args: Numeric operands; the count must equal ``self.arity``.

        Returns:
            The numeric result of the operation.
        """


class OperationRegistry:
    """Registry that stores and retrieves Operation instances by name.

    Operations are keyed by their ``name`` property (or by an explicit
    override passed to :meth:`register`).
    """

    def __init__(self) -> None:
        self._ops: dict[str, Operation] = {}

    def register(self, operation: Operation, name: str | None = None) -> None:
        """Register an operation under a given name.

        Args:
            operation: The Operation instance to register.
            name: Override key.  If None, ``operation.name`` is used.
        """
        key = name if name is not None else operation.name
        self._ops[key] = operation

    def get(self, name: str) -> Operation:
        """Return the operation registered under *name*.

        Args:
            name: The operation's key string.

        Returns:
            The registered Operation instance.

        Raises:
            KeyError: If *name* is not in the registry.
        """
        return self._ops[name]

    def list_all(self) -> list[str]:
        """Return a list of all registered operation names.

        Returns:
            A list of key strings in insertion order.
        """
        return list(self._ops.keys())

    def has(self, name: str) -> bool:
        """Return True if *name* is registered, False otherwise.

        Args:
            name: The operation's key string.
        """
        return name in self._ops
