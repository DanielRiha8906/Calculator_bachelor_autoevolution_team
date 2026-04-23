"""Tests for src.core.mode_abstraction module.

Tests the mode abstraction layer including BaseCalculatorMode, NormalMode,
ScientificMode, and the get_mode_instance factory function.
"""

import pytest
from src.core.mode_abstraction import (
    BaseCalculatorMode,
    NormalMode,
    ScientificMode,
    get_mode_instance,
)
from src.mode import NORMAL_MODE_OPERATIONS, SCIENTIFIC_MODE_OPERATIONS


class TestNormalMode:
    """Test suite for NormalMode class."""

    def test_get_name_returns_normal(self):
        """Test NormalMode.get_name() returns 'normal'."""
        mode = NormalMode()
        assert mode.get_name() == "normal"

    def test_get_operations_returns_list(self):
        """Test NormalMode.get_operations() returns a list."""
        mode = NormalMode()
        ops = mode.get_operations()
        assert isinstance(ops, list)
        assert len(ops) > 0

    def test_get_operations_matches_constant(self):
        """Test NormalMode.get_operations() matches NORMAL_MODE_OPERATIONS."""
        mode = NormalMode()
        ops = mode.get_operations()
        assert ops == list(NORMAL_MODE_OPERATIONS)

    def test_get_operations_returns_copy(self):
        """Test NormalMode.get_operations() returns a copy, not the original."""
        mode = NormalMode()
        ops1 = mode.get_operations()
        ops2 = mode.get_operations()
        # Should be equal but not the same object
        assert ops1 == ops2
        assert ops1 is not ops2

    def test_get_operation_arity_binary(self):
        """Test get_operation_arity for binary operations like 'add'."""
        mode = NormalMode()
        assert mode.get_operation_arity("add") == 2
        assert mode.get_operation_arity("multiply") == 2
        assert mode.get_operation_arity("divide") == 2

    def test_get_operation_arity_unary(self):
        """Test get_operation_arity for unary operations like 'square'."""
        mode = NormalMode()
        assert mode.get_operation_arity("square") == 1
        assert mode.get_operation_arity("square_root") == 1


class TestScientificMode:
    """Test suite for ScientificMode class."""

    def test_get_name_returns_scientific(self):
        """Test ScientificMode.get_name() returns 'scientific'."""
        mode = ScientificMode()
        assert mode.get_name() == "scientific"

    def test_get_operations_returns_list(self):
        """Test ScientificMode.get_operations() returns a list."""
        mode = ScientificMode()
        ops = mode.get_operations()
        assert isinstance(ops, list)
        assert len(ops) > 0

    def test_get_operations_matches_constant(self):
        """Test ScientificMode.get_operations() matches SCIENTIFIC_MODE_OPERATIONS."""
        mode = ScientificMode()
        ops = mode.get_operations()
        assert ops == list(SCIENTIFIC_MODE_OPERATIONS)

    def test_get_operations_is_superset_of_normal(self):
        """Test ScientificMode operations include all Normal mode operations."""
        normal_mode = NormalMode()
        scientific_mode = ScientificMode()
        normal_ops = set(normal_mode.get_operations())
        scientific_ops = set(scientific_mode.get_operations())
        assert normal_ops.issubset(scientific_ops)

    def test_get_operations_has_extra_operations(self):
        """Test ScientificMode has additional operations beyond Normal."""
        normal_mode = NormalMode()
        scientific_mode = ScientificMode()
        normal_ops = set(normal_mode.get_operations())
        scientific_ops = set(scientific_mode.get_operations())
        assert len(scientific_ops) > len(normal_ops)

    def test_get_operation_arity_binary(self):
        """Test get_operation_arity for binary operations."""
        mode = ScientificMode()
        assert mode.get_operation_arity("power") == 2
        assert mode.get_operation_arity("divide") == 2

    def test_get_operation_arity_unary(self):
        """Test get_operation_arity for unary operations in scientific mode."""
        mode = ScientificMode()
        assert mode.get_operation_arity("sin") == 1
        assert mode.get_operation_arity("cos") == 1
        assert mode.get_operation_arity("tan") == 1
        assert mode.get_operation_arity("factorial") == 1
        assert mode.get_operation_arity("cube") == 1
        assert mode.get_operation_arity("cube_root") == 1


