"""Main GUI application for the Calculator.

This module contains :class:`CalculatorGUI`, a tkinter-based calculator
interface that supports both Simple and Scientific modes, maintains a
calculation history panel, and delegates all arithmetic to the
:class:`~src.core.calculator.Calculator` backend.

No arithmetic is performed in this module; the GUI is purely responsible
for input collection, dispatch, display, and history rendering.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import font as tkfont
from typing import Callable

from src.core.calculator import Calculator
from src.support.history import HistoryTracker
from src.gui.modes import CalcMode, SimpleMode, ScientificMode


_THEME = {
    "window_bg": "#000000",
    "display_bg": "#000000",
    "display_fg": "#FFFFFF",
    "display_font": ("Courier", 32, "bold"),
    "btn_font": ("Arial", 18),
    "mode_btn_font": ("Arial", 14),
    # Arithmetic operators (add, subtract, multiply, divide)
    "op_bg": "#FF9500",
    "op_fg": "#FFFFFF",
    "op_hover": "#FFB143",
    # Scientific / utility ops in scientific mode
    "sci_bg": "#1C1C1E",
    "sci_fg": "#FFFFFF",
    "sci_hover": "#2C2C2E",
    # Standard ops in normal mode (non-arithmetic)
    "std_bg": "#333333",
    "std_fg": "#FFFFFF",
    "std_hover": "#4D4D4D",
    # History panel
    "history_bg": "#1C1C1E",
    "history_fg": "#AAAAAA",
    "history_list_fg": "#CCCCCC",
    "history_select_bg": "#FF9500",
    "history_select_fg": "#FFFFFF",
    "frame_bg": "#000000",
}

_SYMBOLS = {
    "add": "+",
    "subtract": "−",
    "multiply": "×",
    "divide": "÷",
    "square": "x²",
    "square_root": "√",
    "cube": "x³",
    "cube_root": "∛",
    "power": "xʸ",
    "factorial": "n!",
    "log": "log",
    "ln": "ln",
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "cot": "cot",
    "asin": "asin",
    "acos": "acos",
    "pi": "π",
    "e": "e",
}

_ARITHMETIC_OPS = {"add", "subtract", "multiply", "divide"}


class CalculatorGUI:
    """Tkinter-based calculator GUI.

    Handles user interaction for a :class:`~src.core.calculator.Calculator`
    backend.  The visible operation buttons are driven entirely by the active
    :class:`~src.gui.modes.CalcMode`, so swapping modes rebuilds the widget
    tree while preserving the shared :class:`~src.support.history.HistoryTracker`.

    Args:
        root: The top-level Tk window.
        calculator: The Calculator instance used for all computation.
        mode: The initial CalcMode (Simple or Scientific).
        history_tracker: The shared HistoryTracker instance.

    Attributes:
        _current_input: The digit/decimal string the user is currently typing.
        _first_operand: The stored first operand for a pending binary operation.
        _pending_op: A ``(callable, arity)`` tuple for the queued operation,
            or ``None`` when no operation is pending.
        _pending_op_name: The name string of the pending operation, used when
            recording history.
    """

    def __init__(
        self,
        root: tk.Tk,
        calculator: Calculator,
        mode: CalcMode,
        history_tracker: HistoryTracker,
    ) -> None:
        self._root = root
        self._calculator = calculator
        self._mode = mode
        self._history_tracker = history_tracker

        # Mutable state
        self._current_input: str = ""
        self._first_operand: float | None = None
        self._pending_op: tuple[Callable, int] | None = None
        self._pending_op_name: str | None = None

        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction helpers
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Build or rebuild the entire widget tree for the current mode.

        Called on initial construction and whenever the mode is switched.
        All previously created widgets are destroyed before rebuilding so
        that a clean layout is produced for the new mode.
        """
        for widget in self._root.winfo_children():
            widget.destroy()

        self._root.configure(bg=_THEME["window_bg"])
        self._root.resizable(True, True)

        # Left frame: calculator
        left_frame = tk.Frame(self._root, bg=_THEME["frame_bg"])
        left_frame.grid(row=0, column=0, sticky="nsew")

        # Right frame: history
        right_frame = tk.Frame(self._root, bg=_THEME["history_bg"])
        right_frame.grid(row=0, column=1, padx=(4, 0), sticky="nsew")

        self._root.columnconfigure(0, weight=3)
        self._root.columnconfigure(1, weight=2)
        self._root.rowconfigure(0, weight=1)

        # Build sections into left_frame
        self._build_display(left_frame)
        self._build_mode_toggle(left_frame)
        self._build_button_grid(left_frame)
        self._build_history_panel(right_frame)

        self._refresh_history()

    def _build_display(self, parent: tk.Frame) -> None:
        """Build the calculator display label widget.

        Args:
            parent: The parent frame to attach the display to.
        """
        self._display_var = tk.StringVar(value="0")
        self._display = tk.Label(
            parent,
            textvariable=self._display_var,
            font=_THEME["display_font"],
            bg=_THEME["display_bg"],
            fg=_THEME["display_fg"],
            anchor="e",
            padx=12,
            pady=8,
        )
        self._display.grid(row=0, column=0, columnspan=4, sticky="ew")
        for c in range(4):
            parent.columnconfigure(c, weight=1)

    def _build_mode_toggle(self, parent: tk.Frame) -> None:
        """Build the single mode-toggle button.

        The button label reflects the mode the calculator will switch TO
        when pressed (i.e. "Scientific" when in Simple mode and vice versa).

        Args:
            parent: The parent frame to attach the button to.
        """
        label = "Scientific" if self._mode.name == "Simple" else "Normal"
        btn = tk.Button(
            parent,
            text=label,
            font=_THEME["mode_btn_font"],
            bg=_THEME["std_bg"],
            fg=_THEME["std_fg"],
            activebackground=_THEME["std_hover"],
            activeforeground=_THEME["std_fg"],
            relief="flat",
            bd=0,
            command=self._toggle_mode,
        )
        btn.grid(row=1, column=0, columnspan=4, sticky="ew")
        self._bind_hover(btn, _THEME["std_bg"], _THEME["std_hover"])

    def _toggle_mode(self) -> None:
        """Toggle between Simple and Scientific modes."""
        if self._mode.name == "Simple":
            self._switch_to_scientific()
        else:
            self._switch_to_simple()

    def _build_button_grid(self, parent: tk.Frame) -> None:
        """Build digit buttons and operation buttons in a unified grid.

        Digit buttons occupy rows 2-5 (columns 0-2 plus the bottom row).
        Operation buttons start at row 6, flowing left-to-right 4 per row,
        coloured according to whether they are arithmetic, scientific, or
        standard operations.

        Args:
            parent: The parent frame to attach the buttons to.
        """
        btn_font = _THEME["btn_font"]
        is_scientific = self._mode.name == "Scientific"
        operations = self._mode.get_operations()

        # Row 2 onward: 4-column grid
        # Number layout rows 2-5: 7/8/9, 4/5/6, 1/2/3, C/0/./=
        digit_layout = [
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2),
        ]

        for label, row, col in digit_layout:
            btn = tk.Button(
                parent,
                text=label,
                font=btn_font,
                bg=_THEME["std_bg"],
                fg=_THEME["std_fg"],
                activebackground=_THEME["std_hover"],
                activeforeground=_THEME["std_fg"],
                relief="flat",
                bd=0,
                command=lambda d=label: self._on_digit(d),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
            self._bind_hover(btn, _THEME["std_bg"], _THEME["std_hover"])

        # Bottom number row (row 5): C, 0, ., =
        clear_btn = tk.Button(
            parent, text="C", font=btn_font,
            bg=_THEME["op_bg"], fg=_THEME["op_fg"],
            activebackground=_THEME["op_hover"], activeforeground=_THEME["op_fg"],
            relief="flat", bd=0, command=self._on_clear,
        )
        clear_btn.grid(row=5, column=0, sticky="nsew", padx=1, pady=1)
        self._bind_hover(clear_btn, _THEME["op_bg"], _THEME["op_hover"])

        zero_btn = tk.Button(
            parent, text="0", font=btn_font,
            bg=_THEME["std_bg"], fg=_THEME["std_fg"],
            activebackground=_THEME["std_hover"], activeforeground=_THEME["std_fg"],
            relief="flat", bd=0, command=lambda: self._on_digit("0"),
        )
        zero_btn.grid(row=5, column=1, sticky="nsew", padx=1, pady=1)
        self._bind_hover(zero_btn, _THEME["std_bg"], _THEME["std_hover"])

        dot_btn = tk.Button(
            parent, text=".", font=btn_font,
            bg=_THEME["std_bg"], fg=_THEME["std_fg"],
            activebackground=_THEME["std_hover"], activeforeground=_THEME["std_fg"],
            relief="flat", bd=0, command=self._on_decimal,
        )
        dot_btn.grid(row=5, column=2, sticky="nsew", padx=1, pady=1)
        self._bind_hover(dot_btn, _THEME["std_bg"], _THEME["std_hover"])

        equals_btn = tk.Button(
            parent, text="=", font=btn_font,
            bg=_THEME["op_bg"], fg=_THEME["op_fg"],
            activebackground=_THEME["op_hover"], activeforeground=_THEME["op_fg"],
            relief="flat", bd=0, command=self._on_equals,
        )
        equals_btn.grid(row=5, column=3, sticky="nsew", padx=1, pady=1)
        self._bind_hover(equals_btn, _THEME["op_bg"], _THEME["op_hover"])

        # Configure row weights for number rows
        for r in range(2, 6):
            parent.rowconfigure(r, weight=1)

        # Operation buttons start at row 6
        for idx, (op_name, (op_callable, arity)) in enumerate(operations.items()):
            row_idx = 6 + idx // 4
            col_idx = idx % 4

            symbol = _SYMBOLS.get(op_name, op_name.replace("_", " "))

            if op_name in _ARITHMETIC_OPS:
                bg, fg, hover = _THEME["op_bg"], _THEME["op_fg"], _THEME["op_hover"]
            elif is_scientific:
                bg, fg, hover = _THEME["sci_bg"], _THEME["sci_fg"], _THEME["sci_hover"]
            else:
                bg, fg, hover = _THEME["std_bg"], _THEME["std_fg"], _THEME["std_hover"]

            btn = tk.Button(
                parent,
                text=symbol,
                font=btn_font,
                bg=bg,
                fg=fg,
                activebackground=hover,
                activeforeground=fg,
                relief="flat",
                bd=0,
                command=lambda name=op_name, fn=op_callable, ar=arity: self._on_operation(name, fn, ar),
            )
            btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
            parent.rowconfigure(row_idx, weight=1)
            self._bind_hover(btn, bg, hover)

    def _bind_hover(self, btn: tk.Button, default_bg: str, hover_bg: str) -> None:
        """Bind mouse enter/leave events to simulate hover colour changes.

        Args:
            btn: The button widget to bind hover events to.
            default_bg: The background colour when the mouse is not hovering.
            hover_bg: The background colour when the mouse is hovering.
        """
        btn.bind("<Enter>", lambda e, b=btn, h=hover_bg: b.configure(bg=h))
        btn.bind("<Leave>", lambda e, b=btn, d=default_bg: b.configure(bg=d))

    def _build_history_panel(self, parent: tk.Frame) -> None:
        """Build the history panel showing past calculations.

        Args:
            parent: The parent frame containing the history widgets.
        """
        label_font = tkfont.Font(family="Arial", size=11, weight="bold")
        history_label = tk.Label(
            parent,
            text="History",
            font=label_font,
            bg=_THEME["history_bg"],
            fg=_THEME["history_fg"],
            anchor="w",
        )
        history_label.pack(fill="x", padx=4, pady=(4, 2))

        list_font = tkfont.Font(family="Courier", size=10)
        self._history_listbox = tk.Listbox(
            parent,
            font=list_font,
            bg=_THEME["history_bg"],
            fg=_THEME["history_list_fg"],
            selectbackground=_THEME["history_select_bg"],
            selectforeground=_THEME["history_select_fg"],
            bd=0,
            highlightthickness=0,
            activestyle="none",
        )
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=self._history_listbox.yview)
        self._history_listbox.configure(yscrollcommand=scrollbar.set)

        self._history_listbox.pack(side="left", fill="both", expand=True, padx=(4, 0), pady=4)
        scrollbar.pack(side="right", fill="y", pady=4)

        parent.rowconfigure(0, weight=1)

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def _set_display(self, text: str) -> None:
        """Update the display widget content.

        Args:
            text: The string to show in the display.
        """
        self._display_var.set(text)

    def _get_display(self) -> str:
        """Return the current display content.

        Returns:
            The string currently shown in the display.
        """
        return self._display_var.get()

    # ------------------------------------------------------------------
    # Input event handlers
    # ------------------------------------------------------------------

    def _on_digit(self, digit: str) -> None:
        """Append a digit character to the current input.

        If the display currently shows an error message the input is reset
        before appending the new digit.

        Args:
            digit: A single digit character "0"-"9".
        """
        if self._current_input.startswith("Error"):
            self._current_input = ""
        self._current_input += digit
        self._set_display(self._current_input)

    def _on_decimal(self) -> None:
        """Append a decimal point to the current input, if not already present.

        Prevents multiple decimal points in the same number.  If the
        display shows an error, the input is reset first.
        """
        if self._current_input.startswith("Error"):
            self._current_input = ""
        if "." not in self._current_input:
            self._current_input += "."
            self._set_display(self._current_input if self._current_input != "." else "0.")

    def _on_clear(self) -> None:
        """Reset all transient state: current input, pending operation, operand."""
        self._current_input = ""
        self._first_operand = None
        self._pending_op = None
        self._pending_op_name = None
        self._set_display("0")

    def _on_operation(self, op_name: str, op_callable: Callable, arity: int) -> None:
        """Handle an operation button press.

        For unary operations (arity 1): execute immediately on the current
        input value.

        For binary operations (arity 2): store the current input as the first
        operand and queue the operation, waiting for a second operand and
        ``=`` press.

        Args:
            op_name: The operation identifier string (e.g. ``"add"``).
            op_callable: The bound Calculator method to invoke.
            arity: The number of operands: 1 (unary) or 2 (binary).
        """
        if arity == 1:
            value = self._parse_current_input()
            if value is None:
                self._set_display("Error: invalid input")
                return
            self._execute_unary(op_name, op_callable, value)
        else:
            # Binary: store first operand and queue operation
            value = self._parse_current_input()
            if value is None:
                self._set_display("Error: invalid input")
                return
            self._first_operand = value
            self._pending_op = (op_callable, arity)
            self._pending_op_name = op_name
            self._current_input = ""

    def _on_equals(self) -> None:
        """Execute the pending binary operation with the second operand.

        Does nothing if no binary operation is queued.  On success the
        display is updated with the result and the state is reset.  On
        failure an error message is shown in the display.
        """
        if self._pending_op is None:
            return

        second_value = self._parse_current_input()
        if second_value is None:
            self._set_display("Error: invalid input")
            return

        op_callable, _ = self._pending_op
        op_name = self._pending_op_name

        try:
            result = op_callable(self._first_operand, second_value)
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            self._set_display(f"Error: {exc}")
            self._current_input = f"Error: {exc}"
            self._pending_op = None
            self._pending_op_name = None
            self._first_operand = None
            return

        self._history_tracker.record(op_name, [self._first_operand, second_value], result)
        self._refresh_history()

        result_str = self._format_result(result)
        self._set_display(result_str)
        self._current_input = result_str
        self._first_operand = None
        self._pending_op = None
        self._pending_op_name = None

    # ------------------------------------------------------------------
    # Calculation helpers
    # ------------------------------------------------------------------

    def _execute_unary(self, op_name: str, op_callable: Callable, value: float) -> None:
        """Run a unary operation and update the display with the result.

        Args:
            op_name: The operation identifier string.
            op_callable: The bound Calculator method to invoke.
            value: The single numeric operand.
        """
        # factorial requires an int; convert if the value is a whole number
        if op_name == "factorial":
            if value != int(value):
                self._set_display("Error: factorial requires an integer")
                self._current_input = "Error: factorial requires an integer"
                return
            value = int(value)

        try:
            result = op_callable(value)
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            self._set_display(f"Error: {exc}")
            self._current_input = f"Error: {exc}"
            return

        self._history_tracker.record(op_name, [value], result)
        self._refresh_history()

        result_str = self._format_result(result)
        self._set_display(result_str)
        self._current_input = result_str

    def _parse_current_input(self) -> float | None:
        """Parse the current input string as a float.

        Returns:
            The parsed float value, or ``None`` if the string is empty or
            cannot be converted.
        """
        raw = self._current_input.strip()
        if not raw or raw.startswith("Error"):
            return None
        try:
            return float(raw)
        except ValueError:
            return None

    @staticmethod
    def _format_result(result: object) -> str:
        """Format a calculation result for display.

        Integers and whole-number floats are displayed without a decimal
        point to keep the output clean (e.g. ``"5"`` instead of ``"5.0"``).
        Very long floats are shown to a maximum of 10 significant digits.

        Args:
            result: The raw value returned by a Calculator method.

        Returns:
            A human-readable string representation of the result.
        """
        if isinstance(result, int):
            return str(result)
        if isinstance(result, float):
            if result == int(result) and not (result != result):  # not NaN
                return str(int(result))
            # Use up to 10 significant digits, strip trailing zeros
            formatted = f"{result:.10g}"
            return formatted
        return str(result)

    # ------------------------------------------------------------------
    # History helpers
    # ------------------------------------------------------------------

    def _refresh_history(self) -> None:
        """Repopulate the history listbox from the HistoryTracker.

        Clears the listbox and inserts all current history entries, then
        scrolls to show the most recent entry.
        """
        self._history_listbox.delete(0, tk.END)
        for entry in self._history_tracker.get_history():
            self._history_listbox.insert(tk.END, entry)
        if self._history_tracker.get_history():
            self._history_listbox.see(tk.END)

    # ------------------------------------------------------------------
    # Mode switching
    # ------------------------------------------------------------------

    def _switch_to_simple(self) -> None:
        """Switch the calculator to Simple mode and rebuild the UI.

        No-op if the current mode is already Simple.
        """
        if self._mode.name == "Simple":
            return
        self._mode = SimpleMode(self._calculator)
        self._reset_transient_state()
        self._build_ui()

    def _switch_to_scientific(self) -> None:
        """Switch the calculator to Scientific mode and rebuild the UI.

        No-op if the current mode is already Scientific.
        """
        if self._mode.name == "Scientific":
            return
        self._mode = ScientificMode(self._calculator)
        self._reset_transient_state()
        self._build_ui()

    def _reset_transient_state(self) -> None:
        """Reset all transient calculator state without touching the history."""
        self._current_input = ""
        self._first_operand = None
        self._pending_op = None
        self._pending_op_name = None
