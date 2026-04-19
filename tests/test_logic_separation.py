"""Comprehensive tests for the logic separation and edge cases.

Tests specifically verify:
- ArithmeticEngine stateless arithmetic operations with edge cases
- ArithmeticEngine error handling and type validation
- Calculator state management and history recording
- Backward compatibility of re-exports
- Package-level exports
"""

import pytest
import math
from datetime import datetime

from src.logic.core import ArithmeticEngine
from src.logic import Calculator
from src.logic.state import Calculator as CalculatorFromState
from src.calculator import Calculator as CalculatorBackCompat
from src import Calculator as CalculatorFromSrc


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def engine():
    """Provides a fresh ArithmeticEngine instance for each test."""
    return ArithmeticEngine()


@pytest.fixture
def calculator():
    """Provides a fresh Calculator instance for each test."""
    return Calculator()


# ============================================================================
# BACKWARD COMPATIBILITY TESTS
# ============================================================================

class TestBackwardCompatibility:
    """Verify all import paths resolve to the same Calculator class."""

    def test_calculator_from_src_logic_imports_correctly(self):
        """Verify import from src.logic works."""
        assert Calculator is not None
        assert hasattr(Calculator, 'add')

    def test_calculator_from_src_logic_state_imports_correctly(self):
        """Verify import from src.logic.state works."""
        assert CalculatorFromState is not None
        assert hasattr(CalculatorFromState, 'add')

    def test_calculator_backward_compat_import_works(self):
        """Verify import from src.calculator works."""
        assert CalculatorBackCompat is not None
        assert hasattr(CalculatorBackCompat, 'add')

    def test_calculator_from_src_package_imports_correctly(self):
        """Verify import from src works."""
        assert CalculatorFromSrc is not None
        assert hasattr(CalculatorFromSrc, 'add')

    def test_all_calculator_imports_reference_same_class(self):
        """Verify all import paths reference the same class."""
        assert Calculator is CalculatorFromState
        assert Calculator is CalculatorBackCompat
        assert Calculator is CalculatorFromSrc

    def test_calculator_instances_are_compatible(self):
        """Verify instances from different imports work the same way."""
        calc1 = Calculator()
        calc2 = CalculatorBackCompat()
        calc3 = CalculatorFromSrc()

        # All should work identically
        assert calc1.add(2, 3) == 5
        assert calc2.add(2, 3) == 5
        assert calc3.add(2, 3) == 5


# ============================================================================
# ARITHMETIC ENGINE - ADD OPERATION EDGE CASES
# ============================================================================

class TestArithmeticEngineAdd:
    """Edge case tests for ArithmeticEngine.add()."""

    def test_add_returns_int_when_both_ints(self, engine):
        """Verify add returns int when both operands are int."""
        result = engine.add(5, 3)
        assert result == 8
        assert isinstance(result, int)

    def test_add_returns_float_when_one_operand_float(self, engine):
        """Verify add promotes to float when one operand is float."""
        result = engine.add(5, 3.0)
        assert result == 8.0
        assert isinstance(result, float)

    def test_add_very_large_integers(self, engine):
        """Test add with very large integers."""
        large_int = 10**100
        result = engine.add(large_int, large_int)
        assert result == 2 * large_int

    def test_add_floats_with_inf(self, engine):
        """Test add with infinity."""
        result = engine.add(float('inf'), 1)
        assert result == float('inf')

    def test_add_inf_and_neg_inf_is_nan(self, engine):
        """Test that inf + (-inf) = nan."""
        result = engine.add(float('inf'), float('-inf'))
        assert math.isnan(result)

    def test_add_nan_propagates(self, engine):
        """Test that NaN + x = NaN."""
        result = engine.add(float('nan'), 5)
        assert math.isnan(result)

    def test_add_booleans_as_numbers(self, engine):
        """Test that booleans work (they are subclass of int in Python)."""
        # In Python, bool is a subclass of int, so True=1, False=0
        result = engine.add(True, True)
        assert result == 2

    def test_add_negative_zero(self, engine):
        """Test add with negative zero."""
        result = engine.add(-0.0, 5.0)
        assert result == 5.0


# ============================================================================
# ARITHMETIC ENGINE - SUBTRACT OPERATION EDGE CASES
# ============================================================================

class TestArithmeticEngineSubtract:
    """Edge case tests for ArithmeticEngine.subtract()."""

    def test_subtract_basic(self, engine):
        """Test basic subtraction."""
        assert engine.subtract(10, 3) == 7

    def test_subtract_negative_result(self, engine):
        """Test subtraction resulting in negative."""
        assert engine.subtract(3, 10) == -7

    def test_subtract_results_in_zero(self, engine):
        """Test subtraction resulting in zero."""
        assert engine.subtract(5, 5) == 0

    def test_subtract_floats(self, engine):
        """Test subtraction with floats."""
        assert engine.subtract(10.5, 3.2) == pytest.approx(7.3)

    def test_subtract_with_inf(self, engine):
        """Test subtraction with infinity."""
        result = engine.subtract(float('inf'), 100)
        assert result == float('inf')

    def test_subtract_inf_from_inf_is_nan(self, engine):
        """Test that inf - inf = nan."""
        result = engine.subtract(float('inf'), float('inf'))
        assert math.isnan(result)

    def test_subtract_very_small_floats(self, engine):
        """Test subtraction with very small floats."""
        result = engine.subtract(1e-100, 1e-101)
        assert result == pytest.approx(1e-100 - 1e-101)


