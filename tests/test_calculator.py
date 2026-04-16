import pytest
import math
from src.calculator import Calculator


def test_divide_by_zero():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(1, 0)
    with pytest.raises(ZeroDivisionError):
        calc.divide(-5, 0)


@pytest.mark.parametrize("numerator,denominator", [
    (1, 0.0),       # float zero denominator
    (1.0, 0.0),     # both floats, zero denominator
    (1, 0j),        # complex zero denominator
])
def test_divide_by_zero_alternate_zero_types(numerator, denominator):
    """Verify ZeroDivisionError is raised for non-integer representations of zero as divisor."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(numerator, denominator)


# Section 1 — Integer happy path (parametrized)

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add_integers(a, b, expected):
    calc = Calculator()
    assert calc.add(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (10, 3, 7),
    (0, 0, 0),
    (3, 10, -7),
    (-5, -3, -2),
])
def test_subtract_integers(a, b, expected):
    calc = Calculator()
    assert calc.subtract(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (3, 4, 12),
    (0, 99, 0),
    (-3, 4, -12),
    (-3, -4, 12),
])
def test_multiply_integers(a, b, expected):
    calc = Calculator()
    assert calc.multiply(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5.0),
    (9, 3, 3.0),
    (-6, 2, -3.0),
    (7, 1, 7.0),
])
def test_divide_integers(a, b, expected):
    calc = Calculator()
    assert calc.divide(a, b) == expected


# Section 2 — Float inputs (use pytest.approx)

@pytest.mark.parametrize("a, b, expected", [
    (0.1, 0.2, pytest.approx(0.3)),
    (1.5, 2.5, pytest.approx(4.0)),
    (-1.1, 0.1, pytest.approx(-1.0)),
])
def test_add_floats(a, b, expected):
    calc = Calculator()
    assert calc.add(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (5.5, 2.2, pytest.approx(3.3)),
    (0.3, 0.1, pytest.approx(0.2)),
    (-1.5, -0.5, pytest.approx(-1.0)),
])
def test_subtract_floats(a, b, expected):
    calc = Calculator()
    assert calc.subtract(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (2.0, 3.0, pytest.approx(6.0)),
    (0.5, 0.4, pytest.approx(0.2)),
    (-1.5, 2.0, pytest.approx(-3.0)),
])
def test_multiply_floats(a, b, expected):
    calc = Calculator()
    assert calc.multiply(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (7.5, 2.5, pytest.approx(3.0)),
    (1.0, 3.0, pytest.approx(0.3333333333333333)),
    (-4.5, 1.5, pytest.approx(-3.0)),
])
def test_divide_floats(a, b, expected):
    calc = Calculator()
    assert calc.divide(a, b) == expected


# Section 3 — Invalid inputs (TypeError)

@pytest.mark.parametrize("a, b", [
    ("a", 1),
    (1, "b"),
    (None, 1),
    (1, None),
])
def test_add_invalid_input(a, b):
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.add(a, b)

@pytest.mark.parametrize("a, b", [
    ("a", 1),
    (1, "b"),
    (None, 5),
])
def test_subtract_invalid_input(a, b):
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.subtract(a, b)

@pytest.mark.parametrize("a, b", [
    ("a", "b"),
    (None, 3),
    ({}, 2),
])
def test_multiply_invalid_input(a, b):
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.multiply(a, b)

@pytest.mark.parametrize("a, b", [
    ("a", 2),
    (None, 3),
    ([], 2),
])
def test_divide_invalid_input(a, b):
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.divide(a, b)


# Section 4 — Edge cases: large numbers, negative, zero operands

@pytest.mark.parametrize("a, b, expected", [
    (10**18, 10**18, 2 * 10**18),
    (-10**18, 10**18, 0),
    (0, 0, 0),
])
def test_add_edge_cases(a, b, expected):
    calc = Calculator()
    assert calc.add(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (10**18, 1, 10**18 - 1),
    (-10**18, -10**18, 0),
    (0, 10**18, -(10**18)),
])
def test_subtract_edge_cases(a, b, expected):
    calc = Calculator()
    assert calc.subtract(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (10**9, 10**9, 10**18),
    (-10**9, 10**9, -(10**18)),
    (0, 10**18, 0),
])
def test_multiply_edge_cases(a, b, expected):
    calc = Calculator()
    assert calc.multiply(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (10**18, 10**9, pytest.approx(10**9)),
    (-10**18, 10**9, pytest.approx(-(10**9))),
    (0, 10**18, pytest.approx(0.0)),
])
def test_divide_edge_cases(a, b, expected):
    calc = Calculator()
    assert calc.divide(a, b) == expected


# Section 5 — multiply with string operands (str * int is valid Python)

def test_multiply_string_by_int_returns_repeated_string():
    """str * int is legal in Python; multiply must not raise TypeError."""
    calc = Calculator()
    assert calc.multiply("a", 2) == "aa"

def test_multiply_int_by_string_returns_repeated_string():
    """int * str is commutative in Python; multiply must not raise TypeError."""
    calc = Calculator()
    assert calc.multiply(2, "a") == "aa"

def test_multiply_string_by_zero_returns_empty_string():
    """Any string multiplied by 0 produces an empty string."""
    calc = Calculator()
    assert calc.multiply("abc", 0) == ""


# Section 6 — divide by negative zero (-0.0)

def test_divide_by_negative_float_zero_raises():
    """IEEE 754 negative zero is still zero; dividing by -0.0 must raise ZeroDivisionError."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(1, -0.0)

