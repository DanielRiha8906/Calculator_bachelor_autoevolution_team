import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(10, 0)


def test_divide_by_float_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(10, 0.0)


def test_divide_negative_numerator_by_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(-5, 0)


def test_divide_zero_by_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        calc.divide(0, 0)


def test_divide_normal_case_returns_correct_result():
    calc = Calculator()
    result = calc.divide(10, 2)
    assert result == 5.0


def test_divide_zero_numerator_nonzero_denominator_returns_zero():
    calc = Calculator()
    result = calc.divide(0, 5)
    assert result == 0.0


def test_add_positive_integers():
    calc = Calculator()
    assert calc.add(3, 4) == 7


def test_add_negative_integers():
    calc = Calculator()
    assert calc.add(-3, -4) == -7


def test_add_float_operands():
    calc = Calculator()
    assert calc.add(1.5, 2.5) == 4.0


def test_add_zero_operand():
    calc = Calculator()
    assert calc.add(0, 5) == 5


def test_subtract_positive_result():
    calc = Calculator()
    assert calc.subtract(10, 3) == 7


def test_subtract_negative_result():
    calc = Calculator()
    assert calc.subtract(3, 10) == -7


def test_subtract_zero_result():
    calc = Calculator()
    assert calc.subtract(5, 5) == 0


def test_subtract_float_operands():
    calc = Calculator()
    assert calc.subtract(5.5, 2.5) == 3.0


def test_multiply_positive_integers():
    calc = Calculator()
    assert calc.multiply(3, 4) == 12


def test_multiply_negative_integers():
    calc = Calculator()
    assert calc.multiply(-3, 4) == -12


def test_multiply_zero_multiplier():
    calc = Calculator()
    assert calc.multiply(5, 0) == 0


def test_multiply_float_operands():
    calc = Calculator()
    assert calc.multiply(2.5, 4.0) == 10.0


# ---------------------------------------------------------------------------
# add – additional edge cases
# ---------------------------------------------------------------------------

def test_add_both_zero():
    calc = Calculator()
    assert calc.add(0, 0) == 0


def test_add_mixed_sign():
    calc = Calculator()
    assert calc.add(-5, 3) == -2


def test_add_large_integers():
    calc = Calculator()
    assert calc.add(10**18, 10**18) == 2 * 10**18


def test_add_float_precision_known_inexact():
    # 0.1 + 0.2 is a well-known IEEE-754 inexactness; use math.isclose
    calc = Calculator()
    result = calc.add(0.1, 0.2)
    assert math.isclose(result, 0.3, rel_tol=1e-9)


def test_add_float_and_int():
    calc = Calculator()
    assert calc.add(1, 0.5) == 1.5


def test_add_none_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.add(None, 1)


def test_add_string_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.add("a", 1)


def test_add_negative_and_positive_cancel():
    calc = Calculator()
    assert calc.add(7, -7) == 0


# ---------------------------------------------------------------------------
# subtract – additional edge cases
# ---------------------------------------------------------------------------

def test_subtract_both_zero():
    calc = Calculator()
    assert calc.subtract(0, 0) == 0


def test_subtract_negative_minus_negative():
    calc = Calculator()
    assert calc.subtract(-3, -8) == 5


def test_subtract_large_integers():
    calc = Calculator()
    assert calc.subtract(10**18, 1) == 10**18 - 1


def test_subtract_float_precision_known_inexact():
    calc = Calculator()
    result = calc.subtract(0.3, 0.1)
    assert math.isclose(result, 0.2, rel_tol=1e-9)


def test_subtract_none_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.subtract(None, 1)


def test_subtract_string_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.subtract("a", 1)


def test_subtract_zero_from_negative():
    calc = Calculator()
    assert calc.subtract(-5, 0) == -5


# ---------------------------------------------------------------------------
# multiply – additional edge cases
# ---------------------------------------------------------------------------

def test_multiply_both_negative_gives_positive():
    calc = Calculator()
    assert calc.multiply(-3, -4) == 12


def test_multiply_by_one_identity():
    calc = Calculator()
    assert calc.multiply(99, 1) == 99


def test_multiply_by_negative_one():
    calc = Calculator()
    assert calc.multiply(7, -1) == -7


def test_multiply_both_zero():
    calc = Calculator()
    assert calc.multiply(0, 0) == 0


def test_multiply_large_integers():
    calc = Calculator()
    assert calc.multiply(10**9, 10**9) == 10**18


def test_multiply_float_precision_known_inexact():
    calc = Calculator()
    result = calc.multiply(0.1, 3)
    assert math.isclose(result, 0.3, rel_tol=1e-9)


def test_multiply_none_raises_type_error():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.multiply(None, 2)


