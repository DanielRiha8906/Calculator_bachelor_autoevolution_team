"""Base abstractions for the operations subsystem.

Defines the ``Operation`` abstract base class and the ``OperationRegistry``
used to register and retrieve named operations at runtime.
"""

import abc
from typing import Optional


class Operation(abc.ABC):
    """Abstract base class for all calculator operations.

    Concrete subclasses must implement ``name``, ``execute``, and
    ``operand_count`` to be usable with ``OperationRegistry``.
    """

    @abc.abstractmethod
    def name(self) -> str:
        """Return the canonical name of this operation.

        Returns:
            A string identifier for the operation (e.g. ``"add"``).
        """

    @abc.abstractmethod
    def execute(self, *args: int | float) -> float:
        """Perform the computation and return the result.

        Args:
            *args: Numeric operands. The number of arguments must match
                ``operand_count()``.

        Returns:
            The numeric result of the operation.
        """

    @abc.abstractmethod
    def operand_count(self) -> int:
        """Return the number of operands this operation requires.

        Returns:
            An integer (1 for unary, 2 for binary, etc.).
        """


class OperationRegistry:
    """Registry that maps operation names to ``Operation`` instances.

    Operations are registered by name and can be retrieved, listed, or
    checked for presence.
    """

    def __init__(self) -> None:
        self._operations: dict[str, Operation] = {}

    def register(self, operation_name: str, op: Operation) -> None:
        """Register an operation under the given name.

        Args:
            operation_name: The string key under which the operation is stored.
            op: The ``Operation`` instance to register.
        """
        self._operations[operation_name] = op

    def get(self, operation_name: str) -> Optional[Operation]:
        """Retrieve a registered operation by name.

        Args:
            operation_name: The name of the operation to look up.

        Returns:
            The ``Operation`` instance if found, or ``None`` if not registered.
        """
        return self._operations.get(operation_name)

    def list_operations(self) -> list[str]:
        """Return a list of all registered operation names.

        Returns:
            A list of operation name strings in insertion order.
        """
        return list(self._operations.keys())

    def is_registered(self, operation_name: str) -> bool:
        """Check whether an operation name has been registered.

        Args:
            operation_name: The name to check.

        Returns:
            ``True`` if the name is registered, ``False`` otherwise.
        """
        return operation_name in self._operations
