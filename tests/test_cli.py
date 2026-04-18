"""Tests for src.cli — CLI interface for the calculator."""

import io
import sys
import pytest

from src.cli import main, build_parser


# ---------------------------------------------------------------------------
# build_parser — parser configuration
# ---------------------------------------------------------------------------

def test_build_parser_creates_parser():
    """Verify build_parser returns an ArgumentParser instance."""
    parser = build_parser()
    assert parser is not None
    assert parser.prog == "calculator"


def test_build_parser_has_three_required_positionals():
    """Verify parser expects exactly three positional arguments."""
    parser = build_parser()
    # Parse valid input and verify it succeeds
    args = parser.parse_args(["2", "+", "3"])
    assert args.operand_a == "2"
    assert args.operator == "+"
    assert args.operand_b == "3"


def test_build_parser_missing_one_argument_fails():
    """Verify parser rejects when fewer than three arguments are provided."""
    parser = build_parser()
    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["2", "+"])
    assert exc_info.value.code == 2


def test_build_parser_missing_all_arguments_fails():
    """Verify parser rejects when no arguments are provided."""
    parser = build_parser()
    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args([])
    assert exc_info.value.code == 2


def test_build_parser_extra_arguments_fails():
    """Verify parser rejects when more than three arguments are provided."""
    parser = build_parser()
    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["2", "+", "3", "extra"])
    assert exc_info.value.code == 2


def test_build_parser_help_flag_exits_zero():
    """Verify --help flag causes exit with code 0."""
    parser = build_parser()
    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["--help"])
    assert exc_info.value.code == 0


def test_build_parser_h_flag_exits_zero():
    """Verify -h flag causes exit with code 0."""
    parser = build_parser()
    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["-h"])
    assert exc_info.value.code == 0


def test_build_parser_description_mentions_calculator():
    """Verify parser description is set."""
    parser = build_parser()
    assert "calculator" in parser.description.lower()


def test_build_parser_positionals_have_help_text():
    """Verify all positional arguments have help text."""
    parser = build_parser()
    # Extract the action objects for positionals
    positional_actions = [
        action for action in parser._actions
        if action.dest in ("operand_a", "operator", "operand_b")
    ]
    assert len(positional_actions) == 3
    for action in positional_actions:
        assert action.help is not None
        assert len(action.help) > 0


# ---------------------------------------------------------------------------
# main — happy path (successful calculations)
# ---------------------------------------------------------------------------

def test_main_addition_success(capsys):
    """Verify main() successfully calculates 2 + 3."""
    main(argv=["2", "+", "3"])
    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out
    assert captured.err == ""


def test_main_subtraction_success(capsys):
    """Verify main() successfully calculates 10 - 5."""
    main(argv=["10", "-", "5"])
    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out
    assert captured.err == ""


def test_main_multiplication_success(capsys):
    """Verify main() successfully calculates 6 * 7."""
    main(argv=["6", "*", "7"])
    captured = capsys.readouterr()
    assert "Result: 42.0" in captured.out
    assert captured.err == ""


def test_main_division_success(capsys):
    """Verify main() successfully calculates 8 / 2."""
    main(argv=["8", "/", "2"])
    captured = capsys.readouterr()
    assert "Result: 4.0" in captured.out
    assert captured.err == ""


def test_main_float_operands(capsys):
    """Verify main() handles float operands correctly."""
    main(argv=["2.5", "+", "3.5"])
    captured = capsys.readouterr()
    assert "Result: 6.0" in captured.out


def test_main_negative_operands(capsys):
    """Verify main() handles negative operands correctly."""
    main(argv=["-5", "+", "-3"])
    captured = capsys.readouterr()
    assert "Result: -8.0" in captured.out


def test_main_whitespace_padded_operands(capsys):
    """Verify main() strips whitespace from operands (via parse_input)."""
    # Note: argv naturally passes strings without extra whitespace,
    # but parse_operand in input_handler.py does strip() internally
    main(argv=["  2  ", "  +  ", "  3  "])
    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out


def test_main_zero_operands(capsys):
    """Verify main() handles zero as an operand."""
    main(argv=["0", "+", "5"])
    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out