def test_multiply_string_raises_type_error():
    # "a" * 2 is valid Python (string repetition), but "a" * "b" is not.
    # Use two string operands to guarantee a TypeError from the * operator.
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.multiply("a", "b")


# ---------------------------------------------------------------------------
# factorial
# ---------------------------------------------------------------------------

def test_factorial_zero_returns_one():
    calc = Calculator()
    assert calc.factorial(0) == 1


def test_factorial_one_returns_one():
    calc = Calculator()
    assert calc.factorial(1) == 1


def test_factorial_five_returns_120():
    calc = Calculator()
    assert calc.factorial(5) == 120


def test_factorial_large_integer_returns_correct_result():
    calc = Calculator()
    assert calc.factorial(10) == math.factorial(10)


def test_factorial_negative_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.factorial(-1)


def test_factorial_float_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.factorial(1.5)


# ---------------------------------------------------------------------------
# square
# ---------------------------------------------------------------------------

def test_square_positive_integer():
    calc = Calculator()
    assert calc.square(4) == 16


def test_square_zero():
    calc = Calculator()
    assert calc.square(0) == 0


def test_square_negative_integer_returns_positive():
    calc = Calculator()
    assert calc.square(-3) == 9


def test_square_float_operand():
    calc = Calculator()
    assert math.isclose(calc.square(2.5), 6.25)


# ---------------------------------------------------------------------------
# cube
# ---------------------------------------------------------------------------

def test_cube_positive_integer():
    calc = Calculator()
    assert calc.cube(3) == 27


def test_cube_zero():
    calc = Calculator()
    assert calc.cube(0) == 0


def test_cube_negative_integer_returns_negative():
    calc = Calculator()
    assert calc.cube(-2) == -8


def test_cube_float_operand():
    calc = Calculator()
    assert math.isclose(calc.cube(1.5), 3.375)


# ---------------------------------------------------------------------------
# square_root
# ---------------------------------------------------------------------------

def test_square_root_perfect_square():
    calc = Calculator()
    assert calc.square_root(9) == 3.0


def test_square_root_non_perfect_square():
    calc = Calculator()
    assert math.isclose(calc.square_root(2), math.sqrt(2))


def test_square_root_zero():
    calc = Calculator()
    assert calc.square_root(0) == 0.0


def test_square_root_negative_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="non-negative"):
        calc.square_root(-1)


# ---------------------------------------------------------------------------
# cube_root
# ---------------------------------------------------------------------------

def test_cube_root_perfect_cube():
    calc = Calculator()
    assert math.isclose(calc.cube_root(27), 3.0)


def test_cube_root_zero():
    calc = Calculator()
    assert calc.cube_root(0) == 0.0


def test_cube_root_negative_input_returns_negative():
    calc = Calculator()
    assert math.isclose(calc.cube_root(-8), -2.0)


def test_cube_root_float_operand():
    calc = Calculator()
    assert math.isclose(calc.cube_root(2.0), math.cbrt(2.0))


# ---------------------------------------------------------------------------
# power
# ---------------------------------------------------------------------------

def test_power_integer_base_and_exponent():
    calc = Calculator()
    assert calc.power(2, 10) == 1024


def test_power_zero_exponent_returns_one():
    calc = Calculator()
    assert calc.power(5, 0) == 1


def test_power_exponent_of_one_returns_base():
    calc = Calculator()
    assert calc.power(7, 1) == 7


def test_power_negative_exponent():
    calc = Calculator()
    assert calc.power(2, -1) == 0.5


def test_power_float_base_and_exponent():
    calc = Calculator()
    assert math.isclose(calc.power(2.0, 0.5), math.sqrt(2.0))


# ---------------------------------------------------------------------------
# log (base-10)
# ---------------------------------------------------------------------------

def test_log_100_returns_two():
    calc = Calculator()
    assert calc.log(100) == 2.0


def test_log_one_returns_zero():
    calc = Calculator()
    assert calc.log(1) == 0.0


def test_log_non_power_of_ten():
    calc = Calculator()
    assert math.isclose(calc.log(50), math.log10(50))


def test_log_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.log(0)


def test_log_negative_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.log(-5)


# ---------------------------------------------------------------------------
# ln (natural logarithm)
# ---------------------------------------------------------------------------

def test_ln_one_returns_zero():
    calc = Calculator()
    assert calc.ln(1) == 0.0


def test_ln_e_returns_approx_one():
    calc = Calculator()
    assert math.isclose(calc.ln(math.e), 1.0)


def test_ln_non_trivial_positive():
    calc = Calculator()
    assert math.isclose(calc.ln(10), math.log(10))


def test_ln_zero_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.ln(0)