# ============================================================================
# ARITHMETIC ENGINE - MULTIPLY OPERATION EDGE CASES
# ============================================================================

class TestArithmeticEngineMultiply:
    """Edge case tests for ArithmeticEngine.multiply()."""

    def test_multiply_basic(self, engine):
        """Test basic multiplication."""
        assert engine.multiply(5, 3) == 15

    def test_multiply_by_zero(self, engine):
        """Test multiplication by zero."""
        assert engine.multiply(100, 0) == 0

    def test_multiply_by_zero_float(self, engine):
        """Test multiplication by zero float."""
        result = engine.multiply(100.5, 0.0)
        assert result == 0.0

    def test_multiply_negative_numbers(self, engine):
        """Test multiplication of negative numbers."""
        assert engine.multiply(-5, -3) == 15
        assert engine.multiply(-5, 3) == -15

    def test_multiply_large_numbers(self, engine):
        """Test multiplication of large numbers."""
        result = engine.multiply(10**50, 10**50)
        assert result == 10**100

    def test_multiply_floats(self, engine):
        """Test multiplication with floats."""
        assert engine.multiply(2.5, 4.0) == pytest.approx(10.0)

    def test_multiply_by_inf(self, engine):
        """Test multiplication by infinity."""
        result = engine.multiply(5, float('inf'))
        assert result == float('inf')

    def test_multiply_zero_by_inf_is_nan(self, engine):
        """Test that 0 * inf = nan."""
        result = engine.multiply(0, float('inf'))
        assert math.isnan(result)

    def test_multiply_negative_inf(self, engine):
        """Test multiplication by negative infinity."""
        result = engine.multiply(-5, float('inf'))
        assert result == float('-inf')


# ============================================================================
# ARITHMETIC ENGINE - DIVIDE OPERATION EDGE CASES
# ============================================================================

class TestArithmeticEngineDivide:
    """Edge case tests for ArithmeticEngine.divide()."""

    def test_divide_basic(self, engine):
        """Test basic division."""
        assert engine.divide(10, 2) == 5.0

    def test_divide_resulting_in_float(self, engine):
        """Test division with float result."""
        result = engine.divide(10, 3)
        assert result == pytest.approx(10/3)

    def test_divide_by_zero_raises_error(self, engine):
        """Test that divide by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            engine.divide(10, 0)

    def test_divide_negative_by_negative(self, engine):
        """Test division of negative by negative."""
        assert engine.divide(-10, -2) == 5.0

    def test_divide_negative_by_positive(self, engine):
        """Test division of negative by positive."""
        assert engine.divide(-10, 2) == -5.0

    def test_divide_positive_by_negative(self, engine):
        """Test division of positive by negative."""
        assert engine.divide(10, -2) == -5.0

    def test_divide_zero_by_number(self, engine):
        """Test division of zero by number."""
        assert engine.divide(0, 5) == 0.0

    def test_divide_floats(self, engine):
        """Test division with floats."""
        result = engine.divide(10.5, 2.0)
        assert result == pytest.approx(5.25)

    def test_divide_by_very_small_number(self, engine):
        """Test division by very small number."""
        result = engine.divide(1, 1e-100)
        assert result == 1e100

    def test_divide_by_negative_zero(self, engine):
        """Test division by negative zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            engine.divide(10, -0.0)

    def test_divide_inf_by_number(self, engine):
        """Test division of infinity by number."""
        result = engine.divide(float('inf'), 5)
        assert result == float('inf')

    def test_divide_inf_by_inf_is_nan(self, engine):
        """Test that inf / inf = nan."""
        result = engine.divide(float('inf'), float('inf'))
        assert math.isnan(result)


# ============================================================================
# ARITHMETIC ENGINE - FACTORIAL OPERATION EDGE CASES
# ============================================================================

class TestArithmeticEngineFactorial:
    """Edge case tests for ArithmeticEngine.factorial()."""

    def test_factorial_of_zero(self, engine):
        """Test factorial of zero is 1."""
        assert engine.factorial(0) == 1

    def test_factorial_of_one(self, engine):
        """Test factorial of 1."""
        assert engine.factorial(1) == 1

    def test_factorial_of_small_positive(self, engine):
        """Test factorial of small positive integers."""
        assert engine.factorial(5) == 120
        assert engine.factorial(10) == 3628800

    def test_factorial_of_float_integer(self, engine):
        """Test factorial with float that is an integer (e.g., 5.0)."""
        assert engine.factorial(5.0) == 120
        assert engine.factorial(0.0) == 1

    def test_factorial_of_negative_int_raises_error(self, engine):
        """Test that factorial of negative int raises ValueError."""
        with pytest.raises(ValueError):
            engine.factorial(-1)

    def test_factorial_of_negative_float_raises_error(self, engine):
        """Test that factorial of negative float raises ValueError."""
        with pytest.raises(ValueError):
            engine.factorial(-5.0)

    def test_factorial_of_non_integer_float_raises_error(self, engine):
        """Test that factorial of non-integer float raises TypeError."""
        with pytest.raises(TypeError):
            engine.factorial(5.5)

    def test_factorial_of_bool_raises_error(self, engine):
        """Test that factorial of bool raises TypeError."""
        with pytest.raises(TypeError):
            engine.factorial(True)
        with pytest.raises(TypeError):
            engine.factorial(False)

    def test_factorial_of_none_raises_error(self, engine):
        """Test that factorial of None raises TypeError."""
        with pytest.raises(TypeError):
            engine.factorial(None)

    def test_factorial_of_string_raises_error(self, engine):
        """Test that factorial of string raises TypeError."""
        with pytest.raises(TypeError):
            engine.factorial("5")

    def test_factorial_of_large_number(self, engine):
        """Test factorial of larger number."""
        result = engine.factorial(20)
        assert result == 2432902008176640000

    def test_factorial_type_returns_int(self, engine):
        """Test that factorial always returns int."""
        assert isinstance(engine.factorial(5), int)
        assert isinstance(engine.factorial(5.0), int)


