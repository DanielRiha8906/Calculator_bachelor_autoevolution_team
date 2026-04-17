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


# Group 5 — Factorial

def test_factorial_zero():
    assert Calculator().factorial(0) == 1


def test_factorial_one():
    assert Calculator().factorial(1) == 1


def test_factorial_small_positive():
    assert Calculator().factorial(5) == 120


def test_factorial_larger_positive():
    assert Calculator().factorial(10) == 3628800


def test_factorial_negative_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().factorial(-1)


def test_factorial_float_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().factorial(2.0)


def test_factorial_string_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().factorial("5")


def test_factorial_none_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().factorial(None)


# Group 6 — Factorial extended edge cases

# --- bool inputs (bool is a subclass of int, intentional pass-through) ---

def test_factorial_true_returns_one():
    # True == 1 as an int, so factorial(True) == factorial(1) == 1
    assert Calculator().factorial(True) == 1


def test_factorial_false_returns_one():
    # False == 0 as an int, so factorial(False) == factorial(0) == 1
    assert Calculator().factorial(False) == 1


# --- large valid inputs ---

def test_factorial_twenty():
    assert Calculator().factorial(20) == 2432902008176640000


def test_factorial_large_value_is_positive_int():
    # Verify math.factorial returns correct type and sign for a large n
    result = Calculator().factorial(100)
    assert isinstance(result, int)
    assert result > 0


def test_factorial_large_value_exact():
    # 20! is well-known; use it as an anchored regression check
    assert Calculator().factorial(20) == math.factorial(20)


# --- boundary: n=2 ---

def test_factorial_two():
    assert Calculator().factorial(2) == 2


# --- negative boundary values ---

def test_factorial_negative_large_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().factorial(-100)


def test_factorial_negative_one_error_message_contains_value():
    with pytest.raises(ValueError, match="-1"):
        Calculator().factorial(-1)


# --- float variants that look integer-like ---

def test_factorial_float_zero_raises_value_error():
    # 0.0 is a float, not an int — must be rejected
    with pytest.raises(ValueError):
        Calculator().factorial(0.0)


def test_factorial_float_one_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().factorial(1.0)


def test_factorial_float_negative_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().factorial(-1.0)


def test_factorial_float_nan_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().factorial(float("nan"))


def test_factorial_float_inf_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().factorial(float("inf"))


# --- other wrong types ---

def test_factorial_list_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().factorial([5])


def test_factorial_dict_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().factorial({"n": 5})


def test_factorial_tuple_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().factorial((5,))


def test_factorial_bytes_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().factorial(b"5")


def test_factorial_complex_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().factorial(complex(5, 0))


# --- error message content ---

def test_factorial_float_error_message_mentions_type():
    with pytest.raises(ValueError, match="float"):
        Calculator().factorial(3.14)


def test_factorial_string_error_message_mentions_type():
    with pytest.raises(ValueError, match="str"):
        Calculator().factorial("hello")


def test_factorial_none_error_message_mentions_type():
    with pytest.raises(ValueError, match="NoneType"):
        Calculator().factorial(None)


# --- parametrized correctness sweep ---

@pytest.mark.parametrize("n,expected", [
    (0, 1),
    (1, 1),
    (2, 2),
    (3, 6),
    (4, 24),
    (5, 120),
    (6, 720),
    (7, 5040),
    (10, 3628800),
    (12, 479001600),
])
def test_factorial_parametrized_known_values(n, expected):
    assert Calculator().factorial(n) == expected


@pytest.mark.parametrize("bad_input", [
    -1, -2, -10, -100,
])
def test_factorial_parametrized_negative_raises(bad_input):
    with pytest.raises(ValueError):
        Calculator().factorial(bad_input)


@pytest.mark.parametrize("bad_input", [
    0.0, 1.0, 2.5, -1.0, float("nan"), float("inf"), float("-inf"),
    "0", "5", "", None, [], {}, (1,), b"5", complex(1, 0),
])
def test_factorial_parametrized_wrong_type_raises(bad_input):
    with pytest.raises(ValueError):
        Calculator().factorial(bad_input)


# --- instance method is bound to the instance (not a static side-effect) ---

def test_factorial_called_on_same_instance_twice_is_consistent():
    calc = Calculator()
    assert calc.factorial(5) == 120
    assert calc.factorial(5) == 120


