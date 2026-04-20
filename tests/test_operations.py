"""Comprehensive pytest tests for the OperationRegistry.

Tests cover:
- Operation frozen dataclass: creation, immutability
- OperationRegistry metadata methods: get_operations(), get_operation(), resolve(), arity(), get_operation_mapping()
- OperationRegistry.dispatch(): all operations, special logarithm handling, error handling
- Edge cases: unknown tokens, invalid domains, special numbers
- Integration with Calculator instance
"""

import pytest
import math
from unittest.mock import Mock, MagicMock

from src.operations import Operation, OperationRegistry, _CATALOG
from src.calculator import Calculator


# ==============================================================================
# FIXTURES
# ==============================================================================

@pytest.fixture
def calculator():
    """Provide a real Calculator instance."""
    return Calculator()


@pytest.fixture
def registry(calculator):
    """Provide an OperationRegistry instance with a real Calculator."""
    return OperationRegistry(calculator)


@pytest.fixture
def mock_calculator():
    """Provide a mocked Calculator instance."""
    return Mock(spec=Calculator)


@pytest.fixture
def mock_registry(mock_calculator):
    """Provide an OperationRegistry with a mocked Calculator."""
    return OperationRegistry(mock_calculator)


# ==============================================================================
# TESTS: Operation Frozen Dataclass
# ==============================================================================

class TestOperationDataclass:
    """Test suite for the Operation frozen dataclass."""

    def test_operation_creation_with_all_fields(self):
        """Test creating an Operation with all fields."""
        op = Operation("add", 2, "Addition", ("+",))
        assert op.name == "add"
        assert op.arity == 2
        assert op.display_name == "Addition"
        assert op.aliases == ("+",)

    def test_operation_creation_without_aliases(self):
        """Test creating an Operation without aliases."""
        op = Operation("factorial", 1, "Factorial")
        assert op.name == "factorial"
        assert op.arity == 1
        assert op.display_name == "Factorial"
        assert op.aliases == ()

    def test_operation_is_frozen(self):
        """Test that Operation instances are immutable (frozen)."""
        op = Operation("add", 2, "Addition", ("+",))
        with pytest.raises(AttributeError):
            op.name = "subtract"

    def test_operation_aliases_default_empty_tuple(self):
        """Test that aliases default to an empty tuple."""
        op = Operation("square", 1, "Square")
        assert op.aliases == ()
        assert isinstance(op.aliases, tuple)

    def test_operation_multiple_aliases(self):
        """Test Operation with multiple aliases."""
        op = Operation("power", 2, "Power", ("^", "**", "pow"))
        assert op.aliases == ("^", "**", "pow")

    def test_operation_arity_one(self):
        """Test Operation with arity 1."""
        op = Operation("square_root", 1, "Square Root", ("sqrt",))
        assert op.arity == 1

    def test_operation_arity_two(self):
        """Test Operation with arity 2."""
        op = Operation("add", 2, "Addition", ("+",))
        assert op.arity == 2


# ==============================================================================
# TESTS: _CATALOG Module Constant
# ==============================================================================

class TestCatalog:
    """Test suite for the _CATALOG module-level constant."""

    def test_catalog_is_list(self):
        """Test that _CATALOG is a list."""
        assert isinstance(_CATALOG, list)

    def test_catalog_has_12_operations(self):
        """Test that _CATALOG contains exactly 12 operations."""
        assert len(_CATALOG) == 12

    def test_catalog_contains_operation_objects(self):
        """Test that all items in _CATALOG are Operation instances."""
        for op in _CATALOG:
            assert isinstance(op, Operation)

    def test_catalog_canonical_names_unique(self):
        """Test that all canonical names in _CATALOG are unique."""
        names = [op.name for op in _CATALOG]
        assert len(names) == len(set(names))

    def test_catalog_contains_all_required_operations(self):
        """Test that _CATALOG contains all required operation names."""
        names = {op.name for op in _CATALOG}
        required = {
            "add", "subtract", "multiply", "divide", "power",
            "logarithm", "factorial", "square", "cube",
            "square_root", "cube_root", "natural_logarithm"
        }
        assert names == required

    def test_catalog_binary_operation_count(self):
        """Test that _CATALOG has exactly 6 binary operations."""
        binary_ops = [op for op in _CATALOG if op.arity == 2]
        assert len(binary_ops) == 6

    def test_catalog_unary_operation_count(self):
        """Test that _CATALOG has exactly 6 unary operations."""
        unary_ops = [op for op in _CATALOG if op.arity == 1]
        assert len(unary_ops) == 6

    def test_catalog_first_operation_is_add(self):
        """Test that the first operation in _CATALOG is 'add'."""
        assert _CATALOG[0].name == "add"

    def test_catalog_last_operation_is_natural_logarithm(self):
        """Test that the last operation in _CATALOG is 'natural_logarithm'."""
        assert _CATALOG[-1].name == "natural_logarithm"


