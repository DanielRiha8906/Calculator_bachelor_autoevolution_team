"""Test suite for tkinter GUI feature (CalculatorMode and CalculatorApp).

Tests cover:
- CalculatorMode abstract base class and concrete subclasses (SimpleMode, ScientificMode)
- CalculatorApp tkinter class with dependency injection
- Mode switching and operation filtering
- Calculation and error handling in GUI context
- History tracking within the app
- Unary vs binary operation classification
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

from src.calculator import Calculator
from src.operation_registry import OperationRegistry
from src.core.operations import OperationMode


class TestCalculatorModeAbstract:
    """Test CalculatorMode base class and abstract interface."""

    def test_calculator_mode_base_class_abstract(self):
        """CalculatorMode cannot be instantiated directly — raises TypeError."""
        with pytest.raises(TypeError):
            from src.ui.modes import CalculatorMode
            CalculatorMode()


class TestSimpleMode:
    """Test SimpleMode concrete implementation."""

    def test_simple_mode_returns_six_operations(self):
        """SimpleMode.get_operations(registry) returns exactly 6 operations."""
        from src.ui.modes import SimpleMode

        calc = Calculator()
        registry = OperationRegistry(calc)
        mode = SimpleMode()

        ops = mode.get_operations(registry)
        assert len(ops) == 6

    def test_simple_mode_operations_exact_set(self):
        """SimpleMode returns specifically: add, subtract, multiply, divide, square, sqrt."""
        from src.ui.modes import SimpleMode

        calc = Calculator()
        registry = OperationRegistry(calc)
        mode = SimpleMode()

        ops = set(mode.get_operations(registry))
        expected = {"add", "subtract", "multiply", "divide", "square", "sqrt"}
        assert ops == expected

    def test_simple_mode_is_subset_of_scientific(self):
        """All simple mode ops are in scientific mode."""
        from src.ui.modes import SimpleMode, ScientificMode

        calc = Calculator()
        registry = OperationRegistry(calc)
        simple = SimpleMode()
        scientific = ScientificMode()

        simple_ops = set(simple.get_operations(registry))
        scientific_ops = set(scientific.get_operations(registry))

        assert simple_ops.issubset(scientific_ops)


class TestScientificMode:
    """Test ScientificMode concrete implementation."""

    def test_scientific_mode_returns_eighteen_operations(self):
        """ScientificMode.get_operations(registry) returns 18 operations including trigonometric functions."""
        from src.ui.modes import ScientificMode

        calc = Calculator()
        registry = OperationRegistry(calc)
        mode = ScientificMode()

        ops = mode.get_operations(registry)
        assert len(ops) == 18

    def test_scientific_mode_includes_advanced_ops(self):
        """ScientificMode includes power, factorial, cube, cbrt, ln, log10, sin, cos, tan, cot, asin, acos."""
        from src.ui.modes import ScientificMode

        calc = Calculator()
        registry = OperationRegistry(calc)
        mode = ScientificMode()

        ops = set(mode.get_operations(registry))
        required = {"power", "factorial", "cube", "cbrt", "ln", "log10", "sin", "cos", "tan", "cot", "asin", "acos"}
        assert required.issubset(ops)


class TestScientificModeTrigonometry:
    """Test that ScientificMode exposes all 6 trigonometric functions."""

    def test_scientific_mode_includes_all_trig_functions(self):
        """ScientificMode.get_operations() includes sin, cos, tan, cot, asin, acos."""
        from src.ui.modes import ScientificMode

        calc = Calculator()
        registry = OperationRegistry(calc)
        mode = ScientificMode()

        ops = set(mode.get_operations(registry))
        trig = {"sin", "cos", "tan", "cot", "asin", "acos"}
        assert trig.issubset(ops)


class TestCalculatorAppInstantiation:
    """Test CalculatorApp instantiation and dependency injection."""

    @patch('src.ui.gui.tk.Tk')
    def test_calculator_app_instantiates_with_mocked_root(self, mock_tk_class):
        """CalculatorApp(root=mock_root) creates without error."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        assert app is not None

    @patch('src.ui.gui.tk.Tk')
    def test_calculator_app_creates_calculator_if_none(self, mock_tk_class):
        """CalculatorApp creates Calculator internally when not provided."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root, calculator=None)
        assert app._calculator is not None

    @patch('src.ui.gui.tk.Tk')
    def test_calculator_app_accepts_custom_calculator(self, mock_tk_class):
        """CalculatorApp accepts Calculator instance."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        custom_calc = Calculator()
        app = CalculatorApp(root=mock_root, calculator=custom_calc)
        assert app._calculator is custom_calc

    @patch('src.ui.gui.tk.Tk')
    def test_calculator_app_accepts_custom_registry(self, mock_tk_class):
        """CalculatorApp accepts OperationRegistry instance."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        calc = Calculator()
        custom_registry = OperationRegistry(calc)
        app = CalculatorApp(root=mock_root, calculator=calc, registry=custom_registry)
        assert app._registry is custom_registry


class TestCalculatorAppModeManagement:
    """Test CalculatorApp mode switching and operation filtering."""

    @patch('src.ui.gui.tk.Tk')
    def test_app_starts_in_simple_mode(self, mock_tk_class):
        """App starts in simple mode by default."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        assert app._current_mode == OperationMode.NORMAL

    @patch('src.ui.gui.tk.Tk')
    def test_app_get_current_mode_operations_simple(self, mock_tk_class):
        """App returns 6 ops in simple mode."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        ops = app.get_current_mode_operations()
        assert len(ops) == 6

    @patch('src.ui.gui.tk.Tk')
    def test_app_switch_to_scientific_mode(self, mock_tk_class):
        """Mode switch updates to 18 ops including trigonometric functions."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.switch_mode(OperationMode.SCIENTIFIC)

        assert app._current_mode == OperationMode.SCIENTIFIC
        ops = app.get_current_mode_operations()
        assert len(ops) == 18

    @patch('src.ui.gui.tk.Tk')
    def test_app_switch_back_to_simple_mode(self, mock_tk_class):
        """Mode can switch back to simple."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.switch_mode(OperationMode.SCIENTIFIC)
        app.switch_mode(OperationMode.NORMAL)

        assert app._current_mode == OperationMode.NORMAL
        ops = app.get_current_mode_operations()
        assert len(ops) == 6

    @patch('src.ui.gui.tk.Tk')
    def test_app_scientific_mode_contains_trig_operations(self, mock_tk_class):
        """After switching to scientific mode, trig ops are available."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.switch_mode(OperationMode.SCIENTIFIC)
        ops = set(app.get_current_mode_operations())
        trig = {"sin", "cos", "tan", "cot", "asin", "acos"}
        assert trig.issubset(ops)

    @patch('src.ui.gui.tk.Tk')
    def test_app_switch_back_to_simple_hides_trig(self, mock_tk_class):
        """After switching back to simple mode, trig ops are gone."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.switch_mode(OperationMode.SCIENTIFIC)
        app.switch_mode(OperationMode.NORMAL)
        ops = set(app.get_current_mode_operations())
        trig = {"sin", "cos", "tan", "cot"}
        assert trig.isdisjoint(ops)


class TestCalculatorAppCalculations:
    """Test CalculatorApp calculation and result display."""

    @patch('src.ui.gui.tk.Tk')
    def test_app_calculate_add_binary(self, mock_tk_class):
        """calculate("add", 5, 3) returns "8" or displays "8"."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        result = app.calculate("add", 5, 3)
        assert result == "8" or "8" in str(result)

    @patch('src.ui.gui.tk.Tk')
    def test_app_calculate_square_unary(self, mock_tk_class):
        """calculate("square", 4) returns "16" or displays "16"."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        result = app.calculate("square", 4)
        assert result == "16" or "16" in str(result)

    @patch('src.ui.gui.tk.Tk')
    def test_app_calculate_divide_by_zero(self, mock_tk_class):
        """calculate("divide", 5, 0) returns error string, not crash."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        result = app.calculate("divide", 5, 0)

        # Should not raise exception; should return error message
        assert isinstance(result, str)
        assert "error" in result.lower() or "division" in result.lower()

    @patch('src.ui.gui.tk.Tk')
    def test_app_calculate_sqrt_negative(self, mock_tk_class):
        """calculate("sqrt", -4) returns error string, not crash."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        result = app.calculate("sqrt", -4)

        # Should not raise exception; should return error message
        assert isinstance(result, str)
        assert "error" in result.lower()

    @patch('src.ui.gui.tk.Tk')
    def test_app_calculate_invalid_operand_string(self, mock_tk_class):
        """calculate with non-numeric input returns error, not crash."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        # Pass invalid operand type
        result = app.calculate("add", "not_a_number", 5)

        # Should not raise exception; should return error message
        assert isinstance(result, str)
        assert "error" in result.lower()

    @patch('src.ui.gui.tk.Tk')
    def test_app_calculate_factorial_scientific(self, mock_tk_class):
        """calculate("factorial", 5) returns 120 (only available in scientific mode)."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.switch_mode(OperationMode.SCIENTIFIC)

        result = app.calculate("factorial", 5)
        assert result == "120" or "120" in str(result)

    @patch('src.ui.gui.tk.Tk')
    def test_app_calculate_power_scientific(self, mock_tk_class):
        """calculate("power", 2, 3) returns 8 (scientific mode)."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.switch_mode(OperationMode.SCIENTIFIC)

        result = app.calculate("power", 2, 3)
        assert result == "8" or "8" in str(result)

    @patch('src.ui.gui.tk.Tk')
    def test_app_calculate_float_operands(self, mock_tk_class):
        """calculate("add", 1.5, 2.5) returns 4.0."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        result = app.calculate("add", 1.5, 2.5)
        assert result == "4.0" or "4.0" in str(result)


class TestTrigonometryCalculations:
    """Test trigonometric function calculations in the GUI."""

    @patch('src.ui.gui.tk.Tk')
    def test_app_calculate_sin(self, mock_tk_class):
        """calculate('sin', '0') returns ~0.0."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        result = app.calculate('sin', '0')
        assert float(result) == pytest.approx(0.0, abs=1e-9)

    @patch('src.ui.gui.tk.Tk')
    def test_app_calculate_cos(self, mock_tk_class):
        """calculate('cos', '0') returns ~1.0."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        result = app.calculate('cos', '0')
        assert float(result) == pytest.approx(1.0, abs=1e-9)

    @patch('src.ui.gui.tk.Tk')
    def test_app_calculate_asin(self, mock_tk_class):
        """calculate('asin', '0.5') returns ~0.5236."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        result = app.calculate('asin', '0.5')
        assert float(result) == pytest.approx(0.5236, abs=0.001)

    @patch('src.ui.gui.tk.Tk')
    def test_app_calculate_acos(self, mock_tk_class):
        """calculate('acos', '0.5') returns ~1.047."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        result = app.calculate('acos', '0.5')
        assert float(result) == pytest.approx(1.047, abs=0.001)


class TestCalculatorAppHistory:
    """Test CalculatorApp history tracking."""

    @patch('src.ui.gui.tk.Tk')
    def test_app_history_empty_on_start(self, mock_tk_class):
        """App.get_history() returns empty list initially."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        history = app.get_history()
        assert history == []

    @patch('src.ui.gui.tk.Tk')
    def test_app_history_records_successful_op(self, mock_tk_class):
        """After calculate("add", 2, 3), history has 1 entry."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.calculate("add", 2, 3)

        history = app.get_history()
        assert len(history) == 1

    @patch('src.ui.gui.tk.Tk')
    def test_app_history_records_multiple_ops(self, mock_tk_class):
        """After multiple calculates, history has correct count."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.calculate("add", 2, 3)
        app.calculate("multiply", 4, 5)
        app.calculate("square", 3)

        history = app.get_history()
        assert len(history) == 3

    @patch('src.ui.gui.tk.Tk')
    def test_app_history_not_cleared_on_mode_switch(self, mock_tk_class):
        """Switching mode preserves history."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.calculate("add", 2, 3)

        app.switch_mode(OperationMode.SCIENTIFIC)

        history = app.get_history()
        assert len(history) == 1

    @patch('src.ui.gui.tk.Tk')
    def test_app_history_entry_contains_operation(self, mock_tk_class):
        """History entry for add(2, 3)=5 contains expected info."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.calculate("add", 2, 3)

        history = app.get_history()
        entry = history[0]

        # Entry should contain operation name, operands, and result
        assert "add" in entry.lower()
        assert "2" in entry or "3" in entry or "5" in entry


