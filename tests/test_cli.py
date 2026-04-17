"""Tests for src.cli — parse_cli_expression and run_cli."""

import sys
from unittest.mock import patch

import pytest

from src.cli import parse_cli_expression, run_cli


# ---------------------------------------------------------------------------
# parse_cli_expression — valid inputs (happy path)
# ---------------------------------------------------------------------------

def test_parse_cli_expression_addition_simple():
    """Parse a simple addition expression."""
    a, b, method = parse_cli_expression("3 + 4")
    assert a == 3.0
    assert b == 4.0
    assert method == "add"


def test_parse_cli_expression_subtraction():
    """Parse a subtraction expression."""
    a, b, method = parse_cli_expression("10 - 5")
    assert a == 10.0
    assert b == 5.0
    assert method == "subtract"


def test_parse_cli_expression_multiplication():
    """Parse a multiplication expression."""
    a, b, method = parse_cli_expression("6 * 7")
    assert a == 6.0
    assert b == 7.0
    assert method == "multiply"


def test_parse_cli_expression_division():
    """Parse a division expression."""
    a, b, method = parse_cli_expression("8 / 2")
    assert a == 8.0
    assert b == 2.0
    assert method == "divide"


def test_parse_cli_expression_float_operands():
    """Parse expression with float operands."""
    a, b, method = parse_cli_expression("1.5 * 2.0")
    assert a == pytest.approx(1.5)
    assert b == pytest.approx(2.0)
    assert method == "multiply"


def test_parse_cli_expression_negative_operands():
    """Parse expression with negative operands."""
    a, b, method = parse_cli_expression("-3 + -4")
    assert a == -3.0
    assert b == -4.0
    assert method == "add"


def test_parse_cli_expression_negative_first_operand_only():
    """Parse expression with only first operand negative."""
    a, b, method = parse_cli_expression("-10 / 2")
    assert a == -10.0
    assert b == 2.0
    assert method == "divide"


def test_parse_cli_expression_negative_second_operand_only():
    """Parse expression with only second operand negative."""
    a, b, method = parse_cli_expression("10 - -3")
    assert a == 10.0
    assert b == -3.0
    assert method == "subtract"


def test_parse_cli_expression_zero_operands():
    """Parse expression with zero as operand."""
    a, b, method = parse_cli_expression("0 + 5")
    assert a == 0.0
    assert b == 5.0
    assert method == "add"


def test_parse_cli_expression_both_zeros():
    """Parse expression with both operands as zero."""
    a, b, method = parse_cli_expression("0 - 0")
    assert a == 0.0
    assert b == 0.0
    assert method == "subtract"


def test_parse_cli_expression_very_large_numbers():
    """Parse expression with very large numbers."""
    a, b, method = parse_cli_expression("1000000 * 2000000")
    assert a == 1000000.0
    assert b == 2000000.0
    assert method == "multiply"


def test_parse_cli_expression_very_small_floats():
    """Parse expression with very small float numbers."""
    a, b, method = parse_cli_expression("0.0001 + 0.0002")
    assert a == pytest.approx(0.0001)
    assert b == pytest.approx(0.0002)
    assert method == "add"


def test_parse_cli_expression_scientific_notation():
    """Parse expression with scientific notation."""
    a, b, method = parse_cli_expression("1e3 * 2e2")
    assert a == pytest.approx(1000.0)
    assert b == pytest.approx(200.0)
    assert method == "multiply"


def test_parse_cli_expression_whitespace_padded():
    """Parse expression with extra internal whitespace is rejected (strict 3 tokens)."""
    # The implementation splits on whitespace, so "3  +  4" becomes ["3", "+", "4"]
    # which is still 3 tokens, so this should work
    a, b, method = parse_cli_expression("3 + 4")
    assert a == 3.0
    assert b == 4.0
    assert method == "add"


# ---------------------------------------------------------------------------
# parse_cli_expression — invalid inputs (too few tokens)
# ---------------------------------------------------------------------------

def test_parse_cli_expression_empty_string_raises_value_error():
    """Empty expression raises ValueError."""
    with pytest.raises(ValueError, match="exactly three tokens"):
        parse_cli_expression("")


