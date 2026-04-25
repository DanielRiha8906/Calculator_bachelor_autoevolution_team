"""Calculator mode definitions for the GUI layer.

Provides an abstract base class ``CalculatorMode`` and two concrete
implementations: ``SimpleMode`` (normal, 6 operations) and
``ScientificMode`` (scientific, all 12 legacy operations).
"""

from abc import ABC, abstractmethod
from typing import List

from ..core.operations import OperationMode


class CalculatorMode(ABC):
    """Abstract base for calculator display modes.

    Each mode controls which operations are exposed to the user.
    Subclasses must implement :meth:`get_operations`.
    """

    @abstractmethod
    def get_operations(self, registry) -> List[str]:
        """Return the list of operation names available in this mode.

        Args:
            registry: An ``OperationRegistry`` instance used to look up
                available operations.

        Returns:
            A list of operation name strings.
        """


class SimpleMode(CalculatorMode):
    """Normal (simple) mode — exposes only the 6 basic operations.

    The 6 operations are: add, subtract, multiply, divide, square, sqrt.
    These correspond to ``OperationMode.NORMAL`` in the registry metadata.
    """

    def get_operations(self, registry) -> List[str]:
        """Return the 6 normal-mode operation names from the registry.

        Args:
            registry: An ``OperationRegistry`` instance.

        Returns:
            A sorted list of 6 operation name strings.
        """
        return registry.get_operations_by_mode(OperationMode.NORMAL)


class ScientificMode(CalculatorMode):
    """Scientific mode — exposes the 12 core (legacy) operations.

    Returns the same 12 operations as ``registry.get_operations()``:
    add, subtract, multiply, divide, square, sqrt, power, factorial,
    cube, cbrt, ln, log10.
    """

    def get_operations(self, registry) -> List[str]:
        """Return the 12 legacy operation names from the registry.

        Args:
            registry: An ``OperationRegistry`` instance.

        Returns:
            A sorted list of 12 operation name strings.
        """
        return registry.get_operations()
