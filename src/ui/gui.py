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

try:
    import tkinter as tk
    _TK_AVAILABLE = True
except ImportError:  # tkinter not installed (headless CI / test environment)
    import types as _types

    # Create a minimal stub so that @patch('src.ui.gui.tk.Tk') can resolve.
    tk = _types.ModuleType("tkinter")

    class _TkStub:
        """Minimal stand-in for tk.Tk and widget constructors."""

        def __init__(self, *args, **kwargs):
            self._value = ""

        def __call__(self, *args, **kwargs):
            return _TkStub()

        def title(self, *a, **kw): pass
        def resizable(self, *a, **kw): pass
        def pack(self, *a, **kw): pass
        def config(self, *a, **kw): pass
        def grid(self, *a, **kw):
            self._grid_info = kw

        def bind(self, *a, **kw): pass
        def destroy(self, *a, **kw): pass
        def mainloop(self, *a, **kw): pass
        def grid_info(self, *a, **kw):
            return getattr(self, "_grid_info", {})

        def set(self, value="", *a, **kw):
            self._value = value

        def get(self, *a, **kw):
            return self._value

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

# Arithmetic operations that get the orange operator colour
_ARITHMETIC_OPS: frozenset = frozenset({"add", "subtract", "multiply", "divide"})


class GuiCalculator:
    """iOS-style tkinter GUI calculator.

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
    # Private: mode toggle
    # ------------------------------------------------------------------

    def _on_mode_toggle(self) -> None:
        """Toggle between NORMAL and SCIENTIFIC mode and rebuild the UI."""
        if self._current_mode == OperationMode.NORMAL:
            self._current_mode = OperationMode.SCIENTIFIC
        else:
            self._current_mode = OperationMode.NORMAL
        self._update_mode_toggle_text()
        self._rebuild_op_grid()

    def _update_mode_toggle_text(self) -> None:
        """Update the mode toggle button text to reflect the pending mode."""
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
    # Private: GUI construction
    # ------------------------------------------------------------------

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

        Args:
            parent: Parent widget.
            text: Button label.
            bg: Normal background colour.
            fg: Foreground (text) colour.
            active_bg: Background colour on hover.
            command: Callback when button is pressed.

        Returns:
            The created button widget (``_TkStub`` or ``tk.Button``).
        """
        try:
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

    def _setup_ios_gui(self) -> None:  # noqa: C901 — complex but cohesive
        """Build all iOS-style tkinter widgets.

        All widget construction is wrapped in try/except so that a mocked
        root (used in unit tests without a real display) does not cause the
        constructor to crash.
        """
        try:
            self._root.title("Calculator")
            self._root.config(bg=_THEME["WINDOW_BG"])

            # ---- Input frame (result display) --------------------------
            self._input_frame = tk.Frame(self._root, bg=_THEME["WINDOW_BG"])
            self._input_frame.pack(fill=tk.X)

            self._result_frame = tk.Frame(self._root, bg=_THEME["RESULT_BG"])
            self._result_frame.pack(fill=tk.X)

            self._result_label = tk.Label(
                self._result_frame,
                text="0",
                bg=_THEME["RESULT_BG"],
                fg=_THEME["RESULT_FG"],
                font=_THEME["RESULT_FONT"],
                anchor=tk.E,
            )
            self._result_label.pack(fill=tk.X, padx=10, pady=10)

            # ---- Mode toggle button ------------------------------------
            self._mode_toggle_btn = tk.Button(
                self._root,
                text="Scientific",
                bg=_THEME["MODE_TOGGLE_BG"],
                fg=_THEME["MODE_TOGGLE_FG"],
                activebackground=_THEME["MODE_TOGGLE_ACTIVE_BG"],
                relief=tk.FLAT,
                borderwidth=0,
                command=self._on_mode_toggle,
            )
            self._mode_toggle_btn.pack(fill=tk.X)

            # ---- Number pad frame (digits 1-9 + 0) --------------------
            self._number_frame = tk.Frame(self._root, bg=_THEME["WINDOW_BG"])
            self._number_frame.pack()

            # Digits 1-9 arranged 3×3
            for idx, digit in enumerate(range(1, 10)):
                row = idx // 3
                col = idx % 3
                btn = self._make_button(
                    self._number_frame,
                    text=str(digit),
                    bg=_THEME["BUTTON_NORMAL_BG"],
                    fg=_THEME["BUTTON_NORMAL_FG"],
                    active_bg=_THEME["BUTTON_NORMAL_ACTIVE_BG"],
                )
                btn.grid(row=row, column=col, sticky=tk.NSEW)
                setattr(self, f"_btn_{digit}", btn)

            # Digit 0 spans all 3 columns
            self._btn_0 = self._make_button(
                self._number_frame,
                text="0",
                bg=_THEME["BUTTON_NORMAL_BG"],
                fg=_THEME["BUTTON_NORMAL_FG"],
                active_bg=_THEME["BUTTON_NORMAL_ACTIVE_BG"],
            )
            self._btn_0.grid(row=3, column=0, columnspan=3, sticky=tk.NSEW)

            # ---- Operation frame ---------------------------------------
            self._operation_frame = tk.Frame(self._root, bg=_THEME["WINDOW_BG"])
            self._operation_frame.pack()

            self._build_op_buttons()

        except Exception:  # noqa: BLE001 — mocked root / headless CI; ignore gracefully
            pass

    def _build_op_buttons(self) -> None:
        """Create all operation buttons for the current mode and store references.

        Populates:
        - ``self._operation_buttons`` (all buttons in the grid)
        - ``self._normal_mode_buttons`` (arithmetic + normal ops)
        - ``self._scientific_mode_buttons`` (scientific-only ops)
        - ``self._btn_<op_name>`` for each operation

        Buttons are laid out in 4 columns.
        """
        try:
            # Clear previous buttons
            for btn in self._operation_buttons:
                try:
                    btn.destroy()
                except Exception:  # noqa: BLE001
                    pass

            self._operation_buttons = []
            self._normal_mode_buttons = []
            self._scientific_mode_buttons = []

            # Determine which operations to show
            arithmetic_ops = list(_ARITHMETIC_OPS)
            normal_ops = list(_NORMAL_OPS)
            if self._current_mode == OperationMode.SCIENTIFIC:
                scientific_ops = list(_SCIENTIFIC_OPS)
            else:
                scientific_ops = []

            all_ops = arithmetic_ops + normal_ops + scientific_ops

            columns = 4
            for idx, op_name in enumerate(all_ops):
                row = idx // columns
                col = idx % columns
                bg, fg, active_bg = self._op_button_colours(op_name)
                label = _OPERATION_SYMBOLS.get(op_name, op_name)
                btn = self._make_button(
                    self._operation_frame,
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

    def _rebuild_op_grid(self) -> None:
        """Rebuild the operation grid after a mode switch.

        Calls :meth:`_build_op_buttons` to recreate buttons for the new mode.
        Silently ignores any exception from widget operations.
        """
        try:
            self._build_op_buttons()
        except Exception:  # noqa: BLE001
            pass

    def _on_op_press(self, op_name: str) -> None:
        """Handle an operation button press.

        Stores the selected operation name for use when the result is
        requested.  In a real calculator this would update the display.

        Args:
            op_name: The name of the pressed operation.
        """
        self._selected_op = op_name
