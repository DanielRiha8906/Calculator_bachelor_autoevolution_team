import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero():
    """Assert that dividing by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        Calculator().divide(1, 0)
    with pytest.raises(ZeroDivisionError):
        Calculator().divide(1.0, 0.0)


# ---------------------------------------------------------------------------
# Edge-case tests for Calculator.divide — zero-divisor scenarios
# ---------------------------------------------------------------------------

@pytest.fixture
def calc():
    return Calculator()


@pytest.mark.parametrize("numerator", [-1, -1000, -(10**18)])
def test_divide_negative_int_numerator_int_zero(calc, numerator):
    """Negative integer numerators with an integer zero divisor still raise."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(numerator, 0)


@pytest.mark.parametrize("numerator", [-1.0, -0.001, -1e308])
def test_divide_negative_float_numerator_float_zero(calc, numerator):
    """Negative float numerators with a float zero divisor still raise."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(numerator, 0.0)


def test_divide_zero_numerator_int_zero(calc):
    """0 / 0 with integer operands must raise ZeroDivisionError (not return NaN)."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(0, 0)


def test_divide_zero_numerator_float_zero(calc):
    """0.0 / 0.0 must raise ZeroDivisionError (Python does not return NaN here)."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(0.0, 0.0)


def test_divide_large_int_numerator_int_zero(calc):
    """Very large integer numerator does not change zero-divisor behavior."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(10**18, 0)


def test_divide_large_float_numerator_float_zero(calc):
    """Very large float numerator does not change zero-divisor behavior."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(1e308, 0.0)


def test_divide_inf_numerator_float_zero(calc):
    """float('inf') as numerator with float zero divisor raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(float("inf"), 0.0)


def test_divide_negative_float_zero_divisor(calc):
    """IEEE 754 negative zero (-0.0) as divisor is still treated as zero by Python."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(1.0, -0.0)


def test_divide_negative_float_zero_divisor_negative_numerator(calc):
    """-0.0 divisor with a negative numerator still raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        calc.divide(-1.0, -0.0)


# ---------------------------------------------------------------------------
# Happy-path tests for Calculator.divide (non-zero denominators)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5.0),
    (-10, 2, -5.0),
    (10, -2, -5.0),
    (-10, -2, 5.0),
    (1, 3, 1 / 3),
    (0, 5, 0.0),
    (1e10, 1e5, 1e5),
])
def test_divide_normal_cases(calc, a, b, expected):
    """Normal division cases return the correct quotient."""
    result = calc.divide(a, b)
    assert math.isclose(result, expected, rel_tol=1e-9), (
        f"divide({a}, {b}) returned {result!r}, expected {expected!r}"
    )


def test_divide_result_is_float_for_int_operands(calc):
    """Python's / operator always returns a float, even for integer operands."""
    result = calc.divide(10, 2)
    assert isinstance(result, float)


def test_divide_does_not_mutate_inputs(calc):
    """divide must be side-effect-free on its arguments."""
    a, b = 6, 3
    calc.divide(a, b)
    assert a == 6
    assert b == 3


# ---------------------------------------------------------------------------
# Tests for Calculator.add
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 5, 5),
    (5, 0, 5),
    (-3, -4, -7),
    (-3, 5, 2),
    (10**18, 1, 10**18 + 1),
    (0.1, 0.2, 0.3),
])
def test_add_cases(calc, a, b, expected):
    """add returns the correct sum across a range of operand types and signs."""
    result = calc.add(a, b)
    assert math.isclose(result, expected, rel_tol=1e-9), (
        f"add({a}, {b}) returned {result!r}, expected {expected!r}"
    )


def test_add_does_not_mutate_inputs(calc):
    """add must be side-effect-free on its arguments."""
    a, b = 4, 7
    calc.add(a, b)
    assert a == 4
    assert b == 7


# ---------------------------------------------------------------------------
# Tests for Calculator.subtract
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("a, b, expected", [
    (10, 3, 7),
    (3, 10, -7),
    (5, 0, 5),
    (-3, -4, 1),
    (1.5, 0.5, 1.0),
    (10**18, 1, 10**18 - 1),
])
def test_subtract_cases(calc, a, b, expected):
    """subtract returns the correct difference across a range of operand types and signs."""
    result = calc.subtract(a, b)
    assert math.isclose(result, expected, rel_tol=1e-9), (
        f"subtract({a}, {b}) returned {result!r}, expected {expected!r}"
    )


