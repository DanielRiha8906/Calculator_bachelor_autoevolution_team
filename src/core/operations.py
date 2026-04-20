"""Centralized operation registry for the Calculator application.

Defines the complete catalog of supported operations, their metadata, and
dispatch logic.  Both the CLI and REPL interaction layers delegate to this
module for operation lookup, arity validation, and Calculator invocation.

Special-case handling for the two-argument ``logarithm`` (log(x, base)) lives
here so that neither the CLI nor the REPL need to implement it independently.
"""

import math
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Operation:
    """Metadata for a single calculator operation.

    Attributes:
        name: The canonical method name on the Calculator (e.g. ``"add"``).
        arity: Number of operands the operation requires (1 or 2).
        display_name: Human-readable label shown in menus (e.g. ``"Addition"``).
        aliases: Additional input tokens that resolve to this operation
            (e.g. ``["+"]`` for ``"add"``).
        mode: Which calculator mode exposes this operation.  One of
            ``"normal"``, ``"scientific"``, or ``"both"`` (default).  Operations
            with ``mode="both"`` are visible in every mode; ``"scientific"``
            operations are only visible when scientific mode is active.
    """

    name: str
    arity: int
    display_name: str
    aliases: tuple[str, ...] = field(default_factory=tuple)
    mode: str = "both"


# The canonical ordered list of operations.  Order determines the REPL menu.
_CATALOG: list[Operation] = [
    Operation("add",               2, "Addition",              ("+",),    "both"),
    Operation("subtract",          2, "Subtraction",           ("-",),    "both"),
    Operation("multiply",          2, "Multiplication",        ("*",),    "both"),
    Operation("divide",            2, "Division",              ("/",),    "both"),
    Operation("power",             2, "Power",                 ("^",),    "both"),
    Operation("logarithm",         2, "Logarithm (base)",      ("log",),  "both"),
    Operation("factorial",         1, "Factorial",             (),        "both"),
    Operation("square",            1, "Square",                (),        "both"),
    Operation("cube",              1, "Cube",                  (),        "both"),
    Operation("square_root",       1, "Square Root",           ("sqrt",), "both"),
    Operation("cube_root",         1, "Cube Root",             ("cbrt",), "both"),
    Operation("natural_logarithm", 1, "Natural Logarithm",     ("ln",),   "both"),
    Operation("sin",               1, "Sine",                  (),        "scientific"),
    Operation("cos",               1, "Cosine",                (),        "scientific"),
    Operation("tan",               1, "Tangent",               (),        "scientific"),
]


