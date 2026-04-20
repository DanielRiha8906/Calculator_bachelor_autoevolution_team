"""Tests for mode-aware operation filtering in OperationRegistry.

Tests cover:
- get_operations() filtering by mode
- resolve() mode-aware validation
- arity() mode-aware validation
- get_operation_mapping() filtering by mode
- set_mode() for registry
- Trigonometric operations (sin, cos, tan) visibility
- All "both" mode operations always visible
- Normal vs scientific mode filtering
"""

import pytest
import math
from src.core.operations import Operation, OperationRegistry, _CATALOG
from src.calculator import Calculator


@pytest.fixture
def calc():
    """Provide a Calculator instance."""
    return Calculator()


@pytest.fixture
def registry(calc):
    """Provide an OperationRegistry instance."""
    return OperationRegistry(calc)


class TestOperationRegistrySetMode:
    """Test OperationRegistry.set_mode() method."""

    def test_set_mode_normal(self, registry):
        """Verify set_mode('normal') works."""
        registry.set_mode("normal")
        assert registry._current_mode == "normal"

    def test_set_mode_scientific(self, registry):
        """Verify set_mode('scientific') works."""
        registry.set_mode("scientific")
        assert registry._current_mode == "scientific"

    def test_set_mode_invalid_raises_error(self, registry):
        """Verify set_mode with invalid mode raises ValueError."""
        with pytest.raises(ValueError, match="Invalid mode"):
            registry.set_mode("invalid_mode")

    def test_set_mode_uppercase_invalid(self, registry):
        """Verify set_mode('NORMAL') raises ValueError."""
        with pytest.raises(ValueError, match="Invalid mode"):
            registry.set_mode("NORMAL")

    def test_set_mode_preserves_calculator(self, registry, calc):
        """Verify set_mode doesn't affect calculator reference."""
        registry.set_mode("scientific")
        assert registry.calculator is calc


class TestGetOperationsFiltering:
    """Test OperationRegistry.get_operations() with mode filtering."""

    def test_get_operations_normal_mode_count(self, registry):
        """Verify normal mode returns correct count of operations."""
        registry.set_mode("normal")
        ops = registry.get_operations()
        # Normal mode should have 12 base operations (no trig)
        assert len(ops) == 12

    def test_get_operations_scientific_mode_count(self, registry):
        """Verify scientific mode returns correct count of operations."""
        registry.set_mode("scientific")
        ops = registry.get_operations()
        # Scientific mode should have 12 base + 3 trig = 15 operations
        assert len(ops) == 15

    def test_get_operations_normal_no_trig(self, registry):
        """Verify normal mode does not include sin, cos, tan."""
        registry.set_mode("normal")
        ops = registry.get_operations()
        names = {op.name for op in ops}
        assert "sin" not in names
        assert "cos" not in names
        assert "tan" not in names

    def test_get_operations_scientific_includes_trig(self, registry):
        """Verify scientific mode includes sin, cos, tan."""
        registry.set_mode("scientific")
        ops = registry.get_operations()
        names = {op.name for op in ops}
        assert "sin" in names
        assert "cos" in names
        assert "tan" in names

    def test_get_operations_normal_includes_basic(self, registry):
        """Verify normal mode includes basic operations."""
        registry.set_mode("normal")
        ops = registry.get_operations()
        names = {op.name for op in ops}
        expected = {"add", "subtract", "multiply", "divide", "power", "factorial",
                    "square", "cube", "square_root", "cube_root", "logarithm",
                    "natural_logarithm"}
        assert expected == names

    def test_get_operations_preserves_order(self, registry):
        """Verify get_operations() preserves catalog order."""
        registry.set_mode("normal")
        ops = registry.get_operations()
        for i, op in enumerate(ops):
            # Find this operation in catalog
            catalog_op = next((o for o in _CATALOG if o.name == op.name), None)
            assert catalog_op is not None
            # Should match catalog position
            catalog_idx = _CATALOG.index(catalog_op)
            assert catalog_idx < i or i == _CATALOG.index(op)

    def test_get_operations_normal_then_scientific(self, registry):
        """Verify switching mode changes get_operations() results."""
        registry.set_mode("normal")
        normal_ops = registry.get_operations()
        normal_count = len(normal_ops)
        registry.set_mode("scientific")
        scientific_ops = registry.get_operations()
        scientific_count = len(scientific_ops)
        assert scientific_count == normal_count + 3


