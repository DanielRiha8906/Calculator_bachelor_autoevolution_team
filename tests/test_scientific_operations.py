"""Comprehensive tests for scientific operations (sin, cos, tan, exp).

Tests cover:
- ArithmeticEngine methods: sin, cos, tan, exp
- Scientific operation classes: Sin, Cos, Tan, Exp
- register_scientific_operations function
"""

import pytest
import math
from src.logic.core import ArithmeticEngine
from src.operations.scientific import (
    Sin, Cos, Tan, Exp,
    register_scientific_operations,
)
from src.operations.base import OperationRegistry


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def engine():
    """Provides a fresh ArithmeticEngine instance for each test."""
    return ArithmeticEngine()


@pytest.fixture
def registry():
    """Provides a fresh OperationRegistry instance for each test."""
    return OperationRegistry()


# ============================================================================
# TEST ARITHMETIC ENGINE SIN
# ============================================================================


class TestArithmeticEngineSin:
    """Test suite for ArithmeticEngine.sin method."""

    def test_sin_zero(self, engine):
        """Test sin(0) = 0."""
        assert engine.sin(0) == pytest.approx(0.0)

    def test_sin_pi_over_2(self, engine):
        """Test sin(π/2) ≈ 1."""
        assert engine.sin(math.pi / 2) == pytest.approx(1.0)

    def test_sin_pi(self, engine):
        """Test sin(π) ≈ 0."""
        assert engine.sin(math.pi) == pytest.approx(0.0, abs=1e-10)

    def test_sin_negative_pi_over_2(self, engine):
        """Test sin(-π/2) ≈ -1."""
        assert engine.sin(-math.pi / 2) == pytest.approx(-1.0)

    def test_sin_pi_over_6(self, engine):
        """Test sin(π/6) ≈ 0.5."""
        assert engine.sin(math.pi / 6) == pytest.approx(0.5)

    def test_sin_negative_number(self, engine):
        """Test sin of negative radian."""
        assert engine.sin(-1.0) == pytest.approx(math.sin(-1.0))

    def test_sin_large_radian(self, engine):
        """Test sin of large radian value."""
        result = engine.sin(100.0)
        assert isinstance(result, float)

    def test_sin_small_positive_float(self, engine):
        """Test sin of small positive float."""
        assert engine.sin(0.1) == pytest.approx(math.sin(0.1))

    def test_sin_integer_input(self, engine):
        """Test sin with integer input."""
        assert engine.sin(1) == pytest.approx(math.sin(1))

    def test_sin_float_input(self, engine):
        """Test sin with float input."""
        assert engine.sin(1.5) == pytest.approx(math.sin(1.5))

    def test_sin_bool_true_raises_type_error(self, engine):
        """Test sin(True) raises TypeError."""
        with pytest.raises(TypeError):
            engine.sin(True)

    def test_sin_bool_false_raises_type_error(self, engine):
        """Test sin(False) raises TypeError."""
        with pytest.raises(TypeError):
            engine.sin(False)

    def test_sin_none_raises_type_error(self, engine):
        """Test sin(None) raises TypeError."""
        with pytest.raises(TypeError):
            engine.sin(None)

    def test_sin_string_raises_type_error(self, engine):
        """Test sin(string) raises TypeError."""
        with pytest.raises(TypeError):
            engine.sin("1.0")

    def test_sin_list_raises_type_error(self, engine):
        """Test sin(list) raises TypeError."""
        with pytest.raises(TypeError):
            engine.sin([1.0])

    def test_sin_dict_raises_type_error(self, engine):
        """Test sin(dict) raises TypeError."""
        with pytest.raises(TypeError):
            engine.sin({"x": 1.0})


# ============================================================================
# TEST ARITHMETIC ENGINE COS
# ============================================================================