class TestCalculatorAppOperationClassification:
    """Test CalculatorApp classification of unary vs binary operations."""

    @patch('src.ui.gui.tk.Tk')
    def test_app_is_unary_operation(self, mock_tk_class):
        """square, sqrt, factorial, ln, log10, cube, cbrt are unary."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.switch_mode(OperationMode.SCIENTIFIC)

        unary_ops = ["square", "sqrt", "factorial", "ln", "log10", "cube", "cbrt"]
        for op in unary_ops:
            is_unary = app.is_unary_operation(op)
            assert is_unary, f"{op} should be unary"

    @patch('src.ui.gui.tk.Tk')
    def test_app_is_binary_operation(self, mock_tk_class):
        """add, subtract, multiply, divide, power are binary."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.switch_mode(OperationMode.SCIENTIFIC)

        binary_ops = ["add", "subtract", "multiply", "divide", "power"]
        for op in binary_ops:
            is_binary = not app.is_unary_operation(op)
            assert is_binary, f"{op} should be binary"


class TestTrigonometryUnaryClassification:
    """Test that trig functions are classified as unary operations."""

    @patch('src.ui.gui.tk.Tk')
    def test_app_is_unary_sin(self, mock_tk_class):
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        assert app.is_unary_operation('sin') is True

    @patch('src.ui.gui.tk.Tk')
    def test_app_is_unary_cos(self, mock_tk_class):
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        assert app.is_unary_operation('cos') is True

    @patch('src.ui.gui.tk.Tk')
    def test_app_is_unary_tan(self, mock_tk_class):
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        assert app.is_unary_operation('tan') is True

    @patch('src.ui.gui.tk.Tk')
    def test_app_is_unary_cot(self, mock_tk_class):
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        assert app.is_unary_operation('cot') is True

    @patch('src.ui.gui.tk.Tk')
    def test_app_is_unary_asin(self, mock_tk_class):
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        assert app.is_unary_operation('asin') is True

    @patch('src.ui.gui.tk.Tk')
    def test_app_is_unary_acos(self, mock_tk_class):
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        assert app.is_unary_operation('acos') is True


