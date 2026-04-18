import math


class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        return a / b

    def factorial(self, n: int) -> int:
        """Return the factorial of n.

        Args:
            n: A non-negative integer whose factorial is to be computed.

        Returns:
            The factorial of n as an integer.

        Raises:
            TypeError: If n is a boolean or not an integer.
            ValueError: If n is a negative integer.
        """
        if isinstance(n, bool):
            raise TypeError(
                f"factorial() does not accept boolean values, got {n!r}"
            )
        if not isinstance(n, int):
            raise TypeError(
                f"factorial() only accepts non-negative integers, got {type(n).__name__!r}"
            )
        if n < 0:
            raise ValueError(
                f"factorial() is not defined for negative integers, got {n!r}"
            )
        return math.factorial(n)

    def square(self, x: float) -> float:
        """Return x raised to the power 2.

        Args:
            x: The number to square.

        Returns:
            x raised to the power 2.
        """
        return x ** 2

    def cube(self, x: float) -> float:
        """Return x raised to the power 3.

        Args:
            x: The number to cube.

        Returns:
            x raised to the power 3.
        """
        return x ** 3

    def square_root(self, x: float) -> float:
        """Return the square root of x.

        Args:
            x: The number whose square root is to be computed.

        Returns:
            The square root of x.

        Raises:
            ValueError: If x is negative.
        """
        if x < 0:
            raise ValueError(
                f"square_root() is not defined for negative numbers, got {x!r}"
            )
        return math.sqrt(x)

    def cube_root(self, x: float) -> float:
        """Return the cube root of x.

        Args:
            x: The number whose cube root is to be computed.

        Returns:
            The cube root of x.
        """
        return math.cbrt(x)

    def log10(self, x: float) -> float:
        """Return the base-10 logarithm of x.

        Args:
            x: The number whose base-10 logarithm is to be computed.

        Returns:
            The base-10 logarithm of x.

        Raises:
            ValueError: If x is less than or equal to 0.
        """
        if x <= 0:
            raise ValueError(
                f"log10() is not defined for x <= 0, got {x!r}"
            )
        return math.log10(x)

    def ln(self, x: float) -> float:
        """Return the natural logarithm of x.

        Args:
            x: The number whose natural logarithm is to be computed.

        Returns:
            The natural logarithm of x.

        Raises:
            ValueError: If x is less than or equal to 0.
        """
        if x <= 0:
            raise ValueError(
                f"ln() is not defined for x <= 0, got {x!r}"
            )
        return math.log(x)

    def power(self, x: float, y: float) -> float:
        """Return x raised to the power y.

        Args:
            x: The base.
            y: The exponent.

        Returns:
            x raised to the power y.
        """
        return x ** y

    # ------------------------------------------------------------------
    # Trigonometric methods
    # ------------------------------------------------------------------

    def sin(self, x: float) -> float:
        """Return the sine of x (x in radians).

        Args:
            x: Angle in radians.

        Returns:
            Sine of x.
        """
        return math.sin(x)

    def cos(self, x: float) -> float:
        """Return the cosine of x (x in radians).

        Args:
            x: Angle in radians.

        Returns:
            Cosine of x.
        """
        return math.cos(x)

    def tan(self, x: float) -> float:
        """Return the tangent of x (x in radians).

        Args:
            x: Angle in radians.

        Returns:
            Tangent of x.
        """
        return math.tan(x)

    def asin(self, x: float) -> float:
        """Return the arcsine of x in radians.

        Args:
            x: Value whose arcsine is to be computed. Must be in [-1, 1].

        Returns:
            Arcsine of x in radians.

        Raises:
            ValueError: If x is outside the domain [-1, 1].
        """
        if x < -1 or x > 1:
            raise ValueError(
                f"asin() is not defined for x outside [-1, 1], got {x!r}"
            )
        return math.asin(x)

    def acos(self, x: float) -> float:
        """Return the arccosine of x in radians.

        Args:
            x: Value whose arccosine is to be computed. Must be in [-1, 1].

        Returns:
            Arccosine of x in radians.

        Raises:
            ValueError: If x is outside the domain [-1, 1].
        """
        if x < -1 or x > 1:
            raise ValueError(
                f"acos() is not defined for x outside [-1, 1], got {x!r}"
            )
        return math.acos(x)

    def atan(self, x: float) -> float:
        """Return the arctangent of x in radians.

        Args:
            x: Value whose arctangent is to be computed.

        Returns:
            Arctangent of x in radians.
        """
        return math.atan(x)

    # ------------------------------------------------------------------
    # Mathematical constants
    # ------------------------------------------------------------------

    def get_pi(self) -> float:
        """Return the mathematical constant pi.

        Returns:
            math.pi (~3.141592653589793).
        """
        return math.pi

    def get_e(self) -> float:
        """Return the mathematical constant e (Euler's number).

        Returns:
            math.e (~2.718281828459045).
        """
        return math.e
