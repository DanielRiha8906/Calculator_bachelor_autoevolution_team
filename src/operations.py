"""Operation registry for the Calculator application.

This module defines the OPERATIONS registry as a module-level constant,
independent of any interaction mode (interactive REPL or CLI). Both
``input_handler`` and ``cli`` import from here to avoid duplication and
to prevent circular imports.

Each registry entry maps a user-facing operation key to dispatch metadata:

* ``method``  — name of the corresponding ``Calculator`` method.
* ``arity``   — number of operands required (1 or 2).
* ``label``   — human-readable description shown in menus.
* ``coerce``  — (optional) callable used to convert raw string operands;
                defaults to ``float`` when absent.
"""

OPERATIONS: dict[str, dict] = {
    "add": {
        "method": "add",
        "arity": 2,
        "label": "Add two numbers",
    },
    "subtract": {
        "method": "subtract",
        "arity": 2,
        "label": "Subtract two numbers",
    },
    "multiply": {
        "method": "multiply",
        "arity": 2,
        "label": "Multiply two numbers",
    },
    "divide": {
        "method": "divide",
        "arity": 2,
        "label": "Divide two numbers",
    },
    "power": {
        "method": "power",
        "arity": 2,
        "label": "Raise a number to a power",
    },
    "factorial": {
        "method": "factorial",
        "arity": 1,
        "label": "Factorial of a non-negative integer",
        "coerce": int,
    },
    "square": {
        "method": "square",
        "arity": 1,
        "label": "Square a number (x^2)",
    },
    "cube": {
        "method": "cube",
        "arity": 1,
        "label": "Cube a number (x^3)",
    },
    "square_root": {
        "method": "square_root",
        "arity": 1,
        "label": "Square root of a number",
    },
    "cube_root": {
        "method": "cube_root",
        "arity": 1,
        "label": "Cube root of a number",
    },
    "log10": {
        "method": "log10",
        "arity": 1,
        "label": "Base-10 logarithm of a number",
    },
    "ln": {
        "method": "ln",
        "arity": 1,
        "label": "Natural logarithm of a number",
    },
}
