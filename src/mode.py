"""Mode management for the calculator system.

Defines the calculator's operating modes and the set of operations available
in each mode.  The ``Mode`` enum is the single source of truth for which
operations are exposed to the user in interactive sessions.

Architecture note
-----------------
This module is intentionally dependency-free within the ``src`` package: it
imports nothing from other ``src`` modules, which prevents circular imports.
Both :mod:`src.input_loop` and :mod:`src.validation` import from here.

Modes
-----
NORMAL
    Basic four-operation arithmetic: add, subtract, multiply, divide.
SCIENTIFIC
    All supported operations, including advanced maths (power, factorial,
    roots, logarithms).
"""

from __future__ import annotations

from enum import Enum


class Mode(Enum):
    """Calculator operating mode.

    Attributes:
        NORMAL: Basic arithmetic mode (four operations only).
        SCIENTIFIC: Full scientific mode (all operations).
    """

    NORMAL = "normal"
    SCIENTIFIC = "scientific"


# Operations available in NORMAL mode.
_NORMAL_OPERATIONS: frozenset[str] = frozenset({
    "add",
    "subtract",
    "multiply",
    "divide",
})

# Operations available in SCIENTIFIC mode (superset of NORMAL).
_SCIENTIFIC_OPERATIONS: frozenset[str] = frozenset({
    "add",
    "subtract",
    "multiply",
    "divide",
    "power",
    "factorial",
    "square",
    "cube",
    "square_root",
    "cube_root",
    "log",
    "ln",
})


def get_normal_operations() -> frozenset[str]:
    """Return the frozenset of operation keys available in NORMAL mode.

    Returns:
        A :class:`frozenset` of operation key strings (add, subtract,
        multiply, divide).
    """
    return _NORMAL_OPERATIONS


def get_scientific_operations() -> frozenset[str]:
    """Return the frozenset of operation keys available in SCIENTIFIC mode.

    Returns:
        A :class:`frozenset` of all supported operation key strings.
    """
    return _SCIENTIFIC_OPERATIONS


def get_operations_for_mode(mode: Mode) -> frozenset[str]:
    """Return the frozenset of operation keys available for *mode*.

    Args:
        mode: A :class:`Mode` enum value.

    Returns:
        A :class:`frozenset` of operation key strings available in the
        given mode.

    Raises:
        ValueError: If *mode* is not a recognised :class:`Mode` value.
    """
    if mode is Mode.NORMAL:
        return _NORMAL_OPERATIONS
    if mode is Mode.SCIENTIFIC:
        return _SCIENTIFIC_OPERATIONS
    raise ValueError(f"Unknown mode: {mode!r}")
