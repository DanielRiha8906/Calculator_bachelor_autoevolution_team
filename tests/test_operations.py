"""Comprehensive tests for arithmetic and advanced operation modules.

Tests cover ArithmeticOperations, AdvancedOperations, and Calculator's
delegation to these modules. All methods are tested for:
  - Happy path / normal execution
  - Edge cases (zero, negative, infinity, NaN, type mismatches)
  - Error handling (ValueError, ZeroDivisionError, TypeError)
"""

import math
import pytest
from src.operations.base import OperationModule
from src.operations.arithmetic import ArithmeticOperations
from src.operations.advanced import AdvancedOperations
from src.calculator import Calculator


# ============================================================================
# ARITHMETIC OPERATIONS TESTS
# ============================================================================

class TestArithmeticOperationsModule:
    """Test the ArithmeticOperations module in isolation."""

    def test_arithmetic_operations_is_operation_module(self):
        """Verify ArithmeticOperations is a subclass of OperationModule."""
        ops = ArithmeticOperations()
        assert isinstance(ops, OperationModule)

    # ========================================================================
    # ADD METHOD TESTS
    # ========================================================================

    def test_add_positive_integers(self):
        """Happy path: add two positive integers."""
        ops = ArithmeticOperations()
        assert ops.add(3, 4) == 7

    def test_add_negative_integers(self):
        """Happy path: add two negative integers."""
        ops = ArithmeticOperations()
        assert ops.add(-3, -4) == -7

    def test_add_mixed_sign(self):
        """Happy path: add numbers with mixed signs."""
        ops = ArithmeticOperations()
        assert ops.add(10, -7) == 3

    def test_add_zero(self):
        """Edge case: adding zero."""
        ops = ArithmeticOperations()
        assert ops.add(5, 0) == 5
        assert ops.add(0, 5) == 5

    def test_add_both_zero(self):
        """Edge case: add zero and zero."""
        ops = ArithmeticOperations()
        assert ops.add(0, 0) == 0

    def test_add_floats(self):
        """Happy path: add two floats."""
        ops = ArithmeticOperations()
        assert ops.add(1.5, 2.5) == pytest.approx(4.0)

    def test_add_float_and_int(self):
        """Happy path: add float and integer."""
        ops = ArithmeticOperations()
        assert ops.add(1.5, 2) == pytest.approx(3.5)

    def test_add_large_integers(self):
        """Edge case: add very large integers."""
        ops = ArithmeticOperations()
        assert ops.add(10**18, 10**18) == 2 * 10**18

    def test_add_infinity(self):
        """Edge case: add infinity."""
        ops = ArithmeticOperations()
        assert ops.add(float("inf"), 1) == float("inf")
        assert ops.add(1, float("inf")) == float("inf")

    def test_add_nan(self):
        """Edge case: add with NaN."""
        ops = ArithmeticOperations()
        result = ops.add(float("nan"), 1)
        assert math.isnan(result)

    def test_add_type_error_first_arg(self):
        """Error: first argument is wrong type."""
        ops = ArithmeticOperations()
        with pytest.raises(TypeError):
            ops.add("a", 1)

    def test_add_type_error_second_arg(self):
        """Error: second argument is wrong type."""
        ops = ArithmeticOperations()
        with pytest.raises(TypeError):
            ops.add(1, "a")

    def test_add_none_first_arg(self):
        """Error: first argument is None."""
        ops = ArithmeticOperations()
        with pytest.raises(TypeError):
            ops.add(None, 1)

    def test_add_none_second_arg(self):
        """Error: second argument is None."""
        ops = ArithmeticOperations()
        with pytest.raises(TypeError):
            ops.add(1, None)

    @pytest.mark.parametrize("a,b,expected", [
        (0, 0, 0),
        (1, 1, 2),
        (-1, -1, -2),
        (10**9, 10**9, 2 * 10**9),
    ])
    def test_add_parametrized(self, a, b, expected):
        """Parametrized correctness test for add."""
        ops = ArithmeticOperations()
        assert ops.add(a, b) == expected

    # ========================================================================
    # SUBTRACT METHOD TESTS
    # ========================================================================

    def test_subtract_positive_integers(self):
        """Happy path: subtract two positive integers."""
        ops = ArithmeticOperations()
        assert ops.subtract(10, 3) == 7

    def test_subtract_negative_integers(self):
        """Happy path: subtract two negative integers."""
        ops = ArithmeticOperations()
        assert ops.subtract(-10, -3) == -7

    def test_subtract_resulting_in_negative(self):
        """Happy path: subtraction yields negative result."""
        ops = ArithmeticOperations()
        assert ops.subtract(3, 10) == -7

    def test_subtract_zero(self):
        """Edge case: subtract zero."""
        ops = ArithmeticOperations()
        assert ops.subtract(5, 0) == 5

    def test_subtract_both_zero(self):
        """Edge case: subtract zero from zero."""
        ops = ArithmeticOperations()
        assert ops.subtract(0, 0) == 0

    def test_subtract_floats(self):
        """Happy path: subtract floats."""
        ops = ArithmeticOperations()
        assert ops.subtract(5.5, 2.5) == pytest.approx(3.0)

    def test_subtract_float_and_int(self):
        """Happy path: subtract float from int."""
        ops = ArithmeticOperations()
        assert ops.subtract(5, 2.5) == pytest.approx(2.5)

    def test_subtract_large_integers(self):
        """Edge case: subtract with large integers."""
        ops = ArithmeticOperations()
        assert ops.subtract(10**18, 10**18 - 1) == 1

    def test_subtract_infinity(self):
        """Edge case: subtract with infinity."""
        ops = ArithmeticOperations()
        assert ops.subtract(float("inf"), 1) == float("inf")

    def test_subtract_nan(self):
        """Edge case: subtract with NaN."""
        ops = ArithmeticOperations()
        result = ops.subtract(float("nan"), 1)
        assert math.isnan(result)

    def test_subtract_type_error_first_arg(self):
        """Error: first argument is wrong type."""
        ops = ArithmeticOperations()
        with pytest.raises(TypeError):
            ops.subtract("a", 1)

    def test_subtract_type_error_second_arg(self):
        """Error: second argument is wrong type."""
        ops = ArithmeticOperations()
        with pytest.raises(TypeError):
            ops.subtract(1, "a")

    def test_subtract_none_args(self):
        """Error: arguments are None."""
        ops = ArithmeticOperations()
        with pytest.raises(TypeError):
            ops.subtract(None, 1)
        with pytest.raises(TypeError):
            ops.subtract(1, None)

    @pytest.mark.parametrize("a,b,expected", [
        (10, 3, 7),
        (-10, -3, -7),
        (5, 5, 0),
        (0, 10, -10),
    ])
    def test_subtract_parametrized(self, a, b, expected):
        """Parametrized correctness test for subtract."""
        ops = ArithmeticOperations()
        assert ops.subtract(a, b) == expected

    # ========================================================================
    # MULTIPLY METHOD TESTS
    # ========================================================================

    def test_multiply_positive_integers(self):
        """Happy path: multiply two positive integers."""
        ops = ArithmeticOperations()
        assert ops.multiply(3, 4) == 12

    def test_multiply_negative_integers(self):
        """Happy path: multiply two negative integers."""
        ops = ArithmeticOperations()
        assert ops.multiply(-3, -4) == 12

    def test_multiply_mixed_sign(self):
        """Happy path: multiply numbers with mixed signs."""
        ops = ArithmeticOperations()
        assert ops.multiply(-3, 4) == -12

    def test_multiply_by_zero(self):
        """Edge case: multiply by zero."""
        ops = ArithmeticOperations()
        assert ops.multiply(5, 0) == 0
        assert ops.multiply(0, 5) == 0

    def test_multiply_both_zero(self):
        """Edge case: multiply zero by zero."""
        ops = ArithmeticOperations()
        assert ops.multiply(0, 0) == 0

    def test_multiply_by_one(self):
        """Edge case: multiply by one."""
        ops = ArithmeticOperations()
        assert ops.multiply(99, 1) == 99

    def test_multiply_floats(self):
        """Happy path: multiply floats."""
        ops = ArithmeticOperations()
        assert ops.multiply(0.1, 0.2) == pytest.approx(0.02)

    def test_multiply_float_and_int(self):
        """Happy path: multiply float and int."""
        ops = ArithmeticOperations()
        assert ops.multiply(2.5, 4) == pytest.approx(10.0)

    def test_multiply_large_integers(self):
        """Edge case: multiply large integers."""
        ops = ArithmeticOperations()
        assert ops.multiply(10**9, 10**9) == 10**18

    def test_multiply_infinity(self):
        """Edge case: multiply with infinity."""
        ops = ArithmeticOperations()
        assert ops.multiply(float("inf"), 2) == float("inf")

    def test_multiply_nan(self):
        """Edge case: multiply with NaN."""
        ops = ArithmeticOperations()
        result = ops.multiply(float("nan"), 2)
        assert math.isnan(result)

    def test_multiply_type_error_incompatible(self):
        """Error: multiply incompatible types (string * string)."""
        ops = ArithmeticOperations()
        with pytest.raises(TypeError):
            ops.multiply("a", "b")

    def test_multiply_type_error_first_arg(self):
        """Error: first argument is wrong type."""
        ops = ArithmeticOperations()
        with pytest.raises(TypeError):
            ops.multiply(None, 1)

    def test_multiply_type_error_second_arg(self):
        """Error: second argument is wrong type."""
        ops = ArithmeticOperations()
        with pytest.raises(TypeError):
            ops.multiply(2, None)

    @pytest.mark.parametrize("a,b,expected", [
        (3, 4, 12),
        (-3, -4, 12),
        (-3, 4, -12),
        (10**9, 10**9, 10**18),
    ])
    def test_multiply_parametrized(self, a, b, expected):
        """Parametrized correctness test for multiply."""
        ops = ArithmeticOperations()
        assert ops.multiply(a, b) == expected

    # ========================================================================
    # DIVIDE METHOD TESTS
    # ========================================================================

    def test_divide_exact_result(self):
        """Happy path: divide with exact integer result."""
        ops = ArithmeticOperations()
        assert ops.divide(10, 2) == 5

    def test_divide_float_result(self):
        """Happy path: divide yielding non-integer result."""
        ops = ArithmeticOperations()
        assert ops.divide(1, 4) == pytest.approx(0.25)

    def test_divide_negative_dividend(self):
        """Happy path: divide with negative dividend."""
        ops = ArithmeticOperations()
        assert ops.divide(-10, 2) == -5

    def test_divide_negative_divisor(self):
        """Happy path: divide with negative divisor."""
        ops = ArithmeticOperations()
        assert ops.divide(10, -2) == -5

    def test_divide_both_negative(self):
        """Happy path: divide with both negative."""
        ops = ArithmeticOperations()
        assert ops.divide(-10, -2) == 5

    def test_divide_zero_numerator(self):
        """Edge case: divide zero (numerator is zero)."""
        ops = ArithmeticOperations()
        assert ops.divide(0, 5) == 0

    def test_divide_by_zero_raises(self):
        """Error: divide by zero raises ZeroDivisionError."""
        ops = ArithmeticOperations()
        with pytest.raises(ZeroDivisionError):
            ops.divide(1, 0)

    def test_divide_zero_by_zero_raises(self):
        """Error: divide zero by zero raises ZeroDivisionError."""
        ops = ArithmeticOperations()
        with pytest.raises(ZeroDivisionError):
            ops.divide(0, 0)

    def test_divide_floats(self):
        """Happy path: divide floats."""
        ops = ArithmeticOperations()
        assert ops.divide(1.0, 3.0) == pytest.approx(1 / 3)

    def test_divide_float_and_int(self):
        """Happy path: divide float by int."""
        ops = ArithmeticOperations()
        assert ops.divide(5.0, 2) == pytest.approx(2.5)

    def test_divide_large_integers(self):
        """Edge case: divide large integers."""
        ops = ArithmeticOperations()
        assert ops.divide(10**18, 10**9) == pytest.approx(10**9)

    def test_divide_infinity_divisor(self):
        """Edge case: divide by infinity."""
        ops = ArithmeticOperations()
        assert ops.divide(1.0, float("inf")) == pytest.approx(0.0)

    def test_divide_nan(self):
        """Edge case: divide with NaN."""
        ops = ArithmeticOperations()
        result = ops.divide(float("nan"), 2)
        assert math.isnan(result)

    def test_divide_type_error_first_arg(self):
        """Error: first argument is wrong type."""
        ops = ArithmeticOperations()
        with pytest.raises(TypeError):
            ops.divide("a", 2)

    def test_divide_type_error_second_arg(self):
        """Error: second argument is wrong type."""
        ops = ArithmeticOperations()
        with pytest.raises(TypeError):
            ops.divide(2, None)

    def test_divide_none_args(self):
        """Error: arguments are None."""
        ops = ArithmeticOperations()
        with pytest.raises(TypeError):
            ops.divide(None, 1)

    @pytest.mark.parametrize("a,b,expected", [
        (6, 3, 2),
        (-6, -3, 2),
        (-6, 3, -2),
        (6, -3, -2),
    ])
    def test_divide_sign_parametrized(self, a, b, expected):
        """Parametrized correctness test for divide."""
        ops = ArithmeticOperations()
        assert ops.divide(a, b) == pytest.approx(expected)


