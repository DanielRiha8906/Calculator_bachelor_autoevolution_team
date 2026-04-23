"""Tkinter window layout and widget management for the Calculator GUI.

:class:`CalculatorWindow` is the main application window.  It owns all
widget construction, layout, and event-callback wiring.  All actual
computation is delegated to the injected :class:`~src.gui.session_adapter.GUISessionAdapter`.
"""

import tkinter as tk

from .session_adapter import GUISessionAdapter


# ---------------------------------------------------------------------------
# Module-level theme constants
# ---------------------------------------------------------------------------

_THEME: dict[str, str] = {
    "bg": "#000000",
    "fg": "#FFFFFF",
    "operator_bg": "#FF9500",
    "operator_active": "#FFB143",
    "sci_bg": "#1C1C1E",
    "sci_active": "#2C2C2E",
    "std_bg": "#333333",
    "std_active": "#4D4D4D",
    "mode_toggle_bg": "#1C1C1E",
    "mode_toggle_active": "#2C2C2E",
    "display_font": ("Courier", 32, "bold"),
    "button_font": ("Courier", 14, "bold"),
    "label_font": ("Courier", 11),
    "entry_font": ("Courier", 12),
    "history_font": ("Courier", 10),
    "error_fg": "#FF453A",
    "success_fg": "#30D158",
}

# ---------------------------------------------------------------------------
# Symbol mapping: canonical operation name → display symbol
# ---------------------------------------------------------------------------

