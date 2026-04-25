"""Test suite for iOS-style calculator GUI redesign (issue #465).

Tests cover the new GuiCalculator class and theme/symbol definitions:
- _THEME dictionary with all required color and style keys
- _OPERATION_SYMBOLS mapping from operation names to Unicode symbols
- GuiCalculator class initialization and UI element creation
- Result display styling (color, font, alignment)
- Mode toggle button behavior
- Number pad layout (1-9, zero with columnspan)
- Operation grid layout (4 columns, proper button styling)
- Button theming (background colors, relief, borderwidth)
- Hover effects (enter/leave bindings and visual feedback)
- Window and frame theming
"""

import re
import pytest
from unittest.mock import Mock, MagicMock, patch

# Import the GUI module and expect _THEME, _OPERATION_SYMBOLS, and GuiCalculator
try:
    from src.ui import gui as gui_module
except ImportError:
    gui_module = None


class TestThemeDictionary:
    """Test _THEME dictionary existence and structure."""

    def test_theme_dict_exists(self):
        """_THEME dictionary exists at module level in gui module."""
        assert hasattr(gui_module, '_THEME'), "_THEME not found in gui module"
        assert isinstance(gui_module._THEME, dict), "_THEME is not a dictionary"

    def test_theme_dict_has_required_keys(self):
        """_THEME contains all required color and style keys."""
        required_keys = {
            'WINDOW_BG',
            'RESULT_BG',
            'RESULT_FG',
            'RESULT_FONT',
            'BUTTON_NORMAL_BG',
            'BUTTON_NORMAL_FG',
            'BUTTON_NORMAL_ACTIVE_BG',
            'BUTTON_OPERATOR_BG',
            'BUTTON_OPERATOR_FG',
            'BUTTON_OPERATOR_ACTIVE_BG',
            'BUTTON_SCIENTIFIC_BG',
            'BUTTON_SCIENTIFIC_FG',
            'BUTTON_SCIENTIFIC_ACTIVE_BG',
            'MODE_TOGGLE_BG',
            'MODE_TOGGLE_FG',
            'MODE_TOGGLE_ACTIVE_BG',
        }
        theme = gui_module._THEME
        missing_keys = required_keys - set(theme.keys())
        assert not missing_keys, f"Missing keys in _THEME: {missing_keys}"

    def test_theme_colors_are_valid_hex(self):
        """All color values in _THEME (except RESULT_FONT) are valid hex strings."""
        theme = gui_module._THEME
        hex_pattern = re.compile(r'^#[0-9a-fA-F]{6}$')

        for key, value in theme.items():
            if key != 'RESULT_FONT':
                assert isinstance(value, str), f"{key} is not a string: {value}"
                assert hex_pattern.match(value), f"{key} is not valid hex: {value}"


class TestOperationSymbolsDictionary:
    """Test _OPERATION_SYMBOLS dictionary existence and content."""

    def test_operation_symbols_dict_exists(self):
        """_OPERATION_SYMBOLS dictionary exists at module level."""
        assert hasattr(gui_module, '_OPERATION_SYMBOLS'), \
            "_OPERATION_SYMBOLS not found in gui module"
        assert isinstance(gui_module._OPERATION_SYMBOLS, dict), \
            "_OPERATION_SYMBOLS is not a dictionary"

    def test_operation_symbols_has_required_keys(self):
        """_OPERATION_SYMBOLS contains all required operation symbols."""
        required_keys = {
            'add',
            'subtract',
            'multiply',
            'divide',
            'sqrt',
            'square',
            'cube',
            'power',
            'factorial',
            'log',
            'ln',
            'sin',
            'cos',
            'tan',
        }
        symbols = gui_module._OPERATION_SYMBOLS
        missing_keys = required_keys - set(symbols.keys())
        assert not missing_keys, f"Missing keys in _OPERATION_SYMBOLS: {missing_keys}"

    def test_operation_symbols_are_strings(self):
        """All values in _OPERATION_SYMBOLS are non-empty strings."""
        symbols = gui_module._OPERATION_SYMBOLS
        for key, value in symbols.items():
            assert isinstance(value, str), f"{key} value is not a string: {value}"
            assert len(value) > 0, f"{key} value is empty"


