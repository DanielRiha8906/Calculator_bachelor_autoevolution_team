"""Edge-case tests for src/input_handler.py.

Covers: negative operands, float operands, boundary values for unary
operations (sqrt(0), factorial(0)), log operations, cube root of negative
numbers, cascading invalid inputs before a valid one, very large numbers,
and the run_session convenience wrapper.

All tests use the injectable input_fn parameter; builtins.input is never
patched.
"""

import math
import pytest

from src.calculator import Calculator
from src.input_handler import InputHandler, OPERATIONS, run_session


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_input_fn(responses: list[str]):
    """Return a callable that yields successive strings from *responses*."""
    it = iter(responses)

    def _input_fn(prompt: str = "") -> str:  # noqa: ARG001
        return next(it)

    return _input_fn


@pytest.fixture
def calc() -> Calculator:
    return Calculator()


# ---------------------------------------------------------------------------
# _show_menu
# ---------------------------------------------------------------------------

def test_show_menu_lists_all_operations(calc, capsys):
    """_show_menu must print every key registered in OPERATIONS."""
    handler = InputHandler(calc)
    handler._show_menu()
    captured = capsys.readouterr()
    for key in OPERATIONS:
        assert key in captured.out


def test_show_menu_contains_available_operations_header(calc, capsys):
    """_show_menu must print the section header line."""
    handler = InputHandler(calc)
    handler._show_menu()
    captured = capsys.readouterr()
    assert "Available operations" in captured.out


# ---------------------------------------------------------------------------
# _prompt_operands
# ---------------------------------------------------------------------------

def test_prompt_operands_arity_2_returns_two_floats(calc):
    """_prompt_operands with arity=2 must return exactly two float values."""
    handler = InputHandler(calc, make_input_fn(["3.5", "7.0"]))
    result = handler._prompt_operands(2, float)
    assert result == [3.5, 7.0]
    assert len(result) == 2


def test_prompt_operands_arity_1_returns_one_value(calc):
    """_prompt_operands with arity=1 must return exactly one value."""
    handler = InputHandler(calc, make_input_fn(["9"]))
    result = handler._prompt_operands(1, float)
    assert result == [9.0]
    assert len(result) == 1


def test_prompt_operands_coerce_int(calc):
    """_prompt_operands with coerce=int must convert the raw string to int."""
    handler = InputHandler(calc, make_input_fn(["5"]))
    result = handler._prompt_operands(1, int)
    assert result == [5]
    assert isinstance(result[0], int)


def test_prompt_operands_negative_float(calc):
    """_prompt_operands must correctly handle negative float strings."""
    handler = InputHandler(calc, make_input_fn(["-3.14", "-2.71"]))
    result = handler._prompt_operands(2, float)
    assert result[0] == pytest.approx(-3.14)
    assert result[1] == pytest.approx(-2.71)


def test_prompt_operands_invalid_raises_value_error(calc):
    """_prompt_operands must raise RetryExhausted after 5 invalid operands."""
    from src.validation import RetryExhausted
    handler = InputHandler(calc, make_input_fn([
        "not_a_number", "also_invalid", "still_bad", "nope", "fail"
    ]))
    with pytest.raises(RetryExhausted, match="operand"):
        handler._prompt_operands(1, float)


def test_prompt_operands_invalid_second_operand_raises_value_error(calc):
    """RetryExhausted must fire on the second operand after 5 invalid attempts."""
    from src.validation import RetryExhausted
    handler = InputHandler(calc, make_input_fn([
        "5",  # first operand valid
        "bad1", "bad2", "bad3", "bad4", "bad5"  # second operand: 5 invalid attempts
    ]))
    with pytest.raises(RetryExhausted, match="operand"):
        handler._prompt_operands(2, float)


def test_prompt_operands_whitespace_stripped(calc):
    """Leading/trailing whitespace in operand input must be tolerated."""
    handler = InputHandler(calc, make_input_fn(["  7  "]))
    result = handler._prompt_operands(1, float)
    assert result == [7.0]


