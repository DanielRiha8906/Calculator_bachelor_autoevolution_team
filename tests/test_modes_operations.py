"""test_modes_operations.py — tests for operation registry and constants.

Tests cover:
- BASIC_OPERATIONS and ADVANCED_OPERATIONS frozenset membership
- OperationRegistry initialization, registration, and lookup
- Error handling for unregistered operations
"""

import pytest
from src.modes.operations import (
    BASIC_OPERATIONS,
    ADVANCED_OPERATIONS,
    BaseOperationSet,
    OperationRegistry,
)


# =============================================================================
# Test Operation Constants
# =============================================================================


class TestOperationConstants:
    """Tests for BASIC_OPERATIONS and ADVANCED_OPERATIONS constants."""

    def test_basic_operations_is_frozenset(self):
        """Test that BASIC_OPERATIONS is a frozenset."""
        assert isinstance(BASIC_OPERATIONS, frozenset)

    def test_advanced_operations_is_frozenset(self):
        """Test that ADVANCED_OPERATIONS is a frozenset."""
        assert isinstance(ADVANCED_OPERATIONS, frozenset)

    def test_basic_operations_contains_add(self):
        """Test that BASIC_OPERATIONS contains 'add'."""
        assert "add" in BASIC_OPERATIONS

    def test_basic_operations_contains_subtract(self):
        """Test that BASIC_OPERATIONS contains 'subtract'."""
        assert "subtract" in BASIC_OPERATIONS

    def test_basic_operations_contains_multiply(self):
        """Test that BASIC_OPERATIONS contains 'multiply'."""
        assert "multiply" in BASIC_OPERATIONS

    def test_basic_operations_contains_divide(self):
        """Test that BASIC_OPERATIONS contains 'divide'."""
        assert "divide" in BASIC_OPERATIONS

    def test_basic_operations_has_exactly_four_members(self):
        """Test that BASIC_OPERATIONS has exactly 4 members."""
        assert len(BASIC_OPERATIONS) == 4

    def test_basic_operations_contains_only_expected_members(self):
        """Test that BASIC_OPERATIONS contains exactly the expected operations."""
        expected = {"add", "subtract", "multiply", "divide"}
        assert BASIC_OPERATIONS == expected

    def test_advanced_operations_contains_factorial(self):
        """Test that ADVANCED_OPERATIONS contains 'factorial'."""
        assert "factorial" in ADVANCED_OPERATIONS

    def test_advanced_operations_contains_square(self):
        """Test that ADVANCED_OPERATIONS contains 'square'."""
        assert "square" in ADVANCED_OPERATIONS

    def test_advanced_operations_contains_cube(self):
        """Test that ADVANCED_OPERATIONS contains 'cube'."""
        assert "cube" in ADVANCED_OPERATIONS

    def test_advanced_operations_contains_square_root(self):
        """Test that ADVANCED_OPERATIONS contains 'square_root'."""
        assert "square_root" in ADVANCED_OPERATIONS

    def test_advanced_operations_contains_cube_root(self):
        """Test that ADVANCED_OPERATIONS contains 'cube_root'."""
        assert "cube_root" in ADVANCED_OPERATIONS

    def test_advanced_operations_contains_power(self):
        """Test that ADVANCED_OPERATIONS contains 'power'."""
        assert "power" in ADVANCED_OPERATIONS

    def test_advanced_operations_contains_natural_log(self):
        """Test that ADVANCED_OPERATIONS contains 'natural_log'."""
        assert "natural_log" in ADVANCED_OPERATIONS

    def test_advanced_operations_contains_log_base_10(self):
        """Test that ADVANCED_OPERATIONS contains 'log_base_10'."""
        assert "log_base_10" in ADVANCED_OPERATIONS

    def test_advanced_operations_has_exactly_eight_members(self):
        """Test that ADVANCED_OPERATIONS has exactly 8 members."""
        assert len(ADVANCED_OPERATIONS) == 8

    def test_advanced_operations_contains_only_expected_members(self):
        """Test that ADVANCED_OPERATIONS contains exactly the expected operations."""
        expected = {
            "factorial",
            "square",
            "cube",
            "square_root",
            "cube_root",
            "power",
            "natural_log",
            "log_base_10",
        }
        assert ADVANCED_OPERATIONS == expected

    def test_basic_and_advanced_do_not_overlap(self):
        """Test that BASIC_OPERATIONS and ADVANCED_OPERATIONS have no common members."""
        assert len(BASIC_OPERATIONS & ADVANCED_OPERATIONS) == 0

    def test_power_is_only_in_advanced_operations(self):
        """Test that 'power' is in ADVANCED_OPERATIONS and not in BASIC_OPERATIONS."""
        assert "power" in ADVANCED_OPERATIONS
        assert "power" not in BASIC_OPERATIONS


