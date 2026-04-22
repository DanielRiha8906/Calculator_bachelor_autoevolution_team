"""Pure output formatting functions for the Calculator CLI.

All functions in this module take simple data types and return strings.
No I/O is performed and no imports from cli, session, or calculator are made.
"""


def format_menu_header(operations: list[str], mode: str | None = None) -> str:
    """Format the menu header and numbered operation list.

    Args:
        operations: The list of available operation name strings.
        mode: Optional mode name (e.g. ``"normal"`` or ``"scientific"``).
            When provided, the header line includes the mode name so the user
            can see which mode is active.  Passing ``None`` (the default)
            reproduces the original behaviour for backward compatibility.

    Returns:
        A multi-line string containing the header and one numbered entry
        per operation.

    Example:
        >>> print(format_menu_header(["add", "subtract"]))
        <BLANKLINE>
        Available operations:
          1. add
          2. subtract
        >>> print(format_menu_header(["add"], mode="normal"))
        <BLANKLINE>
        Available operations (Normal mode):
          1. add
    """
    if mode is not None:
        header = f"\nAvailable operations ({mode.capitalize()} mode):"
    else:
        header = "\nAvailable operations:"
    lines = [header]
    for idx, op_name in enumerate(operations, start=1):
        lines.append(f"  {idx}. {op_name}")
    return "\n".join(lines)


def format_quit_instruction() -> str:
    """Format the quit and history instruction lines shown below the menu.

    Returns:
        A multi-line string with the quit and history shortcut hints.

    Example:
        >>> print(format_quit_instruction())
          (type 'quit', 'exit', or 'q' to exit)
          (type 'history' or 'h' to view operation history)
    """
    return (
        "  (type 'quit', 'exit', or 'q' to exit)\n"
        "  (type 'history' or 'h' to view operation history)"
    )


def format_history_header() -> str:
    """Format the header displayed before the history entry list.

    Returns:
        A string containing the history section header.

    Example:
        >>> format_history_header()
        '\\nOperation history:'
    """
    return "\nOperation history:"


def format_operation_error(operation: str) -> str:
    """Format an error message for an invalid or unrecognised operation.

    Args:
        operation: The operation name (or string) that was not recognised.

    Returns:
        A single-line error string indicating the selection was invalid.

    Example:
        >>> format_operation_error("add, subtract")
        "Invalid operation. Available operations: add, subtract"
    """
    return f"Invalid operation. Available operations: {operation}"


def format_result(op_name: str, operands: list[float], result: object) -> str:
    """Format a successful operation result for display.

    Args:
        op_name: The name of the calculator operation that was executed.
        operands: The list of operand values passed to the operation.
        result: The return value of the operation.

    Returns:
        A single-line string such as ``"  Result: 5"``.

    Example:
        >>> format_result("add", [2.0, 3.0], 5)
        '  Result: 5'
    """
    return f"  Result: {result}"


def format_error(error_msg: str) -> str:
    """Format an error message for display to the user.

    Args:
        error_msg: The error description string (e.g. from an exception).

    Returns:
        A single-line string such as ``"  Error: division by zero"``.

    Example:
        >>> format_error("division by zero")
        '  Error: division by zero'
    """
    return f"  Error: {error_msg}"


def format_mode_menu() -> str:
    """Format the mode selection menu.

    Returns:
        A multi-line string presenting the available calculator modes as a
        numbered list.

    Example:
        >>> print(format_mode_menu())
        Choose Calculator Mode:
          1. Normal
          2. Scientific
    """
    return "Choose Calculator Mode:\n  1. Normal\n  2. Scientific"


def format_current_mode(mode_name: str) -> str:
    """Format a one-line description of the currently active mode.

    Args:
        mode_name: The raw mode string (e.g. ``"normal"`` or ``"scientific"``).

    Returns:
        A string such as ``"Current mode: Normal"``.

    Example:
        >>> format_current_mode("scientific")
        'Current mode: Scientific'
    """
    return f"Current mode: {mode_name.capitalize()}"
