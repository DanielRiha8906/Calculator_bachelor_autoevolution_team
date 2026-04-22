"""Registry mapping operation keys to Calculator methods with metadata."""

from . import error_logger
from .calculator import Calculator


class OperationRegistry:
    """Maps string keys to Calculator bound methods, their arity, and descriptions.

    Each entry in the registry is a tuple of::

        (bound_method, arity: int, description: str)

    where ``arity`` is the number of operands the method expects (1 or 2).
    """

    def __init__(self, calculator: Calculator) -> None:
        """Build the registry from a Calculator instance.

        Args:
            calculator: The Calculator whose methods are registered.
        """
        self._registry: dict[str, tuple] = {
            "add":         (calculator.add,         2, "Addition (a + b)"),
            "subtract":    (calculator.subtract,    2, "Subtraction (a - b)"),
            "multiply":    (calculator.multiply,    2, "Multiplication (a * b)"),
            "divide":      (calculator.divide,      2, "Division (a / b)"),
            "power":       (calculator.power,       2, "Power (x ^ y)"),
            "factorial":   (calculator.factorial,   1, "Factorial (n!)"),
            "square":      (calculator.square,      1, "Square (x^2)"),
            "cube":        (calculator.cube,        1, "Cube (x^3)"),
            "square_root": (calculator.square_root, 1, "Square root (√x)"),
            "cube_root":   (calculator.cube_root,   1, "Cube root (∛x)"),
            "log":         (calculator.log,         1, "Base-10 logarithm (log₁₀ x)"),
            "ln":          (calculator.ln,          1, "Natural logarithm (ln x)"),
        }

    def get_operation(self, key: str) -> tuple:
        """Return the (method, arity, description) tuple for the given key.

        Args:
            key: The operation identifier string.

        Returns:
            A tuple of (bound_method, arity, description).

        Raises:
            KeyError: If ``key`` is not registered.
        """
        if key not in self._registry:
            _msg = f"Unknown operation: '{key}'"
            error_logger.log_operation_error(key, _msg)
            raise KeyError(_msg)
        return self._registry[key]

    def list_operations(self) -> dict:
        """Return a mapping of operation keys to their display strings.

        Returns:
            Dict mapping each key to its human-readable description.
        """
        return {key: entry[2] for key, entry in self._registry.items()}
