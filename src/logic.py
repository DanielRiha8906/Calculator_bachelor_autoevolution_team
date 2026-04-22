"""logic.py — pure computation engine for the calculator system.

Contains :class:`CalculatorEngine`, which implements all arithmetic and
mathematical operations along with operation history tracking.  This module
has no UI or IO dependencies and can be used independently of any interface
layer.

Computation is delegated to the appropriate operation-set objects
(:class:`~src.modes.basic.BasicOperations`,
:class:`~src.modes.advanced.AdvancedOperations`, and
:class:`~src.modes.scientific.ScientificOperations`), which are composed into
the engine at construction time based on the active *mode*.

Supported modes
---------------
``"basic"``
    Only :class:`~src.modes.basic.BasicOperations` (add, subtract, multiply,
    divide).
``"advanced"``
    :class:`~src.modes.basic.BasicOperations` **plus**
    :class:`~src.modes.advanced.AdvancedOperations` (factorial, square, …).
``"scientific"``
    All of the above **plus**
    :class:`~src.modes.scientific.ScientificOperations` (sin, cos, ln, …).
"""

from .logger import get_logger
from .modes.basic import BasicOperations
from .modes.advanced import AdvancedOperations
from .modes.scientific import ScientificOperations

logger = get_logger(__name__)

_VALID_MODES: frozenset[str] = frozenset({"basic", "advanced", "scientific"})


