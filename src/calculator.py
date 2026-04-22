import math

from . import error_logger


class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        """Divide a by b.

        Args:
            a: The dividend.
            b: The divisor.

        Returns:
            The result of a / b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        try:
            return a / b
        except ZeroDivisionError as exc:
            error_logger.log_calculation_error("divide", [a, b], str(exc))
            raise

    def factorial(self, n: int) -> int:
        """
        Compute the factorial of n (n!).

        Args:
            n: A non-negative integer.

        Returns:
            The factorial of n.

        Raises:
            ValueError: If n is negative or not an integer.
        """
        if not isinstance(n, int) or isinstance(n, bool):
            _msg = "Factorial is only defined for non-negative integers"
            error_logger.log_calculation_error("factorial", [n], _msg)
            raise ValueError(_msg)
        if n < 0:
            _msg = "Factorial is only defined for non-negative integers"
            error_logger.log_calculation_error("factorial", [n], _msg)
            raise ValueError(_msg)
        return math.factorial(n)

    def square(self, x: float) -> float:
        """
        Compute the square of x (x^2).

        Args:
            x: A real number.

        Returns:
            x raised to the power of 2.
        """
        return x ** 2

    def cube(self, x: float) -> float:
        """
        Compute the cube of x (x^3).

        Args:
            x: A real number.

        Returns:
            x raised to the power of 3.
        """
        return x ** 3

    def square_root(self, x: float) -> float:
        """
        Compute the square root of x.

        Args:
            x: A non-negative real number.

        Returns:
            The principal (non-negative) square root of x.

        Raises:
            ValueError: If x is negative, as the square root of a negative
                number is not defined in the real numbers.
        """
        if x < 0:
            _msg = "Square root is not defined for negative numbers"
            error_logger.log_calculation_error("square_root", [x], _msg)
            raise ValueError(_msg)
        return math.sqrt(x)

    def cube_root(self, x: float) -> float:
        """
        Compute the real cube root of x.

        The result preserves the sign of x, so cube_root(-8) returns -2.
        This differs from x ** (1/3) which produces a complex result for
        negative inputs in Python.

        Args:
            x: A real number (positive, negative, or zero).

        Returns:
            The real cube root of x with the same sign as x.
        """
        return math.copysign(abs(x) ** (1 / 3), x)

    def power(self, x: float, y: float) -> float:
        """
        Compute x raised to the power of y (x^y).

        Args:
            x: The base, a real number.
            y: The exponent, a real number (including floats).

        Returns:
            x raised to the power y.

        Raises:
            ValueError: If x is 0 and y is negative, as 0^(-n) is undefined
                (division by zero).
        """
        if x == 0 and y < 0:
            _msg = "0 raised to a negative power is undefined"
            error_logger.log_calculation_error("power", [x, y], _msg)
            raise ValueError(_msg)
        return x ** y

    def log(self, x: float) -> float:
        """
        Compute the base-10 logarithm of x (log10(x)).

        Args:
            x: A positive real number.

        Returns:
            The base-10 logarithm of x.

        Raises:
            ValueError: If x is less than or equal to 0, as the logarithm is
                only defined for strictly positive numbers.
        """
        if x <= 0:
            _msg = "Logarithm is only defined for positive numbers"
            error_logger.log_calculation_error("log", [x], _msg)
            raise ValueError(_msg)
        return math.log10(x)

    def ln(self, x: float) -> float:
        """
        Compute the natural logarithm of x (log base e).

        Args:
            x: A positive real number.

        Returns:
            The natural logarithm (base e) of x.

        Raises:
            ValueError: If x is less than or equal to 0, as the natural
                logarithm is only defined for strictly positive numbers.
        """
        if x <= 0:
            _msg = "Natural logarithm is only defined for positive numbers"
            error_logger.log_calculation_error("ln", [x], _msg)
            raise ValueError(_msg)
        return math.log(x)