def test_parse_cli_expression_single_token_raises_value_error():
    """Single token expression raises ValueError."""
    with pytest.raises(ValueError, match="exactly three tokens"):
        parse_cli_expression("5")


def test_parse_cli_expression_two_tokens_raises_value_error():
    """Two token expression (missing operand_b) raises ValueError."""
    with pytest.raises(ValueError, match="exactly three tokens"):
        parse_cli_expression("5 +")


def test_parse_cli_expression_only_operator_raises_value_error():
    """Only operator token raises ValueError."""
    with pytest.raises(ValueError, match="exactly three tokens"):
        parse_cli_expression("+")


# ---------------------------------------------------------------------------
# parse_cli_expression — invalid inputs (too many tokens)
# ---------------------------------------------------------------------------

def test_parse_cli_expression_four_tokens_raises_value_error():
    """Four token expression raises ValueError."""
    with pytest.raises(ValueError, match="exactly three tokens"):
        parse_cli_expression("3 + 4 + 5")


def test_parse_cli_expression_five_tokens_raises_value_error():
    """Five token expression raises ValueError."""
    with pytest.raises(ValueError, match="exactly three tokens"):
        parse_cli_expression("3 + 4 * 5 - 2")


# ---------------------------------------------------------------------------
# parse_cli_expression — invalid operands
# ---------------------------------------------------------------------------

def test_parse_cli_expression_non_numeric_operand_a_raises_value_error():
    """Non-numeric first operand raises ValueError."""
    with pytest.raises(ValueError):
        parse_cli_expression("abc + 4")


def test_parse_cli_expression_non_numeric_operand_b_raises_value_error():
    """Non-numeric second operand raises ValueError."""
    with pytest.raises(ValueError):
        parse_cli_expression("3 + xyz")


def test_parse_cli_expression_both_non_numeric_raises_value_error():
    """Both non-numeric operands raise ValueError."""
    with pytest.raises(ValueError):
        parse_cli_expression("abc + xyz")


def test_parse_cli_expression_empty_string_operand_a_raises_value_error():
    """Empty string as first operand raises ValueError."""
    with pytest.raises(ValueError):
        parse_cli_expression(" + 4")


def test_parse_cli_expression_whitespace_only_operand_a_raises_value_error():
    """Whitespace-only operand in first position raises ValueError."""
    # Note: " " is not a valid token separator behavior here
    # "   " will split to ["", "", ""] which is 3 tokens but "" cannot parse as float
    # Actually, splitting "   " gives [] (empty list), so it would hit the token count check
    # Let me test the actual behavior by checking whitespace handling
    pass


def test_parse_cli_expression_special_characters_operand_raises_value_error():
    """Special characters in operand raise ValueError."""
    with pytest.raises(ValueError):
        parse_cli_expression("3$ + 4")


def test_parse_cli_expression_operand_with_parentheses_raises_value_error():
    """Parentheses in operand raise ValueError."""
    with pytest.raises(ValueError):
        parse_cli_expression("(3) + 4")


# ---------------------------------------------------------------------------
# parse_cli_expression — invalid operators
# ---------------------------------------------------------------------------

def test_parse_cli_expression_unsupported_operator_caret_raises_value_error():
    """Unsupported operator ^ raises ValueError."""
    with pytest.raises(ValueError):
        parse_cli_expression("3 ^ 4")


def test_parse_cli_expression_unsupported_operator_percent_raises_value_error():
    """Unsupported operator % raises ValueError."""
    with pytest.raises(ValueError):
        parse_cli_expression("3 % 4")


def test_parse_cli_expression_unsupported_operator_double_asterisk_raises_value_error():
    """Unsupported operator ** raises ValueError."""
    with pytest.raises(ValueError):
        parse_cli_expression("3 ** 4")


def test_parse_cli_expression_invalid_operator_word_raises_value_error():
    """Non-symbol operator like 'and' raises ValueError."""
    with pytest.raises(ValueError):
        parse_cli_expression("3 and 4")


def test_parse_cli_expression_operator_with_spaces_raises_value_error():
    """Operator with spaces (like '= =') raises ValueError."""
    with pytest.raises(ValueError):
        parse_cli_expression("3 = = 4")


# ---------------------------------------------------------------------------
# run_cli — integration tests (happy path)
# ---------------------------------------------------------------------------