# ============================================================================
# ADVANCED OPERATIONS TESTS
# ============================================================================

class TestAdvancedOperationsModule:
    """Test the AdvancedOperations module in isolation."""

    def test_advanced_operations_is_operation_module(self):
        """Verify AdvancedOperations is a subclass of OperationModule."""
        ops = AdvancedOperations()
        assert isinstance(ops, OperationModule)

    # ========================================================================
    # FACTORIAL METHOD TESTS
    # ========================================================================

    def test_factorial_zero(self):
        """Happy path: factorial of zero is one."""
        ops = AdvancedOperations()
        assert ops.factorial(0) == 1

    def test_factorial_one(self):
        """Happy path: factorial of one is one."""
        ops = AdvancedOperations()
        assert ops.factorial(1) == 1

    def test_factorial_small_positive(self):
        """Happy path: factorial of small positive integer."""
        ops = AdvancedOperations()
        assert ops.factorial(5) == 120

    def test_factorial_larger_positive(self):
        """Happy path: factorial of larger positive integer."""
        ops = AdvancedOperations()
        assert ops.factorial(10) == 3628800

    def test_factorial_twenty(self):
        """Happy path: factorial of 20."""
        ops = AdvancedOperations()
        assert ops.factorial(20) == 2432902008176640000

    def test_factorial_large_value_correct_type(self):
        """Verify large factorial returns int type."""
        ops = AdvancedOperations()
        result = ops.factorial(100)
        assert isinstance(result, int)
        assert result > 0

    def test_factorial_negative_raises_value_error(self):
        """Error: factorial of negative integer."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial(-1)

    def test_factorial_large_negative_raises_value_error(self):
        """Error: factorial of large negative integer."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial(-100)

    def test_factorial_float_raises_value_error(self):
        """Error: factorial with float argument."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial(2.0)

    def test_factorial_float_zero_raises_value_error(self):
        """Error: factorial with 0.0 (float)."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial(0.0)

    def test_factorial_float_one_raises_value_error(self):
        """Error: factorial with 1.0 (float)."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial(1.0)

    def test_factorial_float_negative_raises_value_error(self):
        """Error: factorial with negative float."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial(-1.0)

    def test_factorial_float_nan_raises_value_error(self):
        """Error: factorial with NaN."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial(float("nan"))

    def test_factorial_float_inf_raises_value_error(self):
        """Error: factorial with infinity."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial(float("inf"))

    def test_factorial_string_raises_value_error(self):
        """Error: factorial with string argument."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial("5")

    def test_factorial_none_raises_value_error(self):
        """Error: factorial with None."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial(None)

    def test_factorial_list_raises_value_error(self):
        """Error: factorial with list."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial([5])

    def test_factorial_dict_raises_value_error(self):
        """Error: factorial with dict."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial({"n": 5})

    def test_factorial_tuple_raises_value_error(self):
        """Error: factorial with tuple."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial((5,))

    def test_factorial_complex_raises_value_error(self):
        """Error: factorial with complex number."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial(complex(5, 0))

    def test_factorial_true_returns_one(self):
        """Edge case: factorial(True) == factorial(1) (bool is subclass of int)."""
        ops = AdvancedOperations()
        assert ops.factorial(True) == 1

    def test_factorial_false_returns_one(self):
        """Edge case: factorial(False) == factorial(0) (bool is subclass of int)."""
        ops = AdvancedOperations()
        assert ops.factorial(False) == 1

    def test_factorial_error_message_for_float_mentions_type(self):
        """Verify error message mentions the type."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError, match="float"):
            ops.factorial(3.14)

    def test_factorial_error_message_for_string_mentions_type(self):
        """Verify error message mentions the type."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError, match="str"):
            ops.factorial("hello")

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
    ])
    def test_factorial_parametrized_known_values(self, n, expected):
        """Parametrized test for known factorial values."""
        ops = AdvancedOperations()
        assert ops.factorial(n) == expected

    @pytest.mark.parametrize("bad_input", [-1, -2, -10, -100])
    def test_factorial_parametrized_negative_raises(self, bad_input):
        """Parametrized test for negative input."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial(bad_input)

    @pytest.mark.parametrize("bad_input", [
        0.0, 1.0, 2.5, -1.0, float("nan"), float("inf"),
        "0", "5", "", None, [], {}, (1,), b"5", complex(1, 0),
    ])
    def test_factorial_parametrized_wrong_type_raises(self, bad_input):
        """Parametrized test for wrong type inputs."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.factorial(bad_input)

    # ========================================================================
    # SQUARE METHOD TESTS
    # ========================================================================

    def test_square_positive(self):
        """Happy path: square of positive number."""
        ops = AdvancedOperations()
        assert ops.square(4) == pytest.approx(16)

    def test_square_negative(self):
        """Happy path: square of negative number."""
        ops = AdvancedOperations()
        assert ops.square(-3) == pytest.approx(9)

    def test_square_zero(self):
        """Edge case: square of zero."""
        ops = AdvancedOperations()
        assert ops.square(0) == pytest.approx(0)

    def test_square_float(self):
        """Happy path: square of float."""
        ops = AdvancedOperations()
        assert ops.square(2.5) == pytest.approx(6.25)

    def test_square_one(self):
        """Edge case: square of one."""
        ops = AdvancedOperations()
        assert ops.square(1) == pytest.approx(1)

    def test_square_large_integer(self):
        """Edge case: square of large integer."""
        ops = AdvancedOperations()
        assert ops.square(10**9) == pytest.approx(10**18)

    def test_square_float_inf(self):
        """Edge case: square of infinity."""
        ops = AdvancedOperations()
        assert ops.square(float("inf")) == float("inf")

    def test_square_negative_float_inf(self):
        """Edge case: square of negative infinity."""
        ops = AdvancedOperations()
        assert ops.square(float("-inf")) == float("inf")

    def test_square_nan_propagates(self):
        """Edge case: square of NaN."""
        ops = AdvancedOperations()
        result = ops.square(float("nan"))
        assert math.isnan(result)

    # ========================================================================
    # CUBE METHOD TESTS
    # ========================================================================

    def test_cube_positive(self):
        """Happy path: cube of positive number."""
        ops = AdvancedOperations()
        assert ops.cube(3) == pytest.approx(27)

    def test_cube_negative(self):
        """Happy path: cube of negative number."""
        ops = AdvancedOperations()
        assert ops.cube(-2) == pytest.approx(-8)

    def test_cube_zero(self):
        """Edge case: cube of zero."""
        ops = AdvancedOperations()
        assert ops.cube(0) == pytest.approx(0)

    def test_cube_float(self):
        """Happy path: cube of float."""
        ops = AdvancedOperations()
        assert ops.cube(1.5) == pytest.approx(3.375)

    def test_cube_negative_float(self):
        """Happy path: cube of negative float."""
        ops = AdvancedOperations()
        assert ops.cube(-2.5) == pytest.approx(-15.625)

    def test_cube_large_integer(self):
        """Edge case: cube of large integer."""
        ops = AdvancedOperations()
        assert ops.cube(10**6) == pytest.approx(10**18)

    def test_cube_float_inf(self):
        """Edge case: cube of infinity."""
        ops = AdvancedOperations()
        assert ops.cube(float("inf")) == float("inf")

    def test_cube_negative_float_inf(self):
        """Edge case: cube of negative infinity."""
        ops = AdvancedOperations()
        assert ops.cube(float("-inf")) == float("-inf")

    def test_cube_nan_propagates(self):
        """Edge case: cube of NaN."""
        ops = AdvancedOperations()
        result = ops.cube(float("nan"))
        assert math.isnan(result)

    # ========================================================================
    # SQUARE_ROOT METHOD TESTS
    # ========================================================================

    def test_square_root_perfect_square(self):
        """Happy path: square root of perfect square."""
        ops = AdvancedOperations()
        assert ops.square_root(9) == pytest.approx(3.0)

    def test_square_root_four(self):
        """Happy path: square root of four."""
        ops = AdvancedOperations()
        assert ops.square_root(4) == pytest.approx(2.0)

    def test_square_root_float(self):
        """Happy path: square root of float."""
        ops = AdvancedOperations()
        assert ops.square_root(2.0) == pytest.approx(math.sqrt(2.0))

    def test_square_root_zero(self):
        """Edge case: square root of zero."""
        ops = AdvancedOperations()
        assert ops.square_root(0) == pytest.approx(0.0)

    def test_square_root_one(self):
        """Edge case: square root of one."""
        ops = AdvancedOperations()
        assert ops.square_root(1) == pytest.approx(1.0)

    def test_square_root_float_inf(self):
        """Edge case: square root of infinity."""
        ops = AdvancedOperations()
        assert ops.square_root(float("inf")) == float("inf")

    def test_square_root_very_small_positive(self):
        """Edge case: square root of very small positive number."""
        ops = AdvancedOperations()
        result = ops.square_root(1e-300)
        assert result == pytest.approx(math.sqrt(1e-300))

    def test_square_root_large_float(self):
        """Edge case: square root of large float."""
        ops = AdvancedOperations()
        result = ops.square_root(1e200)
        assert result == pytest.approx(math.sqrt(1e200))

    def test_square_root_nan_propagates(self):
        """Edge case: square root of NaN."""
        ops = AdvancedOperations()
        result = ops.square_root(float("nan"))
        assert math.isnan(result)

    def test_square_root_negative_raises_value_error(self):
        """Error: square root of negative number."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.square_root(-1)

    @pytest.mark.parametrize("x", [-1e-9, -1e100, -0.001])
    def test_square_root_negative_parametrized(self, x):
        """Parametrized test for negative inputs."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.square_root(x)

    # ========================================================================
    # CUBE_ROOT METHOD TESTS
    # ========================================================================

    def test_cube_root_positive(self):
        """Happy path: cube root of positive number."""
        ops = AdvancedOperations()
        assert ops.cube_root(27) == pytest.approx(3.0)

    def test_cube_root_negative(self):
        """Happy path: cube root of negative number."""
        ops = AdvancedOperations()
        assert ops.cube_root(-8) == pytest.approx(-2.0)

    def test_cube_root_zero(self):
        """Edge case: cube root of zero."""
        ops = AdvancedOperations()
        assert ops.cube_root(0) == pytest.approx(0.0)

    def test_cube_root_float(self):
        """Happy path: cube root of float."""
        ops = AdvancedOperations()
        assert ops.cube_root(8.0) == pytest.approx(2.0)

    def test_cube_root_one(self):
        """Edge case: cube root of one."""
        ops = AdvancedOperations()
        assert ops.cube_root(1) == pytest.approx(1.0)

    def test_cube_root_negative_one(self):
        """Edge case: cube root of negative one."""
        ops = AdvancedOperations()
        assert ops.cube_root(-1) == pytest.approx(-1.0)

    def test_cube_root_large_positive(self):
        """Edge case: cube root of large positive number."""
        ops = AdvancedOperations()
        assert ops.cube_root(10**9) == pytest.approx(1000.0)

    def test_cube_root_large_negative(self):
        """Edge case: cube root of large negative number."""
        ops = AdvancedOperations()
        result = ops.cube_root(-10**9)
        assert result == pytest.approx(-1000.0)

    def test_cube_root_float_inf(self):
        """Edge case: cube root of infinity."""
        ops = AdvancedOperations()
        assert ops.cube_root(float("inf")) == float("inf")

    def test_cube_root_negative_float_inf(self):
        """Edge case: cube root of negative infinity."""
        ops = AdvancedOperations()
        assert ops.cube_root(float("-inf")) == float("-inf")

    def test_cube_root_nan_propagates(self):
        """Edge case: cube root of NaN."""
        ops = AdvancedOperations()
        result = ops.cube_root(float("nan"))
        assert math.isnan(result)

    def test_cube_root_negative_sign_preserved(self):
        """Verify negative sign is preserved for negative inputs."""
        ops = AdvancedOperations()
        result = ops.cube_root(-27)
        assert result < 0

    # ========================================================================
    # POWER METHOD TESTS
    # ========================================================================

    def test_power_positive_exponent(self):
        """Happy path: power with positive exponent."""
        ops = AdvancedOperations()
        assert ops.power(2, 10) == pytest.approx(1024.0)

    def test_power_fractional_exponent(self):
        """Happy path: power with fractional exponent."""
        ops = AdvancedOperations()
        assert ops.power(4, 0.5) == pytest.approx(2.0)

    def test_power_zero_zero(self):
        """Edge case: 0 to the power of 0."""
        ops = AdvancedOperations()
        assert ops.power(0, 0) == pytest.approx(1.0)

    def test_power_zero_base_positive_exponent(self):
        """Edge case: 0 to positive power."""
        ops = AdvancedOperations()
        assert ops.power(0, 5) == pytest.approx(0.0)

    def test_power_one_base_any_exponent(self):
        """Edge case: 1 to any power."""
        ops = AdvancedOperations()
        assert ops.power(1, 999) == pytest.approx(1.0)

    def test_power_negative_base_integer_exponent(self):
        """Happy path: negative base with integer exponent."""
        ops = AdvancedOperations()
        assert ops.power(-2, 3) == pytest.approx(-8.0)

    def test_power_negative_exponent(self):
        """Happy path: negative exponent."""
        ops = AdvancedOperations()
        assert ops.power(2, -1) == pytest.approx(0.5)

    def test_power_base_ten(self):
        """Happy path: base 10 power."""
        ops = AdvancedOperations()
        assert ops.power(10, 3) == pytest.approx(1000.0)

    def test_power_fractional_base(self):
        """Happy path: fractional base."""
        ops = AdvancedOperations()
        assert ops.power(0.5, 2) == pytest.approx(0.25)

    def test_power_inf_exponent(self):
        """Edge case: infinity as exponent."""
        ops = AdvancedOperations()
        assert ops.power(2, float("inf")) == float("inf")

    def test_power_negative_base_fractional_exponent_raises(self):
        """Error: negative base with fractional exponent (complex result)."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.power(-2, 0.5)

    @pytest.mark.parametrize("base,exp,expected", [
        (3, 0, 1.0),
        (0, 1, 0.0),
        (2, 8, 256.0),
        (10, 0, 1.0),
    ])
    def test_power_parametrized(self, base, exp, expected):
        """Parametrized test for power."""
        ops = AdvancedOperations()
        assert ops.power(base, exp) == pytest.approx(expected)

    # ========================================================================
    # LOG METHOD TESTS
    # ========================================================================

    def test_log_hundred(self):
        """Happy path: log base 10 of 100."""
        ops = AdvancedOperations()
        assert ops.log(100) == pytest.approx(2.0)

    def test_log_one(self):
        """Edge case: log base 10 of 1."""
        ops = AdvancedOperations()
        assert ops.log(1) == pytest.approx(0.0)

    def test_log_ten(self):
        """Happy path: log base 10 of 10."""
        ops = AdvancedOperations()
        assert ops.log(10) == pytest.approx(1.0)

    def test_log_thousand(self):
        """Happy path: log base 10 of 1000."""
        ops = AdvancedOperations()
        assert ops.log(1000) == pytest.approx(3.0)

    def test_log_float_inf(self):
        """Edge case: log of infinity."""
        ops = AdvancedOperations()
        assert ops.log(float("inf")) == float("inf")

    def test_log_very_small_positive(self):
        """Edge case: log of very small positive number."""
        ops = AdvancedOperations()
        result = ops.log(1e-300)
        assert result == pytest.approx(math.log10(1e-300))

    def test_log_large_number(self):
        """Edge case: log of large number."""
        ops = AdvancedOperations()
        assert ops.log(10**10) == pytest.approx(10.0)

    def test_log_float_value(self):
        """Happy path: log of fractional value."""
        ops = AdvancedOperations()
        assert ops.log(0.1) == pytest.approx(-1.0)

    def test_log_zero_raises_value_error(self):
        """Error: log of zero."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.log(0)

    def test_log_negative_raises_value_error(self):
        """Error: log of negative number."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.log(-1)

    @pytest.mark.parametrize("x", [0, -1, -1e-9, -1e100])
    def test_log_non_positive_parametrized(self, x):
        """Parametrized test for non-positive inputs."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.log(x)

    # ========================================================================
    # LN METHOD TESTS
    # ========================================================================

    def test_ln_e(self):
        """Happy path: natural log of e."""
        ops = AdvancedOperations()
        assert ops.ln(math.e) == pytest.approx(1.0)

    def test_ln_one(self):
        """Edge case: natural log of 1."""
        ops = AdvancedOperations()
        assert ops.ln(1) == pytest.approx(0.0)

    def test_ln_float_inf(self):
        """Edge case: natural log of infinity."""
        ops = AdvancedOperations()
        assert ops.ln(float("inf")) == float("inf")

    def test_ln_very_small_positive(self):
        """Edge case: natural log of very small positive number."""
        ops = AdvancedOperations()
        result = ops.ln(1e-300)
        assert result == pytest.approx(math.log(1e-300))

    def test_ln_large_number(self):
        """Edge case: natural log of large number."""
        ops = AdvancedOperations()
        result = ops.ln(1e100)
        assert result == pytest.approx(math.log(1e100))

    def test_ln_float_value(self):
        """Happy path: natural log of fractional value."""
        ops = AdvancedOperations()
        assert ops.ln(0.5) == pytest.approx(math.log(0.5))

    def test_ln_zero_raises_value_error(self):
        """Error: natural log of zero."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.ln(0)

    def test_ln_negative_raises_value_error(self):
        """Error: natural log of negative number."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.ln(-1)

    @pytest.mark.parametrize("x", [0, -1, -1e-9, -1e100])
    def test_ln_non_positive_parametrized(self, x):
        """Parametrized test for non-positive inputs."""
        ops = AdvancedOperations()
        with pytest.raises(ValueError):
            ops.ln(x)


