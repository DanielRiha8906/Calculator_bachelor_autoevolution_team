"""Calculator mode abstraction layer.

This module defines the CalculatorMode base class and its two concrete
subclasses — SimpleMode and ScientificMode — which filter the operation
registry to match the selected calculator mode.

SimpleMode exposes only the NORMAL_OPERATIONS set.
ScientificMode exposes the full combined OPERATIONS set (NORMAL + SCIENTIFIC).

The GUI imports these classes to determine which operation buttons to render.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..operations import NORMAL_OPERATIONS, OPERATIONS, SCIENTIFIC_OPERATIONS


class CalculatorMode(ABC):
    """Abstract base class for calculator operating modes.

    Subclasses define which subset of the operation registry is available
    for a given mode.  The GUI uses the returned dict to build its operation
    button panel.
    """

    @abstractmethod
    def available_operations(self) -> dict[str, dict]:
        """Return the operations available in this mode.

        Returns:
            A dict mapping operation keys to their dispatch metadata dicts,
            in the same format as OPERATIONS / NORMAL_OPERATIONS.
        """


class SimpleMode(CalculatorMode):
    """Calculator mode exposing only normal (non-scientific) operations.

    Returns NORMAL_OPERATIONS, which covers the standard arithmetic and
    basic math operations (add, subtract, multiply, divide, power,
    factorial, square, cube, square_root, cube_root, log10, ln).
    """

    def available_operations(self) -> dict[str, dict]:
        """Return the normal operation registry.

        Returns:
            NORMAL_OPERATIONS dict from src/operations/normal.py.
        """
        return NORMAL_OPERATIONS


class ScientificMode(CalculatorMode):
    """Calculator mode exposing the full operation registry.

    Returns the combined OPERATIONS dict (NORMAL_OPERATIONS merged with
    SCIENTIFIC_OPERATIONS), making all registered operations available.
    """

    def available_operations(self) -> dict[str, dict]:
        """Return the full combined operation registry.

        Returns:
            OPERATIONS dict composed from NORMAL_OPERATIONS and
            SCIENTIFIC_OPERATIONS in src/operations/__init__.py.
        """
        return OPERATIONS
