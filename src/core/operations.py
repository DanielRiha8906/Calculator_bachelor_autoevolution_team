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
    """

    name: str
    arity: int
    display_name: str
    aliases: tuple[str, ...] = field(default_factory=tuple)


# The canonical ordered list of operations.  Order determines the REPL menu.
_CATALOG: list[Operation] = [
    Operation("add",               2, "Addition",              ("+",)),
    Operation("subtract",          2, "Subtraction",           ("-",)),
    Operation("multiply",          2, "Multiplication",        ("*",)),
    Operation("divide",            2, "Division",              ("/",)),
    Operation("power",             2, "Power",                 ("^",)),
    Operation("logarithm",         2, "Logarithm (base)",      ("log",)),
    Operation("factorial",         1, "Factorial",             ()),
    Operation("square",            1, "Square",                ()),
    Operation("cube",              1, "Cube",                  ()),
    Operation("square_root",       1, "Square Root",           ("sqrt",)),
    Operation("cube_root",         1, "Cube Root",             ("cbrt",)),
    Operation("natural_logarithm", 1, "Natural Logarithm",     ("ln",)),
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

    Args:
        calculator: A Calculator instance whose methods will be called for
            non-special-case operations.
    """

    def __init__(self, calculator: Any) -> None:
        self.calculator = calculator
        # Ordered list of canonical Operation objects (preserves menu order).
        self._operations: list[Operation] = list(_CATALOG)
        # Flat lookup: every accepted token (name + aliases) -> Operation.
        self._lookup: dict[str, Operation] = {}
        for op in self._operations:
            self._lookup[op.name] = op
            for alias in op.aliases:
                self._lookup[alias] = op

    # ------------------------------------------------------------------
    # Metadata access
    # ------------------------------------------------------------------

    def get_operations(self) -> list[Operation]:
        """Return all operations in catalog order.

        Returns:
            A list of :class:`Operation` instances in the order they were
            registered (which determines REPL menu numbering).
        """
        return list(self._operations)

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
            ValueError: If *token* is not a recognised operation or alias.
        """
        op = self._lookup.get(token)
        if op is None:
            raise ValueError(f"Unknown operation: {token!r}")
        return op.name

    def arity(self, token: str) -> int:
        """Return the arity of the operation identified by *token*.

        Args:
            token: An operation name or alias.

        Returns:
            1 for unary operations, 2 for binary operations.

        Raises:
            ValueError: If *token* is not a recognised operation or alias.
        """
        op = self._lookup.get(token)
        if op is None:
            raise ValueError(f"Unknown operation: {token!r}")
        return op.arity

    def get_operation_mapping(self) -> dict[str, str]:
        """Return a flat mapping from every accepted token to its canonical name.

        Useful for components that still need a simple token -> method_name
        dictionary (e.g. the CLI argument parser).

        Returns:
            A dict where keys are all accepted tokens (names and aliases) and
            values are the corresponding canonical operation names.
        """
        return {token: op.name for token, op in self._lookup.items()}

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
