"""Comprehensive tests for src.retry_handler.

Tests cover:
- get_operand_with_retries: valid input, invalid inputs with retries, exhausted retries
- get_operator_with_retries: valid operator, invalid operators, exhausted retries
- get_input_with_retries: full success path, and None returns for each stage
"""

import pytest
from src.retry_handler import (
    get_operand_with_retries,
    get_operator_with_retries,
    get_input_with_retries,
    MAX_RETRIES,
)


# ===========================================================================
# get_operand_with_retries tests
# ===========================================================================


class TestGetOperandWithRetriesHappyPath:
    """Tests for valid operand input on first attempt."""

    def test_valid_integer_on_first_try(self, monkeypatch, capsys):
        monkeypatch.setattr("builtins.input", lambda _: "42")
        result = get_operand_with_retries("Enter: ")
        assert result == 42.0
        captured = capsys.readouterr()
        assert captured.out == ""  # no error messages

    def test_valid_float_on_first_try(self, monkeypatch, capsys):
        monkeypatch.setattr("builtins.input", lambda _: "3.14")
        result = get_operand_with_retries("Enter: ")
        assert result == pytest.approx(3.14)
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_valid_negative_on_first_try(self, monkeypatch, capsys):
        monkeypatch.setattr("builtins.input", lambda _: "-7.5")
        result = get_operand_with_retries("Enter: ")
        assert result == pytest.approx(-7.5)

    def test_valid_zero_on_first_try(self, monkeypatch, capsys):
        monkeypatch.setattr("builtins.input", lambda _: "0")
        result = get_operand_with_retries("Enter: ")
        assert result == 0.0

    def test_valid_scientific_notation_on_first_try(self, monkeypatch, capsys):
        monkeypatch.setattr("builtins.input", lambda _: "1.5e3")
        result = get_operand_with_retries("Enter: ")
        assert result == pytest.approx(1500.0)

    def test_valid_with_whitespace_on_first_try(self, monkeypatch, capsys):
        monkeypatch.setattr("builtins.input", lambda _: "  42  ")
        result = get_operand_with_retries("Enter: ")
        assert result == 42.0

    def test_prompt_message_passed_to_input(self, monkeypatch):
        prompts_seen = []
        def capture_input(prompt):
            prompts_seen.append(prompt)
            return "5"
        monkeypatch.setattr("builtins.input", capture_input)
        get_operand_with_retries("Custom prompt: ")
        assert "Custom prompt: " in prompts_seen


