import pytest
import math
from src.core.calculator import Calculator


# ==================== Addition Tests ====================

def test_add_normal_case():
    """Test normal addition: 2 + 3 = 5."""
    calc = Calculator()
    result = calc.add(2, 3)
    assert result == 5


def test_add_negative_numbers():
    """Test addition with negative numbers: -5 + 3 = -2."""
    calc = Calculator()
    result = calc.add(-5, 3)
    assert result == -2


def test_add_float_arithmetic():
    """Test addition with floats: 2.5 + 1.5 = 4.0."""
    calc = Calculator()
    result = calc.add(2.5, 1.5)
    assert result == 4.0


def test_add_with_zero_operand():
    """Test addition with zero operand: 0 + 5 = 5."""
    calc = Calculator()
    result = calc.add(0, 5)
    assert result == 5


def test_add_both_zero():
    """Test addition of two zeros: 0 + 0 = 0."""
    calc = Calculator()
    result = calc.add(0, 0)
    assert result == 0


def test_add_negative_plus_negative():
    """Test addition of two negative numbers: -3 + -2 = -5."""
    calc = Calculator()
    result = calc.add(-3, -2)
    assert result == -5


# ==================== Subtraction Tests ====================

def test_subtract_normal_case():
    """Test normal subtraction: 10 - 3 = 7."""
    calc = Calculator()
    result = calc.subtract(10, 3)
    assert result == 7


def test_subtract_resulting_in_negative():
    """Test subtraction resulting in negative: 3 - 10 = -7."""
    calc = Calculator()
    result = calc.subtract(3, 10)
    assert result == -7


def test_subtract_float_arithmetic():
    """Test subtraction with floats: 5.5 - 2.5 = 3.0."""
    calc = Calculator()
    result = calc.subtract(5.5, 2.5)
    assert result == 3.0


def test_subtract_with_zero_minuend():
    """Test subtraction from zero: 0 - 5 = -5."""
    calc = Calculator()
    result = calc.subtract(0, 5)
    assert result == -5


def test_subtract_with_zero_subtrahend():
    """Test subtraction with zero subtrahend: 10 - 0 = 10."""
    calc = Calculator()
    result = calc.subtract(10, 0)
    assert result == 10


def test_subtract_negative_minus_negative():
    """Test subtraction of negative numbers: -3 - -5 = 2."""
    calc = Calculator()
    result = calc.subtract(-3, -5)
    assert result == 2


# ==================== Multiplication Tests ====================

def test_multiply_normal_case():
    """Test normal multiplication: 3 * 4 = 12."""
    calc = Calculator()
    result = calc.multiply(3, 4)
    assert result == 12


def test_multiply_negative_by_positive():
    """Test multiplication with negative: -3 * 4 = -12."""
    calc = Calculator()
    result = calc.multiply(-3, 4)
    assert result == -12


def test_multiply_negative_by_negative():
    """Test multiplication of two negatives: -3 * -4 = 12."""
    calc = Calculator()
    result = calc.multiply(-3, -4)
    assert result == 12


def test_multiply_by_zero():
    """Test multiplication by zero: 5 * 0 = 0."""
    calc = Calculator()
    result = calc.multiply(5, 0)
    assert result == 0


def test_multiply_zero_by_zero():
    """Test multiplication of two zeros: 0 * 0 = 0."""
    calc = Calculator()
    result = calc.multiply(0, 0)
    assert result == 0


def test_multiply_float_by_integer():
    """Test multiplication with float: 2.5 * 2 = 5.0."""
    calc = Calculator()
    result = calc.multiply(2.5, 2)
    assert result == 5.0


def test_multiply_float_by_float():
    """Test multiplication of two floats: 1.5 * 2.5 = 3.75."""
    calc = Calculator()
    result = calc.multiply(1.5, 2.5)
    assert result == 3.75


# ==================== Division Tests ====================