def test_subtract_does_not_mutate_inputs(calc):
    """subtract must be side-effect-free on its arguments."""
    a, b = 9, 4
    calc.subtract(a, b)
    assert a == 9
    assert b == 4


# ---------------------------------------------------------------------------
# Tests for Calculator.multiply
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("a, b, expected", [
    (3, 4, 12),
    (5, 0, 0),
    (-3, 4, -12),
    (-3, -4, 12),
    (7, 1, 7),
    (0.5, 4.0, 2.0),
    (10**9, 10**9, 10**18),
])
def test_multiply_cases(calc, a, b, expected):
    """multiply returns the correct product across a range of operand types and signs."""
    result = calc.multiply(a, b)
    assert math.isclose(result, expected, rel_tol=1e-9), (
        f"multiply({a}, {b}) returned {result!r}, expected {expected!r}"
    )


def test_multiply_does_not_mutate_inputs(calc):
    """multiply must be side-effect-free on its arguments."""
    a, b = 3, 8
    calc.multiply(a, b)
    assert a == 3
    assert b == 8


# ---------------------------------------------------------------------------
# Tests for Calculator.factorial
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("n, expected", [
    (0, 1),
    (1, 1),
    (5, 120),
    (10, 3628800),
])
def test_factorial_happy_path(calc, n, expected):
    """factorial returns the correct value for valid non-negative integers."""
    assert calc.factorial(n) == expected, (
        f"factorial({n}) returned {calc.factorial(n)!r}, expected {expected!r}"
    )


def test_factorial_returns_int(calc):
    """factorial must return an int for valid input."""
    result = calc.factorial(5)
    assert isinstance(result, int)


@pytest.mark.parametrize("n", [-1, -5, -100])
def test_factorial_negative_raises_value_error(calc, n):
    """factorial raises ValueError for negative integer arguments."""
    with pytest.raises(ValueError):
        calc.factorial(n)


@pytest.mark.parametrize("n", [1.0, 2.5, "5", None, True, False])
def test_factorial_invalid_type_raises_type_error(calc, n):
    """factorial raises TypeError for non-integer arguments, including booleans."""
    with pytest.raises(TypeError):
        calc.factorial(n)


# ---------------------------------------------------------------------------
# Additional edge-case tests for Calculator.factorial
# ---------------------------------------------------------------------------

def test_factorial_zero_explicit_boundary(calc):
    """factorial(0) is the lower boundary — must return exactly 1, not 0."""
    assert calc.factorial(0) == 1


def test_factorial_large_value(calc):
    """factorial(20) must return the known exact integer 2432902008176640000."""
    assert calc.factorial(20) == 2432902008176640000


def test_factorial_large_value_is_int(calc):
    """factorial(20) must be a plain Python int, not float or any other numeric type."""
    result = calc.factorial(20)
    assert type(result) is int


def test_factorial_very_large_value(calc):
    """factorial accepts large integers and returns the correct big integer."""
    result = calc.factorial(50)
    assert result == math.factorial(50)
    assert type(result) is int


def test_factorial_result_is_always_int_at_boundary(calc):
    """factorial(1) — the second boundary — must return plain int 1."""
    result = calc.factorial(1)
    assert type(result) is int
    assert result == 1


@pytest.mark.parametrize("n", [[], [1, 2], {}, set(), (1,)])
def test_factorial_collection_types_raise_type_error(calc, n):
    """factorial raises TypeError when passed any collection type."""
    with pytest.raises(TypeError):
        calc.factorial(n)


def test_factorial_complex_number_raises_type_error(calc):
    """factorial raises TypeError for a complex number argument."""
    with pytest.raises(TypeError):
        calc.factorial(3 + 0j)


def test_factorial_negative_float_raises_type_error(calc):
    """A negative float like -1.0 must raise TypeError (not ValueError) because
    the type check runs before the sign check."""
    with pytest.raises(TypeError):
        calc.factorial(-1.0)


