"""Menu rendering for the Calculator application.

This module contains the canonical implementation of the operation menu
display.  It has no dependency on session state, input collection, or
calculation logic.
"""


def display_menu(registry: dict) -> None:
    """Print the list of available operations to stdout.

    Args:
        registry: The operation registry returned by
            :func:`~src.core.operations.get_operation_registry`.

    Returns:
        None
    """
    print("\nAvailable operations:")
    for index, name in enumerate(registry, start=1):
        _method, arity = registry[name]
        operand_hint = f"({arity} operand{'s' if arity != 1 else ''})"
        print(f"  {index:2}. {name} {operand_hint}")
    print("   h. View history")
    print("   q. quit")
