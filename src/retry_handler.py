"""Retry logic for interactive calculator input.

Provides helpers that prompt the user for operands and an operator with
a configurable number of retries before aborting. All validation reuses
logic from input_handler so there is no duplication of parsing rules.
"""

from src.parser import BINARY_OPERATORS, parse_operand

MAX_RETRIES: int = 3


def get_operand_with_retries(
    prompt: str, max_retries: int = MAX_RETRIES
) -> float | None:
    """Prompt the user for a numeric operand, retrying on invalid input.

    Args:
        prompt: The message displayed to the user before each attempt.
        max_retries: Maximum number of attempts before giving up.

    Returns:
        The parsed float value on success, or ``None`` if all retries are
        exhausted.
    """
    attempts_left = max_retries
    while attempts_left > 0:
        raw = input(prompt)
        if not raw.strip():
            attempts_left -= 1
            remaining = attempts_left
            print(
                f"Invalid input: operand cannot be empty. "
                f"{remaining} attempt(s) remaining."
            )
            continue
        try:
            return parse_operand(raw)
        except ValueError as exc:
            attempts_left -= 1
            remaining = attempts_left
            print(f"Invalid input: {exc} {remaining} attempt(s) remaining.")

    print("Maximum retries reached. Operation cancelled.")
    return None


def get_operator_with_retries(
    valid_operators: list[str], max_retries: int = MAX_RETRIES
) -> str | None:
    """Prompt the user for an operator, retrying on invalid input.

    Args:
        valid_operators: The set of accepted operator strings.
        max_retries: Maximum number of attempts before giving up.

    Returns:
        The validated operator string on success, or ``None`` if all
        retries are exhausted.
    """
    attempts_left = max_retries
    while attempts_left > 0:
        raw = input(f"Enter operator ({', '.join(valid_operators)}): ")
        stripped = raw.strip()
        if stripped in valid_operators:
            return stripped
        attempts_left -= 1
        remaining = attempts_left
        supported = ", ".join(repr(op) for op in valid_operators)
        print(
            f"Invalid input: {raw!r} is not a supported operator. "
            f"Supported operators are: {supported}. "
            f"{remaining} attempt(s) remaining."
        )

    print("Maximum retries reached. Operation cancelled.")
    return None


def get_input_with_retries(
    max_retries: int = MAX_RETRIES,
) -> tuple[float, str, float] | None:
    """Collect both operands and the operator from the user with retry logic.

    Each individual input (first operand, operator, second operand) is
    attempted up to *max_retries* times independently. If any single
    input exhausts its retries the whole collection is aborted and
    ``None`` is returned.

    Args:
        max_retries: Maximum attempts allowed for each individual input.

    Returns:
        A ``(first_operand, operator, second_operand)`` tuple on success,
        or ``None`` if any input could not be collected within the retry
        limit.
    """
    first_operand = get_operand_with_retries(
        "Enter first operand: ", max_retries=max_retries
    )
    if first_operand is None:
        return None

    second_operand = get_operand_with_retries(
        "Enter second operand: ", max_retries=max_retries
    )
    if second_operand is None:
        return None

    operator = get_operator_with_retries(
        list(BINARY_OPERATORS.keys()), max_retries=max_retries
    )
    if operator is None:
        return None

    return first_operand, operator, second_operand
