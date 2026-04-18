"""Comprehensive pytest tests for src/session/mode.py.

Tests verify:
- Mode enum has NORMAL and SCIENTIFIC members with correct string values
- parse_mode_command() correctly parses "mode normal" and "mode scientific" commands
- Case-insensitive parsing of mode commands
- Invalid mode commands, missing arguments, and non-mode commands return None
- Edge cases: empty strings, whitespace, multiple words
"""

import pytest
from src.session.mode import Mode, parse_mode_command


# ===========================================================================
# Mode Enum: Structure and Members
# ===========================================================================

def test_mode_is_enum():
    """Mode must be an Enum."""
    from enum import Enum
    assert isinstance(Mode, type)
    assert issubclass(Mode, Enum)


def test_mode_has_normal_member():
    """Mode enum must have NORMAL member."""
    assert hasattr(Mode, 'NORMAL')
    assert isinstance(Mode.NORMAL, Mode)


def test_mode_has_scientific_member():
    """Mode enum must have SCIENTIFIC member."""
    assert hasattr(Mode, 'SCIENTIFIC')
    assert isinstance(Mode.SCIENTIFIC, Mode)


def test_mode_normal_value():
    """Mode.NORMAL value must be 'normal'."""
    assert Mode.NORMAL.value == "normal"


def test_mode_scientific_value():
    """Mode.SCIENTIFIC value must be 'scientific'."""
    assert Mode.SCIENTIFIC.value == "scientific"


def test_mode_members_count():
    """Mode enum must have exactly 2 members."""
    assert len(Mode) == 2


def test_mode_members_are_unique():
    """Each Mode member must be unique."""
    members = list(Mode)
    assert len(members) == len(set(members))


# ===========================================================================
# parse_mode_command: Basic Parsing
# ===========================================================================

def test_parse_mode_command_normal():
    """parse_mode_command('mode normal') returns Mode.NORMAL."""
    result = parse_mode_command("mode normal")
    assert result is Mode.NORMAL


def test_parse_mode_command_scientific():
    """parse_mode_command('mode scientific') returns Mode.SCIENTIFIC."""
    result = parse_mode_command("mode scientific")
    assert result is Mode.SCIENTIFIC


def test_parse_mode_command_returns_enum_member():
    """parse_mode_command must return a Mode enum member, not a string."""
    result = parse_mode_command("mode normal")
    assert isinstance(result, Mode)
    assert result is not "normal"


# ===========================================================================
# parse_mode_command: Case Insensitivity
# ===========================================================================

def test_parse_mode_command_uppercase_mode():
    """parse_mode_command('MODE NORMAL') returns Mode.NORMAL (uppercase)."""
    result = parse_mode_command("MODE NORMAL")
    assert result is Mode.NORMAL


def test_parse_mode_command_uppercase_scientific():
    """parse_mode_command('MODE SCIENTIFIC') returns Mode.SCIENTIFIC (uppercase)."""
    result = parse_mode_command("MODE SCIENTIFIC")
    assert result is Mode.SCIENTIFIC


def test_parse_mode_command_mixed_case():
    """parse_mode_command('Mode Normal') returns Mode.NORMAL (mixed case)."""
    result = parse_mode_command("Mode Normal")
    assert result is Mode.NORMAL


def test_parse_mode_command_mode_uppercase_value_lowercase():
    """parse_mode_command('MODE normal') returns Mode.NORMAL."""
    result = parse_mode_command("MODE normal")
    assert result is Mode.NORMAL


def test_parse_mode_command_mode_lowercase_value_uppercase():
    """parse_mode_command('mode NORMAL') returns Mode.NORMAL."""
    result = parse_mode_command("mode NORMAL")
    assert result is Mode.NORMAL


def test_parse_mode_command_all_mixed_case_variations():
    """parse_mode_command handles various mixed-case combinations."""
    test_cases = [
        ("mode NORMAL", Mode.NORMAL),
        ("MODE normal", Mode.NORMAL),
        ("Mode Normal", Mode.NORMAL),
        ("MoDe NoRmAl", Mode.NORMAL),
        ("mode SCIENTIFIC", Mode.SCIENTIFIC),
        ("MODE scientific", Mode.SCIENTIFIC),
        ("Mode Scientific", Mode.SCIENTIFIC),
    ]
    for input_str, expected in test_cases:
        assert parse_mode_command(input_str) is expected, f"Failed for: {input_str}"


