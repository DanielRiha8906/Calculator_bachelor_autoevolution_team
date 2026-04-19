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
        """Compute the factorial of a non-negative integer n.

        Args:
            n: A non-negative integer. bool values are accepted and treated
               as their integer equivalents (False -> 0, True -> 1).

        Returns:
            The factorial of n as an integer. factorial(0) and factorial(1)
            both return 1.

        Raises:
            TypeError: If n is not an int (or bool). Floats, strings, None,
                and other types are rejected.
            ValueError: If n is a negative integer.

        Examples:
            >>> calc = Calculator()
            >>> calc.factorial(0)
            1
            >>> calc.factorial(5)
            120
        """
        if not isinstance(n, int):
            raise TypeError(
                f"factorial() requires an integer argument, got {type(n).__name__!r}"
            )
        if n < 0:
            raise ValueError(
                f"factorial() is not defined for negative integers, got {n}"
            )
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def square(self, x: int | float) -> int | float:
        """Return the square of x (x²).

        Args:
            x: A numeric value (int or float).

        Returns:
            The square of x, preserving the input type for integers.

        Raises:
            TypeError: If x is not an int or float.

        Examples:
            >>> calc = Calculator()
            >>> calc.square(4)
            16
            >>> calc.square(-3.0)
            9.0
        """
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"square() requires a numeric argument, got {type(x).__name__!r}"
            )
        return x * x

    def cube(self, x: int | float) -> int | float:
        """Return the cube of x (x³).

        Args:
            x: A numeric value (int or float).

        Returns:
            The cube of x, preserving the input type for integers.

        Raises:
            TypeError: If x is not an int or float.

        Examples:
            >>> calc = Calculator()
            >>> calc.cube(3)
            27
            >>> calc.cube(-2.0)
            -8.0
        """
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"cube() requires a numeric argument, got {type(x).__name__!r}"
            )
        return x * x * x

    def square_root(self, x: int | float) -> float:
        """Return the square root of x (√x).

        Args:
            x: A non-negative numeric value (int or float).

        Returns:
            The square root of x as a float.

        Raises:
            TypeError: If x is not an int or float.
            ValueError: If x is negative.

        Examples:
            >>> calc = Calculator()
            >>> calc.square_root(9)
            3.0
            >>> calc.square_root(2.0)
            1.4142135623730951
        """
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"square_root() requires a numeric argument, got {type(x).__name__!r}"
            )
        if x < 0:
            raise ValueError(
                f"square_root() is not defined for negative numbers, got {x}"
            )
        return math.sqrt(x)

    def cube_root(self, x: int | float) -> float:
        """Return the cube root of x (∛x).

        Supports negative inputs by applying sign handling so that, for
        example, cube_root(-8) returns -2.0 instead of a complex number.

        Args:
            x: A numeric value (int or float), any sign.

        Returns:
            The real-valued cube root of x as a float.

        Raises:
            TypeError: If x is not an int or float.

        Examples:
            >>> calc = Calculator()
            >>> calc.cube_root(27)
            3.0
            >>> calc.cube_root(-8)
            -2.0
        """
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"cube_root() requires a numeric argument, got {type(x).__name__!r}"
            )
        if x < 0:
            return -(abs(x) ** (1 / 3))
        return abs(x) ** (1 / 3)

    def power(self, base: int | float, exponent: int | float) -> int | float:
        """Return base raised to exponent (base^exponent).

        Args:
            base: A numeric value (int or float).
            exponent: A numeric value (int or float).

        Returns:
            The result of base ** exponent.

        Raises:
            TypeError: If either base or exponent is not an int or float.
            ValueError: If base is negative and exponent is not an integer,
                which would produce a complex result.

        Examples:
            >>> calc = Calculator()
            >>> calc.power(2, 10)
            1024
            >>> calc.power(9.0, 0.5)
            3.0
        """
        if not isinstance(base, (int, float)):
            raise TypeError(
                f"power() requires numeric arguments, got base={type(base).__name__!r}"
            )
        if not isinstance(exponent, (int, float)):
            raise TypeError(
                f"power() requires numeric arguments, got exponent={type(exponent).__name__!r}"
            )
        if base < 0 and not isinstance(exponent, int):
            raise ValueError(
                f"power() with a negative base and non-integer exponent would produce "
                f"a complex result (base={base}, exponent={exponent})"
            )
        return base ** exponent

    def log(self, x: int | float) -> float:
        """Return the base-10 logarithm of x (log₁₀(x)).

        Args:
            x: A positive numeric value (int or float).

        Returns:
            The base-10 logarithm of x as a float.

        Raises:
            TypeError: If x is not an int or float.
            ValueError: If x is less than or equal to zero.

        Examples:
            >>> calc = Calculator()
            >>> calc.log(100)
            2.0
            >>> calc.log(1)
            0.0
        """
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"log() requires a numeric argument, got {type(x).__name__!r}"
            )
        if x <= 0:
            raise ValueError(
                f"log() is not defined for non-positive numbers, got {x}"
            )
        return math.log10(x)

    def ln(self, x: int | float) -> float:
        """Return the natural logarithm of x (ln(x)).

        Args:
            x: A positive numeric value (int or float).

        Returns:
            The natural logarithm of x as a float.

        Raises:
            TypeError: If x is not an int or float.
            ValueError: If x is less than or equal to zero.

        Examples:
            >>> calc = Calculator()
            >>> calc.ln(1)
            0.0
            >>> import math
            >>> calc.ln(math.e)
            1.0
        """
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"ln() requires a numeric argument, got {type(x).__name__!r}"
            )
        if x <= 0:
            raise ValueError(
                f"ln() is not defined for non-positive numbers, got {x}"
            )
        return math.log(x)

