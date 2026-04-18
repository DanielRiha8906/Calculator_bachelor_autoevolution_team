"""Shared base abstraction for mode-aware operation management.

This module provides the BaseMode class, which centralises the logic for
filtering the operation registry based on the current calculator mode.  Both
interactive (InputHandler) and GUI (GuiCalculator) components compose a
BaseMode instance rather than duplicating the filtering rules independently.
"""

from __future__ import annotations

from .mode import Mode
from ..operations import NORMAL_OPERATIONS, OPERATIONS


class BaseMode:
    """Shared base abstraction for mode-aware operation management.

    Encapsulates the rule for which operations are visible in each mode:
    - NORMAL mode: only operations whose keys appear in NORMAL_OPERATIONS.
    - SCIENTIFIC mode: all operations from the unified OPERATIONS registry.

    Intended to be composed (not subclassed) by any component that needs
    mode-filtered operation visibility.
    """

    def get_available_operations(self, mode: Mode) -> dict[str, dict]:
        """Return the operation dict for the given mode.

        Delegates to the appropriate private filter helper based on *mode*.

        Args:
            mode: The current calculator :class:`Mode`.

        Returns:
            A dict mapping operation keys to their registry entries for the
            given mode.  In SCIENTIFIC mode this is the full OPERATIONS dict;
            in NORMAL mode only the subset defined in NORMAL_OPERATIONS is
            returned.
        """
        if mode is Mode.SCIENTIFIC:
            return OPERATIONS
        return self._filter_operations_for_normal_mode(OPERATIONS)

    def _filter_operations_for_normal_mode(self, operations: dict) -> dict:
        """Return only the entries whose keys are in NORMAL_OPERATIONS.

        Args:
            operations: The full unified OPERATIONS registry dict to filter.

        Returns:
            A new dict containing only the key/value pairs from *operations*
            whose keys are also present in NORMAL_OPERATIONS.
        """
        return {key: operations[key] for key in NORMAL_OPERATIONS if key in operations}