class TestResolveWithModeFiltering:
    """Test OperationRegistry.resolve() with mode awareness."""

    def test_resolve_basic_operation_in_normal(self, registry):
        """Verify resolve() works for basic operations in normal mode."""
        registry.set_mode("normal")
        result = registry.resolve("add")
        assert result == "add"

    def test_resolve_basic_operation_in_scientific(self, registry):
        """Verify resolve() works for basic operations in scientific mode."""
        registry.set_mode("scientific")
        result = registry.resolve("add")
        assert result == "add"

    def test_resolve_sin_in_normal_raises_error(self, registry):
        """Verify resolve('sin') raises ValueError in normal mode."""
        registry.set_mode("normal")
        with pytest.raises(ValueError, match="not available in.*mode"):
            registry.resolve("sin")

    def test_resolve_cos_in_normal_raises_error(self, registry):
        """Verify resolve('cos') raises ValueError in normal mode."""
        registry.set_mode("normal")
        with pytest.raises(ValueError, match="not available in.*mode"):
            registry.resolve("cos")

    def test_resolve_tan_in_normal_raises_error(self, registry):
        """Verify resolve('tan') raises ValueError in normal mode."""
        registry.set_mode("normal")
        with pytest.raises(ValueError, match="not available in.*mode"):
            registry.resolve("tan")

    def test_resolve_sin_in_scientific_succeeds(self, registry):
        """Verify resolve('sin') works in scientific mode."""
        registry.set_mode("scientific")
        result = registry.resolve("sin")
        assert result == "sin"

    def test_resolve_cos_in_scientific_succeeds(self, registry):
        """Verify resolve('cos') works in scientific mode."""
        registry.set_mode("scientific")
        result = registry.resolve("cos")
        assert result == "cos"

    def test_resolve_tan_in_scientific_succeeds(self, registry):
        """Verify resolve('tan') works in scientific mode."""
        registry.set_mode("scientific")
        result = registry.resolve("tan")
        assert result == "tan"

    def test_resolve_unknown_operation_raises_error(self, registry):
        """Verify resolve() raises ValueError for unknown operation."""
        registry.set_mode("normal")
        with pytest.raises(ValueError, match="Unknown operation"):
            registry.resolve("unknown")

    def test_resolve_alias_in_normal(self, registry):
        """Verify resolve() works for aliases in normal mode."""
        registry.set_mode("normal")
        result = registry.resolve("+")
        assert result == "add"

    def test_resolve_alias_in_scientific(self, registry):
        """Verify resolve() works for aliases in scientific mode."""
        registry.set_mode("scientific")
        result = registry.resolve("sqrt")
        assert result == "square_root"


class TestArityWithModeFiltering:
    """Test OperationRegistry.arity() with mode awareness."""

    def test_arity_basic_operation_in_normal(self, registry):
        """Verify arity() works for basic operations in normal mode."""
        registry.set_mode("normal")
        result = registry.arity("add")
        assert result == 2

    def test_arity_sin_in_scientific(self, registry):
        """Verify arity('sin') returns 1 in scientific mode."""
        registry.set_mode("scientific")
        result = registry.arity("sin")
        assert result == 1

    def test_arity_cos_in_scientific(self, registry):
        """Verify arity('cos') returns 1 in scientific mode."""
        registry.set_mode("scientific")
        result = registry.arity("cos")
        assert result == 1

    def test_arity_tan_in_scientific(self, registry):
        """Verify arity('tan') returns 1 in scientific mode."""
        registry.set_mode("scientific")
        result = registry.arity("tan")
        assert result == 1

    def test_arity_sin_in_normal_raises_error(self, registry):
        """Verify arity('sin') raises ValueError in normal mode."""
        registry.set_mode("normal")
        with pytest.raises(ValueError, match="not available in.*mode"):
            registry.arity("sin")

    def test_arity_unknown_operation_raises_error(self, registry):
        """Verify arity() raises ValueError for unknown operation."""
        registry.set_mode("normal")
        with pytest.raises(ValueError, match="Unknown operation"):
            registry.arity("unknown")

    def test_arity_by_alias_in_normal(self, registry):
        """Verify arity() works for aliases in normal mode."""
        registry.set_mode("normal")
        result = registry.arity("sqrt")
        assert result == 1


class TestGetOperationMappingFiltering:
    """Test OperationRegistry.get_operation_mapping() with mode filtering."""

    def test_get_operation_mapping_normal_excludes_trig(self, registry):
        """Verify get_operation_mapping in normal mode excludes trig."""
        registry.set_mode("normal")
        mapping = registry.get_operation_mapping()
        assert "sin" not in mapping
        assert "cos" not in mapping
        assert "tan" not in mapping

    def test_get_operation_mapping_scientific_includes_trig(self, registry):
        """Verify get_operation_mapping in scientific mode includes trig."""
        registry.set_mode("scientific")
        mapping = registry.get_operation_mapping()
        assert "sin" in mapping
        assert "cos" in mapping
        assert "tan" in mapping

    def test_get_operation_mapping_normal_includes_basic(self, registry):
        """Verify get_operation_mapping in normal mode includes basic ops."""
        registry.set_mode("normal")
        mapping = registry.get_operation_mapping()
        assert "add" in mapping
        assert "subtract" in mapping
        assert "multiply" in mapping
        assert "divide" in mapping

    def test_get_operation_mapping_includes_aliases(self, registry):
        """Verify get_operation_mapping includes aliases."""
        registry.set_mode("normal")
        mapping = registry.get_operation_mapping()
        # "+" should map to "add"
        assert "+" in mapping
        assert mapping["+"] == "add"

    def test_get_operation_mapping_count_normal(self, registry):
        """Verify get_operation_mapping count in normal mode."""
        registry.set_mode("normal")
        mapping = registry.get_operation_mapping()
        # 12 operations, but some have aliases
        # add(+), subtract(-), multiply(*), divide(/), power(^),
        # logarithm(log), square_root(sqrt), cube_root(cbrt), natural_logarithm(ln)
        # = 9 aliases + 12 names = 21
        assert len(mapping) == 21

    def test_get_operation_mapping_count_scientific(self, registry):
        """Verify get_operation_mapping count in scientific mode."""
        registry.set_mode("scientific")
        mapping = registry.get_operation_mapping()
        # 15 operations: 12 base + 3 trig
        # 9 aliases + 15 names = 24
        assert len(mapping) == 24


