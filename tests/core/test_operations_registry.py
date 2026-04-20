"""Tests for Operation and OperationRegistry from src.core.operations."""

import math
import pytest
from src.core.operations import Operation, OperationRegistry, _CATALOG
from src.calculator import Calculator


class TestOperationDataclass:
    """Test the Operation dataclass."""

    def test_operation_creation(self):
        """Test creating an Operation instance."""
        op = Operation("add", 2, "Addition", ("+",))
        assert op.name == "add"
        assert op.arity == 2
        assert op.display_name == "Addition"
        assert op.aliases == ("+",)

    def test_operation_frozen(self):
        """Test that Operation is frozen (immutable)."""
        op = Operation("add", 2, "Addition", ("+",))
        with pytest.raises(AttributeError):
            op.name = "subtract"

    def test_operation_with_no_aliases(self):
        """Test creating an Operation with no aliases."""
        op = Operation("factorial", 1, "Factorial")
        assert op.aliases == ()

    def test_operation_equality(self):
        """Test that two Operations with same data are equal."""
        op1 = Operation("add", 2, "Addition", ("+",))
        op2 = Operation("add", 2, "Addition", ("+",))
        assert op1 == op2

    def test_operation_inequality(self):
        """Test that Operations with different data are not equal."""
        op1 = Operation("add", 2, "Addition", ("+",))
        op2 = Operation("subtract", 2, "Subtraction", ("-",))
        assert op1 != op2


class TestOperationRegistryInitialization:
    """Test OperationRegistry initialization and metadata access."""

    def test_registry_creation(self):
        """Test creating a registry with a calculator."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        assert registry.calculator is calc

    def test_registry_catalog_copy(self):
        """Test that registry creates its own copy of catalog."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        ops = registry.get_operations()
        # Modifying returned list shouldn't affect registry
        ops.pop()
        # In default normal mode, only 12 operations are visible (the ones with mode="both")
        assert len(registry.get_operations()) == 12

    def test_registry_lookup_initialized(self):
        """Test that registry lookup table is properly initialized."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        # Check that operations by name are in lookup
        assert registry.get_operation("add") is not None
        assert registry.get_operation("subtract") is not None

    def test_registry_aliases_in_lookup(self):
        """Test that aliases are properly indexed in lookup."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        # "+" should resolve to the add operation
        assert registry.get_operation("+") is not None
        # Alias should resolve to same operation as name
        add_op = registry.get_operation("add")
        plus_op = registry.get_operation("+")
        assert add_op == plus_op


class TestOperationRegistryGetOperations:
    """Test OperationRegistry.get_operations method."""

    def test_get_operations_returns_list(self):
        """Test that get_operations returns a list."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        ops = registry.get_operations()
        assert isinstance(ops, list)

    def test_get_operations_count(self):
        """Test that get_operations returns all operations visible in current mode."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        ops = registry.get_operations()
        # In default normal mode, only 12 operations are visible (the ones with mode="both")
        assert len(ops) == 12

    def test_get_operations_preserves_order(self):
        """Test that get_operations preserves catalog order."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        ops = registry.get_operations()
        for i, op in enumerate(ops):
            assert op == _CATALOG[i]

    def test_get_operations_contains_all_expected(self):
        """Test that all expected operations are present in normal mode."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        ops = registry.get_operations()
        names = {op.name for op in ops}
        # In normal mode, only the "both" mode operations are visible
        expected = {
            "add",
            "subtract",
            "multiply",
            "divide",
            "power",
            "logarithm",
            "factorial",
            "square",
            "cube",
            "square_root",
            "cube_root",
            "natural_logarithm",
        }
        assert expected == names