# ===========================================================================
# parse_mode_command: Invalid Modes and Non-Commands
# ===========================================================================

def test_parse_mode_command_invalid_mode_name():
    """parse_mode_command('mode invalid') returns None (unknown mode)."""
    result = parse_mode_command("mode invalid")
    assert result is None


def test_parse_mode_command_unknown_mode():
    """parse_mode_command('mode quantum') returns None (unknown mode)."""
    result = parse_mode_command("mode quantum")
    assert result is None


def test_parse_mode_command_typo_in_normal():
    """parse_mode_command('mode norma') returns None (typo)."""
    result = parse_mode_command("mode norma")
    assert result is None


def test_parse_mode_command_typo_in_scientific():
    """parse_mode_command('mode scientific') with typo returns None."""
    result = parse_mode_command("mode sceintific")
    assert result is None


def test_parse_mode_command_not_a_mode_command():
    """parse_mode_command('add') returns None (not a mode command)."""
    result = parse_mode_command("add")
    assert result is None


def test_parse_mode_command_operation_name():
    """parse_mode_command('sin') returns None (it's an operation, not mode)."""
    result = parse_mode_command("sin")
    assert result is None


def test_parse_mode_command_random_word():
    """parse_mode_command('hello') returns None."""
    result = parse_mode_command("hello")
    assert result is None


# ===========================================================================
# parse_mode_command: Missing or Incomplete Commands
# ===========================================================================

def test_parse_mode_command_empty_string():
    """parse_mode_command('') returns None."""
    result = parse_mode_command("")
    assert result is None


def test_parse_mode_command_only_mode_keyword():
    """parse_mode_command('mode') returns None (no mode name)."""
    result = parse_mode_command("mode")
    assert result is None


def test_parse_mode_command_only_mode_with_spaces():
    """parse_mode_command('mode   ') returns None (no mode name after mode)."""
    result = parse_mode_command("mode   ")
    assert result is None


def test_parse_mode_command_whitespace_only():
    """parse_mode_command('   ') returns None."""
    result = parse_mode_command("   ")
    assert result is None


def test_parse_mode_command_tab_only():
    """parse_mode_command with only tabs returns None."""
    result = parse_mode_command("\t\t")
    assert result is None


# ===========================================================================
# parse_mode_command: Extra Words and Arguments
# ===========================================================================

def test_parse_mode_command_extra_word():
    """parse_mode_command('mode normal extra') returns None (too many parts)."""
    result = parse_mode_command("mode normal extra")
    assert result is None


def test_parse_mode_command_multiple_extra_words():
    """parse_mode_command('mode normal please') returns None."""
    result = parse_mode_command("mode normal please now")
    assert result is None


def test_parse_mode_command_mode_value_value():
    """parse_mode_command('mode normal scientific') returns None."""
    result = parse_mode_command("mode normal scientific")
    assert result is None


# ===========================================================================
# parse_mode_command: Whitespace Handling
# ===========================================================================

def test_parse_mode_command_leading_whitespace():
    """parse_mode_command('  mode normal') handles leading whitespace."""
    result = parse_mode_command("  mode normal")
    assert result is Mode.NORMAL


def test_parse_mode_command_trailing_whitespace():
    """parse_mode_command('mode normal  ') handles trailing whitespace."""
    result = parse_mode_command("mode normal  ")
    assert result is Mode.NORMAL


def test_parse_mode_command_both_leading_trailing_whitespace():
    """parse_mode_command('  mode scientific  ') handles both."""
    result = parse_mode_command("  mode scientific  ")
    assert result is Mode.SCIENTIFIC


def test_parse_mode_command_extra_spaces_between_words():
    """parse_mode_command('mode   normal') with extra spaces between words."""
    result = parse_mode_command("mode   normal")
    assert result is Mode.NORMAL


def test_parse_mode_command_tabs_between_words():
    """parse_mode_command('mode\tnormal') with tab separator."""
    result = parse_mode_command("mode\tnormal")
    assert result is Mode.NORMAL


# ===========================================================================
# parse_mode_command: Edge Cases
# ===========================================================================