def test_divide_normal_division():
    """Test normal division: 10 / 2 = 5.0."""
    calc = Calculator()
    result = calc.divide(10, 2)
    assert result == 5.0


def test_divide_resulting_in_float():
    """Test division resulting in float: 5 / 2 = 2.5."""
    calc = Calculator()
    result = calc.divide(5, 2)
    assert result == 2.5


def test_divide_negative_dividend():
    """Test division with negative dividend: -10 / 2 = -5.0."""
    calc = Calculator()
    result = calc.divide(-10, 2)
    assert result == -5.0


def test_divide_by_one():
    """Test division by one: 7 / 1 = 7.0."""
    calc = Calculator()
    result = calc.divide(7, 1)
    assert result == 7.0


def test_divide_zero_numerator():
    """Test division with zero numerator: 0 / 5 = 0.0."""
    calc = Calculator()
    result = calc.divide(0, 5)
    assert result == 0.0


# ==================== Division by Zero Tests (Issue #139) ====================

def test_divide_integer_by_zero_raises_error():
    """Test that dividing an integer by zero raises ZeroDivisionError."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)


def test_divide_float_by_zero_raises_error():
    """Test that dividing a float by zero raises ZeroDivisionError."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(10.5, 0.0)


def test_divide_negative_by_zero_raises_error():
    """Test that dividing a negative number by zero raises ZeroDivisionError."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(-5, 0)


# ==================== Invalid Input Tests ====================

def test_add_with_string_argument():
    """Test that add raises TypeError when passed a string."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.add("5", 3)


def test_add_with_none_argument():
    """Test that add raises TypeError when passed None."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.add(None, 5)


def test_subtract_with_string_argument():
    """Test that subtract raises TypeError when passed a string."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.subtract("10", 3)


def test_subtract_with_none_argument():
    """Test that subtract raises TypeError when passed None."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.subtract(None, 5)


def test_multiply_string_by_string_raises_error():
    """Test that multiply raises TypeError when both arguments are strings."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.multiply("3", "4")


def test_multiply_with_none_argument():
    """Test that multiply raises TypeError when passed None."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.multiply(None, 5)


def test_divide_with_string_argument():
    """Test that divide raises TypeError when passed a string."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.divide("10", 2)


def test_divide_with_none_argument():
    """Test that divide raises TypeError when passed None."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.divide(None, 5)


# ==================== Factorial Tests ====================

def test_factorial_zero():
    """Test boundary case: factorial(0) == 1."""
    calc = Calculator()
    result = calc.factorial(0)
    assert result == 1


def test_factorial_one():
    """Test boundary case: factorial(1) == 1."""
    calc = Calculator()
    result = calc.factorial(1)
    assert result == 1


def test_factorial_small_integer():
    """Test normal case: factorial(2) == 2."""
    calc = Calculator()
    result = calc.factorial(2)
    assert result == 2


def test_factorial_medium_integer():
    """Test normal case: factorial(5) == 120."""
    calc = Calculator()
    result = calc.factorial(5)
    assert result == 120


def test_factorial_larger_integer():
    """Test normal case: factorial(10) == 3628800."""
    calc = Calculator()
    result = calc.factorial(10)
    assert result == 3628800


def test_factorial_negative_integer():
    """Test error case: factorial(-1) raises ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.factorial(-1)


def test_factorial_negative_five():
    """Test error case: factorial(-5) raises ValueError."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.factorial(-5)


def test_factorial_float():
    """Test error case: factorial(3.5) raises TypeError."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.factorial(3.5)


def test_factorial_string():
    """Test error case: factorial("5") raises TypeError."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.factorial("5")


def test_factorial_none():
    """Test error case: factorial(None) raises TypeError."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.factorial(None)


def test_factorial_bool_true():
    """Test edge case: factorial(True) returns 1 (bool is subclass of int)."""
    calc = Calculator()
    result = calc.factorial(True)
    assert result == 1