# ============================================================================
# ARITHMETIC ENGINE - SQUARE OPERATION EDGE CASES
# ============================================================================

class TestArithmeticEngineSquare:
    """Edge case tests for ArithmeticEngine.square()."""

    def test_square_positive_int(self, engine):
        """Test square of positive integer."""
        assert engine.square(5) == 25

    def test_square_negative_int(self, engine):
        """Test square of negative integer."""
        assert engine.square(-5) == 25

    def test_square_zero(self, engine):
        """Test square of zero."""
        assert engine.square(0) == 0

    def test_square_float(self, engine):
        """Test square of float."""
        result = engine.square(2.5)
        assert result == pytest.approx(6.25)

    def test_square_returns_int_when_int_input(self, engine):
        """Test that square returns int when input is int."""
        result = engine.square(5)
        assert isinstance(result, int)

    def test_square_returns_float_when_float_input(self, engine):
        """Test that square returns float when input is float."""
        result = engine.square(5.0)
        assert isinstance(result, float)

    def test_square_large_number(self, engine):
        """Test square of large number."""
        result = engine.square(10**50)
        assert result == 10**100

    def test_square_negative_float(self, engine):
        """Test square of negative float."""
        result = engine.square(-3.5)
        assert result == pytest.approx(12.25)

    def test_square_of_bool_raises_error(self, engine):
        """Test that square of bool raises TypeError."""
        with pytest.raises(TypeError):
            engine.square(True)

    def test_square_of_none_raises_error(self, engine):
        """Test that square of None raises TypeError."""
        with pytest.raises(TypeError):
            engine.square(None)

    def test_square_of_string_raises_error(self, engine):
        """Test that square of string raises TypeError."""
        with pytest.raises(TypeError):
            engine.square("5")

    def test_square_of_inf(self, engine):
        """Test square of infinity."""
        result = engine.square(float('inf'))
        assert result == float('inf')

    def test_square_of_nan(self, engine):
        """Test square of NaN."""
        result = engine.square(float('nan'))
        assert math.isnan(result)


# ============================================================================
# ARITHMETIC ENGINE - CUBE OPERATION EDGE CASES
# ============================================================================

class TestArithmeticEngineCube:
    """Edge case tests for ArithmeticEngine.cube()."""

    def test_cube_positive_int(self, engine):
        """Test cube of positive integer."""
        assert engine.cube(5) == 125

    def test_cube_negative_int(self, engine):
        """Test cube of negative integer."""
        assert engine.cube(-5) == -125

    def test_cube_zero(self, engine):
        """Test cube of zero."""
        assert engine.cube(0) == 0

    def test_cube_float(self, engine):
        """Test cube of float."""
        result = engine.cube(2.5)
        assert result == pytest.approx(15.625)

    def test_cube_returns_int_when_int_input(self, engine):
        """Test that cube returns int when input is int."""
        result = engine.cube(5)
        assert isinstance(result, int)

    def test_cube_returns_float_when_float_input(self, engine):
        """Test that cube returns float when input is float."""
        result = engine.cube(5.0)
        assert isinstance(result, float)

    def test_cube_negative_float(self, engine):
        """Test cube of negative float."""
        result = engine.cube(-3.5)
        assert result == pytest.approx(-42.875)

    def test_cube_large_number(self, engine):
        """Test cube of large number."""
        result = engine.cube(10**33)
        assert result == 10**99

    def test_cube_of_bool_raises_error(self, engine):
        """Test that cube of bool raises TypeError."""
        with pytest.raises(TypeError):
            engine.cube(True)

    def test_cube_of_none_raises_error(self, engine):
        """Test that cube of None raises TypeError."""
        with pytest.raises(TypeError):
            engine.cube(None)

    def test_cube_of_string_raises_error(self, engine):
        """Test that cube of string raises TypeError."""
        with pytest.raises(TypeError):
            engine.cube("5")


# ============================================================================
# ARITHMETIC ENGINE - SQUARE_ROOT OPERATION EDGE CASES
# ============================================================================

