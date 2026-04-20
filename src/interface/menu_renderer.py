"""Menu rendering for the Calculator application.

This module contains the canonical implementation of the operation menu
display.  It has no dependency on session state, input collection, or
calculation logic.
"""


def display_menu(registry: dict, current_mode: str = "normal") -> None:
    """Print the list of available operations to stdout.

    Displays the current calculator mode at the top of the menu followed by
    the numbered list of operations available in that mode.  A mode-switch
    option ``m`` and a quit option ``q`` are always appended at the bottom.

    Args:
        registry: The operation registry dict mapping operation names to
            ``(method, arity)`` 2-tuples, as returned by
            :func:`~src.core.operations.get_operation_registry` or the
            mode-specific getters on
            :class:`~src.core.operations_manager.OperationRegistry`.
        current_mode: The active calculator mode.  Accepts ``"normal"`` or
            ``"scientific"`` (case-insensitive).  Defaults to ``"normal"``.

    Returns:
        None
    """
    mode_label = "Normal" if current_mode.lower() == "normal" else "Scientific"
    print(f"\nCurrent Mode: {mode_label}")
    print("Available operations:")
    for index, name in enumerate(registry, start=1):
        _method, arity = registry[name]
        operand_hint = f"({arity} operand{'s' if arity != 1 else ''})"
        print(f"  {index:2}. {name} {operand_hint}")
    print("   h. View history")
    print("   m. Switch mode")
    print("   q. quit")