_SYMBOL_MAP: dict[str, str] = {
    "add": "+",
    "subtract": "−",
    "multiply": "×",
    "divide": "÷",
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

# Operations that use the orange operator colour.
_ARITHMETIC_OPS: frozenset[str] = frozenset({"add", "subtract", "multiply", "divide"})


class CalculatorWindow(tk.Tk):
    """Main Tkinter window for the Calculator GUI.

    Layout (top to bottom):
    - Result display: large right-aligned label showing current result.
    - Mode toggle button: switches between normal and scientific modes.
    - Numbers grid: 3×4 grid of digit buttons (0-9).
    - Operations grid: dynamically built from the current mode's operations.
    - Input section: two Entry widgets labelled "Operand 1" / "Operand 2".
    - Execute button.
    - History section: scrollable read-only Text widget.
    - Clear History button.

    Args:
        session_adapter: A configured :class:`~src.gui.session_adapter.GUISessionAdapter`
            that handles all computation and history management.
    """

    def __init__(self, session_adapter: GUISessionAdapter) -> None:
        super().__init__()
        self._adapter: GUISessionAdapter = session_adapter
        self._selected_op: str | None = None

        # Track current mode for the toggle button label.
        self._current_mode: str = "normal"

        self.title("Calculator")
        self.resizable(True, True)
        self.minsize(420, 700)
        self.configure(bg=_THEME["bg"])

        self._build_ui()

        # Start with Normal mode pre-selected.
        self.on_mode_changed("normal")

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Construct and grid all widgets."""
        self.columnconfigure(0, weight=1)

        # ----------------------------------------------------------------
        # Row 0: Result display label
        # ----------------------------------------------------------------
        self._result_var = tk.StringVar(value="0")
        result_label = tk.Label(
            self,
            textvariable=self._result_var,
            anchor="e",
            justify="right",
            bg=_THEME["bg"],
            fg=_THEME["fg"],
            font=_THEME["display_font"],
            padx=12,
            pady=8,
        )
        result_label.grid(row=0, column=0, sticky="ew", padx=0, pady=(8, 0))
        self._result_label_widget = result_label

        # ----------------------------------------------------------------
        # Row 1: Mode toggle button
        # ----------------------------------------------------------------
        self._mode_toggle_btn = tk.Button(
            self,
            text="scientific",
            bg=_THEME["mode_toggle_bg"],
            fg=_THEME["fg"],
            activebackground=_THEME["mode_toggle_active"],
            activeforeground=_THEME["fg"],
            font=_THEME["button_font"],
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=6,
            command=self._on_mode_toggle_clicked,
        )
        self._mode_toggle_btn.grid(row=1, column=0, sticky="ew", padx=4, pady=4)
        self._bind_hover(
            self._mode_toggle_btn,
            _THEME["mode_toggle_bg"],
            _THEME["mode_toggle_active"],
        )

        # ----------------------------------------------------------------
        # Row 2: Numbers grid (3 columns × 4 rows)
        # ----------------------------------------------------------------
        numbers_frame = tk.Frame(self, bg=_THEME["bg"])
        numbers_frame.grid(row=2, column=0, sticky="ew", padx=4, pady=4)

        for col in range(3):
            numbers_frame.columnconfigure(col, weight=1)
        for row in range(4):
            numbers_frame.rowconfigure(row, weight=1)

        # Digit layout: rows 0-2 are 7-9, 4-6, 1-3; row 3 is 0 spanning all cols.
        digit_rows: list[list[str]] = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
        ]
        for row_idx, digits in enumerate(digit_rows):
            for col_idx, digit in enumerate(digits):
                btn = tk.Button(
                    numbers_frame,
                    text=digit,
                    bg=_THEME["std_bg"],
                    fg=_THEME["fg"],
                    activebackground=_THEME["std_active"],
                    activeforeground=_THEME["fg"],
                    font=_THEME["button_font"],
                    relief=tk.FLAT,
                    bd=0,
                    padx=4,
                    pady=10,
                )
                btn.grid(
                    row=row_idx, column=col_idx, sticky="nsew", padx=2, pady=2
                )
                self._bind_hover(btn, _THEME["std_bg"], _THEME["std_active"])

        # Row 3: digit 0 spanning all 3 columns.
        zero_btn = tk.Button(
            numbers_frame,
            text="0",
            bg=_THEME["std_bg"],
            fg=_THEME["fg"],
            activebackground=_THEME["std_active"],
            activeforeground=_THEME["fg"],
            font=_THEME["button_font"],
            relief=tk.FLAT,
            bd=0,
            padx=4,
            pady=10,
        )
        zero_btn.grid(
            row=3, column=0, columnspan=3, sticky="nsew", padx=2, pady=2
        )
        self._bind_hover(zero_btn, _THEME["std_bg"], _THEME["std_active"])

        # ----------------------------------------------------------------
        # Row 3: Operations grid (rebuilt on mode switch)
        # ----------------------------------------------------------------
        self._ops_frame = tk.Frame(self, bg=_THEME["bg"])
        self._ops_frame.grid(row=3, column=0, sticky="ew", padx=4, pady=4)

        # ----------------------------------------------------------------
        # Row 4: Input section
        # ----------------------------------------------------------------
        input_frame = tk.Frame(self, bg=_THEME["bg"])
        input_frame.grid(row=4, column=0, sticky="ew", padx=8, pady=4)
        input_frame.columnconfigure(1, weight=1)

        tk.Label(
            input_frame,
            text="Operand 1:",
            bg=_THEME["bg"],
            fg=_THEME["fg"],
            font=_THEME["label_font"],
        ).grid(row=0, column=0, sticky="w", padx=4, pady=2)

        self._operand1_entry = tk.Entry(
            input_frame,
            bg=_THEME["std_bg"],
            fg=_THEME["fg"],
            insertbackground=_THEME["fg"],
            font=_THEME["entry_font"],
            relief=tk.FLAT,
        )
        self._operand1_entry.grid(row=0, column=1, sticky="ew", padx=4, pady=2)

        self._operand2_label = tk.Label(
            input_frame,
            text="Operand 2:",
            bg=_THEME["bg"],
            fg=_THEME["fg"],
            font=_THEME["label_font"],
        )
        self._operand2_label.grid(row=1, column=0, sticky="w", padx=4, pady=2)

        self._operand2_entry = tk.Entry(
            input_frame,
            bg=_THEME["std_bg"],
            fg=_THEME["fg"],
            insertbackground=_THEME["fg"],
            font=_THEME["entry_font"],
            relief=tk.FLAT,
        )
        self._operand2_entry.grid(row=1, column=1, sticky="ew", padx=4, pady=2)

        # ----------------------------------------------------------------
        # Row 5: Execute button
        # ----------------------------------------------------------------
        execute_btn = tk.Button(
            self,
            text="Execute",
            bg=_THEME["operator_bg"],
            fg=_THEME["fg"],
            activebackground=_THEME["operator_active"],
            activeforeground=_THEME["fg"],
            font=_THEME["button_font"],
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=8,
            command=self.on_execute_clicked,
        )
        execute_btn.grid(row=5, column=0, sticky="ew", padx=8, pady=4)
        self._bind_hover(execute_btn, _THEME["operator_bg"], _THEME["operator_active"])

        # ----------------------------------------------------------------
        # Row 6: History section
        # ----------------------------------------------------------------
        history_frame = tk.Frame(self, bg=_THEME["bg"])
        history_frame.grid(row=6, column=0, sticky="nsew", padx=8, pady=4)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        self.rowconfigure(6, weight=2)

        self._history_text = tk.Text(
            history_frame,
            height=6,
            state="disabled",
            wrap="word",
            bg=_THEME["sci_bg"],
            fg=_THEME["fg"],
            insertbackground=_THEME["fg"],
            font=_THEME["history_font"],
            relief=tk.FLAT,
        )
        hist_scrollbar = tk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self._history_text.yview,
            bg=_THEME["std_bg"],
        )
        self._history_text.configure(yscrollcommand=hist_scrollbar.set)
        self._history_text.grid(row=0, column=0, sticky="nsew")
        hist_scrollbar.grid(row=0, column=1, sticky="ns")

        # ----------------------------------------------------------------
        # Row 7: Clear History button
        # ----------------------------------------------------------------
        clear_btn = tk.Button(
            self,
            text="Clear History",
            bg=_THEME["sci_bg"],
            fg=_THEME["fg"],
            activebackground=_THEME["sci_active"],
            activeforeground=_THEME["fg"],
            font=_THEME["button_font"],
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=6,
            command=self.on_clear_history_clicked,
        )
        clear_btn.grid(row=7, column=0, sticky="ew", padx=8, pady=(0, 8))
        self._bind_hover(clear_btn, _THEME["sci_bg"], _THEME["sci_active"])

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _bind_hover(btn: tk.Button, default_bg: str, active_bg: str) -> None:
        """Bind hover enter/leave colour transitions to *btn*.

        Args:
            btn: The :class:`tk.Button` to bind.
            default_bg: Background colour when the pointer is not over the button.
            active_bg: Background colour when the pointer is over the button.
        """
        btn.bind("<Enter>", lambda _e: btn.config(bg=active_bg))
        btn.bind("<Leave>", lambda _e: btn.config(bg=default_bg))

    def _op_colors(self, op_name: str) -> tuple[str, str]:
        """Return ``(default_bg, active_bg)`` for an operation button.

        Color assignment rules:
        - Arithmetic operators (add, subtract, multiply, divide): orange.
        - Scientific mode, non-arithmetic: dark sci grey.
        - Normal mode, non-arithmetic: standard grey.

        Args:
            op_name: The canonical operation name.

        Returns:
            A 2-tuple of ``(default_bg, active_bg)`` hex color strings.
        """
        if op_name in _ARITHMETIC_OPS:
            return _THEME["operator_bg"], _THEME["operator_active"]
        if self._current_mode == "scientific":
            return _THEME["sci_bg"], _THEME["sci_active"]
        return _THEME["std_bg"], _THEME["std_active"]

    def _on_mode_toggle_clicked(self) -> None:
        """Switch to the opposite mode and update the toggle button label."""
        new_mode = "scientific" if self._current_mode == "normal" else "normal"
        self.on_mode_changed(new_mode)

    def _set_result(self, text: str, is_error: bool = False) -> None:
        """Display *text* in the result label, coloured red if *is_error*.

        Args:
            text: The text to display.
            is_error: When ``True`` the label is coloured as an error.
        """
        self._result_var.set(text if text else "0")
        colour = _THEME["error_fg"] if is_error else _THEME["success_fg"]
        self._result_label_widget.configure(fg=colour)

    # ------------------------------------------------------------------
    # Public event handlers
    # ------------------------------------------------------------------

    def on_mode_changed(self, mode_name: str) -> None:
        """Switch the calculator to *mode_name* and refresh operation buttons.

        Args:
            mode_name: ``"normal"`` or ``"scientific"``.
        """
        self._current_mode = mode_name
        self._adapter.set_mode(mode_name)
        self._selected_op = None
        self._set_result("")

        # Update the toggle button label to show the *other* mode.
        toggle_label = "scientific" if mode_name == "normal" else "normal"
        self._mode_toggle_btn.configure(text=toggle_label)

        self.update_operation_buttons()

    def on_operation_selected(self, op_name: str) -> None:
        """Record the chosen operation and update the Operand 2 field state.

        Operand 2 is disabled for unary operations and re-enabled for binary
        ones.

        Args:
            op_name: The canonical operation name chosen by the user.
        """
        self._selected_op = op_name
        self._set_result("")

        arity = self._adapter.get_arity(op_name)
        if arity == 1:
            self._operand2_entry.delete(0, tk.END)
            self._operand2_entry.configure(state="disabled")
            self._operand2_label.configure(fg="grey")
        else:
            self._operand2_entry.configure(state="normal")
            self._operand2_label.configure(fg=_THEME["fg"])

    def on_execute_clicked(self) -> None:
        """Read inputs, execute the selected operation, and display the result.

        Shows an inline error message (without a popup dialog) when:
        - No operation has been selected.
        - An operand field contains a non-numeric value.
        - The calculator raises an exception (e.g. division by zero).
        """
        if self._selected_op is None:
            self._set_result("Please select an operation first.", is_error=True)
            return

        raw1 = self._operand1_entry.get().strip()
        try:
            op1 = float(raw1)
        except ValueError:
            self._set_result(
                f"Operand 1 is not a valid number: {raw1!r}", is_error=True
            )
            return

        arity = self._adapter.get_arity(self._selected_op)
        operands: list[float] = [op1]

        if arity > 1:
            raw2 = self._operand2_entry.get().strip()
            try:
                op2 = float(raw2)
            except ValueError:
                self._set_result(
                    f"Operand 2 is not a valid number: {raw2!r}", is_error=True
                )
                return
            operands.append(op2)

        result_str, error_msg = self._adapter.execute_operation_safe(
            self._selected_op, operands
        )

        if error_msg:
            self._set_result(f"Error: {error_msg}", is_error=True)
        else:
            self._set_result(f"Result: {result_str}")
            self.update_history_display()

    def on_clear_history_clicked(self) -> None:
        """Clear the session history and refresh the history display."""
        self._adapter.clear_history()
        self.update_history_display()

    def update_history_display(self) -> None:
        """Reload all history entries into the read-only history Text widget."""
        self._history_text.configure(state="normal")
        self._history_text.delete("1.0", tk.END)
        entries = self._adapter.get_history()
        for entry in entries:
            self._history_text.insert(tk.END, entry + "\n")
        self._history_text.configure(state="disabled")
        self._history_text.see(tk.END)

    def update_operation_buttons(self) -> None:
        """Rebuild the operation button grid for the current mode.

        Destroys all existing widgets in the operations frame and creates
        one :class:`tk.Button` per operation returned by the adapter, laid
        out in a 4-column grid with hover effects applied.
        """
        for widget in self._ops_frame.winfo_children():
            widget.destroy()

        operations = self._adapter.get_operations()
        columns = 4

        for col in range(columns):
            self._ops_frame.columnconfigure(col, weight=1)

        for idx, op_name in enumerate(operations):
            row, col = divmod(idx, columns)
            self._ops_frame.rowconfigure(row, weight=1)

            label = _SYMBOL_MAP.get(op_name, op_name)
            default_bg, active_bg = self._op_colors(op_name)

            btn = tk.Button(
                self._ops_frame,
                text=label,
                bg=default_bg,
                fg=_THEME["fg"],
                activebackground=active_bg,
                activeforeground=_THEME["fg"],
                font=_THEME["button_font"],
                relief=tk.FLAT,
                bd=0,
                padx=4,
                pady=10,
                command=lambda name=op_name: self.on_operation_selected(name),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            self._bind_hover(btn, default_bg, active_bg)
