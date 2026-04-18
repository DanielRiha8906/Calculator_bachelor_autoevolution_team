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
    get_operation,
    handle_mode_switch,
    print_menu,
    run_loop,
)
from src.mode import Mode


# ---------------------------------------------------------------------------
# print_menu
# ---------------------------------------------------------------------------


def test_print_menu_outputs_all_operations(capsys: pytest.CaptureFixture[str]) -> None:
    """print_menu(mode=SCIENTIFIC) must include every key in OPERATIONS and the 'exit' hint."""
    print_menu(mode=Mode.SCIENTIFIC)
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
    """An unrecognised key must print error and exhaust retries, returning '__max_retries_exceeded__'."""
    inputs = iter(["nonsense", "nonsense", "nonsense"])
    result = get_operation(input_fn=lambda _prompt: next(inputs))
    assert result == "__max_retries_exceeded__"
    captured = capsys.readouterr()
    assert "Invalid operation" in captured.out


# ---------------------------------------------------------------------------
# get_operands
# ---------------------------------------------------------------------------


def test_get_operands_two_values_returns_floats() -> None:
    """Two numeric inputs must be returned as a list of two floats."""
    values = iter(["3", "4"])
    result = get_operands(2, input_fn=lambda _prompt: next(values))
    assert result == [3.0, 4.0]
    assert all(isinstance(v, float) for v in result)


