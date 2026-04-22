"""Manages the calculator's operational mode (Normal or Scientific).

This module provides the ``CalculatorMode`` enum and the ``ModeManager``
class that controls which operations are available to the user at runtime.
"""

from enum import Enum


class CalculatorMode(Enum):
    """Enumeration of supported calculator modes."""

    NORMAL = "normal"
    SCIENTIFIC = "scientific"


class ModeManager:
    """Controls the active calculator mode and operation availability.

    The mode determines which operations are presented to the user.
    In NORMAL mode, operations tagged as scientific are hidden.
    In SCIENTIFIC mode, all registered operations are visible.

    Example::

        manager = ModeManager()
        manager.get_current_mode()          # CalculatorMode.NORMAL
        manager.switch_mode()
        manager.get_current_mode()          # CalculatorMode.SCIENTIFIC
        manager.is_operation_available("sin", {"sin", "cos"})  # True
    """

    def __init__(self) -> None:
        """Initialise the manager in NORMAL mode."""
        self._current_mode: CalculatorMode = CalculatorMode.NORMAL

    def get_current_mode(self) -> CalculatorMode:
        """Return the currently active mode.

        Returns:
            The current :class:`CalculatorMode` value.
        """
        return self._current_mode

    def switch_mode(self) -> None:
        """Toggle between NORMAL and SCIENTIFIC modes."""
        if self._current_mode is CalculatorMode.NORMAL:
            self._current_mode = CalculatorMode.SCIENTIFIC
        else:
            self._current_mode = CalculatorMode.NORMAL

    def set_mode(self, mode: CalculatorMode) -> None:
        """Explicitly set the active mode.

        Args:
            mode: The :class:`CalculatorMode` to activate.

        Raises:
            TypeError: If ``mode`` is not a :class:`CalculatorMode` instance.
        """
        if not isinstance(mode, CalculatorMode):
            raise TypeError(
                f"'mode' must be a CalculatorMode instance, got {type(mode).__name__!r}."
            )
        self._current_mode = mode

    def get_mode_display_name(self) -> str:
        """Return a human-readable label for the current mode.

        Returns:
            ``"Normal"`` or ``"Scientific"``.
        """
        return "Normal" if self._current_mode is CalculatorMode.NORMAL else "Scientific"

    def is_operation_available(
        self, operation_name: str, scientific_operations: set
    ) -> bool:
        """Determine whether an operation is available in the current mode.

        In NORMAL mode, any operation whose name is in ``scientific_operations``
        is hidden (returns ``False``).  In SCIENTIFIC mode every operation is
        available regardless of its classification.

        Args:
            operation_name: The string key identifying the operation.
            scientific_operations: The set of operation keys tagged as
                scientific by the registry.

        Returns:
            ``True`` if the operation should be offered to the user,
            ``False`` otherwise.
        """
        if self._current_mode is CalculatorMode.SCIENTIFIC:
            return True
        return operation_name not in scientific_operations
