"""Unit tests for OperationRegistry mode-related methods."""

import pytest
import math
from src.calculator import Calculator
from src.operations import OperationRegistry
from src.mode_manager import CalculatorMode, ModeManager


class TestGetScientificOperations:
    """Test suite for OperationRegistry.get_scientific_operations() method."""

    @pytest.fixture
    def registry(self):
        """Fixture to provide a fresh OperationRegistry instance."""
        calculator = Calculator()
        return OperationRegistry(calculator)

    def test_get_scientific_operations_returns_set(self, registry):
        """Test that get_scientific_operations returns a set."""
        result = registry.get_scientific_operations()
        assert isinstance(result, set)

    def test_get_scientific_operations_contains_sin_cos_tan(self, registry):
        """Test that get_scientific_operations includes sin, cos, tan."""
        sci_ops = registry.get_scientific_operations()
        assert "sin" in sci_ops
        assert "cos" in sci_ops
        assert "tan" in sci_ops

    def test_get_scientific_operations_exact_set(self, registry):
        """Test that get_scientific_operations returns exactly sin, cos, tan."""
        sci_ops = registry.get_scientific_operations()
        assert sci_ops == {"sin", "cos", "tan"}

    def test_get_scientific_operations_does_not_include_normal_ops(self, registry):
        """Test that normal operations are not in scientific operations set."""
        sci_ops = registry.get_scientific_operations()
        assert "add" not in sci_ops
        assert "subtract" not in sci_ops
        assert "multiply" not in sci_ops
        assert "divide" not in sci_ops
        assert "log" not in sci_ops
        assert "ln" not in sci_ops
        assert "factorial" not in sci_ops
        assert "square" not in sci_ops

    def test_get_scientific_operations_returns_copy_not_reference(self, registry):
        """Test that get_scientific_operations returns a copy, not internal set."""
        sci_ops1 = registry.get_scientific_operations()
        sci_ops1.add("custom")
        sci_ops2 = registry.get_scientific_operations()
        assert sci_ops2 == {"sin", "cos", "tan"}
        assert "custom" not in sci_ops2


class TestRegisterScientific:
    """Test suite for OperationRegistry.register_scientific() method."""

    @pytest.fixture
    def registry(self):
        """Fixture to provide a fresh OperationRegistry instance."""
        calculator = Calculator()
        return OperationRegistry(calculator)

    def test_register_scientific_adds_to_scientific_operations(self, registry):
        """Test that register_scientific adds operation to scientific set."""
        def custom_op(x):
            return x + 10

        initial_sci_ops = registry.get_scientific_operations()
        assert "custom" not in initial_sci_ops

        registry.register_scientific(
            key="custom",
            method=custom_op,
            arity=1,
            description="Custom operation"
        )

        new_sci_ops = registry.get_scientific_operations()
        assert "custom" in new_sci_ops

    def test_register_scientific_adds_to_registry(self, registry):
        """Test that register_scientific adds operation to main registry."""
        def custom_op(x):
            return x + 10

        registry.register_scientific(
            key="custom",
            method=custom_op,
            arity=1,
            description="Custom operation"
        )

        method, arity, description = registry.get_operation("custom")
        assert method is custom_op
        assert arity == 1

    def test_register_scientific_duplicate_key_raises_value_error(self, registry):
        """Test that registering duplicate scientific key raises ValueError."""
        def custom_op(x):
            return x + 10

        registry.register_scientific(
            key="custom",
            method=custom_op,
            arity=1,
            description="Custom operation"
        )

        with pytest.raises(ValueError, match="already registered"):
            registry.register_scientific(
                key="custom",
                method=custom_op,
                arity=1,
                description="Duplicate"
            )

    def test_register_scientific_sin_already_exists(self, registry):
        """Test that attempting to re-register sin raises ValueError."""
        def new_sin(x):
            return 0.0

        with pytest.raises(ValueError):
            registry.register_scientific(
                key="sin",
                method=new_sin,
                arity=1,
                description="New sine"
            )

    def test_register_scientific_with_non_callable_raises_type_error(self, registry):
        """Test that register_scientific raises TypeError for non-callable."""
        with pytest.raises(TypeError, match="'method' must be callable"):
            registry.register_scientific(
                key="bad_op",
                method="not_callable",
                arity=1,
                description="Bad operation"
            )

    def test_register_scientific_with_invalid_arity_raises_value_error(self, registry):
        """Test that register_scientific raises ValueError for invalid arity."""
        def custom_op(x):
            return x

        with pytest.raises(ValueError, match="'arity' must be a positive integer"):
            registry.register_scientific(
                key="bad_arity",
                method=custom_op,
                arity=0,
                description="Bad arity"
            )


