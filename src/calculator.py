"""calculator.py — backward-compatible facade over CalculatorEngine.

:class:`Calculator` preserves the original public API so that all existing
callers and tests continue to work unchanged.  All computation is delegated
to :class:`~src.logic.CalculatorEngine`.

Supported modes
---------------
``"basic"``
    Only the four arithmetic operations: add, subtract, multiply, divide.
``"advanced"``
    All basic operations plus: factorial, square, cube, square_root,
    cube_root, power, natural_log, log_base_10.
``"scientific"``
    All advanced operations plus: sin, cos, tan, asin, acos, atan,
    sinh, cosh, tanh, degrees, radians, exp, ln.
"""

from .logic import CalculatorEngine


class Calculator:
    """Facade for backward compatibility. Delegates to CalculatorEngine.

    Exposes the same public interface that was present before the
    engine was extracted into :mod:`src.logic`, ensuring that no
    existing caller or test needs to change.

    Supported modes are ``"basic"``, ``"advanced"``, and ``"scientific"``.
    See the module docstring for the operations available in each mode.

    Args:
        mode: Operation mode passed through to :class:`~src.logic.CalculatorEngine`.
            Defaults to ``"advanced"`` so that the full set of arithmetic and
            advanced operations is available by default.
    """

    def __init__(self, mode: str = "advanced") -> None:
        """Initialise the Calculator and its underlying CalculatorEngine.

        Args:
            mode: Operation mode selector.  One of ``"basic"``,
                ``"advanced"``, or ``"scientific"``.  Defaults to
                ``"advanced"``.
        """
        self._engine = CalculatorEngine(mode=mode)
        self._mode: str = mode

    # ------------------------------------------------------------------
    # Mode management
    # ------------------------------------------------------------------

    def get_available_modes_for_operation(self, operation: str) -> list[str]:
        """Return which modes support a given operation.

        Pass-through to :meth:`~src.logic.CalculatorEngine.get_available_modes_for_operation`.

        Args:
            operation: The operation name to look up (e.g. ``"factorial"``).

        Returns:
            A sorted list of mode name strings (e.g. ``["advanced",
            "scientific"]``).  Returns an empty list if the operation is
            not recognised in any mode.
        """
        return self._engine.get_available_modes_for_operation(operation)

    def set_mode(self, mode: str) -> None:
        """Switch the calculator to a different operation mode at runtime.

        Delegates to :meth:`~src.logic.CalculatorEngine.set_mode`.  The
        existing history is **preserved** — no previously recorded entries
        are removed.

        Args:
            mode: The new mode string.  One of ``"basic"``, ``"advanced"``,
                or ``"scientific"``.

        Raises:
            ValueError: If *mode* is not one of the recognised mode strings.
        """
        self._engine.set_mode(mode)
        self._mode = mode

    # ------------------------------------------------------------------
    # History
    # ------------------------------------------------------------------

    def get_history(self) -> list[dict]:
        """Return the full list of recorded operations.

        Returns:
            A list of dicts, each with keys ``operand1``, ``operator``,
            ``operand2``, and ``result``.  The list is in chronological
            order.  One-operand operations store ``None`` for ``operand2``.
        """
        return self._engine.get_history()

    # ------------------------------------------------------------------
    # Arithmetic
    # ------------------------------------------------------------------

    def add(self, a, b):
        return self._engine.add(a, b)

    def subtract(self, a, b):
        return self._engine.subtract(a, b)

    def multiply(self, a, b):
        return self._engine.multiply(a, b)

    def divide(self, a, b):
        return self._engine.divide(a, b)

    # ------------------------------------------------------------------
    # Advanced operations
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
        return self._engine.factorial(n)

    def square(self, x: float) -> float:
        """Return the square of x (x²).

        Args:
            x: The number to square.

        Returns:
            x multiplied by itself.
        """
        return self._engine.square(x)

    def cube(self, x: float) -> float:
        """Return the cube of x (x³).

        Args:
            x: The number to cube.

        Returns:
            x multiplied by itself twice.
        """
        return self._engine.cube(x)

    def square_root(self, x: float) -> float:
        """Return the square root of x (√x).

        Args:
            x: The number to take the square root of.

        Returns:
            The non-negative square root of x.

        Raises:
            ValueError: If x is negative.
        """
        return self._engine.square_root(x)

    def cube_root(self, x: float) -> float:
        """Return the real cube root of x (∛x).

        Supports negative inputs by preserving the sign.

        Args:
            x: The number to take the cube root of.

        Returns:
            The real cube root of x.
        """
        return self._engine.cube_root(x)

    def power(self, base: float, exponent: float) -> float:
        """Return base raised to the given exponent (base^exponent).

        Args:
            base: The base number.
            exponent: The exponent to raise the base to.

        Returns:
            base raised to the power of exponent.
        """
        return self._engine.power(base, exponent)

    def natural_log(self, x: float) -> float:
        """Return the natural logarithm of x (ln(x)).

        Args:
            x: The number to compute the natural log of.

        Returns:
            The natural logarithm of x.

        Raises:
            ValueError: If x is less than or equal to 0.
        """
        return self._engine.natural_log(x)

    def log_base_10(self, x: float) -> float:
        """Return the base-10 logarithm of x (log₁₀(x)).

        Args:
            x: The number to compute the base-10 log of.

        Returns:
            The base-10 logarithm of x.

        Raises:
            ValueError: If x is less than or equal to 0.
        """
        return self._engine.log_base_10(x)

    # ------------------------------------------------------------------
    # Scientific operations
    # ------------------------------------------------------------------

    def sin(self, x: float) -> float:
        """Return the sine of *x* (given in radians).

        Args:
            x: The angle in radians.

        Returns:
            The sine of *x*.
        """
        return self._engine.sin(x)

    def cos(self, x: float) -> float:
        """Return the cosine of *x* (given in radians).

        Args:
            x: The angle in radians.

        Returns:
            The cosine of *x*.
        """
        return self._engine.cos(x)

    def tan(self, x: float) -> float:
        """Return the tangent of *x* (given in radians).

        Args:
            x: The angle in radians.

        Returns:
            The tangent of *x*.
        """
        return self._engine.tan(x)

    def asin(self, x: float) -> float:
        """Return the arc sine of *x*, in radians.

        Args:
            x: A value in the interval [-1, 1].

        Returns:
            The arc sine of *x* in radians.

        Raises:
            ValueError: If *x* is outside [-1, 1].
        """
        return self._engine.asin(x)

    def acos(self, x: float) -> float:
        """Return the arc cosine of *x*, in radians.

        Args:
            x: A value in the interval [-1, 1].

        Returns:
            The arc cosine of *x* in radians.

        Raises:
            ValueError: If *x* is outside [-1, 1].
        """
        return self._engine.acos(x)

    def atan(self, x: float) -> float:
        """Return the arc tangent of *x*, in radians.

        Args:
            x: Any real number.

        Returns:
            The arc tangent of *x* in radians.
        """
        return self._engine.atan(x)

    def sinh(self, x: float) -> float:
        """Return the hyperbolic sine of *x*.

        Args:
            x: Any real number.

        Returns:
            The hyperbolic sine of *x*.
        """
        return self._engine.sinh(x)

    def cosh(self, x: float) -> float:
        """Return the hyperbolic cosine of *x*.

        Args:
            x: Any real number.

        Returns:
            The hyperbolic cosine of *x*.
        """
        return self._engine.cosh(x)

    def tanh(self, x: float) -> float:
        """Return the hyperbolic tangent of *x*.

        Args:
            x: Any real number.

        Returns:
            The hyperbolic tangent of *x*.
        """
        return self._engine.tanh(x)

    def degrees(self, x: float) -> float:
        """Convert angle *x* from radians to degrees.

        Args:
            x: The angle in radians.

        Returns:
            The equivalent angle in degrees.
        """
        return self._engine.degrees(x)

    def radians(self, x: float) -> float:
        """Convert angle *x* from degrees to radians.

        Args:
            x: The angle in degrees.

        Returns:
            The equivalent angle in radians.
        """
        return self._engine.radians(x)

    def exp(self, x: float) -> float:
        """Return *e* raised to the power *x* (eˣ).

        Args:
            x: The exponent.

        Returns:
            e raised to the power *x*.
        """
        return self._engine.exp(x)

    def ln(self, x: float) -> float:
        """Return the natural logarithm of *x* (ln(x)).

        Args:
            x: A strictly positive real number.

        Returns:
            The natural logarithm of *x*.

        Raises:
            ValueError: If *x* is less than or equal to 0.
        """
        return self._engine.ln(x)