def test_factorial_negative_zero_float_raises_type_error(calc):
    """The IEEE 754 negative zero float (-0.0) is not an int and must raise TypeError."""
    with pytest.raises(TypeError):
        calc.factorial(-0.0)


def test_factorial_positive_zero_float_raises_type_error(calc):
    """0.0 is a float, not an int; must raise TypeError even though the value is zero."""
    with pytest.raises(TypeError):
        calc.factorial(0.0)


def test_factorial_inf_raises_type_error(calc):
    """float('inf') is not an int and must raise TypeError."""
    with pytest.raises(TypeError):
        calc.factorial(float("inf"))


def test_factorial_nan_raises_type_error(calc):
    """float('nan') is not an int and must raise TypeError."""
    with pytest.raises(TypeError):
        calc.factorial(float("nan"))


def test_factorial_does_not_mutate_input(calc):
    """factorial must be side-effect-free; passing a name-bound int must leave it unchanged."""
    n = 5
    calc.factorial(n)
    assert n == 5


def test_factorial_type_error_message_contains_type_name(calc):
    """TypeError raised for a float must mention the received type in its message."""
    with pytest.raises(TypeError, match="float"):
        calc.factorial(2.5)


def test_factorial_type_error_for_bool_mentions_boolean(calc):
    """TypeError raised for a boolean must mention 'bool' in its message."""
    with pytest.raises(TypeError, match="bool"):
        calc.factorial(True)


def test_factorial_value_error_message_contains_value(calc):
    """ValueError raised for a negative int must mention the offending value."""
    with pytest.raises(ValueError, match="-3"):
        calc.factorial(-3)


@pytest.mark.parametrize("n, expected", [
    (2, 2),
    (3, 6),
    (4, 24),
    (6, 720),
    (7, 5040),
])
def test_factorial_additional_happy_path(calc, n, expected):
    """Extend happy-path coverage across several small integers not in the base suite."""
    assert calc.factorial(n) == expected


# ---------------------------------------------------------------------------
# Tests for Calculator.square
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("x, expected", [
    (0, 0),
    (1, 1),
    (2, 4),
    (-3, 9),
    (0.5, 0.25),
    (-1.5, 2.25),
])
def test_square_happy_path(calc, x, expected):
    """square returns x**2 for valid inputs spanning zero, positive, negative, and float."""
    result = calc.square(x)
    assert math.isclose(result, expected, rel_tol=1e-9), (
        f"square({x}) returned {result!r}, expected {expected!r}"
    )


def test_square_zero_returns_zero(calc):
    """square(0) must return exactly 0, the additive identity boundary."""
    assert calc.square(0) == 0


def test_square_negative_returns_positive(calc):
    """Squaring any negative number must yield a non-negative result."""
    assert calc.square(-7) >= 0


def test_square_large_integer(calc):
    """square handles very large integers without overflow."""
    result = calc.square(10 ** 9)
    assert result == 10 ** 18


def test_square_does_not_mutate_input(calc):
    """square must be side-effect-free on its argument."""
    x = 5
    calc.square(x)
    assert x == 5


# ---------------------------------------------------------------------------
# Tests for Calculator.cube
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("x, expected", [
    (0, 0),
    (1, 1),
    (2, 8),
    (-2, -8),
    (0.5, 0.125),
    (-1.5, -3.375),
])
def test_cube_happy_path(calc, x, expected):
    """cube returns x**3 for valid inputs spanning zero, positive, negative, and float."""
    result = calc.cube(x)
    assert math.isclose(result, expected, rel_tol=1e-9), (
        f"cube({x}) returned {result!r}, expected {expected!r}"
    )


def test_cube_zero_returns_zero(calc):
    """cube(0) must return exactly 0."""
    assert calc.cube(0) == 0


def test_cube_preserves_sign_of_negative(calc):
    """Cubing a negative number must yield a negative result."""
    assert calc.cube(-3) < 0


def test_cube_large_integer(calc):
    """cube handles very large integers without overflow."""
    result = calc.cube(10 ** 6)
    assert result == 10 ** 18


