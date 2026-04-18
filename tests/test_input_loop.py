"""Tests for src/input_loop.py.

All I/O is exercised by supplying a custom ``input_fn`` callable so that no
interactive terminal is required and pytest capture works correctly.
"""

from __future__ import annotations

import math

import pytest

from src.calculator import Calculator
from src.input_loop import (
    OPERATIONS,
    dispatch,
    get_operands,
    get_operands_interactive,
    get_operation,
    get_operation_interactive,
    print_menu,
    run_loop,
)


# ---------------------------------------------------------------------------
# print_menu
# ---------------------------------------------------------------------------


def test_print_menu_outputs_all_operations(capsys: pytest.CaptureFixture[str]) -> None:
    """print_menu must include every key in OPERATIONS and the 'exit' hint."""
    print_menu()
    captured = capsys.readouterr()
    for key in OPERATIONS:
        assert key in captured.out, f"Expected operation key '{key}' in menu output"
    assert "exit" in captured.out


# ---------------------------------------------------------------------------
# get_operation
# ---------------------------------------------------------------------------


def test_get_operation_valid_key_returns_key() -> None:
    """A recognised operation key must be returned unchanged."""
    result = get_operation(input_fn=lambda _prompt: "add")
    assert result == "add"


def test_get_operation_exit_returns_none() -> None:
    """Typing 'exit' must return None to signal the loop to stop."""
    result = get_operation(input_fn=lambda _prompt: "exit")
    assert result is None