# ==============================================================================
# TESTS: OperationRegistry Initialization
# ==============================================================================

class TestOperationRegistryInitialization:
    """Test suite for OperationRegistry initialization."""

    def test_init_stores_calculator(self, calculator):
        """Test __init__ stores the calculator reference."""
        registry = OperationRegistry(calculator)
        assert registry.calculator is calculator

    def test_init_creates_operations_list(self, calculator):
        """Test __init__ creates an internal operations list."""
        registry = OperationRegistry(calculator)
        assert hasattr(registry, "_operations")
        assert isinstance(registry._operations, list)
        assert len(registry._operations) == 12

    def test_init_creates_lookup_dict(self, calculator):
        """Test __init__ creates an internal lookup dictionary."""
        registry = OperationRegistry(calculator)
        assert hasattr(registry, "_lookup")
        assert isinstance(registry._lookup, dict)

    def test_init_lookup_contains_canonical_names(self, calculator):
        """Test __init__ lookup includes all canonical names."""
        registry = OperationRegistry(calculator)
        for op in _CATALOG:
            assert op.name in registry._lookup
            assert registry._lookup[op.name] == op

    def test_init_lookup_contains_aliases(self, calculator):
        """Test __init__ lookup includes all aliases."""
        registry = OperationRegistry(calculator)
        for op in _CATALOG:
            for alias in op.aliases:
                assert alias in registry._lookup
                assert registry._lookup[alias] == op

    def test_init_with_mock_calculator(self, mock_calculator):
        """Test __init__ works with a mocked calculator."""
        registry = OperationRegistry(mock_calculator)
        assert registry.calculator is mock_calculator


# ==============================================================================
# TESTS: OperationRegistry.get_operations()
# ==============================================================================

class TestGetOperations:
    """Test suite for get_operations() method."""

    def test_get_operations_returns_list(self, registry):
        """Test get_operations returns a list."""
        result = registry.get_operations()
        assert isinstance(result, list)

    def test_get_operations_returns_12_operations(self, registry):
        """Test get_operations returns all 12 operations."""
        result = registry.get_operations()
        assert len(result) == 12

    def test_get_operations_returns_operation_objects(self, registry):
        """Test get_operations returns Operation objects."""
        result = registry.get_operations()
        for op in result:
            assert isinstance(op, Operation)

    def test_get_operations_order_matches_catalog(self, registry):
        """Test get_operations preserves catalog order."""
        result = registry.get_operations()
        for i, op in enumerate(_CATALOG):
            assert result[i].name == op.name

    def test_get_operations_returns_copy(self, registry):
        """Test get_operations returns a copy, not the internal list."""
        result1 = registry.get_operations()
        result2 = registry.get_operations()
        assert result1 is not result2
        # But contents should be the same
        assert [op.name for op in result1] == [op.name for op in result2]

    def test_get_operations_first_is_add(self, registry):
        """Test get_operations first operation is 'add'."""
        result = registry.get_operations()
        assert result[0].name == "add"

    def test_get_operations_last_is_natural_logarithm(self, registry):
        """Test get_operations last operation is 'natural_logarithm'."""
        result = registry.get_operations()
        assert result[-1].name == "natural_logarithm"


# ==============================================================================
# TESTS: OperationRegistry.get_operation()
# ==============================================================================