def test_cube_does_not_mutate_input(calc):
    """cube must be side-effect-free on its argument."""
    x = 4
    calc.cube(x)
    assert x == 4


# ---------------------------------------------------------------------------
# Tests for Calculator.square_root
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("x, expected", [
    (0, 0.0),
    (1, 1.0),
    (4, 2.0),
    (9, 3.0),
    (0.25, 0.5),
])
def test_square_root_happy_path(calc, x, expected):
    """square_root returns math.sqrt(x) for valid non-negative inputs."""
    result = calc.square_root(x)
    assert math.isclose(result, expected, rel_tol=1e-9), (
        f"square_root({x}) returned {result!r}, expected {expected!r}"
    )


@pytest.mark.parametrize("x", [-1, -0.001, -1e10])
def test_square_root_negative_raises_value_error(calc, x):
    """square_root raises ValueError for any negative input."""
    with pytest.raises(ValueError):
        calc.square_root(x)


@pytest.mark.parametrize("x", [-1, -0.001, -1e10])
def test_square_root_error_message_contains_value(calc, x):
    """ValueError message for negative input must contain the offending value."""
    with pytest.raises(ValueError, match=str(x)):
        calc.square_root(x)


def test_square_root_zero_boundary(calc):
    """square_root(0) is the exact lower boundary and must return 0.0, not raise."""
    assert calc.square_root(0) == 0.0


def test_square_root_large_value(calc):
    """square_root handles large inputs correctly."""
    result = calc.square_root(1e16)
    assert math.isclose(result, 1e8, rel_tol=1e-9)


def test_square_root_does_not_mutate_input(calc):
    """square_root must be side-effect-free on its argument."""
    x = 9
    calc.square_root(x)
    assert x == 9


# ---------------------------------------------------------------------------
# Tests for Calculator.cube_root
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("x, expected", [
    (0, 0.0),
    (1, 1.0),
    (8, 2.0),
    (-8, -2.0),
    (27, 3.0),
    (-27, -3.0),
])
def test_cube_root_happy_path(calc, x, expected):
    """cube_root returns the real cube root for positive, negative, and zero inputs."""
    result = calc.cube_root(x)
    assert math.isclose(result, expected, rel_tol=1e-9), (
        f"cube_root({x}) returned {result!r}, expected {expected!r}"
    )


def test_cube_root_negative_eight_exact(calc):
    """cube_root(-8) must equal -2.0 exactly — validates math.cbrt usage, not x**(1/3)."""
    result = calc.cube_root(-8)
    assert result == -2.0, (
        f"cube_root(-8) returned {result!r}; expected -2.0 (requires math.cbrt)"
    )


def test_cube_root_zero_returns_zero(calc):
    """cube_root(0) must return 0.0 without raising."""
    assert calc.cube_root(0) == 0.0


def test_cube_root_large_positive(calc):
    """cube_root handles large positive values correctly."""
    result = calc.cube_root(1e9)
    assert math.isclose(result, 1000.0, rel_tol=1e-9)


def test_cube_root_large_negative(calc):
    """cube_root handles large negative values, returning the negative real root."""
    result = calc.cube_root(-1e9)
    assert math.isclose(result, -1000.0, rel_tol=1e-9)


def test_cube_root_does_not_mutate_input(calc):
    """cube_root must be side-effect-free on its argument."""
    x = 27
    calc.cube_root(x)
    assert x == 27


# ---------------------------------------------------------------------------
# Tests for Calculator.log10
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("x, expected", [
    (1, 0.0),
    (10, 1.0),
    (100, 2.0),
    (0.1, -1.0),
    (1000, 3.0),
])
def test_log10_happy_path(calc, x, expected):
    """log10 returns math.log10(x) for valid positive inputs."""
    result = calc.log10(x)
    assert math.isclose(result, expected, rel_tol=1e-9), (
        f"log10({x}) returned {result!r}, expected {expected!r}"
    )


@pytest.mark.parametrize("x", [0, -1, -100])
def test_log10_non_positive_raises_value_error(calc, x):
    """log10 raises ValueError for x <= 0."""
    with pytest.raises(ValueError):
        calc.log10(x)


