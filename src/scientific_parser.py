"""Parsing logic for scientific unary function expressions.

This module provides ``parse_unary_function`` which converts user-supplied
strings of the form ``func(arg)`` into ``(method_name, operand)`` tuples
that can be dispatched directly on a Calculator or CalculatorWithHistory
instance.  It contains no I/O, no class instantiation, and no side effects
beyond error logging.
"""

import re

from src.logger import get_logger

# Maps the user-facing function name to the Calculator method name.
UNARY_FUNCTIONS: dict[str, str] = {
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "log": "log",
    "ln": "ln",
    "exp": "exp",
    "sqrt": "sqrt",
}

# Compiled pattern: optional whitespace around name, open paren, arg, close paren.
_UNARY_PATTERN: re.Pattern[str] = re.compile(
    r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\s*([^)]+)\s*\)\s*$"
)


def parse_unary_function(raw: str) -> tuple[str, float]:
    """Parse a unary function call string into a (method_name, operand) pair.

    Accepted syntax: ``func(arg)`` where *func* is one of the supported
    function names and *arg* is a numeric value (integer or float).

    Args:
        raw: The user-supplied expression, e.g. ``"sin(1.57)"`` or
            ``"log(100)"``.

    Returns:
        A tuple ``(method_name, operand)`` where *method_name* is the
        corresponding Calculator method name and *operand* is the parsed
        float argument.

    Raises:
        ValueError: If the expression does not match the expected syntax,
            if the function name is not supported, or if the argument
            cannot be converted to a float.
    """
    logger = get_logger(__name__)

    match = _UNARY_PATTERN.match(raw)
    if match is None:
        logger.error(f"parse_unary_function({raw!r}) failed: syntax mismatch")
        raise ValueError(
            f"Invalid expression {raw!r}. "
            "Expected syntax: func(arg), e.g. sin(1.57) or log(100)."
        )

    func_name = match.group(1)
    arg_raw = match.group(2)

    if func_name not in UNARY_FUNCTIONS:
        supported = ", ".join(sorted(UNARY_FUNCTIONS))
        logger.error(
            f"parse_unary_function({raw!r}) failed: unknown function {func_name!r}"
        )
        raise ValueError(
            f"Unknown function {func_name!r}. "
            f"Supported functions are: {supported}."
        )

    try:
        operand = float(arg_raw.strip())
    except ValueError:
        logger.error(
            f"parse_unary_function({raw!r}) failed: "
            f"non-numeric argument {arg_raw!r}"
        )
        raise ValueError(
            f"Invalid argument {arg_raw!r} for function {func_name!r}: "
            "expected a numeric value, e.g. '1.57' or '100'."
        )

    method_name = UNARY_FUNCTIONS[func_name]
    return method_name, operand