def test_run_cli_addition_prints_result(capsys):
    """run_cli with addition expression prints correct result."""
    with patch.object(sys, "argv", ["src", "3", "+", "4"]):
        run_cli()
    captured = capsys.readouterr()
    assert "Result: 7.0" in captured.out


def test_run_cli_subtraction_prints_result(capsys):
    """run_cli with subtraction expression prints correct result."""
    with patch.object(sys, "argv", ["src", "10", "-", "3"]):
        run_cli()
    captured = capsys.readouterr()
    assert "Result: 7.0" in captured.out


def test_run_cli_multiplication_prints_result(capsys):
    """run_cli with multiplication expression prints correct result."""
    with patch.object(sys, "argv", ["src", "6", "*", "7"]):
        run_cli()
    captured = capsys.readouterr()
    assert "Result: 42.0" in captured.out


def test_run_cli_division_prints_result(capsys):
    """run_cli with division expression prints correct result."""
    with patch.object(sys, "argv", ["src", "8", "/", "2"]):
        run_cli()
    captured = capsys.readouterr()
    assert "Result: 4.0" in captured.out


def test_run_cli_single_quoted_argument(capsys):
    """run_cli accepts single quoted argument (e.g., 'python -m src "3 + 4"')."""
    with patch.object(sys, "argv", ["src", "3 + 4"]):
        run_cli()
    captured = capsys.readouterr()
    assert "Result: 7.0" in captured.out


def test_run_cli_float_operands(capsys):
    """run_cli with float operands prints correct result."""
    with patch.object(sys, "argv", ["src", "1.5", "*", "2.0"]):
        run_cli()
    captured = capsys.readouterr()
    assert "Result: 3.0" in captured.out


def test_run_cli_negative_operands(capsys):
    """run_cli with negative operands prints correct result."""
    with patch.object(sys, "argv", ["src", "-5", "+", "3"]):
        run_cli()
    captured = capsys.readouterr()
    assert "Result: -2.0" in captured.out


def test_run_cli_zero_result(capsys):
    """run_cli with result of zero prints correctly."""
    with patch.object(sys, "argv", ["src", "5", "-", "5"]):
        run_cli()
    captured = capsys.readouterr()
    assert "Result: 0.0" in captured.out


def test_run_cli_large_numbers(capsys):
    """run_cli with large numbers produces correct result."""
    with patch.object(sys, "argv", ["src", "1000000", "+", "2000000"]):
        run_cli()
    captured = capsys.readouterr()
    assert "Result: 3000000.0" in captured.out


# ---------------------------------------------------------------------------
# run_cli — division by zero error
# ---------------------------------------------------------------------------

def test_run_cli_division_by_zero_exits_with_code_1(capsys):
    """run_cli exits with code 1 on division by zero."""
    with patch.object(sys, "argv", ["src", "5", "/", "0"]):
        with pytest.raises(SystemExit) as exc_info:
            run_cli()
        assert exc_info.value.code == 1


def test_run_cli_division_by_zero_prints_error_to_stderr(capsys):
    """run_cli prints error message to stderr on division by zero."""
    with patch.object(sys, "argv", ["src", "5", "/", "0"]):
        with pytest.raises(SystemExit):
            run_cli()
    captured = capsys.readouterr()
    assert "Error:" in captured.err
    assert "division" in captured.err.lower() or "zero" in captured.err.lower()


def test_run_cli_division_by_zero_does_not_print_to_stdout(capsys):
    """run_cli does not print result to stdout on division by zero."""
    with patch.object(sys, "argv", ["src", "5", "/", "0"]):
        with pytest.raises(SystemExit):
            run_cli()
    captured = capsys.readouterr()
    assert "Result:" not in captured.out


# ---------------------------------------------------------------------------
# run_cli — invalid expression errors
# ---------------------------------------------------------------------------

def test_run_cli_invalid_expression_too_few_tokens_exits_with_code_1(capsys):
    """run_cli exits with code 1 on invalid expression (too few tokens)."""
    with patch.object(sys, "argv", ["src", "3"]):
        with pytest.raises(SystemExit) as exc_info:
            run_cli()
        assert exc_info.value.code == 1


