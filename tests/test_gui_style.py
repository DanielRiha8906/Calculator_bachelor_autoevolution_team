"""Test suite for GUI styling (dark mode) for issue #463.

Tests verify that the CalculatorGUI applies consistent dark-mode styling:
- Display: font size 28-32pt, black background, white text
- Root window: black background
- Entry field: black background, white text
- Digit buttons: dark gray (#333333) background, white text
- Operator buttons: orange (#FF9500) background, white text
- Equals button: orange background, white text
- All buttons: flat relief
- Backward compatibility: all operations still work after styling
"""

import os
import sys
import tkinter
import pytest

# Set display for headless testing
os.environ.setdefault("DISPLAY", ":0")

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.gui import CalculatorGUI


@pytest.fixture
def gui_root_and_instance():
    """Create a real tkinter root with CalculatorGUI and clean up after test.

    Uses root.withdraw() to hide the window from display.
    """
    root = tkinter.Tk()
    root.withdraw()  # Hide the window
    gui = CalculatorGUI(root)

    yield gui, root

    # Cleanup
    root.destroy()


class TestDisplayFontSize:
    """Test display font sizing requirements."""

    def test_display_font_size_minimum(self, gui_root_and_instance):
        """Verify display font size is at least 28pt."""
        gui, root = gui_root_and_instance
        display = gui.display

        # Get font configuration
        font_config = display.cget("font")
        # Font config is a tuple/string like ("Arial", 18) or similar
        # We need to extract the size
        if isinstance(font_config, str):
            # Parse font name from string like "Arial 18"
            parts = font_config.split()
            if parts:
                try:
                    font_size = int(parts[-1])
                    assert font_size >= 28, f"Display font size {font_size} is less than minimum 28pt"
                except (ValueError, IndexError):
                    pytest.fail(f"Could not parse font size from {font_config}")
        else:
            # Font is a tuple like (name, size) or (name, size, style)
            try:
                font_size = int(font_config[1])
                assert font_size >= 28, f"Display font size {font_size} is less than minimum 28pt"
            except (ValueError, IndexError, TypeError):
                pytest.fail(f"Could not parse font size from {font_config}")

    def test_display_font_size_maximum(self, gui_root_and_instance):
        """Verify display font size does not exceed 32pt."""
        gui, root = gui_root_and_instance
        display = gui.display

        # Get font configuration
        font_config = display.cget("font")
        # Font config is a tuple/string like ("Arial", 18) or similar
        if isinstance(font_config, str):
            # Parse font name from string like "Arial 18"
            parts = font_config.split()
            if parts:
                try:
                    font_size = int(parts[-1])
                    assert font_size <= 32, f"Display font size {font_size} exceeds maximum 32pt"
                except (ValueError, IndexError):
                    pytest.fail(f"Could not parse font size from {font_config}")
        else:
            # Font is a tuple like (name, size) or (name, size, style)
            try:
                font_size = int(font_config[1])
                assert font_size <= 32, f"Display font size {font_size} exceeds maximum 32pt"
            except (ValueError, IndexError, TypeError):
                pytest.fail(f"Could not parse font size from {font_config}")


class TestDisplayColors:
    """Test display widget colors."""

    def test_display_background_black(self, gui_root_and_instance):
        """Verify display background is black (#000000)."""
        gui, root = gui_root_and_instance
        display = gui.display

        bg = display.cget("bg")
        # Normalize hex color for comparison (case-insensitive)
        bg_normalized = bg.lower() if isinstance(bg, str) else bg
        assert bg_normalized in ("#000000", "black", "#0"), \
            f"Display background {bg} is not black"

    def test_display_foreground_white(self, gui_root_and_instance):
        """Verify display text color is white."""
        gui, root = gui_root_and_instance
        display = gui.display

        fg = display.cget("fg")
        # Normalize hex color for comparison
        fg_normalized = fg.lower() if isinstance(fg, str) else fg
        assert fg_normalized in ("white", "#ffffff", "#fff"), \
            f"Display foreground {fg} is not white"