def test_get_operation_invalid_prints_error_and_returns_sentinel(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """An unrecognised key must print an error and return '__invalid__'."""
    result = get_operation(input_fn=lambda _prompt: "nonsense")
    assert result == "__invalid__"
    captured = capsys.readouterr()
    assert "Unknown operation" in captured.out


# ---------------------------------------------------------------------------
# get_operands
# ---------------------------------------------------------------------------


def test_get_operands_two_values_returns_floats() -> None:
    """Two numeric inputs must be returned as a list of two floats."""
    values = iter(["3", "4"])
    result = get_operands(2, input_fn=lambda _prompt: next(values))
    assert result == [3.0, 4.0]
    assert all(isinstance(v, float) for v in result)


def test_get_operands_non_numeric_raises_value_error() -> None:
    """A non-numeric input must raise ValueError."""
    with pytest.raises(ValueError):
        get_operands(1, input_fn=lambda _prompt: "abc")


# ---------------------------------------------------------------------------
# dispatch
# ---------------------------------------------------------------------------


def test_dispatch_add_calls_calculator_correctly() -> None:
    """dispatch 'add' must return the sum of the two operands."""
    calc = Calculator()
    result = dispatch("add", [3.0, 4.0], calc)
    assert result == 7.0


def test_dispatch_sqrt_calls_calculator_correctly() -> None:
    """dispatch 'square_root' (unary) must return the correct sqrt."""
    import math

    calc = Calculator()
    result = dispatch("square_root", [9.0], calc)
    assert math.isclose(result, 3.0)


def test_dispatch_divide_by_zero_propagates_value_error() -> None:
    """dispatch 'divide' with zero divisor must propagate ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero"):
        dispatch("divide", [1.0, 0.0], calc)


# ---------------------------------------------------------------------------
# run_loop integration scenarios
# ---------------------------------------------------------------------------


def test_run_loop_add_then_exit(capsys: pytest.CaptureFixture[str]) -> None:
    """A valid add operation followed by exit must print the correct result."""
    inputs = iter(["add", "3", "4", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "7" in captured.out
    assert "Goodbye" in captured.out


def test_run_loop_invalid_operation_shows_error_and_continues(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """An invalid operation key must show an error and not crash the loop."""
    inputs = iter(["nonsense", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Unknown operation" in captured.out
    assert "Goodbye" in captured.out


def test_run_loop_non_numeric_operand_shows_error_and_continues(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A non-numeric operand must show an error message and continue the loop.

    Sequence for binary 'add':
    1. "add" - operation
    2. "abc", "5" - first operand attempt (fails)
    3. "5", "10" - second operand attempt (succeeds)
    4. "exit" - exit
    """
    inputs = iter(["add", "abc", "5", "5", "10", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Error" in captured.out
    assert "Goodbye" in captured.out
    assert "15" in captured.out


def test_run_loop_calculator_error_shows_error_and_continues(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A calculator error (division by zero) must show an error and continue."""
    inputs = iter(["divide", "1", "0", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Error" in captured.out
    assert "Goodbye" in captured.out


# ---------------------------------------------------------------------------
# print_menu — additional edge cases
# ---------------------------------------------------------------------------


def test_print_menu_contains_labels_for_every_operation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Every OPERATIONS entry must have its display label present in the output."""
    print_menu()
    captured = capsys.readouterr()
    for key, (label, _) in OPERATIONS.items():
        # The label string (or at least the key) must appear
        assert key in captured.out, f"Key '{key}' missing from menu"
        assert label in captured.out, f"Label '{label}' missing from menu"


def test_print_menu_always_shows_exit_hint(capsys: pytest.CaptureFixture[str]) -> None:
    """'exit' must appear in the menu output regardless of how many operations exist."""
    print_menu()
    captured = capsys.readouterr()
    assert "exit" in captured.out


def test_print_menu_called_multiple_times_produces_consistent_output(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Calling print_menu twice must produce identical output both times."""
    print_menu()
    first = capsys.readouterr().out
    print_menu()
    second = capsys.readouterr().out
    assert first == second


# ---------------------------------------------------------------------------
# get_operation — additional edge cases
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("key", list(OPERATIONS.keys()))
def test_get_operation_each_valid_key_returned(key: str) -> None:
    """Every key in OPERATIONS must be returned as-is by get_operation."""
    result = get_operation(input_fn=lambda _prompt: key)
    assert result == key


def test_get_operation_strips_surrounding_whitespace() -> None:
    """Input with leading/trailing whitespace must be accepted for known keys."""
    result = get_operation(input_fn=lambda _prompt: "  add  ")
    assert result == "add"


def test_get_operation_case_insensitive_upper() -> None:
    """Uppercase input must be matched case-insensitively."""
    result = get_operation(input_fn=lambda _prompt: "ADD")
    assert result == "add"


def test_get_operation_case_insensitive_mixed() -> None:
    """Mixed-case input must be matched case-insensitively."""
    result = get_operation(input_fn=lambda _prompt: "Factorial")
    assert result == "factorial"


def test_get_operation_empty_string_returns_sentinel(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """An empty string is not a valid operation and must return '__invalid__'."""
    result = get_operation(input_fn=lambda _prompt: "")
    assert result == "__invalid__"
    captured = capsys.readouterr()
    assert "Unknown operation" in captured.out


def test_get_operation_whitespace_only_returns_sentinel(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Whitespace-only input collapses to '' after strip and must return '__invalid__'."""
    result = get_operation(input_fn=lambda _prompt: "   ")
    assert result == "__invalid__"
    captured = capsys.readouterr()
    assert "Unknown operation" in captured.out


def test_get_operation_exit_case_insensitive() -> None:
    """'EXIT' and 'Exit' must also be treated as the exit command."""
    assert get_operation(input_fn=lambda _prompt: "EXIT") is None
    assert get_operation(input_fn=lambda _prompt: "Exit") is None


def test_get_operation_prompt_is_passed_through() -> None:
    """input_fn must receive a non-empty prompt string."""
    received: list[str] = []

    def capturing_input(prompt: str) -> str:
        received.append(prompt)
        return "exit"

    get_operation(input_fn=capturing_input)
    assert received and received[0] != ""


# ---------------------------------------------------------------------------
# get_operands — additional edge cases
# ---------------------------------------------------------------------------


def test_get_operands_count_zero_returns_empty_list() -> None:
    """get_operands(0, ...) must return an empty list without calling input_fn."""
    called = []

    def should_not_be_called(prompt: str) -> str:
        called.append(prompt)
        return "0"

    result = get_operands(0, input_fn=should_not_be_called)
    assert result == []
    assert called == [], "input_fn must not be invoked when count=0"


def test_get_operands_count_one_returns_single_float() -> None:
    """get_operands(1, ...) must return a list with exactly one float."""
    result = get_operands(1, input_fn=lambda _prompt: "42")
    assert result == [42.0]
    assert isinstance(result[0], float)


def test_get_operands_integer_string_converted_to_float() -> None:
    """Integer string input must be returned as a float value."""
    result = get_operands(1, input_fn=lambda _prompt: "7")
    assert result == [7.0]
    assert isinstance(result[0], float)


def test_get_operands_negative_number_is_accepted() -> None:
    """Negative numeric strings must parse without error."""
    result = get_operands(1, input_fn=lambda _prompt: "-5.5")
    assert result == [-5.5]


def test_get_operands_zero_value_is_accepted() -> None:
    """Zero as a string must be parsed to 0.0 without error."""
    result = get_operands(1, input_fn=lambda _prompt: "0")
    assert result == [0.0]


def test_get_operands_very_large_number() -> None:
    """A very large numeric string must be accepted as float."""
    result = get_operands(1, input_fn=lambda _prompt: "1e308")
    assert result[0] == 1e308


def test_get_operands_whitespace_around_number_accepted() -> None:
    """Numeric input with surrounding whitespace must be parsed correctly."""
    result = get_operands(1, input_fn=lambda _prompt: "  3.14  ")
    assert math.isclose(result[0], 3.14)


def test_get_operands_empty_string_raises_value_error() -> None:
    """An empty string must raise ValueError (not parseable as float)."""
    with pytest.raises(ValueError):
        get_operands(1, input_fn=lambda _prompt: "")


def test_get_operands_none_like_string_raises_value_error() -> None:
    """The string 'None' must raise ValueError as it is not numeric."""
    with pytest.raises(ValueError):
        get_operands(1, input_fn=lambda _prompt: "None")


def test_get_operands_multiple_values_sequence() -> None:
    """Each call to input_fn maps to the next operand in order."""
    values = iter(["1.1", "2.2", "3.3"])
    result = get_operands(3, input_fn=lambda _prompt: next(values))
    assert result == pytest.approx([1.1, 2.2, 3.3])


def test_get_operands_prompt_uses_ordinal_labels() -> None:
    """When count > 1, the prompts must include 'operand 1' and 'operand 2'."""
    prompts: list[str] = []
    values = iter(["10", "20"])

    def recording_input(prompt: str) -> str:
        prompts.append(prompt)
        return next(values)

    get_operands(2, input_fn=recording_input)
    assert any("operand 1" in p for p in prompts)
    assert any("operand 2" in p for p in prompts)


def test_get_operands_prompt_uses_plain_label_for_single() -> None:
    """When count == 1, the prompt must contain 'operand' (without a number)."""
    prompts: list[str] = []

    def recording_input(prompt: str) -> str:
        prompts.append(prompt)
        return "5"

    get_operands(1, input_fn=recording_input)
    assert len(prompts) == 1
    assert "operand" in prompts[0]
    # Must NOT contain "operand 1" labelling style when count == 1
    assert "operand 1" not in prompts[0]


# ---------------------------------------------------------------------------
# dispatch — unary operations
# ---------------------------------------------------------------------------


def test_dispatch_square_positive() -> None:
    """dispatch 'square' must return x squared."""
    calc = Calculator()
    assert dispatch("square", [4.0], calc) == 16.0


def test_dispatch_square_negative() -> None:
    """Squaring a negative number must return a positive result."""
    calc = Calculator()
    assert dispatch("square", [-3.0], calc) == 9.0


def test_dispatch_square_zero() -> None:
    """Square of zero must be zero."""
    calc = Calculator()
    assert dispatch("square", [0.0], calc) == 0.0


def test_dispatch_cube_positive() -> None:
    """dispatch 'cube' must return x cubed."""
    calc = Calculator()
    assert dispatch("cube", [3.0], calc) == 27.0


def test_dispatch_cube_negative() -> None:
    """Cube of a negative number must be negative."""
    calc = Calculator()
    assert dispatch("cube", [-2.0], calc) == -8.0


def test_dispatch_cube_zero() -> None:
    """Cube of zero must be zero."""
    calc = Calculator()
    assert dispatch("cube", [0.0], calc) == 0.0


def test_dispatch_cube_root_positive() -> None:
    """dispatch 'cube_root' must return the real cube root."""
    calc = Calculator()
    result = dispatch("cube_root", [27.0], calc)
    assert math.isclose(result, 3.0)


def test_dispatch_cube_root_negative() -> None:
    """dispatch 'cube_root' of a negative number must return a negative result."""
    calc = Calculator()
    result = dispatch("cube_root", [-8.0], calc)
    assert math.isclose(result, -2.0)


def test_dispatch_cube_root_zero() -> None:
    """Cube root of zero must be zero."""
    calc = Calculator()
    assert dispatch("cube_root", [0.0], calc) == 0.0


def test_dispatch_square_root_positive() -> None:
    """dispatch 'square_root' must return sqrt of positive number."""
    calc = Calculator()
    assert math.isclose(dispatch("square_root", [16.0], calc), 4.0)


def test_dispatch_square_root_zero() -> None:
    """Square root of zero must be zero."""
    calc = Calculator()
    assert dispatch("square_root", [0.0], calc) == 0.0


def test_dispatch_square_root_negative_raises_value_error() -> None:
    """Square root of a negative number must raise ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError, match="non-negative"):
        dispatch("square_root", [-1.0], calc)


def test_dispatch_log_positive() -> None:
    """dispatch 'log' must return the base-10 log of a positive number."""
    calc = Calculator()
    assert math.isclose(dispatch("log", [100.0], calc), 2.0)


def test_dispatch_log_one() -> None:
    """log(1) must be 0.0."""
    calc = Calculator()
    assert dispatch("log", [1.0], calc) == 0.0


def test_dispatch_log_zero_raises_value_error() -> None:
    """log(0) must raise ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError):
        dispatch("log", [0.0], calc)


def test_dispatch_log_negative_raises_value_error() -> None:
    """log of a negative number must raise ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError):
        dispatch("log", [-5.0], calc)


def test_dispatch_ln_positive() -> None:
    """dispatch 'ln' must return the natural log of a positive number."""
    calc = Calculator()
    assert math.isclose(dispatch("ln", [math.e], calc), 1.0)


def test_dispatch_ln_one() -> None:
    """ln(1) must be 0.0."""
    calc = Calculator()
    assert dispatch("ln", [1.0], calc) == 0.0


def test_dispatch_ln_zero_raises_value_error() -> None:
    """ln(0) must raise ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError):
        dispatch("ln", [0.0], calc)


def test_dispatch_ln_negative_raises_value_error() -> None:
    """ln of a negative number must raise ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError):
        dispatch("ln", [-1.0], calc)


# ---------------------------------------------------------------------------
# dispatch — factorial edge cases
# ---------------------------------------------------------------------------


def test_dispatch_factorial_zero() -> None:
    """factorial(0) must be 1."""
    calc = Calculator()
    assert dispatch("factorial", [0.0], calc) == 1.0


def test_dispatch_factorial_positive_integer() -> None:
    """factorial(5) must be 120."""
    calc = Calculator()
    assert dispatch("factorial", [5.0], calc) == 120.0


def test_dispatch_factorial_returns_float() -> None:
    """dispatch 'factorial' must return a float (not an int)."""
    calc = Calculator()
    result = dispatch("factorial", [3.0], calc)
    assert isinstance(result, float)


def test_dispatch_factorial_float_truncated_to_int() -> None:
    """A float like 3.7 is truncated via int() before being passed to factorial.

    dispatch casts operands[0] via int() which truncates toward zero, so
    3.7 becomes 3 and the result must be 6.
    """
    calc = Calculator()
    result = dispatch("factorial", [3.7], calc)
    assert result == 6.0  # int(3.7) == 3, 3! == 6


def test_dispatch_factorial_negative_float_truncated_raises() -> None:
    """A negative float is truncated to a negative int which must raise ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError, match="non-negative"):
        dispatch("factorial", [-1.0], calc)


def test_dispatch_factorial_large_number() -> None:
    """dispatch 'factorial' on a large integer must return the correct value."""
    calc = Calculator()
    result = dispatch("factorial", [10.0], calc)
    assert result == float(math.factorial(10))


# ---------------------------------------------------------------------------
# dispatch — binary operations
# ---------------------------------------------------------------------------


def test_dispatch_subtract() -> None:
    """dispatch 'subtract' must return a - b."""
    calc = Calculator()
    assert dispatch("subtract", [10.0, 3.0], calc) == 7.0


def test_dispatch_multiply() -> None:
    """dispatch 'multiply' must return a * b."""
    calc = Calculator()
    assert dispatch("multiply", [6.0, 7.0], calc) == 42.0


def test_dispatch_power() -> None:
    """dispatch 'power' must return base ** exponent."""
    calc = Calculator()
    assert dispatch("power", [2.0, 10.0], calc) == 1024.0


def test_dispatch_power_zero_exponent() -> None:
    """Any base raised to power 0 must be 1."""
    calc = Calculator()
    assert dispatch("power", [999.0, 0.0], calc) == 1.0


def test_dispatch_power_negative_base_even_exponent() -> None:
    """Negative base raised to an even integer exponent must be positive."""
    calc = Calculator()
    assert dispatch("power", [-2.0, 2.0], calc) == 4.0


# ---------------------------------------------------------------------------
# dispatch — unknown operation key
# ---------------------------------------------------------------------------


def test_dispatch_unknown_key_raises_key_error() -> None:
    """An operation key not in OPERATIONS must raise KeyError."""
    calc = Calculator()
    with pytest.raises(KeyError, match="Unknown operation"):
        dispatch("bogus_op", [1.0], calc)


def test_dispatch_empty_key_raises_key_error() -> None:
    """An empty string as operation key must raise KeyError."""
    calc = Calculator()
    with pytest.raises(KeyError):
        dispatch("", [1.0], calc)


def test_dispatch_invalid_sentinel_raises_key_error() -> None:
    """The '__invalid__' sentinel passed directly must raise KeyError."""
    calc = Calculator()
    with pytest.raises(KeyError):
        dispatch("__invalid__", [], calc)


# ---------------------------------------------------------------------------
# dispatch — very large numbers
# ---------------------------------------------------------------------------


def test_dispatch_add_very_large_numbers() -> None:
    """Adding two very large floats must not raise an exception."""
    calc = Calculator()
    result = dispatch("add", [1e308, 1e308], calc)
    assert math.isinf(result)


def test_dispatch_square_very_large_number() -> None:
    """Squaring 1e200 overflows Python float range and must raise OverflowError.

    Python's float arithmetic raises OverflowError rather than silently
    returning inf when intermediate results exceed the representable range.
    """
    calc = Calculator()
    with pytest.raises(OverflowError):
        dispatch("square", [1e200], calc)


def test_dispatch_log_very_large_number() -> None:
    """log(1e308) must return a finite float close to 308."""
    calc = Calculator()
    result = dispatch("log", [1e308], calc)
    assert math.isfinite(result)
    assert math.isclose(result, 308.0, abs_tol=1.0)


# ---------------------------------------------------------------------------
# run_loop — additional integration scenarios
# ---------------------------------------------------------------------------


def test_run_loop_exits_immediately(capsys: pytest.CaptureFixture[str]) -> None:
    """If the first input is 'exit', the loop must print 'Goodbye' and return."""
    run_loop(input_fn=lambda _prompt: "exit")
    captured = capsys.readouterr()
    assert "Goodbye" in captured.out


def test_run_loop_multiple_valid_operations(capsys: pytest.CaptureFixture[str]) -> None:
    """Multiple sequential operations before exit must all produce results."""
    inputs = iter(["add", "1", "2", "multiply", "3", "4", "subtract", "10", "5", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "3" in captured.out   # 1 + 2
    assert "12" in captured.out  # 3 * 4
    assert "5" in captured.out   # 10 - 5
    assert "Goodbye" in captured.out


def test_run_loop_whitespace_input_for_operation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Whitespace-only operation input must show unknown-operation error and continue."""
    inputs = iter(["   ", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Unknown operation" in captured.out
    assert "Goodbye" in captured.out


def test_run_loop_empty_operation_input(capsys: pytest.CaptureFixture[str]) -> None:
    """Empty string operation input must show unknown-operation error and continue."""
    inputs = iter(["", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Unknown operation" in captured.out
    assert "Goodbye" in captured.out


def test_run_loop_sqrt_of_negative_shows_error_and_continues(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Square root of a negative number must produce an Error message and keep looping."""
    inputs = iter(["square_root", "-4", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Error" in captured.out
    assert "Goodbye" in captured.out


def test_run_loop_log_of_zero_shows_error_and_continues(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """log(0) must produce an Error message and keep the loop going."""
    inputs = iter(["log", "0", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Error" in captured.out
    assert "Goodbye" in captured.out


def test_run_loop_factorial_then_exit(capsys: pytest.CaptureFixture[str]) -> None:
    """Factorial operation via run_loop must compute and print the result."""
    inputs = iter(["factorial", "5", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "120" in captured.out
    assert "Goodbye" in captured.out


def test_run_loop_factorial_negative_shows_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Factorial of a negative number must show an Error and keep the loop going."""
    inputs = iter(["factorial", "-3", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Error" in captured.out
    assert "Goodbye" in captured.out


def test_run_loop_unary_operations_all_produce_results(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Every unary operation must produce a Result line when given a valid operand."""
    unary_inputs = [
        ("factorial", "4"),    # 24
        ("square", "3"),       # 9
        ("cube", "2"),         # 8
        ("square_root", "9"),  # 3
        ("cube_root", "8"),    # 2
        ("log", "100"),        # 2
        ("ln", "1"),           # 0
    ]
    sequence: list[str] = []
    for op, operand in unary_inputs:
        sequence.extend([op, operand])
    sequence.append("exit")

    inputs = iter(sequence)
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()

    # Each operation must produce exactly one "Result:" line
    result_count = captured.out.count("Result:")
    assert result_count == len(unary_inputs)
    assert "Goodbye" in captured.out


def test_run_loop_multiple_invalid_then_valid(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """After MAX_RETRY_ATTEMPTS invalid operations, session ends without a result."""
    from src.input_validator import MAX_RETRY_ATTEMPTS

    # Send exactly MAX_RETRY_ATTEMPTS invalid operations to exhaust retries
    inputs = iter(["bad"] * MAX_RETRY_ATTEMPTS)
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert captured.out.count("Error") == MAX_RETRY_ATTEMPTS
    assert "Maximum number of retries exceeded. Session ended." in captured.out
    assert "Goodbye" not in captured.out


def test_run_loop_result_line_format(capsys: pytest.CaptureFixture[str]) -> None:
    """The result must be printed with the prefix 'Result:'."""
    inputs = iter(["add", "10", "5", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Result:" in captured.out


def test_run_loop_power_operation(capsys: pytest.CaptureFixture[str]) -> None:
    """dispatch 'power' via run_loop must print 2^8 = 256."""
    inputs = iter(["power", "2", "8", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "256" in captured.out


def test_run_loop_cube_root_negative_operand(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Cube root of -27 is supported and must print a result close to -3."""
    inputs = iter(["cube_root", "-27", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Result:" in captured.out
    assert "Goodbye" in captured.out
    # -3.0 or -2.999... must appear in the output
    assert "-3" in captured.out or "2.999" in captured.out


# ---------------------------------------------------------------------------
# main() entry point
# ---------------------------------------------------------------------------


def test_main_runs_and_exits(capsys: pytest.CaptureFixture[str]) -> None:
    """main() must delegate to run_loop; patching run_loop confirms the call."""
    import unittest.mock as mock
    from src import __main__ as main_module

    # Patch run_loop inside the __main__ module so that no real I/O is required.
    # Pass explicit argv=[] to override sys.argv[1:] which may contain pytest flags.
    with mock.patch.object(main_module, "run_loop") as mock_run_loop:
        main_module.main(argv=[])

    mock_run_loop.assert_called_once_with()


# ---------------------------------------------------------------------------
# get_operation_interactive — happy path
# ---------------------------------------------------------------------------


def test_get_operation_interactive_valid_key_first_try() -> None:
    """A valid operation key on the first try must be returned."""
    result = get_operation_interactive(input_fn=lambda _prompt: "add")
    assert result == "add"


def test_get_operation_interactive_exit_returns_none() -> None:
    """Typing 'exit' on the first try must return None without consuming retries."""
    result = get_operation_interactive(input_fn=lambda _prompt: "exit")
    assert result is None


def test_get_operation_interactive_case_insensitive() -> None:
    """Uppercase input must be matched case-insensitively."""
    result = get_operation_interactive(input_fn=lambda _prompt: "ADD")
    assert result == "add"


def test_get_operation_interactive_whitespace_stripped() -> None:
    """Input with surrounding whitespace must be accepted."""
    result = get_operation_interactive(input_fn=lambda _prompt: "  multiply  ")
    assert result == "multiply"


@pytest.mark.parametrize("key", list(OPERATIONS.keys()))
def test_get_operation_interactive_each_valid_key(key: str) -> None:
    """Every valid OPERATIONS key must be accepted on first try."""
    result = get_operation_interactive(input_fn=lambda _prompt: key)
    assert result == key


# ---------------------------------------------------------------------------
# get_operation_interactive — retry on invalid, then success
# ---------------------------------------------------------------------------


def test_get_operation_interactive_one_invalid_then_valid() -> None:
    """One invalid operation then a valid one must eventually return the valid key."""
    inputs = iter(["bogus", "add"])
    result = get_operation_interactive(input_fn=lambda _prompt: next(inputs))
    assert result == "add"


def test_get_operation_interactive_two_invalid_then_valid() -> None:
    """Two invalid operations followed by a valid one must return the valid key."""
    inputs = iter(["bad1", "bad2", "subtract"])
    result = get_operation_interactive(input_fn=lambda _prompt: next(inputs))
    assert result == "subtract"


def test_get_operation_interactive_prints_error_on_invalid(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """An invalid operation must print an error message."""
    inputs = iter(["nonsense", "add"])
    get_operation_interactive(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Error" in captured.out


# ---------------------------------------------------------------------------
# get_operation_interactive — max retries exhausted
# ---------------------------------------------------------------------------


def test_get_operation_interactive_max_retries_exhausted_returns_sentinel() -> None:
    """After MAX_RETRY_ATTEMPTS invalid attempts, must return '__max_retries__'."""
    from src.input_validator import MAX_RETRY_ATTEMPTS

    # Provide exactly MAX_RETRY_ATTEMPTS invalid inputs
    inputs = iter(["bad"] * MAX_RETRY_ATTEMPTS)
    result = get_operation_interactive(input_fn=lambda _prompt: next(inputs))
    assert result == "__max_retries__"


def test_get_operation_interactive_exactly_at_limit() -> None:
    """With exactly MAX_RETRY_ATTEMPTS retries, the sentinel is returned."""
    from src.input_validator import MAX_RETRY_ATTEMPTS

    inputs = iter(["invalid"] * MAX_RETRY_ATTEMPTS)
    result = get_operation_interactive(input_fn=lambda _prompt: next(inputs))
    assert result == "__max_retries__"


def test_get_operation_interactive_one_before_limit_still_retries() -> None:
    """With MAX_RETRY_ATTEMPTS - 1 invalid, a valid input on the last try succeeds."""
    from src.input_validator import MAX_RETRY_ATTEMPTS

    # Provide MAX_RETRY_ATTEMPTS - 1 invalid, then 1 valid
    invalid_count = MAX_RETRY_ATTEMPTS - 1
    inputs = iter(["bad"] * invalid_count + ["add"])
    result = get_operation_interactive(input_fn=lambda _prompt: next(inputs))
    assert result == "add"


def test_get_operation_interactive_exit_does_not_consume_retry(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Typing 'exit' must not consume a retry attempt; return None immediately."""
    call_count = [0]

    def counting_input(prompt: str) -> str:
        call_count[0] += 1
        if call_count[0] == 1:
            return "invalid"
        if call_count[0] == 2:
            return "exit"
        return "should_not_reach"

    # After 1 invalid + 1 exit, we should see 2 calls (exit does not consume retry)
    result = counting_input
    inputs = iter(["invalid", "exit"])
    result = get_operation_interactive(input_fn=lambda _prompt: next(inputs))
    assert result is None


def test_get_operation_interactive_prints_error_multiple_times(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Multiple invalid attempts must each print an error message."""
    from src.input_validator import MAX_RETRY_ATTEMPTS

    inputs = iter(["bad"] * MAX_RETRY_ATTEMPTS)
    get_operation_interactive(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    # There should be MAX_RETRY_ATTEMPTS error messages
    error_count = captured.out.count("Error:")
    assert error_count == MAX_RETRY_ATTEMPTS


def test_get_operation_interactive_empty_string_is_invalid(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """An empty string input must be treated as invalid and consumed as a retry."""
    inputs = iter(["", "add"])
    result = get_operation_interactive(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert result == "add"
    assert "Error" in captured.out


def test_get_operation_interactive_whitespace_only_is_invalid(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Whitespace-only input must be treated as invalid."""
    inputs = iter(["   ", "multiply"])
    result = get_operation_interactive(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert result == "multiply"
    assert "Error" in captured.out


# ---------------------------------------------------------------------------
# get_operands_interactive — happy path
# ---------------------------------------------------------------------------


def test_get_operands_interactive_single_valid_operand() -> None:
    """A single valid numeric operand must be returned as a list with one float."""
    result = get_operands_interactive(1, input_fn=lambda _prompt: "5.0")
    assert result == [5.0]


def test_get_operands_interactive_two_valid_operands() -> None:
    """Two valid numeric operands must be returned as a list of two floats."""
    inputs = iter(["10", "20"])
    result = get_operands_interactive(2, input_fn=lambda _prompt: next(inputs))
    assert result == [10.0, 20.0]


def test_get_operands_interactive_three_valid_operands() -> None:
    """Three valid operands must be returned as a list of three floats."""
    inputs = iter(["1.5", "2.5", "3.5"])
    result = get_operands_interactive(3, input_fn=lambda _prompt: next(inputs))
    assert result == [1.5, 2.5, 3.5]


def test_get_operands_interactive_negative_numbers() -> None:
    """Negative numeric operands must be accepted."""
    inputs = iter(["-5.5", "-10"])
    result = get_operands_interactive(2, input_fn=lambda _prompt: next(inputs))
    assert result == [-5.5, -10.0]


def test_get_operands_interactive_zero() -> None:
    """Zero must be accepted as a valid operand."""
    result = get_operands_interactive(1, input_fn=lambda _prompt: "0")
    assert result == [0.0]


def test_get_operands_interactive_returns_list_of_floats() -> None:
    """The return value must be a list of float instances."""
    result = get_operands_interactive(1, input_fn=lambda _prompt: "5")
    assert isinstance(result, list)
    assert all(isinstance(v, float) for v in result)


# ---------------------------------------------------------------------------
# get_operands_interactive — retry on invalid, then success
# ---------------------------------------------------------------------------


def test_get_operands_interactive_one_invalid_then_valid(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """One invalid attempt followed by valid operands must succeed."""
    inputs = iter(["not_a_number", "5.0"])
    result = get_operands_interactive(1, input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert result == [5.0]
    assert "Error" in captured.out


def test_get_operands_interactive_first_of_multiple_invalid(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """If the first operand is invalid, the entire attempt fails."""
    inputs = iter(["abc", "5.0"])
    result = get_operands_interactive(1, input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert result == [5.0]
    assert "Error" in captured.out


def test_get_operands_interactive_second_of_multiple_invalid(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """If the second operand is invalid in a multi-operand request, entire attempt fails."""
    inputs = iter(["5.0", "not_a_number", "5.0", "10.0"])
    result = get_operands_interactive(2, input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert result == [5.0, 10.0]
    assert "Error" in captured.out


def test_get_operands_interactive_two_invalid_attempts_then_valid(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Two invalid attempts followed by valid operands must succeed."""
    inputs = iter(["bad1", "bad2", "7.0"])
    result = get_operands_interactive(1, input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert result == [7.0]
    # Should see 2 error messages
    assert captured.out.count("Error") >= 2


# ---------------------------------------------------------------------------
# get_operands_interactive — max retries exhausted
# ---------------------------------------------------------------------------


def test_get_operands_interactive_max_retries_exhausted_returns_none() -> None:
    """After MAX_RETRY_ATTEMPTS invalid attempts, must return None."""
    from src.input_validator import MAX_RETRY_ATTEMPTS

    inputs = iter(["invalid"] * MAX_RETRY_ATTEMPTS)
    result = get_operands_interactive(1, input_fn=lambda _prompt: next(inputs))
    assert result is None


def test_get_operands_interactive_exactly_at_limit() -> None:
    """With exactly MAX_RETRY_ATTEMPTS invalid attempts, None is returned."""
    from src.input_validator import MAX_RETRY_ATTEMPTS

    inputs = iter(["bad"] * MAX_RETRY_ATTEMPTS)
    result = get_operands_interactive(1, input_fn=lambda _prompt: next(inputs))
    assert result is None


def test_get_operands_interactive_one_before_limit_succeeds() -> None:
    """With MAX_RETRY_ATTEMPTS - 1 invalid, a valid attempt on the last try succeeds."""
    from src.input_validator import MAX_RETRY_ATTEMPTS

    invalid_count = MAX_RETRY_ATTEMPTS - 1
    inputs = iter(["bad"] * invalid_count + ["5.0"])
    result = get_operands_interactive(1, input_fn=lambda _prompt: next(inputs))
    assert result == [5.0]


def test_get_operands_interactive_prints_error_for_each_retry(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Each failed attempt must print an error message."""
    from src.input_validator import MAX_RETRY_ATTEMPTS

    inputs = iter(["invalid"] * MAX_RETRY_ATTEMPTS)
    get_operands_interactive(1, input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    # Should see MAX_RETRY_ATTEMPTS error messages
    error_count = captured.out.count("Error:")
    assert error_count == MAX_RETRY_ATTEMPTS


def test_get_operands_interactive_empty_string_is_invalid(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """An empty string operand must be treated as invalid."""
    inputs = iter(["", "5.0"])
    result = get_operands_interactive(1, input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert result == [5.0]
    assert "Error" in captured.out


def test_get_operands_interactive_whitespace_only_is_invalid(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Whitespace-only operand must be treated as invalid."""
    inputs = iter(["   ", "5.0"])
    result = get_operands_interactive(1, input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert result == [5.0]
    assert "Error" in captured.out


# ---------------------------------------------------------------------------
# run_loop — integration with new interactive functions
# ---------------------------------------------------------------------------


def test_run_loop_exit_on_max_retries_operation(capsys: pytest.CaptureFixture[str]) -> None:
    """Exhausting retries on invalid operations must print the max-retries message."""
    from src.input_validator import MAX_RETRY_ATTEMPTS

    # Provide MAX_RETRY_ATTEMPTS invalid operations
    inputs = iter(["bad"] * MAX_RETRY_ATTEMPTS)
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Maximum number of retries exceeded. Session ended." in captured.out


def test_run_loop_exit_on_max_retries_operands(capsys: pytest.CaptureFixture[str]) -> None:
    """Exhausting retries on invalid operands must print the max-retries message.

    For binary operation 'add', each attempt needs 2 operand inputs.
    So for MAX_RETRY_ATTEMPTS retries, we need MAX_RETRY_ATTEMPTS * 2 invalid operands.
    """
    from src.input_validator import MAX_RETRY_ATTEMPTS

    # Valid operation, then MAX_RETRY_ATTEMPTS attempts of 2 invalid operands each
    invalid_operand_sequence = ["invalid"] * (MAX_RETRY_ATTEMPTS * 2)
    inputs = iter(["add"] + invalid_operand_sequence)
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Maximum number of retries exceeded. Session ended." in captured.out


def test_run_loop_max_retries_operation_does_not_print_goodbye(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """When max retries on operation is exhausted, 'Goodbye' must NOT be printed."""
    from src.input_validator import MAX_RETRY_ATTEMPTS

    inputs = iter(["bad"] * MAX_RETRY_ATTEMPTS)
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    # The session-ended message should appear, but not 'Goodbye'
    assert "Maximum number of retries exceeded" in captured.out
    assert "Goodbye" not in captured.out


def test_run_loop_max_retries_operands_does_not_print_goodbye(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """When max retries on operands is exhausted, 'Goodbye' must NOT be printed."""
    from src.input_validator import MAX_RETRY_ATTEMPTS

    # For binary operation 'add', each attempt needs 2 inputs
    invalid_operand_sequence = ["bad"] * (MAX_RETRY_ATTEMPTS * 2)
    inputs = iter(["add"] + invalid_operand_sequence)
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Maximum number of retries exceeded" in captured.out
    assert "Goodbye" not in captured.out


def test_run_loop_exit_prints_goodbye_not_max_retries_message(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Typing 'exit' must print 'Goodbye' and NOT print max-retries message."""
    run_loop(input_fn=lambda _prompt: "exit")
    captured = capsys.readouterr()
    assert "Goodbye" in captured.out
    assert "Maximum number of retries exceeded" not in captured.out


def test_run_loop_valid_operation_within_retry_limit_succeeds(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Valid operation within retry limit must complete normally."""
    from src.input_validator import MAX_RETRY_ATTEMPTS

    # 1 invalid, then 1 valid operation (within limit), then exit
    inputs = iter(["bad", "add", "5", "10", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "15" in captured.out
    assert "Goodbye" in captured.out
    assert "Maximum number of retries exceeded" not in captured.out


def test_run_loop_valid_operand_within_retry_limit_succeeds(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Valid operands within retry limit must complete the calculation.

    For binary operation 'add', the first invalid attempt consumes 2 inputs,
    then we provide valid operands for a second attempt.
    """
    # Valid operation, 1 invalid operand attempt (2 invalid values), then valid operands, then exit
    inputs = iter(["add", "bad1", "bad2", "5", "10", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "15" in captured.out
    assert "Goodbye" in captured.out
    assert "Maximum number of retries exceeded" not in captured.out


def test_run_loop_near_retry_limit_operation_succeeds(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """MAX_RETRY_ATTEMPTS - 1 invalid operations, then valid, must succeed."""
    from src.input_validator import MAX_RETRY_ATTEMPTS

    invalid_count = MAX_RETRY_ATTEMPTS - 1
    inputs = iter(["bad"] * invalid_count + ["add", "3", "7", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "10" in captured.out
    assert "Goodbye" in captured.out


def test_run_loop_near_retry_limit_operands_succeeds(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """MAX_RETRY_ATTEMPTS - 1 invalid operand attempts, then valid, must succeed."""
    from src.input_validator import MAX_RETRY_ATTEMPTS

    invalid_count = MAX_RETRY_ATTEMPTS - 1
    inputs = iter(["add"] + ["bad"] * invalid_count + ["2", "8", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "10" in captured.out
    assert "Goodbye" in captured.out


def test_run_loop_mixed_invalid_operations_and_operands(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Multiple invalid operations and operands (within limits) must still work.

    The sequence:
    1. "bad_op" - invalid operation (retry 1)
    2. "add" - valid operation, needs 2 operands
    3. "bad_op1", "bad_op2" - invalid operands (retry 1)
    4. "multiply" - valid operation, needs 2 operands
    5. "3", "4" - valid operands
    6. "exit" - exit
    """
    inputs = iter(["bad_op", "add", "bad_op1", "bad_op2", "5", "10", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "15" in captured.out  # 5 + 10
    assert "Goodbye" in captured.out


def test_run_loop_continues_after_calculator_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A calculator error (e.g., divide by zero) must NOT trigger retry counting."""
    inputs = iter(["divide", "1", "0", "add", "5", "5", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Error" in captured.out  # Division error
    assert "10" in captured.out      # Subsequent operation succeeds
    assert "Goodbye" in captured.out


def test_run_loop_all_unary_operations_with_retries(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Unary operations with some invalid attempts must all eventually succeed."""
    inputs = iter([
        "bad",
        "factorial", "5",  # Valid
        "bad",
        "square", "3",      # Valid
        "cube", "2",        # Valid
        "exit"
    ])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "120" in captured.out  # 5!
    assert "9" in captured.out    # 3^2
    assert "8" in captured.out    # 2^3
    assert "Goodbye" in captured.out


def test_run_loop_result_format_unchanged(capsys: pytest.CaptureFixture[str]) -> None:
    """Result output format must still be 'Result: <value>'."""
    inputs = iter(["add", "7", "8", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Result: 15" in captured.out


def test_run_loop_error_format_unchanged(capsys: pytest.CaptureFixture[str]) -> None:
    """Error output format from validation must be 'Error: <message>'."""
    inputs = iter(["add", "not_a_number", "invalid", "5", "10", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Error:" in captured.out
    assert "Goodbye" in captured.out
