"""Test output formatting consistency with documentation.

Verifies that formatter functions produce output consistent with documented
examples and patterns.
"""

import pytest
from src.formatter import (
    format_menu_header,
    format_quit_instruction,
    format_history_header,
    format_result,
    format_error,
)
from src.core.calculator import Calculator


class TestFormatterConsistency:
    """Test that formatter output matches documented patterns."""

    def test_result_format_matches_example(self):
        """Test that format_result output matches documented format."""
        # From USER_GUIDE.md example: Result: 5
        result = format_result("add", [2.0, 3.0], 5)
        assert result == "  Result: 5"
        assert result.startswith("  Result: ")

    def test_result_format_with_float(self):
        """Test format_result with float values."""
        result = format_result("divide", [10.0, 2.0], 5.0)
        assert result == "  Result: 5.0"
        assert "Result:" in result

    def test_result_format_with_decimal(self):
        """Test format_result with decimal result."""
        result = format_result("divide", [7.0, 2.0], 3.5)
        assert result == "  Result: 3.5"

    def test_error_format_readable(self):
        """Test that error messages follow expected pattern."""
        error_msg = "division by zero"
        result = format_error(error_msg)
        assert result == "  Error: division by zero"
        assert result.startswith("  Error: ")

    def test_error_format_with_various_messages(self):
        """Test error formatting with various error messages."""
        test_cases = [
            "invalid operand",
            "out of domain",
            "incorrect arity",
        ]
        for msg in test_cases:
            result = format_error(msg)
            assert result.startswith("  Error: ")
            assert msg in result

    def test_menu_header_has_operations(self):
        """Test that menu header includes all operations."""
        calc = Calculator()
        operations = [
            name
            for name in dir(calc)
            if not name.startswith("_") and callable(getattr(calc, name))
        ]
        menu = format_menu_header(operations)

        assert "Available operations:" in menu
        for op in operations:
            assert op in menu

    def test_menu_header_has_numbered_list(self):
        """Test that menu header includes numbered list."""
        operations = ["add", "subtract", "multiply"]
        menu = format_menu_header(operations)

        assert "1. add" in menu
        assert "2. subtract" in menu
        assert "3. multiply" in menu

    def test_menu_header_with_single_operation(self):
        """Test menu header with single operation."""
        menu = format_menu_header(["add"])
        assert "1. add" in menu
        assert "Available operations:" in menu

    def test_menu_header_with_many_operations(self):
        """Test menu header with many operations."""
        operations = ["add", "subtract", "multiply", "divide", "square"]
        menu = format_menu_header(operations)

        for idx, op in enumerate(operations, 1):
            assert f"{idx}. {op}" in menu

    def test_quit_instruction_shown(self):
        """Test that quit instruction is present and readable."""
        instruction = format_quit_instruction()
        assert "quit" in instruction.lower()
        assert "exit" in instruction.lower()

    def test_quit_instruction_mentions_quit_aliases(self):
        """Test that quit instruction mentions all quit aliases."""
        instruction = format_quit_instruction()
        assert "'quit'" in instruction
        assert "'exit'" in instruction
        assert "'q'" in instruction

    def test_quit_instruction_mentions_history(self):
        """Test that quit instruction mentions history shortcut."""
        instruction = format_quit_instruction()
        assert "history" in instruction.lower()

    def test_history_header_format(self):
        """Test that history header has correct format."""
        header = format_history_header()
        assert "Operation history:" in header
        assert header.startswith("\n")

    def test_formatter_functions_return_strings(self):
        """Test that all formatters return strings."""
        assert isinstance(format_menu_header(["add"]), str)
        assert isinstance(format_quit_instruction(), str)
        assert isinstance(format_history_header(), str)
        assert isinstance(format_result("add", [1], 2), str)
        assert isinstance(format_error("test"), str)

    def test_format_output_indentation(self):
        """Test that formatted output uses consistent indentation."""
        # Result and error messages should start with two spaces
        assert format_result("add", [1], 2).startswith("  ")
        assert format_error("test").startswith("  ")

    def test_menu_header_newline_start(self):
        """Test that menu header starts with newline."""
        menu = format_menu_header(["add"])
        assert menu.startswith("\n")

    def test_empty_operations_list_menu(self):
        """Test menu header with empty operations list."""
        menu = format_menu_header([])
        assert "Available operations:" in menu
        assert menu.count("\n") >= 0  # Should have at least header line