class TestGetOperation:
    """Test suite for get_operation() method."""

    def test_get_operation_by_canonical_name_add(self, registry):
        """Test get_operation returns Operation for 'add' by name."""
        op = registry.get_operation("add")
        assert op is not None
        assert op.name == "add"

    def test_get_operation_by_alias_plus(self, registry):
        """Test get_operation returns Operation for '+' alias."""
        op = registry.get_operation("+")
        assert op is not None
        assert op.name == "add"

    def test_get_operation_by_canonical_name_square_root(self, registry):
        """Test get_operation returns Operation for 'square_root' by name."""
        op = registry.get_operation("square_root")
        assert op is not None
        assert op.name == "square_root"

    def test_get_operation_by_alias_sqrt(self, registry):
        """Test get_operation returns Operation for 'sqrt' alias."""
        op = registry.get_operation("sqrt")
        assert op is not None
        assert op.name == "square_root"

    def test_get_operation_by_alias_log(self, registry):
        """Test get_operation returns Operation for 'log' alias."""
        op = registry.get_operation("log")
        assert op is not None
        assert op.name == "logarithm"

    def test_get_operation_unknown_token_returns_none(self, registry):
        """Test get_operation returns None for unknown token."""
        op = registry.get_operation("foobar")
        assert op is None

    def test_get_operation_empty_string_returns_none(self, registry):
        """Test get_operation returns None for empty string."""
        op = registry.get_operation("")
        assert op is None

    def test_get_operation_case_sensitive(self, registry):
        """Test get_operation is case-sensitive."""
        op = registry.get_operation("ADD")
        assert op is None

    def test_get_operation_all_canonical_names(self, registry):
        """Test get_operation works for all canonical names."""
        for op_def in _CATALOG:
            op = registry.get_operation(op_def.name)
            assert op is not None
            assert op.name == op_def.name

    def test_get_operation_all_aliases(self, registry):
        """Test get_operation works for all aliases."""
        for op_def in _CATALOG:
            for alias in op_def.aliases:
                op = registry.get_operation(alias)
                assert op is not None
                assert op.name == op_def.name


# ==============================================================================
# TESTS: OperationRegistry.resolve()
# ==============================================================================

class TestResolve:
    """Test suite for resolve() method."""

    def test_resolve_canonical_name_add(self, registry):
        """Test resolve returns canonical name for 'add'."""
        result = registry.resolve("add")
        assert result == "add"

    def test_resolve_alias_plus(self, registry):
        """Test resolve returns canonical name for '+' alias."""
        result = registry.resolve("+")
        assert result == "add"

    def test_resolve_alias_sqrt(self, registry):
        """Test resolve returns canonical name for 'sqrt' alias."""
        result = registry.resolve("sqrt")
        assert result == "square_root"

    def test_resolve_alias_log(self, registry):
        """Test resolve returns canonical name for 'log' alias."""
        result = registry.resolve("log")
        assert result == "logarithm"

    def test_resolve_alias_ln(self, registry):
        """Test resolve returns canonical name for 'ln' alias."""
        result = registry.resolve("ln")
        assert result == "natural_logarithm"

    def test_resolve_alias_cbrt(self, registry):
        """Test resolve returns canonical name for 'cbrt' alias."""
        result = registry.resolve("cbrt")
        assert result == "cube_root"

    def test_resolve_unknown_raises_valueerror(self, registry):
        """Test resolve raises ValueError for unknown token."""
        with pytest.raises(ValueError) as exc_info:
            registry.resolve("foobar")
        assert "Unknown operation" in str(exc_info.value)
        assert "foobar" in str(exc_info.value)

    def test_resolve_empty_string_raises_valueerror(self, registry):
        """Test resolve raises ValueError for empty string."""
        with pytest.raises(ValueError) as exc_info:
            registry.resolve("")
        assert "Unknown operation" in str(exc_info.value)

    def test_resolve_case_sensitive(self, registry):
        """Test resolve is case-sensitive."""
        with pytest.raises(ValueError):
            registry.resolve("ADD")

    def test_resolve_all_canonical_names(self, registry):
        """Test resolve works for all canonical names."""
        for op_def in _CATALOG:
            result = registry.resolve(op_def.name)
            assert result == op_def.name

    def test_resolve_all_aliases(self, registry):
        """Test resolve works for all aliases."""
        for op_def in _CATALOG:
            for alias in op_def.aliases:
                result = registry.resolve(alias)
                assert result == op_def.name


