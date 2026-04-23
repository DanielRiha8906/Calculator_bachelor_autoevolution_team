"""OO base abstraction for calculator modes.

Provides an abstract interface for querying mode names, available operations,
and per-operation arity without coupling GUI code to the internals of
:mod:`src.mode`.
"""

from abc import ABC, abstractmethod

from ..mode import NORMAL_MODE_OPERATIONS, SCIENTIFIC_MODE_OPERATIONS


# Operations that take a single operand (unary).  All others are binary.
_UNARY_OPERATIONS: frozenset[str] = frozenset(
    [
        "square",
        "square_root",
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
)


class BaseCalculatorMode(ABC):
    """Abstract base class defining the interface for a calculator mode.

    Concrete subclasses must implement :meth:`get_name` and
    :meth:`get_operations`.  :meth:`get_operation_arity` is provided as a
    concrete method based on a fixed unary/binary classification table.
    """

    @abstractmethod
    def get_name(self) -> str:
        """Return the canonical string name for this mode.

        Returns:
            A lowercase mode name (e.g. ``"normal"`` or ``"scientific"``).
        """

    @abstractmethod
    def get_operations(self) -> list[str]:
        """Return the ordered list of operation names available in this mode.

        Returns:
            A list of operation name strings.
        """

    def get_operation_arity(self, op_name: str) -> int:
        """Return the arity of *op_name* within this mode.

        Uses a fixed classification table: operations in :data:`_UNARY_OPERATIONS`
        return ``1``; all others return ``2``.

        Args:
            op_name: The canonical operation name to look up.

        Returns:
            ``1`` for unary operations, ``2`` for binary operations.
        """
        return 1 if op_name in _UNARY_OPERATIONS else 2


class NormalMode(BaseCalculatorMode):
    """Encapsulates the Normal calculator mode operations.

    Delegates the operation list to :data:`src.mode.NORMAL_MODE_OPERATIONS`
    to avoid duplication.
    """

    def get_name(self) -> str:
        """Return ``"normal"``."""
        return "normal"

    def get_operations(self) -> list[str]:
        """Return the Normal mode operation list.

        Returns:
            A copy of :data:`src.mode.NORMAL_MODE_OPERATIONS`.
        """
        return list(NORMAL_MODE_OPERATIONS)


class ScientificMode(BaseCalculatorMode):
    """Encapsulates the Scientific calculator mode operations.

    Delegates the operation list to :data:`src.mode.SCIENTIFIC_MODE_OPERATIONS`
    to avoid duplication.
    """

    def get_name(self) -> str:
        """Return ``"scientific"``."""
        return "scientific"

    def get_operations(self) -> list[str]:
        """Return the Scientific mode operation list.

        Returns:
            A copy of :data:`src.mode.SCIENTIFIC_MODE_OPERATIONS`.
        """
        return list(SCIENTIFIC_MODE_OPERATIONS)


def get_mode_instance(mode_name: str) -> BaseCalculatorMode:
    """Return a :class:`BaseCalculatorMode` instance for *mode_name*.

    Performs a case-insensitive lookup.

    Args:
        mode_name: A string such as ``"normal"`` or ``"scientific"``.

    Returns:
        A concrete :class:`BaseCalculatorMode` instance.

    Raises:
        ValueError: If *mode_name* does not correspond to a known mode.

    Example:
        >>> mode = get_mode_instance("normal")
        >>> mode.get_name()
        'normal'
        >>> "add" in mode.get_operations()
        True
    """
    _registry: dict[str, BaseCalculatorMode] = {
        "normal": NormalMode(),
        "scientific": ScientificMode(),
    }
    key = mode_name.lower()
    instance = _registry.get(key)
    if instance is None:
        raise ValueError(f"Unknown calculator mode: {mode_name!r}")
    return instance
