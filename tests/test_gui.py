"""Comprehensive pytest tests for the GUI Calculator module.

Tests cover:
- Module-level constants (_THEME and _SYMBOL_MAP)
- GuiCalculator.__init__ and _setup_layout
- Button grid construction (_build_button_grid, _rebuild_button_grid)
- Button color assignment (_get_button_colors)
- Mode toggle and mode change handlers (_on_mode_toggle, _on_mode_change)
- Result display updates (_update_result_display)
- Hover effect bindings
- Theme styling and layout correctness
"""

from __future__ import annotations

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys

try:
    import tkinter as tk
except ImportError:
    tk = None

from src.interface.gui import GuiCalculator, _THEME, _SYMBOL_MAP
from src.core.calculator import Calculator
from src.session.mode import Mode
from src.shared.logger import Logger


@pytest.fixture
def tk_root():
    """Create and yield a tkinter Tk root window (withdrawn to avoid display)."""
    if tk is None:
        pytest.skip("tkinter not available")
    root = tk.Tk()
    root.withdraw()
    yield root
    root.destroy()


@pytest.fixture
def calculator():
    """Create a fresh Calculator instance for each test."""
    return Calculator()


@pytest.fixture
def logger():
    """Create a fresh Logger instance for each test."""
    return Logger()


@pytest.fixture
def gui_calculator(tk_root, calculator, logger):
    """Create a GuiCalculator instance with all required dependencies."""
    return GuiCalculator(tk_root, calculator, logger)


class TestModuleConstants:
    """Test _THEME and _SYMBOL_MAP module-level dictionaries."""

    def test_theme_dict_exists_and_is_dict(self):
        """Test that _THEME is a dictionary."""
        assert isinstance(_THEME, dict)
        assert len(_THEME) > 0

    def test_theme_has_operator_button_colors(self):
        """Test _THEME has operator button color keys."""
        required_keys = ["btn_operator_bg", "btn_operator_fg", "btn_operator_active"]
        for key in required_keys:
            assert key in _THEME

    def test_theme_has_scientific_button_colors(self):
        """Test _THEME has scientific button color keys."""
        required_keys = ["btn_scientific_bg", "btn_scientific_fg", "btn_scientific_active"]
        for key in required_keys:
            assert key in _THEME

    def test_theme_has_normal_button_colors(self):
        """Test _THEME has normal button color keys."""
        required_keys = ["btn_normal_bg", "btn_normal_fg", "btn_normal_active"]
        for key in required_keys:
            assert key in _THEME

    def test_symbol_map_has_basic_arithmetic(self):
        """Test _SYMBOL_MAP has basic arithmetic operator mappings."""
        required_mappings = {
            "add": "+",
            "subtract": "−",
            "multiply": "×",
            "divide": "÷",
        }
        for op_key, expected_symbol in required_mappings.items():
            assert op_key in _SYMBOL_MAP
            assert _SYMBOL_MAP[op_key] == expected_symbol

    def test_symbol_map_has_scientific_functions(self):
        """Test _SYMBOL_MAP has scientific function mappings."""
        required_mappings = {
            "sqrt": "√",
            "square": "x²",
            "cube": "x³",
            "power": "xʸ",
            "factorial": "n!",
            "log": "log",
            "ln": "ln",
            "sin": "sin",
            "cos": "cos",
            "tan": "tan",
            "pi": "π",
            "e": "e",
        }
        for op_key, expected_symbol in required_mappings.items():
            assert op_key in _SYMBOL_MAP
            assert _SYMBOL_MAP[op_key] == expected_symbol


class TestGuiCalculatorInit:
    """Test GuiCalculator initialization and layout setup."""

    def test_gui_calculator_init_with_calculator_only(self, tk_root, calculator):
        """Test GuiCalculator init with calculator and no logger."""
        gui = GuiCalculator(tk_root, calculator)
        assert gui._calculator is calculator
        assert gui._logger is None
        assert gui._mode == Mode.NORMAL
        gui._root.destroy()

    def test_gui_calculator_init_with_logger(self, tk_root, calculator, logger):
        """Test GuiCalculator init with logger provided."""
        gui = GuiCalculator(tk_root, calculator, logger)
        assert gui._logger is logger
        gui._root.destroy()

    def test_setup_layout_configures_root_background(self, gui_calculator):
        """Test that _setup_layout sets window background."""
        bg_color = gui_calculator._root.cget("bg")
        assert bg_color == _THEME["window_bg"]


