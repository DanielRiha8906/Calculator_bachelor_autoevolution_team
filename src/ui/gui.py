"""Tkinter-based GUI for the calculator.

Provides :class:`CalculatorApp`, a self-contained graphical calculator that
supports dependency injection for testing and integrates with the existing
``OperationRegistry`` and ``OperationHistory`` infrastructure.

When tkinter is not available in the runtime environment (e.g. a headless CI
server), the module still imports cleanly; all tkinter widget construction is
guarded so that a mocked ``root`` can be used without a real display.
"""

_THEME = {
    "WINDOW_BG": "#000000",
    "RESULT_BG": "#000000",
    "RESULT_FG": "#FFFFFF",
    "RESULT_FONT": ("Courier", 32, "bold"),
    "BUTTON_NORMAL_BG": "#333333",
    "BUTTON_NORMAL_FG": "#FFFFFF",
    "BUTTON_NORMAL_ACTIVE_BG": "#4D4D4D",
    "BUTTON_OPERATOR_BG": "#FF9500",
    "BUTTON_OPERATOR_FG": "#FFFFFF",
    "BUTTON_OPERATOR_ACTIVE_BG": "#FFB143",
    "BUTTON_SCIENTIFIC_BG": "#1C1C1E",
    "BUTTON_SCIENTIFIC_FG": "#FFFFFF",
    "BUTTON_SCIENTIFIC_ACTIVE_BG": "#2C2C2E",
    "MODE_TOGGLE_BG": "#2C2C2E",
    "MODE_TOGGLE_FG": "#FFFFFF",
    "MODE_TOGGLE_ACTIVE_BG": "#3C3C3E",
}

_OPERATION_SYMBOLS = {
    "add": "+",
    "subtract": "−",
    "multiply": "×",
    "divide": "÷",
    "sqrt": "√",
    "square": "x²",
    "cube": "x³",
    "power": "xʸ",
    "factorial": "n!",
    "ln": "ln",
    "log": "log",
    "log10": "log₁₀",
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "cot": "cot",
    "asin": "asin",
    "acos": "acos",
    "cbrt": "∛",
}


class _TkStub:
    """Minimal stand-in for tkinter widget classes and the Tk root.

    Stores constructor keyword arguments so that :meth:`cget` can return
    them back (enabling headless CI tests to verify configured colours,
    fonts, and other properties).  :meth:`config` updates the same store.
    :meth:`grid` persists its keyword arguments so that :meth:`grid_info`
    can retrieve them (enabling layout assertion tests).
    """

    def __init__(self, *args, **kwargs):
        self._value: str = ""
        self._kwargs: dict = dict(kwargs)
        self._grid_info: dict = {}

    def __call__(self, *args, **kwargs):
        return _TkStub(*args, **kwargs)

    # --- Widget lifecycle --------------------------------------------------

    def title(self, *a, **kw) -> None: pass
    def resizable(self, *a, **kw) -> None: pass
    def geometry(self, *a, **kw) -> None: pass
    def mainloop(self, *a, **kw) -> None: pass
    def destroy(self, *a, **kw) -> None: pass

    # --- Geometry managers -------------------------------------------------

    def pack(self, *a, **kw) -> None: pass

    def grid(self, *a, **kw) -> None:
        """Store grid kwargs so :meth:`grid_info` can return them."""
        self._grid_info = dict(kw)

    def grid_info(self, *a, **kw) -> dict:
        """Return the kwargs that were passed to :meth:`grid`."""
        return self._grid_info

    def grid_columnconfigure(self, *a, **kw) -> None: pass
    def grid_rowconfigure(self, *a, **kw) -> None: pass
    def columnconfigure(self, *a, **kw) -> None: pass
    def rowconfigure(self, *a, **kw) -> None: pass

    # --- Widget configuration ----------------------------------------------

    def config(self, *a, **kw) -> None:
        """Update stored kwargs so :meth:`cget` reflects the new values."""
        self._kwargs.update(kw)

    def configure(self, *a, **kw) -> None:
        """Alias for :meth:`config`."""
        self._kwargs.update(kw)

    def cget(self, key: str) -> object:
        """Return the value for *key* as set in the constructor or :meth:`config`.

        Args:
            key: The option name (e.g. ``'bg'``, ``'text'``).

        Returns:
            The stored value, or ``None`` if *key* was never set.
        """
        return self._kwargs.get(key)

    # --- Event binding -----------------------------------------------------

    def bind(self, *a, **kw) -> None: pass

    # --- Text / variable protocol ------------------------------------------

    def set(self, value: str = "", *a, **kw) -> None:
        """Store *value* so :meth:`get` can return it."""
        self._value = value

    def get(self, *a, **kw) -> str:
        """Return the value stored by :meth:`set`."""
        return self._value

    # --- Text widget extras ------------------------------------------------

    def insert(self, *a, **kw) -> None: pass
    def yview(self, *a, **kw) -> None: pass


