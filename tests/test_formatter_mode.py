"""Tests for formatter.py mode-related functions."""

import pytest
from src.formatter import (
    format_mode_menu,
    format_current_mode,
    format_menu_header,
)


class TestFormatModeMenu:
    """Test suite for format_mode_menu() function."""

    def test_format_mode_menu_contains_normal(self):
        """Test format_mode_menu output contains 'Normal'."""
        output = format_mode_menu()
        assert "Normal" in output

    def test_format_mode_menu_contains_scientific(self):
        """Test format_mode_menu output contains 'Scientific'."""
        output = format_mode_menu()
        assert "Scientific" in output

    def test_format_mode_menu_contains_choice_labels(self):
        """Test format_mode_menu contains numbered choices."""
        output = format_mode_menu()
        assert "1" in output
        assert "2" in output

    def test_format_mode_menu_is_string(self):
        """Test format_mode_menu returns a string."""
        output = format_mode_menu()
        assert isinstance(output, str)

    def test_format_mode_menu_is_multiline(self):
        """Test format_mode_menu output contains multiple lines."""
        output = format_mode_menu()
        assert "\n" in output

    def test_format_mode_menu_example(self):
        """Test format_mode_menu matches expected format."""
        output = format_mode_menu()
        expected = "Choose Calculator Mode:\n  1. Normal\n  2. Scientific"
        assert output == expected


class TestFormatCurrentMode:
    """Test suite for format_current_mode() function."""

    def test_format_current_mode_normal(self):
        """Test format_current_mode('normal') returns correct string."""
        output = format_current_mode("normal")
        assert output == "Current mode: Normal"

    def test_format_current_mode_scientific(self):
        """Test format_current_mode('scientific') returns correct string."""
        output = format_current_mode("scientific")
        assert output == "Current mode: Scientific"

    def test_format_current_mode_capitalizes(self):
        """Test format_current_mode capitalizes the mode name."""
        output = format_current_mode("normal")
        assert "Normal" in output
        # Should be capitalized, not lowercase
        assert "normal" not in output or "Normal" in output

    def test_format_current_mode_is_string(self):
        """Test format_current_mode returns a string."""
        output = format_current_mode("normal")
        assert isinstance(output, str)

    def test_format_current_mode_includes_prefix(self):
        """Test format_current_mode includes 'Current mode:' prefix."""
        output = format_current_mode("scientific")
        assert output.startswith("Current mode:")

    def test_format_current_mode_mixed_case_input(self):
        """Test format_current_mode handles mixed case input."""
        output = format_current_mode("NORMAL")
        assert "Normal" in output or "NORMAL" in output

    @pytest.mark.parametrize("mode_name,expected", [
        ("normal", "Current mode: Normal"),
        ("scientific", "Current mode: Scientific"),
    ])
    def test_format_current_mode_parametrized(self, mode_name, expected):
        """Test format_current_mode with parametrized inputs."""
        assert format_current_mode(mode_name) == expected


class TestFormatMenuHeaderBackwardCompat:
    """Test suite for format_menu_header() backward compatibility."""

    def test_format_menu_header_without_mode(self):
        """Test format_menu_header without mode argument (backward compat)."""
        operations = ["add", "subtract"]
        output = format_menu_header(operations)
        assert "Available operations:" in output
        assert "add" in output
        assert "subtract" in output

    def test_format_menu_header_without_mode_is_multiline(self):
        """Test format_menu_header without mode returns multiline."""
        operations = ["add"]
        output = format_menu_header(operations)
        assert "\n" in output

    def test_format_menu_header_with_mode_normal(self):
        """Test format_menu_header with mode='normal' includes mode in output."""
        operations = ["add", "subtract"]
        output = format_menu_header(operations, mode="normal")
        assert "Normal" in output or "normal" in output
        assert "add" in output

    def test_format_menu_header_with_mode_scientific(self):
        """Test format_menu_header with mode='scientific' includes mode in output."""
        operations = ["sin", "cos"]
        output = format_menu_header(operations, mode="scientific")
        assert "Scientific" in output or "scientific" in output
        assert "sin" in output

    def test_format_menu_header_includes_mode_label(self):
        """Test format_menu_header with mode includes 'mode' word."""
        operations = ["add"]
        output = format_menu_header(operations, mode="normal")
        assert "mode" in output.lower()

    def test_format_menu_header_none_mode_equivalent_to_no_mode(self):
        """Test format_menu_header with mode=None is same as omitting mode."""
        operations = ["add", "subtract"]
        output_none = format_menu_header(operations, mode=None)
        output_default = format_menu_header(operations)
        assert output_none == output_default

    def test_format_menu_header_numbered_operations(self):
        """Test format_menu_header numbers operations correctly."""
        operations = ["add", "subtract", "multiply"]
        output = format_menu_header(operations)
        assert "1. add" in output
        assert "2. subtract" in output
        assert "3. multiply" in output

    def test_format_menu_header_is_string(self):
        """Test format_menu_header returns a string."""
        output = format_menu_header(["add"])
        assert isinstance(output, str)

    def test_format_menu_header_empty_operations(self):
        """Test format_menu_header handles empty operations list."""
        output = format_menu_header([])
        assert "Available operations:" in output

    def test_format_menu_header_mode_capitalization(self):
        """Test format_menu_header capitalizes mode name."""
        operations = ["add"]
        output = format_menu_header(operations, mode="normal")
        assert "Normal" in output