class TestGetOperandWithRetriesEmptyInput:
    """Tests for empty or whitespace-only input triggering retries."""

    def test_empty_string_triggers_retry_then_success(self, monkeypatch, capsys):
        inputs = iter(["", "42"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operand_with_retries("Enter: ")
        assert result == 42.0
        captured = capsys.readouterr()
        assert "operand cannot be empty" in captured.out
        assert "2 attempt(s) remaining" in captured.out

    def test_whitespace_only_triggers_retry(self, monkeypatch, capsys):
        inputs = iter(["   ", "99"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operand_with_retries("Enter: ")
        assert result == 99.0
        captured = capsys.readouterr()
        assert "operand cannot be empty" in captured.out

    def test_multiple_empty_inputs_then_success(self, monkeypatch, capsys):
        inputs = iter(["", "  ", "", "50"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operand_with_retries("Enter: ", max_retries=4)
        assert result == 50.0


class TestGetOperandWithRetriesNonNumeric:
    """Tests for non-numeric input triggering retries."""

    def test_non_numeric_triggers_retry_then_success(self, monkeypatch, capsys):
        inputs = iter(["abc", "42"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operand_with_retries("Enter: ")
        assert result == 42.0
        captured = capsys.readouterr()
        assert "Invalid input:" in captured.out
        assert "2 attempt(s) remaining" in captured.out

    def test_non_numeric_word_triggers_retry(self, monkeypatch, capsys):
        inputs = iter(["hello", "123"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operand_with_retries("Enter: ")
        assert result == 123.0

    def test_special_character_triggers_retry(self, monkeypatch, capsys):
        inputs = iter(["@#$", "5"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operand_with_retries("Enter: ")
        assert result == 5.0

    def test_multiple_invalid_then_success(self, monkeypatch, capsys):
        inputs = iter(["x", "y", "z", "7.5"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operand_with_retries("Enter: ", max_retries=4)
        assert result == 7.5


class TestGetOperandWithRetriesExhausted:
    """Tests for retry exhaustion returning None."""

    def test_retries_exhausted_returns_none(self, monkeypatch, capsys):
        inputs = iter(["abc", "xyz", "invalid", "bad"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operand_with_retries("Enter: ", max_retries=3)
        assert result is None
        captured = capsys.readouterr()
        assert "Maximum retries reached" in captured.out

    def test_all_empty_inputs_exhausts_retries(self, monkeypatch, capsys):
        inputs = iter(["", "", "", ""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operand_with_retries("Enter: ", max_retries=3)
        assert result is None
        captured = capsys.readouterr()
        assert "Maximum retries reached" in captured.out

    def test_default_max_retries_is_three(self, monkeypatch, capsys):
        inputs = iter(["a", "b", "c", "d"])  # 4 inputs for 3 retries
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operand_with_retries("Enter: ")
        assert result is None

    def test_max_retries_one(self, monkeypatch, capsys):
        inputs = iter(["invalid", "also_invalid"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operand_with_retries("Enter: ", max_retries=1)
        assert result is None

    def test_max_retries_zero(self, monkeypatch, capsys):
        inputs = iter(["42"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operand_with_retries("Enter: ", max_retries=0)
        assert result is None
        captured = capsys.readouterr()
        assert "Maximum retries reached" in captured.out

    def test_error_message_printed_before_exhaustion(self, monkeypatch, capsys):
        inputs = iter(["abc", "xyz"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operand_with_retries("Enter: ", max_retries=2)
        assert result is None
        captured = capsys.readouterr()
        assert "Invalid operand 'abc'" in captured.out
        assert "Invalid operand 'xyz'" in captured.out
        assert "Maximum retries reached" in captured.out


class TestGetOperandWithRetriesEdgeCases:
    """Edge cases: very large numbers, NaN, infinity, special formats."""

    def test_very_large_number(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "1e308")
        result = get_operand_with_retries("Enter: ")
        assert result == pytest.approx(1e308)

    def test_very_small_positive_number(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "1e-308")
        result = get_operand_with_retries("Enter: ")
        assert result == pytest.approx(1e-308)

    def test_nan_input(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "nan")
        result = get_operand_with_retries("Enter: ")
        import math
        assert math.isnan(result)

    def test_inf_input(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "inf")
        result = get_operand_with_retries("Enter: ")
        import math
        assert math.isinf(result)

    def test_underscore_grouping_accepted(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "1_000_000")
        result = get_operand_with_retries("Enter: ")
        assert result == 1_000_000.0


# ===========================================================================
# get_operator_with_retries tests
# ===========================================================================


class TestGetOperatorWithRetriesHappyPath:
    """Tests for valid operator input on first attempt."""

    @pytest.mark.parametrize("operator", ["+", "-", "*", "/"])
    def test_valid_operator_on_first_try(self, monkeypatch, capsys, operator):
        monkeypatch.setattr("builtins.input", lambda _: operator)
        result = get_operator_with_retries(["+", "-", "*", "/"])
        assert result == operator
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_custom_operator_list(self, monkeypatch, capsys):
        monkeypatch.setattr("builtins.input", lambda _: "**")
        result = get_operator_with_retries(["**", "//"])
        assert result == "**"

    def test_single_operator_list(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "+")
        result = get_operator_with_retries(["+"])
        assert result == "+"


class TestGetOperatorWithRetriesInvalid:
    """Tests for invalid operator input triggering retries."""

    def test_invalid_operator_triggers_retry_then_success(self, monkeypatch, capsys):
        inputs = iter(["%", "+"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operator_with_retries(["+", "-", "*", "/"])
        assert result == "+"
        captured = capsys.readouterr()
        assert "Invalid input:" in captured.out
        assert "is not a supported operator" in captured.out
        assert "2 attempt(s) remaining" in captured.out

    def test_word_operator_triggers_retry(self, monkeypatch, capsys):
        inputs = iter(["add", "-"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operator_with_retries(["+", "-", "*", "/"])
        assert result == "-"
        captured = capsys.readouterr()
        assert "'add'" in captured.out

    def test_multiple_invalid_then_success(self, monkeypatch, capsys):
        inputs = iter(["^", "//", "%", "/"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operator_with_retries(["+", "-", "*", "/"], max_retries=4)
        assert result == "/"

    def test_error_shows_supported_operators(self, monkeypatch, capsys):
        inputs = iter(["bad", "+"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        get_operator_with_retries(["+", "-", "*", "/"])
        captured = capsys.readouterr()
        assert "Supported operators are:" in captured.out


class TestGetOperatorWithRetriesExhausted:
    """Tests for retry exhaustion returning None."""

    def test_all_invalid_exhausts_retries_returns_none(self, monkeypatch, capsys):
        inputs = iter(["%", "^", "!", "mod"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operator_with_retries(["+", "-", "*", "/"], max_retries=3)
        assert result is None
        captured = capsys.readouterr()
        assert "Maximum retries reached" in captured.out

    def test_default_max_retries_is_three_for_operator(self, monkeypatch, capsys):
        inputs = iter(["%", "^", "!", "mod"])  # 4 inputs for 3 retries
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operator_with_retries(["+", "-", "*", "/"])
        assert result is None

    def test_max_retries_one_for_operator(self, monkeypatch, capsys):
        inputs = iter(["invalid", "also_bad"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operator_with_retries(["+"], max_retries=1)
        assert result is None

    def test_max_retries_zero_for_operator(self, monkeypatch, capsys):
        inputs = iter(["+"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operator_with_retries(["+"], max_retries=0)
        assert result is None
        captured = capsys.readouterr()
        assert "Maximum retries reached" in captured.out


class TestGetOperatorWithRetriesEdgeCases:
    """Edge cases: empty operator list, whitespace, multi-char operators."""

    def test_multi_character_operator(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "**")
        result = get_operator_with_retries(["**", "//"])
        assert result == "**"

    def test_whitespace_stripped_from_input(self, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "  +  ")
        result = get_operator_with_retries(["+", "-"])
        assert result == "+"

    def test_empty_operator_list_always_fails(self, monkeypatch, capsys):
        inputs = iter(["anything"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_operator_with_retries([], max_retries=1)
        assert result is None


# ===========================================================================
# get_input_with_retries tests (integration)
# ===========================================================================


class TestGetInputWithRetriesHappyPath:
    """Tests for full success path: both operands and operator valid."""

    def test_valid_inputs_returns_tuple(self, monkeypatch, capsys):
        inputs = iter(["3", "4", "+"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries()
        assert result == (3.0, "+", 4.0)
        captured = capsys.readouterr()
        # No errors should be printed
        assert "Invalid input:" not in captured.out

    def test_subtraction_inputs(self, monkeypatch, capsys):
        inputs = iter(["10", "3", "-"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries()
        assert result == (10.0, "-", 3.0)

    def test_multiplication_inputs(self, monkeypatch, capsys):
        inputs = iter(["5.5", "2.0", "*"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries()
        assert result == (5.5, "*", 2.0)

    def test_division_inputs(self, monkeypatch, capsys):
        inputs = iter(["20", "4", "/"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries()
        assert result == (20.0, "/", 4.0)

    def test_negative_operands(self, monkeypatch, capsys):
        inputs = iter(["-3", "-4", "*"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries()
        assert result == (-3.0, "*", -4.0)

    def test_scientific_notation_operands(self, monkeypatch, capsys):
        inputs = iter(["1e2", "1e1", "+"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries()
        assert result == (100.0, "+", 10.0)


class TestGetInputWithRetriesFirstOperandFails:
    """Tests for None return when first operand input exhausts retries."""

    def test_first_operand_all_invalid_returns_none(self, monkeypatch, capsys):
        inputs = iter(["abc", "xyz", "invalid", "bad"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries(max_retries=3)
        assert result is None
        captured = capsys.readouterr()
        assert "Maximum retries reached" in captured.out

    def test_first_operand_exhausted_no_prompt_for_second(self, monkeypatch, capsys):
        inputs = iter(["a", "b", "c", "should_not_reach"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries(max_retries=3)
        assert result is None


class TestGetInputWithRetriesSecondOperandFails:
    """Tests for None return when second operand input exhausts retries."""

    def test_second_operand_all_invalid_returns_none(self, monkeypatch, capsys):
        inputs = iter(["5", "abc", "xyz", "invalid", "bad"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries(max_retries=3)
        assert result is None
        captured = capsys.readouterr()
        assert "Maximum retries reached" in captured.out

    def test_second_operand_exhausted_no_prompt_for_operator(self, monkeypatch, capsys):
        inputs = iter(["5", "x", "y", "z", "should_not_reach"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries(max_retries=3)
        assert result is None


class TestGetInputWithRetriesOperatorFails:
    """Tests for None return when operator input exhausts retries."""

    def test_operator_all_invalid_returns_none(self, monkeypatch, capsys):
        inputs = iter(["5", "3", "%", "^", "!", "mod"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries(max_retries=3)
        assert result is None
        captured = capsys.readouterr()
        assert "Maximum retries reached" in captured.out

    def test_operator_exhausted_returns_none_without_error(self, monkeypatch, capsys):
        inputs = iter(["10", "2", "bad1", "bad2", "bad3", "bad4"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries(max_retries=3)
        assert result is None


class TestGetInputWithRetriesPartialSuccess:
    """Tests for partial retries and recovery within get_input_with_retries."""

    def test_first_operand_retries_then_succeeds_full_success(self, monkeypatch, capsys):
        inputs = iter(["invalid", "5", "3", "+"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries(max_retries=2)
        assert result == (5.0, "+", 3.0)

    def test_operator_retries_then_succeeds_full_success(self, monkeypatch, capsys):
        inputs = iter(["5", "3", "bad", "*"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries(max_retries=2)
        assert result == (5.0, "*", 3.0)

    def test_all_three_stages_have_one_retry_each(self, monkeypatch, capsys):
        inputs = iter(["bad", "5", "bad", "3", "bad", "+"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries(max_retries=2)
        assert result == (5.0, "+", 3.0)


class TestGetInputWithRetriesMaxRetriesCustom:
    """Tests for custom max_retries parameter."""

    def test_max_retries_one(self, monkeypatch, capsys):
        inputs = iter(["5", "3", "bad", "also_bad"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries(max_retries=1)
        assert result is None

    def test_max_retries_five_allows_more_attempts(self, monkeypatch, capsys):
        inputs = iter(["1", "2", "a", "b", "c", "d", "*"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries(max_retries=5)
        assert result == (1.0, "*", 2.0)

    def test_max_retries_zero(self, monkeypatch, capsys):
        inputs = iter(["5", "3", "+"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries(max_retries=0)
        assert result is None


class TestGetInputWithRetriesEdgeCases:
    """Edge cases for the full input collection."""

    def test_zero_operands(self, monkeypatch, capsys):
        inputs = iter(["0", "0", "+"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries()
        assert result == (0.0, "+", 0.0)

    def test_very_large_operands(self, monkeypatch, capsys):
        inputs = iter(["1e308", "1e308", "+"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries()
        assert result == (pytest.approx(1e308), "+", pytest.approx(1e308))

    def test_whitespace_in_all_inputs(self, monkeypatch, capsys):
        inputs = iter(["  5  ", "  3  ", "  +  "])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = get_input_with_retries()
        assert result == (5.0, "+", 3.0)