def test_main_division_result_is_float(capsys):
    """Verify division result is float even if divisible."""
    main(argv=["1", "/", "3"])
    captured = capsys.readouterr()
    # 1/3 ≈ 0.333...
    assert "Result: " in captured.out
    assert "0.333" in captured.out


# ---------------------------------------------------------------------------
# main — division by zero error (exit code 1)
# ---------------------------------------------------------------------------

def test_main_division_by_zero_writes_stderr(capsys):
    """Verify division by zero prints error to stderr."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["5", "/", "0"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err
    assert "division" in captured.err.lower() or "zero" in captured.err.lower()


def test_main_zero_divided_by_zero_exits_one(capsys):
    """Verify 0 / 0 also raises ZeroDivisionError with exit code 1."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["0", "/", "0"])
    assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# main — invalid input errors (exit code 1)
# ---------------------------------------------------------------------------

def test_main_non_numeric_operand_a_exits_one(capsys):
    """Verify non-numeric first operand causes exit 1 with error message."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["abc", "+", "3"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err
    assert "abc" in captured.err or "operand" in captured.err.lower()


def test_main_non_numeric_operand_b_exits_one(capsys):
    """Verify non-numeric second operand causes exit 1 with error message."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["3", "+", "xyz"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err


def test_main_empty_operand_a_exits_one(capsys):
    """Verify empty string as operand causes exit 1."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["", "+", "3"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err


def test_main_empty_operand_b_exits_one(capsys):
    """Verify empty string as second operand causes exit 1."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["3", "+", ""])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err


def test_main_whitespace_only_operand_a_exits_one(capsys):
    """Verify whitespace-only operand causes exit 1."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["   ", "+", "3"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err


def test_main_whitespace_only_operand_b_exits_one(capsys):
    """Verify whitespace-only second operand causes exit 1."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["3", "+", "   "])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err


def test_main_invalid_operator_exits_one(capsys):
    """Verify unsupported operator causes exit 1."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["3", "%", "4"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err
    assert "operator" in captured.err.lower() or "%" in captured.err


def test_main_power_operator_not_supported(capsys):
    """Verify ** operator is not supported."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["2", "**", "3"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err


def test_main_empty_operator_exits_one(capsys):
    """Verify empty operator string causes exit 1."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["3", "", "4"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err


def test_main_word_operator_not_supported(capsys):
    """Verify 'add' as operator string is not supported."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["3", "add", "4"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err


# ---------------------------------------------------------------------------
# main — argument parsing errors (exit code 2)
# ---------------------------------------------------------------------------

def test_main_missing_operand_b_exits_two(capsys):
    """Verify missing third argument causes exit 2 (argparse error)."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["2", "+"])
    assert exc_info.value.code == 2


def test_main_missing_operator_and_operand_b_exits_two(capsys):
    """Verify providing only operand_a causes exit 2."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["2"])
    assert exc_info.value.code == 2


def test_main_no_arguments_exits_two(capsys):
    """Verify no arguments causes exit 2."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=[])
    assert exc_info.value.code == 2


def test_main_extra_arguments_exits_two(capsys):
    """Verify extra arguments cause exit 2."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["2", "+", "3", "extra"])
    assert exc_info.value.code == 2


def test_main_extra_multiple_arguments_exits_two(capsys):
    """Verify multiple extra arguments cause exit 2."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["2", "+", "3", "extra1", "extra2"])
    assert exc_info.value.code == 2


# ---------------------------------------------------------------------------
# main — help and usage (exit code 0)
# ---------------------------------------------------------------------------

def test_main_help_flag_exits_zero(capsys):
    """Verify --help causes exit 0."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["--help"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    # Help output goes to stdout
    assert "usage:" in captured.out.lower() or "calculator" in captured.out.lower()