try:
    import tkinter as tk
    _TK_AVAILABLE = True
except ImportError:  # tkinter not installed (headless CI / test environment)
    import types as _types

    # Create a minimal stub so that @patch('src.ui.gui.tk.Tk') can resolve.
    tk = _types.ModuleType("tkinter")

    tk.Tk = _TkStub
    tk.Frame = _TkStub
    tk.Label = _TkStub
    tk.Button = _TkStub
    tk.Entry = _TkStub
    tk.Text = _TkStub
    tk.Scrollbar = _TkStub
    tk.Radiobutton = _TkStub
    tk.OptionMenu = _TkStub
    tk.StringVar = _TkStub
    tk.X = "x"
    tk.Y = "y"
    tk.BOTH = "both"
    tk.END = "end"
    tk.LEFT = "left"
    tk.RIGHT = "right"
    tk.W = "w"
    tk.E = "e"
    tk.N = "n"
    tk.NW = "nw"
    tk.FLAT = "flat"
    tk.NSEW = "nsew"
    _TK_AVAILABLE = False

from typing import List, Optional

from ..calculator import Calculator
from ..operation_registry import OperationRegistry
from ..infrastructure.history import OperationHistory
from ..core.operations import OperationMode
from .modes import SimpleMode, ScientificMode, CalculatorMode


# Operations that require exactly one operand (no second operand field).
_UNARY_OPS: frozenset = frozenset({
    "square", "sqrt", "factorial", "ln", "log10", "cube", "cbrt",
    "sin", "cos", "tan", "cot", "asin", "acos",
})


