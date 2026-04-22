"""Interactive command-line interface for the Calculator.

Provides a menu-driven REPL that allows a user to select and invoke any
public operation exposed by a Calculator instance without knowing its
internal structure in advance.
"""

import inspect

from .calculator import Calculator


def get_arity(calculator: Calculator, op_name: str) -> int:
    """Return the number of operands required by a Calculator operation.

    Uses :func:`inspect.signature` to count the parameters of the named
    method, excluding ``self``.

    Args:
        calculator: The Calculator instance whose method is inspected.
        op_name: The name of the public method to examine.

    Returns:
        The number of parameters the method accepts, not counting ``self``.

    Example:
        >>> calc = Calculator()
        >>> get_arity(calc, "add")
        2
        >>> get_arity(calc, "square")
        1
    """
    method = getattr(calculator, op_name)
    sig = inspect.signature(method)
    # ``method`` is already a bound method, so ``self`` is not present in
    # the signature — every parameter counted here is a real operand.
    return len(sig.parameters)


def get_operation_menu(calculator: Calculator) -> list[str]:
    """Return all public (non-dunder) method names on a Calculator instance.

    Args:
        calculator: The Calculator instance to introspect.

    Returns:
        A list of method name strings sorted in the order they are
        returned by :func:`dir`, with dunder names excluded.
    """
    return [
        name
        for name in dir(calculator)
        if not name.startswith("_") and callable(getattr(calculator, name))
    ]


def parse_float(value: str) -> float:
    """Parse a string as a float, raising ValueError if it is not numeric.

    Args:
        value: The raw string entered by the user.

    Returns:
        The parsed float value.

    Raises:
        ValueError: If *value* cannot be converted to a float.
    """
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"'{value}' is not a valid number.")


def get_operands(arity: int) -> list[float]:
    """Prompt the user for the required number of numeric operands.

    Loops until *arity* valid floats have been collected.  An invalid entry
    causes an error message to be printed and the same prompt to repeat.

    Args:
        arity: The number of operands to collect (typically 1 or 2).

    Returns:
        A list of *arity* floats in entry order.
    """
    operands: list[float] = []
    for i in range(1, arity + 1):
        while True:
            raw = input(f"  Enter operand {i}: ")
            try:
                operands.append(parse_float(raw))
                break
            except ValueError as exc:
                print(f"  Invalid input: {exc}  Please try again.")
    return operands


def interactive_session(calculator: Calculator) -> None:
    """Run a menu-driven interactive session for the given calculator.

    Displays a numbered list of all public operations, prompts the user to
    select one by number, collects the required operands, executes the
    operation, and prints the result.  The loop continues until the user
    types ``quit``, ``exit``, or ``q`` at the selection prompt.

    Args:
        calculator: The Calculator instance to use for all computations.
    """
    while True:
        operations = get_operation_menu(calculator)

        print("\nAvailable operations:")
        for idx, op_name in enumerate(operations, start=1):
            print(f"  {idx}. {op_name}")
        print("  (type 'quit', 'exit', or 'q' to exit)")

        raw_choice = input("\nSelect operation (number): ").strip().lower()

        if raw_choice in {"quit", "exit", "q"}:
            print("Goodbye!")
            break

        try:
            choice = int(raw_choice)
        except ValueError:
            print(f"  Invalid selection '{raw_choice}'. Please enter a number.")
            continue

        if choice < 1 or choice > len(operations):
            print(f"  Selection out of range. Choose between 1 and {len(operations)}.")
            continue

        op_name = operations[choice - 1]
        arity = get_arity(calculator, op_name)

        operands = get_operands(arity)

        try:
            result = getattr(calculator, op_name)(*operands)
            print(f"  Result: {result}")
        except Exception as exc:  # noqa: BLE001
            print(f"  Error: {exc}")