class TestGetAvailableOperations:
    """Test suite for OperationRegistry.get_available_operations() method."""

    @pytest.fixture
    def registry(self):
        """Fixture to provide a fresh OperationRegistry instance."""
        calculator = Calculator()
        return OperationRegistry(calculator)

    def test_get_available_operations_with_none_returns_all_normal(self, registry):
        """Test that get_available_operations(None) returns all normal operations."""
        ops = registry.get_available_operations(mode_manager=None)
        # Should return only normal operations (not scientific)
        assert len(ops) == 12
        assert "add" in ops
        assert "sin" not in ops
        assert "cos" not in ops
        assert "tan" not in ops

    def test_get_available_operations_normal_mode_excludes_scientific(self, registry):
        """Test that NORMAL mode excludes scientific operations."""
        manager = ModeManager()
        assert manager.get_current_mode() is CalculatorMode.NORMAL
        ops = registry.get_available_operations(manager)
        assert "sin" not in ops
        assert "cos" not in ops
        assert "tan" not in ops
        assert "add" in ops
        assert len(ops) == 12

    def test_get_available_operations_scientific_mode_includes_all(self, registry):
        """Test that SCIENTIFIC mode includes all operations."""
        manager = ModeManager()
        manager.switch_mode()
        assert manager.get_current_mode() is CalculatorMode.SCIENTIFIC
        ops = registry.get_available_operations(manager)
        assert "sin" in ops
        assert "cos" in ops
        assert "tan" in ops
        assert "add" in ops
        assert len(ops) == 15

    def test_get_available_operations_returns_dict(self, registry):
        """Test that get_available_operations returns a dictionary."""
        manager = ModeManager()
        result = registry.get_available_operations(manager)
        assert isinstance(result, dict)

    def test_get_available_operations_values_are_descriptions(self, registry):
        """Test that dict values are operation descriptions."""
        manager = ModeManager()
        ops = registry.get_available_operations(manager)
        for key, description in ops.items():
            assert isinstance(description, str)
            assert len(description) > 0

    def test_get_available_operations_switches_between_modes(self, registry):
        """Test get_available_operations when mode is switched."""
        manager = ModeManager()
        normal_ops = registry.get_available_operations(manager)
        assert "sin" not in normal_ops
        assert len(normal_ops) == 12

        manager.switch_mode()
        scientific_ops = registry.get_available_operations(manager)
        assert "sin" in scientific_ops
        assert len(scientific_ops) == 15


class TestListOperationsExcludesScientific:
    """Test suite verifying list_operations() excludes scientific operations."""

    @pytest.fixture
    def registry(self):
        """Fixture to provide a fresh OperationRegistry instance."""
        calculator = Calculator()
        return OperationRegistry(calculator)

    def test_list_operations_excludes_sin(self, registry):
        """Test that list_operations does not include sin."""
        ops = registry.list_operations()
        assert "sin" not in ops

    def test_list_operations_excludes_cos(self, registry):
        """Test that list_operations does not include cos."""
        ops = registry.list_operations()
        assert "cos" not in ops

    def test_list_operations_excludes_tan(self, registry):
        """Test that list_operations does not include tan."""
        ops = registry.list_operations()
        assert "tan" not in ops

    def test_list_operations_returns_exactly_12_operations(self, registry):
        """Test that list_operations returns exactly 12 (non-scientific) operations."""
        ops = registry.list_operations()
        assert len(ops) == 12

    def test_list_operations_includes_normal_operations(self, registry):
        """Test that list_operations includes all normal operations."""
        ops = registry.list_operations()
        normal_ops = {"add", "subtract", "multiply", "divide", "power",
                      "factorial", "square", "cube", "square_root", "cube_root",
                      "log", "ln"}
        assert set(ops.keys()) == normal_ops


