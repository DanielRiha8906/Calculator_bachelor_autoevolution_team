"""Mode management for the calculator application.

Tracks whether the calculator is operating in "normal" (binary arithmetic)
mode or "scientific" (unary trigonometric/transcendental) mode.  Mode
changes are validated and logged.
"""

from src.logger import get_logger

_VALID_MODES: frozenset[str] = frozenset({"normal", "scientific"})


class ModeManager:
    """Tracks and controls the active calculator mode.

    Attributes:
        _mode: The currently active mode name ("normal" or "scientific").
    """

    def __init__(self) -> None:
        """Initialise ModeManager with the default "normal" mode."""
        self._mode: str = "normal"

    def get_mode(self) -> str:
        """Return the currently active mode name.

        Returns:
            One of "normal" or "scientific".
        """
        return self._mode

    def set_mode(self, mode_name: str) -> None:
        """Switch to the given mode.

        Args:
            mode_name: The desired mode.  Must be "normal" or "scientific".

        Raises:
            ValueError: If mode_name is not a recognised mode.
        """
        logger = get_logger(__name__)
        if mode_name not in _VALID_MODES:
            supported = ", ".join(repr(m) for m in sorted(_VALID_MODES))
            logger.error(f"set_mode({mode_name!r}) failed: unknown mode")
            raise ValueError(
                f"Unknown mode {mode_name!r}. Supported modes are: {supported}."
            )
        if mode_name != self._mode:
            logger.info(f"Mode changed from {self._mode!r} to {mode_name!r}")
            self._mode = mode_name

    def is_scientific(self) -> bool:
        """Return True when the active mode is "scientific".

        Returns:
            True if the current mode is "scientific", False otherwise.
        """
        return self._mode == "scientific"