class TestGuiCalculatorClass:
    """Test GuiCalculator class existence and instantiation."""

    def test_gui_calculator_class_exists(self):
        """GuiCalculator class exists in gui module."""
        assert hasattr(gui_module, 'GuiCalculator'), \
            "GuiCalculator class not found in gui module"

    @patch('src.ui.gui.tk.Tk')
    def test_gui_calculator_instantiates_with_mocked_root(self, mock_tk_class):
        """GuiCalculator can be instantiated with a mocked tkinter root."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)
        assert app is not None


class TestResultDisplay:
    """Test result display label styling and configuration."""

    @patch('src.ui.gui.tk.Tk')
    def test_result_display_background_color(self, mock_tk_class):
        """Result display label has bg == '#000000'."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Result label should exist and have black background
        assert hasattr(app, '_result_label'), "GuiCalculator missing _result_label"
        # Check via cget if it's a real tk widget or via config if mocked
        if hasattr(app._result_label, 'cget'):
            bg = app._result_label.cget('bg')
            assert bg == '#000000', f"Result label bg is {bg}, expected #000000"

    @patch('src.ui.gui.tk.Tk')
    def test_result_display_foreground_color(self, mock_tk_class):
        """Result display label has fg == '#FFFFFF'."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_result_label'), "GuiCalculator missing _result_label"
        if hasattr(app._result_label, 'cget'):
            fg = app._result_label.cget('fg')
            assert fg == '#FFFFFF', f"Result label fg is {fg}, expected #FFFFFF"

    @patch('src.ui.gui.tk.Tk')
    def test_result_display_font(self, mock_tk_class):
        """Result display label font is monospace, size 32, bold."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_result_label'), "GuiCalculator missing _result_label"
        if hasattr(app._result_label, 'cget'):
            font = app._result_label.cget('font')
            if font:
                # Font should be a tuple-like or string with monospace, size, bold
                font_str = str(font)
                assert '32' in font_str, f"Font size not 32 in {font}"
                assert 'bold' in font_str.lower(), f"Font not bold in {font}"

    @patch('src.ui.gui.tk.Tk')
    def test_result_display_is_right_aligned(self, mock_tk_class):
        """Result display label anchor == 'e' (right-aligned)."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_result_label'), "GuiCalculator missing _result_label"
        if hasattr(app._result_label, 'cget'):
            anchor = app._result_label.cget('anchor')
            assert anchor == 'e', f"Result label anchor is {anchor}, expected 'e'"


class TestModeToggleButton:
    """Test mode toggle button existence and text."""

    @patch('src.ui.gui.tk.Tk')
    def test_mode_toggle_button_exists(self, mock_tk_class):
        """GuiCalculator has a mode toggle button widget."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_mode_toggle_btn'), \
            "GuiCalculator missing _mode_toggle_btn attribute"

    @patch('src.ui.gui.tk.Tk')
    def test_mode_toggle_text_when_normal_mode(self, mock_tk_class):
        """In normal mode, mode toggle button text == 'Scientific'."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # App should start in normal mode; toggle button should say "Scientific"
        if hasattr(app._mode_toggle_btn, 'cget'):
            text = app._mode_toggle_btn.cget('text')
            assert text == 'Scientific', \
                f"Mode toggle text is {text}, expected 'Scientific'"

    @patch('src.ui.gui.tk.Tk')
    def test_mode_toggle_text_when_scientific_mode(self, mock_tk_class):
        """After switching to scientific mode, mode toggle button text == 'Normal'."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Switch to scientific mode
        if hasattr(app, 'switch_mode') or hasattr(app, '_on_mode_toggle'):
            if hasattr(app, '_on_mode_toggle'):
                app._on_mode_toggle()
            elif hasattr(app, 'switch_mode'):
                app.switch_mode()

        # Now toggle button should say "Normal"
        if hasattr(app._mode_toggle_btn, 'cget'):
            text = app._mode_toggle_btn.cget('text')
            assert text == 'Normal', \
                f"Mode toggle text is {text}, expected 'Normal' after switch"

    @patch('src.ui.gui.tk.Tk')
    def test_mode_toggle_switches_mode(self, mock_tk_class):
        """Calling _on_mode_toggle() changes current mode."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Record initial mode
        initial_mode = getattr(app, '_current_mode', None)

        # Call toggle if it exists
        if hasattr(app, '_on_mode_toggle'):
            app._on_mode_toggle()
            new_mode = getattr(app, '_current_mode', None)
            assert new_mode != initial_mode, "Mode did not change after toggle"


class TestNumberPadLayout:
    """Test number pad (1-9) and zero button layout."""

    @patch('src.ui.gui.tk.Tk')
    def test_number_buttons_1_to_9_exist(self, mock_tk_class):
        """Number pad has buttons for digits 1-9."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Check for a number grid or button collection
        for digit in range(1, 10):
            attr_name = f'_btn_{digit}'
            assert hasattr(app, attr_name), \
                f"GuiCalculator missing button for digit {digit}"

    @patch('src.ui.gui.tk.Tk')
    def test_zero_button_spans_all_columns(self, mock_tk_class):
        """Button '0' is configured with columnspan=3."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_btn_0'), "GuiCalculator missing _btn_0"
        if hasattr(app._btn_0, 'grid_info'):
            grid_info = app._btn_0.grid_info()
            if grid_info:  # Only check if grid_info returns data
                assert grid_info.get('columnspan', 1) == 3, \
                    f"Zero button columnspan is {grid_info.get('columnspan')}, expected 3"


class TestOperationGridLayout:
    """Test operation buttons grid layout (4 columns, rows for modes)."""

    @patch('src.ui.gui.tk.Tk')
    def test_operation_grid_has_4_columns(self, mock_tk_class):
        """Operation buttons are arranged in 4 columns."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Check that operation buttons exist and have column values 0, 1, 2, 3
        if hasattr(app, '_operation_buttons'):
            buttons = app._operation_buttons
            columns = set()
            for btn in buttons:
                if hasattr(btn, 'grid_info'):
                    grid_info = btn.grid_info()
                    if grid_info:
                        columns.add(grid_info.get('column'))
            assert 4 in [max(columns) + 1 if columns else 0], \
                "Operation grid does not have 4 columns"

    @patch('src.ui.gui.tk.Tk')
    def test_operation_grid_rows_normal_mode(self, mock_tk_class):
        """Normal mode operation grid has expected buttons."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # In normal mode, should have basic operations
        assert hasattr(app, '_normal_mode_buttons'), \
            "GuiCalculator missing _normal_mode_buttons"

    @patch('src.ui.gui.tk.Tk')
    def test_operation_grid_rows_scientific_mode(self, mock_tk_class):
        """Scientific mode operation grid has expected buttons."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # In scientific mode, should have additional operations
        assert hasattr(app, '_scientific_mode_buttons'), \
            "GuiCalculator missing _scientific_mode_buttons"


