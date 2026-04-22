"""calculator.py — backward-compatible facade over CalculatorEngine.

:class:`Calculator` preserves the original public API so that all existing
callers and tests continue to work unchanged.  All computation is delegated
to :class:`~src.logic.CalculatorEngine`.
"""

from .logic import CalculatorEngine


class Calculator:
    """Facade for backward compatibility. Delegates to CalculatorEngine.

    Exposes the same public interface that was present before the
    engine was extracted into :mod:`src.logic`, ensuring that no
    existing caller or test needs to change.

    Args:
        mode: Operation mode passed through to :class:`~src.logic.CalculatorEngine`.
            Defaults to ``'basic'``.  Currently both basic and advanced
            operations are always available; the parameter is accepted for
            future extensibility.
    """

    def __init__(self, mode: str = "basic") -> None:
        """Initialise the Calculator and its underlying CalculatorEngine.

        Args:
            mode: Operation mode selector.  Defaults to ``'basic'``.
        """
        self._mode = mode
        self._engine = CalculatorEngine(mode=mode)

    # ------------------------------------------------------------------
    # Mode management
    # ------------------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        """Switch the calculator to a different operation mode at runtime.

        Re-instantiates the underlying :class:`~src.logic.CalculatorEngine`
        with the new mode.  Existing history is cleared as part of the
        re-instantiation.

        Args:
            mode: The new mode string (e.g. ``'basic'``).
        """
        self._mode = mode
        self._engine = CalculatorEngine(mode=mode)

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