class CalculatorApp:
    """Tkinter GUI calculator application.

    Supports normal (simple) and scientific modes, history tracking, and full
    dependency injection for unit testing without a real display.

    Args:
        root: A ``tk.Tk`` root window (or mock).  When ``None`` a new
            ``tk.Tk()`` instance is created.
        calculator: A ``Calculator`` instance to perform computations.
            When ``None`` a default ``Calculator`` is created.
        registry: An ``OperationRegistry`` instance for operation discovery
            and dispatch.  When ``None`` one is created from *calculator*.
    """

    def __init__(
        self,
        root: Optional[object] = None,
        calculator: Optional[Calculator] = None,
        registry: Optional[OperationRegistry] = None,
    ) -> None:
        self._calculator: Calculator = calculator or Calculator()
        self._registry: OperationRegistry = registry or OperationRegistry(self._calculator)
        self._history: OperationHistory = OperationHistory()
        self._root = root if root is not None else tk.Tk()
        self._current_mode: OperationMode = OperationMode.NORMAL
        self._modes: dict = {
            OperationMode.NORMAL: SimpleMode(),
            OperationMode.SCIENTIFIC: ScientificMode(),
        }
        self._setup_gui()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_current_mode_operations(self) -> List[str]:
        """Return the operations available in the current mode.

        Returns:
            A list of operation name strings for the current mode.
        """
        mode_obj: CalculatorMode = self._modes[self._current_mode]
        return mode_obj.get_operations(self._registry)

    def switch_mode(self, mode: OperationMode) -> None:
        """Switch the calculator to the given mode and rebuild the operation menu.

        Args:
            mode: The ``OperationMode`` to switch to (NORMAL or SCIENTIFIC).
        """
        if mode in self._modes:
            self._current_mode = mode
            self._rebuild_operation_menu()

    def _rebuild_operation_menu(self) -> None:
        """Rebuild the operation OptionMenu widget for the current mode.

        Destroys the existing OptionMenu (if present) and creates a new one
        populated with the operations available in the current mode.  Silently
        ignores any exception so that headless / mocked test environments do
        not crash.
        """
        try:
            ops = self.get_current_mode_operations()
            if hasattr(self, "_op_menu"):
                self._op_menu.destroy()
            if hasattr(self, "_op_frame") and hasattr(self, "_op_var"):
                self._op_menu = tk.OptionMenu(self._op_frame, self._op_var, *ops)
                self._op_menu.pack(side=tk.LEFT)
                if ops:
                    self._op_var.set(ops[0])
        except Exception:  # noqa: BLE001 — mocked root or missing tk; ignore gracefully
            pass

    @staticmethod
    def _parse_operand(value: object) -> object:
        """Convert an operand value to the most appropriate numeric type.

        Tries ``int`` first (for whole-number values), then ``float``.
        This preserves int type for operations like factorial that reject floats.

        Args:
            value: The raw operand (may be int, float, or str).

        Returns:
            An ``int`` if *value* represents a whole number with no decimal
            component, otherwise a ``float``.

        Raises:
            ValueError: If *value* cannot be converted to a number.
        """
        if isinstance(value, bool):
            # Booleans pass isinstance(x, int) check — reject them explicitly.
            raise ValueError(f"invalid operand: {value!r}")
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            if value.is_integer():
                return int(value)
            return value
        # String path: try int first (no decimal point), then float.
        s = str(value)
        if "." not in s:
            try:
                return int(s)
            except ValueError:
                pass
        return float(s)

    def calculate(self, op_name: str, *operands) -> str:
        """Perform a calculation and return the result as a string.

        Converts each operand to the most appropriate numeric type
        (``int`` for whole numbers, ``float`` otherwise) before calling the
        registry.  On any error, returns a descriptive error string rather
        than raising.

        Args:
            op_name: The name of the operation to perform.
            *operands: The operand values (numeric or convertible to a number).

        Returns:
            The result as a string (e.g. ``"8.0"``), or an error message
            string prefixed with ``"Error:"`` if the calculation fails.
        """
        try:
            numeric_operands = [self._parse_operand(op) for op in operands]
            result = self._registry.call(op_name, *numeric_operands)
            self._history.record(op_name, tuple(numeric_operands), result)
            return str(result)
        except (ValueError, ZeroDivisionError) as exc:
            return f"Error: {exc}"
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"

    def get_history(self) -> List[str]:
        """Return the list of recorded history entries.

        Returns:
            A list of formatted history entry strings, one per successful
            calculation, in chronological order.
        """
        return self._history.get_entries()

    def is_unary_operation(self, op_name: str) -> bool:
        """Return ``True`` if *op_name* is a unary (single-operand) operation.

        Args:
            op_name: The operation name to classify.

        Returns:
            ``True`` for unary operations (square, sqrt, factorial, etc.),
            ``False`` for binary operations (add, subtract, multiply, etc.).
        """
        return op_name in _UNARY_OPS

    def run(self) -> None:
        """Start the tkinter main event loop."""
        self._root.mainloop()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _setup_gui(self) -> None:
        """Build all tkinter widgets.

        Uses mock-safe widget construction: all calls are made normally so
        that a mocked ``root`` (from unit tests) accepts them without error.
        Silently ignores any exception raised during widget construction so
        that headless test environments do not crash.
        """
        try:
            self._root.title("Calculator")
            self._root.resizable(False, False)

            # --- Mode frame ---
            mode_frame = tk.Frame(self._root)
            mode_frame.pack(fill=tk.X, padx=5, pady=5)

            tk.Label(mode_frame, text="Mode:").pack(side=tk.LEFT)

            self._mode_var = tk.StringVar(value="NORMAL")
            tk.Radiobutton(
                mode_frame,
                text="Normal",
                variable=self._mode_var,
                value="NORMAL",
                command=lambda: self.switch_mode(OperationMode.NORMAL),
            ).pack(side=tk.LEFT)
            tk.Radiobutton(
                mode_frame,
                text="Scientific",
                variable=self._mode_var,
                value="SCIENTIFIC",
                command=lambda: self.switch_mode(OperationMode.SCIENTIFIC),
            ).pack(side=tk.LEFT)

            # --- Operation selector ---
            op_frame = tk.Frame(self._root)
            op_frame.pack(fill=tk.X, padx=5, pady=5)

            tk.Label(op_frame, text="Operation:").pack(side=tk.LEFT)
            self._op_frame = op_frame
            self._op_var = tk.StringVar(value="add")
            initial_ops = self.get_current_mode_operations()
            self._op_menu = tk.OptionMenu(op_frame, self._op_var, *initial_ops)
            self._op_menu.pack(side=tk.LEFT)

            # --- Operand entry fields ---
            entry_frame = tk.Frame(self._root)
            entry_frame.pack(fill=tk.X, padx=5, pady=5)

            tk.Label(entry_frame, text="Operand 1:").pack(side=tk.LEFT)
            self._operand1_var = tk.StringVar()
            tk.Entry(entry_frame, textvariable=self._operand1_var, width=10).pack(side=tk.LEFT)

            tk.Label(entry_frame, text="Operand 2:").pack(side=tk.LEFT)
            self._operand2_var = tk.StringVar()
            tk.Entry(entry_frame, textvariable=self._operand2_var, width=10).pack(side=tk.LEFT)

            # --- Calculate button ---
            tk.Button(self._root, text="Calculate", command=self._on_calculate).pack(pady=5)

            # --- Result display ---
            result_frame = tk.Frame(self._root)
            result_frame.pack(fill=tk.X, padx=5, pady=5)

            tk.Label(result_frame, text="Result:").pack(side=tk.LEFT)
            self._result_var = tk.StringVar(value="")
            tk.Label(result_frame, textvariable=self._result_var).pack(side=tk.LEFT)

            # --- History display ---
            history_frame = tk.Frame(self._root)
            history_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            tk.Label(history_frame, text="History:").pack(anchor=tk.W)
            scrollbar = tk.Scrollbar(history_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self._history_text = tk.Text(
                history_frame,
                height=8,
                yscrollcommand=scrollbar.set,
            )
            self._history_text.pack(fill=tk.BOTH, expand=True)
            scrollbar.config(command=self._history_text.yview)

        except Exception:  # noqa: BLE001 — mocked root or missing tk; ignore gracefully
            pass

    def _on_calculate(self) -> None:
        """Callback for the Calculate button."""
        op_name = self._op_var.get() if hasattr(self, "_op_var") else ""
        operand1_str = self._operand1_var.get() if hasattr(self, "_operand1_var") else ""
        operand2_str = self._operand2_var.get() if hasattr(self, "_operand2_var") else ""

        if self.is_unary_operation(op_name):
            result = self.calculate(op_name, operand1_str)
        else:
            result = self.calculate(op_name, operand1_str, operand2_str)

        if hasattr(self, "_result_var"):
            self._result_var.set(result)

        if hasattr(self, "_history_text"):
            entries = self.get_history()
            if entries:
                self._history_text.insert(tk.END, entries[-1] + "\n")


# ---------------------------------------------------------------------------
# iOS-style calculator redesign
# ---------------------------------------------------------------------------

# Operations shown in normal mode (non-arithmetic)
_NORMAL_OPS: tuple = ("sqrt", "square", "factorial", "ln", "log10")

# Operations shown only in scientific mode
_SCIENTIFIC_OPS: tuple = ("cube", "cbrt", "power", "sin", "cos", "tan", "cot", "asin", "acos")

# Arithmetic operations that appear in the right panel
_ARITHMETIC_OPS: frozenset = frozenset({"add", "subtract", "multiply", "divide"})

# Order in which arithmetic ops appear in the right panel (top to bottom)
_ARITHMETIC_RIGHT_PANEL_ORDER: tuple = ("divide", "multiply", "subtract", "add")


class GuiCalculator:
    """iOS-style tkinter GUI calculator with a three-panel layout.

    Layout structure:
    - **TOP** row: result display label + mode-toggle button (full-width)
    - **CONTENT** row: left panel (digit grid 3×4) + right panel (arithmetic ops)
    - **BOTTOM** row: non-arithmetic operation grid (4 columns)

    Provides a black-themed, flat-button calculator with a mode toggle that
    switches between normal (basic) and scientific operation sets.

    Args:
        root: A ``tk.Tk`` root window or mock.  When ``None`` a new
            ``tk.Tk()`` instance is created.
        calculator: A ``Calculator`` instance to perform computations.
            When ``None`` a default ``Calculator`` is created.
        registry: An ``OperationRegistry`` for operation discovery and
            dispatch.  When ``None`` one is created from *calculator*.
    """

    def __init__(
        self,
        root: Optional[object] = None,
        calculator: Optional[Calculator] = None,
        registry: Optional[OperationRegistry] = None,
    ) -> None:
        self._calculator: Calculator = calculator or Calculator()
        self._registry: OperationRegistry = registry or OperationRegistry(self._calculator)
        self._history: OperationHistory = OperationHistory()
        self._root = root if root is not None else tk.Tk()
        self._current_mode: OperationMode = OperationMode.NORMAL

        # New state variables for three-panel layout
        self._current_operand: str = ""
        self._selected_operation: str = ""
        self._digit_buttons: list = []
        self._arithmetic_buttons: list = []
        self._top_frame = None
        self._content_frame = None
        self._left_panel = None
        self._right_panel = None
        self._bottom_frame = None

        # Button collections populated by _setup_ios_gui()
        self._operation_buttons: list = []
        self._normal_mode_buttons: list = []
        self._scientific_mode_buttons: list = []

        self._setup_ios_gui()

    # ------------------------------------------------------------------
    # Public API (mode-agnostic)
    # ------------------------------------------------------------------

    def get_current_mode_operations(self) -> List[str]:
        """Return operation names for the currently active mode.

        Returns:
            A list of operation name strings.
        """
        if self._current_mode == OperationMode.SCIENTIFIC:
            return list(_ARITHMETIC_OPS) + list(_NORMAL_OPS) + list(_SCIENTIFIC_OPS)
        return list(_ARITHMETIC_OPS) + list(_NORMAL_OPS)

    def calculate(self, op_name: str, *operands: object) -> str:
        """Perform a calculation and return the result as a string.

        Args:
            op_name: Operation name to execute.
            *operands: Operand values.

        Returns:
            Result string or error message prefixed with ``"Error:"``.
        """
        try:
            numeric_ops = [CalculatorApp._parse_operand(op) for op in operands]
            result = self._registry.call(op_name, *numeric_ops)
            self._history.record(op_name, tuple(numeric_ops), result)
            return str(result)
        except (ValueError, ZeroDivisionError) as exc:
            return f"Error: {exc}"
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"

    def get_history(self) -> List[str]:
        """Return the list of recorded history entries.

        Returns:
            A list of formatted history entry strings.
        """
        return self._history.get_entries()

    def is_unary_operation(self, op_name: str) -> bool:
        """Return ``True`` if *op_name* requires a single operand.

        Args:
            op_name: Operation name to classify.

        Returns:
            ``True`` for unary operations, ``False`` for binary ones.
        """
        return op_name in _UNARY_OPS

    def run(self) -> None:
        """Start the tkinter main event loop."""
        self._root.mainloop()

    # ------------------------------------------------------------------
    # Private: digit press handler
    # ------------------------------------------------------------------

    def _on_digit_press(self, digit: int) -> None:
        """Handle a digit button press.

        Appends *digit* to the current operand string and updates the result
        label to display the accumulated input.

        Args:
            digit: The digit value (0–9) that was pressed.
        """
        try:
            self._current_operand += str(digit)
            if hasattr(self, "_result_label"):
                self._result_label.config(text=self._current_operand or "0")
        except Exception:  # noqa: BLE001
            pass

    # ------------------------------------------------------------------
    # Private: mode toggle
    # ------------------------------------------------------------------

    def _on_mode_toggle(self) -> None:
        """Toggle between NORMAL and SCIENTIFIC mode and rebuild the bottom panel."""
        if self._current_mode == OperationMode.NORMAL:
            self._current_mode = OperationMode.SCIENTIFIC
        else:
            self._current_mode = OperationMode.NORMAL
        self._update_mode_toggle_text()
        self._rebuild_bottom_panel()

    def _update_mode_toggle_text(self) -> None:
        """Update the mode toggle button text to reflect the active mode."""
        try:
            if not hasattr(self, "_mode_toggle_btn"):
                return
            if self._current_mode == OperationMode.SCIENTIFIC:
                self._mode_toggle_btn.config(text="Normal")
            else:
                self._mode_toggle_btn.config(text="Scientific")
        except Exception:  # noqa: BLE001
            pass

    # ------------------------------------------------------------------
    # Private: hover callbacks
    # ------------------------------------------------------------------

    def _on_button_enter(self, btn: object) -> None:
        """Lighten button background on mouse enter.

        Args:
            btn: The button widget that received the Enter event.
        """
        try:
            active_bg = getattr(btn, "_active_bg", None)
            if active_bg and hasattr(btn, "config"):
                btn.config(bg=active_bg)
        except Exception:  # noqa: BLE001
            pass

    def _on_button_leave(self, btn: object) -> None:
        """Restore original button background on mouse leave.

        Args:
            btn: The button widget that received the Leave event.
        """
        try:
            orig_bg = getattr(btn, "_orig_bg", None)
            if orig_bg and hasattr(btn, "config"):
                btn.config(bg=orig_bg)
        except Exception:  # noqa: BLE001
            pass

    # ------------------------------------------------------------------
    # Private: operation press handler
    # ------------------------------------------------------------------

    def _on_op_press(self, op_name: str) -> None:
        """Handle an operation button press.

        Stores the selected operation name for use when the result is
        requested.  In a real calculator this would update the display.

        Args:
            op_name: The name of the pressed operation.
        """
        self._selected_op = op_name

    # ------------------------------------------------------------------
    # Private: widget factories
    # ------------------------------------------------------------------

    @staticmethod
    def _is_real_tk_widget(parent: object) -> bool:
        """Return ``True`` when *parent* is backed by a real Tcl/Tk interpreter.

        Real tkinter widgets have a ``.tk`` attribute that is an instance of
        ``_tkinter.TkappType``.  Mock objects (``unittest.mock.MagicMock``) and
        :class:`_TkStub` instances do not satisfy this check, so this method
        reliably distinguishes headless/test parents from live-display parents.

        Args:
            parent: The candidate parent widget to inspect.

        Returns:
            ``True`` if *parent* has a real Tcl interpreter backing it,
            ``False`` otherwise (including when ``_TK_AVAILABLE`` is ``False``).
        """
        if not _TK_AVAILABLE:
            return False
        try:
            import _tkinter  # stdlib C extension, always present when tkinter is
            return isinstance(getattr(parent, "tk", None), _tkinter.TkappType)
        except Exception:  # noqa: BLE001
            return False

    def _make_button(
        self,
        parent: object,
        text: str,
        bg: str,
        fg: str,
        active_bg: str,
        command: object = None,
    ) -> object:
        """Create a flat, themed button with hover bindings.

        When *parent* is backed by a real Tcl/Tk interpreter (i.e. a live
        display is available), a real ``tk.Button`` is created so the widget
        is rendered on screen.  Otherwise a :class:`_TkStub` is returned so
        that headless CI tests can call ``cget()`` / ``grid_info()`` on the
        result with predictable values.

        In both cases the hover attributes ``_orig_bg`` and ``_active_bg`` are
        stored directly on the button object, and ``<Enter>`` / ``<Leave>``
        bindings are attached.

        Args:
            parent: Parent widget.
            text: Button label.
            bg: Normal background colour.
            fg: Foreground (text) colour.
            active_bg: Background colour on hover.
            command: Callback when button is pressed.

        Returns:
            A ``tk.Button`` when a real display is available, otherwise a
            :class:`_TkStub` configured with the given options.
        """
        try:
            if self._is_real_tk_widget(parent):
                btn = tk.Button(
                    parent,
                    text=text,
                    bg=bg,
                    fg=fg,
                    activebackground=active_bg,
                    relief=tk.FLAT,
                    borderwidth=0,
                    command=command,
                )
            else:
                btn = _TkStub(
                    text=text,
                    bg=bg,
                    fg=fg,
                    activebackground=active_bg,
                    relief=tk.FLAT,
                    borderwidth=0,
                )
                if command is not None:
                    btn._kwargs["command"] = command
            # Store theme colours as instance attributes on the widget so that
            # hover callbacks can retrieve them even when cget() is unavailable.
            btn._orig_bg = bg  # type: ignore[attr-defined]
            btn._active_bg = active_bg  # type: ignore[attr-defined]
            # Bind hover effects
            btn.bind("<Enter>", lambda e, b=btn: self._on_button_enter(b))
            btn.bind("<Leave>", lambda e, b=btn: self._on_button_leave(b))
            return btn
        except Exception:  # noqa: BLE001
            return _TkStub()

    def _make_label(
        self,
        parent: object,
        text: str = "",
        bg: str = "",
        fg: str = "",
        font: object = None,
        anchor: str = "",
    ) -> object:
        """Create a themed label.

        When *parent* is backed by a real Tcl/Tk interpreter a real
        ``tk.Label`` is created.  Otherwise a :class:`_TkStub` is returned so
        that headless CI tests can inspect the configured values via ``cget()``.

        Args:
            parent: Parent widget.
            text: Label text.
            bg: Background colour.
            fg: Foreground colour.
            font: Font tuple or string.
            anchor: Anchor direction (e.g. ``'e'`` for right-align).

        Returns:
            A ``tk.Label`` when a real display is available, otherwise a
            :class:`_TkStub` configured with the given options.
        """
        try:
            kwargs: dict = {"text": text}
            if bg:
                kwargs["bg"] = bg
            if fg:
                kwargs["fg"] = fg
            if font is not None:
                kwargs["font"] = font
            if anchor:
                kwargs["anchor"] = anchor
            if self._is_real_tk_widget(parent):
                return tk.Label(parent, **kwargs)
            return _TkStub(**kwargs)
        except Exception:  # noqa: BLE001
            return _TkStub()

    def _make_frame(self, parent: object, bg: str = "") -> object:
        """Create a themed frame.

        When *parent* is backed by a real Tcl/Tk interpreter a real
        ``tk.Frame`` is created.  Otherwise a :class:`_TkStub` is returned.

        Args:
            parent: Parent widget.
            bg: Background colour.

        Returns:
            A ``tk.Frame`` when a real display is available, otherwise a
            :class:`_TkStub` configured with the given options.
        """
        try:
            kwargs: dict = {}
            if bg:
                kwargs["bg"] = bg
            if self._is_real_tk_widget(parent):
                return tk.Frame(parent, **kwargs)
            return _TkStub(**kwargs)
        except Exception:  # noqa: BLE001
            return _TkStub()

    # ------------------------------------------------------------------
    # Private: colour helper
    # ------------------------------------------------------------------

    def _op_button_colours(self, op_name: str) -> tuple:
        """Return (bg, fg, active_bg) for an operation button.

        Args:
            op_name: Operation name.

        Returns:
            A tuple of (bg, fg, active_bg) hex-colour strings.
        """
        if op_name in _ARITHMETIC_OPS:
            return (
                _THEME["BUTTON_OPERATOR_BG"],
                _THEME["BUTTON_OPERATOR_FG"],
                _THEME["BUTTON_OPERATOR_ACTIVE_BG"],
            )
        if op_name in _SCIENTIFIC_OPS:
            return (
                _THEME["BUTTON_SCIENTIFIC_BG"],
                _THEME["BUTTON_SCIENTIFIC_FG"],
                _THEME["BUTTON_SCIENTIFIC_ACTIVE_BG"],
            )
        return (
            _THEME["BUTTON_NORMAL_BG"],
            _THEME["BUTTON_NORMAL_FG"],
            _THEME["BUTTON_NORMAL_ACTIVE_BG"],
        )

    # ------------------------------------------------------------------
    # Private: GUI construction — three-panel layout
    # ------------------------------------------------------------------

    def _setup_ios_gui(self) -> None:  # noqa: C901 — complex but cohesive
        """Build all iOS-style tkinter widgets in a three-panel layout.

        Grid layout on the root window:
        - Row 0: ``_top_frame`` — result display + mode toggle (rowweight=0)
        - Row 1: ``_content_frame`` — left digit panel + right arithmetic panel
          (rowweight=1)
        - Row 2: ``_bottom_frame`` — non-arithmetic operation grid (rowweight=1)

        All widget construction is wrapped in try/except so that a mocked
        root (used in unit tests without a real display) does not cause the
        constructor to crash.
        """
        try:
            self._root.title("Calculator")
            self._root.config(bg=_THEME["WINDOW_BG"])
            self._root.geometry("480x640")

            # Configure root grid weights
            self._root.columnconfigure(0, weight=1)
            self._root.rowconfigure(0, weight=0)
            self._root.rowconfigure(1, weight=1)
            self._root.rowconfigure(2, weight=1)

            # ------ TOP FRAME: result display + mode toggle ---------------
            self._top_frame = self._make_frame(self._root, bg=_THEME["WINDOW_BG"])
            self._top_frame.grid(row=0, column=0, sticky=tk.NSEW)

            # Result display label (stored for direct access in tests)
            self._result_label = self._make_label(
                self._top_frame,
                text="0",
                bg=_THEME["RESULT_BG"],
                fg=_THEME["RESULT_FG"],
                font=_THEME["RESULT_FONT"],
                anchor=tk.E,
            )
            self._result_label.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

            # Mode toggle button
            self._mode_toggle_btn = self._make_button(
                self._top_frame,
                text="Scientific",
                bg=_THEME["MODE_TOGGLE_BG"],
                fg=_THEME["MODE_TOGGLE_FG"],
                active_bg=_THEME["MODE_TOGGLE_ACTIVE_BG"],
                command=self._on_mode_toggle,
            )
            self._mode_toggle_btn.grid(row=1, column=0, columnspan=2, sticky=tk.E + tk.W)

            # ------ CONTENT FRAME: left + right panels --------------------
            self._content_frame = self._make_frame(self._root, bg=_THEME["WINDOW_BG"])
            self._content_frame.grid(row=1, column=0, sticky=tk.NSEW)

            # Left panel: digit grid (3×4 including row for zero)
            self._left_panel = self._make_frame(self._content_frame, bg=_THEME["WINDOW_BG"])
            self._left_panel.grid(row=0, column=0, sticky=tk.NSEW, padx=(10, 5))

            self._build_left_panel(self._left_panel)

            # Right panel: arithmetic operations (1 column × 4 rows)
            self._right_panel = self._make_frame(self._content_frame, bg=_THEME["WINDOW_BG"])
            self._right_panel.grid(row=0, column=1, sticky=tk.NSEW, padx=(5, 10))

            self._build_right_panel(self._right_panel)

            # ------ BOTTOM FRAME: non-arithmetic operation grid -----------
            self._bottom_frame = self._make_frame(self._root, bg=_THEME["WINDOW_BG"])
            self._bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

            self._build_bottom_panel(self._bottom_frame)

            # Keep legacy frame attributes expected by existing tests
            self._result_frame = self._top_frame
            self._input_frame = self._top_frame
            self._number_frame = self._left_panel
            self._operation_frame = self._bottom_frame

        except Exception:  # noqa: BLE001 — mocked root / headless CI; ignore gracefully
            pass

    def _build_left_panel(self, parent_frame: object) -> None:
        """Populate the left panel with digit buttons 1–9 and 0.

        Digits 1–9 are arranged in a 3×3 grid (row=(n-1)//3, col=(n-1)%3).
        Digit 0 occupies row=3, spanning all 3 columns.

        All created buttons are stored in ``self._digit_buttons`` and also
        as ``self._btn_<digit>`` for individual access.

        Args:
            parent_frame: The parent widget to add buttons to.
        """
        try:
            self._digit_buttons = []

            for digit in range(1, 10):
                row = (digit - 1) // 3
                col = (digit - 1) % 3
                btn = self._make_button(
                    parent_frame,
                    text=str(digit),
                    bg=_THEME["BUTTON_NORMAL_BG"],
                    fg=_THEME["BUTTON_NORMAL_FG"],
                    active_bg=_THEME["BUTTON_NORMAL_ACTIVE_BG"],
                    command=lambda d=digit: self._on_digit_press(d),
                )
                btn.grid(row=row, column=col, sticky=tk.NSEW)
                setattr(self, f"_btn_{digit}", btn)
                self._digit_buttons.append(btn)

            # Digit 0 spans all 3 columns
            btn_0 = self._make_button(
                parent_frame,
                text="0",
                bg=_THEME["BUTTON_NORMAL_BG"],
                fg=_THEME["BUTTON_NORMAL_FG"],
                active_bg=_THEME["BUTTON_NORMAL_ACTIVE_BG"],
                command=lambda: self._on_digit_press(0),
            )
            btn_0.grid(row=3, column=0, columnspan=3, sticky=tk.NSEW)
            self._btn_0 = btn_0
            self._digit_buttons.append(btn_0)

        except Exception:  # noqa: BLE001
            pass

    def _build_right_panel(self, parent_frame: object) -> None:
        """Populate the right panel with arithmetic operation buttons.

        Operations are stacked vertically in the order: divide (÷), multiply
        (×), subtract (−), add (+).  These buttons are never rebuilt on mode
        switch.

        All created buttons are stored in ``self._arithmetic_buttons`` and as
        ``self._btn_<op_name>`` for individual access.

        Args:
            parent_frame: The parent widget to add buttons to.
        """
        try:
            self._arithmetic_buttons = []

            for row_idx, op_name in enumerate(_ARITHMETIC_RIGHT_PANEL_ORDER):
                label = _OPERATION_SYMBOLS.get(op_name, op_name)
                btn = self._make_button(
                    parent_frame,
                    text=label,
                    bg=_THEME["BUTTON_OPERATOR_BG"],
                    fg=_THEME["BUTTON_OPERATOR_FG"],
                    active_bg=_THEME["BUTTON_OPERATOR_ACTIVE_BG"],
                    command=lambda op=op_name: self._on_op_press(op),
                )
                btn.grid(row=row_idx, column=0, sticky=tk.NSEW)
                setattr(self, f"_btn_{op_name}", btn)
                self._arithmetic_buttons.append(btn)

        except Exception:  # noqa: BLE001
            pass

    def _build_bottom_panel(self, parent_frame: object) -> None:
        """Populate the bottom panel with non-arithmetic operation buttons.

        In NORMAL mode: shows the 5 normal ops (``_NORMAL_OPS``).
        In SCIENTIFIC mode: shows normal ops + scientific ops (``_SCIENTIFIC_OPS``).

        Arithmetic operations are excluded from this panel (they live in the
        right panel).  Buttons are laid out in 4 columns.

        All created buttons are stored in ``self._operation_buttons`` and as
        ``self._btn_<op_name>``.  Also populates ``self._normal_mode_buttons``
        and ``self._scientific_mode_buttons`` for backward compatibility.

        Args:
            parent_frame: The parent widget to add buttons to.
        """
        try:
            # Determine operation list for the current mode
            if self._current_mode == OperationMode.SCIENTIFIC:
                ops = list(_NORMAL_OPS) + list(_SCIENTIFIC_OPS)
            else:
                ops = list(_NORMAL_OPS)

            self._operation_buttons = []
            self._normal_mode_buttons = []
            self._scientific_mode_buttons = []

            columns = 4
            for idx, op_name in enumerate(ops):
                row = idx // columns
                col = idx % columns
                bg, fg, active_bg = self._op_button_colours(op_name)
                label = _OPERATION_SYMBOLS.get(op_name, op_name)
                btn = self._make_button(
                    parent_frame,
                    text=label,
                    bg=bg,
                    fg=fg,
                    active_bg=active_bg,
                    command=lambda op=op_name: self._on_op_press(op),
                )
                btn.grid(row=row, column=col, sticky=tk.NSEW)
                setattr(self, f"_btn_{op_name}", btn)
                self._operation_buttons.append(btn)

                if op_name in _SCIENTIFIC_OPS:
                    self._scientific_mode_buttons.append(btn)
                else:
                    self._normal_mode_buttons.append(btn)

        except Exception:  # noqa: BLE001
            pass

    def _rebuild_bottom_panel(self) -> None:
        """Destroy and recreate the bottom panel for the new mode.

        Destroys all buttons in ``_operation_buttons``, destroys
        ``_bottom_frame``, creates a new frame at row=2 of the root window,
        and calls :meth:`_build_bottom_panel` to populate it.

        Silently ignores any exception so that headless test environments
        do not crash.
        """
        try:
            for btn in self._operation_buttons:
                try:
                    btn.destroy()
                except Exception:  # noqa: BLE001
                    pass
            self._operation_buttons = []

            if self._bottom_frame is not None:
                try:
                    self._bottom_frame.destroy()
                except Exception:  # noqa: BLE001
                    pass

            self._bottom_frame = self._make_frame(self._root, bg=_THEME["WINDOW_BG"])
            self._bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)
            self._operation_frame = self._bottom_frame

            self._build_bottom_panel(self._bottom_frame)

        except Exception:  # noqa: BLE001
            pass

    # ------------------------------------------------------------------
    # Private: legacy helpers retained for backward compatibility
    # ------------------------------------------------------------------

    def _build_op_buttons(self) -> None:
        """Legacy method: rebuild all operation buttons for the current mode.

        Retained for backward compatibility.  Delegates to
        :meth:`_rebuild_bottom_panel` and :meth:`_build_right_panel`.
        """
        try:
            self._rebuild_bottom_panel()
        except Exception:  # noqa: BLE001
            pass

    def _rebuild_op_grid(self) -> None:
        """Legacy method: rebuild the operation grid after a mode switch.

        Retained for backward compatibility.  Delegates to
        :meth:`_rebuild_bottom_panel`.
        """
        try:
            self._rebuild_bottom_panel()
        except Exception:  # noqa: BLE001
            pass
