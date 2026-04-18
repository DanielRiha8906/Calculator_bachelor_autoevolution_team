"""Scientific operation module for the calculator application.

Provides unary trigonometric and transcendental functions: sin, cos, tan,
log (base-10), ln (natural log), exp, and sqrt.  Input validation and
error handling mirror the conventions of AdvancedOperations so that the
Calculator facade can delegate transparently.

All trigonometric functions expect their argument in radians.
"""

import math

from src.logger import get_logger
from src.operations.base import OperationModule


class ScientificOperations(OperationModule):
    """Implements scientific unary mathematical operations.

    All methods perform domain validation, log errors via the shared
    logger, and raise ValueError for out-of-domain inputs.  Trigonometric
    functions accept arguments in radians.
    """

    def sin(self, x: float) -> float:
        """Return the sine of x (in radians).

        Args:
            x: The angle in radians.

        Returns:
            The sine of x.
        """
        return math.sin(x)

    def cos(self, x: float) -> float:
        """Return the cosine of x (in radians).

        Args:
            x: The angle in radians.

        Returns:
            The cosine of x.
        """
        return math.cos(x)

    def tan(self, x: float) -> float:
        """Return the tangent of x (in radians).

        Args:
            x: The angle in radians.

        Returns:
            The tangent of x.
        """
        return math.tan(x)

    def log(self, x: float) -> float:
        """Return the base-10 logarithm of x.

        Args:
            x: A strictly positive number.

        Returns:
            The base-10 logarithm of x.

        Raises:
            ValueError: If x is zero or negative.
        """
        logger = get_logger(__name__)
        if x <= 0:
            logger.error(f"log({x}) failed: non-positive number")
            raise ValueError(f"log requires a positive number, got {x}")
        return math.log10(x)

    def ln(self, x: float) -> float:
        """Return the natural (base-e) logarithm of x.

        Args:
            x: A strictly positive number.

        Returns:
            The natural logarithm of x.

        Raises:
            ValueError: If x is zero or negative.
        """
        logger = get_logger(__name__)
        if x <= 0:
            logger.error(f"ln({x}) failed: non-positive number")
            raise ValueError(f"ln requires a positive number, got {x}")
        return math.log(x)

    def exp(self, x: float) -> float:
        """Return e raised to the power of x.

        Args:
            x: The exponent.

        Returns:
            e ** x.
        """
        return math.exp(x)

    def sqrt(self, x: float) -> float:
        """Return the square root of x.

        Args:
            x: A non-negative number.

        Returns:
            The square root of x.

        Raises:
            ValueError: If x is negative.
        """
        logger = get_logger(__name__)
        if x < 0:
            logger.error(f"sqrt({x}) failed: negative number")
            raise ValueError(f"sqrt requires a non-negative number, got {x}")
        return math.sqrt(x)