def test_parse_mode_command_numeric_input():
    """parse_mode_command('123') returns None."""
    result = parse_mode_command("123")
    assert result is None


def test_parse_mode_command_special_characters():
    """parse_mode_command('mode @#$%') returns None."""
    result = parse_mode_command("mode @#$%")
    assert result is None


def test_parse_mode_command_numeric_mode():
    """parse_mode_command('mode 1') returns None."""
    result = parse_mode_command("mode 1")
    assert result is None


def test_parse_mode_command_unicode_characters():
    """parse_mode_command with unicode returns None for invalid mode."""
    result = parse_mode_command("mode naïve")
    assert result is None


def test_parse_mode_command_newline_in_string():
    """parse_mode_command('mode\\nnormal') with newline is treated as whitespace."""
    # When stripped, "mode\nnormal" becomes "mode normal" which is valid
    result = parse_mode_command("mode\nnormal")
    # Since split() treats newlines as separators, this actually works
    assert result is Mode.NORMAL


# ===========================================================================
# parse_mode_command: Consistency and Return Type
# ===========================================================================

def test_parse_mode_command_returns_none_or_mode():
    """parse_mode_command always returns either Mode enum member or None."""
    test_inputs = [
        "mode normal",
        "mode scientific",
        "mode invalid",
        "add",
        "",
        "mode",
        "mode normal extra",
    ]
    for input_str in test_inputs:
        result = parse_mode_command(input_str)
        assert result is None or isinstance(result, Mode)


def test_parse_mode_command_same_input_consistent_output():
    """Calling parse_mode_command twice with same input yields same result."""
    input_str = "mode scientific"
    result1 = parse_mode_command(input_str)
    result2 = parse_mode_command(input_str)
    assert result1 is result2


def test_parse_mode_command_idempotent():
    """parse_mode_command does not modify state."""
    initial_result = parse_mode_command("mode normal")
    repeated_result = parse_mode_command("mode normal")
    assert initial_result is repeated_result


# ===========================================================================
# Mode Enum: Conversion and Comparison
# ===========================================================================

def test_mode_normal_str():
    """str(Mode.NORMAL) is a meaningful representation."""
    s = str(Mode.NORMAL)
    assert "NORMAL" in s or "normal" in s.lower()


def test_mode_scientific_str():
    """str(Mode.SCIENTIFIC) is a meaningful representation."""
    s = str(Mode.SCIENTIFIC)
    assert "SCIENTIFIC" in s or "scientific" in s.lower()


def test_mode_equality():
    """Mode.NORMAL is equal to itself."""
    assert Mode.NORMAL == Mode.NORMAL
    assert Mode.SCIENTIFIC == Mode.SCIENTIFIC
    assert Mode.NORMAL != Mode.SCIENTIFIC


def test_mode_value_by_name():
    """Mode enum can be accessed by name."""
    assert Mode["NORMAL"] == Mode.NORMAL
    assert Mode["SCIENTIFIC"] == Mode.SCIENTIFIC


def test_mode_value_by_string():
    """Mode enum values can be looked up by string value."""
    assert Mode("normal") == Mode.NORMAL
    assert Mode("scientific") == Mode.SCIENTIFIC


def test_mode_invalid_string_lookup_raises():
    """Mode('invalid') raises ValueError."""
    with pytest.raises(ValueError):
        Mode("invalid")


# ===========================================================================
# Integration: parse_mode_command with Mode enum
# ===========================================================================

def test_parse_mode_command_result_matches_enum():
    """Result of parse_mode_command matches actual enum member."""
    result = parse_mode_command("mode normal")
    assert result == Mode.NORMAL
    assert result.value == "normal"


def test_parse_mode_command_scientific_result_matches_enum():
    """Result for scientific matches actual enum member."""
    result = parse_mode_command("mode scientific")
    assert result == Mode.SCIENTIFIC
    assert result.value == "scientific"


def test_parse_mode_command_none_not_confused_with_any_mode():
    """None returned by parse_mode_command is distinct from any Mode member."""
    result = parse_mode_command("invalid")
    assert result is None
    assert result is not Mode.NORMAL
    assert result is not Mode.SCIENTIFIC
    assert result != Mode.NORMAL
    assert result != Mode.SCIENTIFIC