def test_factorial_bool_false():
    """Test edge case: factorial(False) returns 1 (bool is subclass of int)."""
    calc = Calculator()
    result = calc.factorial(False)
    assert result == 1


# ==================== Square Tests ====================

def test_square_positive_integer():
    """Test normal case: square(3) == 9."""
    calc = Calculator()
    result = calc.square(3)
    assert result == 9


def test_square_positive_float():
    """Test normal case with float: square(2.5) == 6.25."""
    calc = Calculator()
    result = calc.square(2.5)
    assert result == pytest.approx(6.25)


def test_square_negative_integer():
    """Test negative input: square(-4) == 16."""
    calc = Calculator()
    result = calc.square(-4)
    assert result == 16


def test_square_negative_float():
    """Test negative float: square(-3.5) == 12.25."""
    calc = Calculator()
    result = calc.square(-3.5)
    assert result == pytest.approx(12.25)


def test_square_zero():
    """Test boundary case: square(0) == 0."""
    calc = Calculator()
    result = calc.square(0)
    assert result == 0


def test_square_large_integer():
    """Test large integer: square(1000) == 1000000."""
    calc = Calculator()
    result = calc.square(1000)
    assert result == 1000000


def test_square_string_raises_error():
    """Test that square raises TypeError with string argument."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.square("5")


def test_square_none_raises_error():
    """Test that square raises TypeError with None argument."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.square(None)


# ==================== Cube Tests ====================

def test_cube_positive_integer():
    """Test normal case: cube(3) == 27."""
    calc = Calculator()
    result = calc.cube(3)
    assert result == 27


def test_cube_positive_float():
    """Test normal case with float: cube(2.0) == 8.0."""
    calc = Calculator()
    result = calc.cube(2.0)
    assert result == pytest.approx(8.0)


def test_cube_negative_integer():
    """Test negative input: cube(-3) == -27."""
    calc = Calculator()
    result = calc.cube(-3)
    assert result == -27


def test_cube_negative_float():
    """Test negative float: cube(-2.5) == -15.625."""
    calc = Calculator()
    result = calc.cube(-2.5)
    assert result == pytest.approx(-15.625)


def test_cube_zero():
    """Test boundary case: cube(0) == 0."""
    calc = Calculator()
    result = calc.cube(0)
    assert result == 0


def test_cube_one():
    """Test boundary case: cube(1) == 1."""
    calc = Calculator()
    result = calc.cube(1)
    assert result == 1


def test_cube_large_integer():
    """Test large integer: cube(10) == 1000."""
    calc = Calculator()
    result = calc.cube(10)
    assert result == 1000


def test_cube_string_raises_error():
    """Test that cube raises TypeError with string argument."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.cube("3")


def test_cube_none_raises_error():
    """Test that cube raises TypeError with None argument."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.cube(None)


# ==================== Square Root Tests ====================

def test_square_root_perfect_square():
    """Test perfect square: square_root(9) == 3.0."""
    calc = Calculator()
    result = calc.square_root(9)
    assert result == pytest.approx(3.0)


def test_square_root_non_perfect_square():
    """Test non-perfect square: square_root(2) ≈ 1.414."""
    calc = Calculator()
    result = calc.square_root(2)
    assert result == pytest.approx(1.4142135623730951)


def test_square_root_float_input():
    """Test float input: square_root(6.25) == 2.5."""
    calc = Calculator()
    result = calc.square_root(6.25)
    assert result == pytest.approx(2.5)


def test_square_root_zero():
    """Test boundary case: square_root(0) == 0.0."""
    calc = Calculator()
    result = calc.square_root(0)
    assert result == pytest.approx(0.0)


def test_square_root_one():
    """Test boundary case: square_root(1) == 1.0."""
    calc = Calculator()
    result = calc.square_root(1)
    assert result == pytest.approx(1.0)


def test_square_root_large_number():
    """Test large number: square_root(10000) == 100.0."""
    calc = Calculator()
    result = calc.square_root(10000)
    assert result == pytest.approx(100.0)


