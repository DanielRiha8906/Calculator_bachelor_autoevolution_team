"""Comprehensive tests for the operations base module.

Tests cover:
- OperationRegistry: registration, retrieval, listing, duplicate handling
- Operation abstract interface: instantiation, abstract method enforcement
"""

import pytest
from src.operations.base import Operation, OperationRegistry


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def registry():
    """Provides a fresh OperationRegistry instance for each test."""
    return OperationRegistry()


class MockOperation(Operation):
    """A minimal concrete Operation for testing."""

    def name(self) -> str:
        return "mock"

    def operand_count(self) -> int:
        return 2

    def execute(self, *args) -> float:
        return 42.0


# ============================================================================
# TEST OPERATION ABSTRACT INTERFACE
# ============================================================================


class TestOperationAbstractInterface:
    """Verify that Operation enforces abstract method implementation."""

    def test_cannot_instantiate_operation_directly(self):
        """Test that Operation() raises TypeError (abstract)."""
        with pytest.raises(TypeError):
            Operation()

    def test_concrete_operation_must_implement_name(self):
        """Test that concrete class without name() raises TypeError."""

        class IncompleteOp1(Operation):
            def operand_count(self) -> int:
                return 1

            def execute(self, *args) -> float:
                return 0.0

        with pytest.raises(TypeError):
            IncompleteOp1()

    def test_concrete_operation_must_implement_execute(self):
        """Test that concrete class without execute() raises TypeError."""

        class IncompleteOp2(Operation):
            def name(self) -> str:
                return "incomplete"

            def operand_count(self) -> int:
                return 1

        with pytest.raises(TypeError):
            IncompleteOp2()

    def test_concrete_operation_must_implement_operand_count(self):
        """Test that concrete class without operand_count() raises TypeError."""

        class IncompleteOp3(Operation):
            def name(self) -> str:
                return "incomplete"

            def execute(self, *args) -> float:
                return 0.0

        with pytest.raises(TypeError):
            IncompleteOp3()

    def test_concrete_operation_with_all_methods_works(self):
        """Test that a properly implemented concrete Operation can be instantiated."""
        op = MockOperation()
        assert op is not None
        assert op.name() == "mock"
        assert op.operand_count() == 2
        assert op.execute(1, 2) == 42.0


# ============================================================================
# TEST OPERATION REGISTRY
# ============================================================================


class TestOperationRegistry:
    """Test suite for OperationRegistry."""

    def test_new_registry_is_empty(self, registry):
        """Test that a new registry has no operations."""
        assert registry.list_operations() == []

    def test_register_and_get_operation(self, registry):
        """Test registering and retrieving a single operation."""
        op = MockOperation()
        registry.register("mock", op)
        retrieved = registry.get("mock")
        assert retrieved is op

    def test_get_nonexistent_returns_none(self, registry):
        """Test that get() returns None for unregistered names."""
        assert registry.get("nonexistent") is None

    def test_list_operations_empty(self, registry):
        """Test that list_operations() returns empty list for new registry."""
        assert registry.list_operations() == []

    def test_list_operations_after_register(self, registry):
        """Test that list_operations() includes registered operation."""
        op = MockOperation()
        registry.register("mock", op)
        assert "mock" in registry.list_operations()

    def test_is_registered_true_after_register(self, registry):
        """Test that is_registered() returns True after registering."""
        op = MockOperation()
        registry.register("test_op", op)
        assert registry.is_registered("test_op") is True

    def test_is_registered_false_before_register(self, registry):
        """Test that is_registered() returns False before registering."""
        assert registry.is_registered("never_registered") is False

    def test_register_duplicate_overwrites(self, registry):
        """Test that registering the same name twice replaces the previous operation."""
        op1 = MockOperation()
        op2 = MockOperation()
        registry.register("op", op1)
        assert registry.get("op") is op1
        registry.register("op", op2)
        assert registry.get("op") is op2

    def test_list_operations_returns_all_names(self, registry):
        """Test that list_operations() returns all registered names."""

        class Op1(Operation):
            def name(self) -> str:
                return "op1"

            def operand_count(self) -> int:
                return 1

            def execute(self, *args) -> float:
                return 1.0

        class Op2(Operation):
            def name(self) -> str:
                return "op2"

            def operand_count(self) -> int:
                return 1

            def execute(self, *args) -> float:
                return 2.0

        class Op3(Operation):
            def name(self) -> str:
                return "op3"

            def operand_count(self) -> int:
                return 1

            def execute(self, *args) -> float:
                return 3.0

        op1 = Op1()
        op2 = Op2()
        op3 = Op3()
        registry.register("op1", op1)
        registry.register("op2", op2)
        registry.register("op3", op3)

        operations = registry.list_operations()
        assert len(operations) == 3
        assert "op1" in operations
        assert "op2" in operations
        assert "op3" in operations

    def test_registry_operations_maintains_insertion_order(self, registry):
        """Test that list_operations() returns names in insertion order."""

        class OpA(Operation):
            def name(self) -> str:
                return "a"

            def operand_count(self) -> int:
                return 1

            def execute(self, *args) -> float:
                return 0.0

        class OpB(Operation):
            def name(self) -> str:
                return "b"

            def operand_count(self) -> int:
                return 1

            def execute(self, *args) -> float:
                return 0.0

        class OpC(Operation):
            def name(self) -> str:
                return "c"

            def operand_count(self) -> int:
                return 1

            def execute(self, *args) -> float:
                return 0.0

        registry.register("a", OpA())
        registry.register("b", OpB())
        registry.register("c", OpC())

        assert registry.list_operations() == ["a", "b", "c"]

    def test_register_multiple_different_operations(self, registry):
        """Test registering multiple different operations."""

        class DummyOp(Operation):
            def __init__(self, op_name):
                self._name = op_name

            def name(self) -> str:
                return self._name

            def operand_count(self) -> int:
                return 1

            def execute(self, *args) -> float:
                return 0.0

        for i in range(5):
            op_name = f"op{i}"
            registry.register(op_name, DummyOp(op_name))

        assert len(registry.list_operations()) == 5
        for i in range(5):
            assert registry.is_registered(f"op{i}")

    def test_get_returns_exact_operation_instance(self, registry):
        """Test that get() returns the exact instance that was registered."""
        op = MockOperation()
        registry.register("unique", op)
        retrieved = registry.get("unique")
        assert retrieved is op  # Same object identity

    def test_is_registered_case_sensitive(self, registry):
        """Test that is_registered() is case-sensitive."""
        op = MockOperation()
        registry.register("Test", op)
        assert registry.is_registered("Test") is True
        assert registry.is_registered("test") is False
        assert registry.is_registered("TEST") is False

    def test_get_case_sensitive(self, registry):
        """Test that get() is case-sensitive."""
        op = MockOperation()
        registry.register("OpName", op)
        assert registry.get("OpName") is op
        assert registry.get("opname") is None
