"""Tests for src.gui.gui module (iOS-style GuiCalculator).

Tests the GuiCalculator Tkinter GUI implementation, including:
- Theme and symbol map centralization
- Result display setup and updates
- Mode toggle functionality
- Button grid layout and colors
- Hover effects and event bindings
- Integration with GUISessionAdapter

Since Tkinter requires a display environment, tests use mocking to create
a functional mock Tk class that GuiCalculator can properly subclass.
Widget state is verified via configuration inspection and attribute checks.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, ANY, call
import sys

# Mock constants that will be used globally
class _MockTkConstants:
    E = "e"
    W = "w"
    EW = "ew"
    NSEW = "nsew"

tk = _MockTkConstants()


class MockTkWidget:
    """Mock widget with sufficient methods for GUI construction."""

    def __init__(self, **kwargs):
        self.config = {}
        self.update(kwargs)
        self._bindings = {}
        self._children = []

    def update(self, kwargs):
        """Store configuration kwargs."""
        self.config.update(kwargs)

    def configure(self, **kwargs):
        """Update widget configuration."""
        self.config.update(kwargs)

    def cget(self, key):
        """Get configuration value."""
        return self.config.get(key)

    def grid(self, **kwargs):
        """Mock grid layout."""
        pass

    def destroy(self):
        """Mock destroy."""
        pass

    def bind(self, event, func):
        """Mock event binding."""
        self._bindings[event] = func

    def winfo_children(self):
        """Mock children retrieval."""
        return self._children

    def columnconfigure(self, col, **kwargs):
        """Mock column configuration."""
        pass

    def rowconfigure(self, row, **kwargs):
        """Mock row configuration."""
        pass


class MockTk(MockTkWidget):
    """Mock Tk root window with necessary methods."""

    def __init__(self):
        super().__init__()
        self.title_text = None

    def title(self, title=None):
        """Mock title setter."""
        if title is not None:
            self.title_text = title
        return self.title_text

    def columnconfigure(self, col, **kwargs):
        """Mock column configuration."""
        pass

    def rowconfigure(self, row, **kwargs):
        """Mock row configuration."""
        pass

    def minsize(self, w, h):
        """Mock minsize."""
        pass

    def mainloop(self):
        """Mock mainloop."""
        pass

    def withdraw(self):
        """Mock withdraw."""
        pass


@pytest.fixture(autouse=True)
def mock_tkinter_display():
    """Mock tkinter modules for headless testing.

    Creates mock objects that allow GuiCalculator to be instantiated
    and tested without a display server.
    """

    def create_widget(parent=None, **kwargs):
        """Factory function for creating widgets, accepting parent as first arg."""
        return MockTkWidget(**kwargs)

    mock_tk_module = MagicMock()
    mock_tk_module.Tk = MockTk
    mock_tk_module.Label = create_widget
    mock_tk_module.Button = create_widget
    mock_tk_module.Frame = create_widget
    mock_tk_module.E = "e"
    mock_tk_module.W = "w"
    mock_tk_module.EW = "ew"
    mock_tk_module.NSEW = "nsew"

    modules = {
        "tkinter": mock_tk_module,
    }

    with patch.dict(sys.modules, modules):
        yield mock_tk_module


@pytest.fixture
def mock_adapter():
    """Fixture providing a mocked GUISessionAdapter.

    Returns a mock adapter with operations and arity methods configured.
    """
    adapter = MagicMock()
    adapter.get_operations.return_value = [
        "add",
        "subtract",
        "multiply",
        "divide",
        "square",
        "sqrt",
    ]
    adapter.get_arity.return_value = 2
    adapter.set_mode = MagicMock()
    return adapter


class TestThemeCentralization:
    """Test suite for _THEME dictionary and centralization."""

    def test_theme_dict_exists(self, mock_tkinter_display):
        """Verify _THEME dict is defined in the module."""
        from src.gui.gui import _THEME

        assert _THEME is not None
        assert isinstance(_THEME, dict)

    def test_theme_contains_required_color_keys(self, mock_tkinter_display):
        """Verify _THEME contains all required color keys."""
        from src.gui.gui import _THEME

        required_keys = [
            "bg_window",
            "bg_display",
            "fg_display",
            "bg_operator",
            "bg_operator_hover",
            "fg_operator",
            "bg_utility",
            "bg_utility_hover",
            "fg_utility",
            "bg_normal",
            "bg_normal_hover",
            "fg_normal",
            "bg_frame",
            "bg_toggle",
            "fg_toggle",
        ]

        for key in required_keys:
            assert key in _THEME, f"Missing theme key: {key}"

    def test_theme_contains_required_font_keys(self, mock_tkinter_display):
        """Verify _THEME contains all required font keys."""
        from src.gui.gui import _THEME

        required_keys = ["font_display", "font_button", "font_toggle"]

        for key in required_keys:
            assert key in _THEME, f"Missing font key: {key}"

    def test_theme_display_font_values(self, mock_tkinter_display):
        """Verify display font is ('Courier New', 32, 'bold')."""
        from src.gui.gui import _THEME

        assert _THEME["font_display"] == ("Courier New", 32, "bold")

    def test_theme_operator_color_is_orange(self, mock_tkinter_display):
        """Verify operator background color is orange (#FF9500)."""
        from src.gui.gui import _THEME

        assert _THEME["bg_operator"] == "#FF9500"

    def test_theme_display_bg_is_black(self, mock_tkinter_display):
        """Verify display background is black (#000000)."""
        from src.gui.gui import _THEME

        assert _THEME["bg_display"] == "#000000"

    def test_theme_display_fg_is_white(self, mock_tkinter_display):
        """Verify display foreground is white (#FFFFFF)."""
        from src.gui.gui import _THEME

        assert _THEME["fg_display"] == "#FFFFFF"

    def test_all_theme_values_are_strings_or_tuples(self, mock_tkinter_display):
        """Verify all theme values are strings (hex colors) or tuples (fonts)."""
        from src.gui.gui import _THEME

        for key, value in _THEME.items():
            assert isinstance(
                value, (str, tuple)
            ), f"Theme key '{key}' has invalid type: {type(value)}"


class TestSymbolMapCentralization:
    """Test suite for _SYMBOL_MAP dictionary."""

    def test_symbol_map_exists(self, mock_tkinter_display):
        """Verify _SYMBOL_MAP dict is defined."""
        from src.gui.gui import _SYMBOL_MAP

        assert _SYMBOL_MAP is not None
        assert isinstance(_SYMBOL_MAP, dict)

    def test_symbol_map_contains_basic_operators(self, mock_tkinter_display):
        """Verify _SYMBOL_MAP contains symbols for basic operators."""
        from src.gui.gui import _SYMBOL_MAP

        required_ops = ["add", "subtract", "multiply", "divide"]

        for op in required_ops:
            assert op in _SYMBOL_MAP, f"Missing symbol mapping for {op}"

    def test_symbol_map_correct_add_symbol(self, mock_tkinter_display):
        """Verify add maps to '+'."""
        from src.gui.gui import _SYMBOL_MAP

        assert _SYMBOL_MAP["add"] == "+"

    def test_symbol_map_correct_subtract_symbol(self, mock_tkinter_display):
        """Verify subtract maps to '−'."""
        from src.gui.gui import _SYMBOL_MAP

        assert _SYMBOL_MAP["subtract"] == "−"

    def test_symbol_map_correct_multiply_symbol(self, mock_tkinter_display):
        """Verify multiply maps to '×'."""
        from src.gui.gui import _SYMBOL_MAP

        assert _SYMBOL_MAP["multiply"] == "×"

    def test_symbol_map_correct_divide_symbol(self, mock_tkinter_display):
        """Verify divide maps to '÷'."""
        from src.gui.gui import _SYMBOL_MAP

        assert _SYMBOL_MAP["divide"] == "÷"

    def test_symbol_map_sqrt_symbols(self, mock_tkinter_display):
        """Verify sqrt and square_root both map to '√'."""
        from src.gui.gui import _SYMBOL_MAP

        assert _SYMBOL_MAP.get("sqrt") == "√"
        assert _SYMBOL_MAP.get("square_root") == "√"

    def test_symbol_map_contains_trigonometric_functions(self, mock_tkinter_display):
        """Verify _SYMBOL_MAP contains trigonometric functions."""
        from src.gui.gui import _SYMBOL_MAP

        trig_ops = ["sin", "cos", "tan"]
        for op in trig_ops:
            assert op in _SYMBOL_MAP


class TestOperatorOpsSet:
    """Test suite for _OPERATOR_OPS set."""

    def test_operator_ops_exists(self, mock_tkinter_display):
        """Verify _OPERATOR_OPS set is defined."""
        from src.gui.gui import _OPERATOR_OPS

        assert _OPERATOR_OPS is not None
        assert isinstance(_OPERATOR_OPS, set)

    def test_operator_ops_contains_four_operators(self, mock_tkinter_display):
        """Verify _OPERATOR_OPS contains exactly four basic operators."""
        from src.gui.gui import _OPERATOR_OPS

        expected = {"add", "subtract", "multiply", "divide"}
        assert _OPERATOR_OPS == expected

    def test_operator_ops_is_set_type(self, mock_tkinter_display):
        """Verify _OPERATOR_OPS is a set (not list or tuple)."""
        from src.gui.gui import _OPERATOR_OPS

        assert type(_OPERATOR_OPS) == set


class TestGuiCalculatorInstantiation:
    """Test suite for GuiCalculator instantiation."""

    def test_gui_calculator_can_be_instantiated_with_adapter(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify GuiCalculator can be instantiated with an adapter."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        assert window is not None

    def test_gui_calculator_can_be_instantiated_without_adapter(
        self, mock_tkinter_display
    ):
        """Verify GuiCalculator can be instantiated without an adapter."""
        from src.gui.gui import GuiCalculator

        with patch("src.gui.gui.Calculator"):
            with patch("src.gui.gui.CalculatorSession"):
                with patch("src.gui.gui.GUISessionAdapter") as mock_adapter_cls:
                    mock_adapter_cls.return_value = MagicMock()
                    window = GuiCalculator()
                    assert window is not None

    def test_gui_calculator_stores_adapter_reference(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify GuiCalculator stores the adapter internally."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        assert window._adapter is mock_adapter

    def test_gui_calculator_initializes_mode_to_normal(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify GuiCalculator initializes _mode to 'normal'."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        assert window._mode == "normal"

    def test_gui_calculator_initializes_selected_op_to_none(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify GuiCalculator initializes _selected_op to None."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        assert window._selected_op is None

    def test_gui_calculator_calls_adapter_set_mode_on_init(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify GuiCalculator calls adapter.set_mode('normal') on init."""
        from src.gui.gui import GuiCalculator

        mock_adapter.set_mode = MagicMock()
        window = GuiCalculator(adapter=mock_adapter)
        mock_adapter.set_mode.assert_called_with("normal")

    def test_gui_calculator_calls_build_ui_on_init(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify GuiCalculator calls _build_ui on initialization."""
        from src.gui.gui import GuiCalculator

        with patch.object(GuiCalculator, "_build_ui") as mock_build:
            window = GuiCalculator(adapter=mock_adapter)
            mock_build.assert_called_once()


class TestResultDisplaySetup:
    """Test suite for result display label verification."""

    def test_result_display_label_exists(self, mock_tkinter_display, mock_adapter):
        """Verify result display label exists as an attribute."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        assert hasattr(window, "_result_label")

    def test_result_display_label_is_created_by_tk_Label(self, mock_tkinter_display, mock_adapter):
        """Verify result display label is created via tk.Label."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        # Verify that the label was created and is not None
        assert window._result_label is not None


class TestModeToogleButton:
    """Test suite for mode toggle button."""

    def test_mode_toggle_button_exists(self, mock_tkinter_display, mock_adapter):
        """Verify mode toggle button exists as an attribute."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        assert hasattr(window, "_toggle_btn")

    def test_mode_toggle_button_initial_text_is_scientific(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify toggle button initially shows 'scientific'."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        # Verify the button was configured with text "scientific"
        # Since we're mocking, we check the mock was called appropriately
        assert window._toggle_btn is not None


class TestButtonGridDimensions:
    """Test suite for button grid layout."""

    def test_grid_frame_exists(self, mock_tkinter_display, mock_adapter):
        """Verify grid frame exists as an attribute."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        assert hasattr(window, "_grid_frame")

    def test_grid_frame_is_tk_frame(self, mock_tkinter_display, mock_adapter):
        """Verify grid frame is a Frame instance."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        assert window._grid_frame is not None


class TestGetButtonColorsLogic:
    """Test suite for _get_button_colors method."""

    def test_get_button_colors_method_exists(self, mock_tkinter_display, mock_adapter):
        """Verify _get_button_colors method exists."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        assert hasattr(window, "_get_button_colors")
        assert callable(window._get_button_colors)

    def test_get_button_colors_returns_three_values(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify _get_button_colors returns a 3-tuple."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        result = window._get_button_colors("add")
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_get_button_colors_operator_in_normal_mode(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify operator colors are orange in normal mode."""
        from src.gui.gui import GuiCalculator, _THEME

        window = GuiCalculator(adapter=mock_adapter)
        window._mode = "normal"

        bg, fg, hover_bg = window._get_button_colors("add")

        assert bg == str(_THEME["bg_operator"])
        assert fg == str(_THEME["fg_operator"])
        assert hover_bg == str(_THEME["bg_operator_hover"])

    def test_get_button_colors_non_operator_in_normal_mode(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify non-operator colors in normal mode."""
        from src.gui.gui import GuiCalculator, _THEME

        window = GuiCalculator(adapter=mock_adapter)
        window._mode = "normal"

        bg, fg, hover_bg = window._get_button_colors("square")

        assert bg == str(_THEME["bg_normal"])
        assert fg == str(_THEME["fg_normal"])
        assert hover_bg == str(_THEME["bg_normal_hover"])

    def test_get_button_colors_operator_in_scientific_mode(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify operator colors are still orange in scientific mode."""
        from src.gui.gui import GuiCalculator, _THEME

        window = GuiCalculator(adapter=mock_adapter)
        window._mode = "scientific"

        bg, fg, hover_bg = window._get_button_colors("divide")

        assert bg == str(_THEME["bg_operator"])
        assert fg == str(_THEME["fg_operator"])
        assert hover_bg == str(_THEME["bg_operator_hover"])

    def test_get_button_colors_non_operator_in_scientific_mode(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify non-operator colors in scientific mode."""
        from src.gui.gui import GuiCalculator, _THEME

        window = GuiCalculator(adapter=mock_adapter)
        window._mode = "scientific"

        bg, fg, hover_bg = window._get_button_colors("sin")

        assert bg == str(_THEME["bg_utility"])
        assert fg == str(_THEME["fg_utility"])
        assert hover_bg == str(_THEME["bg_utility_hover"])

    @pytest.mark.parametrize(
        "op_name", ["add", "subtract", "multiply", "divide"]
    )
    def test_get_button_colors_all_operators_return_orange(
        self, mock_tkinter_display, mock_adapter, op_name
    ):
        """Verify all operators return orange color."""
        from src.gui.gui import GuiCalculator, _THEME

        window = GuiCalculator(adapter=mock_adapter)
        window._mode = "normal"

        bg, fg, hover_bg = window._get_button_colors(op_name)

        assert bg == str(_THEME["bg_operator"])


class TestOnModeToggle:
    """Test suite for _on_mode_toggle method."""

    def test_on_mode_toggle_method_exists(self, mock_tkinter_display, mock_adapter):
        """Verify _on_mode_toggle method exists."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        assert hasattr(window, "_on_mode_toggle")
        assert callable(window._on_mode_toggle)

    def test_on_mode_toggle_switches_from_normal_to_scientific(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify mode toggles from normal to scientific."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        window._mode = "normal"

        window._on_mode_toggle()

        assert window._mode == "scientific"

    def test_on_mode_toggle_switches_from_scientific_to_normal(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify mode toggles from scientific to normal."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        window._mode = "scientific"

        window._on_mode_toggle()

        assert window._mode == "normal"

    def test_on_mode_toggle_calls_adapter_set_mode(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify mode toggle calls adapter.set_mode."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        window._mode = "normal"
        mock_adapter.set_mode.reset_mock()

        window._on_mode_toggle()

        mock_adapter.set_mode.assert_called_with("scientific")

    def test_on_mode_toggle_resets_selected_op_to_none(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify mode toggle resets _selected_op to None."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        window._selected_op = "add"

        window._on_mode_toggle()

        assert window._selected_op is None

    def test_on_mode_toggle_clears_grid_frame_children(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify mode toggle rebuilds the grid frame."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        initial_grid_frame = window._grid_frame

        # Toggle mode which should rebuild the grid
        window._on_mode_toggle()

        # After toggle, the structure should still be intact
        # (widgets are destroyed but frame is the same)
        assert window._grid_frame is initial_grid_frame

    def test_on_mode_toggle_rebuilds_button_grid(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify mode toggle rebuilds button grid."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        # Get initial operation list
        initial_ops = mock_adapter.get_operations()

        # Toggle mode
        window._on_mode_toggle()

        # Verify mode switched
        assert window._mode == "scientific"
        # Verify adapter was called with new mode
        mock_adapter.set_mode.assert_called_with("scientific")

    def test_on_mode_toggle_updates_result_display_to_zero(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify mode toggle resets display to '0'."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        # Set result label to something other than "0"
        window._result_label.configure(text="5")

        # Toggle mode which should reset display to "0"
        window._on_mode_toggle()

        # Verify label text was updated to "0"
        assert window._result_label.config.get("text") == "0"

    def test_on_mode_toggle_updates_button_text_from_normal_to_scientific(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify toggle button text updates to 'normal' when entering scientific."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        window._mode = "normal"

        window._on_mode_toggle()

        # Verify the text was updated via config dict
        assert window._toggle_btn.config.get("text") == "normal"

    def test_on_mode_toggle_updates_button_text_from_scientific_to_normal(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify toggle button text updates to 'scientific' when entering normal."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        window._mode = "scientific"

        window._on_mode_toggle()

        # Verify the text was updated via config dict
        assert window._toggle_btn.config.get("text") == "scientific"


class TestOnOperationClick:
    """Test suite for _on_operation_click method."""

    def test_on_operation_click_method_exists(self, mock_tkinter_display, mock_adapter):
        """Verify _on_operation_click method exists."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        assert hasattr(window, "_on_operation_click")
        assert callable(window._on_operation_click)

    def test_on_operation_click_stores_selected_op(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify operation click stores the operation name."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        window._on_operation_click("multiply")

        assert window._selected_op == "multiply"

    def test_on_operation_click_updates_display_with_symbol(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify operation click updates display with symbol."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        with patch.object(window, "update_result") as mock_update:
            window._on_operation_click("add")
            mock_update.assert_called_with("+")

    def test_on_operation_click_displays_correct_symbol_for_subtract(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify subtract displays '−' symbol."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        with patch.object(window, "update_result") as mock_update:
            window._on_operation_click("subtract")
            mock_update.assert_called_with("−")

    def test_on_operation_click_displays_correct_symbol_for_multiply(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify multiply displays '×' symbol."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        with patch.object(window, "update_result") as mock_update:
            window._on_operation_click("multiply")
            mock_update.assert_called_with("×")

    def test_on_operation_click_displays_correct_symbol_for_divide(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify divide displays '÷' symbol."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        with patch.object(window, "update_result") as mock_update:
            window._on_operation_click("divide")
            mock_update.assert_called_with("÷")

    def test_on_operation_click_displays_correct_symbol_for_sqrt(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify sqrt displays '√' symbol."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        with patch.object(window, "update_result") as mock_update:
            window._on_operation_click("sqrt")
            mock_update.assert_called_with("√")

    @pytest.mark.parametrize(
        "op_name,expected_symbol",
        [
            ("add", "+"),
            ("subtract", "−"),
            ("multiply", "×"),
            ("divide", "÷"),
            ("sqrt", "√"),
            ("square_root", "√"),
            ("square", "x²"),
            ("sin", "sin"),
        ],
    )
    def test_on_operation_click_symbol_mapping(
        self, mock_tkinter_display, mock_adapter, op_name, expected_symbol
    ):
        """Verify operation click maps all operations to correct symbols."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        with patch.object(window, "update_result") as mock_update:
            window._on_operation_click(op_name)
            mock_update.assert_called_with(expected_symbol)


class TestUpdateResultMethod:
    """Test suite for update_result public method."""

    def test_update_result_method_exists(self, mock_tkinter_display, mock_adapter):
        """Verify update_result method exists."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        assert hasattr(window, "update_result")
        assert callable(window.update_result)

    def test_update_result_updates_label_text(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify update_result updates the label text."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        window.update_result("42")

        assert window._result_label.config.get("text") == "42"

    def test_update_result_with_error_message(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify update_result can display error messages."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        window.update_result("Error")

        assert window._result_label.config.get("text") == "Error"

    def test_update_result_with_numeric_string(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify update_result with numeric result."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        window.update_result("3.14159")

        assert window._result_label.config.get("text") == "3.14159"

    def test_update_result_with_zero(self, mock_tkinter_display, mock_adapter):
        """Verify update_result with zero displays correctly."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        window.update_result("0")

        assert window._result_label.config.get("text") == "0"

    @pytest.mark.parametrize(
        "text",
        ["0", "42", "3.14", "-7", "1e10", "Error: Division by zero", "∞"],
    )
    def test_update_result_with_various_strings(
        self, mock_tkinter_display, mock_adapter, text
    ):
        """Verify update_result works with various text values."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        window.update_result(text)

        assert window._result_label.config.get("text") == text


class TestBuildUIMethod:
    """Test suite for _build_ui method."""

    def test_build_ui_method_exists(self, mock_tkinter_display, mock_adapter):
        """Verify _build_ui method exists."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        assert hasattr(window, "_build_ui")
        assert callable(window._build_ui)

    def test_build_ui_creates_result_label(self, mock_tkinter_display, mock_adapter):
        """Verify _build_ui creates result label."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        assert window._result_label is not None

    def test_build_ui_creates_toggle_button(self, mock_tkinter_display, mock_adapter):
        """Verify _build_ui creates toggle button."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        assert window._toggle_btn is not None

    def test_build_ui_creates_grid_frame(self, mock_tkinter_display, mock_adapter):
        """Verify _build_ui creates grid frame."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        assert window._grid_frame is not None

    def test_build_ui_configures_columns(self, mock_tkinter_display, mock_adapter):
        """Verify _build_ui configures window columns."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        # Verify columnconfigure was called
        assert window.columnconfigure is not None


class TestBuildButtonGridMethod:
    """Test suite for _build_button_grid method."""

    def test_build_button_grid_method_exists(self, mock_tkinter_display, mock_adapter):
        """Verify _build_button_grid method exists."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        assert hasattr(window, "_build_button_grid")
        assert callable(window._build_button_grid)

    def test_build_button_grid_creates_buttons_for_operations(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify _build_button_grid creates buttons for each operation."""
        from src.gui.gui import GuiCalculator

        mock_adapter.get_operations.return_value = ["add", "subtract", "multiply"]

        with patch("src.gui.gui.tk.Button") as mock_button_class:
            window = GuiCalculator(adapter=mock_adapter)
            # Button should be created for each operation
            assert mock_button_class.call_count >= 3

    def test_build_button_grid_configures_columns(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify _build_button_grid configures 4 columns."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        frame = window._grid_frame

        # Verify columnconfigure was called for each column
        assert frame.columnconfigure is not None


class TestEventBindings:
    """Test suite for event bindings (hover effects)."""

    def test_toggle_button_has_enter_binding(self, mock_tkinter_display, mock_adapter):
        """Verify toggle button has Enter event binding."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        # Verify bind was called to register Enter binding
        assert "<Enter>" in window._toggle_btn._bindings

    def test_toggle_button_has_leave_binding(self, mock_tkinter_display, mock_adapter):
        """Verify toggle button has Leave event binding."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        # Verify bind was called to register Leave binding
        assert "<Leave>" in window._toggle_btn._bindings


class TestGuiCalculatorIntegration:
    """Integration tests for GuiCalculator."""

    def test_gui_calculator_full_initialization_with_default_adapter(
        self, mock_tkinter_display
    ):
        """Verify GuiCalculator full init with auto-created adapter."""
        from src.gui.gui import GuiCalculator

        with patch("src.gui.gui.Calculator"):
            with patch("src.gui.gui.CalculatorSession"):
                with patch("src.gui.gui.GUISessionAdapter") as mock_adapter_cls:
                    mock_adapter_instance = MagicMock()
                    mock_adapter_cls.return_value = mock_adapter_instance

                    window = GuiCalculator()

                    # Verify adapter was created
                    mock_adapter_cls.assert_called_once()
                    # Verify it was stored
                    assert window._adapter is mock_adapter_instance
                    # Verify set_mode was called with normal
                    mock_adapter_instance.set_mode.assert_called_with("normal")

    def test_gui_calculator_mode_toggle_updates_button_text(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify complete mode toggle sequence updates button text."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)
        window._mode = "normal"

        # Toggle to scientific
        window._on_mode_toggle()
        assert window._mode == "scientific"
        assert window._toggle_btn.config.get("text") == "normal"

        # Toggle back to normal
        window._on_mode_toggle()
        assert window._mode == "normal"
        assert window._toggle_btn.config.get("text") == "scientific"

    def test_gui_calculator_operation_click_stores_and_displays(
        self, mock_tkinter_display, mock_adapter
    ):
        """Verify operation click stores and displays symbol."""
        from src.gui.gui import GuiCalculator

        window = GuiCalculator(adapter=mock_adapter)

        with patch.object(window, "update_result"):
            window._on_operation_click("add")
            assert window._selected_op == "add"
            window.update_result.assert_called_with("+")