def test_ln_negative_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.ln(-1)


# ---------------------------------------------------------------------------
# square – supplementary edge cases
# ---------------------------------------------------------------------------

def test_square_negative_zero_returns_zero():
    # -0.0 ** 2 == 0.0 (IEEE-754: sign is lost when squaring)
    calc = Calculator()
    assert calc.square(-0.0) == 0.0


def test_square_one_returns_one():
    calc = Calculator()
    assert calc.square(1) == 1


def test_square_minus_one_returns_one():
    calc = Calculator()
    assert calc.square(-1) == 1


def test_square_infinity_returns_infinity():
    calc = Calculator()
    assert calc.square(float('inf')) == float('inf')


def test_square_negative_infinity_returns_infinity():
    calc = Calculator()
    assert calc.square(float('-inf')) == float('inf')


def test_square_nan_returns_nan():
    calc = Calculator()
    assert math.isnan(calc.square(float('nan')))


def test_square_large_integer():
    calc = Calculator()
    assert calc.square(10**9) == 10**18


def test_square_very_small_float():
    calc = Calculator()
    assert math.isclose(calc.square(1e-150), 1e-300)


# ---------------------------------------------------------------------------
# cube – supplementary edge cases
# ---------------------------------------------------------------------------

def test_cube_negative_zero_returns_negative_zero():
    # -0.0 ** 3 == -0.0  (sign is preserved for odd powers)
    calc = Calculator()
    result = calc.cube(-0.0)
    assert result == 0.0 and math.copysign(1, result) == -1.0


def test_cube_one_returns_one():
    calc = Calculator()
    assert calc.cube(1) == 1


def test_cube_minus_one_returns_minus_one():
    calc = Calculator()
    assert calc.cube(-1) == -1


def test_cube_infinity_returns_infinity():
    calc = Calculator()
    assert calc.cube(float('inf')) == float('inf')


def test_cube_negative_infinity_returns_negative_infinity():
    calc = Calculator()
    assert calc.cube(float('-inf')) == float('-inf')


def test_cube_nan_returns_nan():
    calc = Calculator()
    assert math.isnan(calc.cube(float('nan')))


def test_cube_large_integer():
    calc = Calculator()
    assert calc.cube(10**6) == 10**18


# ---------------------------------------------------------------------------
# square_root – supplementary edge cases
# ---------------------------------------------------------------------------

def test_square_root_negative_zero_returns_zero():
    # -0.0 >= 0 so no ValueError; math.sqrt(-0.0) returns -0.0
    # We just require it doesn't raise and returns a value equal to 0.0
    calc = Calculator()
    result = calc.square_root(-0.0)
    assert result == 0.0


def test_square_root_infinity_returns_infinity():
    calc = Calculator()
    assert calc.square_root(float('inf')) == float('inf')


def test_square_root_nan_returns_nan():
    calc = Calculator()
    assert math.isnan(calc.square_root(float('nan')))


def test_square_root_large_perfect_square():
    calc = Calculator()
    assert calc.square_root(10**18) == 10**9


def test_square_root_negative_raises_value_error_message():
    # Verify the error message contains the word "non-negative"
    calc = Calculator()
    with pytest.raises(ValueError, match="non-negative"):
        calc.square_root(-0.001)


def test_square_root_very_negative_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="non-negative"):
        calc.square_root(-1e300)


# ---------------------------------------------------------------------------
# cube_root – supplementary edge cases
# ---------------------------------------------------------------------------

def test_cube_root_negative_eight_exact():
    # Exact check: cbrt(-8) must be exactly -2.0, not complex or wrong-signed
    calc = Calculator()
    result = calc.cube_root(-8)
    assert result == -2.0


def test_cube_root_negative_zero():
    # cbrt(-0.0) returns -0.0
    calc = Calculator()
    result = calc.cube_root(-0.0)
    assert result == 0.0


def test_cube_root_infinity():
    calc = Calculator()
    assert calc.cube_root(float('inf')) == float('inf')


def test_cube_root_negative_infinity():
    calc = Calculator()
    assert calc.cube_root(float('-inf')) == float('-inf')


def test_cube_root_nan_returns_nan():
    calc = Calculator()
    assert math.isnan(calc.cube_root(float('nan')))


def test_cube_root_very_large_positive():
    # cbrt(1e300) == 1e100
    calc = Calculator()
    assert math.isclose(calc.cube_root(1e300), 1e100, rel_tol=1e-9)


def test_cube_root_very_large_negative():
    calc = Calculator()
    assert math.isclose(calc.cube_root(-1e300), -1e100, rel_tol=1e-9)


def test_cube_root_one_returns_one():
    calc = Calculator()
    assert math.isclose(calc.cube_root(1), 1.0)