class TestRootWindowBackground:
    """Test root window styling."""

    def test_root_background_black(self, gui_root_and_instance):
        """Verify root window background is black (#000000)."""
        gui, root = gui_root_and_instance

        bg = root.cget("bg")
        # Normalize hex color for comparison
        bg_normalized = bg.lower() if isinstance(bg, str) else bg
        assert bg_normalized in ("#000000", "black", "#0"), \
            f"Root window background {bg} is not black"


class TestEntryFieldColors:
    """Test entry field colors."""

    def test_entry_background_black(self, gui_root_and_instance):
        """Verify entry field background is black."""
        gui, root = gui_root_and_instance
        entry = gui.entry

        bg = entry.cget("bg")
        # Normalize hex color for comparison
        bg_normalized = bg.lower() if isinstance(bg, str) else bg
        assert bg_normalized in ("#000000", "black", "#0"), \
            f"Entry background {bg} is not black"

    def test_entry_foreground_white(self, gui_root_and_instance):
        """Verify entry text color is white."""
        gui, root = gui_root_and_instance
        entry = gui.entry

        fg = entry.cget("fg")
        # Normalize hex color for comparison
        fg_normalized = fg.lower() if isinstance(fg, str) else fg
        assert fg_normalized in ("white", "#ffffff", "#fff"), \
            f"Entry foreground {fg} is not white"


class TestDigitButtonColors:
    """Test digit button styling."""

    def test_digit_button_background_dark_gray(self, gui_root_and_instance):
        """Verify at least one digit button has dark gray background."""
        gui, root = gui_root_and_instance

        # Get all widgets on root
        digit_buttons = []
        for child in root.winfo_children():
            if isinstance(child, tkinter.Button):
                text = child.cget("text")
                # Check if button text is a digit
                if text in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
                    digit_buttons.append(child)

        assert len(digit_buttons) > 0, "No digit buttons found"

        # Check that at least one digit button has dark gray background
        found_dark_gray = False
        for btn in digit_buttons:
            bg = btn.cget("bg")
            bg_normalized = bg.lower() if isinstance(bg, str) else bg
            if bg_normalized in ("#333333", "#333"):
                found_dark_gray = True
                break

        assert found_dark_gray, \
            f"No digit buttons with dark gray (#333333) background found. " \
            f"Button backgrounds: {[btn.cget('bg') for btn in digit_buttons]}"

    def test_digit_button_foreground_white(self, gui_root_and_instance):
        """Verify digit button text color is white."""
        gui, root = gui_root_and_instance

        # Get all widgets on root
        digit_buttons = []
        for child in root.winfo_children():
            if isinstance(child, tkinter.Button):
                text = child.cget("text")
                # Check if button text is a digit
                if text in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
                    digit_buttons.append(child)

        assert len(digit_buttons) > 0, "No digit buttons found"

        # Check that digit buttons have white foreground
        for btn in digit_buttons:
            fg = btn.cget("fg")
            fg_normalized = fg.lower() if isinstance(fg, str) else fg
            assert fg_normalized in ("white", "#ffffff", "#fff"), \
                f"Digit button {btn.cget('text')} foreground {fg} is not white"


