"""iOS-style visual theme constants for the Calculator GUI.

:data:`_THEME` contains all colour and font values used by the iOS-style
layout.  :data:`OPERATION_SYMBOLS` maps canonical operation names to the
Unicode glyphs displayed on each button.
"""

from typing import Final

_THEME: Final[dict[str, object]] = {
    "bg_window": "#000000",
    "bg_result_display": "#000000",
    "fg_result_display": "#FFFFFF",
    "font_result": ("Courier", 32, "bold"),
    "bg_operator_button": "#FF9500",
    "fg_operator_button": "#FFFFFF",
    "active_bg_operator_button": "#FFB143",
    "bg_utility_button": "#1C1C1E",
    "fg_utility_button": "#FFFFFF",
    "active_bg_utility_button": "#2C2C2E",
    "bg_standard_button": "#333333",
    "fg_standard_button": "#FFFFFF",
    "active_bg_standard_button": "#4D4D4D",
    "fg_button": "#FFFFFF",
    "bg_mode_button": "#1C1C1E",
    "fg_mode_button": "#FFFFFF",
    "active_bg_mode_button": "#2C2C2E",
}

OPERATION_SYMBOLS: Final[dict[str, str]] = {
    "add": "+",
    "subtract": "−",       # − (U+2212 MINUS SIGN)
    "multiply": "×",       # ×
    "divide": "÷",         # ÷
    "sqrt": "√",           # √
    "square_root": "√",    # √
    "square": "x²",        # x²
    "cube": "x³",          # x³
    "cube_root": "∛",      # ∛
    "power": "xʸ",         # xʸ
    "factorial": "n!",
    "log": "log",
    "logarithm": "log",
    "ln": "ln",
    "natural_logarithm": "ln",
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "cot": "cot",
    "asin": "asin",
    "acos": "acos",
    "atan": "atan",
    "pi": "π",             # π
    "e": "e",
}