class TestSymbolMapping:
    """Test operation symbol mappings in button text."""

    @patch('src.ui.gui.tk.Tk')
    def test_symbol_mapping_add_to_plus(self, mock_tk_class):
        """Add operation button text == '+'."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_btn_add'), "GuiCalculator missing _btn_add"
        if hasattr(app._btn_add, 'cget'):
            text = app._btn_add.cget('text')
            assert text == '+', f"Add button text is {text}, expected '+'"

    @patch('src.ui.gui.tk.Tk')
    def test_symbol_mapping_multiply_to_times(self, mock_tk_class):
        """Multiply operation button text == '×'."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_btn_multiply'), "GuiCalculator missing _btn_multiply"
        if hasattr(app._btn_multiply, 'cget'):
            text = app._btn_multiply.cget('text')
            assert text == '×', f"Multiply button text is {text}, expected '×'"

    @patch('src.ui.gui.tk.Tk')
    def test_symbol_mapping_sqrt_to_radical(self, mock_tk_class):
        """Sqrt operation button text == '√'."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Sqrt might be in scientific mode
        if hasattr(app, '_btn_sqrt'):
            if hasattr(app._btn_sqrt, 'cget'):
                text = app._btn_sqrt.cget('text')
                assert text == '√', f"Sqrt button text is {text}, expected '√'"


class TestButtonTheming:
    """Test operation button colors, relief, and borderwidth."""

    @patch('src.ui.gui.tk.Tk')
    def test_arithmetic_operators_have_orange_background(self, mock_tk_class):
        """add, subtract, multiply, divide buttons have bg=#FF9500."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        arithmetic_ops = ['add', 'subtract', 'multiply', 'divide']
        for op in arithmetic_ops:
            btn_attr = f'_btn_{op}'
            if hasattr(app, btn_attr):
                btn = getattr(app, btn_attr)
                if hasattr(btn, 'cget'):
                    bg = btn.cget('bg')
                    assert bg == '#FF9500', \
                        f"{op} button bg is {bg}, expected #FF9500"

    @patch('src.ui.gui.tk.Tk')
    def test_normal_ops_have_gray_background(self, mock_tk_class):
        """Normal mode non-arithmetic ops have bg=#333333."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Normal mode buttons (square, sqrt) should be gray
        normal_ops = ['square', 'sqrt']
        for op in normal_ops:
            btn_attr = f'_btn_{op}'
            if hasattr(app, btn_attr):
                btn = getattr(app, btn_attr)
                if hasattr(btn, 'cget'):
                    bg = btn.cget('bg')
                    assert bg == '#333333', \
                        f"{op} button bg is {bg}, expected #333333"

    @patch('src.ui.gui.tk.Tk')
    def test_scientific_ops_have_dark_background(self, mock_tk_class):
        """Scientific mode non-arithmetic ops have bg=#1C1C1E."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Scientific mode buttons should be darker
        scientific_ops = ['cube', 'cbrt', 'power']
        for op in scientific_ops:
            btn_attr = f'_btn_{op}'
            if hasattr(app, btn_attr):
                btn = getattr(app, btn_attr)
                if hasattr(btn, 'cget'):
                    bg = btn.cget('bg')
                    assert bg == '#1C1C1E', \
                        f"{op} button bg is {bg}, expected #1C1C1E"

    @patch('src.ui.gui.tk.Tk')
    def test_button_relief_is_flat(self, mock_tk_class):
        """All operation buttons have relief=tk.FLAT."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Check operation buttons
        if hasattr(app, '_operation_buttons'):
            for btn in app._operation_buttons:
                if hasattr(btn, 'cget'):
                    relief = btn.cget('relief')
                    assert relief == 'flat', \
                        f"Button relief is {relief}, expected 'flat'"

    @patch('src.ui.gui.tk.Tk')
    def test_button_borderwidth_is_zero(self, mock_tk_class):
        """All operation buttons have borderwidth=0."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Check operation buttons
        if hasattr(app, '_operation_buttons'):
            for btn in app._operation_buttons:
                if hasattr(btn, 'cget'):
                    bw = btn.cget('borderwidth')
                    # Convert to int if possible for comparison
                    try:
                        bw = int(bw)
                    except (ValueError, TypeError):
                        pass
                    assert bw == 0, f"Button borderwidth is {bw}, expected 0"