class TestScientificOperationsFunctionality:
    """Test suite for scientific operations' actual functionality."""

    @pytest.fixture
    def registry(self):
        """Fixture to provide a fresh OperationRegistry instance."""
        calculator = Calculator()
        return OperationRegistry(calculator)

    def test_sin_operation_90_degrees(self, registry):
        """Test that sin(90) returns approximately 1.0."""
        sin_method, _, _ = registry.get_operation("sin")
        result = sin_method(90)
        assert abs(result - 1.0) < 1e-9

    def test_sin_operation_0_degrees(self, registry):
        """Test that sin(0) returns approximately 0.0."""
        sin_method, _, _ = registry.get_operation("sin")
        result = sin_method(0)
        assert abs(result - 0.0) < 1e-9

    def test_sin_operation_45_degrees(self, registry):
        """Test that sin(45) returns approximately sqrt(2)/2."""
        sin_method, _, _ = registry.get_operation("sin")
        result = sin_method(45)
        expected = math.sqrt(2) / 2
        assert abs(result - expected) < 1e-9

    def test_cos_operation_0_degrees(self, registry):
        """Test that cos(0) returns approximately 1.0."""
        cos_method, _, _ = registry.get_operation("cos")
        result = cos_method(0)
        assert abs(result - 1.0) < 1e-9

    def test_cos_operation_90_degrees(self, registry):
        """Test that cos(90) returns approximately 0.0."""
        cos_method, _, _ = registry.get_operation("cos")
        result = cos_method(90)
        assert abs(result - 0.0) < 1e-9

    def test_cos_operation_60_degrees(self, registry):
        """Test that cos(60) returns approximately 0.5."""
        cos_method, _, _ = registry.get_operation("cos")
        result = cos_method(60)
        assert abs(result - 0.5) < 1e-9

    def test_tan_operation_45_degrees(self, registry):
        """Test that tan(45) returns approximately 1.0."""
        tan_method, _, _ = registry.get_operation("tan")
        result = tan_method(45)
        assert abs(result - 1.0) < 1e-9

    def test_tan_operation_0_degrees(self, registry):
        """Test that tan(0) returns approximately 0.0."""
        tan_method, _, _ = registry.get_operation("tan")
        result = tan_method(0)
        assert abs(result - 0.0) < 1e-9

    def test_sin_has_arity_1(self, registry):
        """Test that sin has arity of 1."""
        _, arity, _ = registry.get_operation("sin")
        assert arity == 1

    def test_cos_has_arity_1(self, registry):
        """Test that cos has arity of 1."""
        _, arity, _ = registry.get_operation("cos")
        assert arity == 1

    def test_tan_has_arity_1(self, registry):
        """Test that tan has arity of 1."""
        _, arity, _ = registry.get_operation("tan")
        assert arity == 1

    def test_scientific_operations_accept_negative_degrees(self, registry):
        """Test that scientific operations accept negative degree values."""
        sin_method, _, _ = registry.get_operation("sin")
        result = sin_method(-90)
        assert abs(result - (-1.0)) < 1e-9

    def test_scientific_operations_accept_large_degree_values(self, registry):
        """Test that scientific operations accept values > 360 degrees."""
        sin_method, _, _ = registry.get_operation("sin")
        result1 = sin_method(450)  # 450 = 360 + 90
        result2 = sin_method(90)
        assert abs(result1 - result2) < 1e-9
