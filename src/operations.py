"""Registry mapping operation keys to Calculator methods with metadata.

The registry is intentionally open to extension: third-party or scientific
operations can be added at runtime without modifying this module or
``Calculator``.  Example::

    import math
    from src.operations import OperationRegistry
    from src.calculator import Calculator

    calc = Calculator()
    registry = OperationRegistry(calc)

    # Register a new scientific operation — sine with one operand.
    registry.register_operation(
        key="sin",
        method=math.sin,
        arity=1,
        description="Sine of x in radians (sin x)",
    )

    # The engine will now resolve "sin" like any built-in operation.
"""

from . import error_logger
from .calculator import Calculator


class OperationRegistry:
    """Maps string keys to Calculator bound methods, their arity, and descriptions.

    Each entry in the registry is a tuple of::

        (bound_method, arity: int, description: str)

    where ``arity`` is the number of operands the method expects (1 or 2).

    Built-in operations are populated in ``__init__``.  Additional operations
    can be added at any time via :meth:`register_operation` without subclassing
    or modifying this file.  Any operation registered this way is immediately
    available to ``CalculationEngine.execute_operation``.

    Example — adding a scientific function after construction::

        registry.register_operation(
            key="sin",
            method=math.sin,
            arity=1,
            description="Sine of x in radians (sin x)",
        )
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

    def register_operation(
        self,
        key: str,
        method: callable,
        arity: int,
        description: str,
    ) -> None:
        """Register a new operation in the registry.

        Allows callers to extend the registry with custom or scientific
        operations at runtime without modifying this module or
        ``Calculator``.

        Args:
            key: Unique string identifier for the operation (e.g. ``"sin"``).
                Must not already exist in the registry.
            method: A callable that accepts exactly ``arity`` positional
                numeric arguments and returns a numeric result.
            arity: The number of operands the operation expects.  Must be a
                positive integer (>= 1).
            description: A short human-readable description shown by
                :meth:`list_operations` (e.g. ``"Sine of x in radians"``).

        Raises:
            ValueError: If ``key`` is already registered, or if ``arity`` is
                not a positive integer.
            TypeError: If ``method`` is not callable.
        """
        if key in self._registry:
            raise ValueError(
                f"Operation '{key}' is already registered. "
                "Use a different key or remove the existing entry first."
            )
        if not callable(method):
            raise TypeError(
                f"'method' must be callable, got {type(method).__name__!r}."
            )
        if not isinstance(arity, int) or isinstance(arity, bool) or arity < 1:
            raise ValueError(
                f"'arity' must be a positive integer, got {arity!r}."
            )
        self._registry[key] = (method, arity, description)