class TestArithmeticEngineCos:
    """Test suite for ArithmeticEngine.cos method."""

    def test_cos_zero(self, engine):
        """Test cos(0) = 1."""
        assert engine.cos(0) == pytest.approx(1.0)

    def test_cos_pi(self, engine):
        """Test cos(π) ≈ -1."""
        assert engine.cos(math.pi) == pytest.approx(-1.0)

    def test_cos_pi_over_2(self, engine):
        """Test cos(π/2) ≈ 0."""
        assert engine.cos(math.pi / 2) == pytest.approx(0.0, abs=1e-10)

    def test_cos_pi_over_3(self, engine):
        """Test cos(π/3) ≈ 0.5."""
        assert engine.cos(math.pi / 3) == pytest.approx(0.5)

    def test_cos_negative_value(self, engine):
        """Test cos of negative radian."""
        assert engine.cos(-1.0) == pytest.approx(math.cos(-1.0))

    def test_cos_large_radian(self, engine):
        """Test cos of large radian value."""
        result = engine.cos(100.0)
        assert isinstance(result, float)

    def test_cos_small_positive_float(self, engine):
        """Test cos of small positive float."""
        assert engine.cos(0.1) == pytest.approx(math.cos(0.1))

    def test_cos_integer_input(self, engine):
        """Test cos with integer input."""
        assert engine.cos(1) == pytest.approx(math.cos(1))

    def test_cos_float_input(self, engine):
        """Test cos with float input."""
        assert engine.cos(1.5) == pytest.approx(math.cos(1.5))

    def test_cos_bool_true_raises_type_error(self, engine):
        """Test cos(True) raises TypeError."""
        with pytest.raises(TypeError):
            engine.cos(True)

    def test_cos_bool_false_raises_type_error(self, engine):
        """Test cos(False) raises TypeError."""
        with pytest.raises(TypeError):
            engine.cos(False)

    def test_cos_none_raises_type_error(self, engine):
        """Test cos(None) raises TypeError."""
        with pytest.raises(TypeError):
            engine.cos(None)

    def test_cos_string_raises_type_error(self, engine):
        """Test cos(string) raises TypeError."""
        with pytest.raises(TypeError):
            engine.cos("1.0")

    def test_cos_list_raises_type_error(self, engine):
        """Test cos(list) raises TypeError."""
        with pytest.raises(TypeError):
            engine.cos([1.0])


# ============================================================================
# TEST ARITHMETIC ENGINE TAN
# ============================================================================


class TestArithmeticEngineTan:
    """Test suite for ArithmeticEngine.tan method."""

    def test_tan_zero(self, engine):
        """Test tan(0) = 0."""
        assert engine.tan(0) == pytest.approx(0.0)

    def test_tan_pi_over_4(self, engine):
        """Test tan(π/4) ≈ 1."""
        assert engine.tan(math.pi / 4) == pytest.approx(1.0)

    def test_tan_negative_value(self, engine):
        """Test tan of negative radian."""
        assert engine.tan(-1.0) == pytest.approx(math.tan(-1.0))

    def test_tan_small_positive_float(self, engine):
        """Test tan of small positive float."""
        assert engine.tan(0.1) == pytest.approx(math.tan(0.1))

    def test_tan_integer_input(self, engine):
        """Test tan with integer input."""
        assert engine.tan(1) == pytest.approx(math.tan(1))

    def test_tan_float_input(self, engine):
        """Test tan with float input."""
        assert engine.tan(0.5) == pytest.approx(math.tan(0.5))

    def test_tan_pi_over_6(self, engine):
        """Test tan(π/6) ≈ 0.577."""
        assert engine.tan(math.pi / 6) == pytest.approx(math.tan(math.pi / 6))

    def test_tan_bool_true_raises_type_error(self, engine):
        """Test tan(True) raises TypeError."""
        with pytest.raises(TypeError):
            engine.tan(True)

    def test_tan_bool_false_raises_type_error(self, engine):
        """Test tan(False) raises TypeError."""
        with pytest.raises(TypeError):
            engine.tan(False)

    def test_tan_none_raises_type_error(self, engine):
        """Test tan(None) raises TypeError."""
        with pytest.raises(TypeError):
            engine.tan(None)

    def test_tan_string_raises_type_error(self, engine):
        """Test tan(string) raises TypeError."""
        with pytest.raises(TypeError):
            engine.tan("1.0")

    def test_tan_list_raises_type_error(self, engine):
        """Test tan(list) raises TypeError."""
        with pytest.raises(TypeError):
            engine.tan([1.0])


