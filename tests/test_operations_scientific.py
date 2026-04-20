"""Comprehensive tests for scientific operation classes.

Tests cover:
- All 8 operation classes: Sin, Cos, Tan, Exp, Log, Log10, Sqrt, Factorial
- Names match expected strings
- operand_count() = 1 for all
- execute() returns correct results
- Domain error cases (Tan(pi/2), Log(-1), Sqrt(-1), etc.)
- Factorial with edge cases
- register_scientific_operations adds all 8 to registry
"""

import pytest
import math
from src.operations.scientific import (
    Sin, Cos, Tan, Exp, Log, Log10, Sqrt, Factorial,
    register_scientific_operations,
)
from src.operations.base import OperationRegistry


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def registry():
    """Provides a fresh OperationRegistry instance for each test."""
    return OperationRegistry()


# ============================================================================
# SIN OPERATION TESTS
# ============================================================================

class TestSinOperation:
    """Test suite for Sin operation class."""

    def test_sin_name(self):
        """Test that Sin operation has name 'sin'."""
        assert Sin().name() == "sin"

    def test_sin_operand_count(self):
        """Test that Sin has operand_count 1."""
        assert Sin().operand_count() == 1

    def test_sin_zero(self):
        """Test sin(0) == 0."""
        assert Sin().execute(0) == pytest.approx(0.0)

    def test_sin_pi_over_2(self):
        """Test sin(pi/2) == 1."""
        assert Sin().execute(math.pi / 2) == pytest.approx(1.0)

    def test_sin_pi_over_4(self):
        """Test sin(pi/4) == sqrt(2)/2."""
        assert Sin().execute(math.pi / 4) == pytest.approx(math.sqrt(2) / 2)


# ============================================================================
# COS OPERATION TESTS
# ============================================================================

class TestCosOperation:
    """Test suite for Cos operation class."""

    def test_cos_name(self):
        """Test that Cos operation has name 'cos'."""
        assert Cos().name() == "cos"

    def test_cos_operand_count(self):
        """Test that Cos has operand_count 1."""
        assert Cos().operand_count() == 1

    def test_cos_zero(self):
        """Test cos(0) == 1."""
        assert Cos().execute(0) == pytest.approx(1.0)

    def test_cos_pi(self):
        """Test cos(pi) == -1."""
        assert Cos().execute(math.pi) == pytest.approx(-1.0)

    def test_cos_pi_over_4(self):
        """Test cos(pi/4) == sqrt(2)/2."""
        assert Cos().execute(math.pi / 4) == pytest.approx(math.sqrt(2) / 2)


# ============================================================================
# TAN OPERATION TESTS
# ============================================================================

class TestTanOperation:
    """Test suite for Tan operation class."""

    def test_tan_name(self):
        """Test that Tan operation has name 'tan'."""
        assert Tan().name() == "tan"

    def test_tan_operand_count(self):
        """Test that Tan has operand_count 1."""
        assert Tan().operand_count() == 1

    def test_tan_zero(self):
        """Test tan(0) == 0."""
        assert Tan().execute(0) == pytest.approx(0.0)

    def test_tan_pi_over_4(self):
        """Test tan(pi/4) == 1."""
        assert Tan().execute(math.pi / 4) == pytest.approx(1.0)

    def test_tan_pi_over_2_raises_valueerror(self):
        """Test that tan(pi/2) raises ValueError."""
        with pytest.raises(ValueError):
            Tan().execute(math.pi / 2)

    def test_tan_3pi_over_2_raises_valueerror(self):
        """Test that tan(3*pi/2) raises ValueError."""
        with pytest.raises(ValueError):
            Tan().execute(3 * math.pi / 2)


# ============================================================================
# EXP OPERATION TESTS
# ============================================================================

class TestExpOperation:
    """Test suite for Exp operation class."""

    def test_exp_name(self):
        """Test that Exp operation has name 'exp'."""
        assert Exp().name() == "exp"

    def test_exp_operand_count(self):
        """Test that Exp has operand_count 1."""
        assert Exp().operand_count() == 1

    def test_exp_zero(self):
        """Test exp(0) == 1."""
        assert Exp().execute(0) == pytest.approx(1.0)

    def test_exp_one(self):
        """Test exp(1) == e."""
        assert Exp().execute(1) == pytest.approx(math.e)

    def test_exp_negative_one(self):
        """Test exp(-1) == 1/e."""
        assert Exp().execute(-1) == pytest.approx(1 / math.e)


# ============================================================================
# LOG OPERATION TESTS
# ============================================================================