# ============================================================================
# CALCULATOR INITIALIZATION AND DELEGATION TESTS
# ============================================================================

class TestCalculatorIntegration:
    """Test Calculator's initialization and delegation to operation modules."""

    def test_calculator_init_creates_arithmetic_module(self):
        """Verify Calculator.__init__ creates an ArithmeticOperations instance."""
        calc = Calculator()
        assert hasattr(calc, '_arithmetic')
        assert isinstance(calc._arithmetic, ArithmeticOperations)
        assert isinstance(calc._arithmetic, OperationModule)

    def test_calculator_init_creates_advanced_module(self):
        """Verify Calculator.__init__ creates an AdvancedOperations instance."""
        calc = Calculator()
        assert hasattr(calc, '_advanced')
        assert isinstance(calc._advanced, AdvancedOperations)
        assert isinstance(calc._advanced, OperationModule)

    def test_calculator_creates_independent_instances(self):
        """Verify each Calculator instance has its own module instances."""
        calc1 = Calculator()
        calc2 = Calculator()
        assert calc1._arithmetic is not calc2._arithmetic
        assert calc1._advanced is not calc2._advanced

    # Arithmetic delegation tests

    def test_calculator_add_delegates_to_arithmetic(self):
        """Verify Calculator.add delegates to ArithmeticOperations."""
        calc = Calculator()
        assert calc.add(3, 4) == 7

    def test_calculator_subtract_delegates_to_arithmetic(self):
        """Verify Calculator.subtract delegates to ArithmeticOperations."""
        calc = Calculator()
        assert calc.subtract(10, 3) == 7

    def test_calculator_multiply_delegates_to_arithmetic(self):
        """Verify Calculator.multiply delegates to ArithmeticOperations."""
        calc = Calculator()
        assert calc.multiply(3, 4) == 12

    def test_calculator_divide_delegates_to_arithmetic(self):
        """Verify Calculator.divide delegates to ArithmeticOperations."""
        calc = Calculator()
        assert calc.divide(10, 2) == 5

    def test_calculator_divide_zero_raises_from_arithmetic(self):
        """Verify ZeroDivisionError from divide is preserved."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(1, 0)

    # Advanced delegation tests

    def test_calculator_factorial_delegates_to_advanced(self):
        """Verify Calculator.factorial delegates to AdvancedOperations."""
        calc = Calculator()
        assert calc.factorial(5) == 120

    def test_calculator_square_delegates_to_advanced(self):
        """Verify Calculator.square delegates to AdvancedOperations."""
        calc = Calculator()
        assert calc.square(4) == pytest.approx(16)

    def test_calculator_cube_delegates_to_advanced(self):
        """Verify Calculator.cube delegates to AdvancedOperations."""
        calc = Calculator()
        assert calc.cube(3) == pytest.approx(27)

    def test_calculator_square_root_delegates_to_advanced(self):
        """Verify Calculator.square_root delegates to AdvancedOperations."""
        calc = Calculator()
        assert calc.square_root(9) == pytest.approx(3.0)

    def test_calculator_cube_root_delegates_to_advanced(self):
        """Verify Calculator.cube_root delegates to AdvancedOperations."""
        calc = Calculator()
        assert calc.cube_root(27) == pytest.approx(3.0)

    def test_calculator_power_delegates_to_advanced(self):
        """Verify Calculator.power delegates to AdvancedOperations."""
        calc = Calculator()
        assert calc.power(2, 10) == pytest.approx(1024.0)

    def test_calculator_log_delegates_to_advanced(self):
        """Verify Calculator.log delegates to AdvancedOperations."""
        calc = Calculator()
        assert calc.log(100) == pytest.approx(2.0)

    def test_calculator_ln_delegates_to_advanced(self):
        """Verify Calculator.ln delegates to AdvancedOperations."""
        calc = Calculator()
        assert calc.ln(math.e) == pytest.approx(1.0)

    # Error preservation tests

    def test_calculator_factorial_value_error_preserved(self):
        """Verify ValueError from factorial is preserved."""
        calc = Calculator()
        with pytest.raises(ValueError):
            calc.factorial(-1)

    def test_calculator_square_root_value_error_preserved(self):
        """Verify ValueError from square_root is preserved."""
        calc = Calculator()
        with pytest.raises(ValueError):
            calc.square_root(-1)

    def test_calculator_log_value_error_preserved(self):
        """Verify ValueError from log is preserved."""
        calc = Calculator()
        with pytest.raises(ValueError):
            calc.log(0)

    def test_calculator_ln_value_error_preserved(self):
        """Verify ValueError from ln is preserved."""
        calc = Calculator()
        with pytest.raises(ValueError):
            calc.ln(0)

    # Behavior consistency tests (same results as direct operations)

    @pytest.mark.parametrize("method,args,expected", [
        ("add", (3, 4), 7),
        ("subtract", (10, 3), 7),
        ("multiply", (3, 4), 12),
    ])
    def test_calculator_arithmetic_operations_match_modules(self, method, args, expected):
        """Verify Calculator delegates give same results as direct module calls."""
        calc = Calculator()
        module = calc._arithmetic
        calc_result = getattr(calc, method)(*args)
        module_result = getattr(module, method)(*args)
        assert calc_result == module_result == expected

    @pytest.mark.parametrize("method,args,expected", [
        ("factorial", (5,), 120),
        ("square", (4,), 16),
        ("cube", (3,), 27),
    ])
    def test_calculator_advanced_operations_match_modules(self, method, args, expected):
        """Verify Calculator delegates give same results as direct module calls."""
        calc = Calculator()
        module = calc._advanced
        calc_result = getattr(calc, method)(*args)
        module_result = getattr(module, method)(*args)
        assert calc_result == pytest.approx(module_result) == pytest.approx(expected)

    def test_calculator_multiple_calls_consistent(self):
        """Verify Calculator behavior is consistent across multiple calls."""
        calc = Calculator()
        assert calc.add(5, 3) == 8
        assert calc.add(5, 3) == 8
        assert calc.multiply(4, 2) == 8
        assert calc.multiply(4, 2) == 8

    def test_calculator_does_not_mutate_inputs(self):
        """Verify Calculator does not mutate input arguments."""
        calc = Calculator()
        a, b = 5, 3
        calc.add(a, b)
        assert a == 5 and b == 3

        n = 10
        calc.factorial(n)
        assert n == 10