# ============================================================================
# TEST ARITHMETIC ENGINE EXP
# ============================================================================


class TestArithmeticEngineExp:
    """Test suite for ArithmeticEngine.exp method."""

    def test_exp_zero(self, engine):
        """Test exp(0) = 1."""
        assert engine.exp(0) == pytest.approx(1.0)

    def test_exp_one(self, engine):
        """Test exp(1) ≈ e."""
        assert engine.exp(1) == pytest.approx(math.e)

    def test_exp_negative_one(self, engine):
        """Test exp(-1) ≈ 1/e."""
        assert engine.exp(-1) == pytest.approx(1 / math.e)

    def test_exp_two(self, engine):
        """Test exp(2) ≈ e^2."""
        assert engine.exp(2) == pytest.approx(math.exp(2))

    def test_exp_negative_value(self, engine):
        """Test exp of negative value."""
        assert engine.exp(-2.0) == pytest.approx(math.exp(-2.0))

    def test_exp_large_positive(self, engine):
        """Test exp of large positive value."""
        result = engine.exp(10.0)
        assert result == pytest.approx(math.exp(10.0))

    def test_exp_small_positive_float(self, engine):
        """Test exp of small positive float."""
        assert engine.exp(0.1) == pytest.approx(math.exp(0.1))

    def test_exp_integer_input(self, engine):
        """Test exp with integer input."""
        assert engine.exp(1) == pytest.approx(math.exp(1))

    def test_exp_float_input(self, engine):
        """Test exp with float input."""
        assert engine.exp(1.5) == pytest.approx(math.exp(1.5))

    def test_exp_bool_true_raises_type_error(self, engine):
        """Test exp(True) raises TypeError."""
        with pytest.raises(TypeError):
            engine.exp(True)

    def test_exp_bool_false_raises_type_error(self, engine):
        """Test exp(False) raises TypeError."""
        with pytest.raises(TypeError):
            engine.exp(False)

    def test_exp_none_raises_type_error(self, engine):
        """Test exp(None) raises TypeError."""
        with pytest.raises(TypeError):
            engine.exp(None)

    def test_exp_string_raises_type_error(self, engine):
        """Test exp(string) raises TypeError."""
        with pytest.raises(TypeError):
            engine.exp("1.0")

    def test_exp_list_raises_type_error(self, engine):
        """Test exp(list) raises TypeError."""
        with pytest.raises(TypeError):
            engine.exp([1.0])


# ============================================================================
# TEST OPERATION CLASS: SIN
# ============================================================================


class TestSinOperation:
    """Test suite for Sin operation class."""

    def test_sin_name(self):
        """Test that Sin operation has name 'sin'."""
        assert Sin().name() == "sin"

    def test_sin_operand_count(self):
        """Test that Sin has operand_count 1."""
        assert Sin().operand_count() == 1

    def test_sin_execute_zero(self):
        """Test Sin.execute(0)."""
        assert Sin().execute(0) == pytest.approx(0.0)

    def test_sin_execute_pi_over_2(self):
        """Test Sin.execute(π/2)."""
        assert Sin().execute(math.pi / 2) == pytest.approx(1.0)

    def test_sin_execute_float(self):
        """Test Sin.execute with float operand."""
        assert Sin().execute(1.5) == pytest.approx(math.sin(1.5))

    def test_sin_execute_negative(self):
        """Test Sin.execute with negative operand."""
        assert Sin().execute(-1.0) == pytest.approx(math.sin(-1.0))

    def test_sin_execute_bool_raises_type_error(self):
        """Test Sin.execute(True) raises TypeError."""
        with pytest.raises(TypeError):
            Sin().execute(True)

    def test_sin_execute_none_raises_type_error(self):
        """Test Sin.execute(None) raises TypeError."""
        with pytest.raises(TypeError):
            Sin().execute(None)

    def test_sin_execute_string_raises_type_error(self):
        """Test Sin.execute(string) raises TypeError."""
        with pytest.raises(TypeError):
            Sin().execute("1.0")