# ==============================================================================
# TESTS: OperationRegistry.arity()
# ==============================================================================

class TestArity:
    """Test suite for arity() method."""

    def test_arity_add_is_2(self, registry):
        """Test arity of 'add' is 2."""
        assert registry.arity("add") == 2

    def test_arity_plus_is_2(self, registry):
        """Test arity of '+' alias is 2."""
        assert registry.arity("+") == 2

    def test_arity_factorial_is_1(self, registry):
        """Test arity of 'factorial' is 1."""
        assert registry.arity("factorial") == 1

    def test_arity_square_is_1(self, registry):
        """Test arity of 'square' is 1."""
        assert registry.arity("square") == 1

    def test_arity_sqrt_is_1(self, registry):
        """Test arity of 'sqrt' alias is 1."""
        assert registry.arity("sqrt") == 1

    def test_arity_logarithm_is_2(self, registry):
        """Test arity of 'logarithm' is 2."""
        assert registry.arity("logarithm") == 2

    def test_arity_log_is_2(self, registry):
        """Test arity of 'log' alias is 2."""
        assert registry.arity("log") == 2

    def test_arity_all_binary_operations(self, registry):
        """Test arity of all binary operations is 2."""
        binary_names = ["add", "+", "subtract", "-", "multiply", "*", "divide", "/", "power", "^", "logarithm", "log"]
        for name in binary_names:
            assert registry.arity(name) == 2, f"arity({name}) should be 2"

    def test_arity_all_unary_operations(self, registry):
        """Test arity of all unary operations is 1."""
        unary_names = ["factorial", "square", "cube", "square_root", "sqrt", "cube_root", "cbrt", "natural_logarithm", "ln"]
        for name in unary_names:
            assert registry.arity(name) == 1, f"arity({name}) should be 1"

    def test_arity_unknown_raises_valueerror(self, registry):
        """Test arity raises ValueError for unknown token."""
        with pytest.raises(ValueError) as exc_info:
            registry.arity("foobar")
        assert "Unknown operation" in str(exc_info.value)

    def test_arity_empty_string_raises_valueerror(self, registry):
        """Test arity raises ValueError for empty string."""
        with pytest.raises(ValueError):
            registry.arity("")


# ==============================================================================
# TESTS: OperationRegistry.get_operation_mapping()
# ==============================================================================

class TestGetOperationMapping:
    """Test suite for get_operation_mapping() method."""

    def test_get_operation_mapping_returns_dict(self, registry):
        """Test get_operation_mapping returns a dictionary."""
        result = registry.get_operation_mapping()
        assert isinstance(result, dict)

    def test_get_operation_mapping_contains_all_names(self, registry):
        """Test mapping contains all canonical operation names."""
        mapping = registry.get_operation_mapping()
        for op_def in _CATALOG:
            assert op_def.name in mapping

    def test_get_operation_mapping_contains_all_aliases(self, registry):
        """Test mapping contains all aliases."""
        mapping = registry.get_operation_mapping()
        for op_def in _CATALOG:
            for alias in op_def.aliases:
                assert alias in mapping

    def test_get_operation_mapping_name_to_canonical(self, registry):
        """Test mapping values are canonical names."""
        mapping = registry.get_operation_mapping()
        assert mapping["add"] == "add"
        assert mapping["square"] == "square"

    def test_get_operation_mapping_alias_to_canonical(self, registry):
        """Test mapping aliases to canonical names."""
        mapping = registry.get_operation_mapping()
        assert mapping["+"] == "add"
        assert mapping["sqrt"] == "square_root"
        assert mapping["log"] == "logarithm"
        assert mapping["ln"] == "natural_logarithm"

    def test_get_operation_mapping_size(self, registry):
        """Test mapping has expected number of entries."""
        mapping = registry.get_operation_mapping()
        # 12 canonical names + number of aliases
        alias_count = sum(len(op.aliases) for op in _CATALOG)
        expected_size = 12 + alias_count
        assert len(mapping) == expected_size

    def test_get_operation_mapping_returns_copy(self, registry):
        """Test get_operation_mapping returns a new dict each time."""
        mapping1 = registry.get_operation_mapping()
        mapping2 = registry.get_operation_mapping()
        assert mapping1 is not mapping2
        assert mapping1 == mapping2


