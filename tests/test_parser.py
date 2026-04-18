"""Comprehensive tests for src.parser module.

Tests the pure parsing logic including BINARY_OPERATORS constant,
parse_operand(), and parse_input() functions with extensive edge cases.
"""

import math
import pytest

from src.parser import BINARY_OPERATORS, parse_operand, parse_input


# ============================================================================
# BINARY_OPERATORS — constant definition and completeness
# ============================================================================


class TestBinaryOperators:
    """Tests for the BINARY_OPERATORS constant."""

    def test_binary_operators_is_dict(self):
        """BINARY_OPERATORS must be a dictionary."""
        assert isinstance(BINARY_OPERATORS, dict)

    def test_binary_operators_has_four_entries(self):
        """BINARY_OPERATORS must have exactly four entries."""
        assert len(BINARY_OPERATORS) == 4

    def test_binary_operators_contains_addition(self):
        """BINARY_OPERATORS must map '+' to 'add'."""
        assert BINARY_OPERATORS["+"] == "add"

    def test_binary_operators_contains_subtraction(self):
        """BINARY_OPERATORS must map '-' to 'subtract'."""
        assert BINARY_OPERATORS["-"] == "subtract"

    def test_binary_operators_contains_multiplication(self):
        """BINARY_OPERATORS must map '*' to 'multiply'."""
        assert BINARY_OPERATORS["*"] == "multiply"

    def test_binary_operators_contains_division(self):
        """BINARY_OPERATORS must map '/' to 'divide'."""
        assert BINARY_OPERATORS["/"] == "divide"

    def test_binary_operators_keys_are_strings(self):
        """All keys in BINARY_OPERATORS must be strings."""
        for key in BINARY_OPERATORS.keys():
            assert isinstance(key, str)

    def test_binary_operators_values_are_strings(self):
        """All values in BINARY_OPERATORS must be strings."""
        for value in BINARY_OPERATORS.values():
            assert isinstance(value, str)


# ============================================================================
# parse_operand — Happy path: valid numeric strings
# ============================================================================


class TestParseOperandHappyPath:
    """Tests for parse_operand with valid numeric inputs."""

    def test_parse_operand_integer_string(self):
        """parse_operand('42') should return 42.0."""
        result = parse_operand("42")
        assert result == pytest.approx(42.0)

    def test_parse_operand_float_string(self):
        """parse_operand('3.14') should return approximately 3.14."""
        result = parse_operand("3.14")
        assert result == pytest.approx(3.14)

    def test_parse_operand_negative_integer(self):
        """parse_operand('-7') should return -7.0."""
        result = parse_operand("-7")
        assert result == pytest.approx(-7.0)

    def test_parse_operand_negative_float(self):
        """parse_operand('-3.5') should return -3.5."""
        result = parse_operand("-3.5")
        assert result == pytest.approx(-3.5)

    def test_parse_operand_zero(self):
        """parse_operand('0') should return 0.0."""
        result = parse_operand("0")
        assert result == pytest.approx(0.0)

    def test_parse_operand_negative_zero(self):
        """parse_operand('-0') should return 0.0."""
        result = parse_operand("-0")
        assert result == pytest.approx(0.0)

    def test_parse_operand_leading_whitespace(self):
        """parse_operand('  5') should strip and return 5.0."""
        result = parse_operand("  5")
        assert result == pytest.approx(5.0)

    def test_parse_operand_trailing_whitespace(self):
        """parse_operand('5  ') should strip and return 5.0."""
        result = parse_operand("5  ")
        assert result == pytest.approx(5.0)

    def test_parse_operand_both_sides_whitespace(self):
        """parse_operand('  5  ') should strip and return 5.0."""
        result = parse_operand("  5  ")
        assert result == pytest.approx(5.0)

    def test_parse_operand_returns_float_type(self):
        """parse_operand must always return a float, even for integer input."""
        result = parse_operand("10")
        assert isinstance(result, float)

    def test_parse_operand_scientific_notation_positive(self):
        """parse_operand('1.5e3') should return 1500.0."""
        result = parse_operand("1.5e3")
        assert result == pytest.approx(1500.0)

    def test_parse_operand_scientific_notation_negative_exponent(self):
        """parse_operand('2.5e-2') should return 0.025."""
        result = parse_operand("2.5e-2")
        assert result == pytest.approx(0.025)

    def test_parse_operand_scientific_notation_uppercase_e(self):
        """parse_operand('1.5E3') should return 1500.0."""
        result = parse_operand("1.5E3")
        assert result == pytest.approx(1500.0)

    def test_parse_operand_very_large_number(self):
        """parse_operand('1e308') should return a very large float."""
        result = parse_operand("1e308")
        assert result == pytest.approx(1e308)

    def test_parse_operand_very_small_number(self):
        """parse_operand('1e-308') should return a very small positive float."""
        result = parse_operand("1e-308")
        assert result == pytest.approx(1e-308)

    def test_parse_operand_tab_whitespace(self):
        """parse_operand with tab characters should be stripped."""
        result = parse_operand("\t42\t")
        assert result == pytest.approx(42.0)

    def test_parse_operand_newline_whitespace(self):
        """parse_operand with newline characters should be stripped."""
        result = parse_operand("\n42\n")
        assert result == pytest.approx(42.0)

    def test_parse_operand_mixed_whitespace(self):
        """parse_operand with mixed whitespace should be stripped."""
        result = parse_operand(" \t\n 42 \n\t ")
        assert result == pytest.approx(42.0)