def test_cube_root_minus_one_returns_minus_one():
    calc = Calculator()
    assert math.isclose(calc.cube_root(-1), -1.0)


# ---------------------------------------------------------------------------
# power – supplementary edge cases
# ---------------------------------------------------------------------------

def test_power_zero_to_zero_returns_one():
    # Python defines 0**0 == 1 (integer convention)
    calc = Calculator()
    assert calc.power(0, 0) == 1


def test_power_float_zero_to_zero_returns_one():
    calc = Calculator()
    assert calc.power(0.0, 0) == 1.0


def test_power_zero_base_positive_exponent_returns_zero():
    calc = Calculator()
    assert calc.power(0, 5) == 0


def test_power_zero_base_negative_exponent_raises():
    # 0 ** -1 raises ZeroDivisionError in Python
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.power(0, -1)


def test_power_very_large_integer_exponent():
    # 2**1000 is a valid Python big integer — no overflow
    calc = Calculator()
    assert calc.power(2, 1000) == 2**1000


def test_power_float_large_exponent_raises_overflow():
    # 2.0 ** 1e300 overflows float representation
    calc = Calculator()
    with pytest.raises(OverflowError):
        calc.power(2.0, 1e300)


def test_power_negative_base_even_exponent_positive():
    calc = Calculator()
    assert calc.power(-3, 2) == 9


def test_power_negative_base_odd_exponent_negative():
    calc = Calculator()
    assert calc.power(-2, 3) == -8


def test_power_infinity_base_positive_exponent():
    calc = Calculator()
    assert calc.power(float('inf'), 2) == float('inf')


def test_power_infinity_exponent_base_greater_than_one():
    calc = Calculator()
    assert calc.power(2.0, float('inf')) == float('inf')


def test_power_any_base_zero_exponent_returns_one():
    # Including inf**0 and nan**0 — Python returns 1.0 for these
    calc = Calculator()
    assert calc.power(float('inf'), 0) == 1.0
    assert calc.power(float('nan'), 0) == 1.0


def test_power_one_to_any_exponent_returns_one():
    calc = Calculator()
    assert calc.power(1, 10**9) == 1


# ---------------------------------------------------------------------------
# log (base-10) – supplementary edge cases
# ---------------------------------------------------------------------------

def test_log_zero_raises_value_error_message_contains_positive():
    calc = Calculator()
    with pytest.raises(ValueError, match="positive"):
        calc.log(0)


def test_log_negative_raises_value_error_message_contains_positive():
    calc = Calculator()
    with pytest.raises(ValueError, match="positive"):
        calc.log(-1)


def test_log_negative_float_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="positive"):
        calc.log(-0.001)


def test_log_very_small_positive_returns_large_negative():
    # log10(1e-300) == -300
    calc = Calculator()
    assert math.isclose(calc.log(1e-300), -300.0, rel_tol=1e-9)


def test_log_ten_returns_one():
    calc = Calculator()
    assert math.isclose(calc.log(10), 1.0)


def test_log_infinity_returns_infinity():
    calc = Calculator()
    assert calc.log(float('inf')) == float('inf')


def test_log_nan_returns_nan():
    calc = Calculator()
    assert math.isnan(calc.log(float('nan')))


def test_log_negative_zero_raises_value_error():
    # -0.0 <= 0, so must raise
    calc = Calculator()
    with pytest.raises(ValueError, match="positive"):
        calc.log(-0.0)


# ---------------------------------------------------------------------------
# ln (natural logarithm) – supplementary edge cases
# ---------------------------------------------------------------------------

def test_ln_zero_raises_value_error_message_contains_positive():
    calc = Calculator()
    with pytest.raises(ValueError, match="positive"):
        calc.ln(0)


def test_ln_negative_raises_value_error_message_contains_positive():
    calc = Calculator()
    with pytest.raises(ValueError, match="positive"):
        calc.ln(-1)


def test_ln_negative_float_raises_value_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="positive"):
        calc.ln(-0.001)


def test_ln_very_small_positive_is_large_negative():
    # ln(1e-300) ≈ -690.78
    calc = Calculator()
    assert math.isclose(calc.ln(1e-300), math.log(1e-300), rel_tol=1e-9)


def test_ln_infinity_returns_infinity():
    calc = Calculator()
    assert calc.ln(float('inf')) == float('inf')


def test_ln_nan_returns_nan():
    calc = Calculator()
    assert math.isnan(calc.ln(float('nan')))


def test_ln_negative_zero_raises_value_error():
    # -0.0 <= 0, so must raise
    calc = Calculator()
    with pytest.raises(ValueError, match="positive"):
        calc.ln(-0.0)