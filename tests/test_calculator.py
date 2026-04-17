import pathlib
import math

import pytest
from src.calculator import Calculator


def test_divide_by_zero():
    calculator = Calculator()
    with pytest.raises(ZeroDivisionError):
        calculator.divide(1, 0)


# Group 1 — Core operations

def test_add_two_positive_integers():
    assert Calculator().add(3, 4) == 7


def test_add_negative_numbers():
    assert Calculator().add(-3, -4) == -7


def test_add_with_zero():
    assert Calculator().add(5, 0) == 5


def test_subtract_positive_numbers():
    assert Calculator().subtract(10, 3) == 7


def test_subtract_resulting_in_negative():
    assert Calculator().subtract(3, 10) == -7


def test_subtract_with_zero():
    assert Calculator().subtract(5, 0) == 5


def test_multiply_two_positive_integers():
    assert Calculator().multiply(3, 4) == 12


def test_multiply_by_zero():
    assert Calculator().multiply(5, 0) == 0


def test_multiply_negative_numbers():
    assert Calculator().multiply(-3, 4) == -12


def test_divide_exact_result():
    assert Calculator().divide(10, 2) == 5


def test_divide_resulting_in_float():
    assert Calculator().divide(1, 4) == pytest.approx(0.25)


# Group 2 — Edge cases

def test_add_large_integers():
    assert Calculator().add(10**18, 10**18) == 2 * 10**18


def test_multiply_floats():
    assert Calculator().multiply(0.1, 0.2) == pytest.approx(0.02)


def test_divide_float_dividend():
    assert Calculator().divide(1.0, 3.0) == pytest.approx(1 / 3)


def test_add_invalid_type_raises():
    with pytest.raises(TypeError):
        Calculator().add(None, 1)


def test_subtract_invalid_type_raises():
    with pytest.raises(TypeError):
        Calculator().subtract(None, 1)


def test_multiply_invalid_type_raises():
    with pytest.raises(TypeError):
        Calculator().multiply(None, 1)


def test_divide_invalid_type_raises():
    with pytest.raises(TypeError):
        Calculator().divide(None, 1)


# Group 4 — Additional edge cases (boundary values, float precision, sign handling)

# --- add ---

def test_add_both_zero():
    assert Calculator().add(0, 0) == 0


def test_add_float_and_int():
    assert Calculator().add(1.5, 2) == pytest.approx(3.5)


def test_add_positive_and_negative_cancel():
    assert Calculator().add(7, -7) == 0


def test_add_float_inf():
    assert Calculator().add(float("inf"), 1) == float("inf")


def test_add_float_nan_is_nan():
    result = Calculator().add(float("nan"), 1)
    assert math.isnan(result)


def test_add_string_raises_type_error():
    with pytest.raises(TypeError):
        Calculator().add("a", 1)


def test_add_second_operand_invalid_type_raises():
    with pytest.raises(TypeError):
        Calculator().add(1, None)


# --- subtract ---

def test_subtract_both_zero():
    assert Calculator().subtract(0, 0) == 0


def test_subtract_same_value_gives_zero():
    assert Calculator().subtract(42, 42) == 0


def test_subtract_large_integers():
    assert Calculator().subtract(10**18, 10**18 - 1) == 1


def test_subtract_float_inf():
    assert Calculator().subtract(float("inf"), 1) == float("inf")


def test_subtract_string_raises_type_error():
    with pytest.raises(TypeError):
        Calculator().subtract("a", 1)


def test_subtract_second_operand_invalid_type_raises():
    with pytest.raises(TypeError):
        Calculator().subtract(1, None)


# --- multiply ---

def test_multiply_both_negative():
    assert Calculator().multiply(-3, -4) == 12


def test_multiply_both_zero():
    assert Calculator().multiply(0, 0) == 0


def test_multiply_one():
    assert Calculator().multiply(99, 1) == 99


def test_multiply_large_integers():
    assert Calculator().multiply(10**9, 10**9) == 10**18


def test_multiply_float_inf():
    assert Calculator().multiply(float("inf"), 2) == float("inf")


def test_multiply_string_raises_type_error():
    # "a" * 2 is valid Python (string repetition), so both operands must be
    # non-numeric to trigger TypeError from the * operator.
    with pytest.raises(TypeError):
        Calculator().multiply("a", "b")


def test_multiply_second_operand_invalid_type_raises():
    with pytest.raises(TypeError):
        Calculator().multiply(2, None)


# --- divide ---

def test_divide_negative_dividend():
    assert Calculator().divide(-10, 2) == -5


def test_divide_negative_divisor():
    assert Calculator().divide(10, -2) == -5


def test_divide_both_negative():
    assert Calculator().divide(-10, -2) == 5


def test_divide_zero_numerator():
    assert Calculator().divide(0, 5) == 0


def test_divide_zero_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        Calculator().divide(0, 0)


def test_divide_large_integers():
    assert Calculator().divide(10**18, 10**9) == pytest.approx(10**9)


def test_divide_float_inf_divisor():
    assert Calculator().divide(1.0, float("inf")) == pytest.approx(0.0)


def test_divide_string_raises_type_error():
    with pytest.raises(TypeError):
        Calculator().divide("a", 2)


def test_divide_second_operand_invalid_type_raises():
    with pytest.raises(TypeError):
        Calculator().divide(2, None)


@pytest.mark.parametrize("a,b,expected", [
    (0, 0, 0),
    (1, 1, 2),
    (-1, -1, -2),
    (10**9, 10**9, 2 * 10**9),
])
def test_add_parametrized(a, b, expected):
    assert Calculator().add(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [
    (6, 3, 2),
    (-6, -3, 2),
    (-6, 3, -2),
    (6, -3, -2),
])
def test_divide_sign_parametrized(a, b, expected):
    assert Calculator().divide(a, b) == pytest.approx(expected)


# Group 3 — Self-modification output syntax validation

def test_generated_output_files_are_syntactically_valid_python():
    """Validates that any Python artifacts produced by the self-evolution engine are syntactically valid. Passes vacuously when no generated files exist."""
    repo_root = pathlib.Path(__file__).parent.parent
    for dir_name in ("output", "patches"):
        target_dir = repo_root / dir_name
        if not target_dir.exists():
            continue
        for py_file in target_dir.rglob("*.py"):
            source = py_file.read_text(encoding="utf-8")
            try:
                compile(source, str(py_file), "exec")
            except SyntaxError as exc:
                raise AssertionError(f"Syntax error in generated file {py_file}: {exc}") from exc