# ==============================================================================
# TESTS: OperationRegistry.dispatch() - HAPPY PATH
# ==============================================================================

class TestDispatchBinaryOps:
    """Test suite for dispatch() with binary operations."""

    def test_dispatch_add(self, registry):
        """Test dispatch for add operation."""
        result = registry.dispatch("add", [2.0, 3.0])
        assert result == 5.0

    def test_dispatch_subtract(self, registry):
        """Test dispatch for subtract operation."""
        result = registry.dispatch("subtract", [10.0, 3.0])
        assert result == 7.0

    def test_dispatch_multiply(self, registry):
        """Test dispatch for multiply operation."""
        result = registry.dispatch("multiply", [5.0, 6.0])
        assert result == 30.0

    def test_dispatch_divide(self, registry):
        """Test dispatch for divide operation."""
        result = registry.dispatch("divide", [12.0, 3.0])
        assert result == 4.0

    def test_dispatch_power(self, registry):
        """Test dispatch for power operation."""
        result = registry.dispatch("power", [2.0, 3.0])
        assert result == 8.0


class TestDispatchUnaryOps:
    """Test suite for dispatch() with unary operations."""

    def test_dispatch_factorial(self, registry):
        """Test dispatch for factorial operation."""
        result = registry.dispatch("factorial", [5.0])
        assert result == 120

    def test_dispatch_square(self, registry):
        """Test dispatch for square operation."""
        result = registry.dispatch("square", [4.0])
        assert result == 16.0

    def test_dispatch_cube(self, registry):
        """Test dispatch for cube operation."""
        result = registry.dispatch("cube", [3.0])
        assert result == 27.0

    def test_dispatch_square_root(self, registry):
        """Test dispatch for square_root operation."""
        result = registry.dispatch("square_root", [16.0])
        assert result == 4.0

    def test_dispatch_cube_root(self, registry):
        """Test dispatch for cube_root operation."""
        result = registry.dispatch("cube_root", [8.0])
        assert result == 2.0

    def test_dispatch_natural_logarithm(self, registry):
        """Test dispatch for natural_logarithm operation."""
        result = registry.dispatch("natural_logarithm", [math.e])
        assert abs(result - 1.0) < 0.0001


# ==============================================================================
# TESTS: OperationRegistry.dispatch() - LOGARITHM SPECIAL HANDLING
# ==============================================================================

