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
        """Compute the factorial of a non-negative integer.

        Args:
            n: The non-negative integer whose factorial is to be computed.
                Float values are accepted only when they represent an exact
                integer (e.g. 5.0), in which case they are treated as int.

        Returns:
            The factorial of n (n!). Returns 1 when n is 0.

        Raises:
            TypeError: If n is not an int or a float that equals an integer
                value.
            ValueError: If n is negative.
        """
        if isinstance(n, bool):
            raise TypeError(
                f"Expected a non-negative integer, got {type(n).__name__}."
            )
        if isinstance(n, float):
            if not n.is_integer():
                raise TypeError(
                    f"Float value {n} is not an integer value; "
                    "cannot compute factorial."
                )
            n = int(n)
        if not isinstance(n, int):
            raise TypeError(
                f"Expected a non-negative integer, got {type(n).__name__}."
            )
        if n < 0:
            raise ValueError(
                f"Factorial is not defined for negative numbers; got {n}."
            )
        result: int = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def square(self, x: int | float) -> int | float:
        """Compute the square of a number.

        Args:
            x: The number to square. Must be an int or float (not bool or None).

        Returns:
            x squared. Returns int if x is int, float if x is float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
        """
        if isinstance(x, bool):
            raise TypeError(
                f"Expected an int or float, got {type(x).__name__}."
            )
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Expected an int or float, got {type(x).__name__}."
            )
        return x * x

    def cube(self, x: int | float) -> int | float:
        """Compute the cube of a number.

        Args:
            x: The number to cube. Must be an int or float (not bool or None).

        Returns:
            x cubed. Returns int if x is int, float if x is float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
        """
        if isinstance(x, bool):
            raise TypeError(
                f"Expected an int or float, got {type(x).__name__}."
            )
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Expected an int or float, got {type(x).__name__}."
            )
        return x * x * x

    def square_root(self, x: int | float) -> float:
        """Compute the square root of a non-negative number.

        Args:
            x: The number whose square root is to be computed. Must be an int
                or float (not bool or None) and must be non-negative.

        Returns:
            The square root of x as a float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
            ValueError: If x is negative.
        """
        if isinstance(x, bool):
            raise TypeError(
                f"Expected a non-negative int or float, got {type(x).__name__}."
            )
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Expected a non-negative int or float, got {type(x).__name__}."
            )
        if x < 0:
            raise ValueError(
                f"Square root is not defined for negative numbers; got {x}."
            )
        return math.sqrt(x)

    def cube_root(self, x: int | float) -> float:
        """Compute the cube root of a number.

        Args:
            x: The number whose cube root is to be computed. Must be an int or
                float (not bool or None). Negative values are supported.

        Returns:
            The cube root of x as a float, preserving the sign of x.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
        """
        if isinstance(x, bool):
            raise TypeError(
                f"Expected an int or float, got {type(x).__name__}."
            )
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Expected an int or float, got {type(x).__name__}."
            )
        return math.copysign(abs(x) ** (1 / 3), x)

    def power(self, base: int | float, exponent: int | float) -> float:
        """Raise base to the power of exponent.

        Args:
            base: The base value. Must be an int or float (not bool or None).
            exponent: The exponent value. Must be an int or float (not bool
                or None).

        Returns:
            base raised to the power of exponent, as a float.

        Raises:
            TypeError: If base or exponent is a bool, None, or any non-numeric
                type.
        """
        if isinstance(base, bool):
            raise TypeError(
                f"Expected an int or float for base, got {type(base).__name__}."
            )
        if not isinstance(base, (int, float)):
            raise TypeError(
                f"Expected an int or float for base, got {type(base).__name__}."
            )
        if isinstance(exponent, bool):
            raise TypeError(
                f"Expected an int or float for exponent, got {type(exponent).__name__}."
            )
        if not isinstance(exponent, (int, float)):
            raise TypeError(
                f"Expected an int or float for exponent, got {type(exponent).__name__}."
            )
        return float(base ** exponent)

    def log10(self, x: int | float) -> float:
        """Compute the base-10 logarithm of a positive number.

        Args:
            x: The number whose base-10 logarithm is to be computed. Must be
                an int or float (not bool or None) and must be strictly positive.

        Returns:
            The base-10 logarithm of x as a float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
            ValueError: If x is less than or equal to zero.
        """
        if isinstance(x, bool):
            raise TypeError(
                f"Expected a positive int or float, got {type(x).__name__}."
            )
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Expected a positive int or float, got {type(x).__name__}."
            )
        if x <= 0:
            raise ValueError(
                f"log10 is not defined for non-positive numbers; got {x}."
            )
        return math.log10(x)

    def natural_log(self, x: int | float) -> float:
        """Compute the natural logarithm (base e) of a positive number.

        Args:
            x: The number whose natural logarithm is to be computed. Must be
                an int or float (not bool or None) and must be strictly positive.

        Returns:
            The natural logarithm of x as a float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
            ValueError: If x is less than or equal to zero.
        """
        if isinstance(x, bool):
            raise TypeError(
                f"Expected a positive int or float, got {type(x).__name__}."
            )
        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Expected a positive int or float, got {type(x).__name__}."
            )
        if x <= 0:
            raise ValueError(
                f"Natural log is not defined for non-positive numbers; got {x}."
            )
        return math.log(x)
