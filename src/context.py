"""Calculator context module holding mode state.

Tracks the current operating mode ("normal" or "scientific") and provides
validated accessors so that interface layers and the operation registry stay
in sync.
"""

_VALID_MODES: frozenset[str] = frozenset({"normal", "scientific"})


class CalculatorContext:
    """Hold and validate the current calculator operating mode.

    The context acts as a single source of truth for mode state.  Both the
    REPL and CLI layers read from it; the REPL also writes to it when the user
    issues a mode-switch command.

    Attributes:
        current_mode: The active mode string; either ``"normal"`` or
            ``"scientific"``.  Defaults to ``"normal"`` at construction.
    """

    def __init__(self) -> None:
        self.current_mode: str = "normal"

    def set_mode(self, mode: str) -> None:
        """Set the current operating mode.

        Args:
            mode: The desired mode.  Must be ``"normal"`` or ``"scientific"``.

        Raises:
            ValueError: If *mode* is not a recognised mode string.
        """
        if mode not in _VALID_MODES:
            raise ValueError(
                f"Invalid mode {mode!r}. Valid modes are: "
                + ", ".join(sorted(_VALID_MODES))
            )
        self.current_mode = mode

    def get_mode(self) -> str:
        """Return the current operating mode.

        Returns:
            The current mode string (``"normal"`` or ``"scientific"``).
        """
        return self.current_mode

    def is_scientific_mode(self) -> bool:
        """Return True when the calculator is in scientific mode.

        Returns:
            ``True`` if the current mode is ``"scientific"``, ``False``
            otherwise.
        """
        return self.current_mode == "scientific"