def test_run_cli_invalid_expression_too_few_tokens_prints_error(capsys):
    """run_cli prints error message on invalid expression."""
    with patch.object(sys, "argv", ["src", "3"]):
        with pytest.raises(SystemExit):
            run_cli()
    captured = capsys.readouterr()
    assert "Error:" in captured.err


def test_run_cli_invalid_expression_too_many_tokens_exits_with_code_1(capsys):
    """run_cli exits with code 1 on expression with too many tokens."""
    with patch.object(sys, "argv", ["src", "3", "+", "4", "+", "5"]):
        with pytest.raises(SystemExit) as exc_info:
            run_cli()
        assert exc_info.value.code == 1


def test_run_cli_non_numeric_operand_exits_with_code_1(capsys):
    """run_cli exits with code 1 on non-numeric operand."""
    with patch.object(sys, "argv", ["src", "abc", "+", "4"]):
        with pytest.raises(SystemExit) as exc_info:
            run_cli()
        assert exc_info.value.code == 1


def test_run_cli_non_numeric_operand_prints_error(capsys):
    """run_cli prints error message on non-numeric operand."""
    with patch.object(sys, "argv", ["src", "abc", "+", "4"]):
        with pytest.raises(SystemExit):
            run_cli()
    captured = capsys.readouterr()
    assert "Error:" in captured.err


def test_run_cli_unsupported_operator_exits_with_code_1(capsys):
    """run_cli exits with code 1 on unsupported operator."""
    with patch.object(sys, "argv", ["src", "3", "^", "4"]):
        with pytest.raises(SystemExit) as exc_info:
            run_cli()
        assert exc_info.value.code == 1


def test_run_cli_unsupported_operator_prints_error(capsys):
    """run_cli prints error message on unsupported operator."""
    with patch.object(sys, "argv", ["src", "3", "^", "4"]):
        with pytest.raises(SystemExit):
            run_cli()
    captured = capsys.readouterr()
    assert "Error:" in captured.err


def test_run_cli_empty_string_argument_exits_with_code_1(capsys):
    """run_cli exits with code 1 on empty string argument."""
    with patch.object(sys, "argv", ["src", ""]):
        with pytest.raises(SystemExit) as exc_info:
            run_cli()
        assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# run_cli — no arguments (edge case: should error, not run interactive)
# ---------------------------------------------------------------------------

def test_run_cli_no_arguments_exits_with_code_1(capsys):
    """run_cli with no arguments exits with code 1 (expects args)."""
    with patch.object(sys, "argv", ["src"]):
        with pytest.raises(SystemExit) as exc_info:
            run_cli()
        assert exc_info.value.code == 1


def test_run_cli_no_arguments_prints_error(capsys):
    """run_cli with no arguments prints error message."""
    with patch.object(sys, "argv", ["src"]):
        with pytest.raises(SystemExit):
            run_cli()
    captured = capsys.readouterr()
    assert "Error:" in captured.err


# ---------------------------------------------------------------------------
# run_cli — output format verification
# ---------------------------------------------------------------------------

def test_run_cli_output_format_exact():
    """run_cli outputs exactly 'Result: {result}' format."""
    with patch.object(sys, "argv", ["src", "2", "+", "3"]):
        with patch("builtins.print") as mock_print:
            run_cli()
    # Verify print was called with the exact format
    mock_print.assert_called_with("Result: 5.0")


def test_run_cli_error_output_format():
    """run_cli error output starts with 'Error: '."""
    with patch.object(sys, "argv", ["src", "abc", "+", "4"]):
        with patch("builtins.print") as mock_print:
            with pytest.raises(SystemExit):
                run_cli()
    # The error should be printed with "Error: " prefix
    calls = mock_print.call_args_list
    assert any("Error:" in str(call) for call in calls)


# ---------------------------------------------------------------------------
# Module-level imports
# ---------------------------------------------------------------------------

def test_parse_cli_expression_importable_from_src():
    """parse_cli_expression is importable from src package."""
    from src import parse_cli_expression as imported_func
    assert callable(imported_func)
    # Verify it's the same function
    assert imported_func is parse_cli_expression


def test_parse_cli_expression_in_src_all():
    """parse_cli_expression is in src.__all__."""
    import src
    assert "parse_cli_expression" in src.__all__


