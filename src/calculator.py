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

    def square(self, a):
        """Return a squared (a ** 2).

        Works for all real numbers.

        Args:
            a: The number to square.

        Returns:
            The square of a.
        """
        return a ** 2

    def cube(self, a):
        """Return a cubed (a ** 3).

        Works for all real numbers.

        Args:
            a: The number to cube.

        Returns:
            The cube of a.
        """
        return a ** 3

    def square_root(self, a):
        """Return the square root of a.

        Args:
            a: The number to take the square root of. Must be non-negative.

        Returns:
            The square root of a.

        Raises:
            ValueError: If a is negative.
        """
        if a < 0:
            raise ValueError("Cannot take square root of a negative number.")
        return math.sqrt(a)

    def cube_root(self, a):
        """Return the cube root of a.

        Handles negative inputs by computing -(abs(a) ** (1/3)).

        Args:
            a: The number to take the cube root of.

        Returns:
            The cube root of a.
        """
        if a == 0:
            return 0.0
        if a < 0:
            return -(abs(a) ** (1 / 3))
        return a ** (1 / 3)

    def factorial(self, n):
        """Return the factorial of n.

        Args:
            n: A non-negative integer.

        Returns:
            The factorial of n.

        Raises:
            ValueError: If n is negative, not an integer, or is a boolean.
        """
        if isinstance(n, bool) or not isinstance(n, int):
            raise ValueError("Factorial is only defined for non-negative integers.")
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        return math.factorial(n)

    def power(self, base, exp):
        """Return base raised to the power of exp.

        Args:
            base: The base number.
            exp: The exponent.

        Returns:
            base ** exp.
        """
        return base ** exp

    def log(self, a):
        """Return the base-10 logarithm of a.

        Args:
            a: The number to take the logarithm of. Must be positive.

        Returns:
            The base-10 logarithm of a.

        Raises:
            ValueError: If a is less than or equal to 0.
        """
        if a <= 0:
            raise ValueError("Logarithm is only defined for positive numbers.")
        return math.log10(a)

    def ln(self, a):
        """Return the natural logarithm of a.

        Args:
            a: The number to take the natural logarithm of. Must be positive.

        Returns:
            The natural logarithm of a.

        Raises:
            ValueError: If a is less than or equal to 0.
        """
        if a <= 0:
            raise ValueError("Natural logarithm is only defined for positive numbers.")
        return math.log(a)
