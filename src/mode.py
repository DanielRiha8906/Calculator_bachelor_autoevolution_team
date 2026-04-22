"""Calculator mode definitions and configuration.

Defines the available calculator modes (Normal and Scientific), the sets of
operations available in each mode, and a factory function for retrieving a
mode configuration by name.
"""

from dataclasses import dataclass
from enum import Enum


class CalculatorMode(Enum):
    """Enumeration of supported calculator operating modes."""

    NORMAL = "normal"
    SCIENTIFIC = "scientific"


NORMAL_MODE_OPERATIONS: list[str] = [
    "add",
    "subtract",
    "multiply",
    "divide",
    "square",
    "square_root",
]

SCIENTIFIC_MODE_OPERATIONS: list[str] = NORMAL_MODE_OPERATIONS + [
    "power",
    "cube",
    "cube_root",
    "factorial",
    "logarithm",
    "natural_logarithm",
    "sin",
    "cos",
    "tan",
    "cot",
    "asin",
    "acos",
]


@dataclass
class ModeConfig:
    """Configuration for a calculator operating mode.

    Attributes:
        mode: The :class:`CalculatorMode` value for this configuration.
        operations: The list of operation names available in this mode.
    """

    mode: CalculatorMode
    operations: list[str]


def get_mode_config(mode_name: str) -> ModeConfig | None:
    """Return a :class:`ModeConfig` for the given mode name, or ``None``.

    Performs a case-insensitive lookup against :class:`CalculatorMode` values.

    Args:
        mode_name: A string such as ``"normal"`` or ``"scientific"``.

    Returns:
        The matching :class:`ModeConfig`, or ``None`` if *mode_name* does not
        correspond to any known :class:`CalculatorMode`.

    Example:
        >>> cfg = get_mode_config("normal")
        >>> cfg.mode
        <CalculatorMode.NORMAL: 'normal'>
        >>> "add" in cfg.operations
        True
    """
    try:
        mode = CalculatorMode(mode_name.lower())
    except ValueError:
        return None

    if mode is CalculatorMode.NORMAL:
        return ModeConfig(mode=mode, operations=list(NORMAL_MODE_OPERATIONS))
    if mode is CalculatorMode.SCIENTIFIC:
        return ModeConfig(mode=mode, operations=list(SCIENTIFIC_MODE_OPERATIONS))

    # Unreachable given the current enum, but keeps exhaustiveness explicit.
    return None  # pragma: no cover