class OperationRegistry:
    """Manage the operation catalog and dispatch operations to a Calculator.

    The registry is the single authoritative source for:
    - which operations are supported (names, aliases, arity, display names),
    - arity lookup for input validation,
    - dispatching a resolved operation and its operands to the injected
      Calculator instance.

    The ``logarithm`` operation is treated as a two-argument variant —
    ``log(x, base)`` via ``math.log`` — because ``Calculator.logarithm``
    only accepts one argument (base-10).  This special case is isolated here
    so that neither ``CLIHandler`` nor ``REPLInterface`` needs to know about it.

    Mode filtering: the registry keeps an internal ``_current_mode`` (default
    ``"normal"``).  Methods that return or evaluate operations respect the
    current mode: an operation is visible/available when its ``mode`` field is
    ``"both"`` or equal to the current mode.

    Args:
        calculator: A Calculator instance whose methods will be called for
            non-special-case operations.
    """

    def __init__(self, calculator: Any) -> None:
        self.calculator = calculator
        # Active mode for filtering — kept in sync with CalculatorContext.
        self._current_mode: str = "normal"
        # Ordered list of canonical Operation objects (preserves menu order).
        self._operations: list[Operation] = list(_CATALOG)
        # Flat lookup: every accepted token (name + aliases) -> Operation.
        self._lookup: dict[str, Operation] = {}
        for op in self._operations:
            self._lookup[op.name] = op
            for alias in op.aliases:
                self._lookup[alias] = op

    def set_mode(self, mode: str) -> None:
        """Set the active mode used to filter operations.

        Args:
            mode: The desired mode.  Must be ``"normal"`` or ``"scientific"``.

        Raises:
            ValueError: If *mode* is not ``"normal"`` or ``"scientific"``.
        """
        _VALID_REGISTRY_MODES: frozenset[str] = frozenset({"normal", "scientific"})
        if mode not in _VALID_REGISTRY_MODES:
            raise ValueError(
                f"Invalid mode {mode!r}. Valid modes are: "
                + ", ".join(sorted(_VALID_REGISTRY_MODES))
            )
        self._current_mode = mode

    # ------------------------------------------------------------------
    # Metadata access
    # ------------------------------------------------------------------

    def get_operations(self) -> list[Operation]:
        """Return operations visible in the current mode, in catalog order.

        An operation is included when its ``mode`` field is ``"both"`` or
        matches the current mode set via :meth:`set_mode`.

        Returns:
            A filtered list of :class:`Operation` instances in catalog order
            (which determines REPL menu numbering).
        """
        return [
            op for op in self._operations
            if op.mode == "both" or op.mode == self._current_mode
        ]

    def get_operation(self, token: str) -> Operation | None:
        """Return the :class:`Operation` for *token*, or ``None`` if unknown.

        Args:
            token: An operation name or alias (e.g. ``"add"``, ``"+"``,
                ``"sqrt"``).

        Returns:
            The matching :class:`Operation`, or ``None`` when *token* is not
            recognised.
        """
        return self._lookup.get(token)

    def resolve(self, token: str) -> str:
        """Return the canonical operation name for *token*.

        Args:
            token: An operation name or alias.

        Returns:
            The canonical ``name`` attribute of the matching operation.

        Raises:
            ValueError: If *token* is not a recognised operation or alias, or
                if the operation is not compatible with the current mode.
        """
        op = self._lookup.get(token)
        if op is None:
            raise ValueError(f"Unknown operation: {token!r}")
        if op.mode != "both" and op.mode != self._current_mode:
            raise ValueError(
                f"Operation {token!r} is not available in {self._current_mode!r} mode"
            )
        return op.name

    def arity(self, token: str) -> int:
        """Return the arity of the operation identified by *token*.

        Args:
            token: An operation name or alias.

        Returns:
            1 for unary operations, 2 for binary operations.

        Raises:
            ValueError: If *token* is not a recognised operation or alias, or
                if the operation is not compatible with the current mode.
        """
        op = self._lookup.get(token)
        if op is None:
            raise ValueError(f"Unknown operation: {token!r}")
        if op.mode != "both" and op.mode != self._current_mode:
            raise ValueError(
                f"Operation {token!r} is not available in {self._current_mode!r} mode"
            )
        return op.arity

    def get_operation_mapping(self) -> dict[str, str]:
        """Return a flat mapping from every accepted token to its canonical name.

        Only tokens belonging to operations compatible with the current mode are
        included (``mode="both"`` or ``mode == current_mode``).

        Useful for components that still need a simple token -> method_name
        dictionary (e.g. the CLI argument parser).

        Returns:
            A dict where keys are all accepted tokens (names and aliases) for
            mode-compatible operations and values are the corresponding
            canonical operation names.
        """
        return {
            token: op.name
            for token, op in self._lookup.items()
            if op.mode == "both" or op.mode == self._current_mode
        }

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------

    def dispatch(self, operation: str, operands: list[float]) -> float:
        """Execute *operation* with *operands* and return the numeric result.

        The ``logarithm`` operation is handled as a two-argument variant:
        ``math.log(x, base)`` with validation of both arguments.  All other
        operations are forwarded to the injected Calculator via ``getattr``.

        Args:
            operation: The canonical operation name (as returned by
                :meth:`resolve`).
            operands: The list of operand values.  Length must match the
                operation's arity.

        Returns:
            The numeric result of the operation.

        Raises:
            ValueError: If operand values violate domain constraints (e.g.
                non-positive logarithm argument or invalid base).
            ZeroDivisionError: Propagated from the Calculator.
            TypeError: Propagated from the Calculator (e.g. factorial of a
                non-integer float).
            OverflowError: Propagated from math operations.
        """
        if operation == "logarithm":
            x, base = operands
            if base <= 0 or base == 1:
                raise ValueError(
                    "logarithm base must be positive and not equal to 1"
                )
            if x <= 0:
                raise ValueError(
                    "logarithm() not defined for non-positive values"
                )
            return math.log(x, base)

        method = getattr(self.calculator, operation)
        return method(*operands)
