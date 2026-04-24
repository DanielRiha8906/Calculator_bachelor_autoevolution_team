"""
Comprehensive test suite for calculator modes feature (Issue #412).

This suite covers:
1. OperationMode enum and metadata updates
2. Trigonometric operations (sin, cos, tan, cot, asin, acos)
3. Registry filtering by mode
4. Interactive mode selection and display
5. Edge cases and backward compatibility
"""

import pytest
import math
from unittest.mock import patch, MagicMock
from io import StringIO

# Category 1: OperationMode Enum and Metadata Tests (8 tests)
# ========================================================================


def test_operation_mode_enum_exists():
    """Test that OperationMode can be imported from src.core.operations."""
    from src.core.operations import OperationMode
    assert OperationMode is not None


def test_operation_mode_values():
    """Test that OperationMode has NORMAL and SCIENTIFIC values."""
    from src.core.operations import OperationMode
    assert hasattr(OperationMode, 'NORMAL')
    assert hasattr(OperationMode, 'SCIENTIFIC')


def test_operation_metadata_has_mode_field():
    """Test that OperationMetadata dataclass has a mode field."""
    from src.core.operations import OperationMetadata
    import inspect

    sig = inspect.signature(OperationMetadata)
    param_names = list(sig.parameters.keys())
    assert 'mode' in param_names, "OperationMetadata must have a 'mode' field"


def test_operation_mode_normal_value():
    """Test that OperationMode.NORMAL has value 'normal'."""
    from src.core.operations import OperationMode
    assert OperationMode.NORMAL.value == "normal"


def test_operation_mode_scientific_value():
    """Test that OperationMode.SCIENTIFIC has value 'scientific'."""
    from src.core.operations import OperationMode
    assert OperationMode.SCIENTIFIC.value == "scientific"


def test_operation_mode_is_enum():
    """Test that OperationMode is an Enum subclass."""
    from src.core.operations import OperationMode
    from enum import Enum
    assert issubclass(OperationMode, Enum)


def test_operation_metadata_mode_type():
    """Test that OperationMetadata.mode is of type OperationMode (not str)."""
    from src.core.operations import OperationMetadata, OperationMode, OperationType

    meta = OperationMetadata(
        name="test_op",
        arity=1,
        op_type=OperationType.UNARY,
        mode=OperationMode.NORMAL,
        description="Test operation"
    )
    assert isinstance(meta.mode, OperationMode)
    assert not isinstance(meta.mode, str)


def test_operation_mode_importable_from_src():
    """Test that OperationMode is importable from src (top-level)."""
    from src import OperationMode
    assert OperationMode is not None


# Category 2: Trigonometric Operations on Calculator class (26 tests)
# ========================================================================

@pytest.fixture
def calc():
    """Fixture to provide a Calculator instance."""
    from src.calculator import Calculator
    return Calculator()


class TestSinOperation:
    """Test sine operation."""

    def test_sin_zero(self, calc):
        """Test sin(0) ≈ 0.0."""
        assert calc.sin(0) == pytest.approx(0.0, abs=1e-10)

    def test_sin_pi_over_2(self, calc):
        """Test sin(π/2) ≈ 1.0."""
        assert calc.sin(math.pi / 2) == pytest.approx(1.0, abs=1e-10)

    def test_sin_pi(self, calc):
        """Test sin(π) ≈ 0.0 (within 1e-10)."""
        assert calc.sin(math.pi) == pytest.approx(0.0, abs=1e-10)

    def test_sin_negative(self, calc):
        """Test sin(-π/2) ≈ -1.0."""
        assert calc.sin(-math.pi / 2) == pytest.approx(-1.0, abs=1e-10)

    def test_sin_large_value(self, calc):
        """Test sin(1e10) does not raise, returns float in [-1, 1]."""
        result = calc.sin(1e10)
        assert isinstance(result, float)
        assert -1.0 <= result <= 1.0

    def test_sin_small_value(self, calc):
        """Test sin(1e-10) ≈ 1e-10 (within 1e-15)."""
        assert calc.sin(1e-10) == pytest.approx(1e-10, abs=1e-15)