class CalculatorEngine:
    """Pure computation engine with operation history tracking.

    Provides arithmetic and mathematical operations.  Each successful
    operation is appended to an internal history list that can be retrieved
    via :meth:`get_history`.

    Computation is delegated to one or more operation-set objects selected
    by the *mode* parameter.  The active mode can be changed at runtime via
    :meth:`set_mode` without clearing history.

    No UI or IO dependencies are present in this class; it is safe to
    instantiate and use in any context.

    Args:
        mode: Operation mode selector.  One of ``"basic"``, ``"advanced"``,
            or ``"scientific"``.  Defaults to ``"advanced"`` for backward
            compatibility (both basic and advanced operations are available).
    """

    def __init__(self, mode: str = "advanced") -> None:
        """Initialise the CalculatorEngine with an empty history.

        Args:
            mode: Operation mode selector.  Defaults to ``"advanced"``.

        Raises:
            ValueError: If *mode* is not one of the recognised mode strings.
        """
        self._history: list[dict] = []
        self._basic: BasicOperations | None = None
        self._advanced: AdvancedOperations | None = None
        self._scientific: ScientificOperations | None = None
        self._mode: str = ""
        self._activate_mode(mode)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _activate_mode(self, mode: str) -> None:
        """Instantiate operation sets appropriate for *mode*.

        Args:
            mode: One of ``"basic"``, ``"advanced"``, or ``"scientific"``.

        Raises:
            ValueError: If *mode* is not recognised.
        """
        if mode not in _VALID_MODES:
            raise ValueError(
                f"Unknown mode '{mode}'. Valid modes: "
                f"{', '.join(sorted(_VALID_MODES))}"
            )
        self._mode = mode
        # Always provide basic operations.
        self._basic = BasicOperations(record_callback=None)
        # Advanced operations available in "advanced" and "scientific" modes.
        if mode in {"advanced", "scientific"}:
            self._advanced = AdvancedOperations(record_callback=None)
        else:
            self._advanced = None
        # Scientific operations available only in "scientific" mode.
        if mode == "scientific":
            self._scientific = ScientificOperations(record_callback=None)
        else:
            self._scientific = None

        logger.debug("CalculatorEngine mode set to %r", mode)

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
    # Public interface — mode management
    # ------------------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        """Switch the active operation sets to those defined by *mode*.

        History is **preserved** across mode switches; no previously recorded
        entries are removed.

        Args:
            mode: One of ``"basic"``, ``"advanced"``, or ``"scientific"``.

        Raises:
            ValueError: If *mode* is not recognised.
        """
        self._activate_mode(mode)

    def get_operations(self) -> dict[str, object]:
        """Return the union of all operations from active operation sets.

        Returns:
            A dict mapping operation name strings to bound callables for
            every operation available in the current mode.
        """
        ops: dict[str, object] = {}
        if self._basic is not None:
            ops.update(self._basic.get_operations())
        if self._advanced is not None:
            ops.update(self._advanced.get_operations())
        if self._scientific is not None:
            ops.update(self._scientific.get_operations())
        return ops

    # ------------------------------------------------------------------
    # Public interface — history
    # ------------------------------------------------------------------

    def get_history(self) -> list[dict]:
        """Return the full list of recorded operations.

        Returns:
            A list of dicts, each with keys ``operand1``, ``operator``,
            ``operand2``, and ``result``.  The list is in chronological
            order.  One-operand operations store ``None`` for ``operand2``.
        """
        return self._history

    # ------------------------------------------------------------------
    # Public interface — basic operations
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Public interface — advanced operations
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Public interface — scientific operations
    # ------------------------------------------------------------------

    def sin(self, x: float) -> float:
        """Return the sine of *x* (given in radians).

        Args:
            x: The angle in radians.

        Returns:
            The sine of *x*.
        """
        result = self._scientific.sin(x)
        self._record_history(x, "sin", None, result)
        return result

    def cos(self, x: float) -> float:
        """Return the cosine of *x* (given in radians).

        Args:
            x: The angle in radians.

        Returns:
            The cosine of *x*.
        """
        result = self._scientific.cos(x)
        self._record_history(x, "cos", None, result)
        return result

    def tan(self, x: float) -> float:
        """Return the tangent of *x* (given in radians).

        Args:
            x: The angle in radians.

        Returns:
            The tangent of *x*.
        """
        result = self._scientific.tan(x)
        self._record_history(x, "tan", None, result)
        return result

    def asin(self, x: float) -> float:
        """Return the arc sine of *x*, in radians.

        Args:
            x: A value in the interval [-1, 1].

        Returns:
            The arc sine of *x* in radians.

        Raises:
            ValueError: If *x* is outside [-1, 1].
        """
        result = self._scientific.asin(x)
        self._record_history(x, "asin", None, result)
        return result

    def acos(self, x: float) -> float:
        """Return the arc cosine of *x*, in radians.

        Args:
            x: A value in the interval [-1, 1].

        Returns:
            The arc cosine of *x* in radians.

        Raises:
            ValueError: If *x* is outside [-1, 1].
        """
        result = self._scientific.acos(x)
        self._record_history(x, "acos", None, result)
        return result

    def atan(self, x: float) -> float:
        """Return the arc tangent of *x*, in radians.

        Args:
            x: Any real number.

        Returns:
            The arc tangent of *x* in radians.
        """
        result = self._scientific.atan(x)
        self._record_history(x, "atan", None, result)
        return result

    def sinh(self, x: float) -> float:
        """Return the hyperbolic sine of *x*.

        Args:
            x: Any real number.

        Returns:
            The hyperbolic sine of *x*.
        """
        result = self._scientific.sinh(x)
        self._record_history(x, "sinh", None, result)
        return result

    def cosh(self, x: float) -> float:
        """Return the hyperbolic cosine of *x*.

        Args:
            x: Any real number.

        Returns:
            The hyperbolic cosine of *x*.
        """
        result = self._scientific.cosh(x)
        self._record_history(x, "cosh", None, result)
        return result

    def tanh(self, x: float) -> float:
        """Return the hyperbolic tangent of *x*.

        Args:
            x: Any real number.

        Returns:
            The hyperbolic tangent of *x*.
        """
        result = self._scientific.tanh(x)
        self._record_history(x, "tanh", None, result)
        return result

    def degrees(self, x: float) -> float:
        """Convert angle *x* from radians to degrees.

        Args:
            x: The angle in radians.

        Returns:
            The equivalent angle in degrees.
        """
        result = self._scientific.degrees(x)
        self._record_history(x, "degrees", None, result)
        return result

    def radians(self, x: float) -> float:
        """Convert angle *x* from degrees to radians.

        Args:
            x: The angle in degrees.

        Returns:
            The equivalent angle in radians.
        """
        result = self._scientific.radians(x)
        self._record_history(x, "radians", None, result)
        return result

    def exp(self, x: float) -> float:
        """Return *e* raised to the power *x* (eˣ).

        Args:
            x: The exponent.

        Returns:
            e raised to the power *x*.
        """
        result = self._scientific.exp(x)
        self._record_history(x, "exp", None, result)
        return result

    def ln(self, x: float) -> float:
        """Return the natural logarithm of *x* (ln(x)).

        Args:
            x: A strictly positive real number.

        Returns:
            The natural logarithm of *x*.

        Raises:
            ValueError: If *x* is less than or equal to 0.
        """
        result = self._scientific.ln(x)
        self._record_history(x, "ln", None, result)
        return result
