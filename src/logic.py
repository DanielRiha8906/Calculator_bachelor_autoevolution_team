"""logic.py — pure computation engine for the calculator system.

Contains :class:`CalculatorEngine`, which implements all arithmetic and
mathematical operations along with operation history tracking.  This module
has no UI or IO dependencies and can be used independently of any interface
layer.

Computation is delegated to :class:`~src.modes.basic.BasicOperations` and
:class:`~src.modes.advanced.AdvancedOperations`, which are composed into the
engine at construction time.
"""

from .logger import get_logger
from .modes.basic import BasicOperations
from .modes.advanced import AdvancedOperations

logger = get_logger(__name__)


class CalculatorEngine:
    """Pure computation engine with operation history tracking.

    Provides all arithmetic and mathematical operations.  Each successful
    operation is appended to an internal history list that can be retrieved
    via :meth:`get_history`.

    Computation is delegated to :class:`~src.modes.basic.BasicOperations`
    and :class:`~src.modes.advanced.AdvancedOperations`, which are injected
    with a history-recording callback.

    No UI or IO dependencies are present in this class; it is safe to
    instantiate and use in any context.

    Args:
        mode: Reserved for future use.  Defaults to ``'basic'``.  Currently
            both basic and advanced operations are always available regardless
            of this setting, preserving full backward compatibility.
    """

    def __init__(self, mode: str = "basic") -> None:
        """Initialise the CalculatorEngine with an empty history.

        Args:
            mode: Operation mode selector.  Defaults to ``'basic'``.
        """
        self._mode = mode
        self._history: list[dict] = []
        # Operation sets are composed in, receiving a partial callback so
        # that they trigger _record_history without knowing about it.
        self._basic = BasicOperations(record_callback=None)
        self._advanced = AdvancedOperations(record_callback=None)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _record_history(
        self,
        operand1,
        operator: str,
        operand2,
        result,
    ) -> None:
        """Append one operation record to the internal history list.

        Args:
            operand1: The primary (or only) operand.
            operator: The operation name (e.g. ``"add"``, ``"square"``).
            operand2: The second operand, or ``None`` for unary operations.
            result: The value returned by the operation.
        """
        self._history.append(
            {
                "operand1": operand1,
                "operator": operator,
                "operand2": operand2,
                "result": result,
            }
        )

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def get_history(self) -> list[dict]:
        """Return the full list of recorded operations.

        Returns:
            A list of dicts, each with keys ``operand1``, ``operator``,
            ``operand2``, and ``result``.  The list is in chronological
            order.  One-operand operations store ``None`` for ``operand2``.
        """
        return self._history

    def add(self, a, b):
        result = self._basic.add(a, b)
        self._record_history(a, "add", b, result)
        return result

    def subtract(self, a, b):
        result = self._basic.subtract(a, b)
        self._record_history(a, "subtract", b, result)
        return result

    def multiply(self, a, b):
        result = self._basic.multiply(a, b)
        self._record_history(a, "multiply", b, result)
        return result

    def divide(self, a, b):
        # ZeroDivisionError is raised inside BasicOperations.divide (with
        # its own logging) and propagates unchanged here.
        result = self._basic.divide(a, b)
        self._record_history(a, "divide", b, result)
        return result

    def factorial(self, n: int) -> int:
        """Compute the factorial of a non-negative integer n.

        Args:
            n: The non-negative integer whose factorial is to be computed.

        Returns:
            The factorial of n (n!).

        Raises:
            TypeError: If n is not an integer (e.g. float, str, list, None).
            ValueError: If n is a negative integer.
        """
        result = self._advanced.factorial(n)
        self._record_history(n, "factorial", None, result)
        return result

    def square(self, x: float) -> float:
        """Return the square of x (x²).

        Args:
            x: The number to square.

        Returns:
            x multiplied by itself.
        """
        result = self._advanced.square(x)
        self._record_history(x, "square", None, result)
        return result

    def cube(self, x: float) -> float:
        """Return the cube of x (x³).

        Args:
            x: The number to cube.

        Returns:
            x multiplied by itself twice.
        """
        result = self._advanced.cube(x)
        self._record_history(x, "cube", None, result)
        return result

    def square_root(self, x: float) -> float:
        """Return the square root of x (√x).

        Args:
            x: The number to take the square root of.

        Returns:
            The non-negative square root of x.

        Raises:
            ValueError: If x is negative.
        """
        result = self._advanced.square_root(x)
        self._record_history(x, "square_root", None, result)
        return result

    def cube_root(self, x: float) -> float:
        """Return the real cube root of x (∛x).

        Supports negative inputs by preserving the sign.

        Args:
            x: The number to take the cube root of.

        Returns:
            The real cube root of x.
        """
        result = self._advanced.cube_root(x)
        self._record_history(x, "cube_root", None, result)
        return result

    def power(self, base: float, exponent: float) -> float:
        """Return base raised to the given exponent (base^exponent).

        Args:
            base: The base number.
            exponent: The exponent to raise the base to.

        Returns:
            base raised to the power of exponent.
        """
        result = self._advanced.power(base, exponent)
        self._record_history(base, "power", exponent, result)
        return result

    def natural_log(self, x: float) -> float:
        """Return the natural logarithm of x (ln(x)).

        Args:
            x: The number to compute the natural log of.

        Returns:
            The natural logarithm of x.

        Raises:
            ValueError: If x is less than or equal to 0.
        """
        result = self._advanced.natural_log(x)
        self._record_history(x, "natural_log", None, result)
        return result

    def log_base_10(self, x: float) -> float:
        """Return the base-10 logarithm of x (log₁₀(x)).

        Args:
            x: The number to compute the base-10 log of.

        Returns:
            The base-10 logarithm of x.

        Raises:
            ValueError: If x is less than or equal to 0.
        """
        result = self._advanced.log_base_10(x)
        self._record_history(x, "log_base_10", None, result)
        return result