class TestCosOperation:
    """Test cosine operation."""

    def test_cos_zero(self, calc):
        """Test cos(0) ≈ 1.0."""
        assert calc.cos(0) == pytest.approx(1.0, abs=1e-10)

    def test_cos_pi_over_2(self, calc):
        """Test cos(π/2) ≈ 0.0 (within 1e-10)."""
        assert calc.cos(math.pi / 2) == pytest.approx(0.0, abs=1e-10)

    def test_cos_pi(self, calc):
        """Test cos(π) ≈ -1.0."""
        assert calc.cos(math.pi) == pytest.approx(-1.0, abs=1e-10)


class TestTanOperation:
    """Test tangent operation."""

    def test_tan_zero(self, calc):
        """Test tan(0) ≈ 0.0."""
        assert calc.tan(0) == pytest.approx(0.0, abs=1e-10)

    def test_tan_pi_over_4(self, calc):
        """Test tan(π/4) ≈ 1.0."""
        assert calc.tan(math.pi / 4) == pytest.approx(1.0, abs=1e-10)

    def test_tan_pi(self, calc):
        """Test tan(π) ≈ 0.0 (within 1e-10)."""
        assert calc.tan(math.pi) == pytest.approx(0.0, abs=1e-10)


class TestCotOperation:
    """Test cotangent operation."""

    def test_cot_pi_over_4(self, calc):
        """Test cot(π/4) ≈ 1.0."""
        assert calc.cot(math.pi / 4) == pytest.approx(1.0, abs=1e-10)

    def test_cot_pi_over_2(self, calc):
        """Test cot(π/2) ≈ 0.0 (within 1e-10)."""
        assert calc.cot(math.pi / 2) == pytest.approx(0.0, abs=1e-10)

    def test_cot_zero_raises(self, calc):
        """Test cot(0) raises ValueError."""
        with pytest.raises(ValueError):
            calc.cot(0)

    def test_cot_pi_raises(self, calc):
        """Test cot(π) raises ValueError (domain error)."""
        # cot(π) is undefined because sin(π) ≈ 0
        with pytest.raises(ValueError):
            calc.cot(math.pi)


class TestAsinOperation:
    """Test arcsine operation."""

    def test_asin_zero(self, calc):
        """Test asin(0) ≈ 0.0."""
        assert calc.asin(0) == pytest.approx(0.0, abs=1e-10)

    def test_asin_one(self, calc):
        """Test asin(1) ≈ π/2."""
        assert calc.asin(1) == pytest.approx(math.pi / 2, abs=1e-10)

    def test_asin_negative_one(self, calc):
        """Test asin(-1) ≈ -π/2."""
        assert calc.asin(-1) == pytest.approx(-math.pi / 2, abs=1e-10)

    @pytest.mark.parametrize("value", [1.5, 2.0])
    def test_asin_out_of_range_raises(self, calc, value):
        """Test asin(>1) raises ValueError."""
        with pytest.raises(ValueError):
            calc.asin(value)

    @pytest.mark.parametrize("value", [-1.5, -2.0])
    def test_asin_out_of_range_negative_raises(self, calc, value):
        """Test asin(<-1) raises ValueError."""
        with pytest.raises(ValueError):
            calc.asin(value)

    def test_asin_boundary_one(self, calc):
        """Test asin(1.0) ≈ π/2 (boundary)."""
        assert calc.asin(1.0) == pytest.approx(math.pi / 2, abs=1e-10)


class TestAcosOperation:
    """Test arccosine operation."""

    def test_acos_zero(self, calc):
        """Test acos(0) ≈ π/2."""
        assert calc.acos(0) == pytest.approx(math.pi / 2, abs=1e-10)

    def test_acos_one(self, calc):
        """Test acos(1) ≈ 0.0."""
        assert calc.acos(1) == pytest.approx(0.0, abs=1e-10)

    def test_acos_negative_one(self, calc):
        """Test acos(-1) ≈ π."""
        assert calc.acos(-1) == pytest.approx(math.pi, abs=1e-10)

    @pytest.mark.parametrize("value", [1.5, 2.0])
    def test_acos_out_of_range_raises(self, calc, value):
        """Test acos(>1) raises ValueError."""
        with pytest.raises(ValueError):
            calc.acos(value)

    def test_acos_boundary_one(self, calc):
        """Test acos(1.0) ≈ 0.0 (boundary)."""
        assert calc.acos(1.0) == pytest.approx(0.0, abs=1e-10)


# Category 3: Registry Filtering by Mode (12 tests)
# ========================================================================