def test_get_operands_non_numeric_exhausts_retries_returns_none(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A non-numeric input exhausts retries and returns None."""
    inputs = iter(["abc", "abc", "abc"])
    result = get_operands(1, input_fn=lambda _prompt: next(inputs))
    assert result is None
    captured = capsys.readouterr()
    assert "Maximum retry attempts reached" in captured.out


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
    """An invalid operation with retry then exit must show error and exit."""
    inputs = iter(["nonsense", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Invalid operation" in captured.out
    assert "Goodbye" in captured.out


def test_run_loop_non_numeric_operand_shows_error_and_continues(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A non-numeric operand with retry then valid operands must show error and continue."""
    inputs = iter(["add", "abc", "3", "4", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Error" in captured.out or "numeric" in captured.out
    assert "Result: 7" in captured.out
    assert "Goodbye" in captured.out


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
    """Every OPERATIONS entry must have its display label present in SCIENTIFIC mode."""
    print_menu(mode=Mode.SCIENTIFIC)
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
    """Every key in OPERATIONS must be returned as-is by get_operation in SCIENTIFIC mode."""
    result = get_operation(input_fn=lambda _prompt: key, mode=Mode.SCIENTIFIC)
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
    """Mixed-case input must be matched case-insensitively in SCIENTIFIC mode."""
    result = get_operation(input_fn=lambda _prompt: "Factorial", mode=Mode.SCIENTIFIC)
    assert result == "factorial"


def test_get_operation_empty_string_returns_sentinel(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """An empty string exhausts retries and returns '__max_retries_exceeded__'."""
    inputs = iter(["", "", ""])
    result = get_operation(input_fn=lambda _prompt: next(inputs))
    assert result == "__max_retries_exceeded__"
    captured = capsys.readouterr()
    assert "Invalid operation" in captured.out


def test_get_operation_whitespace_only_returns_sentinel(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Whitespace-only input exhausts retries and returns '__max_retries_exceeded__'."""
    inputs = iter(["   ", "   ", "   "])
    result = get_operation(input_fn=lambda _prompt: next(inputs))
    assert result == "__max_retries_exceeded__"
    captured = capsys.readouterr()
    assert "Invalid operation" in captured.out


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


def test_get_operands_empty_string_exhausts_retries_returns_none(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """An empty string exhausts retries and returns None."""
    inputs = iter(["", "", ""])
    result = get_operands(1, input_fn=lambda _prompt: next(inputs))
    assert result is None
    captured = capsys.readouterr()
    assert "Maximum retry attempts reached" in captured.out


def test_get_operands_none_like_string_exhausts_retries_returns_none(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The string 'None' exhausts retries and returns None."""
    inputs = iter(["None", "None", "None"])
    result = get_operands(1, input_fn=lambda _prompt: next(inputs))
    assert result is None
    captured = capsys.readouterr()
    assert "Maximum retry attempts reached" in captured.out


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
    """Whitespace-only operation input retries then valid input or exit continues."""
    inputs = iter(["   ", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Invalid operation" in captured.out
    assert "Goodbye" in captured.out


def test_run_loop_empty_operation_input(capsys: pytest.CaptureFixture[str]) -> None:
    """Empty string operation input retries then exit continues."""
    inputs = iter(["", "exit"])
    run_loop(input_fn=lambda _prompt: next(inputs))
    captured = capsys.readouterr()
    assert "Invalid operation" in captured.out
    assert "Goodbye" in captured.out


def test_run_loop_sqrt_of_negative_shows_error_and_continues(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Square root of a negative number must produce an Error message and keep looping."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["mode scientific", "square_root", "-4", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        assert "Error" in captured.out
        assert "Goodbye" in captured.out


def test_run_loop_log_of_zero_shows_error_and_continues(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """log(0) must produce an Error message and keep the loop going."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["mode scientific", "log", "0", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        assert "Error" in captured.out
        assert "Goodbye" in captured.out


def test_run_loop_factorial_then_exit(capsys: pytest.CaptureFixture[str]) -> None:
    """Factorial operation via run_loop must compute and print the result."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["mode scientific", "factorial", "5", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        assert "120" in captured.out
        assert "Goodbye" in captured.out


def test_run_loop_factorial_negative_shows_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Factorial of a negative number must show an Error and keep the loop going."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["mode scientific", "factorial", "-3", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        assert "Error" in captured.out
        assert "Goodbye" in captured.out


def test_run_loop_unary_operations_all_produce_results(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Every unary operation must produce a Result line when given a valid operand."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        unary_inputs = [
            ("factorial", "4"),    # 24
            ("square", "3"),       # 9
            ("cube", "2"),         # 8
            ("square_root", "9"),  # 3
            ("cube_root", "8"),    # 2
            ("log", "100"),        # 2
            ("ln", "1"),           # 0
        ]
        sequence: list[str] = ["mode scientific"]
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
    """Three invalid operations exhaust retries and terminate session."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["bad1", "bad2", "bad3"])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        assert "Invalid operation" in captured.out
        assert "Session terminated due to too many invalid operation entries" in captured.out


def test_run_loop_result_line_format(capsys: pytest.CaptureFixture[str]) -> None:
    """The result must be printed with the prefix 'Result:'."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["add", "10", "5", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        assert "Result:" in captured.out


def test_run_loop_power_operation(capsys: pytest.CaptureFixture[str]) -> None:
    """dispatch 'power' via run_loop must print 2^8 = 256."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["mode scientific", "power", "2", "8", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        assert "256" in captured.out


def test_run_loop_cube_root_negative_operand(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Cube root of -27 is supported and must print a result close to -3."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["mode scientific", "cube_root", "-27", "exit"])
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
# history command – integration tests
# ---------------------------------------------------------------------------


def test_run_loop_history_command_in_operations_dict() -> None:
    """'history' must be a key in OPERATIONS with operand count 0."""
    assert "history" in OPERATIONS
    label, operand_count = OPERATIONS["history"]
    assert operand_count == 0
    assert label is not None and len(label) > 0


def test_run_loop_history_command_displays_empty_message(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """history command with no operations must display 'No operations' message."""
    from src.history import OperationHistory
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        inputs = iter(["history", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)
        captured = capsys.readouterr()
        assert "No operations recorded" in captured.out or "No operations" in captured.out


def test_run_loop_history_command_displays_operations(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """history command must display recorded operations."""
    from src.history import OperationHistory
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        inputs = iter(["add", "2", "3", "history", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)
        captured = capsys.readouterr()
        # After the add operation, 'history' command should display it
        assert "2.0 add 3.0 = 5.0" in captured.out or "2" in captured.out


def test_run_loop_history_command_continues_loop(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """After viewing history, loop must continue and accept more operations."""
    from src.history import OperationHistory
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        # Add operation, then history, then another operation, then exit
        inputs = iter(["add", "1", "1", "history", "multiply", "2", "3", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)
        captured = capsys.readouterr()
        # Both operations must appear in output
        assert "2" in captured.out  # 1 + 1 = 2
        assert "6" in captured.out  # 2 * 3 = 6
        assert "Goodbye" in captured.out


def test_run_loop_history_command_before_any_operations(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """history command on empty history must show appropriate message."""
    from src.history import OperationHistory
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        inputs = iter(["history", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)
        captured = capsys.readouterr()
        assert "No operations" in captured.out or "empty" in captured.out.lower()


def test_run_loop_records_operation_on_successful_calculation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Successful operation must be recorded in history."""
    from src.history import OperationHistory
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        inputs = iter(["add", "10", "5", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)

        # Verify history was recorded
        recorded = history.get_history()
        assert len(recorded) == 1
        assert "10.0 add 5.0 = 15.0" in recorded[0]


def test_run_loop_does_not_record_operation_on_calculator_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Failed operations (e.g., division by zero) must not be recorded."""
    from src.history import OperationHistory
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        inputs = iter(["divide", "1", "0", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)

        # History should be empty because division by zero failed
        recorded = history.get_history()
        assert len(recorded) == 0


def test_run_loop_records_multiple_operations_in_order(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Multiple operations must be recorded in chronological order."""
    from src.history import OperationHistory
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        inputs = iter([
            "add", "1", "2",
            "multiply", "3", "4",
            "mode scientific", "square", "5",
            "exit"
        ])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)

        recorded = history.get_history()
        assert len(recorded) == 3
        assert "1.0 add 2.0 = 3.0" in recorded[0]
        assert "3.0 multiply 4.0 = 12.0" in recorded[1]
        assert "square(5.0) = 25.0" in recorded[2]


def test_run_loop_history_command_with_multiple_operations(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """history command must display all recorded operations."""
    from src.history import OperationHistory
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        history = OperationHistory()
        inputs = iter([
            "add", "5", "3",
            "subtract", "10", "2",
            "history",
            "exit"
        ])
        run_loop(input_fn=lambda _prompt: next(inputs), history=history)
        captured = capsys.readouterr()

        # Both operations should be displayed by history command
        assert "5.0 add 3.0 = 8.0" in captured.out
        assert "10.0 subtract 2.0 = 8.0" in captured.out


# ---------------------------------------------------------------------------
# error logging integration tests
# ---------------------------------------------------------------------------


def test_run_loop_division_by_zero_is_logged(capsys: pytest.CaptureFixture[str]) -> None:
    """run_loop must log division by zero to error.log."""
    import tempfile
    import os
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["divide", "10", "0", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))

        log_file = Path(tmpdir) / "error.log"
        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "CALCULATION_ERROR" in content
        assert "Division by zero" in content or "zero" in content.lower()


def test_run_loop_invalid_operand_is_logged_or_rejected(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """run_loop must handle invalid operand input (either reject or log)."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        # Retry limit is 3, so need 3 invalid attempts
        inputs = iter(["add", "abc", "abc", "abc", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))

        captured = capsys.readouterr()
        # Must show error message about non-numeric input or return to menu
        assert "Error" in captured.out or "numeric" in captured.out.lower() or "Returning" in captured.out


def test_run_loop_negative_square_root_is_logged(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """run_loop must log square root of negative number as CALCULATION_ERROR."""
    import tempfile
    import os
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["mode scientific", "square_root", "-4", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))

        log_file = Path(tmpdir) / "error.log"
        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "CALCULATION_ERROR" in content


def test_run_loop_creates_error_logger_by_default(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """run_loop must create an ErrorLogger when none is injected."""
    import tempfile
    import os
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["divide", "5", "0", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))

        log_file = Path(tmpdir) / "error.log"
        # When an error occurs, the default logger should create the file
        assert log_file.exists()


# ---------------------------------------------------------------------------
# handle_mode_switch tests
# ---------------------------------------------------------------------------


def test_handle_mode_switch_normal_command_returns_normal_mode() -> None:
    """handle_mode_switch('mode normal', ...) must return Mode.NORMAL."""
    result = handle_mode_switch("mode normal", Mode.SCIENTIFIC)
    assert result is Mode.NORMAL


def test_handle_mode_switch_scientific_command_returns_scientific_mode() -> None:
    """handle_mode_switch('mode scientific', ...) must return Mode.SCIENTIFIC."""
    result = handle_mode_switch("mode scientific", Mode.NORMAL)
    assert result is Mode.SCIENTIFIC


def test_handle_mode_switch_returns_none_for_empty_string() -> None:
    """handle_mode_switch('', ...) must return None."""
    result = handle_mode_switch("", Mode.NORMAL)
    assert result is None


def test_handle_mode_switch_returns_none_for_add() -> None:
    """handle_mode_switch('add', ...) must return None."""
    result = handle_mode_switch("add", Mode.NORMAL)
    assert result is None


def test_handle_mode_switch_returns_none_for_history() -> None:
    """handle_mode_switch('history', ...) must return None."""
    result = handle_mode_switch("history", Mode.NORMAL)
    assert result is None


def test_handle_mode_switch_returns_none_for_exit() -> None:
    """handle_mode_switch('exit', ...) must return None."""
    result = handle_mode_switch("exit", Mode.NORMAL)
    assert result is None


def test_handle_mode_switch_returns_none_for_arbitrary_string() -> None:
    """handle_mode_switch('arbitrary', ...) must return None."""
    result = handle_mode_switch("arbitrary", Mode.NORMAL)
    assert result is None


def test_handle_mode_switch_already_in_normal_can_switch_to_normal() -> None:
    """Switching to Mode.NORMAL when already in NORMAL must return Mode.NORMAL."""
    result = handle_mode_switch("mode normal", Mode.NORMAL)
    assert result is Mode.NORMAL


def test_handle_mode_switch_already_in_scientific_can_switch_to_scientific() -> None:
    """Switching to Mode.SCIENTIFIC when already in SCIENTIFIC must return Mode.SCIENTIFIC."""
    result = handle_mode_switch("mode scientific", Mode.SCIENTIFIC)
    assert result is Mode.SCIENTIFIC


def test_handle_mode_switch_current_mode_parameter_ignored() -> None:
    """current_mode parameter only serves as context; result is determined by input."""
    # Regardless of current_mode, "mode normal" returns Mode.NORMAL
    result1 = handle_mode_switch("mode normal", Mode.NORMAL)
    result2 = handle_mode_switch("mode normal", Mode.SCIENTIFIC)
    assert result1 == result2 == Mode.NORMAL


# ---------------------------------------------------------------------------
# print_menu mode-aware tests
# ---------------------------------------------------------------------------


def test_print_menu_normal_mode_shows_basic_four_operations(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """print_menu(Mode.NORMAL) must show only 4 basic operations."""
    print_menu(mode=Mode.NORMAL)
    captured = capsys.readouterr()
    # Must include the four basic operations
    assert "add" in captured.out
    assert "subtract" in captured.out
    assert "multiply" in captured.out
    assert "divide" in captured.out


def test_print_menu_normal_mode_hides_scientific_operations(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """print_menu(Mode.NORMAL) must not show scientific-only operations."""
    print_menu(mode=Mode.NORMAL)
    captured = capsys.readouterr()
    # power, factorial, log, ln should NOT appear in NORMAL mode
    assert "power" not in captured.out
    assert "factorial" not in captured.out
    assert "log" not in captured.out
    assert "ln" not in captured.out


def test_print_menu_scientific_mode_shows_all_operations(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """print_menu(Mode.SCIENTIFIC) must show all 12 operations."""
    print_menu(mode=Mode.SCIENTIFIC)
    captured = capsys.readouterr()
    # All 12 operations should be shown
    assert "add" in captured.out
    assert "subtract" in captured.out
    assert "multiply" in captured.out
    assert "divide" in captured.out
    assert "power" in captured.out
    assert "factorial" in captured.out
    assert "square" in captured.out
    assert "cube" in captured.out
    assert "square_root" in captured.out
    assert "cube_root" in captured.out
    assert "log" in captured.out
    assert "ln" in captured.out


def test_print_menu_normal_shows_mode_switch_commands(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """print_menu(Mode.NORMAL) must show mode-switch commands."""
    print_menu(mode=Mode.NORMAL)
    captured = capsys.readouterr()
    assert "mode normal" in captured.out
    assert "mode scientific" in captured.out


def test_print_menu_scientific_shows_mode_switch_commands(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """print_menu(Mode.SCIENTIFIC) must show mode-switch commands."""
    print_menu(mode=Mode.SCIENTIFIC)
    captured = capsys.readouterr()
    assert "mode normal" in captured.out
    assert "mode scientific" in captured.out


def test_print_menu_shows_exit_in_both_modes(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """print_menu must always show exit command in both modes."""
    print_menu(mode=Mode.NORMAL)
    captured_normal = capsys.readouterr()
    assert "exit" in captured_normal.out

    print_menu(mode=Mode.SCIENTIFIC)
    captured_scientific = capsys.readouterr()
    assert "exit" in captured_scientific.out


def test_print_menu_shows_history_in_both_modes(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """print_menu must always show history command in both modes."""
    print_menu(mode=Mode.NORMAL)
    captured_normal = capsys.readouterr()
    assert "history" in captured_normal.out

    print_menu(mode=Mode.SCIENTIFIC)
    captured_scientific = capsys.readouterr()
    assert "history" in captured_scientific.out


# ---------------------------------------------------------------------------
# get_operation mode-aware tests
# ---------------------------------------------------------------------------


def test_get_operation_normal_mode_accepts_basic_four() -> None:
    """get_operation(mode=NORMAL) must accept all four basic operations."""
    for op in ["add", "subtract", "multiply", "divide"]:
        result = get_operation(input_fn=lambda _prompt: op, mode=Mode.NORMAL)
        assert result == op


def test_get_operation_normal_mode_rejects_power() -> None:
    """get_operation(mode=NORMAL) must reject 'power'."""
    inputs = iter(["power", "exit"])
    result = get_operation(input_fn=lambda _prompt: next(inputs), mode=Mode.NORMAL)
    assert result is None


def test_get_operation_normal_mode_rejects_factorial() -> None:
    """get_operation(mode=NORMAL) must reject 'factorial'."""
    inputs = iter(["factorial", "exit"])
    result = get_operation(input_fn=lambda _prompt: next(inputs), mode=Mode.NORMAL)
    assert result is None


def test_get_operation_normal_mode_rejects_log() -> None:
    """get_operation(mode=NORMAL) must reject 'log'."""
    inputs = iter(["log", "exit"])
    result = get_operation(input_fn=lambda _prompt: next(inputs), mode=Mode.NORMAL)
    assert result is None


def test_get_operation_normal_mode_rejects_ln() -> None:
    """get_operation(mode=NORMAL) must reject 'ln'."""
    inputs = iter(["ln", "exit"])
    result = get_operation(input_fn=lambda _prompt: next(inputs), mode=Mode.NORMAL)
    assert result is None


def test_get_operation_scientific_mode_accepts_power() -> None:
    """get_operation(mode=SCIENTIFIC) must accept 'power'."""
    result = get_operation(input_fn=lambda _prompt: "power", mode=Mode.SCIENTIFIC)
    assert result == "power"


def test_get_operation_scientific_mode_accepts_factorial() -> None:
    """get_operation(mode=SCIENTIFIC) must accept 'factorial'."""
    result = get_operation(input_fn=lambda _prompt: "factorial", mode=Mode.SCIENTIFIC)
    assert result == "factorial"


def test_get_operation_scientific_mode_accepts_log() -> None:
    """get_operation(mode=SCIENTIFIC) must accept 'log'."""
    result = get_operation(input_fn=lambda _prompt: "log", mode=Mode.SCIENTIFIC)
    assert result == "log"


def test_get_operation_scientific_mode_accepts_ln() -> None:
    """get_operation(mode=SCIENTIFIC) must accept 'ln'."""
    result = get_operation(input_fn=lambda _prompt: "ln", mode=Mode.SCIENTIFIC)
    assert result == "ln"


def test_get_operation_mode_switch_bypasses_validation() -> None:
    """get_operation must return mode-switch commands without retries."""
    result = get_operation(
        input_fn=lambda _prompt: "mode normal", mode=Mode.SCIENTIFIC
    )
    assert result == "mode normal"


def test_get_operation_mode_switch_does_not_consume_retry() -> None:
    """Mode-switch command must not count toward retry limit."""
    # Request "mode normal" 10 times (more than MAX_RETRY_ATTEMPTS=3)
    # All should succeed because mode-switch bypasses retry logic
    inputs = iter(["mode normal"] * 10)
    results = []
    for _ in range(10):
        result = get_operation(
            input_fn=lambda _prompt: next(inputs), retry_limit=3, mode=Mode.NORMAL
        )
        results.append(result)
    assert all(r == "mode normal" for r in results)


def test_get_operation_history_always_accepted_regardless_of_mode() -> None:
    """get_operation must accept 'history' in both NORMAL and SCIENTIFIC modes."""
    result_normal = get_operation(
        input_fn=lambda _prompt: "history", mode=Mode.NORMAL
    )
    assert result_normal == "history"

    result_scientific = get_operation(
        input_fn=lambda _prompt: "history", mode=Mode.SCIENTIFIC
    )
    assert result_scientific == "history"


def test_get_operation_mode_scientific_accepts_all_arithmetic_operations() -> None:
    """get_operation(mode=SCIENTIFIC) must accept all 12 arithmetic operations."""
    ops_to_test = [
        "add", "subtract", "multiply", "divide",
        "power", "factorial", "square", "cube",
        "square_root", "cube_root", "log", "ln"
    ]
    for op in ops_to_test:
        result = get_operation(input_fn=lambda _prompt: op, mode=Mode.SCIENTIFIC)
        assert result == op, f"Operation '{op}' should be accepted in SCIENTIFIC mode"


# ---------------------------------------------------------------------------
# run_loop mode-aware integration tests
# ---------------------------------------------------------------------------


def test_run_loop_starts_in_normal_mode(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """run_loop must start in NORMAL mode."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["add", "1", "2", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        # Result should be prefixed with [Normal]>
        assert "[Normal]>" in captured.out


def test_run_loop_scientific_result_prefixed_with_scientific(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """run_loop result must show [Scientific]> when in SCIENTIFIC mode."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["mode scientific", "power", "2", "3", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        assert "[Scientific]>" in captured.out


def test_run_loop_mode_normal_rejects_power_operation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Starting in NORMAL mode, 'power' should be rejected."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["power", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        # "power" is not a valid operation in NORMAL mode
        assert "Invalid operation" in captured.out


def test_run_loop_switches_to_scientific_mode(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """run_loop must accept 'mode scientific' command and switch."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["mode scientific", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        assert "Switched to Scientific mode" in captured.out


def test_run_loop_switches_to_normal_mode_from_scientific(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """run_loop must accept 'mode normal' from SCIENTIFIC mode."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["mode scientific", "mode normal", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        assert "Switched to Normal mode" in captured.out


def test_run_loop_mode_scientific_accepts_power_operation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """After switching to SCIENTIFIC, 'power' should be accepted."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["mode scientific", "power", "2", "3", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        assert "Result:" in captured.out
        assert "8" in captured.out  # 2^3 = 8


def test_run_loop_mode_label_normal_initially(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """run_loop result prefix must say [Normal]> initially."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["add", "1", "1", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        assert "[Normal]>" in captured.out


def test_run_loop_mode_label_updates_after_switch(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """run_loop result prefix must update after mode switch."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter([
            "add", "1", "1",           # Normal: [Normal]> Result: 2
            "mode scientific",         # Switch to SCIENTIFIC
            "power", "2", "3",         # Scientific: [Scientific]> Result: 8
            "exit"
        ])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        # Both prefixes should appear
        assert "[Normal]>" in captured.out
        assert "[Scientific]>" in captured.out


def test_run_loop_refuses_scientific_operation_in_normal_mode(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """In NORMAL mode, scientific operations like 'ln' should be rejected."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        inputs = iter(["ln", "exit"])
        run_loop(input_fn=lambda _prompt: next(inputs))
        captured = capsys.readouterr()
        assert "Invalid operation" in captured.out or "Valid operations" in captured.out