@pytest.mark.parametrize("x", [0, -1, -100])
def test_log10_error_message_contains_value(calc, x):
    """ValueError message for x <= 0 must contain the offending value."""
    with pytest.raises(ValueError, match=str(x)):
        calc.log10(x)


def test_log10_very_small_positive(calc):
    """log10 of a very small positive number returns a large negative value."""
    result = calc.log10(1e-10)
    assert math.isclose(result, -10.0, rel_tol=1e-9)


def test_log10_large_value(calc):
    """log10 handles large inputs without raising."""
    result = calc.log10(1e100)
    assert math.isclose(result, 100.0, rel_tol=1e-9)


def test_log10_does_not_mutate_input(calc):
    """log10 must be side-effect-free on its argument."""
    x = 100
    calc.log10(x)
    assert x == 100


# ---------------------------------------------------------------------------
# Tests for Calculator.ln
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("x, expected", [
    (1, 0.0),
    (math.e, 1.0),
    (math.e ** 2, 2.0),
])
def test_ln_happy_path(calc, x, expected):
    """ln returns math.log(x) for valid positive inputs."""
    result = calc.ln(x)
    assert math.isclose(result, expected, rel_tol=1e-9), (
        f"ln({x}) returned {result!r}, expected {expected!r}"
    )


@pytest.mark.parametrize("x", [0, -1, -1e10])
def test_ln_non_positive_raises_value_error(calc, x):
    """ln raises ValueError for x <= 0."""
    with pytest.raises(ValueError):
        calc.ln(x)


@pytest.mark.parametrize("x", [0, -1, -1e10])
def test_ln_error_message_contains_value(calc, x):
    """ValueError message for x <= 0 must contain the offending value."""
    with pytest.raises(ValueError, match=str(x)):
        calc.ln(x)


def test_ln_very_small_positive(calc):
    """ln of a very small positive number returns a large negative value."""
    result = calc.ln(1e-10)
    assert math.isclose(result, -10 * math.log(10), rel_tol=1e-9)


def test_ln_large_value(calc):
    """ln handles large inputs without raising."""
    result = calc.ln(math.e ** 100)
    assert math.isclose(result, 100.0, rel_tol=1e-6)


def test_ln_does_not_mutate_input(calc):
    """ln must be side-effect-free on its argument."""
    x = math.e
    calc.ln(x)
    assert math.isclose(x, math.e)


# ---------------------------------------------------------------------------
# Tests for Calculator.power
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("x, y, expected", [
    (2, 3, 8),
    (3, 2, 9),
    (2, 0, 1),
    (0, 5, 0),
    (2, -1, 0.5),
    (4, 0.5, 2.0),
    (-2, 3, -8),
])
def test_power_happy_path(calc, x, y, expected):
    """power returns x**y for valid inputs spanning positive, negative, zero exponents."""
    result = calc.power(x, y)
    assert math.isclose(result, expected, rel_tol=1e-9), (
        f"power({x}, {y}) returned {result!r}, expected {expected!r}"
    )


def test_power_zero_base_negative_exponent_raises_zero_division_error(calc):
    """power(0, -1) raises ZeroDivisionError — native Python behavior with no guard needed."""
    with pytest.raises(ZeroDivisionError):
        calc.power(0, -1)


def test_power_identity_exponent_one(calc):
    """Any base raised to the power 1 equals the base."""
    assert calc.power(7, 1) == 7


def test_power_base_one_any_exponent(calc):
    """1 raised to any exponent must equal 1."""
    assert calc.power(1, 1000) == 1


def test_power_fractional_exponent(calc):
    """power supports fractional exponents, e.g. 27**(1/3) ~= 3.0."""
    result = calc.power(27, 1 / 3)
    assert math.isclose(result, 3.0, rel_tol=1e-9)


def test_power_large_exponent(calc):
    """power handles large integer exponents correctly."""
    result = calc.power(2, 10)
    assert result == 1024


def test_power_does_not_mutate_inputs(calc):
    """power must be side-effect-free on its arguments."""
    x, y = 3, 4
    calc.power(x, y)
    assert x == 3
    assert y == 4