class TestOperationRegistryGetOperation:
    """Test OperationRegistry.get_operation method."""

    def test_get_operation_by_name(self):
        """Test retrieving operation by canonical name."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        op = registry.get_operation("add")
        assert op is not None
        assert op.name == "add"

    def test_get_operation_by_alias(self):
        """Test retrieving operation by alias."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        op = registry.get_operation("+")
        assert op is not None
        assert op.name == "add"

    def test_get_operation_unknown_returns_none(self):
        """Test that unknown operation returns None."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        op = registry.get_operation("unknown_op")
        assert op is None

    def test_get_operation_all_names(self):
        """Test retrieving all operations by name."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        for catalog_op in _CATALOG:
            op = registry.get_operation(catalog_op.name)
            assert op == catalog_op

    def test_get_operation_all_aliases(self):
        """Test retrieving all operations by alias."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        for catalog_op in _CATALOG:
            for alias in catalog_op.aliases:
                op = registry.get_operation(alias)
                assert op == catalog_op

    def test_get_operation_empty_string(self):
        """Test that empty string returns None."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        op = registry.get_operation("")
        assert op is None


class TestOperationRegistryResolve:
    """Test OperationRegistry.resolve method."""

    def test_resolve_by_name(self):
        """Test resolving operation by canonical name."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        assert registry.resolve("add") == "add"

    def test_resolve_by_alias(self):
        """Test resolving operation by alias."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        assert registry.resolve("+") == "add"

    def test_resolve_unknown_raises_error(self):
        """Test that unknown operation raises ValueError."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        with pytest.raises(ValueError, match="Unknown operation"):
            registry.resolve("unknown_op")

    def test_resolve_empty_string_raises_error(self):
        """Test that empty string raises ValueError."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        with pytest.raises(ValueError):
            registry.resolve("")

    def test_resolve_case_sensitive(self):
        """Test that resolve is case-sensitive."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        with pytest.raises(ValueError):
            registry.resolve("ADD")

    @pytest.mark.parametrize("token", ["add", "subtract", "multiply", "divide"])
    def test_resolve_basic_operations(self, token):
        """Test resolving basic operations."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        assert registry.resolve(token) == token


class TestOperationRegistryArity:
    """Test OperationRegistry.arity method."""

    def test_arity_binary_operations(self):
        """Test arity of binary operations."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        assert registry.arity("add") == 2
        assert registry.arity("subtract") == 2
        assert registry.arity("multiply") == 2
        assert registry.arity("divide") == 2
        assert registry.arity("power") == 2
        assert registry.arity("logarithm") == 2

    def test_arity_unary_operations(self):
        """Test arity of unary operations."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        assert registry.arity("factorial") == 1
        assert registry.arity("square") == 1
        assert registry.arity("cube") == 1
        assert registry.arity("square_root") == 1
        assert registry.arity("cube_root") == 1
        assert registry.arity("natural_logarithm") == 1

    def test_arity_by_alias(self):
        """Test arity lookup by alias."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        assert registry.arity("+") == 2
        assert registry.arity("sqrt") == 1
        assert registry.arity("log") == 2

    def test_arity_unknown_raises_error(self):
        """Test that unknown operation raises ValueError."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        with pytest.raises(ValueError, match="Unknown operation"):
            registry.arity("unknown_op")


class TestOperationRegistryGetOperationMapping:
    """Test OperationRegistry.get_operation_mapping method."""

    def test_get_operation_mapping_returns_dict(self):
        """Test that get_operation_mapping returns a dict."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        mapping = registry.get_operation_mapping()
        assert isinstance(mapping, dict)

    def test_get_operation_mapping_all_names_present(self):
        """Test that all operation names visible in current mode are in mapping."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        mapping = registry.get_operation_mapping()
        # Only operations visible in normal mode should be in mapping
        for op in _CATALOG:
            if op.mode == "both" or op.mode == "normal":
                assert op.name in mapping
                assert mapping[op.name] == op.name

    def test_get_operation_mapping_all_aliases_present(self):
        """Test that all aliases are in mapping."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        mapping = registry.get_operation_mapping()
        for op in _CATALOG:
            for alias in op.aliases:
                assert alias in mapping
                assert mapping[alias] == op.name

    def test_get_operation_mapping_values_are_canonical_names(self):
        """Test that all mapping values are canonical operation names."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        mapping = registry.get_operation_mapping()
        valid_names = {op.name for op in _CATALOG}
        for value in mapping.values():
            assert value in valid_names