class TestLogOperation:
    """Test suite for Log operation class (natural logarithm)."""

    def test_log_name(self):
        """Test that Log operation has name 'log'."""
        assert Log().name() == "log"

    def test_log_operand_count(self):
        """Test that Log has operand_count 1."""
        assert Log().operand_count() == 1

    def test_log_one(self):
        """Test log(1) == 0."""
        assert Log().execute(1) == pytest.approx(0.0)

    def test_log_e(self):
        """Test log(e) == 1."""
        assert Log().execute(math.e) == pytest.approx(1.0)

    def test_log_e_squared(self):
        """Test log(e^2) == 2."""
        assert Log().execute(math.e ** 2) == pytest.approx(2.0)

    def test_log_zero_raises_valueerror(self):
        """Test that log(0) raises ValueError."""
        with pytest.raises(ValueError):
            Log().execute(0)

    def test_log_negative_raises_valueerror(self):
        """Test that log of negative raises ValueError."""
        with pytest.raises(ValueError):
            Log().execute(-1)


# ============================================================================
# LOG10 OPERATION TESTS
# ============================================================================

class TestLog10Operation:
    """Test suite for Log10 operation class."""

    def test_log10_name(self):
        """Test that Log10 operation has name 'log10'."""
        assert Log10().name() == "log10"

    def test_log10_operand_count(self):
        """Test that Log10 has operand_count 1."""
        assert Log10().operand_count() == 1

    def test_log10_one(self):
        """Test log10(1) == 0."""
        assert Log10().execute(1) == pytest.approx(0.0)

    def test_log10_ten(self):
        """Test log10(10) == 1."""
        assert Log10().execute(10) == pytest.approx(1.0)

    def test_log10_hundred(self):
        """Test log10(100) == 2."""
        assert Log10().execute(100) == pytest.approx(2.0)

    def test_log10_zero_raises_valueerror(self):
        """Test that log10(0) raises ValueError."""
        with pytest.raises(ValueError):
            Log10().execute(0)

    def test_log10_negative_raises_valueerror(self):
        """Test that log10 of negative raises ValueError."""
        with pytest.raises(ValueError):
            Log10().execute(-5)


# ============================================================================
# SQRT OPERATION TESTS
# ============================================================================

class TestSqrtOperation:
    """Test suite for Sqrt operation class."""

    def test_sqrt_name(self):
        """Test that Sqrt operation has name 'sqrt'."""
        assert Sqrt().name() == "sqrt"

    def test_sqrt_operand_count(self):
        """Test that Sqrt has operand_count 1."""
        assert Sqrt().operand_count() == 1

    def test_sqrt_zero(self):
        """Test sqrt(0) == 0."""
        assert Sqrt().execute(0) == pytest.approx(0.0)

    def test_sqrt_one(self):
        """Test sqrt(1) == 1."""
        assert Sqrt().execute(1) == pytest.approx(1.0)

    def test_sqrt_four(self):
        """Test sqrt(4) == 2."""
        assert Sqrt().execute(4) == pytest.approx(2.0)

    def test_sqrt_two(self):
        """Test sqrt(2) == sqrt(2)."""
        assert Sqrt().execute(2) == pytest.approx(math.sqrt(2))

    def test_sqrt_negative_raises_valueerror(self):
        """Test that sqrt of negative raises ValueError."""
        with pytest.raises(ValueError):
            Sqrt().execute(-1)


# ============================================================================
# FACTORIAL OPERATION TESTS
# ============================================================================

class TestFactorialOperation:
    """Test suite for Factorial operation class."""

    def test_factorial_name(self):
        """Test that Factorial operation has name 'factorial'."""
        assert Factorial().name() == "factorial"

    def test_factorial_operand_count(self):
        """Test that Factorial has operand_count 1."""
        assert Factorial().operand_count() == 1

    def test_factorial_zero(self):
        """Test factorial(0) == 1."""
        assert Factorial().execute(0) == 1

    def test_factorial_one(self):
        """Test factorial(1) == 1."""
        assert Factorial().execute(1) == 1

    def test_factorial_five(self):
        """Test factorial(5) == 120."""
        assert Factorial().execute(5) == 120

    def test_factorial_ten(self):
        """Test factorial(10) == 3628800."""
        assert Factorial().execute(10) == 3628800

    def test_factorial_float_equal_to_integer(self):
        """Test that float values equal to integers are accepted."""
        assert Factorial().execute(5.0) == 120
        assert Factorial().execute(0.0) == 1
        assert Factorial().execute(10.0) == 3628800

    def test_factorial_negative_raises_valueerror(self):
        """Test that factorial of negative raises ValueError."""
        with pytest.raises(ValueError):
            Factorial().execute(-1)

    def test_factorial_non_integer_float_raises_valueerror(self):
        """Test that factorial of non-integer float raises ValueError."""
        with pytest.raises(ValueError):
            Factorial().execute(1.5)

        with pytest.raises(ValueError):
            Factorial().execute(5.5)


# ============================================================================
# OPERATION REGISTRATION TESTS
# ============================================================================

