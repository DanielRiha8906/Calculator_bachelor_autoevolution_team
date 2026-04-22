"""Pure calculation engine that orchestrates operation execution."""

from .calculator import Calculator
from .operations import OperationRegistry


class CalculationEngine:
    """Executes calculator operations using a Calculator and OperationRegistry.

    This class is a pure computation layer with no I/O or UI dependencies.
    It retrieves the appropriate method from the registry, invokes it with the
    supplied operands, and returns the result.  Any domain or arithmetic
    exceptions raised by the underlying Calculator methods are propagated
    unchanged to the caller.
    """

    def __init__(self, calculator: Calculator, registry: OperationRegistry) -> None:
        """Initialise the engine with a Calculator and an OperationRegistry.

        Args:
            calculator: The Calculator instance whose methods perform arithmetic.
            registry: The OperationRegistry that maps operation keys to methods.
        """
        self._calculator: Calculator = calculator
        self._registry: OperationRegistry = registry

    def execute_operation(self, operation_key: str, operands: list[float]) -> float:
        """Execute a named operation with the given operands and return the result.

        Looks up ``operation_key`` in the registry to obtain the bound method,
        then calls that method with the unpacked ``operands`` list.

        Args:
            operation_key: The string identifier for the operation (e.g. ``"add"``).
            operands: A list of numeric operand values.  The length must match
                the arity recorded in the registry.

        Returns:
            The numeric result of the operation.

        Raises:
            KeyError: If ``operation_key`` is not found in the registry.
            ValueError: If the operands are invalid for the requested operation
                (e.g. negative input for square root, non-integer for factorial).
            ZeroDivisionError: If the operation attempts division by zero.
        """
        method, _arity, _description = self._registry.get_operation(operation_key)
        return method(*operands)
