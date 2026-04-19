"""Interface utilities for the Calculator application.

This package provides argument parsing, operand conversion, result
formatting, and menu display helpers used by both the CLI and interactive
session layers.
"""

from .input_parser import parse_cli_args, convert_operand
from .output_formatter import format_result
from .menu_renderer import display_menu

__all__ = ["parse_cli_args", "convert_operand", "format_result", "display_menu"]