def test_factorial_does_not_mutate_input_variable():
    n = 5
    Calculator().factorial(n)
    assert n == 5


# Group 7 — Power and root functions

# --- square ---

def test_square_positive():
    assert Calculator().square(4) == pytest.approx(16)


def test_square_negative():
    assert Calculator().square(-3) == pytest.approx(9)


def test_square_zero():
    assert Calculator().square(0) == pytest.approx(0)


def test_square_float():
    assert Calculator().square(2.5) == pytest.approx(6.25)


# --- cube ---

def test_cube_positive():
    assert Calculator().cube(3) == pytest.approx(27)


def test_cube_negative():
    assert Calculator().cube(-2) == pytest.approx(-8)


def test_cube_zero():
    assert Calculator().cube(0) == pytest.approx(0)


# --- square_root ---

def test_square_root_perfect_square():
    assert Calculator().square_root(9) == pytest.approx(3.0)


def test_square_root_four():
    assert Calculator().square_root(4) == pytest.approx(2.0)


def test_square_root_float():
    assert Calculator().square_root(2.0) == pytest.approx(math.sqrt(2.0))


def test_square_root_negative_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().square_root(-1)


# --- cube_root ---

def test_cube_root_positive():
    assert Calculator().cube_root(27) == pytest.approx(3.0)


def test_cube_root_negative():
    assert Calculator().cube_root(-8) == pytest.approx(-2.0)


def test_cube_root_zero():
    assert Calculator().cube_root(0) == pytest.approx(0.0)


def test_cube_root_float():
    assert Calculator().cube_root(8.0) == pytest.approx(2.0)


# --- power ---

def test_power_positive_exponent():
    assert Calculator().power(2, 10) == pytest.approx(1024.0)


def test_power_fractional_exponent():
    assert Calculator().power(4, 0.5) == pytest.approx(2.0)


def test_power_zero_zero():
    assert Calculator().power(0, 0) == pytest.approx(1.0)


def test_power_negative_base_integer_exponent():
    assert Calculator().power(-2, 3) == pytest.approx(-8.0)


# --- log (base-10) ---

def test_log_hundred():
    assert Calculator().log(100) == pytest.approx(2.0)


def test_log_zero_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().log(0)


def test_log_negative_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().log(-1)


# --- ln (natural log) ---

def test_ln_e():
    assert Calculator().ln(math.e) == pytest.approx(1.0)


def test_ln_zero_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().ln(0)


def test_ln_negative_raises_value_error():
    with pytest.raises(ValueError):
        Calculator().ln(-1)


# Group 8 — Additional edge cases for power/root/log methods

# --- square ---

def test_square_large_integer():
    assert Calculator().square(10**9) == pytest.approx(10**18)


def test_square_float_inf():
    assert Calculator().square(float("inf")) == float("inf")


def test_square_negative_float_inf():
    # (-inf)^2 == +inf
    assert Calculator().square(float("-inf")) == float("inf")


def test_square_nan_propagates():
    result = Calculator().square(float("nan"))
    assert math.isnan(result)


def test_square_one():
    assert Calculator().square(1) == pytest.approx(1)


def test_square_does_not_mutate_input():
    x = 5
    Calculator().square(x)
    assert x == 5


# --- cube ---

def test_cube_float():
    assert Calculator().cube(1.5) == pytest.approx(3.375)


def test_cube_negative_float():
    assert Calculator().cube(-2.5) == pytest.approx(-15.625)


def test_cube_large_integer():
    assert Calculator().cube(10**6) == pytest.approx(10**18)


def test_cube_float_inf():
    assert Calculator().cube(float("inf")) == float("inf")


def test_cube_negative_float_inf():
    # (-inf)^3 == -inf
    assert Calculator().cube(float("-inf")) == float("-inf")


def test_cube_nan_propagates():
    result = Calculator().cube(float("nan"))
    assert math.isnan(result)


# --- square_root ---

def test_square_root_zero():
    # Boundary: exactly at the valid/invalid threshold
    assert Calculator().square_root(0) == pytest.approx(0.0)


def test_square_root_one():
    assert Calculator().square_root(1) == pytest.approx(1.0)


def test_square_root_float_inf():
    assert Calculator().square_root(float("inf")) == float("inf")


def test_square_root_very_small_positive():
    result = Calculator().square_root(1e-300)
    assert result == pytest.approx(math.sqrt(1e-300))