class TestArithmeticEngineSquareRoot:
    """Edge case tests for ArithmeticEngine.square_root()."""

    def test_square_root_of_positive_int(self, engine):
        """Test square root of positive integer."""
        assert engine.square_root(25) == 5.0

    def test_square_root_of_perfect_square(self, engine):
        """Test square root of perfect squares."""
        assert engine.square_root(1) == 1.0
        assert engine.square_root(4) == 2.0
        assert engine.square_root(9) == 3.0

    def test_square_root_of_non_perfect_square(self, engine):
        """Test square root of non-perfect squares."""
        result = engine.square_root(2)
        assert result == pytest.approx(math.sqrt(2))

    def test_square_root_of_zero(self, engine):
        """Test square root of zero."""
        assert engine.square_root(0) == 0.0

    def test_square_root_of_float(self, engine):
        """Test square root of float."""
        result = engine.square_root(6.25)
        assert result == pytest.approx(2.5)

    def test_square_root_returns_float(self, engine):
        """Test that square_root always returns float."""
        assert isinstance(engine.square_root(25), float)
        assert isinstance(engine.square_root(25.0), float)

    def test_square_root_of_negative_raises_error(self, engine):
        """Test that square root of negative raises ValueError."""
        with pytest.raises(ValueError):
            engine.square_root(-1)

    def test_square_root_of_negative_float_raises_error(self, engine):
        """Test that square root of negative float raises ValueError."""
        with pytest.raises(ValueError):
            engine.square_root(-5.5)

    def test_square_root_of_bool_raises_error(self, engine):
        """Test that square root of bool raises TypeError."""
        with pytest.raises(TypeError):
            engine.square_root(True)

    def test_square_root_of_none_raises_error(self, engine):
        """Test that square root of None raises TypeError."""
        with pytest.raises(TypeError):
            engine.square_root(None)

    def test_square_root_of_string_raises_error(self, engine):
        """Test that square root of string raises TypeError."""
        with pytest.raises(TypeError):
            engine.square_root("5")

    def test_square_root_of_very_large_number(self, engine):
        """Test square root of very large number."""
        result = engine.square_root(10**20)
        assert result == pytest.approx(10**10)

    def test_square_root_of_very_small_number(self, engine):
        """Test square root of very small number."""
        result = engine.square_root(1e-20)
        assert result == pytest.approx(1e-10)


# ============================================================================
# ARITHMETIC ENGINE - CUBE_ROOT OPERATION EDGE CASES
# ============================================================================

class TestArithmeticEngineCubeRoot:
    """Edge case tests for ArithmeticEngine.cube_root()."""

    def test_cube_root_of_positive_int(self, engine):
        """Test cube root of positive integer."""
        result = engine.cube_root(27)
        assert result == pytest.approx(3.0)

    def test_cube_root_of_negative_int(self, engine):
        """Test cube root of negative integer (should be negative)."""
        result = engine.cube_root(-27)
        assert result == pytest.approx(-3.0)

    def test_cube_root_of_zero(self, engine):
        """Test cube root of zero."""
        assert engine.cube_root(0) == 0.0

    def test_cube_root_of_one(self, engine):
        """Test cube root of one."""
        assert engine.cube_root(1) == 1.0

    def test_cube_root_of_negative_one(self, engine):
        """Test cube root of negative one."""
        assert engine.cube_root(-1) == pytest.approx(-1.0)

    def test_cube_root_of_float(self, engine):
        """Test cube root of float."""
        result = engine.cube_root(8.0)
        assert result == pytest.approx(2.0)

    def test_cube_root_preserves_sign(self, engine):
        """Test that cube root preserves sign for negative numbers."""
        result = engine.cube_root(-8.0)
        assert result == pytest.approx(-2.0)

    def test_cube_root_returns_float(self, engine):
        """Test that cube_root always returns float."""
        assert isinstance(engine.cube_root(8), float)
        assert isinstance(engine.cube_root(8.0), float)

    def test_cube_root_of_bool_raises_error(self, engine):
        """Test that cube root of bool raises TypeError."""
        with pytest.raises(TypeError):
            engine.cube_root(True)

    def test_cube_root_of_none_raises_error(self, engine):
        """Test that cube root of None raises TypeError."""
        with pytest.raises(TypeError):
            engine.cube_root(None)

    def test_cube_root_of_string_raises_error(self, engine):
        """Test that cube root of string raises TypeError."""
        with pytest.raises(TypeError):
            engine.cube_root("5")

    def test_cube_root_of_very_large_number(self, engine):
        """Test cube root of very large number."""
        result = engine.cube_root(10**30)
        assert result == pytest.approx(10**10)

    def test_cube_root_of_very_small_negative_number(self, engine):
        """Test cube root of very small negative number."""
        result = engine.cube_root(-1e-30)
        assert result == pytest.approx(-1e-10)


# ============================================================================
# ARITHMETIC ENGINE - POWER OPERATION EDGE CASES
# ============================================================================