class TestDispatchLogarithm:
    """Test suite for dispatch() with logarithm (special two-argument case)."""

    def test_dispatch_logarithm_base_2(self, registry):
        """Test dispatch logarithm with base 2."""
        result = registry.dispatch("logarithm", [8.0, 2.0])
        assert result == 3.0

    def test_dispatch_logarithm_base_10(self, registry):
        """Test dispatch logarithm with base 10."""
        result = registry.dispatch("logarithm", [100.0, 10.0])
        assert result == 2.0

    def test_dispatch_logarithm_base_e(self, registry):
        """Test dispatch logarithm with base e (natural log)."""
        result = registry.dispatch("logarithm", [math.e, math.e])
        assert abs(result - 1.0) < 0.0001

    def test_dispatch_logarithm_uses_math_log(self, registry):
        """Test dispatch uses math.log for logarithm."""
        x, base = 16.0, 2.0
        result = registry.dispatch("logarithm", [x, base])
        expected = math.log(x, base)
        assert result == expected

    def test_dispatch_logarithm_fractional_result(self, registry):
        """Test dispatch logarithm with fractional result."""
        result = registry.dispatch("logarithm", [2.0, 10.0])
        expected = math.log(2.0, 10.0)
        assert abs(result - expected) < 0.0001

    def test_dispatch_logarithm_invalid_base_zero(self, registry):
        """Test dispatch logarithm with base 0 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            registry.dispatch("logarithm", [8.0, 0.0])
        assert "base must be positive and not equal to 1" in str(exc_info.value)

    def test_dispatch_logarithm_invalid_base_one(self, registry):
        """Test dispatch logarithm with base 1 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            registry.dispatch("logarithm", [8.0, 1.0])
        assert "base must be positive and not equal to 1" in str(exc_info.value)

    def test_dispatch_logarithm_invalid_base_negative(self, registry):
        """Test dispatch logarithm with negative base raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            registry.dispatch("logarithm", [8.0, -2.0])
        assert "base must be positive and not equal to 1" in str(exc_info.value)

    def test_dispatch_logarithm_invalid_x_zero(self, registry):
        """Test dispatch logarithm with x=0 raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            registry.dispatch("logarithm", [0.0, 2.0])
        assert "not defined for non-positive values" in str(exc_info.value)

    def test_dispatch_logarithm_invalid_x_negative(self, registry):
        """Test dispatch logarithm with negative x raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            registry.dispatch("logarithm", [-5.0, 2.0])
        assert "not defined for non-positive values" in str(exc_info.value)

    def test_dispatch_logarithm_very_small_x(self, registry):
        """Test dispatch logarithm with very small x."""
        result = registry.dispatch("logarithm", [0.0001, 10.0])
        expected = math.log(0.0001, 10.0)
        assert abs(result - expected) < 0.0001

    def test_dispatch_logarithm_very_large_x(self, registry):
        """Test dispatch logarithm with very large x."""
        result = registry.dispatch("logarithm", [1e10, 10.0])
        expected = math.log(1e10, 10.0)
        assert abs(result - expected) < 0.0001


# ==============================================================================
# TESTS: OperationRegistry.dispatch() - ERROR HANDLING
# ==============================================================================

class TestDispatchErrorHandling:
    """Test suite for dispatch() error handling and propagation."""

    def test_dispatch_divide_by_zero(self, registry):
        """Test dispatch propagates ZeroDivisionError from Calculator."""
        with pytest.raises(ZeroDivisionError):
            registry.dispatch("divide", [10.0, 0.0])

    def test_dispatch_square_root_negative(self, registry):
        """Test dispatch propagates ValueError from Calculator."""
        with pytest.raises(ValueError) as exc_info:
            registry.dispatch("square_root", [-4.0])
        assert "not defined for negative values" in str(exc_info.value)

    def test_dispatch_factorial_non_integer(self, registry):
        """Test dispatch propagates TypeError from Calculator."""
        with pytest.raises(TypeError) as exc_info:
            registry.dispatch("factorial", [2.5])
        assert "only accepts integer values" in str(exc_info.value)

    def test_dispatch_factorial_negative(self, registry):
        """Test dispatch propagates ValueError for negative factorial."""
        with pytest.raises(ValueError) as exc_info:
            registry.dispatch("factorial", [-5.0])
        assert "not defined for negative values" in str(exc_info.value)

    def test_dispatch_natural_logarithm_zero(self, registry):
        """Test dispatch propagates ValueError for ln(0)."""
        with pytest.raises(ValueError):
            registry.dispatch("natural_logarithm", [0.0])

    def test_dispatch_natural_logarithm_negative(self, registry):
        """Test dispatch propagates ValueError for ln(negative)."""
        with pytest.raises(ValueError):
            registry.dispatch("natural_logarithm", [-1.0])


# ==============================================================================
# TESTS: OperationRegistry.dispatch() - EDGE CASES
# ==============================================================================

class TestDispatchEdgeCases:
    """Test suite for dispatch() edge cases."""

    def test_dispatch_add_zero(self, registry):
        """Test dispatch add with zero."""
        result = registry.dispatch("add", [0.0, 5.0])
        assert result == 5.0

    def test_dispatch_add_negative(self, registry):
        """Test dispatch add with negative numbers."""
        result = registry.dispatch("add", [-3.0, -4.0])
        assert result == -7.0

    def test_dispatch_multiply_zero(self, registry):
        """Test dispatch multiply by zero."""
        result = registry.dispatch("multiply", [100.0, 0.0])
        assert result == 0.0

    def test_dispatch_multiply_negative(self, registry):
        """Test dispatch multiply negative numbers."""
        result = registry.dispatch("multiply", [-5.0, -6.0])
        assert result == 30.0

    def test_dispatch_square_zero(self, registry):
        """Test dispatch square of zero."""
        result = registry.dispatch("square", [0.0])
        assert result == 0.0

    def test_dispatch_square_negative(self, registry):
        """Test dispatch square of negative number."""
        result = registry.dispatch("square", [-5.0])
        assert result == 25.0

    def test_dispatch_cube_negative(self, registry):
        """Test dispatch cube of negative number."""
        result = registry.dispatch("cube", [-2.0])
        assert result == -8.0

    def test_dispatch_cube_root_negative(self, registry):
        """Test dispatch cube root of negative number."""
        result = registry.dispatch("cube_root", [-8.0])
        assert abs(result - (-2.0)) < 0.0001

    def test_dispatch_power_zero_exponent(self, registry):
        """Test dispatch power with zero exponent."""
        result = registry.dispatch("power", [5.0, 0.0])
        assert result == 1.0

    def test_dispatch_power_fractional_exponent(self, registry):
        """Test dispatch power with fractional exponent."""
        result = registry.dispatch("power", [4.0, 0.5])
        assert abs(result - 2.0) < 0.0001

    def test_dispatch_factorial_zero(self, registry):
        """Test dispatch factorial of zero."""
        result = registry.dispatch("factorial", [0.0])
        assert result == 1

    def test_dispatch_factorial_one(self, registry):
        """Test dispatch factorial of one."""
        result = registry.dispatch("factorial", [1.0])
        assert result == 1

    def test_dispatch_divide_result_fraction(self, registry):
        """Test dispatch division with fractional result."""
        result = registry.dispatch("divide", [10.0, 3.0])
        expected = 10.0 / 3.0
        assert abs(result - expected) < 0.0001

    def test_dispatch_subtract_negative_result(self, registry):
        """Test dispatch subtraction resulting in negative."""
        result = registry.dispatch("subtract", [3.0, 10.0])
        assert result == -7.0


# ==============================================================================
# TESTS: OperationRegistry with Mock Calculator
# ==============================================================================

class TestDispatchWithMockCalculator:
    """Test suite for dispatch() behavior with mocked Calculator."""

    def test_dispatch_calls_calculator_method(self, mock_registry):
        """Test dispatch calls the correct Calculator method."""
        mock_registry.calculator.add = Mock(return_value=5.0)
        result = mock_registry.dispatch("add", [2.0, 3.0])
        mock_registry.calculator.add.assert_called_once_with(2.0, 3.0)
        assert result == 5.0

    def test_dispatch_calls_correct_method_for_operation(self, mock_registry):
        """Test dispatch calls operation-specific method."""
        mock_registry.calculator.square = Mock(return_value=16.0)
        result = mock_registry.dispatch("square", [4.0])
        mock_registry.calculator.square.assert_called_once_with(4.0)
        assert result == 16.0

    def test_dispatch_propagates_calculator_exception(self, mock_registry):
        """Test dispatch propagates exceptions from Calculator."""
        mock_registry.calculator.divide = Mock(side_effect=ZeroDivisionError("Cannot divide by zero"))
        with pytest.raises(ZeroDivisionError):
            mock_registry.dispatch("divide", [10.0, 0.0])

    def test_dispatch_logarithm_skips_calculator(self, mock_registry):
        """Test dispatch for logarithm does not call Calculator.logarithm."""
        result = mock_registry.dispatch("logarithm", [8.0, 2.0])
        # logarithm should use math.log directly, not calculator
        mock_registry.calculator.logarithm.assert_not_called()
        assert result == 3.0


# ==============================================================================
# TESTS: OperationRegistry Consistency
# ==============================================================================

class TestRegistryConsistency:
    """Test suite for consistency between registry methods."""

    def test_resolve_and_arity_consistency(self, registry):
        """Test that resolve() and arity() use consistent operation lookup."""
        for op_def in _CATALOG:
            # For all canonical names and aliases
            tokens = [op_def.name] + list(op_def.aliases)
            for token in tokens:
                canonical = registry.resolve(token)
                arity = registry.arity(token)
                assert canonical == op_def.name
                assert arity == op_def.arity

    def test_get_operation_and_resolve_consistency(self, registry):
        """Test that get_operation() and resolve() are consistent."""
        for token in registry.get_operation_mapping().keys():
            op = registry.get_operation(token)
            canonical = registry.resolve(token)
            assert op is not None
            assert op.name == canonical

    def test_get_operation_mapping_consistency(self, registry):
        """Test that get_operation_mapping() matches resolve() output."""
        mapping = registry.get_operation_mapping()
        for token, canonical in mapping.items():
            assert registry.resolve(token) == canonical

    def test_dispatch_uses_resolved_operation(self, registry):
        """Test that dispatch works with both names and aliases."""
        result_by_name = registry.dispatch("add", [2.0, 3.0])
        # Should be the same operation semantically
        calc_result = registry.calculator.add(2.0, 3.0)
        assert result_by_name == calc_result == 5.0


# ==============================================================================
# TESTS: Special Float Values
# ==============================================================================

class TestSpecialFloatValues:
    """Test suite for dispatch() with special float values."""

    def test_dispatch_add_infinity(self, registry):
        """Test dispatch add with infinity."""
        result = registry.dispatch("add", [float('inf'), 1.0])
        assert result == float('inf')

    def test_dispatch_add_negative_infinity(self, registry):
        """Test dispatch add with negative infinity."""
        result = registry.dispatch("add", [float('-inf'), 1.0])
        assert result == float('-inf')

    def test_dispatch_multiply_by_infinity(self, registry):
        """Test dispatch multiply by infinity."""
        result = registry.dispatch("multiply", [2.0, float('inf')])
        assert result == float('inf')

    def test_dispatch_logarithm_base_very_small(self, registry):
        """Test dispatch logarithm with very small base > 0."""
        result = registry.dispatch("logarithm", [2.0, 1.0001])
        # Should work since base is > 0 and != 1
        assert not math.isnan(result)
        assert result > 0

    def test_dispatch_logarithm_very_small_x_and_small_base(self, registry):
        """Test dispatch logarithm with very small x and base."""
        result = registry.dispatch("logarithm", [0.00001, 0.5])
        expected = math.log(0.00001, 0.5)
        assert abs(result - expected) < 0.0001


# ==============================================================================
# TESTS: Numeric Precision
# ==============================================================================

class TestNumericPrecision:
    """Test suite for numeric precision in dispatch()."""

    def test_dispatch_power_fractional_precision(self, registry):
        """Test dispatch power maintains precision with fractional exponents."""
        result = registry.dispatch("power", [2.0, 0.5])
        expected = math.sqrt(2.0)
        assert abs(result - expected) < 1e-10

    def test_dispatch_logarithm_precision(self, registry):
        """Test dispatch logarithm maintains precision."""
        x, base = 1000.0, 10.0
        result = registry.dispatch("logarithm", [x, base])
        expected = math.log(x, base)
        assert abs(result - expected) < 1e-10

    def test_dispatch_square_root_precision(self, registry):
        """Test dispatch square_root maintains precision."""
        result = registry.dispatch("square_root", [2.0])
        expected = math.sqrt(2.0)
        assert abs(result - expected) < 1e-10


# ==============================================================================
# TESTS: Large and Small Numbers
# ==============================================================================

class TestLargeAndSmallNumbers:
    """Test suite for dispatch() with very large and very small numbers."""

    def test_dispatch_add_very_large(self, registry):
        """Test dispatch add with very large numbers."""
        result = registry.dispatch("add", [1e100, 1e100])
        assert result == 2e100

    def test_dispatch_multiply_very_large(self, registry):
        """Test dispatch multiply with large numbers (may overflow)."""
        # This might result in infinity
        result = registry.dispatch("multiply", [1e200, 1e200])
        assert result == float('inf')

    def test_dispatch_very_small_operand(self, registry):
        """Test dispatch with very small positive operands."""
        result = registry.dispatch("add", [1e-300, 1e-300])
        # Result might underflow to zero
        assert result >= 0

    def test_dispatch_square_root_very_small(self, registry):
        """Test dispatch square root of very small number."""
        result = registry.dispatch("square_root", [1e-100])
        expected = math.sqrt(1e-100)
        assert abs(result - expected) < 1e-110
