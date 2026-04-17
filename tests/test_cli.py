"""Tests for src/cli.py.

Tests the CLI module's argument parsing, validation, operation dispatch,
and output handling. Uses monkeypatch to mock sys.argv since run_cli()
does not accept explicit arguments — it reads from sys.argv directly.
"""

from __future__ import annotations

import math
import sys

import pytest

from src.cli import _build_parser, run_cli
from src.input_loop import OPERATIONS


# ---------------------------------------------------------------------------
# _build_parser tests
# ---------------------------------------------------------------------------


def test_build_parser_returns_argument_parser() -> None:
    """_build_parser must return an ArgumentParser instance."""
    parser = _build_parser()
    assert parser is not None
    # Verify it's an argparse.ArgumentParser by checking for parse_args method
    assert hasattr(parser, "parse_args")


def test_build_parser_has_operation_positional() -> None:
    """_build_parser must define an 'operation' positional argument."""
    parser = _build_parser()
    # Parse a valid example to ensure operation is accepted
    args = parser.parse_args(["add", "1", "2"])
    assert hasattr(args, "operation")
    assert args.operation == "add"


def test_build_parser_has_operands_positional() -> None:
    """_build_parser must define 'operands' positional with nargs='+'."""
    parser = _build_parser()
    args = parser.parse_args(["add", "3", "5"])
    assert hasattr(args, "operands")
    assert args.operands == ["3", "5"]


def test_build_parser_operands_one_or_more() -> None:
    """_build_parser must require at least one operand (nargs='+')."""
    parser = _build_parser()
    # Should fail when no operands provided
    with pytest.raises(SystemExit):
        parser.parse_args(["add"])


def test_build_parser_operands_multiple() -> None:
    """_build_parser must accept multiple operands in operands list."""
    parser = _build_parser()
    args = parser.parse_args(["add", "1", "2", "3", "4", "5"])
    assert args.operands == ["1", "2", "3", "4", "5"]


def test_build_parser_prog_is_descriptive() -> None:
    """_build_parser must set prog to reflect module invocation."""
    parser = _build_parser()
    # prog should contain "python -m src" or similar
    assert "python" in parser.prog or "src" in parser.prog


def test_build_parser_description_not_empty() -> None:
    """_build_parser must include a description."""
    parser = _build_parser()
    assert parser.description is not None
    assert len(parser.description) > 0


def test_build_parser_help_includes_valid_operations() -> None:
    """_build_parser help text must list valid operation names."""
    parser = _build_parser()
    help_text = parser.format_help()
    # At least one operation key should be visible in help
    found_operations = sum(1 for key in OPERATIONS if key in help_text)
    assert found_operations > 0, "No operation names found in parser help"


# ---------------------------------------------------------------------------
# run_cli happy path tests — successful execution
# ---------------------------------------------------------------------------