class TestGetModeInstance:
    """Test suite for get_mode_instance factory function."""

    def test_get_mode_instance_normal_lowercase(self):
        """Test get_mode_instance('normal') returns NormalMode instance."""
        mode = get_mode_instance("normal")
        assert isinstance(mode, NormalMode)
        assert mode.get_name() == "normal"

    def test_get_mode_instance_scientific_lowercase(self):
        """Test get_mode_instance('scientific') returns ScientificMode instance."""
        mode = get_mode_instance("scientific")
        assert isinstance(mode, ScientificMode)
        assert mode.get_name() == "scientific"

    def test_get_mode_instance_normal_uppercase(self):
        """Test get_mode_instance is case-insensitive for 'NORMAL'."""
        mode = get_mode_instance("NORMAL")
        assert isinstance(mode, NormalMode)
        assert mode.get_name() == "normal"

    def test_get_mode_instance_scientific_uppercase(self):
        """Test get_mode_instance is case-insensitive for 'SCIENTIFIC'."""
        mode = get_mode_instance("SCIENTIFIC")
        assert isinstance(mode, ScientificMode)
        assert mode.get_name() == "scientific"

    def test_get_mode_instance_mixed_case(self):
        """Test get_mode_instance handles mixed case like 'NorMal'."""
        mode = get_mode_instance("NorMal")
        assert isinstance(mode, NormalMode)

    def test_get_mode_instance_unknown_raises_value_error(self):
        """Test get_mode_instance raises ValueError for unknown mode."""
        with pytest.raises(ValueError) as exc_info:
            get_mode_instance("unknown")
        assert "Unknown calculator mode" in str(exc_info.value)

    def test_get_mode_instance_empty_string_raises_value_error(self):
        """Test get_mode_instance raises ValueError for empty string."""
        with pytest.raises(ValueError):
            get_mode_instance("")

    def test_get_mode_instance_none_raises_attribute_error(self):
        """Test get_mode_instance raises error when passed None."""
        with pytest.raises(AttributeError):
            get_mode_instance(None)  # type: ignore[arg-type]

    def test_get_mode_instance_numeric_string_raises_value_error(self):
        """Test get_mode_instance raises ValueError for numeric string."""
        with pytest.raises(ValueError):
            get_mode_instance("123")

    def test_get_mode_instance_returns_instance_with_valid_operations(self):
        """Test get_mode_instance returns mode with valid operation lists."""
        mode = get_mode_instance("normal")
        ops = mode.get_operations()
        assert "add" in ops
        assert "subtract" in ops

    def test_get_mode_instance_scientific_has_sin(self):
        """Test ScientificMode obtained via factory has sin operation."""
        mode = get_mode_instance("scientific")
        ops = mode.get_operations()
        assert "sin" in ops


class TestBaseCalculatorModeInterface:
    """Test suite for BaseCalculatorMode abstract interface."""

    def test_base_calculator_mode_is_abstract(self):
        """Test BaseCalculatorMode cannot be instantiated directly."""
        # BaseCalculatorMode is abstract and requires implementing get_name and get_operations
        with pytest.raises(TypeError):
            BaseCalculatorMode()  # type: ignore[abstract]

    def test_get_operation_arity_with_unary_operations(self):
        """Test get_operation_arity returns 1 for all unary operations."""
        mode = ScientificMode()
        unary_ops = [
            "square",
            "square_root",
            "cube",
            "cube_root",
            "factorial",
            "logarithm",
            "natural_logarithm",
            "sin",
            "cos",
            "tan",
            "cot",
            "asin",
            "acos",
        ]
        for op in unary_ops:
            assert mode.get_operation_arity(op) == 1, f"Expected {op} to be unary"

    def test_get_operation_arity_with_binary_operations(self):
        """Test get_operation_arity returns 2 for binary operations."""
        mode = ScientificMode()
        binary_ops = ["add", "subtract", "multiply", "divide", "power"]
        for op in binary_ops:
            assert mode.get_operation_arity(op) == 2, f"Expected {op} to be binary"

    def test_get_operation_arity_defaults_to_binary_for_unknown(self):
        """Test get_operation_arity defaults to 2 for unknown operations."""
        mode = NormalMode()
        # Unknown operations should default to binary (2)
        assert mode.get_operation_arity("unknown_op") == 2