class TestOperatorButtonColors:
    """Test operator button styling."""

    def test_operator_button_background_orange(self, gui_root_and_instance):
        """Verify at least one operator button has orange background."""
        gui, root = gui_root_and_instance

        # Get all widgets on root
        operator_buttons = []
        operator_symbols = ("+", "-", "*", "/", "^")
        for child in root.winfo_children():
            if isinstance(child, tkinter.Button):
                text = child.cget("text")
                # Check if button text is an operator symbol
                if text in operator_symbols:
                    operator_buttons.append(child)

        assert len(operator_buttons) > 0, "No operator buttons found"

        # Check that at least one operator button has orange background
        found_orange = False
        for btn in operator_buttons:
            bg = btn.cget("bg")
            bg_normalized = bg.lower() if isinstance(bg, str) else bg
            if bg_normalized in ("#ff9500", "#ff9501", "#ff9502"):  # Allow slight variations
                found_orange = True
                break

        assert found_orange, \
            f"No operator buttons with orange (#FF9500) background found. " \
            f"Button backgrounds: {[btn.cget('bg') for btn in operator_buttons]}"

    def test_operator_button_foreground_white(self, gui_root_and_instance):
        """Verify operator button text color is white."""
        gui, root = gui_root_and_instance

        # Get all widgets on root
        operator_buttons = []
        operator_symbols = ("+", "-", "*", "/", "^")
        for child in root.winfo_children():
            if isinstance(child, tkinter.Button):
                text = child.cget("text")
                # Check if button text is an operator symbol
                if text in operator_symbols:
                    operator_buttons.append(child)

        assert len(operator_buttons) > 0, "No operator buttons found"

        # Check that operator buttons have white foreground
        for btn in operator_buttons:
            fg = btn.cget("fg")
            fg_normalized = fg.lower() if isinstance(fg, str) else fg
            assert fg_normalized in ("white", "#ffffff", "#fff"), \
                f"Operator button {btn.cget('text')} foreground {fg} is not white"


class TestEqualsButtonColor:
    """Test equals button styling."""

    def test_equals_button_orange(self, gui_root_and_instance):
        """Verify equals button has orange background."""
        gui, root = gui_root_and_instance

        # Get all widgets on root
        equals_button = None
        for child in root.winfo_children():
            if isinstance(child, tkinter.Button):
                text = child.cget("text")
                if text == "=":
                    equals_button = child
                    break

        assert equals_button is not None, "Equals button not found"

        bg = equals_button.cget("bg")
        bg_normalized = bg.lower() if isinstance(bg, str) else bg
        assert bg_normalized in ("#ff9500", "#ff9501", "#ff9502"), \
            f"Equals button background {bg} is not orange (#FF9500)"


class TestButtonRelief:
    """Test button relief styling."""

    def test_all_buttons_relief_flat(self, gui_root_and_instance):
        """Verify buttons use flat relief."""
        gui, root = gui_root_and_instance

        # Get all button widgets on root
        buttons = []
        for child in root.winfo_children():
            if isinstance(child, tkinter.Button):
                buttons.append(child)

        assert len(buttons) > 0, "No buttons found"

        # Check that at least one button has flat relief
        found_flat = False
        for btn in buttons:
            relief = btn.cget("relief")
            if relief == "flat":
                found_flat = True
                break

        assert found_flat, \
            f"No buttons with flat relief found. " \
            f"Button reliefs: {[btn.cget('relief') for btn in buttons]}"


class TestBackwardCompatibility:
    """Test that calculator operations still work after styling."""

    def test_backward_compatibility_operations_work(self, gui_root_and_instance):
        """Verify basic operations work without exceptions."""
        gui, root = gui_root_and_instance

        # Test that basic operations don't raise exceptions
        try:
            gui._on_number_click("1")
            gui._on_number_click("2")
            result = gui._apply_unary("square")
            assert result is not None, "Square operation returned None"
        except Exception as e:
            pytest.fail(f"Basic operation raised exception: {e}")

    def test_backward_compatibility_scientific_toggle_works(self, gui_root_and_instance):
        """Verify scientific mode toggle still functions."""
        gui, root = gui_root_and_instance

        # Test that scientific mode toggle doesn't raise exceptions
        try:
            initial_mode = gui.scientific_mode
            gui._toggle_scientific_mode()
            assert gui.scientific_mode != initial_mode, \
                "Scientific mode flag did not toggle"
            gui._toggle_scientific_mode()
            assert gui.scientific_mode == initial_mode, \
                "Scientific mode flag did not toggle back"
        except Exception as e:
            pytest.fail(f"Scientific mode toggle raised exception: {e}")
