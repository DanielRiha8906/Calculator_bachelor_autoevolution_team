"""Scientific operation registry for the Calculator application.

Defines the SCIENTIFIC_OPERATIONS registry as a module-level constant.
These operations are only visible to the user when the session is in
SCIENTIFIC mode.

Each registry entry maps a user-facing operation key to dispatch metadata:

* ``method``  — name of the corresponding ``Calculator`` method.
* ``arity``   — number of operands required (0, 1, or 2).
* ``label``   — human-readable description shown in menus.
* ``coerce``  — (optional) callable used to convert raw string operands;
                defaults to ``float`` when absent.
"""

SCIENTIFIC_OPERATIONS: dict[str, dict] = {
    "sin": {
        "method": "sin",
        "arity": 1,
        "label": "Sine of x (x in radians)",
    },
    "cos": {
        "method": "cos",
        "arity": 1,
        "label": "Cosine of x (x in radians)",
    },
    "tan": {
        "method": "tan",
        "arity": 1,
        "label": "Tangent of x (x in radians)",
    },
    "asin": {
        "method": "asin",
        "arity": 1,
        "label": "Arcsine of x (result in radians, domain: [-1, 1])",
    },
    "acos": {
        "method": "acos",
        "arity": 1,
        "label": "Arccosine of x (result in radians, domain: [-1, 1])",
    },
    "atan": {
        "method": "atan",
        "arity": 1,
        "label": "Arctangent of x (result in radians)",
    },
    "pi": {
        "method": "get_pi",
        "arity": 0,
        "label": "Mathematical constant pi (~3.14159)",
    },
    "e": {
        "method": "get_e",
        "arity": 0,
        "label": "Mathematical constant e (~2.71828)",
    },
}