# ============================================================================
# parse_operand — Edge cases: special numeric values
# ============================================================================


class TestParseOperandSpecialValues:
    """Tests for parse_operand with special float values."""

    def test_parse_operand_nan_string(self):
        """parse_operand('nan') should return NaN (float('nan') is valid)."""
        result = parse_operand("nan")
        assert math.isnan(result)

    def test_parse_operand_inf_string(self):
        """parse_operand('inf') should return positive infinity."""
        result = parse_operand("inf")
        assert math.isinf(result) and result > 0

    def test_parse_operand_negative_inf_string(self):
        """parse_operand('-inf') should return negative infinity."""
        result = parse_operand("-inf")
        assert math.isinf(result) and result < 0

    def test_parse_operand_uppercase_nan(self):
        """parse_operand('NAN') should return NaN."""
        result = parse_operand("NAN")
        assert math.isnan(result)

    def test_parse_operand_uppercase_inf(self):
        """parse_operand('INF') should return infinity."""
        result = parse_operand("INF")
        assert math.isinf(result)

    def test_parse_operand_underscore_grouping(self):
        """parse_operand('1_000') should return 1000.0 (Python 3.6+ feature)."""
        result = parse_operand("1_000")
        assert result == pytest.approx(1000.0)

    def test_parse_operand_multiple_underscore_grouping(self):
        """parse_operand('1_000_000') should return 1000000.0."""
        result = parse_operand("1_000_000")
        assert result == pytest.approx(1000000.0)


# ============================================================================
# parse_operand — Error cases: invalid strings
# ============================================================================