class TestRegisterScientificOperations:
    """Test the register_scientific_operations function."""

    def test_register_scientific_operations_adds_all_eight(self, registry):
        """Test that register_scientific_operations registers all 8 operations."""
        assert registry.list_operations() == []
        register_scientific_operations(registry)
        operations = registry.list_operations()

        assert len(operations) == 8
        assert set(operations) == {"sin", "cos", "tan", "exp", "log", "log10", "sqrt", "factorial"}

    def test_all_registered_operations_are_callable(self, registry):
        """Test that each registered operation can be executed."""
        register_scientific_operations(registry)

        sin_op = registry.get("sin")
        assert sin_op is not None
        assert sin_op.execute(0) == pytest.approx(0.0)

        cos_op = registry.get("cos")
        assert cos_op is not None
        assert cos_op.execute(0) == pytest.approx(1.0)

        sqrt_op = registry.get("sqrt")
        assert sqrt_op is not None
        assert sqrt_op.execute(4) == pytest.approx(2.0)

    def test_registered_operations_have_correct_operand_counts(self, registry):
        """Test that all registered scientific operations have operand_count == 1."""
        register_scientific_operations(registry)

        for op_name in ["sin", "cos", "tan", "exp", "log", "log10", "sqrt", "factorial"]:
            op = registry.get(op_name)
            assert op is not None
            assert op.operand_count() == 1

    def test_register_multiple_times(self, registry):
        """Test that calling register_scientific_operations twice works correctly."""
        register_scientific_operations(registry)
        first_list = set(registry.list_operations())

        register_scientific_operations(registry)
        second_list = set(registry.list_operations())

        assert first_list == second_list
        assert len(first_list) == 8

    def test_registered_sin_operation_name(self, registry):
        """Test that registered sin operation has correct name."""
        register_scientific_operations(registry)
        sin_op = registry.get("sin")
        assert sin_op.name() == "sin"

    def test_registered_cos_operation_name(self, registry):
        """Test that registered cos operation has correct name."""
        register_scientific_operations(registry)
        cos_op = registry.get("cos")
        assert cos_op.name() == "cos"

    def test_registered_tan_operation_name(self, registry):
        """Test that registered tan operation has correct name."""
        register_scientific_operations(registry)
        tan_op = registry.get("tan")
        assert tan_op.name() == "tan"

    def test_registered_exp_operation_name(self, registry):
        """Test that registered exp operation has correct name."""
        register_scientific_operations(registry)
        exp_op = registry.get("exp")
        assert exp_op.name() == "exp"

    def test_registered_log_operation_name(self, registry):
        """Test that registered log operation has correct name."""
        register_scientific_operations(registry)
        log_op = registry.get("log")
        assert log_op.name() == "log"

    def test_registered_log10_operation_name(self, registry):
        """Test that registered log10 operation has correct name."""
        register_scientific_operations(registry)
        log10_op = registry.get("log10")
        assert log10_op.name() == "log10"

    def test_registered_sqrt_operation_name(self, registry):
        """Test that registered sqrt operation has correct name."""
        register_scientific_operations(registry)
        sqrt_op = registry.get("sqrt")
        assert sqrt_op.name() == "sqrt"

    def test_registered_factorial_operation_name(self, registry):
        """Test that registered factorial operation has correct name."""
        register_scientific_operations(registry)
        factorial_op = registry.get("factorial")
        assert factorial_op.name() == "factorial"


# ============================================================================
# EDGE CASES AND SPECIAL VALUES
# ============================================================================

class TestScientificOperationsEdgeCases:
    """Test edge cases for scientific operations."""

    def test_sin_large_angle(self):
        """Test sin with large angle."""
        # sin(10*pi) should be approximately 0
        assert Sin().execute(10 * math.pi) == pytest.approx(0.0, abs=1e-9)

    def test_cos_large_angle(self):
        """Test cos with large angle."""
        # cos(10*pi) should be approximately 1
        assert Cos().execute(10 * math.pi) == pytest.approx(1.0, abs=1e-9)

    def test_exp_large_negative(self):
        """Test exp with large negative number."""
        # exp(-100) should be approximately 0
        result = Exp().execute(-100)
        assert result < 1e-40

    def test_log_very_small_positive(self):
        """Test log of very small positive number."""
        result = Log().execute(1e-10)
        assert result < 0
        assert result == pytest.approx(math.log(1e-10))

    def test_sqrt_perfect_squares(self):
        """Test sqrt with various perfect squares."""
        for i in range(0, 20):
            assert Sqrt().execute(i * i) == pytest.approx(float(i))

    def test_factorial_small_values(self):
        """Test factorial with small values."""
        expected = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
        for i, exp in enumerate(expected):
            assert Factorial().execute(i) == exp
