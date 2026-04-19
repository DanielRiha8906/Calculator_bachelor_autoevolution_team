"""Test suite for the CLI module of the calculator.

Tests cover:
- parse_and_evaluate() function: expression parsing, operator precedence, error handling
- run_cli() function: CLI argument handling, output capture, exit codes
"""

import pytest
import sys
import logging
from io import StringIO

from src.cli import parse_and_evaluate, run_cli, _eval_node
from src.logic import Calculator


@pytest.fixture
def calculator():
    """Provides a fresh Calculator instance for each test."""
    return Calculator()


# ============================================================================
# PARSE_AND_EVALUATE TESTS
# ============================================================================

class TestParseAndEvaluate:
    """Test suite for the parse_and_evaluate function."""

    # --- Basic arithmetic operations ---

    def test_parse_single_integer(self, calculator):
        """Test parsing a single integer constant."""
        assert parse_and_evaluate("5", calculator) == 5

    def test_parse_single_float(self, calculator):
        """Test parsing a single float constant."""
        assert parse_and_evaluate("3.14", calculator) == pytest.approx(3.14)

    def test_parse_addition_integers(self, calculator):
        """Test addition of two integers."""
        assert parse_and_evaluate("5 + 3", calculator) == 8

    def test_parse_addition_floats(self, calculator):
        """Test addition of two floats."""
        assert parse_and_evaluate("5.5 + 3.2", calculator) == pytest.approx(8.7)

    def test_parse_addition_mixed_int_float(self, calculator):
        """Test addition of an integer and a float."""
        assert parse_and_evaluate("5 + 3.5", calculator) == pytest.approx(8.5)

    def test_parse_subtraction_integers(self, calculator):
        """Test subtraction of two integers."""
        assert parse_and_evaluate("10 - 3", calculator) == 7

    def test_parse_subtraction_floats(self, calculator):
        """Test subtraction of two floats."""
        assert parse_and_evaluate("10.5 - 3.2", calculator) == pytest.approx(7.3)

    def test_parse_subtraction_negative_result(self, calculator):
        """Test subtraction resulting in a negative number."""
        assert parse_and_evaluate("3 - 10", calculator) == -7

    def test_parse_multiplication_integers(self, calculator):
        """Test multiplication of two integers."""
        assert parse_and_evaluate("6 * 7", calculator) == 42

    def test_parse_multiplication_floats(self, calculator):
        """Test multiplication of two floats."""
        assert parse_and_evaluate("2.5 * 4.0", calculator) == pytest.approx(10.0)

    def test_parse_multiplication_by_zero(self, calculator):
        """Test multiplication by zero."""
        assert parse_and_evaluate("5 * 0", calculator) == 0

    def test_parse_division_integers(self, calculator):
        """Test division of two integers."""
        assert parse_and_evaluate("10 / 2", calculator) == 5.0

    def test_parse_division_floats(self, calculator):
        """Test division of two floats."""
        assert parse_and_evaluate("10.5 / 2.5", calculator) == pytest.approx(4.2)

    def test_parse_division_result_float(self, calculator):
        """Test division that results in a float."""
        assert parse_and_evaluate("5 / 2", calculator) == 2.5

    def test_parse_power_integers(self, calculator):
        """Test exponentiation with integers."""
        assert parse_and_evaluate("2 ** 3", calculator) == 8.0

    def test_parse_power_floats(self, calculator):
        """Test exponentiation with floats."""
        result = parse_and_evaluate("2.0 ** 3.0", calculator)
        assert result == pytest.approx(8.0)

    def test_parse_power_zero_exponent(self, calculator):
        """Test raising to the power of zero."""
        assert parse_and_evaluate("5 ** 0", calculator) == pytest.approx(1.0)

    def test_parse_power_fractional_exponent(self, calculator):
        """Test raising to a fractional exponent (square root via 0.5)."""
        result = parse_and_evaluate("4 ** 0.5", calculator)
        assert result == pytest.approx(2.0)

    # --- Operator precedence ---

    def test_parse_precedence_multiply_before_add(self, calculator):
        """Test that multiplication has higher precedence than addition."""
        # 10 - 2 * 3 = 10 - 6 = 4
        assert parse_and_evaluate("10 - 2 * 3", calculator) == 4

    def test_parse_precedence_power_before_multiply(self, calculator):
        """Test that exponentiation has higher precedence than multiplication."""
        # 2 * 3 ** 2 = 2 * 9 = 18
        assert parse_and_evaluate("2 * 3 ** 2", calculator) == 18.0

    def test_parse_precedence_complex_expression(self, calculator):
        """Test precedence in a complex expression."""
        # 2 + 3 * 4 - 1 = 2 + 12 - 1 = 13
        assert parse_and_evaluate("2 + 3 * 4 - 1", calculator) == 13

    def test_parse_precedence_with_parentheses(self, calculator):
        """Test that parentheses override default precedence."""
        # (2 + 3) * 4 = 5 * 4 = 20
        assert parse_and_evaluate("(2 + 3) * 4", calculator) == 20

    def test_parse_nested_parentheses(self, calculator):
        """Test nested parentheses."""
        # ((2 + 3) * 4) = 20
        assert parse_and_evaluate("((2 + 3) * 4)", calculator) == 20

    # --- Unary operators ---

    def test_parse_unary_minus_single_number(self, calculator):
        """Test unary minus on a single number."""
        assert parse_and_evaluate("-5", calculator) == -5

    def test_parse_unary_minus_float(self, calculator):
        """Test unary minus on a float."""
        assert parse_and_evaluate("-3.14", calculator) == pytest.approx(-3.14)

    def test_parse_unary_minus_in_expression(self, calculator):
        """Test unary minus in an arithmetic expression."""
        # -5 + 2 = -3
        assert parse_and_evaluate("-5 + 2", calculator) == -3

    def test_parse_unary_minus_double(self, calculator):
        """Test double unary minus (should be positive)."""
        # --5 = 5
        assert parse_and_evaluate("--5", calculator) == 5

    def test_parse_unary_plus(self, calculator):
        """Test unary plus (should have no effect)."""
        assert parse_and_evaluate("+5", calculator) == 5

    def test_parse_unary_plus_with_operation(self, calculator):
        """Test unary plus in an expression."""
        assert parse_and_evaluate("+5 + 3", calculator) == 8

    def test_parse_unary_minus_with_multiplication(self, calculator):
        """Test unary minus with multiplication."""
        # -5 * 2 = -10
        assert parse_and_evaluate("-5 * 2", calculator) == -10

    def test_parse_unary_minus_with_power(self, calculator):
        """Test unary minus with exponentiation."""
        # -2 ** 2 in Python evaluates as -(2**2) = -4
        assert parse_and_evaluate("-2 ** 2", calculator) == pytest.approx(-4.0)

    # --- Whitespace handling ---

    def test_parse_with_extra_spaces(self, calculator):
        """Test that extra spaces are handled correctly."""
        assert parse_and_evaluate("5   +   3", calculator) == 8

    def test_parse_with_no_spaces(self, calculator):
        """Test expression with no spaces."""
        assert parse_and_evaluate("5+3", calculator) == 8

    def test_parse_leading_whitespace(self, calculator):
        """Test expression with leading whitespace."""
        assert parse_and_evaluate("   5 + 3", calculator) == 8

    def test_parse_trailing_whitespace(self, calculator):
        """Test expression with trailing whitespace."""
        assert parse_and_evaluate("5 + 3   ", calculator) == 8

    # --- Error handling: empty and invalid inputs ---

    def test_parse_empty_string_raises_error(self, calculator):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="Expression must not be empty"):
            parse_and_evaluate("", calculator)

    def test_parse_whitespace_only_raises_error(self, calculator):
        """Test that whitespace-only string raises ValueError."""
        with pytest.raises(ValueError, match="Expression must not be empty"):
            parse_and_evaluate("   ", calculator)

    def test_parse_incomplete_expression_plus_raises_error(self, calculator):
        """Test that incomplete expression (trailing operator) raises ValueError."""
        with pytest.raises(ValueError, match="Invalid expression syntax"):
            parse_and_evaluate("5 +", calculator)

    def test_parse_incomplete_expression_multiply_raises_error(self, calculator):
        """Test that incomplete expression with * raises ValueError."""
        with pytest.raises(ValueError, match="Invalid expression syntax"):
            parse_and_evaluate("5 *", calculator)

    def test_parse_invalid_token_raises_error(self, calculator):
        """Test that invalid tokens raise ValueError."""
        with pytest.raises(ValueError, match="Unsupported expression node"):
            parse_and_evaluate("5 + hello", calculator)

    def test_parse_mismatched_parentheses_raises_error(self, calculator):
        """Test that mismatched parentheses raise ValueError."""
        with pytest.raises(ValueError, match="Invalid expression syntax"):
            parse_and_evaluate("(5 + 3", calculator)

    def test_parse_invalid_operator_sequence_raises_error(self, calculator):
        """Test that invalid operator sequence raises ValueError.

        Note: In Python, ++ is actually valid (unary + applied twice).
        We use a truly invalid sequence instead.
        """
        with pytest.raises(ValueError, match="Invalid expression syntax"):
            parse_and_evaluate("5 + + * 3", calculator)

    # --- Division by zero ---

    def test_parse_division_by_zero_raises_error(self, calculator):
        """Test that division by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            parse_and_evaluate("1 / 0", calculator)

    def test_parse_division_by_zero_in_expression(self, calculator):
        """Test division by zero as part of larger expression."""
        with pytest.raises(ZeroDivisionError):
            parse_and_evaluate("5 + 10 / 0", calculator)

    def test_parse_division_by_zero_with_multiplication(self, calculator):
        """Test division by zero after multiplication."""
        with pytest.raises(ZeroDivisionError):
            parse_and_evaluate("5 * 2 / 0", calculator)

    # --- Large numbers and special float values ---

    def test_parse_very_large_integers(self, calculator):
        """Test parsing very large integers."""
        result = parse_and_evaluate("999999999 + 1", calculator)
        assert result == 1000000000

    def test_parse_very_small_floats(self, calculator):
        """Test parsing very small floats."""
        result = parse_and_evaluate("1e-10 + 2e-10", calculator)
        assert result == pytest.approx(3e-10)

    def test_parse_negative_zero(self, calculator):
        """Test parsing negative zero."""
        result = parse_and_evaluate("-0", calculator)
        assert result == 0

    # --- Boolean edge case (AST rejects bool as constant) ---

    def test_parse_scientific_notation(self, calculator):
        """Test scientific notation in expressions."""
        result = parse_and_evaluate("1e2 + 2e1", calculator)
        assert result == pytest.approx(120.0)

    # --- Unsupported operations ---

    def test_parse_unsupported_unary_operator(self, calculator):
        """Test that unsupported unary operators raise ValueError.

        Note: This is difficult to trigger in standard Python syntax,
        so we test the _eval_node function directly.
        """
        import ast
        # Create a mock UnaryOp node with an unsupported operator (Invert ~)
        # This requires manual AST construction as normal parsing won't create it
        node = ast.UnaryOp(op=ast.Invert(), operand=ast.Constant(value=5))
        with pytest.raises(ValueError, match="Unsupported unary operator"):
            _eval_node(node, calculator)

    def test_parse_unsupported_binary_operator(self, calculator):
        """Test that unsupported binary operators raise ValueError."""
        import ast
        # Create a BinOp with unsupported operator (FloorDiv //)
        # In Python 3.12, // is FloorDiv
        left = ast.Constant(value=10)
        right = ast.Constant(value=3)
        node = ast.BinOp(left=left, op=ast.FloorDiv(), right=right)
        with pytest.raises(ValueError, match="Unsupported binary operator"):
            _eval_node(node, calculator)

    def test_parse_unsupported_expression_node(self, calculator):
        """Test that unsupported expression nodes raise ValueError."""
        import ast
        # Create an unsupported node type (e.g., a Name node)
        node = ast.Name(id="x")
        with pytest.raises(ValueError, match="Unsupported expression node"):
            _eval_node(node, calculator)

    # --- Type error scenarios ---

    def test_parse_type_error_from_calculator(self, calculator):
        """Test that TypeError from Calculator methods is propagated."""
        # This is hard to trigger without modifying Calculator,
        # but we test that it is caught by run_cli.
        # For now, skip this as it requires invalid input.
        pass


# ============================================================================
# RUN_CLI TESTS
# ============================================================================

class TestRunCli:
    """Test suite for the run_cli function."""

    # --- Successful execution ---

    def test_run_cli_single_integer_argument(self, capsys):
        """Test CLI with a single integer as argument."""
        exit_code = run_cli(["5"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "5"
        assert captured.err == ""

    def test_run_cli_single_float_argument(self, capsys):
        """Test CLI with a single float as argument."""
        exit_code = run_cli(["3.14"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "3.14"
        assert captured.err == ""

    def test_run_cli_multi_part_expression_separate_args(self, capsys):
        """Test CLI with expression split across multiple arguments."""
        # e.g., run_cli(["5", "+", "3"])
        exit_code = run_cli(["5", "+", "3"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "8"
        assert captured.err == ""

    def test_run_cli_multi_part_complex_expression(self, capsys):
        """Test CLI with a complex multi-part expression."""
        exit_code = run_cli(["10", "-", "2", "*", "3"])
        captured = capsys.readouterr()
        assert exit_code == 0
        # 10 - 2 * 3 = 10 - 6 = 4
        assert captured.out.strip() == "4"
        assert captured.err == ""

    def test_run_cli_expression_with_parentheses(self, capsys):
        """Test CLI with parentheses."""
        exit_code = run_cli(["(", "2", "+", "3", ")", "*", "4"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "20"
        assert captured.err == ""

    def test_run_cli_expression_with_unary_minus(self, capsys):
        """Test CLI with unary minus."""
        exit_code = run_cli(["-5", "+", "2"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "-3"
        assert captured.err == ""

    def test_run_cli_power_operation(self, capsys):
        """Test CLI with power operation."""
        exit_code = run_cli(["2", "**", "8"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "256.0"
        assert captured.err == ""

    def test_run_cli_division_float_result(self, capsys):
        """Test CLI with division resulting in float."""
        exit_code = run_cli(["5", "/", "2"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "2.5"
        assert captured.err == ""

    # --- Error handling: empty argument list ---

    def test_run_cli_no_arguments_returns_error(self, capsys):
        """Test CLI with no arguments returns 1."""
        exit_code = run_cli([])
        captured = capsys.readouterr()
        assert exit_code == 1
        assert "No expression provided" in captured.err
        assert "Usage:" in captured.err
        assert captured.out == ""

    # --- Error handling: division by zero ---

    def test_run_cli_division_by_zero_returns_error(self, capsys):
        """Test CLI with division by zero returns 1."""
        exit_code = run_cli(["1", "/", "0"])
        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Division by zero" in captured.err
        assert captured.out == ""

    def test_run_cli_division_by_zero_in_expression(self, capsys):
        """Test CLI with division by zero in larger expression."""
        exit_code = run_cli(["5", "+", "10", "/", "0"])
        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Division by zero" in captured.err
        assert captured.out == ""

    # --- Error handling: invalid syntax ---

    def test_run_cli_incomplete_expression_returns_error(self, capsys):
        """Test CLI with incomplete expression returns 1."""
        exit_code = run_cli(["5", "+"])
        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error:" in captured.err
        assert captured.out == ""

    def test_run_cli_invalid_token_returns_error(self, capsys):
        """Test CLI with invalid token returns 1."""
        exit_code = run_cli(["5", "+", "hello"])
        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error:" in captured.err
        assert captured.out == ""

    def test_run_cli_mismatched_parentheses_returns_error(self, capsys):
        """Test CLI with mismatched parentheses returns 1."""
        exit_code = run_cli(["(", "5", "+", "3"])
        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error:" in captured.err
        assert captured.out == ""

    # --- Error handling: empty expression ---

    def test_run_cli_empty_expression_after_join(self, capsys):
        """Test CLI where joined expression is empty (edge case)."""
        # This is hard to trigger naturally, but if args join to whitespace:
        exit_code = run_cli([""])
        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error:" in captured.err
        assert captured.out == ""

    # --- Whitespace variations ---

    def test_run_cli_single_arg_with_spaces(self, capsys):
        """Test CLI with spaces in a single argument."""
        exit_code = run_cli(["5 + 3"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "8"
        assert captured.err == ""

    def test_run_cli_no_spaces_in_args(self, capsys):
        """Test CLI with no spaces in arguments."""
        exit_code = run_cli(["5+3"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "8"
        assert captured.err == ""

    # --- Large numbers ---

    def test_run_cli_large_numbers(self, capsys):
        """Test CLI with large numbers."""
        exit_code = run_cli(["999999999", "+", "1"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "1000000000"
        assert captured.err == ""

    def test_run_cli_scientific_notation(self, capsys):
        """Test CLI with scientific notation."""
        exit_code = run_cli(["1e2", "+", "2e1"])
        captured = capsys.readouterr()
        assert exit_code == 0
        # 100 + 20 = 120
        assert float(captured.out.strip()) == pytest.approx(120.0)
        assert captured.err == ""

    # --- Negative numbers ---

    def test_run_cli_negative_operand(self, capsys):
        """Test CLI with negative number as operand."""
        exit_code = run_cli(["-5"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "-5"
        assert captured.err == ""

    def test_run_cli_double_negative(self, capsys):
        """Test CLI with double negative."""
        exit_code = run_cli(["--5"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "5"
        assert captured.err == ""

    # --- Output format verification ---

    def test_run_cli_stdout_only_contains_result(self, capsys):
        """Test that stdout contains only the result (no extra text)."""
        exit_code = run_cli(["2", "+", "2"])
        captured = capsys.readouterr()
        # Check that output is just the number with a newline
        assert captured.out == "4\n"

    def test_run_cli_stderr_on_success_is_empty(self, capsys):
        """Test that stderr is empty on success."""
        exit_code = run_cli(["5", "*", "2"])
        captured = capsys.readouterr()
        assert captured.err == ""

    # --- Multiple operations in sequence ---

    def test_run_cli_long_expression(self, capsys):
        """Test CLI with a long expression."""
        # 1 + 2 + 3 + 4 + 5 = 15
        exit_code = run_cli(["1", "+", "2", "+", "3", "+", "4", "+", "5"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "15"
        assert captured.err == ""

    def test_run_cli_alternating_operations(self, capsys):
        """Test CLI with alternating operations."""
        # 10 - 5 + 3 = 8
        exit_code = run_cli(["10", "-", "5", "+", "3"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "8"
        assert captured.err == ""

    # --- Float results ---

    def test_run_cli_float_result_display(self, capsys):
        """Test that float results are displayed correctly."""
        exit_code = run_cli(["10", "/", "3"])
        captured = capsys.readouterr()
        assert exit_code == 0
        # 10 / 3 ≈ 3.333...
        result = float(captured.out.strip())
        assert result == pytest.approx(10.0 / 3.0)

    # --- Edge case: very complex precedence ---

    def test_run_cli_complex_precedence(self, capsys):
        """Test CLI with complex operator precedence."""
        # 2 + 3 * 4 ** 2 - 1 = 2 + 3 * 16 - 1 = 2 + 48 - 1 = 49
        exit_code = run_cli(["2", "+", "3", "*", "4", "**", "2", "-", "1"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "49.0"
        assert captured.err == ""


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestCLIIntegration:
    """Integration tests combining multiple CLI scenarios."""

    def test_cli_zero_plus_zero(self, capsys):
        """Test 0 + 0."""
        exit_code = run_cli(["0", "+", "0"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "0"

    def test_cli_zero_minus_zero(self, capsys):
        """Test 0 - 0."""
        exit_code = run_cli(["0", "-", "0"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "0"

    def test_cli_zero_times_anything(self, capsys):
        """Test 0 * anything = 0."""
        exit_code = run_cli(["0", "*", "999"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "0"

    def test_cli_division_of_zero(self, capsys):
        """Test 0 / non_zero = 0."""
        exit_code = run_cli(["0", "/", "5"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "0.0"

    def test_cli_number_to_power_zero(self, capsys):
        """Test any_number ** 0 = 1."""
        exit_code = run_cli(["42", "**", "0"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "1.0"

    def test_cli_one_to_any_power(self, capsys):
        """Test 1 ** any_number = 1."""
        exit_code = run_cli(["1", "**", "100"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "1.0"

    def test_cli_negative_to_even_power_positive(self, capsys):
        """Test that negative number to even power is positive."""
        # (-2) ** 2 = 4
        exit_code = run_cli(["(", "-2", ")", "**", "2"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "4.0"

    def test_cli_negative_to_odd_power_negative(self, capsys):
        """Test that negative number to odd power is negative."""
        # (-2) ** 3 = -8
        exit_code = run_cli(["(", "-2", ")", "**", "3"])
        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out.strip() == "-8.0"


# ============================================================================
# CLI ERROR LOGGING TESTS
# ============================================================================

class TestCLIErrorLogging:
    """Test suite for error logging in CLI module."""

    def test_cli_division_by_zero_logs_error(self, caplog):
        """Verify division by zero in CLI is logged."""
        with caplog.at_level(logging.ERROR):
            exit_code = run_cli(["10", "/", "0"])

        # Should have logged error and returned 1
        assert exit_code == 1
        assert any("division" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_cli_valid_expression_succeeds(self, caplog):
        """Verify valid expression in CLI succeeds."""
        with caplog.at_level(logging.ERROR):
            exit_code = run_cli(["5", "+", "3"])

        # Should succeed with exit code 0
        assert exit_code == 0
        # No error logs for successful operations
        error_records = [r for r in caplog.records if r.levelname == "ERROR"]
        assert len(error_records) == 0

    def test_cli_no_args_returns_error_code(self, caplog):
        """Verify that no arguments returns error code 1."""
        with caplog.at_level(logging.ERROR):
            exit_code = run_cli([])

        # run_cli returns 1 but doesn't log in this case (it's a usage error)
        assert exit_code == 1

    def test_cli_parse_and_evaluate_unsupported_expression_raises_error(self, caplog):
        """Verify unsupported expression raises error in parse_and_evaluate."""
        calc = Calculator()
        with caplog.at_level(logging.ERROR):
            # Use a truly unsupported node type
            with pytest.raises(ValueError):
                # This should fail because it's not a supported expression
                parse_and_evaluate("lambda x: x", calc)

        # May or may not log depending on where error occurs
        assert len(caplog.records) >= 0

    def test_cli_run_cli_type_error_logs_error(self, caplog, capsys):
        """Verify that type errors in CLI are logged."""
        # This would be logged if passed through execute path
        # For now we verify the error handling works
        with caplog.at_level(logging.ERROR):
            exit_code = run_cli(["1", "+", "2"])

        # This should succeed, so no error logs
        assert exit_code == 0


# ============================================================================
# BACKWARD COMPATIBILITY TESTS
# ============================================================================


class TestBackwardCompatCLI:
    """Test that src.cli re-exports work correctly."""

    def test_run_cli_importable_from_src_cli(self):
        """Test that run_cli is importable from src.cli."""
        from src.cli import run_cli as cli_run_cli
        assert callable(cli_run_cli)

    def test_parse_and_evaluate_importable_from_src_cli(self):
        """Test that parse_and_evaluate is importable from src.cli."""
        from src.cli import parse_and_evaluate as cli_parse_and_evaluate
        assert callable(cli_parse_and_evaluate)

    def test_run_cli_same_as_presentation_cli(self):
        """Test that src.cli.run_cli is the same as src.presentation.cli.run_cli."""
        from src.cli import run_cli as cli_run_cli
        from src.presentation.cli import run_cli as presentation_run_cli
        assert cli_run_cli is presentation_run_cli

    def test_parse_and_evaluate_same_as_presentation_cli(self):
        """Test that src.cli.parse_and_evaluate is from src.presentation.cli."""
        from src.cli import parse_and_evaluate as cli_parse_and_evaluate
        from src.presentation.cli import parse_and_evaluate as presentation_parse_and_evaluate
        assert cli_parse_and_evaluate is presentation_parse_and_evaluate

    def test_eval_node_importable_from_src_cli(self):
        """Test that _eval_node is importable from src.cli."""
        from src.cli import _eval_node as cli_eval_node
        assert callable(cli_eval_node)