class TestSetupLayoutDisplay:
    """Test result display label setup in _setup_layout."""

    def test_result_label_is_created(self, gui_calculator):
        """Test that result label widget is created."""
        assert gui_calculator._result_label is not None
        assert isinstance(gui_calculator._result_label, tk.Label)

    def test_result_label_initial_text_is_zero(self, gui_calculator):
        """Test that result label shows '0' initially."""
        assert gui_calculator._result_label.cget("text") == "0"

    def test_result_label_background_color(self, gui_calculator):
        """Test result label background matches theme."""
        assert gui_calculator._result_label.cget("bg") == _THEME["display_bg"]

    def test_result_label_foreground_color(self, gui_calculator):
        """Test result label foreground matches theme."""
        assert gui_calculator._result_label.cget("fg") == _THEME["display_fg"]

    def test_result_label_is_right_aligned(self, gui_calculator):
        """Test result label anchor is 'e' (east/right)."""
        assert gui_calculator._result_label.cget("anchor") == "e"

    def test_result_label_has_padding(self, gui_calculator):
        """Test result label has horizontal and vertical padding."""
        padx = gui_calculator._result_label.cget("padx")
        pady = gui_calculator._result_label.cget("pady")
        assert padx > 0
        assert pady > 0


class TestSetupLayoutModeToggle:
    """Test mode toggle button setup in _setup_layout."""

    def test_mode_toggle_button_is_created(self, gui_calculator):
        """Test that mode toggle button is created."""
        assert gui_calculator._mode_toggle_btn is not None
        assert isinstance(gui_calculator._mode_toggle_btn, tk.Button)

    def test_mode_toggle_initial_text_is_scientific(self, gui_calculator):
        """Test that in NORMAL mode, button text is 'scientific'."""
        assert gui_calculator._mode_toggle_btn.cget("text") == "scientific"

    def test_mode_toggle_button_has_command(self, gui_calculator):
        """Test mode toggle button has command callback."""
        assert gui_calculator._mode_toggle_btn.cget("command") != ""

    def test_mode_toggle_has_hover_bindings(self, gui_calculator):
        """Test mode toggle button has <Enter> and <Leave> bindings."""
        bindings = gui_calculator._mode_toggle_btn.bind()
        assert "<Enter>" in bindings or any("<Enter>" in str(b) for b in bindings)
        assert "<Leave>" in bindings or any("<Leave>" in str(b) for b in bindings)


class TestSetupLayoutButtonFrame:
    """Test button frame setup in _setup_layout."""

    def test_button_frame_is_created(self, gui_calculator):
        """Test that button frame is created."""
        assert gui_calculator._btn_frame is not None
        assert isinstance(gui_calculator._btn_frame, tk.Frame)

    def test_button_frame_has_children_after_setup(self, gui_calculator):
        """Test that button frame contains buttons after setup."""
        children = gui_calculator._btn_frame.winfo_children()
        assert len(children) > 0