# ============================================================================
# TEST OPERATION CLASS: COS
# ============================================================================


class TestCosOperation:
    """Test suite for Cos operation class."""

    def test_cos_name(self):
        """Test that Cos operation has name 'cos'."""
        assert Cos().name() == "cos"

    def test_cos_operand_count(self):
        """Test that Cos has operand_count 1."""
        assert Cos().operand_count() == 1

    def test_cos_execute_zero(self):
        """Test Cos.execute(0)."""
        assert Cos().execute(0) == pytest.approx(1.0)

    def test_cos_execute_pi(self):
        """Test Cos.execute(π)."""
        assert Cos().execute(math.pi) == pytest.approx(-1.0)

    def test_cos_execute_float(self):
        """Test Cos.execute with float operand."""
        assert Cos().execute(1.5) == pytest.approx(math.cos(1.5))

    def test_cos_execute_negative(self):
        """Test Cos.execute with negative operand."""
        assert Cos().execute(-1.0) == pytest.approx(math.cos(-1.0))

    def test_cos_execute_bool_raises_type_error(self):
        """Test Cos.execute(True) raises TypeError."""
        with pytest.raises(TypeError):
            Cos().execute(True)

    def test_cos_execute_none_raises_type_error(self):
        """Test Cos.execute(None) raises TypeError."""
        with pytest.raises(TypeError):
            Cos().execute(None)

    def test_cos_execute_string_raises_type_error(self):
        """Test Cos.execute(string) raises TypeError."""
        with pytest.raises(TypeError):
            Cos().execute("1.0")


# ============================================================================
# TEST OPERATION CLASS: TAN
# ============================================================================


class TestTanOperation:
    """Test suite for Tan operation class."""

    def test_tan_name(self):
        """Test that Tan operation has name 'tan'."""
        assert Tan().name() == "tan"

    def test_tan_operand_count(self):
        """Test that Tan has operand_count 1."""
        assert Tan().operand_count() == 1

    def test_tan_execute_zero(self):
        """Test Tan.execute(0)."""
        assert Tan().execute(0) == pytest.approx(0.0)

    def test_tan_execute_pi_over_4(self):
        """Test Tan.execute(π/4)."""
        assert Tan().execute(math.pi / 4) == pytest.approx(1.0)

    def test_tan_execute_float(self):
        """Test Tan.execute with float operand."""
        assert Tan().execute(0.5) == pytest.approx(math.tan(0.5))

    def test_tan_execute_negative(self):
        """Test Tan.execute with negative operand."""
        assert Tan().execute(-1.0) == pytest.approx(math.tan(-1.0))

    def test_tan_execute_bool_raises_type_error(self):
        """Test Tan.execute(True) raises TypeError."""
        with pytest.raises(TypeError):
            Tan().execute(True)

    def test_tan_execute_none_raises_type_error(self):
        """Test Tan.execute(None) raises TypeError."""
        with pytest.raises(TypeError):
            Tan().execute(None)

    def test_tan_execute_string_raises_type_error(self):
        """Test Tan.execute(string) raises TypeError."""
        with pytest.raises(TypeError):
            Tan().execute("1.0")


# ============================================================================
# TEST OPERATION CLASS: EXP
# ============================================================================


