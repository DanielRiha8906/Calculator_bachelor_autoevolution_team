"""Mode management module for the Calculator session.

Defines the Mode enum representing the two calculator modes (NORMAL and
SCIENTIFIC), and provides a helper function for parsing user-entered mode
switch commands.
"""

from __future__ import annotations

from enum import Enum


class Mode(Enum):
    """Calculator operation mode.

    Members:
        NORMAL: Exposes only basic arithmetic and standard operations.
        SCIENTIFIC: Exposes all operations, including trigonometry and
            mathematical constants.
    """

    NORMAL = "normal"
    SCIENTIFIC = "scientific"


def parse_mode_command(input_str: str) -> Mode | None:
    """Parse a mode-switch command from user input.

    Recognises commands of the form ``"mode <name>"`` (case-insensitive).
    Returns the corresponding :class:`Mode` member when the command is valid,
    or ``None`` when the input is not a mode command or contains an unknown
    mode name.

    Args:
        input_str: Raw user input string (already stripped and lowercased by
            the caller, but this function tolerates either case).

    Returns:
        The matching :class:`Mode` enum member, or ``None`` if the input is
        not a recognised mode command.

    Examples:
        >>> parse_mode_command("mode scientific")
        <Mode.SCIENTIFIC: 'scientific'>
        >>> parse_mode_command("mode normal")
        <Mode.NORMAL: 'normal'>
        >>> parse_mode_command("mode invalid")
        >>> parse_mode_command("add")
    """
    normalised = input_str.strip().lower()
    parts = normalised.split()
    if len(parts) != 2 or parts[0] != "mode":
        return None
    mode_name = parts[1]
    try:
        return Mode(mode_name)
    except ValueError:
        return None