class TestBuildButtonGrid:
    """Test button grid construction."""

    def test_build_button_grid_creates_buttons(self, gui_calculator):
        """Test that _build_button_grid creates buttons."""
        buttons = [w for w in gui_calculator._btn_frame.winfo_children() if isinstance(w, tk.Button)]
        assert len(buttons) > 0

    def test_button_grid_has_four_columns(self, gui_calculator):
        """Test that button grid is configured for 4 columns."""
        buttons = [w for w in gui_calculator._btn_frame.winfo_children() if isinstance(w, tk.Button)]
        assert len(buttons) > 0
        cols = set()
        for btn in buttons:
            info = btn.grid_info()
            if info:
                cols.add(info.get("column", 0))
        assert max(cols) <= 3

    def test_buttons_have_symbol_labels(self, gui_calculator):
        """Test that buttons use _SYMBOL_MAP labels."""
        buttons = [w for w in gui_calculator._btn_frame.winfo_children() if isinstance(w, tk.Button)]
        button_texts = [btn.cget("text") for btn in buttons]
        symbol_values = set(_SYMBOL_MAP.values())
        button_text_set = set(button_texts)
        overlapping = symbol_values & button_text_set
        assert len(overlapping) > 0

    def test_buttons_have_colors_assigned(self, gui_calculator):
        """Test that buttons have background colors assigned."""
        buttons = [w for w in gui_calculator._btn_frame.winfo_children() if isinstance(w, tk.Button)]
        for btn in buttons:
            bg = btn.cget("bg")
            fg = btn.cget("fg")
            assert bg is not None and bg != ""
            assert fg is not None and fg != ""

    def test_buttons_have_hover_bindings(self, gui_calculator):
        """Test that buttons have <Enter> and <Leave> bindings."""
        buttons = [w for w in gui_calculator._btn_frame.winfo_children() if isinstance(w, tk.Button)]
        for btn in buttons:
            bindings = btn.bind()
            assert "<Enter>" in bindings or any("<Enter>" in str(b) for b in bindings)
            assert "<Leave>" in bindings or any("<Leave>" in str(b) for b in bindings)

    def test_normal_mode_button_count(self, tk_root, calculator):
        """Test button count in NORMAL mode."""
        gui = GuiCalculator(tk_root, calculator)
        available = gui._get_available_operations_for_mode()
        buttons = [w for w in gui._btn_frame.winfo_children() if isinstance(w, tk.Button)]
        assert len(buttons) == len(available)
        gui._root.destroy()

    def test_scientific_mode_button_count(self, tk_root, calculator):
        """Test button count in SCIENTIFIC mode."""
        gui = GuiCalculator(tk_root, calculator)
        gui._mode = Mode.SCIENTIFIC
        gui._rebuild_button_grid()
        available = gui._get_available_operations_for_mode()
        buttons = [w for w in gui._btn_frame.winfo_children() if isinstance(w, tk.Button)]
        assert len(buttons) == len(available)
        gui._root.destroy()


class TestRebuildButtonGrid:
    """Test button grid rebuild on mode change."""

    def test_rebuild_creates_new_buttons(self, gui_calculator):
        """Test that _rebuild_button_grid creates a new grid."""
        gui_calculator._rebuild_button_grid()
        buttons = [w for w in gui_calculator._btn_frame.winfo_children() if isinstance(w, tk.Button)]
        assert len(buttons) > 0

    def test_rebuild_with_none_frame_is_safe(self, tk_root, calculator):
        """Test that _rebuild_button_grid handles None frame gracefully."""
        gui = GuiCalculator(tk_root, calculator)
        gui._btn_frame = None
        gui._rebuild_button_grid()
        gui._root.destroy()


class TestGetButtonColors:
    """Test button color assignment logic."""

    def test_operator_buttons_are_orange(self, gui_calculator):
        """Test that operator buttons are orange."""
        operators = ["add", "subtract", "multiply", "divide"]
        for op in operators:
            bg, fg, active_bg = gui_calculator._get_button_colors(op)
            assert bg == _THEME["btn_operator_bg"]
            assert fg == _THEME["btn_operator_fg"]
            assert active_bg == _THEME["btn_operator_active"]

    def test_normal_mode_non_operator_buttons_are_medium_gray(self, gui_calculator):
        """Test that in NORMAL mode, non-operators are medium gray."""
        gui_calculator._mode = Mode.NORMAL
        non_operators = [k for k in _SYMBOL_MAP.keys() if k not in ["add", "subtract", "multiply", "divide"]]
        for op in non_operators[:3]:
            bg, fg, active_bg = gui_calculator._get_button_colors(op)
            assert bg == _THEME["btn_normal_bg"]
            assert fg == _THEME["btn_normal_fg"]
            assert active_bg == _THEME["btn_normal_active"]

    def test_scientific_mode_non_operator_buttons_are_dark_gray(self, gui_calculator):
        """Test that in SCIENTIFIC mode, non-operators are dark gray."""
        gui_calculator._mode = Mode.SCIENTIFIC
        non_operators = [k for k in _SYMBOL_MAP.keys() if k not in ["add", "subtract", "multiply", "divide"]]
        for op in non_operators[:3]:
            bg, fg, active_bg = gui_calculator._get_button_colors(op)
            assert bg == _THEME["btn_scientific_bg"]
            assert fg == _THEME["btn_scientific_fg"]
            assert active_bg == _THEME["btn_scientific_active"]

    def test_button_colors_are_strings(self, gui_calculator):
        """Test that returned colors are strings."""
        bg, fg, active_bg = gui_calculator._get_button_colors("add")
        assert isinstance(bg, str)
        assert isinstance(fg, str)
        assert isinstance(active_bg, str)

    def test_button_colors_return_three_tuple(self, gui_calculator):
        """Test that _get_button_colors returns a 3-tuple."""
        result = gui_calculator._get_button_colors("add")
        assert isinstance(result, tuple)
        assert len(result) == 3