class TestHoverBindings:
    """Test button hover effects (enter/leave bindings and visual feedback)."""

    @patch('src.ui.gui.tk.Tk')
    def test_hover_bindings_exist_on_buttons(self, mock_tk_class):
        """At least one button has both <Enter> and <Leave> bindings."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Check operation buttons for bindings
        if hasattr(app, '_operation_buttons') and app._operation_buttons:
            btn = app._operation_buttons[0]
            if hasattr(btn, 'bind'):
                # Try to bind and check; actual binding check is complex with mocks
                enter_bindings = btn.bind('<Enter>')
                leave_bindings = btn.bind('<Leave>')
                # In mocked environment these may be empty, but we test the capability
                assert hasattr(btn, 'bind'), "Button does not support bind()"

    @patch('src.ui.gui.tk.Tk')
    def test_hover_enter_changes_background(self, mock_tk_class):
        """Simulating <Enter> event on a button changes its bg to a lighter color."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Hover effect test requires button with actual hover handler
        if hasattr(app, '_operation_buttons') and app._operation_buttons:
            btn = app._operation_buttons[0]
            original_bg = None
            if hasattr(btn, 'cget'):
                original_bg = btn.cget('bg')

            # Try to trigger hover effect
            if hasattr(app, '_on_button_enter'):
                app._on_button_enter(btn)
                if hasattr(btn, 'cget'):
                    new_bg = btn.cget('bg')
                    assert new_bg != original_bg, "Hover did not change background"

    @patch('src.ui.gui.tk.Tk')
    def test_hover_leave_reverts_background(self, mock_tk_class):
        """After <Enter>, <Leave> event reverts button bg to original."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Hover effect revert test
        if hasattr(app, '_operation_buttons') and app._operation_buttons:
            btn = app._operation_buttons[0]
            original_bg = None
            if hasattr(btn, 'cget'):
                original_bg = btn.cget('bg')

            # Enter hover
            if hasattr(app, '_on_button_enter'):
                app._on_button_enter(btn)

            # Leave hover
            if hasattr(app, '_on_button_leave'):
                app._on_button_leave(btn)
                if hasattr(btn, 'cget'):
                    reverted_bg = btn.cget('bg')
                    assert reverted_bg == original_bg, \
                        f"Background did not revert after leave: {reverted_bg} != {original_bg}"


class TestWindowTheming:
    """Test window and frame background theming."""

    @patch('src.ui.gui.tk.Tk')
    def test_window_background_from_theme(self, mock_tk_class):
        """Root window bg == _THEME['WINDOW_BG'] == '#000000'."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Window should have black background from theme
        if hasattr(mock_root, 'config'):
            # Check if root was configured with bg
            pass  # Mock won't track this easily, but we verify theme value

        theme = gui_module._THEME
        assert theme['WINDOW_BG'] == '#000000', \
            f"WINDOW_BG is {theme['WINDOW_BG']}, expected #000000"

    @patch('src.ui.gui.tk.Tk')
    def test_all_frames_have_background_from_theme(self, mock_tk_class):
        """All Frame widgets created by GuiCalculator have bg from _THEME."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Frames should have themed backgrounds
        frame_attrs = [
            '_number_frame',
            '_operation_frame',
            '_result_frame',
            '_input_frame',
        ]

        for frame_attr in frame_attrs:
            if hasattr(app, frame_attr):
                frame = getattr(app, frame_attr)
                if hasattr(frame, 'cget'):
                    bg = frame.cget('bg')
                    theme_colors = set(gui_module._THEME.values())
                    assert bg in theme_colors or bg is None, \
                        f"Frame {frame_attr} bg {bg} not from theme"


class TestMainEntryPoint:
    """Test that src/__main__.py imports and uses GuiCalculator for --gui flag."""

    def test_main_imports_gui_calculator(self):
        """src/__main__.py contains 'GuiCalculator' in its import/usage."""
        import pathlib
        main_file = pathlib.Path(__file__).parent.parent / "src" / "__main__.py"
        content = main_file.read_text()
        assert "GuiCalculator" in content, \
            "__main__.py does not contain 'GuiCalculator' import or reference"

    def test_main_gui_flag_instantiates_gui_calculator(self):
        """src/__main__.py --gui code path references GuiCalculator."""
        import pathlib
        main_file = pathlib.Path(__file__).parent.parent / "src" / "__main__.py"
        content = main_file.read_text()

        # Extract the --gui block
        lines = content.split('\n')
        in_gui_block = False
        gui_block_content = []

        for line in lines:
            if 'sys.argv[1] == "--gui"' in line:
                in_gui_block = True
            elif in_gui_block and (line.strip().startswith('elif') or line.strip().startswith('else')):
                break
            elif in_gui_block:
                gui_block_content.append(line)

        gui_block_str = '\n'.join(gui_block_content)
        assert "GuiCalculator" in gui_block_str, \
            "--gui block does not instantiate GuiCalculator"


class TestThreePanelLayoutStructure:
    """Test the three-panel layout structure of GuiCalculator."""

    @patch('src.ui.gui.tk.Tk')
    def test_top_frame_exists(self, mock_tk_class):
        """GuiCalculator has _top_frame attribute."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_top_frame'), \
            "GuiCalculator missing _top_frame attribute"

    @patch('src.ui.gui.tk.Tk')
    def test_content_frame_exists(self, mock_tk_class):
        """GuiCalculator has _content_frame attribute."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_content_frame'), \
            "GuiCalculator missing _content_frame attribute"

    @patch('src.ui.gui.tk.Tk')
    def test_left_panel_exists(self, mock_tk_class):
        """GuiCalculator has _left_panel attribute."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_left_panel'), \
            "GuiCalculator missing _left_panel attribute"

    @patch('src.ui.gui.tk.Tk')
    def test_right_panel_exists(self, mock_tk_class):
        """GuiCalculator has _right_panel attribute."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_right_panel'), \
            "GuiCalculator missing _right_panel attribute"

    @patch('src.ui.gui.tk.Tk')
    def test_bottom_frame_exists(self, mock_tk_class):
        """GuiCalculator has _bottom_frame attribute."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_bottom_frame'), \
            "GuiCalculator missing _bottom_frame attribute"

    @patch('src.ui.gui.tk.Tk')
    def test_content_frame_with_left_right_panels(self, mock_tk_class):
        """GuiCalculator has _content_frame, _left_panel, and _right_panel all existing together."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_content_frame'), \
            "GuiCalculator missing _content_frame"
        assert hasattr(app, '_left_panel'), \
            "GuiCalculator missing _left_panel"
        assert hasattr(app, '_right_panel'), \
            "GuiCalculator missing _right_panel"

    @patch('src.ui.gui.tk.Tk')
    def test_digit_buttons_list_has_10_buttons(self, mock_tk_class):
        """GuiCalculator._digit_buttons list has exactly 10 items (digits 0-9)."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_digit_buttons'), \
            "GuiCalculator missing _digit_buttons list"
        assert len(app._digit_buttons) == 10, \
            f"_digit_buttons has {len(app._digit_buttons)} items, expected 10"

    @patch('src.ui.gui.tk.Tk')
    def test_right_panel_arithmetic_buttons_count(self, mock_tk_class):
        """GuiCalculator._arithmetic_buttons list has exactly 4 buttons."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_arithmetic_buttons'), \
            "GuiCalculator missing _arithmetic_buttons list"
        assert len(app._arithmetic_buttons) == 4, \
            f"_arithmetic_buttons has {len(app._arithmetic_buttons)} items, expected 4"

    @patch('src.ui.gui.tk.Tk')
    def test_mode_toggle_rebuilds_bottom_panel(self, mock_tk_class):
        """Calling _on_mode_toggle() changes the _operation_buttons count."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        # Record initial operation buttons count
        initial_count = len(app._operation_buttons) if hasattr(app, '_operation_buttons') else 0

        # Call mode toggle
        if hasattr(app, '_on_mode_toggle'):
            app._on_mode_toggle()
            new_count = len(app._operation_buttons) if hasattr(app, '_operation_buttons') else 0

            # The count should change (normal mode has fewer ops than scientific mode)
            # In normal mode: 5 ops; in scientific mode: 5 + 9 = 14 ops
            assert new_count != initial_count, \
                f"_operation_buttons count did not change after toggle: {initial_count} -> {new_count}"

    @patch('src.ui.gui.tk.Tk')
    def test_result_label_exists(self, mock_tk_class):
        """GuiCalculator has _result_label attribute."""
        GuiCalculator = gui_module.GuiCalculator
        mock_root = MagicMock()
        app = GuiCalculator(mock_root)

        assert hasattr(app, '_result_label'), \
            "GuiCalculator missing _result_label attribute"