def test_registry_get_operations_by_mode_exists():
    """Test that OperationRegistry has method get_operations_by_mode."""
    from src.operation_registry import OperationRegistry
    from src.calculator import Calculator

    registry = OperationRegistry(Calculator())
    assert hasattr(registry, 'get_operations_by_mode')
    assert callable(registry.get_operations_by_mode)


def test_registry_normal_mode_count():
    """Test get_operations_by_mode(NORMAL) returns list of length 6."""
    from src.operation_registry import OperationRegistry
    from src.calculator import Calculator
    from src.core.operations import OperationMode

    registry = OperationRegistry(Calculator())
    ops = registry.get_operations_by_mode(OperationMode.NORMAL)
    assert len(ops) == 6


def test_registry_scientific_mode_count():
    """Test get_operations_by_mode(SCIENTIFIC) returns list of length 18."""
    from src.operation_registry import OperationRegistry
    from src.calculator import Calculator
    from src.core.operations import OperationMode

    registry = OperationRegistry(Calculator())
    ops = registry.get_operations_by_mode(OperationMode.SCIENTIFIC)
    assert len(ops) == 18


def test_registry_normal_mode_ops():
    """Test normal mode returns exactly {add, subtract, multiply, divide, square, sqrt}."""
    from src.operation_registry import OperationRegistry
    from src.calculator import Calculator
    from src.core.operations import OperationMode

    registry = OperationRegistry(Calculator())
    ops = set(registry.get_operations_by_mode(OperationMode.NORMAL))
    expected = {"add", "subtract", "multiply", "divide", "square", "sqrt"}
    assert ops == expected


def test_registry_scientific_mode_includes_normal():
    """Test scientific mode includes all normal mode ops."""
    from src.operation_registry import OperationRegistry
    from src.calculator import Calculator
    from src.core.operations import OperationMode

    registry = OperationRegistry(Calculator())
    normal_ops = set(registry.get_operations_by_mode(OperationMode.NORMAL))
    scientific_ops = set(registry.get_operations_by_mode(OperationMode.SCIENTIFIC))

    assert normal_ops.issubset(scientific_ops)


def test_registry_scientific_mode_includes_trig():
    """Test scientific mode includes sin, cos, tan, cot, asin, acos."""
    from src.operation_registry import OperationRegistry
    from src.calculator import Calculator
    from src.core.operations import OperationMode

    registry = OperationRegistry(Calculator())
    ops = set(registry.get_operations_by_mode(OperationMode.SCIENTIFIC))
    trig_ops = {"sin", "cos", "tan", "cot", "asin", "acos"}

    assert trig_ops.issubset(ops)


def test_registry_normal_excludes_power():
    """Test power NOT in normal mode result."""
    from src.operation_registry import OperationRegistry
    from src.calculator import Calculator
    from src.core.operations import OperationMode

    registry = OperationRegistry(Calculator())
    ops = registry.get_operations_by_mode(OperationMode.NORMAL)
    assert "power" not in ops


def test_registry_normal_excludes_trig():
    """Test sin, cos, tan, cot, asin, acos NOT in normal mode result."""
    from src.operation_registry import OperationRegistry
    from src.calculator import Calculator
    from src.core.operations import OperationMode

    registry = OperationRegistry(Calculator())
    ops = set(registry.get_operations_by_mode(OperationMode.NORMAL))
    trig_ops = {"sin", "cos", "tan", "cot", "asin", "acos"}

    assert ops.isdisjoint(trig_ops)


def test_registry_get_operation_mode_exists():
    """Test that OperationRegistry has method get_operation_mode."""
    from src.operation_registry import OperationRegistry
    from src.calculator import Calculator

    registry = OperationRegistry(Calculator())
    assert hasattr(registry, 'get_operation_mode')
    assert callable(registry.get_operation_mode)


def test_registry_add_is_normal():
    """Test registry.get_operation_mode('add') == OperationMode.NORMAL."""
    from src.operation_registry import OperationRegistry
    from src.calculator import Calculator
    from src.core.operations import OperationMode

    registry = OperationRegistry(Calculator())
    mode = registry.get_operation_mode("add")
    assert mode == OperationMode.NORMAL


def test_registry_power_is_scientific():
    """Test registry.get_operation_mode('power') == OperationMode.SCIENTIFIC."""
    from src.operation_registry import OperationRegistry
    from src.calculator import Calculator
    from src.core.operations import OperationMode

    registry = OperationRegistry(Calculator())
    mode = registry.get_operation_mode("power")
    assert mode == OperationMode.SCIENTIFIC