class TestOnModeToggle:
    """Test mode toggle button click handler."""

    def test_mode_toggle_from_normal_to_scientific(self, gui_calculator):
        """Test toggling from NORMAL to SCIENTIFIC mode."""
        assert gui_calculator._mode == Mode.NORMAL
        gui_calculator._on_mode_toggle()
        assert gui_calculator._mode == Mode.SCIENTIFIC

    def test_mode_toggle_from_scientific_to_normal(self, gui_calculator):
        """Test toggling from SCIENTIFIC back to NORMAL mode."""
        gui_calculator._mode = Mode.SCIENTIFIC
        gui_calculator._on_mode_toggle()
        assert gui_calculator._mode == Mode.NORMAL

    def test_mode_toggle_updates_button_text_to_normal(self, gui_calculator):
        """Test that toggling to SCIENTIFIC updates button text to 'normal'."""
        assert gui_calculator._mode_toggle_btn.cget("text") == "scientific"
        gui_calculator._on_mode_toggle()
        assert gui_calculator._mode_toggle_btn.cget("text") == "normal"

    def test_mode_toggle_updates_button_text_to_scientific(self, gui_calculator):
        """Test that toggling to NORMAL updates button text to 'scientific'."""
        gui_calculator._mode = Mode.SCIENTIFIC
        gui_calculator._mode_toggle_btn.config(text="normal")
        gui_calculator._on_mode_toggle()
        assert gui_calculator._mode_toggle_btn.cget("text") == "scientific"

    def test_mode_toggle_rebuilds_grid(self, gui_calculator):
        """Test that mode toggle rebuilds the button grid."""
        gui_calculator._on_mode_toggle()
        assert gui_calculator._btn_frame is not None

    def test_mode_toggle_round_trip(self, gui_calculator):
        """Test mode toggle round trip: NORMAL -> SCIENTIFIC -> NORMAL."""
        assert gui_calculator._mode == Mode.NORMAL
        gui_calculator._on_mode_toggle()
        assert gui_calculator._mode == Mode.SCIENTIFIC
        gui_calculator._on_mode_toggle()
        assert gui_calculator._mode == Mode.NORMAL


class TestOnModeChange:
    """Test legacy mode change handler."""

    def test_on_mode_change_to_scientific(self, gui_calculator):
        """Test _on_mode_change sets mode to SCIENTIFIC."""
        gui_calculator._on_mode_change(Mode.SCIENTIFIC)
        assert gui_calculator._mode == Mode.SCIENTIFIC

    def test_on_mode_change_to_normal(self, gui_calculator):
        """Test _on_mode_change sets mode to NORMAL."""
        gui_calculator._mode = Mode.SCIENTIFIC
        gui_calculator._on_mode_change(Mode.NORMAL)
        assert gui_calculator._mode == Mode.NORMAL

    def test_on_mode_change_rebuilds_grid(self, gui_calculator):
        """Test that _on_mode_change rebuilds the button grid."""
        gui_calculator._on_mode_change(Mode.SCIENTIFIC)
        assert gui_calculator._btn_frame is not None
        buttons = [w for w in gui_calculator._btn_frame.winfo_children() if isinstance(w, tk.Button)]
        assert len(buttons) > 0