def test_square_root_large_float():
    result = Calculator().square_root(1e200)
    assert result == pytest.approx(math.sqrt(1e200))


def test_square_root_nan_propagates():
    # NaN is not < 0, so no ValueError; math.sqrt(nan) returns nan
    result = Calculator().square_root(float("nan"))
    assert math.isnan(result)


@pytest.mark.parametrize("x", [-1e-9, -1e100, -0.001])
def test_square_root_negative_parametrized(x):
    with pytest.raises(ValueError):
        Calculator().square_root(x)


# --- cube_root ---

def test_cube_root_one():
    assert Calculator().cube_root(1) == pytest.approx(1.0)


def test_cube_root_negative_one():
    assert Calculator().cube_root(-1) == pytest.approx(-1.0)


def test_cube_root_large_positive():
    assert Calculator().cube_root(10**9) == pytest.approx(1000.0)


def test_cube_root_large_negative():
    result = Calculator().cube_root(-10**9)
    assert result == pytest.approx(-1000.0)


def test_cube_root_float_inf():
    assert Calculator().cube_root(float("inf")) == float("inf")


def test_cube_root_negative_float_inf():
    assert Calculator().cube_root(float("-inf")) == float("-inf")


def test_cube_root_nan_propagates():
    result = Calculator().cube_root(float("nan"))
    assert math.isnan(result)


def test_cube_root_negative_sign_preserved():
    # Verify copysign logic: result must be negative for negative input
    result = Calculator().cube_root(-27)
    assert result < 0


# --- power ---

def test_power_zero_base_positive_exponent():
    assert Calculator().power(0, 5) == pytest.approx(0.0)


def test_power_one_base_any_exponent():
    assert Calculator().power(1, 999) == pytest.approx(1.0)


def test_power_negative_exponent():
    assert Calculator().power(2, -1) == pytest.approx(0.5)


def test_power_base_ten():
    assert Calculator().power(10, 3) == pytest.approx(1000.0)


def test_power_fractional_base():
    assert Calculator().power(0.5, 2) == pytest.approx(0.25)


def test_power_inf_exponent():
    # math.pow(2, inf) == inf
    assert Calculator().power(2, float("inf")) == float("inf")


def test_power_negative_base_fractional_exponent_raises():
    # math.pow(-2, 0.5) raises ValueError because the result is complex
    with pytest.raises(ValueError):
        Calculator().power(-2, 0.5)


@pytest.mark.parametrize("base,exp,expected", [
    (3, 0, 1.0),
    (0, 1, 0.0),
    (2, 8, 256.0),
    (10, 0, 1.0),
])
def test_power_parametrized(base, exp, expected):
    assert Calculator().power(base, exp) == pytest.approx(expected)


# --- log (base-10) ---

def test_log_one():
    # log10(1) == 0
    assert Calculator().log(1) == pytest.approx(0.0)


def test_log_ten():
    assert Calculator().log(10) == pytest.approx(1.0)


def test_log_thousand():
    assert Calculator().log(1000) == pytest.approx(3.0)


def test_log_float_inf():
    assert Calculator().log(float("inf")) == float("inf")


def test_log_very_small_positive():
    result = Calculator().log(1e-300)
    assert result == pytest.approx(math.log10(1e-300))


def test_log_large_number():
    assert Calculator().log(10**10) == pytest.approx(10.0)


def test_log_float_value():
    assert Calculator().log(0.1) == pytest.approx(-1.0)


@pytest.mark.parametrize("x", [0, -1, -1e-9, -1e100])
def test_log_non_positive_parametrized(x):
    with pytest.raises(ValueError):
        Calculator().log(x)


# --- ln (natural log) ---

def test_ln_one():
    # ln(1) == 0
    assert Calculator().ln(1) == pytest.approx(0.0)


def test_ln_float_inf():
    assert Calculator().ln(float("inf")) == float("inf")


def test_ln_very_small_positive():
    result = Calculator().ln(1e-300)
    assert result == pytest.approx(math.log(1e-300))


def test_ln_large_number():
    result = Calculator().ln(1e100)
    assert result == pytest.approx(math.log(1e100))


def test_ln_float_value():
    assert Calculator().ln(0.5) == pytest.approx(math.log(0.5))


@pytest.mark.parametrize("x", [0, -1, -1e-9, -1e100])
def test_ln_non_positive_parametrized(x):
    with pytest.raises(ValueError):
        Calculator().ln(x)


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