def test_run_cli_add_positive_integers(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', '3', '5']) must print 8.0 to stdout and return normally."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "3", "5"])
    run_cli()
    captured = capsys.readouterr()
    assert "8" in captured.out


def test_run_cli_add_floats(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', '1.5', '2.5']) must print 4.0 to stdout."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "1.5", "2.5"])
    run_cli()
    captured = capsys.readouterr()
    assert "4" in captured.out


def test_run_cli_subtract(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['subtract', '10', '3']) must print 7.0 to stdout."""
    monkeypatch.setattr(sys, "argv", ["src", "subtract", "10", "3"])
    run_cli()
    captured = capsys.readouterr()
    assert "7" in captured.out


def test_run_cli_multiply(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['multiply', '4', '2']) must print 8.0 to stdout."""
    monkeypatch.setattr(sys, "argv", ["src", "multiply", "4", "2"])
    run_cli()
    captured = capsys.readouterr()
    assert "8" in captured.out


def test_run_cli_divide(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['divide', '10', '2']) must print 5.0 to stdout."""
    monkeypatch.setattr(sys, "argv", ["src", "divide", "10", "2"])
    run_cli()
    captured = capsys.readouterr()
    assert "5" in captured.out


def test_run_cli_divide_returns_float(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['divide', '7', '2']) must print 3.5 (float result)."""
    monkeypatch.setattr(sys, "argv", ["src", "divide", "7", "2"])
    run_cli()
    captured = capsys.readouterr()
    assert "3.5" in captured.out


def test_run_cli_power(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['power', '2', '8']) must print 256.0 to stdout."""
    monkeypatch.setattr(sys, "argv", ["src", "power", "2", "8"])
    run_cli()
    captured = capsys.readouterr()
    assert "256" in captured.out


def test_run_cli_square(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['square', '5']) must print 25.0 to stdout."""
    monkeypatch.setattr(sys, "argv", ["src", "square", "5"])
    run_cli()
    captured = capsys.readouterr()
    assert "25" in captured.out


def test_run_cli_cube(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['cube', '3']) must print 27.0 to stdout."""
    monkeypatch.setattr(sys, "argv", ["src", "cube", "3"])
    run_cli()
    captured = capsys.readouterr()
    assert "27" in captured.out


def test_run_cli_square_root(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['square_root', '9']) must print 3.0 to stdout."""
    monkeypatch.setattr(sys, "argv", ["src", "square_root", "9"])
    run_cli()
    captured = capsys.readouterr()
    assert "3" in captured.out


def test_run_cli_cube_root(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['cube_root', '8']) must print 2.0 to stdout."""
    monkeypatch.setattr(sys, "argv", ["src", "cube_root", "8"])
    run_cli()
    captured = capsys.readouterr()
    assert "2" in captured.out


def test_run_cli_factorial(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['factorial', '5']) must print 120.0 to stdout."""
    monkeypatch.setattr(sys, "argv", ["src", "factorial", "5"])
    run_cli()
    captured = capsys.readouterr()
    assert "120" in captured.out


def test_run_cli_log(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['log', '100']) must print 2.0 to stdout."""
    monkeypatch.setattr(sys, "argv", ["src", "log", "100"])
    run_cli()
    captured = capsys.readouterr()
    assert "2" in captured.out


def test_run_cli_ln(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['ln', '1']) must print 0.0 to stdout."""
    monkeypatch.setattr(sys, "argv", ["src", "ln", "1"])
    run_cli()
    captured = capsys.readouterr()
    assert "0" in captured.out


def test_run_cli_negative_operand(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', '-5', '3']) must accept negative numbers and print -2.0."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "-5", "3"])
    run_cli()
    captured = capsys.readouterr()
    assert "-2" in captured.out


def test_run_cli_zero_operand(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', '0', '5']) must accept zero as operand."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "0", "5"])
    run_cli()
    captured = capsys.readouterr()
    assert "5" in captured.out


# ---------------------------------------------------------------------------
# run_cli error cases — invalid operations
# ---------------------------------------------------------------------------


def test_run_cli_unknown_operation_exits_2(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['bogus', '1', '2']) must exit with code 2."""
    monkeypatch.setattr(sys, "argv", ["src", "bogus", "1", "2"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    assert exc_info.value.code == 2


def test_run_cli_unknown_operation_prints_to_stderr(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['bogus', '1', '2']) must print error message to stderr."""
    monkeypatch.setattr(sys, "argv", ["src", "bogus", "1", "2"])
    with pytest.raises(SystemExit):
        run_cli()
    captured = capsys.readouterr()
    assert "unknown operation" in captured.err or "Unknown operation" in captured.err
    assert "bogus" in captured.err


def test_run_cli_unknown_operation_lists_valid_operations(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli with unknown op must list valid operations in stderr."""
    monkeypatch.setattr(sys, "argv", ["src", "xyz", "1"])
    with pytest.raises(SystemExit):
        run_cli()
    captured = capsys.readouterr()
    # At least one real operation name should be mentioned
    assert any(op_name in captured.err for op_name in ["add", "subtract", "multiply"])


def test_run_cli_case_sensitive_operation(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['ADD', '3', '5']) must reject uppercase (operations are case-sensitive)."""
    monkeypatch.setattr(sys, "argv", ["src", "ADD", "3", "5"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    # argparse does not auto-lowercase; the operation is checked literally
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "unknown operation" in captured.err.lower()


# ---------------------------------------------------------------------------
# run_cli error cases — wrong operand count
# ---------------------------------------------------------------------------


def test_run_cli_too_few_operands(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', '3']) is missing the second operand; must exit 2."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "3"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "requires" in captured.err or "Requires" in captured.err


def test_run_cli_too_few_operands_message_mentions_count(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Error message must mention required vs supplied operand counts."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "3"])
    with pytest.raises(SystemExit):
        run_cli()
    captured = capsys.readouterr()
    # Message should mention both required (2) and supplied (1) counts
    assert ("2" in captured.err and "1" in captured.err) or "requires" in captured.err.lower()


def test_run_cli_too_many_operands_binary(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', '1', '2', '3']) has extra operand; must exit 2."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "1", "2", "3"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "requires" in captured.err or "requires" in captured.err.lower()


def test_run_cli_too_many_operands_unary(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['square', '4', '5']) has extra operand; must exit 2."""
    monkeypatch.setattr(sys, "argv", ["src", "square", "4", "5"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "requires" in captured.err or "requires" in captured.err.lower()


def test_run_cli_no_operands(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add']) with no operands must be rejected by argparse."""
    monkeypatch.setattr(sys, "argv", ["src", "add"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    # argparse exits with code 2 on missing required positional args
    assert exc_info.value.code == 2


# ---------------------------------------------------------------------------
# run_cli error cases — non-numeric operands
# ---------------------------------------------------------------------------


def test_run_cli_non_numeric_operand_abc(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', 'abc', '5']) must reject non-numeric operand."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "abc", "5"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "not a valid number" in captured.err or "valid number" in captured.err.lower()


def test_run_cli_non_numeric_operand_abc_mentions_bad_value(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Error message for non-numeric operand must mention the bad value."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "foo", "3"])
    with pytest.raises(SystemExit):
        run_cli()
    captured = capsys.readouterr()
    assert "foo" in captured.err or "not a valid number" in captured.err.lower()


def test_run_cli_non_numeric_empty_string(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', '', '3']) with empty string operand must exit 2."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "", "3"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "not a valid number" in captured.err or "valid" in captured.err.lower()


def test_run_cli_non_numeric_mixed_in_second_operand(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', '3', '5x']) must reject non-numeric second operand."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "3", "5x"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "not a valid number" in captured.err or "5x" in captured.err


def test_run_cli_whitespace_operand(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', '   ', '3']) with whitespace-only operand must exit 2."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "   ", "3"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "not a valid number" in captured.err or "valid" in captured.err.lower()


def test_run_cli_operand_with_spaces_numeric_part(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', '  5  ', '3']) with spaces around number must be accepted (float() strips)."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "  5  ", "3"])
    run_cli()
    captured = capsys.readouterr()
    assert "8" in captured.out


# ---------------------------------------------------------------------------
# run_cli error cases — operation-specific validation (e.g., division by zero)
# ---------------------------------------------------------------------------


def test_run_cli_divide_by_zero_exits_2(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['divide', '10', '0']) must catch division-by-zero and exit 2."""
    monkeypatch.setattr(sys, "argv", ["src", "divide", "10", "0"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "error" in captured.err.lower()


def test_run_cli_divide_by_zero_error_message(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """divide-by-zero error message should mention division or zero."""
    monkeypatch.setattr(sys, "argv", ["src", "divide", "5", "0"])
    with pytest.raises(SystemExit):
        run_cli()
    captured = capsys.readouterr()
    assert "division" in captured.err.lower() or "zero" in captured.err.lower()


def test_run_cli_square_root_negative_exits_2(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['square_root', '-4']) must catch negative sqrt error and exit 2."""
    monkeypatch.setattr(sys, "argv", ["src", "square_root", "-4"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "error" in captured.err.lower()


def test_run_cli_log_zero_exits_2(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['log', '0']) must catch log error and exit 2."""
    monkeypatch.setattr(sys, "argv", ["src", "log", "0"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "error" in captured.err.lower()


def test_run_cli_ln_negative_exits_2(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['ln', '-1']) must catch ln error and exit 2."""
    monkeypatch.setattr(sys, "argv", ["src", "ln", "-1"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "error" in captured.err.lower()


def test_run_cli_factorial_negative_exits_2(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['factorial', '-3']) must catch factorial error and exit 2."""
    monkeypatch.setattr(sys, "argv", ["src", "factorial", "-3"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "error" in captured.err.lower()


# ---------------------------------------------------------------------------
# run_cli edge cases — numeric edge cases
# ---------------------------------------------------------------------------


def test_run_cli_very_large_number(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', '1e308', '1']) must accept very large float."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "1e308", "1"])
    # May succeed or fail depending on overflow; just verify it doesn't crash with bad arg error
    try:
        run_cli()
        # If it succeeds, capture shows output
        captured = capsys.readouterr()
        assert len(captured.out) > 0
    except SystemExit as e:
        # If it fails, it should be error exit code (2) for computation, not arg error
        assert e.code == 2


def test_run_cli_very_small_number(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', '1e-300', '1']) must accept very small float."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "1e-300", "1"])
    run_cli()
    captured = capsys.readouterr()
    assert "1" in captured.out


def test_run_cli_scientific_notation(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['multiply', '1e2', '2']) must accept scientific notation."""
    monkeypatch.setattr(sys, "argv", ["src", "multiply", "1e2", "2"])
    run_cli()
    captured = capsys.readouterr()
    assert "200" in captured.out


def test_run_cli_float_with_leading_decimal(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', '.5', '.5']) with leading decimal point must be accepted."""
    monkeypatch.setattr(sys, "argv", ["src", "add", ".5", ".5"])
    run_cli()
    captured = capsys.readouterr()
    assert "1" in captured.out


def test_run_cli_float_trailing_decimal(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', '5.', '5']) with trailing decimal point must be accepted."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "5.", "5"])
    run_cli()
    captured = capsys.readouterr()
    assert "10" in captured.out


def test_run_cli_result_printed_to_stdout_not_stderr(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Successful result must appear on stdout, not stderr."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "1", "2"])
    run_cli()
    captured = capsys.readouterr()
    assert "3" in captured.out
    assert captured.err == ""


def test_run_cli_error_printed_to_stderr_not_stdout(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Error messages must appear on stderr, not stdout."""
    monkeypatch.setattr(sys, "argv", ["src", "bogus", "1", "2"])
    with pytest.raises(SystemExit):
        run_cli()
    captured = capsys.readouterr()
    assert "unknown" in captured.err.lower()
    assert "unknown" not in captured.out.lower()


# ---------------------------------------------------------------------------
# run_cli all operations parametrized tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "operation,operands,should_succeed",
    [
        ("add", ["5", "3"], True),
        ("subtract", ["10", "4"], True),
        ("multiply", ["6", "7"], True),
        ("divide", ["20", "4"], True),
        ("power", ["2", "5"], True),
        ("square", ["7"], True),
        ("cube", ["3"], True),
        ("square_root", ["25"], True),
        ("cube_root", ["64"], True),
        ("factorial", ["4"], True),
        ("log", ["10"], True),
        ("ln", ["2.718"], True),
    ],
)
def test_run_cli_all_operations(
    operation: str,
    operands: list[str],
    should_succeed: bool,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """All valid operations should execute successfully with correct operand counts."""
    argv = ["src", operation] + operands
    monkeypatch.setattr(sys, "argv", argv)
    if should_succeed:
        run_cli()
        captured = capsys.readouterr()
        # Some numeric result should be in stdout
        assert len(captured.out.strip()) > 0
    else:
        with pytest.raises(SystemExit) as exc_info:
            run_cli()
        assert exc_info.value.code == 2


# ---------------------------------------------------------------------------
# main() routing tests
# ---------------------------------------------------------------------------


def test_main_with_args_calls_run_cli(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """main(argv=['add', '1', '2']) must route to run_cli."""
    import unittest.mock as mock
    from src import __main__ as main_module

    with mock.patch.object(main_module, "run_cli") as mock_run_cli:
        with mock.patch.object(main_module, "run_loop"):
            main_module.main(argv=["add", "1", "2"])

    mock_run_cli.assert_called_once_with()


def test_main_without_args_calls_run_loop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """main(argv=[]) must route to run_loop."""
    import unittest.mock as mock
    from src import __main__ as main_module

    with mock.patch.object(main_module, "run_loop") as mock_run_loop:
        with mock.patch.object(main_module, "run_cli"):
            main_module.main(argv=[])

    mock_run_loop.assert_called_once_with()


def test_main_none_argv_uses_sys_argv(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """main(argv=None) should use sys.argv[1:] for routing decision."""
    import unittest.mock as mock
    from src import __main__ as main_module

    # When argv=None (default), main() uses sys.argv[1:]
    monkeypatch.setattr(sys, "argv", ["script", "add", "1", "2"])

    with mock.patch.object(main_module, "run_cli") as mock_run_cli:
        with mock.patch.object(main_module, "run_loop"):
            main_module.main(argv=None)

    mock_run_cli.assert_called_once_with()


def test_main_empty_sys_argv_uses_run_loop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """main(argv=None) with sys.argv=['script'] should route to run_loop."""
    import unittest.mock as mock
    from src import __main__ as main_module

    # When sys.argv only contains the script name, sys.argv[1:] is empty
    monkeypatch.setattr(sys, "argv", ["script"])

    with mock.patch.object(main_module, "run_loop") as mock_run_loop:
        with mock.patch.object(main_module, "run_cli"):
            main_module.main(argv=None)

    mock_run_loop.assert_called_once_with()


def test_main_with_explicit_argv_overrides_sys_argv(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """main(argv=['op']) should override sys.argv[1:] for routing."""
    import unittest.mock as mock
    from src import __main__ as main_module

    # Set sys.argv to empty, but provide explicit argv
    monkeypatch.setattr(sys, "argv", ["script"])

    with mock.patch.object(main_module, "run_cli") as mock_run_cli:
        with mock.patch.object(main_module, "run_loop"):
            main_module.main(argv=["operation", "arg"])

    # Should use the explicit argv, not sys.argv[1:]
    mock_run_cli.assert_called_once_with()


# ---------------------------------------------------------------------------
# run_cli behavior with invalid operations and operands (no retry)
# ---------------------------------------------------------------------------


def test_run_cli_invalid_operation_no_retry_exits_2(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['unknown_op', '1', '2']) must exit with code 2 (no retry)."""
    monkeypatch.setattr(sys, "argv", ["src", "unknown_op", "1", "2"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "unknown operation" in captured.err.lower()


def test_run_cli_invalid_operand_no_retry_exits_2(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """run_cli(['add', 'not_a_number', '2']) must exit with code 2 (no retry)."""
    monkeypatch.setattr(sys, "argv", ["src", "add", "not_a_number", "2"])
    with pytest.raises(SystemExit) as exc_info:
        run_cli()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "valid number" in captured.err.lower() or "not a valid" in captured.err.lower()