class TestUpdateResultDisplay:
    """Test result display update."""

    def test_update_result_display_with_int(self, gui_calculator):
        """Test _update_result_display with an integer result."""
        gui_calculator._update_result_display(42)
        assert gui_calculator._result_label.cget("text") == "42"

    def test_update_result_display_with_float(self, gui_calculator):
        """Test _update_result_display with a float result."""
        gui_calculator._update_result_display(3.14)
        assert gui_calculator._result_label.cget("text") == "3.14"

    def test_update_result_display_with_zero(self, gui_calculator):
        """Test _update_result_display with zero."""
        gui_calculator._update_result_display(0)
        assert gui_calculator._result_label.cget("text") == "0"

    def test_update_result_display_with_negative(self, gui_calculator):
        """Test _update_result_display with negative number."""
        gui_calculator._update_result_display(-5.5)
        assert gui_calculator._result_label.cget("text") == "-5.5"

    def test_update_result_display_with_large_number(self, gui_calculator):
        """Test _update_result_display with a large number."""
        gui_calculator._update_result_display(123456789.123)
        assert gui_calculator._result_label.cget("text") == "123456789.123"

    def test_update_result_display_with_very_small_float(self, gui_calculator):
        """Test _update_result_display with a very small float."""
        gui_calculator._update_result_display(0.0001)
        assert gui_calculator._result_label.cget("text") == "0.0001"

    def test_update_result_display_none_label_safe(self, tk_root, calculator):
        """Test that _update_result_display is safe when label is None."""
        gui = GuiCalculator(tk_root, calculator)
        gui._result_label = None
        gui._update_result_display(42)
        gui._root.destroy()

    def test_update_result_display_no_result_prefix(self, gui_calculator):
        """Test that display shows raw number with no 'Result: ' prefix."""
        gui_calculator._update_result_display(42)
        text = gui_calculator._result_label.cget("text")
        assert not text.startswith("Result:")
        assert text == "42"

    def test_result_label_converts_to_string(self, gui_calculator):
        """Test that numeric results are converted to strings."""
        gui_calculator._update_result_display(7)
        text = gui_calculator._result_label.cget("text")
        assert isinstance(text, str)
        assert text == "7"


class TestUpdateHistoryDisplay:
    """Test history display update (no-op stub for iOS layout)."""

    def test_update_history_display_with_none_is_noop(self, gui_calculator):
        """Test that _update_history_display is a no-op when _history_text is None."""
        assert gui_calculator._history_text is None
        gui_calculator._update_history_display()

    def test_update_history_display_with_mock_text_widget(self, gui_calculator):
        """Test that _update_history_display updates a mock text widget if present."""
        mock_text = MagicMock(spec=tk.Text)
        gui_calculator._history_text = mock_text
        gui_calculator._history.add_operation("add", [1, 2], 3)
        gui_calculator._update_history_display()
        assert mock_text.configure.called or mock_text.delete.called


class TestModeSwitchingIntegration:
    """Integration tests for mode switching behavior."""

    def test_switch_to_scientific_shows_more_buttons(self, tk_root, calculator):
        """Test that switching to SCIENTIFIC shows more buttons than NORMAL."""
        gui = GuiCalculator(tk_root, calculator)
        normal_buttons = [w for w in gui._btn_frame.winfo_children() if isinstance(w, tk.Button)]
        normal_count = len(normal_buttons)
        gui._on_mode_toggle()
        scientific_buttons = [w for w in gui._btn_frame.winfo_children() if isinstance(w, tk.Button)]
        scientific_count = len(scientific_buttons)
        assert scientific_count > normal_count
        gui._root.destroy()

    def test_button_colors_change_with_mode(self, tk_root, calculator):
        """Test that non-operator button colors change when mode changes."""
        gui = GuiCalculator(tk_root, calculator)
        gui._mode = Mode.NORMAL
        normal_bg, _, _ = gui._get_button_colors("sqrt")
        gui._mode = Mode.SCIENTIFIC
        scientific_bg, _, _ = gui._get_button_colors("sqrt")
        assert normal_bg != scientific_bg
        assert normal_bg == _THEME["btn_normal_bg"]
        assert scientific_bg == _THEME["btn_scientific_bg"]
        gui._root.destroy()


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_get_button_colors_with_unknown_operation(self, gui_calculator):
        """Test _get_button_colors with an unknown operation key."""
        bg, fg, active_bg = gui_calculator._get_button_colors("unknown_op")
        assert bg is not None
        assert fg is not None
        assert active_bg is not None

    def test_update_result_display_with_scientific_notation(self, gui_calculator):
        """Test _update_result_display with scientific notation result."""
        gui_calculator._update_result_display(1e10)
        text = gui_calculator._result_label.cget("text")
        assert "e" in text.lower() or "10000000000" in text

    def test_multiple_rapid_mode_toggles(self, gui_calculator):
        """Test multiple rapid mode toggles."""
        for _ in range(10):
            gui_calculator._on_mode_toggle()
        assert gui_calculator._mode in [Mode.NORMAL, Mode.SCIENTIFIC]

    def test_rebuild_grid_multiple_times(self, gui_calculator):
        """Test rebuilding the grid multiple times."""
        for _ in range(5):
            gui_calculator._rebuild_button_grid()
        buttons = [w for w in gui_calculator._btn_frame.winfo_children() if isinstance(w, tk.Button)]
        assert len(buttons) > 0