class TestArithmeticEnginePower:
    """Edge case tests for ArithmeticEngine.power()."""

    def test_power_basic(self, engine):
        """Test basic power operation."""
        result = engine.power(2, 3)
        assert result == pytest.approx(8.0)

    def test_power_with_zero_exponent(self, engine):
        """Test power with zero exponent (should be 1)."""
        result = engine.power(5, 0)
        assert result == pytest.approx(1.0)

    def test_power_with_negative_exponent(self, engine):
        """Test power with negative exponent."""
        result = engine.power(2, -2)
        assert result == pytest.approx(0.25)

    def test_power_with_float_exponent(self, engine):
        """Test power with float exponent."""
        result = engine.power(4, 0.5)
        assert result == pytest.approx(2.0)

    def test_power_with_negative_base_even_exponent(self, engine):
        """Test power with negative base and even exponent."""
        result = engine.power(-2, 2)
        assert result == pytest.approx(4.0)

    def test_power_with_negative_base_odd_exponent(self, engine):
        """Test power with negative base and odd exponent."""
        result = engine.power(-2, 3)
        assert result == pytest.approx(-8.0)

    def test_power_returns_float(self, engine):
        """Test that power always returns float."""
        assert isinstance(engine.power(2, 3), float)
        assert isinstance(engine.power(2.0, 3.0), float)

    def test_power_base_is_bool_raises_error(self, engine):
        """Test that power with bool base raises TypeError."""
        with pytest.raises(TypeError):
            engine.power(True, 2)

    def test_power_exponent_is_bool_raises_error(self, engine):
        """Test that power with bool exponent raises TypeError."""
        with pytest.raises(TypeError):
            engine.power(2, True)

    def test_power_base_is_none_raises_error(self, engine):
        """Test that power with None base raises TypeError."""
        with pytest.raises(TypeError):
            engine.power(None, 2)

    def test_power_exponent_is_none_raises_error(self, engine):
        """Test that power with None exponent raises TypeError."""
        with pytest.raises(TypeError):
            engine.power(2, None)

    def test_power_base_is_string_raises_error(self, engine):
        """Test that power with string base raises TypeError."""
        with pytest.raises(TypeError):
            engine.power("2", 3)

    def test_power_exponent_is_string_raises_error(self, engine):
        """Test that power with string exponent raises TypeError."""
        with pytest.raises(TypeError):
            engine.power(2, "3")

    def test_power_with_large_numbers(self, engine):
        """Test power with large numbers."""
        result = engine.power(10, 20)
        assert result == pytest.approx(1e20)

    def test_power_zero_to_positive_exponent(self, engine):
        """Test 0 to positive exponent is 0."""
        result = engine.power(0, 5)
        assert result == pytest.approx(0.0)

    def test_power_zero_to_zero_is_one(self, engine):
        """Test 0^0 = 1 (Python convention)."""
        result = engine.power(0, 0)
        assert result == pytest.approx(1.0)


# ============================================================================
# ARITHMETIC ENGINE - LOG10 OPERATION EDGE CASES
# ============================================================================

class TestArithmeticEngineLog10:
    """Edge case tests for ArithmeticEngine.log10()."""

    def test_log10_of_ten(self, engine):
        """Test log10 of 10 is 1."""
        result = engine.log10(10)
        assert result == pytest.approx(1.0)

    def test_log10_of_one_hundred(self, engine):
        """Test log10 of 100 is 2."""
        result = engine.log10(100)
        assert result == pytest.approx(2.0)

    def test_log10_of_one(self, engine):
        """Test log10 of 1 is 0."""
        result = engine.log10(1)
        assert result == pytest.approx(0.0)

    def test_log10_of_float(self, engine):
        """Test log10 of float."""
        result = engine.log10(2.5)
        assert result == pytest.approx(math.log10(2.5))

    def test_log10_returns_float(self, engine):
        """Test that log10 always returns float."""
        assert isinstance(engine.log10(10), float)
        assert isinstance(engine.log10(10.0), float)

    def test_log10_of_zero_raises_error(self, engine):
        """Test that log10 of 0 raises ValueError."""
        with pytest.raises(ValueError):
            engine.log10(0)

    def test_log10_of_negative_raises_error(self, engine):
        """Test that log10 of negative raises ValueError."""
        with pytest.raises(ValueError):
            engine.log10(-10)

    def test_log10_of_negative_float_raises_error(self, engine):
        """Test that log10 of negative float raises ValueError."""
        with pytest.raises(ValueError):
            engine.log10(-5.5)

    def test_log10_of_bool_raises_error(self, engine):
        """Test that log10 of bool raises TypeError."""
        with pytest.raises(TypeError):
            engine.log10(True)

    def test_log10_of_none_raises_error(self, engine):
        """Test that log10 of None raises TypeError."""
        with pytest.raises(TypeError):
            engine.log10(None)

    def test_log10_of_string_raises_error(self, engine):
        """Test that log10 of string raises TypeError."""
        with pytest.raises(TypeError):
            engine.log10("10")

    def test_log10_of_very_small_positive_number(self, engine):
        """Test log10 of very small positive number."""
        result = engine.log10(1e-100)
        assert result == pytest.approx(-100.0)

    def test_log10_of_very_large_number(self, engine):
        """Test log10 of very large number."""
        result = engine.log10(1e100)
        assert result == pytest.approx(100.0)


# ============================================================================
# ARITHMETIC ENGINE - NATURAL_LOG OPERATION EDGE CASES
# ============================================================================

