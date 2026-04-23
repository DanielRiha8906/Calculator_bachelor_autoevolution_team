"""Integration tests for CalculatorGUI iOS-style button-grid calculator.

These tests run in a headless environment without a display server.
Tests use tk.Tk() with withdraw() to avoid window rendering, and directly
test internal state and button click handlers.
"""

from unittest import mock

import pytest

pytestmark = pytest.mark.gui

# Skip all tests in this module if tkinter is unavailable
tk = pytest.importorskip("tkinter")

from src.gui import CalculatorGUI
from src.session_history import SessionHistory
from src.mode_manager import CalculatorMode


class TestCalculatorGUIInitialization:
    """Test suite for CalculatorGUI initialization and widget creation."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_gui_window_created_with_correct_title(self, gui_setup):
        """Verify that the Tk root window is created and titled 'Calculator'."""
        gui = gui_setup
        assert isinstance(gui.root, tk.Tk)
        assert gui.root.title() == "Calculator"

    def test_gui_background_color_is_black(self, gui_setup):
        """Verify that the GUI background is black (#000000)."""
        gui = gui_setup
        bg_color = gui.root.cget("bg")
        assert bg_color == "#000000"

    def test_display_label_exists_and_right_aligned(self, gui_setup):
        """Verify display label exists with correct font and right alignment."""
        gui = gui_setup
        assert hasattr(gui, "_display_label")
        assert isinstance(gui._display_label, tk.Label)
        anchor = gui._display_label.cget("anchor")
        assert anchor == "e"  # 'e' means east/right-aligned
        # Verify font is present and is Helvetica
        font_info = gui._display_label.cget("font")
        assert "Helvetica" in str(font_info)

    def test_standard_frame_exists(self, gui_setup):
        """Verify standard grid frame exists."""
        gui = gui_setup
        assert hasattr(gui, "_standard_frame")
        assert isinstance(gui._standard_frame, tk.Frame)

    def test_scientific_frame_exists_but_hidden_initially(self, gui_setup):
        """Verify scientific frame exists and is hidden in standard mode."""
        gui = gui_setup
        assert hasattr(gui, "_scientific_frame")
        assert isinstance(gui._scientific_frame, tk.Frame)
        # Check if it's packed (visible) or not
        try:
            packing_info = gui._scientific_frame.pack_info()
            is_visible = bool(packing_info)
        except tk.TclError:
            # If pack_info() raises, the widget is not packed
            is_visible = False
        assert not is_visible, "Scientific frame should be hidden initially"

    def test_initial_calculator_state(self, gui_setup):
        """Verify initial internal state is correct."""
        gui = gui_setup
        assert gui._display_value == "0"
        assert gui._accumulated_value is None
        assert gui._pending_operator is None
        assert gui._is_new_number is True

    def test_engine_components_initialized(self, gui_setup):
        """Verify calculator engine components are created."""
        gui = gui_setup
        assert gui._calc is not None
        assert gui._registry is not None
        assert gui._mode_manager is not None
        assert isinstance(gui._history, SessionHistory)


class TestDigitInput:
    """Test suite for digit button handling and accumulation."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_digit_accumulation(self, gui_setup):
        """Verify clicking digits 1, 2, 3 produces '123' in display_value."""
        gui = gui_setup
        gui._on_digit("1")
        gui._on_digit("2")
        gui._on_digit("3")
        assert gui._display_value == "123"

    def test_leading_zero_prevention(self, gui_setup):
        """Verify digit replaces '0', not appends to it."""
        gui = gui_setup
        assert gui._display_value == "0"
        gui._on_digit("5")
        assert gui._display_value == "5", "Digit should replace initial '0'"
        gui._on_digit("7")
        assert gui._display_value == "57", "Subsequent digit should append"

    def test_is_new_number_flag_after_clear(self, gui_setup):
        """Verify _is_new_number is True after clear, next digit replaces '0'."""
        gui = gui_setup
        gui._on_digit("5")
        assert gui._is_new_number is False
        gui._on_clear()
        assert gui._is_new_number is True
        gui._on_digit("9")
        assert gui._display_value == "9"

    @pytest.mark.parametrize("digit", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
    def test_all_digits_accepted(self, gui_setup, digit):
        """Verify all digit buttons 0-9 are accepted."""
        gui = gui_setup
        gui._on_digit(digit)
        assert gui._display_value == digit


class TestDecimalInput:
    """Test suite for decimal point handling."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_decimal_added_to_display(self, gui_setup):
        """Verify clicking '.' adds decimal point to current display."""
        gui = gui_setup
        gui._on_digit("5")
        gui._on_decimal()
        assert gui._display_value == "5."

    def test_decimal_only_once(self, gui_setup):
        """Verify second decimal press does nothing when one already exists."""
        gui = gui_setup
        gui._on_digit("3")
        gui._on_decimal()
        assert gui._display_value == "3."
        gui._on_decimal()
        assert gui._display_value == "3.", "Second decimal should not be added"

    def test_decimal_starts_with_zero(self, gui_setup):
        """Verify decimal on new number produces '0.' not just '.'."""
        gui = gui_setup
        gui._on_clear()
        assert gui._is_new_number is True
        gui._on_decimal()
        assert gui._display_value == "0."


class TestOperatorInput:
    """Test suite for binary operator button handling."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_binary_operator_stores_accumulator(self, gui_setup):
        """Verify pressing operator after digit stores accumulated value."""
        gui = gui_setup
        gui._on_digit("5")
        gui._on_operator("+")
        assert gui._accumulated_value == 5.0
        assert gui._pending_operator == "+"
        assert gui._is_new_number is True

    def test_full_addition(self, gui_setup):
        """Verify 5 + 3 = displays '8'."""
        gui = gui_setup
        gui._on_digit("5")
        gui._on_operator("+")
        gui._on_digit("3")
        gui._on_equals()
        assert gui._display_value == "8"
        assert gui._accumulated_value == 8.0

    def test_full_subtraction(self, gui_setup):
        """Verify 9 − 4 = displays '5'."""
        gui = gui_setup
        gui._on_digit("9")
        gui._on_operator("−")
        gui._on_digit("4")
        gui._on_equals()
        assert gui._display_value == "5"

    def test_full_multiplication(self, gui_setup):
        """Verify 6 × 7 = displays '42'."""
        gui = gui_setup
        gui._on_digit("6")
        gui._on_operator("×")
        gui._on_digit("7")
        gui._on_equals()
        assert gui._display_value == "42"

    def test_full_division(self, gui_setup):
        """Verify 8 ÷ 2 = displays '4'."""
        gui = gui_setup
        gui._on_digit("8")
        gui._on_operator("÷")
        gui._on_digit("2")
        gui._on_equals()
        assert gui._display_value == "4"

    def test_binary_operator_chaining(self, gui_setup):
        """Verify 5 + 3 × executes 5+3=8, stores 8 as accumulator."""
        gui = gui_setup
        gui._on_digit("5")
        gui._on_operator("+")
        gui._on_digit("3")
        gui._on_operator("×")
        # After second operator, 5+3 should be executed
        assert gui._display_value == "8"
        assert gui._accumulated_value == 8.0
        assert gui._pending_operator == "×"

    def test_equals_with_no_pending_operator_is_noop(self, gui_setup):
        """Verify pressing '=' with no pending operator is a no-op."""
        gui = gui_setup
        gui._on_digit("5")
        gui._on_equals()
        # Should not crash, display should remain "5"
        assert gui._display_value == "5"

    def test_division_by_zero_shows_error(self, gui_setup):
        """Verify 5 ÷ 0 = shows an error string (not crash)."""
        gui = gui_setup
        gui._on_digit("5")
        gui._on_operator("÷")
        gui._on_digit("0")
        gui._on_equals()
        # Should show error, not crash
        assert "Error" in gui._display_value or "division" in gui._display_value.lower()

    @pytest.mark.parametrize("op", ["+", "−", "×", "÷"])
    def test_all_binary_operators_accepted(self, gui_setup, op):
        """Verify all binary operator symbols are accepted."""
        gui = gui_setup
        gui._on_digit("2")
        gui._on_operator(op)
        assert gui._pending_operator == op


class TestUnaryOperators:
    """Test suite for unary operator handling."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_square_root_unary_operator(self, gui_setup):
        """Verify √ operator executes immediately on display value."""
        gui = gui_setup
        gui._on_digit("9")
        gui._on_operator("√")
        # sqrt(9) = 3
        assert gui._display_value == "3"
        assert gui._is_new_number is True

    def test_square_unary_operator(self, gui_setup):
        """Verify x² operator executes immediately."""
        gui = gui_setup
        gui._on_digit("5")
        gui._on_operator("x²")
        # 5^2 = 25
        assert gui._display_value == "25"

    def test_factorial_unary_operator(self, gui_setup):
        """Verify n! operator executes immediately."""
        gui = gui_setup
        gui._on_digit("5")
        gui._on_operator("n!")
        # 5! = 120
        assert gui._display_value == "120"

    @pytest.mark.parametrize("op", ["√", "x²", "n!", "ln", "log", "sin", "cos", "tan"])
    def test_all_unary_operators_accepted(self, gui_setup, op):
        """Verify all unary operator symbols are accepted without crashing."""
        gui = gui_setup
        gui._on_digit("2")
        # Should not crash, might show error for ln(2) etc but that's ok
        gui._on_operator(op)
        assert isinstance(gui._display_value, str)


class TestDeleteButton:
    """Test suite for delete/backspace button."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_delete_removes_last_char(self, gui_setup):
        """Verify '123' → delete → '12'."""
        gui = gui_setup
        gui._on_digit("1")
        gui._on_digit("2")
        gui._on_digit("3")
        assert gui._display_value == "123"
        gui._on_delete()
        assert gui._display_value == "12"

    def test_delete_single_char_becomes_zero(self, gui_setup):
        """Verify '5' → delete → '0'."""
        gui = gui_setup
        gui._on_digit("5")
        assert gui._display_value == "5"
        gui._on_delete()
        assert gui._display_value == "0"

    def test_delete_when_is_new_number(self, gui_setup):
        """Verify delete after computation (is_new_number=True) resets to '0'."""
        gui = gui_setup
        gui._on_digit("5")
        gui._on_operator("+")
        gui._on_digit("3")
        gui._on_equals()
        # Now is_new_number should be True
        assert gui._is_new_number is True
        gui._on_delete()
        assert gui._display_value == "0"

    def test_delete_decimal_point(self, gui_setup):
        """Verify delete works on decimal numbers '3.5' → '3.'."""
        gui = gui_setup
        gui._on_digit("3")
        gui._on_decimal()
        gui._on_digit("5")
        assert gui._display_value == "3.5"
        gui._on_delete()
        assert gui._display_value == "3."


class TestClearButton:
    """Test suite for clear button."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_clear_resets_all_state(self, gui_setup):
        """Verify clear resets all internal state to initial values."""
        gui = gui_setup
        # Set up some state
        gui._on_digit("5")
        gui._on_operator("+")
        gui._on_digit("3")
        # Verify state is modified
        assert gui._display_value != "0"
        assert gui._accumulated_value == 5.0
        assert gui._pending_operator == "+"
        # After operator, is_new_number is True; after digit, it's False
        assert gui._is_new_number is False

        # Clear
        gui._on_clear()

        # Verify reset
        assert gui._display_value == "0"
        assert gui._accumulated_value is None
        assert gui._pending_operator is None
        assert gui._is_new_number is True

    def test_clear_after_calculation(self, gui_setup):
        """Verify clear works after a full calculation."""
        gui = gui_setup
        gui._on_digit("7")
        gui._on_operator("×")
        gui._on_digit("6")
        gui._on_equals()
        assert gui._display_value == "42"
        gui._on_clear()
        assert gui._display_value == "0"
        assert gui._accumulated_value is None


class TestModeSwitch:
    """Test suite for mode switching between Standard and Scientific."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_mode_switch_calls_mode_manager(self, gui_setup):
        """Verify _on_mode_switch() calls mode_manager.switch_mode()."""
        gui = gui_setup
        initial_mode = gui._mode_manager.get_current_mode()
        gui._on_mode_switch()
        new_mode = gui._mode_manager.get_current_mode()
        assert initial_mode != new_mode

    def test_scientific_frame_hidden_initially(self, gui_setup):
        """Verify scientific frame is not packed initially."""
        gui = gui_setup
        try:
            packing_info = gui._scientific_frame.pack_info()
            is_packed = bool(packing_info)
        except tk.TclError:
            # If pack_info() raises, the widget is not packed
            is_packed = False
        assert not is_packed, "Scientific frame should not be packed initially"

    def test_scientific_frame_visible_after_first_toggle(self, gui_setup):
        """Verify scientific frame is visible after first mode toggle."""
        gui = gui_setup
        gui._on_mode_switch()
        packing_info = gui._scientific_frame.pack_info()
        assert bool(packing_info), "Scientific frame should be packed after toggle to Scientific"
        assert gui._mode_manager.get_current_mode() is CalculatorMode.SCIENTIFIC

    def test_scientific_frame_hidden_after_second_toggle(self, gui_setup):
        """Verify scientific frame is hidden after toggle back to Standard."""
        gui = gui_setup
        gui._on_mode_switch()
        gui._on_mode_switch()
        try:
            packing_info = gui._scientific_frame.pack_info()
            is_packed = bool(packing_info)
        except tk.TclError:
            # If pack_info() raises, the widget is not packed
            is_packed = False
        assert not is_packed, "Scientific frame should not be packed after toggle back to NORMAL"
        assert gui._mode_manager.get_current_mode() is CalculatorMode.NORMAL

    def test_mode_toggle_multiple_times(self, gui_setup):
        """Verify mode can be toggled multiple times."""
        gui = gui_setup
        for _ in range(4):
            gui._on_mode_switch()
        # After even number of toggles, should be back to NORMAL
        assert gui._mode_manager.get_current_mode() is CalculatorMode.NORMAL


class TestSymbolMapping:
    """Test suite for symbol-to-operation key mapping."""

    def test_symbol_to_operation_add(self):
        """Verify '+' maps to 'add'."""
        result = CalculatorGUI._symbol_to_operation("+")
        assert result == "add"

    def test_symbol_to_operation_subtract(self):
        """Verify '−' maps to 'subtract'."""
        result = CalculatorGUI._symbol_to_operation("−")
        assert result == "subtract"

    def test_symbol_to_operation_multiply(self):
        """Verify '×' maps to 'multiply'."""
        result = CalculatorGUI._symbol_to_operation("×")
        assert result == "multiply"

    def test_symbol_to_operation_divide(self):
        """Verify '÷' maps to 'divide'."""
        result = CalculatorGUI._symbol_to_operation("÷")
        assert result == "divide"

    def test_symbol_to_operation_sqrt(self):
        """Verify '√' maps to 'square_root'."""
        result = CalculatorGUI._symbol_to_operation("√")
        assert result == "square_root"

    def test_symbol_to_operation_square(self):
        """Verify 'x²' maps to 'square'."""
        result = CalculatorGUI._symbol_to_operation("x²")
        assert result == "square"

    def test_symbol_to_operation_power(self):
        """Verify 'xʸ' maps to 'power'."""
        result = CalculatorGUI._symbol_to_operation("xʸ")
        assert result == "power"

    def test_symbol_to_operation_factorial(self):
        """Verify 'n!' maps to 'factorial'."""
        result = CalculatorGUI._symbol_to_operation("n!")
        assert result == "factorial"

    def test_symbol_to_operation_ln(self):
        """Verify 'ln' maps to 'ln'."""
        result = CalculatorGUI._symbol_to_operation("ln")
        assert result == "ln"

    def test_symbol_to_operation_log(self):
        """Verify 'log' maps to 'log'."""
        result = CalculatorGUI._symbol_to_operation("log")
        assert result == "log"

    def test_symbol_to_operation_sin(self):
        """Verify 'sin' maps to 'sin'."""
        result = CalculatorGUI._symbol_to_operation("sin")
        assert result == "sin"

    def test_symbol_to_operation_cos(self):
        """Verify 'cos' maps to 'cos'."""
        result = CalculatorGUI._symbol_to_operation("cos")
        assert result == "cos"

    def test_symbol_to_operation_tan(self):
        """Verify 'tan' maps to 'tan'."""
        result = CalculatorGUI._symbol_to_operation("tan")
        assert result == "tan"

    def test_symbol_to_operation_invalid_raises_keyerror(self):
        """Verify invalid symbol raises KeyError."""
        with pytest.raises(KeyError):
            CalculatorGUI._symbol_to_operation("invalid")


class TestFormatResult:
    """Test suite for result formatting."""

    def test_format_whole_number(self):
        """Verify _format_result(3.0) returns '3' not '3.0'."""
        result = CalculatorGUI._format_result(3.0)
        assert result == "3"

    def test_format_decimal(self):
        """Verify _format_result(3.5) returns '3.5'."""
        result = CalculatorGUI._format_result(3.5)
        assert result == "3.5"

    def test_format_zero(self):
        """Verify _format_result(0.0) returns '0'."""
        result = CalculatorGUI._format_result(0.0)
        assert result == "0"

    def test_format_large_whole_number(self):
        """Verify large whole numbers are formatted without decimal."""
        result = CalculatorGUI._format_result(1000.0)
        assert result == "1000"

    def test_format_small_decimal(self):
        """Verify small decimal numbers are preserved."""
        result = CalculatorGUI._format_result(0.1)
        assert result == "0.1"

    def test_format_negative_whole(self):
        """Verify negative whole numbers are formatted correctly."""
        result = CalculatorGUI._format_result(-5.0)
        assert result == "-5"

    def test_format_negative_decimal(self):
        """Verify negative decimals are preserved."""
        result = CalculatorGUI._format_result(-3.14)
        assert result == "-3.14"


class TestUpdateDisplay:
    """Test suite for display label updates."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_display_label_updated_on_digit(self, gui_setup):
        """Verify display label shows current _display_value after digit."""
        gui = gui_setup
        gui._on_digit("7")
        label_text = gui._display_label.cget("text")
        assert label_text == "7"

    def test_display_label_updated_on_clear(self, gui_setup):
        """Verify display label shows '0' after clear."""
        gui = gui_setup
        gui._on_digit("5")
        gui._on_clear()
        label_text = gui._display_label.cget("text")
        assert label_text == "0"

    def test_display_label_updated_on_operation(self, gui_setup):
        """Verify display label updated after operation execution."""
        gui = gui_setup
        gui._on_digit("4")
        gui._on_operator("+")
        gui._on_digit("2")
        gui._on_equals()
        label_text = gui._display_label.cget("text")
        assert label_text == "6"


class TestHistoryIntegration:
    """Test suite for SessionHistory integration with GUI."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_operation_recorded_in_history_after_equals(self, gui_setup):
        """Verify operation is recorded in SessionHistory after equals."""
        gui = gui_setup
        gui._on_digit("5")
        gui._on_operator("+")
        gui._on_digit("3")
        gui._on_equals()

        # Check history
        history_entries = gui._history.get_history()
        assert len(history_entries) == 1
        assert history_entries[0]["operation"] == "add"
        assert history_entries[0]["operands"] == [5.0, 3.0]
        assert history_entries[0]["result"] == 8.0

    def test_multiple_operations_recorded(self, gui_setup):
        """Verify multiple operations are recorded in order."""
        gui = gui_setup
        # First: 5 + 3 = 8
        gui._on_digit("5")
        gui._on_operator("+")
        gui._on_digit("3")
        gui._on_equals()

        # Second: 8 × 2 = 16
        gui._on_digit("2")
        gui._on_operator("×")
        gui._on_equals()

        history_entries = gui._history.get_history()
        assert len(history_entries) == 2
        assert history_entries[0]["operation"] == "add"
        assert history_entries[1]["operation"] == "multiply"

    def test_unary_operation_recorded_in_history(self, gui_setup):
        """Verify unary operations are recorded in history."""
        gui = gui_setup
        gui._on_digit("9")
        gui._on_operator("√")

        history_entries = gui._history.get_history()
        assert len(history_entries) == 1
        assert history_entries[0]["operation"] == "square_root"
        assert history_entries[0]["operands"] == [9.0]
        assert history_entries[0]["result"] == 3.0


class TestEdgeCases:
    """Test suite for edge cases and error conditions."""

    @pytest.fixture
    def gui_setup(self):
        """Create a test GUI with withdrawn window."""
        root = tk.Tk()
        root.withdraw()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        yield gui
        root.destroy()

    def test_multiple_decimal_points_prevented(self, gui_setup):
        """Verify only one decimal point can be added to a number."""
        gui = gui_setup
        gui._on_digit("3")
        gui._on_decimal()
        gui._on_decimal()
        gui._on_decimal()
        assert gui._display_value == "3."
        assert gui._display_value.count(".") == 1

    def test_operation_chain_complex(self, gui_setup):
        """Verify complex operation chain: 10 + 5 - 3 = 12."""
        gui = gui_setup
        gui._on_digit("1")
        gui._on_digit("0")
        gui._on_operator("+")
        gui._on_digit("5")
        gui._on_operator("−")
        # 10 + 5 should execute first, result is 15
        assert gui._display_value == "15"
        gui._on_digit("3")
        gui._on_equals()
        assert gui._display_value == "12"

    def test_invalid_input_in_operator_handler(self, gui_setup):
        """Verify non-numeric display doesn't crash operator handler."""
        gui = gui_setup
        gui._display_value = "abc"
        gui._on_operator("+")
        # Should show error instead of crashing
        assert gui._display_value == "Error"

    def test_delete_on_already_zero(self, gui_setup):
        """Verify delete on '0' stays at '0'."""
        gui = gui_setup
        assert gui._display_value == "0"
        gui._on_delete()
        assert gui._display_value == "0"

    def test_operations_with_negative_results(self, gui_setup):
        """Verify operations that produce negative results."""
        gui = gui_setup
        gui._on_digit("3")
        gui._on_operator("−")
        gui._on_digit("5")
        gui._on_equals()
        assert gui._display_value == "-2"

    def test_very_long_number_accumulation(self, gui_setup):
        """Verify long numbers can be entered."""
        gui = gui_setup
        for digit in "123456789":
            gui._on_digit(digit)
        assert gui._display_value == "123456789"

    def test_decimal_at_start_of_new_number(self, gui_setup):
        """Verify decimal at start of new number produces '0.'."""
        gui = gui_setup
        gui._on_digit("5")
        gui._on_operator("+")
        # Now is_new_number is True
        gui._on_decimal()
        assert gui._display_value == "0."

    def test_equals_without_first_operand(self, gui_setup):
        """Verify pressing equals immediately is safe."""
        gui = gui_setup
        gui._on_equals()
        # Should not crash, display should remain "0"
        assert gui._display_value == "0"

    def test_accumulated_value_preserved_during_chaining(self, gui_setup):
        """Verify accumulated value is updated during operator chaining."""
        gui = gui_setup
        gui._on_digit("7")
        gui._on_operator("+")
        assert gui._accumulated_value == 7.0
        gui._on_digit("2")
        gui._on_operator("×")
        # After chaining, accumulated should be 7 + 2 = 9
        assert gui._accumulated_value == 9.0

    def test_display_shows_error_on_invalid_display_parse(self, gui_setup):
        """Verify error display when display_value is non-numeric during execution."""
        gui = gui_setup
        gui._display_value = "NotANumber"
        gui._pending_operator = "+"
        gui._accumulated_value = 5.0
        gui._execute_pending()
        assert gui._display_value == "Error"