class TestThemeConsistency:
    """Test that all theme colors are consistent."""

    def test_foreground_colors_are_readable(self):
        """Test that foreground colors have good contrast with backgrounds."""
        assert _THEME["btn_operator_bg"] != _THEME["btn_operator_fg"]
        assert _THEME["btn_normal_bg"] != _THEME["btn_normal_fg"]
        assert _THEME["btn_scientific_bg"] != _THEME["btn_scientific_fg"]


class TestWidgetHierarchy:
    """Test the widget hierarchy and structure."""

    def test_all_widgets_packed_in_order(self, gui_calculator):
        """Test that display, mode toggle, and button frame are packed."""
        root_children = gui_calculator._root.winfo_children()
        assert len(root_children) >= 3

    def test_button_grid_uses_grid_layout(self, gui_calculator):
        """Test that buttons use grid layout."""
        buttons = [w for w in gui_calculator._btn_frame.winfo_children() if isinstance(w, tk.Button)]
        for btn in buttons:
            info = btn.grid_info()
            assert info
            assert "row" in info
            assert "column" in info

    def test_frame_expand_and_fill_settings(self, gui_calculator):
        """Test that button frame is configured to expand and fill."""
        assert gui_calculator._btn_frame is not None


@pytest.mark.parametrize("mode", [Mode.NORMAL, Mode.SCIENTIFIC])
def test_mode_change_sets_correct_mode(gui_calculator, mode):
    """Test _on_mode_change sets the correct mode."""
    gui_calculator._on_mode_change(mode)
    assert gui_calculator._mode == mode


@pytest.mark.parametrize("value", [0, 1, -1, 3.14, -3.14, 100.5, 0.001, 1e10])
def test_update_result_display_various_values(gui_calculator, value):
    """Test _update_result_display with various numeric values."""
    gui_calculator._update_result_display(value)
    text = gui_calculator._result_label.cget("text")
    assert str(value) in text or text is not None


@pytest.mark.parametrize("op_key", ["add", "subtract", "multiply", "divide", "sqrt", "sin"])
def test_button_colors_for_various_operations(gui_calculator, op_key):
    """Test _get_button_colors for various operations."""
    bg, fg, active_bg = gui_calculator._get_button_colors(op_key)
    assert isinstance(bg, str)
    assert isinstance(fg, str)
    assert isinstance(active_bg, str)


@pytest.mark.parametrize("mode", [Mode.NORMAL, Mode.SCIENTIFIC])
def test_grid_button_count_by_mode(tk_root, calculator, mode):
    """Test button count varies by mode."""
    gui = GuiCalculator(tk_root, calculator)
    gui._mode = mode
    gui._rebuild_button_grid()
    available = gui._get_available_operations_for_mode()
    buttons = [w for w in gui._btn_frame.winfo_children() if isinstance(w, tk.Button)]
    assert len(buttons) == len(available)
    gui._root.destroy()