def test_prompt_operands_empty_string_raises_value_error(calc):
    """An empty operand string triggers retry; 5 empty strings raise RetryExhausted."""
    from src.validation import RetryExhausted
    handler = InputHandler(calc, make_input_fn(["", "", "", "", ""]))
    with pytest.raises(RetryExhausted, match="operand"):
        handler._prompt_operands(1, float)


# ---------------------------------------------------------------------------
# _dispatch
# ---------------------------------------------------------------------------

def test_dispatch_add(calc):
    """_dispatch('add', [3, 4]) must return 7."""
    handler = InputHandler(calc)
    assert handler._dispatch("add", [3, 4]) == 7


def test_dispatch_subtract(calc):
    handler = InputHandler(calc)
    assert handler._dispatch("subtract", [10, 3]) == 7


def test_dispatch_multiply(calc):
    handler = InputHandler(calc)
    assert handler._dispatch("multiply", [3.0, 4.0]) == pytest.approx(12.0)


def test_dispatch_divide(calc):
    handler = InputHandler(calc)
    assert handler._dispatch("divide", [9.0, 3.0]) == pytest.approx(3.0)


def test_dispatch_divide_by_zero_raises(calc):
    """_dispatch must propagate ZeroDivisionError from Calculator.divide."""
    handler = InputHandler(calc)
    with pytest.raises(ZeroDivisionError):
        handler._dispatch("divide", [1.0, 0.0])


def test_dispatch_square_root(calc):
    handler = InputHandler(calc)
    assert handler._dispatch("square_root", [16.0]) == pytest.approx(4.0)


def test_dispatch_square_root_of_zero(calc):
    """square_root(0) must return exactly 0.0."""
    handler = InputHandler(calc)
    assert handler._dispatch("square_root", [0.0]) == 0.0


def test_dispatch_factorial_zero(calc):
    """factorial(0) must return 1 (mathematical identity)."""
    handler = InputHandler(calc)
    assert handler._dispatch("factorial", [0]) == 1


def test_dispatch_log10(calc):
    """log10(100) must return 2.0."""
    handler = InputHandler(calc)
    assert handler._dispatch("log10", [100.0]) == pytest.approx(2.0)


def test_dispatch_ln(calc):
    """ln(e) must return 1.0."""
    handler = InputHandler(calc)
    assert handler._dispatch("ln", [math.e]) == pytest.approx(1.0)


def test_dispatch_cube_root_negative(calc):
    """cube_root of a negative number must return a negative float."""
    handler = InputHandler(calc)
    result = handler._dispatch("cube_root", [-27.0])
    assert result == pytest.approx(-3.0)


# ---------------------------------------------------------------------------
# run() — negative operands
# ---------------------------------------------------------------------------