def test_square_root_negative_raises_error():
    """Test that square_root raises ValueError for negative input."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.square_root(-1)


def test_square_root_string_raises_error():
    """Test that square_root raises TypeError with string argument."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.square_root("9")


def test_square_root_none_raises_error():
    """Test that square_root raises TypeError with None argument."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.square_root(None)


# ==================== Cube Root Tests ====================

def test_cube_root_perfect_cube():
    """Test perfect cube: cube_root(8) == 2.0."""
    calc = Calculator()
    result = calc.cube_root(8)
    assert result == pytest.approx(2.0)


def test_cube_root_non_perfect_cube():
    """Test non-perfect cube: cube_root(10) ≈ 2.154."""
    calc = Calculator()
    result = calc.cube_root(10)
    assert result == pytest.approx(2.154434690031884)


def test_cube_root_negative_perfect_cube():
    """Test negative perfect cube: cube_root(-8) == -2.0."""
    calc = Calculator()
    result = calc.cube_root(-8)
    assert result == pytest.approx(-2.0)


def test_cube_root_negative_number():
    """Test negative non-perfect cube: cube_root(-27) == -3.0."""
    calc = Calculator()
    result = calc.cube_root(-27)
    assert result == pytest.approx(-3.0)


def test_cube_root_zero():
    """Test boundary case: cube_root(0) == 0.0."""
    calc = Calculator()
    result = calc.cube_root(0)
    assert result == pytest.approx(0.0)


def test_cube_root_one():
    """Test boundary case: cube_root(1) == 1.0."""
    calc = Calculator()
    result = calc.cube_root(1)
    assert result == pytest.approx(1.0)


def test_cube_root_float_input():
    """Test float input: cube_root(8.0) == 2.0."""
    calc = Calculator()
    result = calc.cube_root(8.0)
    assert result == pytest.approx(2.0)


def test_cube_root_fractional_input():
    """Test fractional input: cube_root(0.125) == 0.5."""
    calc = Calculator()
    result = calc.cube_root(0.125)
    assert result == pytest.approx(0.5)


def test_cube_root_string_raises_error():
    """Test that cube_root raises TypeError with string argument."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.cube_root("8")


def test_cube_root_none_raises_error():
    """Test that cube_root raises TypeError with None argument."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.cube_root(None)


# ==================== Power Tests ====================

def test_power_integer_base_and_exponent():
    """Test integer power: power(2, 3) == 8."""
    calc = Calculator()
    result = calc.power(2, 3)
    assert result == 8


def test_power_float_base():
    """Test float base: power(2.5, 2) == 6.25."""
    calc = Calculator()
    result = calc.power(2.5, 2)
    assert result == pytest.approx(6.25)


def test_power_float_exponent():
    """Test float exponent: power(9.0, 0.5) == 3.0."""
    calc = Calculator()
    result = calc.power(9.0, 0.5)
    assert result == pytest.approx(3.0)


def test_power_zero_exponent():
    """Test zero exponent: power(5, 0) == 1."""
    calc = Calculator()
    result = calc.power(5, 0)
    assert result == 1


def test_power_one_exponent():
    """Test exponent of one: power(7, 1) == 7."""
    calc = Calculator()
    result = calc.power(7, 1)
    assert result == 7


def test_power_negative_exponent():
    """Test negative exponent: power(2, -1) == 0.5."""
    calc = Calculator()
    result = calc.power(2, -1)
    assert result == pytest.approx(0.5)


def test_power_large_integers():
    """Test large integers: power(2, 10) == 1024."""
    calc = Calculator()
    result = calc.power(2, 10)
    assert result == 1024


def test_power_negative_base_even_exponent():
    """Test negative base with even exponent: power(-3, 2) == 9."""
    calc = Calculator()
    result = calc.power(-3, 2)
    assert result == 9


def test_power_negative_base_odd_exponent():
    """Test negative base with odd exponent: power(-3, 3) == -27."""
    calc = Calculator()
    result = calc.power(-3, 3)
    assert result == -27


def test_power_negative_base_float_exponent_raises_error():
    """Test that power raises ValueError for negative base and float exponent."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.power(-2, 0.5)