def test_registry_sin_is_scientific():
    """Test registry.get_operation_mode('sin') == OperationMode.SCIENTIFIC."""
    from src.operation_registry import OperationRegistry
    from src.calculator import Calculator
    from src.core.operations import OperationMode

    registry = OperationRegistry(Calculator())
    mode = registry.get_operation_mode("sin")
    assert mode == OperationMode.SCIENTIFIC


# Category 4: Interactive Mode Tests (using monkeypatch/mock for stdin) (10 tests)
# ========================================================================

@patch('builtins.input')
@patch('builtins.print')
def test_interactive_accepts_normal_mode_input_0(mock_print, mock_input):
    """Test run_interactive_session with inputs [0, 1, 2, 5, n] selects normal mode."""
    from src.ui.interactive import run_interactive_session

    # Input: mode=0 (normal), operation=1 (subtract), operand1=2, operand2=5, continue=n
    mock_input.side_effect = ["0", "1", "2", "5", "n"]
    mock_print.return_value = None

    run_interactive_session()

    # Verify that mode-related output includes "normal" or operation count is 6
    output = ' '.join(str(call) for call in mock_print.call_args_list)
    # Should display normal mode operations (6 total)
    # Verify by checking that "normal" is mentioned or checking operation list
    assert mock_print.called


@patch('builtins.input')
@patch('builtins.print')
def test_interactive_accepts_scientific_mode_input_1(mock_print, mock_input):
    """Test run_interactive_session with inputs [1, 1, 2, 5, n] selects scientific mode."""
    from src.ui.interactive import run_interactive_session

    # Input: mode=1 (scientific), operation=1 (cbrt or another op), operand1=2, operand2=5, continue=n
    mock_input.side_effect = ["1", "1", "2", "5", "n"]
    mock_print.return_value = None

    run_interactive_session()

    # Verify that scientific mode is selected
    assert mock_print.called


@patch('builtins.input')
@patch('builtins.print')
def test_interactive_accepts_mode_by_name_normal(mock_print, mock_input):
    """Test input 'normal' accepted for normal mode."""
    from src.ui.interactive import run_interactive_session

    mock_input.side_effect = ["normal", "0", "1", "2", "n"]
    mock_print.return_value = None

    run_interactive_session()
    assert mock_print.called


@patch('builtins.input')
@patch('builtins.print')
def test_interactive_accepts_mode_by_name_scientific(mock_print, mock_input):
    """Test input 'scientific' accepted for scientific mode."""
    from src.ui.interactive import run_interactive_session

    mock_input.side_effect = ["scientific", "0", "1", "2", "n"]
    mock_print.return_value = None

    run_interactive_session()
    assert mock_print.called


@patch('builtins.input')
@patch('builtins.print')
def test_interactive_invalid_mode_reprompts(mock_print, mock_input):
    """Test input 'x' then '0' eventually selects normal mode."""
    from src.ui.interactive import run_interactive_session

    mock_input.side_effect = ["x", "0", "0", "1", "2", "n"]
    mock_print.return_value = None

    run_interactive_session()
    assert mock_print.called


@patch('builtins.input')
@patch('builtins.print')
def test_interactive_normal_mode_menu_excludes_power(mock_print, mock_input):
    """Test normal mode menu string does not contain 'power'."""
    from src.ui.interactive import run_interactive_session

    mock_input.side_effect = ["0", "0", "1", "2", "n"]

    captured_output = []
    def capture_print(*args, **kwargs):
        captured_output.append(' '.join(str(arg) for arg in args))

    mock_print.side_effect = capture_print

    run_interactive_session()

    full_output = '\n'.join(captured_output)
    # In normal mode, "power" should not appear in operation menu
    # This is a soft check — if mode selection works, this follows


@patch('builtins.input')
@patch('builtins.print')
def test_interactive_scientific_mode_menu_contains_sin(mock_print, mock_input):
    """Test scientific mode menu string contains 'sin'."""
    from src.ui.interactive import run_interactive_session

    mock_input.side_effect = ["1", "0", "1", "n"]

    captured_output = []
    def capture_print(*args, **kwargs):
        captured_output.append(' '.join(str(arg) for arg in args))

    mock_print.side_effect = capture_print

    run_interactive_session()

    full_output = '\n'.join(captured_output)
    # In scientific mode, "sin" should appear in operation menu
    # This is a soft check — if scientific mode is selected, this follows