class TestArithmeticEngineNaturalLog:
    """Edge case tests for ArithmeticEngine.natural_log()."""

    def test_natural_log_of_e(self, engine):
        """Test natural log of e is 1."""
        result = engine.natural_log(math.e)
        assert result == pytest.approx(1.0)

    def test_natural_log_of_one(self, engine):
        """Test natural log of 1 is 0."""
        result = engine.natural_log(1)
        assert result == pytest.approx(0.0)

    def test_natural_log_of_float(self, engine):
        """Test natural log of float."""
        result = engine.natural_log(2.5)
        assert result == pytest.approx(math.log(2.5))

    def test_natural_log_returns_float(self, engine):
        """Test that natural_log always returns float."""
        assert isinstance(engine.natural_log(math.e), float)
        assert isinstance(engine.natural_log(math.e * 1.0), float)

    def test_natural_log_of_zero_raises_error(self, engine):
        """Test that natural_log of 0 raises ValueError."""
        with pytest.raises(ValueError):
            engine.natural_log(0)

    def test_natural_log_of_negative_raises_error(self, engine):
        """Test that natural_log of negative raises ValueError."""
        with pytest.raises(ValueError):
            engine.natural_log(-1)

    def test_natural_log_of_negative_float_raises_error(self, engine):
        """Test that natural_log of negative float raises ValueError."""
        with pytest.raises(ValueError):
            engine.natural_log(-5.5)

    def test_natural_log_of_bool_raises_error(self, engine):
        """Test that natural_log of bool raises TypeError."""
        with pytest.raises(TypeError):
            engine.natural_log(True)

    def test_natural_log_of_none_raises_error(self, engine):
        """Test that natural_log of None raises TypeError."""
        with pytest.raises(TypeError):
            engine.natural_log(None)

    def test_natural_log_of_string_raises_error(self, engine):
        """Test that natural_log of string raises TypeError."""
        with pytest.raises(TypeError):
            engine.natural_log("e")

    def test_natural_log_of_very_small_positive_number(self, engine):
        """Test natural_log of very small positive number."""
        result = engine.natural_log(1e-100)
        assert result == pytest.approx(math.log(1e-100))

    def test_natural_log_of_very_large_number(self, engine):
        """Test natural_log of very large number."""
        result = engine.natural_log(1e100)
        assert result == pytest.approx(math.log(1e100))


# ============================================================================
# CALCULATOR - HISTORY RECORDING TESTS
# ============================================================================

class TestCalculatorHistoryRecording:
    """Verify that Calculator records operations in history."""

    def test_add_records_operation_in_history(self, calculator):
        """Verify add operation is recorded."""
        calculator.add(5, 3)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0].operation_name == "add"
        assert history[0].operands == [5, 3]
        assert history[0].result == 8

    def test_subtract_records_operation_in_history(self, calculator):
        """Verify subtract operation is recorded."""
        calculator.subtract(10, 3)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0].operation_name == "subtract"
        assert history[0].operands == [10, 3]
        assert history[0].result == 7

    def test_multiply_records_operation_in_history(self, calculator):
        """Verify multiply operation is recorded."""
        calculator.multiply(5, 4)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0].operation_name == "multiply"
        assert history[0].operands == [5, 4]
        assert history[0].result == 20

    def test_divide_records_operation_in_history(self, calculator):
        """Verify divide operation is recorded."""
        calculator.divide(10, 2)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0].operation_name == "divide"
        assert history[0].operands == [10, 2]
        assert history[0].result == 5.0

    def test_factorial_records_operation_in_history(self, calculator):
        """Verify factorial operation is recorded."""
        calculator.factorial(5)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0].operation_name == "factorial"
        assert history[0].operands == [5]
        assert history[0].result == 120

    def test_square_records_operation_in_history(self, calculator):
        """Verify square operation is recorded."""
        calculator.square(5)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0].operation_name == "square"
        assert history[0].operands == [5]
        assert history[0].result == 25

    def test_cube_records_operation_in_history(self, calculator):
        """Verify cube operation is recorded."""
        calculator.cube(5)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0].operation_name == "cube"
        assert history[0].operands == [5]
        assert history[0].result == 125

    def test_square_root_records_operation_in_history(self, calculator):
        """Verify square_root operation is recorded."""
        calculator.square_root(25)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0].operation_name == "square_root"
        assert history[0].operands == [25]
        assert history[0].result == 5.0

    def test_cube_root_records_operation_in_history(self, calculator):
        """Verify cube_root operation is recorded."""
        calculator.cube_root(27)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0].operation_name == "cube_root"
        assert history[0].operands == [27]
        assert history[0].result == pytest.approx(3.0)

    def test_power_records_operation_in_history(self, calculator):
        """Verify power operation is recorded."""
        calculator.power(2, 3)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0].operation_name == "power"
        assert history[0].operands == [2, 3]
        assert history[0].result == 8.0

    def test_log10_records_operation_in_history(self, calculator):
        """Verify log10 operation is recorded."""
        calculator.log10(100)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0].operation_name == "log10"
        assert history[0].operands == [100]
        assert history[0].result == 2.0

    def test_natural_log_records_operation_in_history(self, calculator):
        """Verify natural_log operation is recorded."""
        calculator.natural_log(math.e)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0].operation_name == "natural_log"
        assert history[0].operands == [math.e]
        assert history[0].result == pytest.approx(1.0)

    def test_multiple_operations_all_recorded(self, calculator):
        """Verify multiple operations are all recorded."""
        calculator.add(5, 3)
        calculator.multiply(8, 2)
        calculator.square(4)
        history = calculator.get_history()
        assert len(history) == 3
        assert history[0].operation_name == "add"
        assert history[1].operation_name == "multiply"
        assert history[2].operation_name == "square"

    def test_operations_have_timestamp(self, calculator):
        """Verify operations have timestamps."""
        calculator.add(5, 3)
        history = calculator.get_history()
        assert history[0].timestamp is not None
        assert isinstance(history[0].timestamp, datetime)

    def test_factorial_with_float_records_as_int(self, calculator):
        """Verify factorial with float 5.0 records as int 5."""
        calculator.factorial(5.0)
        history = calculator.get_history()
        assert history[0].operands == [5]  # Should be int, not float

    def test_failed_operation_not_recorded(self, calculator):
        """Verify failed operations are not recorded in history."""
        initial_count = len(calculator.get_history())
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)
        # History should not have been modified
        assert len(calculator.get_history()) == initial_count

    def test_failed_type_error_not_recorded(self, calculator):
        """Verify failed type error operations are not recorded."""
        initial_count = len(calculator.get_history())
        with pytest.raises(TypeError):
            calculator.square(None)
        assert len(calculator.get_history()) == initial_count


