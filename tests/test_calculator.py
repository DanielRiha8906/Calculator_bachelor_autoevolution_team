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