def test_power_base_type_error():
    """Test that power raises TypeError with non-numeric base."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.power("2", 3)


def test_power_exponent_type_error():
    """Test that power raises TypeError with non-numeric exponent."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.power(2, "3")


def test_power_base_none_raises_error():
    """Test that power raises TypeError with None base."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.power(None, 3)


def test_power_exponent_none_raises_error():
    """Test that power raises TypeError with None exponent."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.power(2, None)


# ==================== Log (Base 10) Tests ====================

def test_log_power_of_ten():
    """Test log of power of 10: log(100) == 2.0."""
    calc = Calculator()
    result = calc.log(100)
    assert result == pytest.approx(2.0)


def test_log_ten():
    """Test log base: log(10) == 1.0."""
    calc = Calculator()
    result = calc.log(10)
    assert result == pytest.approx(1.0)


def test_log_one():
    """Test boundary case: log(1) == 0.0."""
    calc = Calculator()
    result = calc.log(1)
    assert result == pytest.approx(0.0)


def test_log_non_power_of_ten():
    """Test non-power of 10: log(2) ≈ 0.301."""
    calc = Calculator()
    result = calc.log(2)
    assert result == pytest.approx(0.3010299956639812)


def test_log_float_input():
    """Test float input: log(1000.0) == 3.0."""
    calc = Calculator()
    result = calc.log(1000.0)
    assert result == pytest.approx(3.0)


def test_log_large_number():
    """Test large number: log(1e6) == 6.0."""
    calc = Calculator()
    result = calc.log(1e6)
    assert result == pytest.approx(6.0)


def test_log_zero_raises_error():
    """Test that log raises ValueError for zero input."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.log(0)


def test_log_negative_raises_error():
    """Test that log raises ValueError for negative input."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.log(-10)


def test_log_string_raises_error():
    """Test that log raises TypeError with string argument."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.log("100")


def test_log_none_raises_error():
    """Test that log raises TypeError with None argument."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.log(None)


# ==================== Natural Logarithm (ln) Tests ====================

def test_ln_e():
    """Test natural logarithm of e: ln(e) == 1.0."""
    calc = Calculator()
    result = calc.ln(math.e)
    assert result == pytest.approx(1.0)


def test_ln_one():
    """Test boundary case: ln(1) == 0.0."""
    calc = Calculator()
    result = calc.ln(1)
    assert result == pytest.approx(0.0)


def test_ln_arbitrary_positive():
    """Test arbitrary positive number: ln(10) ≈ 2.302."""
    calc = Calculator()
    result = calc.ln(10)
    assert result == pytest.approx(2.302585092994046)


def test_ln_e_squared():
    """Test ln(e²) == 2.0."""
    calc = Calculator()
    result = calc.ln(math.e ** 2)
    assert result == pytest.approx(2.0)


def test_ln_float_input():
    """Test float input: ln(2.718) ≈ 1.0."""
    calc = Calculator()
    result = calc.ln(2.718)
    assert result == pytest.approx(1.0006315, abs=0.001)


def test_ln_large_number():
    """Test large number: ln(1e10)."""
    calc = Calculator()
    result = calc.ln(1e10)
    assert result == pytest.approx(23.025850929940455)


def test_ln_zero_raises_error():
    """Test that ln raises ValueError for zero input."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.ln(0)


def test_ln_negative_raises_error():
    """Test that ln raises ValueError for negative input."""
    calc = Calculator()
    with pytest.raises(ValueError):
        calc.ln(-5)


def test_ln_string_raises_error():
    """Test that ln raises TypeError with string argument."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.ln("10")


def test_ln_none_raises_error():
    """Test that ln raises TypeError with None argument."""
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.ln(None)