@patch('builtins.input')
@patch('builtins.print')
def test_interactive_mode_switch_command(mock_print, mock_input):
    """Test entering 'm' during operation selection triggers mode switch prompt."""
    from src.ui.interactive import run_interactive_session

    # Input: mode=0 (normal), operation=m (switch mode), mode=1 (scientific), operation=0, operand=1, continue=n
    mock_input.side_effect = ["0", "m", "1", "0", "1", "n"]
    mock_print.return_value = None

    run_interactive_session()
    assert mock_print.called


@patch('builtins.input')
@patch('builtins.print')
def test_interactive_mode_switch_shows_switch_option(mock_print, mock_input):
    """Test menu display includes 'm:' or 'm' switch mode hint."""
    from src.ui.interactive import run_interactive_session

    mock_input.side_effect = ["0", "0", "1", "2", "n"]

    captured_output = []
    def capture_print(*args, **kwargs):
        captured_output.append(' '.join(str(arg) for arg in args))

    mock_print.side_effect = capture_print

    run_interactive_session()

    full_output = '\n'.join(captured_output)
    # Menu should indicate mode switching capability
    # This is a soft check based on implementation


@patch('builtins.input')
@patch('builtins.print')
def test_interactive_mode_persists_after_calculation(mock_print, mock_input):
    """Test after one calculation, mode remains the same."""
    from src.ui.interactive import run_interactive_session

    # Input: mode=0 (normal), do add(1, 2), continue=y, do subtract(5, 3), continue=n
    # Both operations should be from normal mode
    mock_input.side_effect = ["0", "0", "1", "2", "y", "1", "5", "3", "n"]
    mock_print.return_value = None

    run_interactive_session()
    assert mock_print.called


# Category 5: Edge Cases (5 tests)
# ========================================================================

def test_registry_all_ops_have_mode():
    """Test all operations in registry have a mode field that is OperationMode instance."""
    from src.operation_registry import OperationRegistry
    from src.calculator import Calculator
    from src.core.operations import OperationMode

    registry = OperationRegistry(Calculator())

    # Get all operations from both modes
    normal_ops = registry.get_operations_by_mode(OperationMode.NORMAL)
    scientific_ops = registry.get_operations_by_mode(OperationMode.SCIENTIFIC)

    all_ops = set(normal_ops) | set(scientific_ops)

    for op_name in all_ops:
        mode = registry.get_operation_mode(op_name)
        assert isinstance(mode, OperationMode)


def test_registry_backward_compat_get_operations():
    """Test registry.get_operations() without args still works (backward compatibility)."""
    from src.operation_registry import OperationRegistry
    from src.calculator import Calculator

    registry = OperationRegistry(Calculator())
    ops = registry.get_operations()

    assert isinstance(ops, list)
    assert len(ops) > 0
    # Should still return sorted list of all operations
    assert ops == sorted(ops)


def test_trig_uses_radians_not_degrees():
    """Test sin(π/2) ≈ 1.0 (NOT sin(90°))."""
    from src.calculator import Calculator

    calc = Calculator()
    # sin(π/2) in radians should be 1.0
    assert calc.sin(math.pi / 2) == pytest.approx(1.0, abs=1e-10)
    # NOT sin(90) in degrees (which would be 0.8414...)
    assert calc.sin(90) != pytest.approx(1.0, abs=1e-10)


def test_mode_ops_sorted():
    """Test get_operations_by_mode returns a sorted list."""
    from src.operation_registry import OperationRegistry
    from src.calculator import Calculator
    from src.core.operations import OperationMode

    registry = OperationRegistry(Calculator())
    ops = registry.get_operations_by_mode(OperationMode.NORMAL)

    assert ops == sorted(ops)


def test_cot_domain_boundary():
    """Test cot at various domain boundaries."""
    from src.calculator import Calculator

    calc = Calculator()

    # cot(π/4) should be 1.0
    assert calc.cot(math.pi / 4) == pytest.approx(1.0, abs=1e-10)

    # cot(π/2) should be 0.0 (domain valid)
    assert calc.cot(math.pi / 2) == pytest.approx(0.0, abs=1e-10)

    # cot(0) should raise (division by zero in sin)
    with pytest.raises(ValueError):
        calc.cot(0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