class TestParseOperandInvalidStrings:
    """Tests for parse_operand with invalid non-numeric input."""

    def test_parse_operand_empty_string_raises(self):
        """parse_operand('') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_operand("")

    def test_parse_operand_whitespace_only_raises(self):
        """parse_operand('   ') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_operand("   ")

    def test_parse_operand_alphabetic_raises(self):
        """parse_operand('abc') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_operand("abc")

    def test_parse_operand_two_decimal_points_raises(self):
        """parse_operand('1.2.3') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_operand("1.2.3")

    def test_parse_operand_comma_separator_raises(self):
        """parse_operand('1,000') should raise ValueError (comma not valid)."""
        with pytest.raises(ValueError):
            parse_operand("1,000")

    def test_parse_operand_space_between_digits_raises(self):
        """parse_operand('1 2') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_operand("1 2")

    def test_parse_operand_double_plus_raises(self):
        """parse_operand('++1') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_operand("++1")

    def test_parse_operand_double_minus_raises(self):
        """parse_operand('--1') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_operand("--1")

    def test_parse_operand_incomplete_scientific_notation_raises(self):
        """parse_operand('1e') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_operand("1e")

    def test_parse_operand_hex_notation_raises(self):
        """parse_operand('0x10') should raise ValueError (not float format)."""
        with pytest.raises(ValueError):
            parse_operand("0x10")

    def test_parse_operand_special_characters_raises(self):
        """parse_operand('@#$%') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_operand("@#$%")

    def test_parse_operand_error_message_includes_input(self):
        """ValueError message should mention the invalid input."""
        with pytest.raises(ValueError, match="xyz"):
            parse_operand("xyz")


# ============================================================================
# parse_operand — Error cases: invalid types
# ============================================================================


class TestParseOperandInvalidTypes:
    """Tests for parse_operand with non-string input."""

    def test_parse_operand_none_raises(self):
        """parse_operand(None) should raise AttributeError or TypeError."""
        with pytest.raises((AttributeError, TypeError)):
            parse_operand(None)  # type: ignore[arg-type]

    def test_parse_operand_integer_raises(self):
        """parse_operand(42) should raise AttributeError (int has no strip())."""
        with pytest.raises(AttributeError):
            parse_operand(42)  # type: ignore[arg-type]

    def test_parse_operand_float_raises(self):
        """parse_operand(3.14) should raise AttributeError."""
        with pytest.raises(AttributeError):
            parse_operand(3.14)  # type: ignore[arg-type]

    def test_parse_operand_list_raises(self):
        """parse_operand([1, 2]) should raise AttributeError."""
        with pytest.raises(AttributeError):
            parse_operand([1, 2])  # type: ignore[arg-type]

    def test_parse_operand_dict_raises(self):
        """parse_operand({'a': 1}) should raise AttributeError."""
        with pytest.raises(AttributeError):
            parse_operand({"a": 1})  # type: ignore[arg-type]


# ============================================================================
# parse_input — Happy path: valid operator and operand combinations
# ============================================================================


class TestParseInputHappyPath:
    """Tests for parse_input with valid inputs."""

    def test_parse_input_addition(self):
        """parse_input('3', '4', '+') should return (3.0, 4.0, 'add')."""
        a, b, method = parse_input("3", "4", "+")
        assert a == pytest.approx(3.0)
        assert b == pytest.approx(4.0)
        assert method == "add"

    def test_parse_input_subtraction(self):
        """parse_input('10', '5', '-') should return (10.0, 5.0, 'subtract')."""
        a, b, method = parse_input("10", "5", "-")
        assert a == pytest.approx(10.0)
        assert b == pytest.approx(5.0)
        assert method == "subtract"

    def test_parse_input_multiplication(self):
        """parse_input('6', '7', '*') should return (6.0, 7.0, 'multiply')."""
        a, b, method = parse_input("6", "7", "*")
        assert a == pytest.approx(6.0)
        assert b == pytest.approx(7.0)
        assert method == "multiply"

    def test_parse_input_division(self):
        """parse_input('8', '2', '/') should return (8.0, 2.0, 'divide')."""
        a, b, method = parse_input("8", "2", "/")
        assert a == pytest.approx(8.0)
        assert b == pytest.approx(2.0)
        assert method == "divide"

    def test_parse_input_floats(self):
        """parse_input with float strings should parse correctly."""
        a, b, method = parse_input("1.5", "2.5", "+")
        assert a == pytest.approx(1.5)
        assert b == pytest.approx(2.5)
        assert method == "add"

    def test_parse_input_negative_operands(self):
        """parse_input with negative operands should parse correctly."""
        a, b, method = parse_input("-3", "-4", "*")
        assert a == pytest.approx(-3.0)
        assert b == pytest.approx(-4.0)
        assert method == "multiply"

    def test_parse_input_whitespace_padded_operands(self):
        """parse_input should strip whitespace from operands."""
        a, b, method = parse_input("  3  ", "  4  ", "+")
        assert a == pytest.approx(3.0)
        assert b == pytest.approx(4.0)

    def test_parse_input_whitespace_padded_operator(self):
        """parse_input should strip whitespace from operator."""
        a, b, method = parse_input("3", "4", " + ")
        assert method == "add"

    def test_parse_input_operator_mapping_completeness(self):
        """All BINARY_OPERATORS entries should map correctly."""
        for symbol, expected_method in BINARY_OPERATORS.items():
            a, b, method = parse_input("1", "2", symbol)
            assert method == expected_method


# ============================================================================
# parse_input — Error cases: invalid operand_a
# ============================================================================


class TestParseInputInvalidOperandA:
    """Tests for parse_input with invalid first operand."""

    def test_parse_input_non_numeric_operand_a_raises(self):
        """parse_input('abc', '4', '+') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_input("abc", "4", "+")

    def test_parse_input_empty_operand_a_raises(self):
        """parse_input('', '4', '+') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_input("", "4", "+")

    def test_parse_input_whitespace_only_operand_a_raises(self):
        """parse_input('   ', '4', '+') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_input("   ", "4", "+")

    def test_parse_input_error_message_mentions_operand_a(self):
        """ValueError should be raised from operand_a validation."""
        with pytest.raises(ValueError):
            parse_input("invalid", "4", "+")