def test_main_h_flag_exits_zero(capsys):
    """Verify -h causes exit 0."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["-h"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "usage:" in captured.out.lower() or "calculator" in captured.out.lower()


# ---------------------------------------------------------------------------
# main — edge cases and special numeric values
# ---------------------------------------------------------------------------

def test_main_very_large_numbers(capsys):
    """Verify main handles very large numbers."""
    main(argv=["1e10", "+", "1e10"])
    captured = capsys.readouterr()
    assert "Result:" in captured.out


def test_main_very_small_float(capsys):
    """Verify main handles very small float values."""
    main(argv=["0.0001", "*", "0.0001"])
    captured = capsys.readouterr()
    assert "Result:" in captured.out


def test_main_negative_float_numbers(capsys):
    """Verify main handles negative floats."""
    main(argv=["-2.5", "-", "-1.5"])
    captured = capsys.readouterr()
    assert "Result:" in captured.out


def test_main_multiplication_by_zero(capsys):
    """Verify multiplication by zero works correctly."""
    main(argv=["100", "*", "0"])
    captured = capsys.readouterr()
    assert "Result: 0.0" in captured.out


def test_main_subtraction_resulting_in_negative(capsys):
    """Verify subtraction can produce negative results."""
    main(argv=["3", "-", "10"])
    captured = capsys.readouterr()
    assert "Result: -7.0" in captured.out


# ---------------------------------------------------------------------------
# main — error message formatting
# ---------------------------------------------------------------------------

def test_main_error_message_prefixed_with_error(capsys):
    """Verify error messages are prefixed with 'Error:'."""
    with pytest.raises(SystemExit):
        main(argv=["abc", "+", "3"])
    captured = capsys.readouterr()
    assert captured.err.startswith("Error:")


def test_main_error_goes_to_stderr_not_stdout(capsys):
    """Verify errors go to stderr, not stdout."""
    with pytest.raises(SystemExit):
        main(argv=["5", "/", "0"])
    captured = capsys.readouterr()
    assert captured.err != ""
    # The error message should not be in stdout
    assert "Error:" not in captured.out or captured.out == ""


def test_main_success_goes_to_stdout_not_stderr(capsys):
    """Verify successful output goes to stdout, not stderr."""
    main(argv=["2", "+", "3"])
    captured = capsys.readouterr()
    assert "Result:" in captured.out
    assert captured.err == ""


# ---------------------------------------------------------------------------
# main — argv parameter behavior
# ---------------------------------------------------------------------------

def test_main_with_none_argv_reads_from_sys_argv(monkeypatch, capsys):
    """Verify main(argv=None) reads from sys.argv[1:] when provided."""
    # Simulate sys.argv as if the script was called: python -m src 2 + 3
    monkeypatch.setattr(sys, "argv", ["calculator", "2", "+", "3"])
    main(argv=None)
    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out


def test_main_argv_parameter_overrides_sys_argv(monkeypatch, capsys):
    """Verify argv parameter takes precedence over sys.argv."""
    # Set sys.argv to different values
    monkeypatch.setattr(sys, "argv", ["calculator", "99", "+", "99"])
    # But call main with explicit argv
    main(argv=["2", "+", "3"])
    captured = capsys.readouterr()
    # Should use the passed argv, not sys.argv
    assert "Result: 5.0" in captured.out


# ---------------------------------------------------------------------------
# Integration-like tests (subprocess approach)
# ---------------------------------------------------------------------------

def test_main_subprocess_style_addition(capsys):
    """Test addition as if called from command line."""
    # This simulates: python -m src 10 + 20
    main(argv=["10", "+", "20"])
    captured = capsys.readouterr()
    assert "Result: 30.0" in captured.out
    assert captured.err == ""


def test_main_subprocess_style_division(capsys):
    """Test division as if called from command line."""
    # This simulates: python -m src 100 / 4
    main(argv=["100", "/", "4"])
    captured = capsys.readouterr()
    assert "Result: 25.0" in captured.out
    assert captured.err == ""


def test_main_subprocess_style_invalid_operator(capsys):
    """Test invalid operator as if called from command line."""
    # This simulates: python -m src 5 & 3
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["5", "&", "3"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err


# ---------------------------------------------------------------------------
# Parametrized tests for all valid operators
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "operand_a,operator,operand_b,expected_result",
    [
        ("5", "+", "3", "8.0"),
        ("10", "-", "4", "6.0"),
        ("6", "*", "7", "42.0"),
        ("8", "/", "2", "4.0"),
        ("1.5", "+", "2.5", "4.0"),
        ("-5", "+", "3", "-2.0"),
        ("0", "*", "100", "0.0"),
    ]
)
def test_main_valid_calculations(operand_a, operator, operand_b, expected_result, capsys):
    """Parametrized test for various valid calculations."""
    main(argv=[operand_a, operator, operand_b])
    captured = capsys.readouterr()
    assert f"Result: {expected_result}" in captured.out


@pytest.mark.parametrize(
    "operand_a,operator,operand_b",
    [
        ("abc", "+", "3"),
        ("3", "+", "xyz"),
        ("3", "%", "4"),
        ("2", "**", "3"),
        ("3", "and", "4"),
    ]
)
def test_main_invalid_inputs(operand_a, operator, operand_b, capsys):
    """Parametrized test for various invalid inputs."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=[operand_a, operator, operand_b])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err