class TestExpOperation:
    """Test suite for Exp operation class."""

    def test_exp_name(self):
        """Test that Exp operation has name 'exp'."""
        assert Exp().name() == "exp"

    def test_exp_operand_count(self):
        """Test that Exp has operand_count 1."""
        assert Exp().operand_count() == 1

    def test_exp_execute_zero(self):
        """Test Exp.execute(0)."""
        assert Exp().execute(0) == pytest.approx(1.0)

    def test_exp_execute_one(self):
        """Test Exp.execute(1)."""
        assert Exp().execute(1) == pytest.approx(math.e)

    def test_exp_execute_float(self):
        """Test Exp.execute with float operand."""
        assert Exp().execute(1.5) == pytest.approx(math.exp(1.5))

    def test_exp_execute_negative(self):
        """Test Exp.execute with negative operand."""
        assert Exp().execute(-1.0) == pytest.approx(math.exp(-1.0))

    def test_exp_execute_bool_raises_type_error(self):
        """Test Exp.execute(True) raises TypeError."""
        with pytest.raises(TypeError):
            Exp().execute(True)

    def test_exp_execute_none_raises_type_error(self):
        """Test Exp.execute(None) raises TypeError."""
        with pytest.raises(TypeError):
            Exp().execute(None)

    def test_exp_execute_string_raises_type_error(self):
        """Test Exp.execute(string) raises TypeError."""
        with pytest.raises(TypeError):
            Exp().execute("1.0")


# ============================================================================
# TEST REGISTER_SCIENTIFIC_OPERATIONS
# ============================================================================


class TestRegisterScientificOperations:
    """Test suite for register_scientific_operations function."""

    def test_register_scientific_operations_adds_sin(self, registry):
        """Test that register_scientific_operations registers sin."""
        register_scientific_operations(registry)
        assert "sin" in registry.list_operations()

    def test_register_scientific_operations_adds_cos(self, registry):
        """Test that register_scientific_operations registers cos."""
        register_scientific_operations(registry)
        assert "cos" in registry.list_operations()

    def test_register_scientific_operations_adds_tan(self, registry):
        """Test that register_scientific_operations registers tan."""
        register_scientific_operations(registry)
        assert "tan" in registry.list_operations()

    def test_register_scientific_operations_adds_exp(self, registry):
        """Test that register_scientific_operations registers exp."""
        register_scientific_operations(registry)
        assert "exp" in registry.list_operations()

    def test_register_scientific_operations_adds_four_operations(self, registry):
        """Test that register_scientific_operations adds exactly 4 operations."""
        assert len(registry.list_operations()) == 0
        register_scientific_operations(registry)
        assert len(registry.list_operations()) == 4

    def test_register_scientific_operations_sin_is_executable(self, registry):
        """Test that registered sin operation can be executed."""
        register_scientific_operations(registry)
        sin_op = registry.get("sin")
        assert sin_op is not None
        assert sin_op.execute(math.pi / 2) == pytest.approx(1.0)

    def test_register_scientific_operations_cos_is_executable(self, registry):
        """Test that registered cos operation can be executed."""
        register_scientific_operations(registry)
        cos_op = registry.get("cos")
        assert cos_op is not None
        assert cos_op.execute(0) == pytest.approx(1.0)

    def test_register_scientific_operations_tan_is_executable(self, registry):
        """Test that registered tan operation can be executed."""
        register_scientific_operations(registry)
        tan_op = registry.get("tan")
        assert tan_op is not None
        assert tan_op.execute(math.pi / 4) == pytest.approx(1.0)

    def test_register_scientific_operations_exp_is_executable(self, registry):
        """Test that registered exp operation can be executed."""
        register_scientific_operations(registry)
        exp_op = registry.get("exp")
        assert exp_op is not None
        assert exp_op.execute(0) == pytest.approx(1.0)

    def test_register_scientific_operations_all_have_correct_operand_count(self, registry):
        """Test that all registered scientific operations have operand_count 1."""
        register_scientific_operations(registry)
        for name in ["sin", "cos", "tan", "exp"]:
            op = registry.get(name)
            assert op.operand_count() == 1

    def test_register_scientific_operations_multiple_calls(self, registry):
        """Test that calling register_scientific_operations twice works correctly."""
        register_scientific_operations(registry)
        first_list = set(registry.list_operations())

        register_scientific_operations(registry)
        second_list = set(registry.list_operations())

        # Both calls should result in all 4 operations being present
        assert len(first_list) == 4
        assert len(second_list) == 4