class TestCalculatorAppRunMethod:
    """Test CalculatorApp run method."""

    @patch('src.ui.gui.tk.Tk')
    def test_app_run_method_exists(self, mock_tk_class):
        """App has a run() method."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        assert hasattr(app, "run")
        assert callable(app.run)


class TestModeSwitchingBehavior:
    """Test mode-switching behavior after fix to _rebuild_operation_menu."""

    @patch('src.ui.gui.tk.Tk')
    def test_switch_scientific_returns_18_operations(self, mock_tk_class):
        """After switch_mode(OperationMode.SCIENTIFIC), get_current_mode_operations() returns 18 operations."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.switch_mode(OperationMode.SCIENTIFIC)
        ops = app.get_current_mode_operations()
        assert len(ops) == 18

    @patch('src.ui.gui.tk.Tk')
    def test_switch_back_to_normal_returns_6_operations(self, mock_tk_class):
        """After switching to SCIENTIFIC then back to NORMAL, get_current_mode_operations() returns 6 operations."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.switch_mode(OperationMode.SCIENTIFIC)
        app.switch_mode(OperationMode.NORMAL)
        ops = app.get_current_mode_operations()
        assert len(ops) == 6

    @patch('src.ui.gui.tk.Tk')
    def test_op_var_reset_to_first_scientific_operation(self, mock_tk_class):
        """After switch_mode(OperationMode.SCIENTIFIC), _op_var.get() is reset to first scientific operation."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.switch_mode(OperationMode.SCIENTIFIC)

        # Get the first operation from scientific mode
        scientific_ops = app.get_current_mode_operations()
        expected_first = scientific_ops[0] if scientific_ops else None

        # Check _op_var is set to the first operation (if _op_var exists)
        if hasattr(app, "_op_var"):
            current_op = app._op_var.get()
            assert current_op == expected_first

    @patch('src.ui.gui.tk.Tk')
    def test_op_var_valid_normal_operation_after_switch(self, mock_tk_class):
        """After switch_mode(OperationMode.NORMAL), _op_var.get() is a valid normal-mode operation."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.switch_mode(OperationMode.SCIENTIFIC)
        app.switch_mode(OperationMode.NORMAL)

        normal_ops = app.get_current_mode_operations()

        if hasattr(app, "_op_var"):
            current_op = app._op_var.get()
            assert current_op in normal_ops

    @patch('src.ui.gui.tk.Tk')
    def test_multiple_mode_switches_stable(self, mock_tk_class):
        """Switching modes multiple times (NORMAL→SCIENTIFIC→NORMAL→SCIENTIFIC) is stable."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)

        # Switch: NORMAL (6) → SCIENTIFIC (18) → NORMAL (6) → SCIENTIFIC (18)
        ops = app.get_current_mode_operations()
        assert len(ops) == 6

        app.switch_mode(OperationMode.SCIENTIFIC)
        ops = app.get_current_mode_operations()
        assert len(ops) == 18

        app.switch_mode(OperationMode.NORMAL)
        ops = app.get_current_mode_operations()
        assert len(ops) == 6

        app.switch_mode(OperationMode.SCIENTIFIC)
        ops = app.get_current_mode_operations()
        assert len(ops) == 18

    @patch('src.ui.gui.tk.Tk')
    def test_invalid_mode_is_noop(self, mock_tk_class):
        """Switching to an invalid/unknown mode is a no-op (internal state unchanged)."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        original_mode = app._current_mode

        # Try to switch to an invalid mode (that doesn't exist in _modes dict)
        # This should be a no-op due to the if check in switch_mode
        invalid_mode = "INVALID_MODE_THAT_DOES_NOT_EXIST"
        app.switch_mode(invalid_mode)

        # Mode should not have changed
        assert app._current_mode == original_mode

    @patch('src.ui.gui.tk.Tk')
    def test_rebuild_operation_menu_no_exception(self, mock_tk_class):
        """_rebuild_operation_menu() called directly does not raise any exception."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)

        # Should not raise any exception
        try:
            app._rebuild_operation_menu()
        except Exception as e:
            pytest.fail(f"_rebuild_operation_menu raised {type(e).__name__}: {e}")

    @patch('src.ui.gui.tk.Tk')
    def test_mode_switch_persistence(self, mock_tk_class):
        """After mode switch, subsequent get_current_mode_operations() call returns same set."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)

        app.switch_mode(OperationMode.SCIENTIFIC)
        ops1 = app.get_current_mode_operations()
        ops2 = app.get_current_mode_operations()

        # Both calls should return identical operation lists
        assert ops1 == ops2
        assert len(ops1) == 18

    @patch('src.ui.gui.tk.Tk')
    def test_switch_mode_preserves_calculator_instance(self, mock_tk_class):
        """Switching modes does not affect _calculator instance identity."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        original_calc_id = id(app._calculator)
        original_registry_id = id(app._registry)

        app.switch_mode(OperationMode.SCIENTIFIC)

        # Calculator and registry should be the same instances
        assert id(app._calculator) == original_calc_id
        assert id(app._registry) == original_registry_id

    @patch('src.ui.gui.tk.Tk')
    def test_scientific_mode_has_scientific_only_operations(self, mock_tk_class):
        """Scientific mode includes expected ops: power, factorial, cube, cbrt, ln, log10."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.switch_mode(OperationMode.SCIENTIFIC)

        scientific_ops = set(app.get_current_mode_operations())
        required_scientific_ops = {"power", "factorial", "cube", "cbrt", "ln", "log10"}

        # All scientific-only operations should be present
        assert required_scientific_ops.issubset(scientific_ops)

    @patch('src.ui.gui.tk.Tk')
    def test_normal_mode_exact_operations(self, mock_tk_class):
        """Normal mode includes exactly: add, subtract, multiply, divide, square, sqrt."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)
        app.switch_mode(OperationMode.NORMAL)

        normal_ops = set(app.get_current_mode_operations())
        expected_normal_ops = {"add", "subtract", "multiply", "divide", "square", "sqrt"}

        # Exact set match for normal mode
        assert normal_ops == expected_normal_ops

    @patch('src.ui.gui.tk.Tk')
    def test_op_menu_not_duplicated_on_multiple_switches(self, mock_tk_class):
        """After two switches, _op_menu is replaced (not accumulated; singular widget)."""
        from src.ui.gui import CalculatorApp

        mock_root = Mock()
        app = CalculatorApp(root=mock_root)

        # First switch should replace the menu
        app.switch_mode(OperationMode.SCIENTIFIC)

        # Second switch should destroy old menu and create new one (not accumulate)
        app.switch_mode(OperationMode.NORMAL)

        # The _op_menu attribute should exist and be a single widget (not a list/accumulated)
        if hasattr(app, "_op_menu"):
            # Verify it's a widget, not a list of widgets
            assert not isinstance(app._op_menu, list)