# ---------------------------------------------------------------------------
# --history / -H flag functionality
# ---------------------------------------------------------------------------

def test_main_history_flag_long_form_displays_history(capsys):
    """Verify --history flag displays operation history."""
    main(argv=["2", "+", "3", "--history"])
    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out
    assert "History:" in captured.out
    assert "2.0 + 3.0 = 5.0" in captured.out


def test_main_history_flag_short_form_displays_history(capsys):
    """Verify -H flag displays operation history."""
    main(argv=["2", "+", "3", "-H"])
    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out
    assert "History:" in captured.out
    assert "2.0 + 3.0 = 5.0" in captured.out


def test_main_no_history_flag_no_history_output(capsys):
    """Verify without --history flag, no history is displayed."""
    main(argv=["2", "+", "3"])
    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out
    assert "History:" not in captured.out


def test_main_history_flag_with_subtraction(capsys):
    """Verify history displays subtraction operation."""
    main(argv=["10", "-", "3", "--history"])
    captured = capsys.readouterr()
    assert "Result: 7.0" in captured.out
    assert "History:" in captured.out
    assert "10.0 - 3.0 = 7.0" in captured.out


def test_main_history_flag_with_multiplication(capsys):
    """Verify history displays multiplication operation."""
    main(argv=["6", "*", "7", "--history"])
    captured = capsys.readouterr()
    assert "Result: 42.0" in captured.out
    assert "History:" in captured.out
    assert "6.0 * 7.0 = 42.0" in captured.out


def test_main_history_flag_with_division(capsys):
    """Verify history displays division operation."""
    main(argv=["8", "/", "2", "--history"])
    captured = capsys.readouterr()
    assert "Result: 4.0" in captured.out
    assert "History:" in captured.out
    assert "8.0 / 2.0 = 4.0" in captured.out


def test_main_history_flag_with_float_division_result(capsys):
    """Verify history displays float division result correctly."""
    main(argv=["1", "/", "3", "--history"])
    captured = capsys.readouterr()
    assert "Result:" in captured.out
    assert "History:" in captured.out
    assert "1.0 / 3.0" in captured.out


def test_main_history_flag_with_negative_operands(capsys):
    """Verify history displays operations with negative operands."""
    main(argv=["-5", "+", "-3", "--history"])
    captured = capsys.readouterr()
    assert "Result: -8.0" in captured.out
    assert "History:" in captured.out


def test_main_history_flag_indentation_formatting(capsys):
    """Verify history entries are indented with two spaces."""
    main(argv=["2", "+", "3", "--history"])
    captured = capsys.readouterr()
    # The history entries should be indented
    lines = captured.out.split("\n")
    history_lines = [line for line in lines if "=" in line and line.startswith("  ")]
    assert len(history_lines) >= 1


def test_main_history_flag_division_by_zero_no_history_output(capsys):
    """Verify history is not shown when division by zero occurs."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["5", "/", "0", "--history"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    # No history should be displayed on error
    assert "History:" not in captured.out


def test_main_history_flag_invalid_input_no_history_output(capsys):
    """Verify history is not shown when input is invalid."""
    with pytest.raises(SystemExit) as exc_info:
        main(argv=["abc", "+", "3", "--history"])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "History:" not in captured.out


def test_main_history_flag_with_scientific_notation(capsys):
    """Verify history displays scientific notation operands."""
    main(argv=["1e2", "+", "1e1", "--history"])
    captured = capsys.readouterr()
    assert "Result: 110.0" in captured.out
    assert "History:" in captured.out
    assert "+" in captured.out