# ============================================================================
# CALCULATOR - CLEAR HISTORY TESTS
# ============================================================================

class TestCalculatorClearHistory:
    """Verify that Calculator can clear its history."""

    def test_clear_history_removes_all_records(self, calculator):
        """Verify clear_history removes all records."""
        calculator.add(5, 3)
        calculator.multiply(8, 2)
        assert len(calculator.get_history()) == 2
        calculator.clear_history()
        assert len(calculator.get_history()) == 0

    def test_clear_history_on_empty_history(self, calculator):
        """Verify clear_history works on empty history."""
        assert len(calculator.get_history()) == 0
        calculator.clear_history()
        assert len(calculator.get_history()) == 0

    def test_operations_after_clear_are_recorded(self, calculator):
        """Verify operations after clear are still recorded."""
        calculator.add(5, 3)
        calculator.clear_history()
        calculator.multiply(8, 2)
        history = calculator.get_history()
        assert len(history) == 1
        assert history[0].operation_name == "multiply"

    def test_get_history_returns_copy(self, calculator):
        """Verify get_history returns independent copy."""
        calculator.add(5, 3)
        history1 = calculator.get_history()
        calculator.multiply(8, 2)
        history2 = calculator.get_history()
        assert len(history1) == 1
        assert len(history2) == 2


# ============================================================================
# CALCULATOR - STATEFUL BEHAVIOR TESTS
# ============================================================================

class TestCalculatorStateful:
    """Verify Calculator state isolation between instances."""

    def test_multiple_calculator_instances_have_separate_history(self):
        """Verify each Calculator instance has its own history."""
        calc1 = Calculator()
        calc2 = Calculator()

        calc1.add(5, 3)
        calc2.add(10, 20)

        assert len(calc1.get_history()) == 1
        assert len(calc2.get_history()) == 1
        assert calc1.get_history()[0].result == 8
        assert calc2.get_history()[0].result == 30

    def test_calculator_engine_isolation(self):
        """Verify ArithmeticEngine instances are independent."""
        engine1 = ArithmeticEngine()
        engine2 = ArithmeticEngine()

        # Both should compute the same value independently
        assert engine1.add(5, 3) == engine2.add(5, 3)
        # Engines don't have state, so no need to verify isolation

    def test_calculator_operations_dont_share_state(self):
        """Verify calculator operations don't affect other instances."""
        calc1 = Calculator()
        calc2 = Calculator()

        calc1.add(5, 3)
        calc1.clear_history()

        # calc2 should be unaffected
        assert len(calc2.get_history()) == 0


# ============================================================================
# CALCULATOR - INTEGRATION TESTS
# ============================================================================

class TestCalculatorIntegration:
    """Integration tests for Calculator wrapping ArithmeticEngine."""

    def test_calculator_produces_same_results_as_engine(self, calculator, engine):
        """Verify Calculator delegates to engine correctly."""
        # Test add
        calc_result = calculator.add(5, 3)
        engine_result = engine.add(5, 3)
        assert calc_result == engine_result

        # Test subtract
        calc_result = calculator.subtract(10, 3)
        engine_result = engine.subtract(10, 3)
        assert calc_result == engine_result

        # Test multiply
        calc_result = calculator.multiply(5, 4)
        engine_result = engine.multiply(5, 4)
        assert calc_result == engine_result

        # Test divide
        calc_result = calculator.divide(10, 2)
        engine_result = engine.divide(10, 2)
        assert calc_result == engine_result

    def test_calculator_complex_operation_sequence(self, calculator):
        """Test complex sequence of operations."""
        result1 = calculator.add(10, 5)  # 15
        result2 = calculator.multiply(result1, 2)  # 30
        result3 = calculator.divide(result2, 3)  # 10.0

        assert result1 == 15
        assert result2 == 30
        assert result3 == pytest.approx(10.0)

        history = calculator.get_history()
        assert len(history) == 3

    def test_calculator_error_propagates_from_engine(self, calculator):
        """Verify Calculator propagates engine errors correctly."""
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)

        with pytest.raises(ValueError):
            calculator.square_root(-1)

        with pytest.raises(TypeError):
            calculator.factorial("5")