class TestOperationRegistryDispatch:
    """Test OperationRegistry.dispatch method."""

    def test_dispatch_add(self):
        """Test dispatching add operation."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("add", [2, 3])
        assert result == 5

    def test_dispatch_subtract(self):
        """Test dispatching subtract operation."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("subtract", [5, 3])
        assert result == 2

    def test_dispatch_multiply(self):
        """Test dispatching multiply operation."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("multiply", [3, 4])
        assert result == 12

    def test_dispatch_divide(self):
        """Test dispatching divide operation."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("divide", [6, 2])
        assert result == 3.0

    def test_dispatch_divide_by_zero_raises_error(self):
        """Test that dispatching divide by zero raises ZeroDivisionError."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        with pytest.raises(ZeroDivisionError):
            registry.dispatch("divide", [5, 0])

    def test_dispatch_logarithm_basic10(self):
        """Test dispatching logarithm (base 10)."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("logarithm", [100, 10])
        assert result == pytest.approx(2.0)

    def test_dispatch_logarithm_base2(self):
        """Test dispatching logarithm with base 2."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("logarithm", [8, 2])
        assert result == pytest.approx(3.0)

    def test_dispatch_logarithm_base_e(self):
        """Test dispatching logarithm with base e."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("logarithm", [math.e, math.e])
        assert result == pytest.approx(1.0)

    def test_dispatch_logarithm_zero_raises_error(self):
        """Test that log(0, base) raises ValueError."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        with pytest.raises(ValueError, match="not defined for non-positive values"):
            registry.dispatch("logarithm", [0, 10])

    def test_dispatch_logarithm_negative_raises_error(self):
        """Test that log(negative, base) raises ValueError."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        with pytest.raises(ValueError, match="not defined for non-positive values"):
            registry.dispatch("logarithm", [-5, 10])

    def test_dispatch_logarithm_invalid_base_zero(self):
        """Test that log(x, 0) raises ValueError."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        with pytest.raises(ValueError, match="base must be positive"):
            registry.dispatch("logarithm", [5, 0])

    def test_dispatch_logarithm_invalid_base_negative(self):
        """Test that log(x, negative) raises ValueError."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        with pytest.raises(ValueError, match="base must be positive"):
            registry.dispatch("logarithm", [5, -2])

    def test_dispatch_logarithm_invalid_base_one(self):
        """Test that log(x, 1) raises ValueError."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        with pytest.raises(ValueError, match="base must be positive and not equal to 1"):
            registry.dispatch("logarithm", [5, 1])

    def test_dispatch_power(self):
        """Test dispatching power operation."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("power", [2, 3])
        assert result == 8

    def test_dispatch_factorial(self):
        """Test dispatching factorial operation."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("factorial", [5])
        assert result == 120

    def test_dispatch_square(self):
        """Test dispatching square operation."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("square", [5])
        assert result == 25

    def test_dispatch_cube(self):
        """Test dispatching cube operation."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("cube", [3])
        assert result == 27

    def test_dispatch_square_root(self):
        """Test dispatching square_root operation."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("square_root", [16])
        assert result == 4.0

    def test_dispatch_cube_root(self):
        """Test dispatching cube_root operation."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("cube_root", [8])
        assert result == pytest.approx(2.0)

    def test_dispatch_natural_logarithm(self):
        """Test dispatching natural_logarithm operation."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("natural_logarithm", [math.e])
        assert result == pytest.approx(1.0)

    def test_dispatch_with_negative_operands(self):
        """Test dispatch with negative operands."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("add", [-5, -3])
        assert result == -8

    def test_dispatch_with_float_operands(self):
        """Test dispatch with float operands."""
        calc = Calculator()
        registry = OperationRegistry(calc)
        result = registry.dispatch("multiply", [2.5, 4.0])
        assert result == 10.0