# ============================================================================
# parse_input — Error cases: invalid operand_b
# ============================================================================


class TestParseInputInvalidOperandB:
    """Tests for parse_input with invalid second operand."""

    def test_parse_input_non_numeric_operand_b_raises(self):
        """parse_input('3', 'xyz', '+') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_input("3", "xyz", "+")

    def test_parse_input_empty_operand_b_raises(self):
        """parse_input('3', '', '+') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_input("3", "", "+")

    def test_parse_input_whitespace_only_operand_b_raises(self):
        """parse_input('3', '   ', '+') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_input("3", "   ", "+")


# ============================================================================
# parse_input — Error cases: unsupported operator
# ============================================================================


class TestParseInputUnsupportedOperator:
    """Tests for parse_input with invalid operator."""

    def test_parse_input_unsupported_operator_percent_raises(self):
        """parse_input('3', '4', '%') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_input("3", "4", "%")

    def test_parse_input_unsupported_operator_power_raises(self):
        """parse_input('2', '3', '**') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_input("2", "3", "**")

    def test_parse_input_empty_operator_raises(self):
        """parse_input('3', '4', '') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_input("3", "4", "")

    def test_parse_input_word_operator_raises(self):
        """parse_input('3', '4', 'add') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_input("3", "4", "add")

    def test_parse_input_caret_operator_raises(self):
        """parse_input('2', '3', '^') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_input("2", "3", "^")

    def test_parse_input_floor_division_raises(self):
        """parse_input('5', '2', '//') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_input("5", "2", "//")

    def test_parse_input_error_message_mentions_operator(self):
        """ValueError should mention unsupported operator."""
        with pytest.raises(ValueError, match="Unsupported operator"):
            parse_input("3", "4", "%")

    def test_parse_input_error_message_lists_supported_operators(self):
        """ValueError should list supported operators."""
        with pytest.raises(ValueError, match="Supported operators"):
            parse_input("3", "4", "xyz")


# ============================================================================
# parse_input — Error cases: both operands invalid
# ============================================================================


class TestParseInputBothInvalid:
    """Tests for parse_input when both operands are invalid."""

    def test_parse_input_both_operands_non_numeric_raises(self):
        """parse_input('abc', 'xyz', '+') should raise ValueError."""
        with pytest.raises(ValueError):
            parse_input("abc", "xyz", "+")

    def test_parse_input_first_invalid_takes_precedence(self):
        """First invalid operand error should be raised before second is checked."""
        # parse_operand is called for operand_a first, so its error should propagate
        with pytest.raises(ValueError):
            parse_input("abc", "xyz", "+")


# ============================================================================
# parse_input — Parametrized tests for comprehensive coverage
# ============================================================================


class TestParseInputParametrized:
    """Parametrized tests for parse_input covering all operators and edge cases."""

    @pytest.mark.parametrize("symbol,expected_method", [
        ("+", "add"),
        ("-", "subtract"),
        ("*", "multiply"),
        ("/", "divide"),
    ])
    def test_all_operators_map_correctly(self, symbol, expected_method):
        """Each operator symbol must map to correct method name."""
        _, _, method = parse_input("1", "2", symbol)
        assert method == expected_method

    @pytest.mark.parametrize("invalid_op", [
        "%", "**", "//", "^", "add", "subtract", "multiply", "divide",
        "mod", "pow", "!!", "==", "!=", "<<", ">>", "&", "|", "~",
    ])
    def test_unsupported_operators_raise(self, invalid_op):
        """All unsupported operators must raise ValueError."""
        with pytest.raises(ValueError):
            parse_input("1", "2", invalid_op)

    @pytest.mark.parametrize("invalid_operand", [
        "abc", "xyz", "12.34.56", "1e", "0x10", "@#$", "1,000",
    ])
    def test_invalid_operands_raise(self, invalid_operand):
        """All invalid operand strings must raise ValueError."""
        with pytest.raises(ValueError):
            parse_input(invalid_operand, "2", "+")


# ============================================================================
# parse_operand and parse_input — Integration and consistency
# ============================================================================


class TestParserConsistency:
    """Tests ensuring parse_operand and parse_input work consistently together."""

    def test_parse_input_uses_parse_operand_logic(self):
        """parse_input should parse operands the same way as parse_operand."""
        a_direct = parse_operand("3.5")
        a_from_input, _, _ = parse_input("3.5", "2.5", "+")
        assert a_direct == pytest.approx(a_from_input)

    def test_parse_input_invalid_operand_raises_same_as_direct(self):
        """parse_input error for operand should match parse_operand error."""
        with pytest.raises(ValueError):
            parse_operand("invalid")
        with pytest.raises(ValueError):
            parse_input("invalid", "2", "+")

    def test_parse_input_scientific_notation_works(self):
        """parse_input should handle scientific notation operands."""
        a, b, _ = parse_input("1e2", "2e1", "+")
        assert a == pytest.approx(100.0)
        assert b == pytest.approx(20.0)

    def test_parse_input_with_special_floats(self):
        """parse_input should accept inf and nan operands."""
        a, b, _ = parse_input("inf", "nan", "+")
        assert math.isinf(a)
        assert math.isnan(b)


# ============================================================================
# parse_operand — Boundary and extreme values
# ============================================================================


class TestParseOperandBoundaryValues:
    """Tests for parse_operand with boundary and extreme values."""

    def test_parse_operand_max_float_approximation(self):
        """parse_operand should handle values near float maximum."""
        result = parse_operand("1e308")
        assert result == pytest.approx(1e308)

    def test_parse_operand_min_float_approximation(self):
        """parse_operand should handle very small positive values."""
        result = parse_operand("1e-308")
        assert result == pytest.approx(1e-308)

    def test_parse_operand_zero_variants(self):
        """parse_operand should handle zero and its variants."""
        assert parse_operand("0") == pytest.approx(0.0)
        assert parse_operand("+0") == pytest.approx(0.0)
        assert parse_operand("-0") == pytest.approx(0.0)
        assert parse_operand("0.0") == pytest.approx(0.0)

    def test_parse_operand_trailing_zeros(self):
        """parse_operand should handle trailing zeros correctly."""
        assert parse_operand("1.0") == pytest.approx(1.0)
        assert parse_operand("1.00") == pytest.approx(1.0)
        assert parse_operand("1.000") == pytest.approx(1.0)


# ============================================================================
# parse_input — Return value structure
# ============================================================================


class TestParseInputReturnStructure:
    """Tests verifying parse_input return value structure."""

    def test_parse_input_returns_tuple(self):
        """parse_input must return a tuple."""
        result = parse_input("1", "2", "+")
        assert isinstance(result, tuple)

    def test_parse_input_returns_three_element_tuple(self):
        """parse_input must return exactly three elements."""
        result = parse_input("1", "2", "+")
        assert len(result) == 3

    def test_parse_input_first_element_is_float(self):
        """First tuple element must be a float."""
        a, _, _ = parse_input("1", "2", "+")
        assert isinstance(a, float)

    def test_parse_input_second_element_is_float(self):
        """Second tuple element must be a float."""
        _, b, _ = parse_input("1", "2", "+")
        assert isinstance(b, float)

    def test_parse_input_third_element_is_string(self):
        """Third tuple element must be a string (method name)."""
        _, _, method = parse_input("1", "2", "+")
        assert isinstance(method, str)

    def test_parse_input_third_element_in_values(self):
        """Third element must be a value from BINARY_OPERATORS."""
        _, _, method = parse_input("1", "2", "+")
        assert method in BINARY_OPERATORS.values()