def test_divide_by_negative_float_zero_negative_numerator_raises():
    """Negative numerator over -0.0 must also raise ZeroDivisionError."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(-1.0, -0.0)


# Section 7 — float overflow to inf

def test_add_large_floats_overflows_to_inf():
    """Adding sys.float_info.max to itself overflows to positive infinity."""
    import sys
    import math
    calc = Calculator()
    result = calc.add(sys.float_info.max, sys.float_info.max)
    assert math.isinf(result) and result > 0

def test_multiply_large_float_overflows_to_inf():
    """Multiplying sys.float_info.max by 2 overflows to positive infinity."""
    import sys
    import math
    calc = Calculator()
    result = calc.multiply(sys.float_info.max, 2.0)
    assert math.isinf(result) and result > 0

def test_divide_produces_inf_when_result_overflows():
    """Dividing sys.float_info.max by a very small positive float overflows to inf."""
    import sys
    import math
    calc = Calculator()
    result = calc.divide(sys.float_info.max, 0.5)
    assert math.isinf(result) and result > 0


# Section 8 — inf operand behaviour

def test_add_inf_and_finite_returns_inf():
    """Adding a finite number to infinity returns infinity."""
    import math
    calc = Calculator()
    result = calc.add(float("inf"), 1)
    assert math.isinf(result) and result > 0

def test_add_positive_inf_and_negative_inf_returns_nan():
    """inf + (-inf) is an indeterminate form; result must be NaN."""
    import math
    calc = Calculator()
    result = calc.add(float("inf"), float("-inf"))
    assert math.isnan(result)

def test_divide_inf_by_inf_returns_nan():
    """inf / inf is an indeterminate form; result must be NaN."""
    import math
    calc = Calculator()
    result = calc.divide(float("inf"), float("inf"))
    assert math.isnan(result)

def test_divide_finite_by_inf_returns_zero():
    """Any finite number divided by infinity converges to zero."""
    calc = Calculator()
    result = calc.divide(1.0, float("inf"))
    assert result == 0.0

def test_multiply_inf_by_zero_returns_nan():
    """inf * 0 is an indeterminate form; result must be NaN."""
    import math
    calc = Calculator()
    result = calc.multiply(float("inf"), 0)
    assert math.isnan(result)

def test_subtract_inf_from_itself_returns_nan():
    """inf - inf is an indeterminate form; result must be NaN."""
    import math
    calc = Calculator()
    result = calc.subtract(float("inf"), float("inf"))
    assert math.isnan(result)


# Section 9 — NaN propagation

def test_add_nan_propagates():
    """Any operation involving NaN must return NaN."""
    import math
    calc = Calculator()
    assert math.isnan(calc.add(float("nan"), 1))

def test_multiply_nan_propagates():
    """Multiplying by NaN must return NaN even when the other operand is 0."""
    import math
    calc = Calculator()
    assert math.isnan(calc.multiply(0, float("nan")))

def test_divide_nan_propagates():
    """Dividing NaN by a finite number must return NaN."""
    import math
    calc = Calculator()
    assert math.isnan(calc.divide(float("nan"), 2.0))


# Section 10 — negative zero as a result

def test_multiply_by_negative_zero_produces_negative_zero():
    """Multiplying a positive float by -0.0 should yield -0.0 (IEEE 754)."""
    import math
    calc = Calculator()
    result = calc.multiply(1.0, -0.0)
    # result == 0.0 (== comparison), but sign bit is negative
    assert result == 0.0
    assert math.copysign(1, result) == -1.0

def test_divide_negative_zero_by_positive_returns_negative_zero():
    """Dividing -0.0 by a positive number should yield -0.0 (IEEE 754)."""
    import math
    calc = Calculator()
    result = calc.divide(-0.0, 1.0)
    assert result == 0.0
    assert math.copysign(1, result) == -1.0