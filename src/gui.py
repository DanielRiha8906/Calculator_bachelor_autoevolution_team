"""Tkinter GUI for the calculator application.

Provides a window-based interface supporting both normal (binary arithmetic)
and scientific (unary function) modes.  All calculation dispatch goes through
the public API in dispatcher (run_calculation, run_unary_calculation).  Mode
state is tracked via ModeManager.

This module is self-contained: no other src module imports it.
"""

import tkinter as tk
from tkinter import font as tkfont

from src.dispatcher import run_calculation, run_unary_calculation
from src.logger import get_logger
from src.mode_manager import ModeManager
from src.parser import BINARY_OPERATORS, UNARY_FUNCTIONS

_DISPLAY_BG = "#1e1e1e"
_DISPLAY_FG = "#ffffff"
_BTN_BG = "#3c3c3c"
_BTN_FG = "#ffffff"
_BTN_OP_BG = "#ff9500"
_BTN_OP_FG = "#ffffff"
_BTN_SCI_BG = "#2a5298"
_BTN_SCI_FG = "#ffffff"
_BTN_MODE_BG = "#555555"
_BTN_MODE_FG = "#ffffff"
_BTN_CLEAR_BG = "#a5a5a5"
_BTN_CLEAR_FG = "#1e1e1e"
_BTN_EQUAL_BG = "#ff9500"
_BTN_EQUAL_FG = "#ffffff"
_WINDOW_BG = "#2b2b2b"
_HISTORY_BG = "#1e1e1e"
_HISTORY_FG = "#aaaaaa"
_ERROR_FG = "#ff4444"