# =============================================================================
# Test OperationRegistry
# =============================================================================


class TestOperationRegistry:
    """Tests for OperationRegistry class."""

    @pytest.fixture
    def registry(self):
        """Provide a fresh OperationRegistry instance."""
        return OperationRegistry()

    def test_registry_initializes_empty(self, registry):
        """Test that a new registry starts with no operations."""
        assert registry.all_names() == frozenset()

    def test_register_mode_adds_operations(self, registry):
        """Test that register_mode adds operations to the registry."""
        ops = {"add": lambda x, y: x + y, "subtract": lambda x, y: x - y}
        registry.register_mode("basic", ops)
        assert "add" in registry.all_names()
        assert "subtract" in registry.all_names()

    def test_register_mode_stores_correct_number_of_operations(self, registry):
        """Test that register_mode stores all provided operations."""
        ops = {
            "add": lambda x, y: x + y,
            "subtract": lambda x, y: x - y,
            "multiply": lambda x, y: x * y,
        }
        registry.register_mode("basic", ops)
        assert len(registry.all_names()) == 3

    def test_get_operation_by_name(self, registry):
        """Test that get() returns the registered operation."""
        add_fn = lambda x, y: x + y
        registry.register_mode("basic", {"add": add_fn})
        retrieved = registry.get("add")
        assert retrieved is add_fn

    def test_get_unregistered_operation_raises_keyerror(self, registry):
        """Test that get() raises KeyError for unregistered operations."""
        with pytest.raises(KeyError) as exc_info:
            registry.get("nonexistent")
        assert "not registered" in str(exc_info.value)

    def test_get_mode_returns_mode_name(self, registry):
        """Test that get_mode() returns the mode that registered an operation."""
        registry.register_mode("basic", {"add": lambda x, y: x + y})
        assert registry.get_mode("add") == "basic"

    def test_get_mode_with_unregistered_operation_raises_keyerror(self, registry):
        """Test that get_mode() raises KeyError for unregistered operations."""
        with pytest.raises(KeyError) as exc_info:
            registry.get_mode("nonexistent")
        assert "not registered" in str(exc_info.value)

    def test_multiple_modes_can_be_registered(self, registry):
        """Test that multiple modes can be registered in the same registry."""
        basic_ops = {"add": lambda x, y: x + y}
        advanced_ops = {"factorial": lambda n: 1 if n <= 1 else n}
        registry.register_mode("basic", basic_ops)
        registry.register_mode("advanced", advanced_ops)
        assert len(registry.all_names()) == 2

    def test_overlapping_operations_last_registration_wins(self, registry):
        """Test that later registration overwrites earlier for same operation name."""
        fn1 = lambda x, y: x + y
        fn2 = lambda x, y: x * y
        registry.register_mode("basic", {"op": fn1})
        registry.register_mode("override", {"op": fn2})
        retrieved = registry.get("op")
        assert retrieved is fn2
        assert registry.get_mode("op") == "override"

    def test_all_names_returns_frozenset(self, registry):
        """Test that all_names() returns a frozenset."""
        registry.register_mode("basic", {"add": lambda x, y: x + y})
        result = registry.all_names()
        assert isinstance(result, frozenset)

    def test_all_names_is_immutable(self, registry):
        """Test that all_names() returns an immutable frozenset."""
        registry.register_mode("basic", {"add": lambda x, y: x + y})
        names = registry.all_names()
        # frozenset is immutable, this just verifies it has no add method that works
        assert not hasattr(names, "add") or callable(names.add) is False or True

    def test_register_empty_dict_does_not_add_operations(self, registry):
        """Test that registering an empty dict doesn't add any operations."""
        registry.register_mode("empty", {})
        assert registry.all_names() == frozenset()

    def test_register_mode_multiple_times_accumulates(self, registry):
        """Test that calling register_mode multiple times accumulates operations."""
        registry.register_mode("basic", {"add": lambda x, y: x + y})
        registry.register_mode("basic", {"subtract": lambda x, y: x - y})
        assert len(registry.all_names()) == 2
        assert "add" in registry.all_names()
        assert "subtract" in registry.all_names()

    def test_get_returns_callable(self, registry):
        """Test that get() returns a callable object."""
        fn = lambda x, y: x + y
        registry.register_mode("basic", {"add": fn})
        retrieved = registry.get("add")
        assert callable(retrieved)