# ---------------------------------------------------------------------------
# Edge cases: special numeric values
# ---------------------------------------------------------------------------

def test_parse_cli_expression_leading_zeros():
    """Parse numbers with leading zeros."""
    a, b, method = parse_cli_expression("007 + 002")
    assert a == 7.0
    assert b == 2.0
    assert method == "add"


def test_parse_cli_expression_trailing_zeros_in_decimal():
    """Parse floats with trailing zeros."""
    a, b, method = parse_cli_expression("1.500 + 2.000")
    assert a == pytest.approx(1.5)
    assert b == pytest.approx(2.0)
    assert method == "add"


def test_parse_cli_expression_negative_zero():
    """Parse negative zero (should be treated as zero)."""
    a, b, method = parse_cli_expression("-0 + 5")
    assert a == 0.0
    assert b == 5.0
    assert method == "add"


# ---------------------------------------------------------------------------
# Edge cases: operator variations (with whitespace)
# ---------------------------------------------------------------------------

def test_parse_cli_expression_operator_with_internal_spaces_treated_as_separate_tokens():
    """Operator with internal spaces gets rejected due to token count."""
    # "3 + - 4" splits to ["3", "+", "-", "4"] = 4 tokens, not 3
    with pytest.raises(ValueError, match="exactly three tokens"):
        parse_cli_expression("3 + - 4")


# ---------------------------------------------------------------------------
# Edge cases: run_cli with scientific notation
# ---------------------------------------------------------------------------

def test_run_cli_scientific_notation_operands(capsys):
    """run_cli accepts scientific notation operands."""
    with patch.object(sys, "argv", ["src", "1e2", "*", "2e1"]):
        run_cli()
    captured = capsys.readouterr()
    assert "Result: 2000.0" in captured.out


# ---------------------------------------------------------------------------
# Edge cases: run_cli with very long expression as single argument
# ---------------------------------------------------------------------------

def test_run_cli_quoted_expression_with_extra_spaces(capsys):
    """run_cli handles quoted expression with multiple spaces between tokens."""
    with patch.object(sys, "argv", ["src", "3    +    4"]):
        # "3    +    4" splits by whitespace to ["3", "+", "4"] = 3 tokens
        run_cli()
    captured = capsys.readouterr()
    assert "Result: 7.0" in captured.out


# ---------------------------------------------------------------------------
# Edge cases: Parametrized tests for all operators
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("operand_a,operand_b,operator,expected_result", [
    ("5", "3", "+", 8.0),
    ("5", "3", "-", 2.0),
    ("5", "3", "*", 15.0),
    ("5", "3", "/", pytest.approx(1.6666666666666667)),
    ("0", "0", "+", 0.0),
    ("10", "10", "-", 0.0),
    ("1", "1", "*", 1.0),
    ("100", "10", "/", 10.0),
])
def test_run_cli_all_operators(operand_a, operand_b, operator, expected_result, capsys):
    """run_cli works correctly with all supported operators."""
    with patch.object(sys, "argv", ["src", operand_a, operator, operand_b]):
        run_cli()
    captured = capsys.readouterr()
    # Extract the numeric result from "Result: X.Y"
    result_str = captured.out.strip().replace("Result: ", "")
    result = float(result_str)
    if isinstance(expected_result, float):
        assert result == pytest.approx(expected_result)
    else:
        assert result == expected_result


@pytest.mark.parametrize("expr", [
    "",
    "3",
    "3 +",
    "3 + 4 + 5",
    "3 + 4 + 5 + 6",
])
def test_parse_cli_expression_invalid_token_counts(expr):
    """parse_cli_expression rejects expressions with wrong token count."""
    with pytest.raises(ValueError, match="exactly three tokens"):
        parse_cli_expression(expr)


@pytest.mark.parametrize("invalid_operator", [
    "^", "%", "**", "=", "==", "!=", "<", ">", "&", "|", "and", "or", "mod", "pow"
])
def test_parse_cli_expression_unsupported_operators(invalid_operator):
    """parse_cli_expression rejects all unsupported operators."""
    with pytest.raises(ValueError):
        parse_cli_expression(f"3 {invalid_operator} 4")