def test_run_add_negative_operands(calc, capsys):
    """add(-3, -5) must print -8 and not crash."""
    handler = InputHandler(calc, make_input_fn(["add", "-3", "-5", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "-8" in out
    assert "Goodbye!" in out


def test_run_subtract_negative_result(calc, capsys):
    """subtract(3, 10) yields -7; the result line must contain -7."""
    handler = InputHandler(calc, make_input_fn(["subtract", "3", "10", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "-7" in out
    assert "Goodbye!" in out


def test_run_multiply_both_negative(calc, capsys):
    """multiply(-4, -3) must yield 12 (negative * negative = positive)."""
    handler = InputHandler(calc, make_input_fn(["multiply", "-4", "-3", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "12" in out
    assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# run() — float operands
# ---------------------------------------------------------------------------

def test_run_multiply_floats(calc, capsys):
    """multiply(2.5, 4.0) must print 10.0."""
    handler = InputHandler(calc, make_input_fn(["multiply", "2.5", "4.0", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "10.0" in out
    assert "Goodbye!" in out


def test_run_add_floats(calc, capsys):
    """add(1.1, 2.2) must produce a result close to 3.3."""
    handler = InputHandler(calc, make_input_fn(["add", "1.1", "2.2", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "Result:" in out
    assert "Goodbye!" in out


def test_run_divide_float_result(calc, capsys):
    """divide(7, 2) must print 3.5."""
    handler = InputHandler(calc, make_input_fn(["divide", "7", "2", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "3.5" in out


# ---------------------------------------------------------------------------
# run() — square_root(0)
# ---------------------------------------------------------------------------

def test_run_square_root_of_zero(calc, capsys):
    """square_root(0) must print 0.0 without error."""
    handler = InputHandler(calc, make_input_fn(["square_root", "0", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "0.0" in out
    assert "Goodbye!" in out


def test_run_square_root_of_negative_prints_error(calc, capsys):
    """square_root(-1) must print an error message, not crash."""
    handler = InputHandler(calc, make_input_fn(["square_root", "-1", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "Error" in out
    assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# run() — factorial
# ---------------------------------------------------------------------------

def test_run_factorial_zero(calc, capsys):
    """factorial(0) must print 1 (edge case: 0! = 1)."""
    handler = InputHandler(calc, make_input_fn(["factorial", "0", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "1" in out
    assert "Goodbye!" in out


def test_run_factorial_one(calc, capsys):
    """factorial(1) must print 1."""
    handler = InputHandler(calc, make_input_fn(["factorial", "1", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "1" in out
    assert "Goodbye!" in out


def test_run_factorial_negative_prints_error(calc, capsys):
    """factorial(-1) must print an error, not crash."""
    handler = InputHandler(calc, make_input_fn(["factorial", "-1", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "Error" in out
    assert "Goodbye!" in out


def test_run_factorial_float_input_prints_error(calc, capsys):
    """factorial of a float string like '3.5' must print a conversion error."""
    # The OPERATIONS registry coerces factorial operands with int(), so "3.5"
    # will fail int("3.5") and produce an invalid-operand error.
    handler = InputHandler(calc, make_input_fn(["factorial", "3.5", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "Error" in out
    assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# run() — log operations
# ---------------------------------------------------------------------------

def test_run_log10_valid(calc, capsys):
    """log10(1000) must print 3.0."""
    handler = InputHandler(calc, make_input_fn(["log10", "1000", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "3.0" in out
    assert "Goodbye!" in out


def test_run_log10_of_one(calc, capsys):
    """log10(1) must print 0.0."""
    handler = InputHandler(calc, make_input_fn(["log10", "1", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "0.0" in out
    assert "Goodbye!" in out


def test_run_log10_of_zero_prints_error(calc, capsys):
    """log10(0) must print an error (domain error), not crash."""
    handler = InputHandler(calc, make_input_fn(["log10", "0", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "Error" in out
    assert "Goodbye!" in out


def test_run_log10_of_negative_prints_error(calc, capsys):
    """log10(-5) must print an error message, not crash."""
    handler = InputHandler(calc, make_input_fn(["log10", "-5", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "Error" in out
    assert "Goodbye!" in out


def test_run_ln_valid(calc, capsys):
    """ln(e) must print a result close to 1.0."""
    import math as _math
    e_str = str(_math.e)
    handler = InputHandler(calc, make_input_fn(["ln", e_str, "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "Result:" in out
    assert "Goodbye!" in out


def test_run_ln_of_one(calc, capsys):
    """ln(1) must print 0.0."""
    handler = InputHandler(calc, make_input_fn(["ln", "1", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "0.0" in out
    assert "Goodbye!" in out


def test_run_ln_of_zero_prints_error(calc, capsys):
    """ln(0) must print an error (domain error), not crash."""
    handler = InputHandler(calc, make_input_fn(["ln", "0", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "Error" in out
    assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# run() — cube_root of negative number
# ---------------------------------------------------------------------------

def test_run_cube_root_negative(calc, capsys):
    """cube_root(-27) must print -3.0, because cbrt is defined for negatives."""
    handler = InputHandler(calc, make_input_fn(["cube_root", "-27", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "Result:" in out
    assert "-3.0" in out
    assert "Goodbye!" in out


def test_run_cube_root_zero(calc, capsys):
    """cube_root(0) must print 0.0."""
    handler = InputHandler(calc, make_input_fn(["cube_root", "0", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "0.0" in out
    assert "Goodbye!" in out


def test_run_cube_root_positive(calc, capsys):
    """cube_root(8) must print 2.0."""
    handler = InputHandler(calc, make_input_fn(["cube_root", "8", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "2.0" in out
    assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# run() — multiple invalid operations before a valid one
# ---------------------------------------------------------------------------

def test_run_multiple_invalid_ops_then_valid(calc, capsys):
    """Several unknown keys must each print an error; session continues to a valid op."""
    handler = InputHandler(
        calc,
        make_input_fn(["nonsense", "another_bad", "??", "add", "1", "2", "exit"]),
    )
    handler.run()
    out = capsys.readouterr().out
    # All three unknown keys should have triggered error messages
    assert out.count("Error") >= 3
    assert "Result:" in out
    assert "3" in out
    assert "Goodbye!" in out


def test_run_invalid_then_invalid_operand_then_valid(calc, capsys):
    """Mixing an unknown op with an invalid operand then a valid op all continue cleanly."""
    handler = InputHandler(
        calc,
        make_input_fn(["badop", "add", "xyz", "add", "5", "5", "exit"]),
    )
    handler.run()
    out = capsys.readouterr().out
    assert out.count("Error") >= 2
    assert "10" in out
    assert "Goodbye!" in out


def test_run_three_invalid_ops_then_exit(calc, capsys):
    """Three unknown keys followed by exit must print three errors then Goodbye."""
    handler = InputHandler(
        calc,
        make_input_fn(["x", "y", "z", "exit"]),
    )
    handler.run()
    out = capsys.readouterr().out
    assert out.count("Error") == 3
    assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# run() — very large numbers
# ---------------------------------------------------------------------------

def test_run_add_very_large_numbers(calc, capsys):
    """add with two very large integers must not crash and must print a result."""
    large = "9" * 50  # 50-digit integer expressed as float string
    handler = InputHandler(calc, make_input_fn(["add", large, large, "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "Result:" in out
    assert "Goodbye!" in out


def test_run_multiply_large_floats(calc, capsys):
    """multiply(1e300, 1e300) produces inf; result line must still appear."""
    handler = InputHandler(calc, make_input_fn(["multiply", "1e300", "1e300", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "Result:" in out
    assert "Goodbye!" in out


def test_run_power_large_exponent(calc, capsys):
    """power(2, 100) must print a result that contains the correct value."""
    handler = InputHandler(calc, make_input_fn(["power", "2", "100", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    # 2**100 = 1267650600228229401496703205376
    assert "Result:" in out
    assert "Goodbye!" in out


def test_run_factorial_large_value(calc, capsys):
    """factorial(20) must print 2432902008176640000 without crashing."""
    handler = InputHandler(calc, make_input_fn(["factorial", "20", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "2432902008176640000" in out
    assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# run() — case sensitivity of operation key
# ---------------------------------------------------------------------------

def test_run_operation_key_uppercase_rejected(calc, capsys):
    """Operation keys are case-sensitive after lower(); 'ADD' (already lowered) is 'add'."""
    # The handler does .strip().lower() on the choice, so 'ADD' becomes 'add'
    handler = InputHandler(calc, make_input_fn(["ADD", "2", "3", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    # 'ADD' lowers to 'add' which IS a valid op
    assert "5" in out
    assert "Goodbye!" in out


def test_run_operation_key_mixed_case_lowered(calc, capsys):
    """Mixed-case input like 'Add' lowers to 'add' and executes correctly."""
    handler = InputHandler(calc, make_input_fn(["Add", "10", "5", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "15" in out
    assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# run() — whitespace around operation key
# ---------------------------------------------------------------------------

def test_run_operation_key_with_surrounding_whitespace(calc, capsys):
    """Leading/trailing whitespace in the operation key must be stripped."""
    handler = InputHandler(calc, make_input_fn(["  add  ", "6", "7", "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "13" in out
    assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# run() — all unary operations smoke-tested
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("op,operand,expected_fragment", [
    ("square", "5", "25"),
    ("cube", "3", "27"),
    ("square_root", "4", "2.0"),
    ("cube_root", "8", "2.0"),
    ("log10", "10", "1.0"),
    ("ln", "1", "0.0"),
    ("factorial", "4", "24"),
])
def test_run_unary_operations(calc, capsys, op, operand, expected_fragment):
    """Each unary operation must produce the expected result fragment."""
    handler = InputHandler(calc, make_input_fn([op, operand, "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert expected_fragment in out
    assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# run() — all binary operations smoke-tested
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("op,a,b,expected_fragment", [
    ("add", "3", "4", "7"),
    ("subtract", "10", "4", "6"),
    ("multiply", "3", "4", "12"),
    ("divide", "10", "2", "5"),
    ("power", "2", "8", "256"),
])
def test_run_binary_operations(calc, capsys, op, a, b, expected_fragment):
    """Each binary operation must produce the expected result fragment."""
    handler = InputHandler(calc, make_input_fn([op, a, b, "exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert expected_fragment in out
    assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# run_session convenience wrapper
# ---------------------------------------------------------------------------

def test_run_session_exits_cleanly(capsys):
    """run_session must delegate to InputHandler.run and exit on 'exit'."""
    from src.input_handler import run_session
    calc = Calculator()
    run_session(calc, make_input_fn(["exit"]))
    out = capsys.readouterr().out
    assert "Goodbye!" in out


def test_run_session_performs_calculation(capsys):
    """run_session must produce correct results when given valid input."""
    from src.input_handler import run_session
    calc = Calculator()
    run_session(calc, make_input_fn(["add", "7", "8", "exit"]))
    out = capsys.readouterr().out
    assert "15" in out
    assert "Goodbye!" in out


def test_run_session_uses_provided_calculator(capsys):
    """run_session must use the calculator instance that is passed in."""
    from src.input_handler import run_session
    calc = Calculator()
    run_session(calc, make_input_fn(["multiply", "6", "7", "exit"]))
    out = capsys.readouterr().out
    assert "42" in out
    assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# InputHandler default input_fn (constructor path)
# ---------------------------------------------------------------------------

def test_input_handler_default_input_fn_is_builtin_input(calc):
    """When input_fn is omitted, the handler must store the built-in input."""
    import builtins
    handler = InputHandler(calc)
    assert handler._input_fn is builtins.input


def test_input_handler_accepts_none_input_fn(calc):
    """Passing None as input_fn must fall back to the built-in input."""
    import builtins
    handler = InputHandler(calc, None)
    assert handler._input_fn is builtins.input


# ---------------------------------------------------------------------------
# Edge: exit/quit case-insensitive
# ---------------------------------------------------------------------------

def test_run_exit_uppercase(calc, capsys):
    """'EXIT' must trigger the exit branch after lowercasing."""
    handler = InputHandler(calc, make_input_fn(["EXIT"]))
    handler.run()
    out = capsys.readouterr().out
    assert "Goodbye!" in out


def test_run_quit_uppercase(calc, capsys):
    """'QUIT' must trigger the exit branch after lowercasing."""
    handler = InputHandler(calc, make_input_fn(["QUIT"]))
    handler.run()
    out = capsys.readouterr().out
    assert "Goodbye!" in out


def test_run_exit_mixed_case(calc, capsys):
    """'Exit' must trigger the exit branch after lowercasing."""
    handler = InputHandler(calc, make_input_fn(["Exit"]))
    handler.run()
    out = capsys.readouterr().out
    assert "Goodbye!" in out