# ============================================================================
# CALCULATOR REGISTRY INTEGRATION TESTS
# ============================================================================


class TestCalculatorRegistryIntegration:
    """Test that Calculator has integrated OperationRegistry correctly."""

    def test_calculator_has_registry_attribute(self, calculator):
        """Test that Calculator has a _registry attribute."""
        assert hasattr(calculator, '_registry')
        assert calculator._registry is not None

    def test_registry_is_operation_registry_instance(self, calculator):
        """Test that _registry is an OperationRegistry instance."""
        from src.operations.base import OperationRegistry
        assert isinstance(calculator._registry, OperationRegistry)

    def test_registry_has_all_12_basic_operations(self, calculator):
        """Test that the registry has all 12 basic operations registered."""
        operations = calculator._registry.list_operations()
        assert len(operations) >= 12

        expected_operations = [
            "add", "subtract", "multiply", "divide",
            "factorial", "square", "cube",
            "square_root", "cube_root",
            "power", "log10", "natural_log"
        ]

        for op_name in expected_operations:
            assert op_name in operations, f"Operation '{op_name}' not found in registry"

    def test_calculator_registry_has_add_operation(self, calculator):
        """Test that the registry has the 'add' operation."""
        assert calculator._registry.is_registered("add")
        add_op = calculator._registry.get("add")
        assert add_op is not None

    def test_calculator_registry_has_multiply_operation(self, calculator):
        """Test that the registry has the 'multiply' operation."""
        assert calculator._registry.is_registered("multiply")
        multiply_op = calculator._registry.get("multiply")
        assert multiply_op is not None

    def test_calculator_registry_has_divide_operation(self, calculator):
        """Test that the registry has the 'divide' operation."""
        assert calculator._registry.is_registered("divide")
        divide_op = calculator._registry.get("divide")
        assert divide_op is not None

    def test_calculator_registry_has_factorial_operation(self, calculator):
        """Test that the registry has the 'factorial' operation."""
        assert calculator._registry.is_registered("factorial")
        factorial_op = calculator._registry.get("factorial")
        assert factorial_op is not None

    def test_calculator_registry_has_square_operation(self, calculator):
        """Test that the registry has the 'square' operation."""
        assert calculator._registry.is_registered("square")
        square_op = calculator._registry.get("square")
        assert square_op is not None

    def test_calculator_registry_has_power_operation(self, calculator):
        """Test that the registry has the 'power' operation."""
        assert calculator._registry.is_registered("power")
        power_op = calculator._registry.get("power")
        assert power_op is not None

    def test_registry_operations_are_callable(self, calculator):
        """Test that each registered operation can be executed."""
        # Test Add
        add_op = calculator._registry.get("add")
        result = add_op.execute(3, 4)
        assert result == 7.0

        # Test Multiply
        multiply_op = calculator._registry.get("multiply")
        result = multiply_op.execute(3, 4)
        assert result == 12.0

        # Test Square
        square_op = calculator._registry.get("square")
        result = square_op.execute(4)
        assert result == 16.0

        # Test Factorial
        factorial_op = calculator._registry.get("factorial")
        result = factorial_op.execute(5)
        assert result == 120.0

    def test_registry_operations_have_correct_operand_counts(self, calculator):
        """Test that operations report correct operand counts."""
        # Binary operations
        assert calculator._registry.get("add").operand_count() == 2
        assert calculator._registry.get("subtract").operand_count() == 2
        assert calculator._registry.get("multiply").operand_count() == 2
        assert calculator._registry.get("divide").operand_count() == 2
        assert calculator._registry.get("power").operand_count() == 2

        # Unary operations
        assert calculator._registry.get("factorial").operand_count() == 1
        assert calculator._registry.get("square").operand_count() == 1
        assert calculator._registry.get("cube").operand_count() == 1
        assert calculator._registry.get("square_root").operand_count() == 1
        assert calculator._registry.get("cube_root").operand_count() == 1
        assert calculator._registry.get("log10").operand_count() == 1
        assert calculator._registry.get("natural_log").operand_count() == 1

    def test_multiple_calculator_instances_have_independent_registries(self):
        """Test that each Calculator instance has its own independent registry."""
        from src.logic import Calculator

        calc1 = Calculator()
        calc2 = Calculator()

        # They should be different instances
        assert calc1._registry is not calc2._registry

        # But they should both have the same operations
        assert set(calc1._registry.list_operations()) == set(calc2._registry.list_operations())

    def test_registry_does_not_affect_calculator_arithmetic(self, calculator):
        """Test that adding registry doesn't break Calculator arithmetic."""
        # The Calculator should still work normally
        result = calculator.add(5, 3)
        assert result == 8

        result = calculator.multiply(4, 5)
        assert result == 20

        result = calculator.divide(10, 2)
        assert result == 5.0

        # And history should be recorded
        history = calculator.get_history()
        assert len(history) == 3