class TestTrigonometricOperationFiltering:
    """Test that trigonometric operations are properly filtered."""

    def test_sin_operation_has_scientific_mode(self):
        """Verify sin operation has mode='scientific'."""
        sin_op = next((op for op in _CATALOG if op.name == "sin"), None)
        assert sin_op is not None
        assert sin_op.mode == "scientific"

    def test_cos_operation_has_scientific_mode(self):
        """Verify cos operation has mode='scientific'."""
        cos_op = next((op for op in _CATALOG if op.name == "cos"), None)
        assert cos_op is not None
        assert cos_op.mode == "scientific"

    def test_tan_operation_has_scientific_mode(self):
        """Verify tan operation has mode='scientific'."""
        tan_op = next((op for op in _CATALOG if op.name == "tan"), None)
        assert tan_op is not None
        assert tan_op.mode == "scientific"

    def test_all_base_operations_have_both_mode(self):
        """Verify all basic operations have mode='both'."""
        base_ops = ["add", "subtract", "multiply", "divide", "power", "factorial",
                    "square", "cube", "square_root", "cube_root", "logarithm",
                    "natural_logarithm"]
        for op_name in base_ops:
            op = next((op for op in _CATALOG if op.name == op_name), None)
            assert op is not None
            assert op.mode == "both", f"{op_name} should have mode='both'"

    def test_only_trig_have_scientific_mode(self):
        """Verify only trigonometric operations have mode='scientific'."""
        scientific_ops = [op for op in _CATALOG if op.mode == "scientific"]
        scientific_names = {op.name for op in scientific_ops}
        assert scientific_names == {"sin", "cos", "tan"}


class TestModeFilteringConsistency:
    """Test consistency of mode filtering across all methods."""

    def test_get_operations_resolve_consistency(self, registry):
        """Verify resolve() works for all operations in get_operations()."""
        for mode in ["normal", "scientific"]:
            registry.set_mode(mode)
            ops = registry.get_operations()
            for op in ops:
                # resolve should work for operation name
                resolved = registry.resolve(op.name)
                assert resolved == op.name

    def test_get_operations_arity_consistency(self, registry):
        """Verify arity() works for all operations in get_operations()."""
        for mode in ["normal", "scientific"]:
            registry.set_mode(mode)
            ops = registry.get_operations()
            for op in ops:
                # arity should work for operation name
                arity = registry.arity(op.name)
                assert arity == op.arity

    def test_get_operation_mapping_completeness(self, registry):
        """Verify get_operation_mapping includes all operations and aliases."""
        for mode in ["normal", "scientific"]:
            registry.set_mode(mode)
            mapping = registry.get_operation_mapping()
            ops = registry.get_operations()
            # Every operation name should be in mapping
            for op in ops:
                assert op.name in mapping
                # Every alias should be in mapping
                for alias in op.aliases:
                    assert alias in mapping

    def test_mode_switch_consistency(self, registry):
        """Verify operations are consistent after mode switches."""
        registry.set_mode("normal")
        normal_ops = {op.name for op in registry.get_operations()}
        registry.set_mode("scientific")
        scientific_ops = {op.name for op in registry.get_operations()}
        # Normal operations should be subset of scientific
        assert normal_ops.issubset(scientific_ops)
        # Scientific should have 3 more
        assert len(scientific_ops) - len(normal_ops) == 3


class TestDispatchWithModeFiltering:
    """Test that dispatch respects mode filtering indirectly."""

    def test_dispatch_sin_in_scientific(self, registry):
        """Verify dispatch('sin', [π/2]) works in scientific mode."""
        registry.set_mode("scientific")
        result = registry.dispatch("sin", [math.pi / 2])
        assert abs(result - 1.0) < 1e-10

    def test_dispatch_cos_in_scientific(self, registry):
        """Verify dispatch('cos', [0]) works in scientific mode."""
        registry.set_mode("scientific")
        result = registry.dispatch("cos", [0])
        assert abs(result - 1.0) < 1e-10

    def test_dispatch_tan_in_scientific(self, registry):
        """Verify dispatch('tan', [π/4]) works in scientific mode."""
        registry.set_mode("scientific")
        result = registry.dispatch("tan", [math.pi / 4])
        assert abs(result - 1.0) < 1e-10