class CalculatorGUI:
    """Main tkinter GUI application for the calculator.

    Owns a Tk root window, a display area, numeric/operator buttons, and
    a mode toggle.  Binary calculations use run_calculation(); unary
    scientific calculations use run_unary_calculation().

    Attributes:
        _root: The tkinter root window.
        _mode_manager: Tracks normal / scientific mode.
        _current_input: Accumulated display string for the ongoing expression.
        _first_operand: Parsed float of the first operand (normal mode).
        _operator: The pending operator symbol (normal mode).
        _awaiting_second: True when the next digit input starts the 2nd operand.
        _logger: Module-level logger.
    """

    def __init__(self) -> None:
        """Initialise the calculator GUI window and all widgets."""
        self._logger = get_logger(__name__)
        self._mode_manager: ModeManager = ModeManager()

        # State for normal (binary) mode
        self._current_input: str = ""
        self._first_operand: float | None = None
        self._operator: str | None = None
        self._awaiting_second: bool = False

        # State for scientific (unary) mode
        self._sci_function: str | None = None
        self._sci_awaiting_arg: bool = False

        self._root = tk.Tk()
        self._root.title("Calculator")
        self._root.resizable(False, False)
        self._root.configure(bg=_WINDOW_BG)

        self._build_display()
        self._build_history_area()
        self._build_mode_bar()
        self._build_normal_buttons()
        self._build_scientific_buttons()
        self._refresh_mode_layout()

    # ------------------------------------------------------------------
    # UI construction helpers
    # ------------------------------------------------------------------

    def _build_display(self) -> None:
        """Create the main expression display at the top of the window."""
        display_frame = tk.Frame(self._root, bg=_DISPLAY_BG, pady=4)
        display_frame.pack(fill=tk.X, padx=8, pady=(8, 0))

        display_font = tkfont.Font(family="Helvetica", size=32, weight="bold")
        self._display_var = tk.StringVar(value="0")
        self._display_label = tk.Label(
            display_frame,
            textvariable=self._display_var,
            font=display_font,
            bg=_DISPLAY_BG,
            fg=_DISPLAY_FG,
            anchor="e",
            padx=12,
            pady=8,
            width=14,
        )
        self._display_label.pack(fill=tk.X)

    def _build_history_area(self) -> None:
        """Create a small history label below the main display."""
        history_font = tkfont.Font(family="Helvetica", size=11)
        self._history_var = tk.StringVar(value="")
        self._history_label = tk.Label(
            self._root,
            textvariable=self._history_var,
            font=history_font,
            bg=_WINDOW_BG,
            fg=_HISTORY_FG,
            anchor="e",
            padx=12,
        )
        self._history_label.pack(fill=tk.X, padx=8)

    def _build_mode_bar(self) -> None:
        """Create the mode-toggle bar (Normal / Scientific)."""
        mode_frame = tk.Frame(self._root, bg=_WINDOW_BG, pady=4)
        mode_frame.pack(fill=tk.X, padx=8)

        btn_font = tkfont.Font(family="Helvetica", size=12)
        self._mode_normal_btn = tk.Button(
            mode_frame,
            text="Normal",
            font=btn_font,
            bg=_BTN_MODE_BG,
            fg=_BTN_MODE_FG,
            relief=tk.FLAT,
            padx=10,
            pady=4,
            command=lambda: self._on_mode_switch("normal"),
        )
        self._mode_normal_btn.pack(side=tk.LEFT, padx=(0, 4))

        self._mode_scientific_btn = tk.Button(
            mode_frame,
            text="Scientific",
            font=btn_font,
            bg=_BTN_MODE_BG,
            fg=_BTN_MODE_FG,
            relief=tk.FLAT,
            padx=10,
            pady=4,
            command=lambda: self._on_mode_switch("scientific"),
        )
        self._mode_scientific_btn.pack(side=tk.LEFT)

        self._mode_status_label = tk.Label(
            mode_frame,
            text="",
            font=btn_font,
            bg=_WINDOW_BG,
            fg=_HISTORY_FG,
        )
        self._mode_status_label.pack(side=tk.RIGHT, padx=8)

    def _make_button(
        self,
        parent: tk.Frame,
        text: str,
        command,
        bg: str = _BTN_BG,
        fg: str = _BTN_FG,
        colspan: int = 1,
    ) -> tk.Button:
        """Create and return a styled calculator button.

        Args:
            parent: The parent frame to attach the button to.
            text: Label shown on the button.
            command: Callback invoked on click.
            bg: Background colour.
            fg: Foreground (text) colour.
            colspan: Not used for grid — kept for interface symmetry.

        Returns:
            The configured Button widget.
        """
        btn_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        btn = tk.Button(
            parent,
            text=text,
            font=btn_font,
            bg=bg,
            fg=fg,
            relief=tk.FLAT,
            activebackground=bg,
            activeforeground=fg,
            padx=8,
            pady=14,
            width=4,
            command=command,
        )
        return btn

    def _build_normal_buttons(self) -> None:
        """Build the normal-mode button grid (digits, operators, clear, equals)."""
        self._normal_frame = tk.Frame(self._root, bg=_WINDOW_BG, pady=4)

        # Row layout: each inner list is one row of (label, bg, fg, action)
        rows: list[list[tuple[str, str, str, str]]] = [
            [
                ("C", _BTN_CLEAR_BG, _BTN_CLEAR_FG, "clear"),
                ("+/-", _BTN_CLEAR_BG, _BTN_CLEAR_FG, "negate"),
                ("%", _BTN_CLEAR_BG, _BTN_CLEAR_FG, "percent"),
                ("/", _BTN_OP_BG, _BTN_OP_FG, "op:/"),
            ],
            [
                ("7", _BTN_BG, _BTN_FG, "num:7"),
                ("8", _BTN_BG, _BTN_FG, "num:8"),
                ("9", _BTN_BG, _BTN_FG, "num:9"),
                ("*", _BTN_OP_BG, _BTN_OP_FG, "op:*"),
            ],
            [
                ("4", _BTN_BG, _BTN_FG, "num:4"),
                ("5", _BTN_BG, _BTN_FG, "num:5"),
                ("6", _BTN_BG, _BTN_FG, "num:6"),
                ("-", _BTN_OP_BG, _BTN_OP_FG, "op:-"),
            ],
            [
                ("1", _BTN_BG, _BTN_FG, "num:1"),
                ("2", _BTN_BG, _BTN_FG, "num:2"),
                ("3", _BTN_BG, _BTN_FG, "num:3"),
                ("+", _BTN_OP_BG, _BTN_OP_FG, "op:+"),
            ],
            [
                ("0", _BTN_BG, _BTN_FG, "num:0"),
                (".", _BTN_BG, _BTN_FG, "num:."),
                ("=", _BTN_EQUAL_BG, _BTN_EQUAL_FG, "equals"),
            ],
        ]

        for r_idx, row in enumerate(rows):
            col_span_remaining = 4
            c_idx = 0
            for label, bg, fg, action in row:
                # "0" button gets double width on last row
                col_span = 2 if (label == "0") else 1
                btn = self._make_button(
                    self._normal_frame,
                    label,
                    command=lambda a=action: self._on_normal_action(a),
                    bg=bg,
                    fg=fg,
                )
                btn.grid(
                    row=r_idx,
                    column=c_idx,
                    columnspan=col_span,
                    padx=3,
                    pady=3,
                    sticky=tk.NSEW,
                )
                c_idx += col_span
                col_span_remaining -= col_span

        for i in range(4):
            self._normal_frame.columnconfigure(i, weight=1)

    def _build_scientific_buttons(self) -> None:
        """Build the scientific-mode button grid (unary functions + digits + equals)."""
        self._sci_frame = tk.Frame(self._root, bg=_WINDOW_BG, pady=4)

        sci_labels = list(UNARY_FUNCTIONS.keys())  # sin cos tan log ln exp sqrt

        # Row 0: scientific function buttons
        sci_row0 = sci_labels[:4]
        sci_row1 = sci_labels[4:]

        for c_idx, func in enumerate(sci_row0):
            btn = self._make_button(
                self._sci_frame,
                func,
                command=lambda f=func: self._on_sci_function(f),
                bg=_BTN_SCI_BG,
                fg=_BTN_SCI_FG,
            )
            btn.grid(row=0, column=c_idx, padx=3, pady=3, sticky=tk.NSEW)

        for c_idx, func in enumerate(sci_row1):
            btn = self._make_button(
                self._sci_frame,
                func,
                command=lambda f=func: self._on_sci_function(f),
                bg=_BTN_SCI_BG,
                fg=_BTN_SCI_FG,
            )
            btn.grid(row=1, column=c_idx, padx=3, pady=3, sticky=tk.NSEW)

        # Rows 2-5: digit + clear + equals
        digit_rows: list[list[tuple[str, str, str, str]]] = [
            [
                ("C", _BTN_CLEAR_BG, _BTN_CLEAR_FG, "clear"),
                ("+/-", _BTN_CLEAR_BG, _BTN_CLEAR_FG, "negate"),
                (".", _BTN_BG, _BTN_FG, "num:."),
                ("=", _BTN_EQUAL_BG, _BTN_EQUAL_FG, "equals"),
            ],
            [
                ("7", _BTN_BG, _BTN_FG, "num:7"),
                ("8", _BTN_BG, _BTN_FG, "num:8"),
                ("9", _BTN_BG, _BTN_FG, "num:9"),
            ],
            [
                ("4", _BTN_BG, _BTN_FG, "num:4"),
                ("5", _BTN_BG, _BTN_FG, "num:5"),
                ("6", _BTN_BG, _BTN_FG, "num:6"),
            ],
            [
                ("1", _BTN_BG, _BTN_FG, "num:1"),
                ("2", _BTN_BG, _BTN_FG, "num:2"),
                ("3", _BTN_BG, _BTN_FG, "num:3"),
            ],
            [
                ("0", _BTN_BG, _BTN_FG, "num:0"),
            ],
        ]

        for r_offset, row in enumerate(digit_rows):
            c_idx = 0
            for label, bg, fg, action in row:
                col_span = 2 if (label == "0") else 1
                btn = self._make_button(
                    self._sci_frame,
                    label,
                    command=lambda a=action: self._on_sci_action(a),
                    bg=bg,
                    fg=fg,
                )
                btn.grid(
                    row=r_offset + 2,
                    column=c_idx,
                    columnspan=col_span,
                    padx=3,
                    pady=3,
                    sticky=tk.NSEW,
                )
                c_idx += col_span

        for i in range(4):
            self._sci_frame.columnconfigure(i, weight=1)

    # ------------------------------------------------------------------
    # Mode management
    # ------------------------------------------------------------------

    def _refresh_mode_layout(self) -> None:
        """Show the correct button frame and update mode indicator labels."""
        mode = self._mode_manager.get_mode()
        self._mode_status_label.config(text=f"Mode: {mode}")

        # Highlight active mode button
        if mode == "scientific":
            self._mode_scientific_btn.config(relief=tk.SUNKEN)
            self._mode_normal_btn.config(relief=tk.FLAT)
            self._normal_frame.pack_forget()
            self._sci_frame.pack(padx=8, pady=(0, 8))
        else:
            self._mode_normal_btn.config(relief=tk.SUNKEN)
            self._mode_scientific_btn.config(relief=tk.FLAT)
            self._sci_frame.pack_forget()
            self._normal_frame.pack(padx=8, pady=(0, 8))

    def _on_mode_switch(self, mode_name: str) -> None:
        """Handle a mode toggle button press.

        Args:
            mode_name: "normal" or "scientific".
        """
        try:
            self._mode_manager.set_mode(mode_name)
        except ValueError as exc:
            self._show_error(str(exc))
            return

        self._clear_state()
        self._refresh_mode_layout()
        self._logger.info(f"GUI mode switched to {mode_name!r}")

    # ------------------------------------------------------------------
    # Normal-mode event handlers
    # ------------------------------------------------------------------

    def _on_normal_action(self, action: str) -> None:
        """Dispatch a normal-mode button action.

        Args:
            action: A string token such as "num:3", "op:+", "equals",
                "clear", "negate", or "percent".
        """
        if action == "clear":
            self._clear_state()
        elif action == "negate":
            self._negate_display()
        elif action == "percent":
            self._apply_percent()
        elif action == "equals":
            self._execute_normal()
        elif action.startswith("num:"):
            digit = action[4:]
            self._append_digit(digit)
        elif action.startswith("op:"):
            operator = action[3:]
            self._set_operator(operator)

    def _append_digit(self, digit: str) -> None:
        """Append a digit or decimal point to the current display input.

        Args:
            digit: A single character digit or ".".
        """
        if self._awaiting_second:
            self._current_input = ""
            self._awaiting_second = False

        if digit == "." and "." in self._current_input:
            return
        if self._current_input in ("0", "") and digit != ".":
            self._current_input = digit
        else:
            self._current_input += digit

        self._display_var.set(self._current_input)

    def _set_operator(self, operator: str) -> None:
        """Record the first operand and pending operator.

        If an operator is already pending and a second operand has been
        entered, chains the calculation first.

        Args:
            operator: One of "+", "-", "*", "/".
        """
        if operator not in BINARY_OPERATORS:
            return

        if self._first_operand is not None and not self._awaiting_second:
            # Chain: evaluate the previous operation before setting the new one
            self._execute_normal(chain=True)

        try:
            value = float(self._current_input) if self._current_input else 0.0
        except ValueError:
            return

        self._first_operand = value
        self._operator = operator
        self._awaiting_second = True
        self._history_var.set(f"{self._format_number(value)} {operator}")

    def _negate_display(self) -> None:
        """Toggle the sign of the current display value."""
        if not self._current_input or self._current_input == "0":
            return
        if self._current_input.startswith("-"):
            self._current_input = self._current_input[1:]
        else:
            self._current_input = "-" + self._current_input
        self._display_var.set(self._current_input)

    def _apply_percent(self) -> None:
        """Convert the current display value to its percentage (divide by 100)."""
        try:
            value = float(self._current_input)
        except ValueError:
            return
        result = value / 100.0
        self._current_input = self._format_number(result)
        self._display_var.set(self._current_input)

    def _execute_normal(self, chain: bool = False) -> None:
        """Evaluate the pending binary calculation and update the display.

        Args:
            chain: When True, the result is kept as the new first operand
                instead of clearing state after display.
        """
        if self._first_operand is None or self._operator is None:
            return

        try:
            second = float(self._current_input) if self._current_input else 0.0
        except ValueError:
            return

        method_name = BINARY_OPERATORS.get(self._operator)
        if method_name is None:
            return

        expr = (
            f"{self._format_number(self._first_operand)} "
            f"{self._operator} "
            f"{self._format_number(second)}"
        )

        try:
            result, _calc = run_calculation(self._first_operand, second, method_name)
        except ZeroDivisionError:
            self._show_error("Division by zero")
            return
        except ValueError as exc:
            self._show_error(str(exc))
            return

        formatted = self._format_number(result)
        self._history_var.set(f"{expr} =")
        self._display_var.set(formatted)
        self._logger.info(f"Normal calc: {expr} = {formatted}")

        if chain:
            self._first_operand = result
            self._current_input = formatted
            self._awaiting_second = True
        else:
            self._current_input = formatted
            self._first_operand = None
            self._operator = None
            self._awaiting_second = False

    # ------------------------------------------------------------------
    # Scientific-mode event handlers
    # ------------------------------------------------------------------

    def _on_sci_function(self, func_name: str) -> None:
        """Select the scientific function to apply.

        Args:
            func_name: One of the supported UNARY_FUNCTIONS keys
                (e.g. "sin", "sqrt").
        """
        self._sci_function = func_name
        self._sci_awaiting_arg = True
        self._current_input = ""
        self._display_var.set("0")
        self._history_var.set(f"{func_name}( ... )")

    def _on_sci_action(self, action: str) -> None:
        """Dispatch a scientific-mode button action.

        Args:
            action: A string token such as "num:3", "equals", "clear",
                or "negate".
        """
        if action == "clear":
            self._clear_state()
        elif action == "negate":
            self._negate_display()
        elif action == "equals":
            self._execute_scientific()
        elif action.startswith("num:"):
            digit = action[4:]
            self._append_digit(digit)

    def _execute_scientific(self) -> None:
        """Evaluate the pending unary scientific calculation and update display."""
        if self._sci_function is None:
            self._show_error("Select a function first")
            return

        try:
            operand = float(self._current_input) if self._current_input else 0.0
        except ValueError:
            self._show_error("Invalid operand")
            return

        method_name = UNARY_FUNCTIONS.get(self._sci_function)
        if method_name is None:
            self._show_error(f"Unknown function: {self._sci_function}")
            return

        expr = f"{self._sci_function}({self._format_number(operand)})"

        try:
            result, _calc = run_unary_calculation(operand, method_name)
        except ValueError as exc:
            self._show_error(str(exc))
            return

        formatted = self._format_number(result)
        self._history_var.set(f"{expr} =")
        self._display_var.set(formatted)
        self._logger.info(f"Scientific calc: {expr} = {formatted}")

        self._current_input = formatted
        self._sci_function = None
        self._sci_awaiting_arg = False

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def _clear_state(self) -> None:
        """Reset all input state and clear the display."""
        self._current_input = ""
        self._first_operand = None
        self._operator = None
        self._awaiting_second = False
        self._sci_function = None
        self._sci_awaiting_arg = False
        self._display_var.set("0")
        self._history_var.set("")

    def _show_error(self, message: str) -> None:
        """Display an error message on the calculator display.

        Args:
            message: Human-readable error text.
        """
        self._logger.error(f"GUI error: {message}")
        self._display_label.config(fg=_ERROR_FG)
        self._display_var.set(message[:16])
        # Reset colour after 2 seconds
        self._root.after(2000, lambda: self._display_label.config(fg=_DISPLAY_FG))
        self._clear_state()

    @staticmethod
    def _format_number(value: float) -> str:
        """Format a float for display, removing unnecessary trailing zeros.

        Args:
            value: The numeric value to format.

        Returns:
            A compact string representation (e.g. "3" instead of "3.0").
        """
        if value == int(value) and abs(value) < 1e15:
            return str(int(value))
        return f"{value:.10g}"

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the tkinter event loop.  Blocks until the window is closed."""
        self._root.mainloop()
