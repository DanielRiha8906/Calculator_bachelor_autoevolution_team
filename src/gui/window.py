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
    "square": "x²",
    "square_root": "√",
    "cube": "x³",
    "cube_root": "∛",
    "power": "xʸ",
    "factorial": "n!",
    "logarithm": "log",
    "natural_logarithm": "ln",
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "cot": "cot",
    "asin": "sin⁻¹",
    "acos": "cos⁻¹",
    "pi": "π",
    "e": "e",
}

# Base arithmetic operations — always displayed first in the operations grid.
_ARITHMETIC_OPS: tuple[str, ...] = ("add", "subtract", "multiply", "divide")


class CalculatorWindow(tk.Tk):
    """Main Tkinter window for the Calculator GUI.

    Layout (top to bottom):
    - Result display: large right-aligned label showing accumulated expression.
    - Mode toggle button: switches between normal and scientific modes.
    - Numbers grid: 3×4 grid of digit buttons (0-9), wired to :meth:`on_number_clicked`.
    - Operations grid: dynamically built from the current mode's operations,
      with base arithmetic operations always pinned to the top.
    - Execute / Equals button.
    - History toggle button: shows/hides the history panel.
    - History section: scrollable read-only Text widget (hidden by default).
    - Clear History button.

    Interaction model (iOS-style, button-only):
    - Digit buttons append to :attr:`_display_value`.
    - Binary operator buttons store operand1 and pend the operator.
    - The ``=`` button executes the pending binary operation.
    - Unary operator buttons execute immediately on the current display value.

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

        # Display accumulator — the string shown in the main display label.
        self._display_value: str = "0"
        self._display_var: tk.StringVar = tk.StringVar(value="0")

        # Tracks a pending binary operator waiting for the second operand.
        self._pending_binary_op: str | None = None

        # Whether the calculation history panel is visible.
        self._history_visible: bool = False

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
                    command=lambda d=digit: self.on_number_clicked(d),
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
            command=lambda: self.on_number_clicked("0"),
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
        # Row 4: Execute / Equals button
        # ----------------------------------------------------------------
        execute_btn = tk.Button(
            self,
            text="= / Execute",
            bg=_THEME["operator_bg"],
            fg=_THEME["fg"],
            activebackground=_THEME["operator_active"],
            activeforeground=_THEME["fg"],
            font=_THEME["button_font"],
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=8,
            command=self.on_equals_clicked,
        )
        execute_btn.grid(row=4, column=0, sticky="ew", padx=8, pady=4)
        self._bind_hover(execute_btn, _THEME["operator_bg"], _THEME["operator_active"])

        # ----------------------------------------------------------------
        # Row 5: History toggle button
        # ----------------------------------------------------------------
        self._history_toggle_btn = tk.Button(
            self,
            text="Show History",
            bg=_THEME["mode_toggle_bg"],
            fg=_THEME["fg"],
            activebackground=_THEME["mode_toggle_active"],
            activeforeground=_THEME["fg"],
            font=_THEME["button_font"],
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=6,
            command=self.on_history_toggle_clicked,
        )
        self._history_toggle_btn.grid(row=5, column=0, sticky="ew", padx=4, pady=4)
        self._bind_hover(
            self._history_toggle_btn,
            _THEME["mode_toggle_bg"],
            _THEME["mode_toggle_active"],
        )

        # ----------------------------------------------------------------
        # Row 6: History section (hidden by default)
        # ----------------------------------------------------------------
        self._history_frame = tk.Frame(self, bg=_THEME["bg"])
        self._history_frame.grid(row=6, column=0, sticky="nsew", padx=8, pady=4)
        self._history_frame.columnconfigure(0, weight=1)
        self._history_frame.rowconfigure(0, weight=1)
        self.rowconfigure(6, weight=2)

        self._history_text = tk.Text(
            self._history_frame,
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
            self._history_frame,
            orient="vertical",
            command=self._history_text.yview,
            bg=_THEME["std_bg"],
        )
        self._history_text.configure(yscrollcommand=hist_scrollbar.set)
        self._history_text.grid(row=0, column=0, sticky="nsew")
        hist_scrollbar.grid(row=0, column=1, sticky="ns")

        # Hide the history frame on startup.
        self._history_frame.grid_remove()

        # ----------------------------------------------------------------
        # Row 7: Clear History button (hidden by default alongside history)
        # ----------------------------------------------------------------
        self._clear_history_btn = tk.Button(
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
        self._clear_history_btn.grid(row=7, column=0, sticky="ew", padx=8, pady=(0, 8))
        self._bind_hover(self._clear_history_btn, _THEME["sci_bg"], _THEME["sci_active"])

        # Hide the clear-history button on startup to match hidden history panel.
        self._clear_history_btn.grid_remove()

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

    def on_number_clicked(self, digit: str) -> None:
        """Append *digit* to the display accumulator.

        If the current display value is ``"0"`` (the initial state), the digit
        replaces it rather than appending, so the display never shows a
        leading zero.

        Args:
            digit: A single digit character (``"0"``–``"9"``).
        """
        if self._display_value == "0":
            self._display_value = digit
        else:
            self._display_value += digit
        self._display_var.set(self._display_value)

    def on_mode_changed(self, mode_name: str) -> None:
        """Switch the calculator to *mode_name* and refresh operation buttons.

        Also clears any pending binary operation and resets the display.

        Args:
            mode_name: ``"normal"`` or ``"scientific"``.
        """
        self._current_mode = mode_name
        self._adapter.set_mode(mode_name)
        self._selected_op = None
        self._pending_binary_op = None
        self._adapter.clear_pending_operand()
        self._display_value = "0"
        self._display_var.set("0")
        self._set_result("")

        # Update the toggle button label to show the *other* mode.
        toggle_label = "scientific" if mode_name == "normal" else "normal"
        self._mode_toggle_btn.configure(text=toggle_label)

        self.update_operation_buttons()

    def on_operation_selected(self, op_name: str) -> None:
        """Handle an operation button press.

        For **unary** operations (arity=1): executes immediately on the
        current display value and shows the result.

        For **binary** operations (arity=2): stores the current display value
        as operand1, records the pending operator, and appends the operator
        symbol to the display expression so the user can see what they have
        typed so far.

        Args:
            op_name: The canonical operation name chosen by the user.
        """
        self._selected_op = op_name
        arity = self._adapter.get_arity(op_name)

        if arity == 1:
            # Execute immediately on the current display value.
            self._execute_unary_from_display(op_name)
        else:
            # Store first operand and arm the pending operator.
            try:
                op1_value = float(self._display_value)
            except ValueError:
                self._set_result(
                    f"Display is not a valid number: {self._display_value!r}",
                    is_error=True,
                )
                return
            self._adapter.store_first_operand(op1_value)
            self._pending_binary_op = op_name
            symbol = _SYMBOL_MAP.get(op_name, op_name)
            self._display_value = f"{self._display_value} {symbol} "
            self._display_var.set(self._display_value)
            self._set_result("")

    def _execute_unary_from_display(self, op_name: str) -> None:
        """Execute a unary *op_name* on the current display value.

        Updates the display with the result or shows an inline error.

        Args:
            op_name: The canonical unary operation name.
        """
        try:
            operand = float(self._display_value)
        except ValueError:
            self._set_result(
                f"Display is not a valid number: {self._display_value!r}",
                is_error=True,
            )
            return

        result_str, error_msg = self._adapter.execute_operation_safe(
            op_name, [operand]
        )
        if error_msg:
            self._set_result(f"Error: {error_msg}", is_error=True)
        else:
            self._display_value = result_str
            self._display_var.set(result_str)
            self._set_result(f"Result: {result_str}")
            self.update_history_display()

    def _execute_binary_operation(self) -> None:
        """Execute the pending binary operation using the current display value.

        Reads the second operand from the trailing portion of
        :attr:`_display_value` (everything after the last space following the
        operator symbol), delegates to the adapter with ``use_pending=True``,
        and updates the display with the result.

        Does nothing if :attr:`_pending_binary_op` is ``None``.
        """
        if self._pending_binary_op is None:
            return

        # The display looks like "3 + " or "3 + 4"; extract the second operand.
        raw_display = self._display_value.strip()
        parts = raw_display.split()
        # parts[-1] is either a digit string (operand2) or the operator symbol
        # when the user has not yet typed operand2.
        op_symbol = _SYMBOL_MAP.get(self._pending_binary_op, self._pending_binary_op)
        if parts and parts[-1] != op_symbol:
            raw2 = parts[-1]
        else:
            raw2 = ""

        if not raw2:
            self._set_result("Enter the second operand.", is_error=True)
            return

        try:
            op2 = float(raw2)
        except ValueError:
            self._set_result(
                f"Operand 2 is not a valid number: {raw2!r}", is_error=True
            )
            return

        result_str, error_msg = self._adapter.execute_operation_safe(
            self._pending_binary_op, [op2], use_pending=True
        )
        if error_msg:
            self._set_result(f"Error: {error_msg}", is_error=True)
        else:
            self._display_value = result_str
            self._display_var.set(result_str)
            self._pending_binary_op = None
            self._adapter.clear_pending_operand()
            self._set_result(f"Result: {result_str}")
            self.update_history_display()

    def on_equals_clicked(self) -> None:
        """Execute the accumulated expression or fall back to legacy entry flow.

        When a binary operation is pending (iOS-style flow), delegates to
        :meth:`_execute_binary_operation`.  Otherwise falls back to the
        legacy entry-widget execute flow so that keyboard-typed operands
        still work as before.
        """
        if self._pending_binary_op is not None:
            self._execute_binary_operation()
        else:
            self.on_execute_clicked()

    def on_execute_clicked(self) -> None:
        """Execute the pending binary operation via the accumulator-based flow.

        Delegates to :meth:`_execute_binary_operation` when a binary operator
        is pending.  When no operation is pending this is a no-op; the caller
        (:meth:`on_equals_clicked`) already handles this branch.
        """
        if self._pending_binary_op is not None:
            self._execute_binary_operation()

    def on_history_toggle_clicked(self) -> None:
        """Toggle the visibility of the history panel.

        When the panel is shown, the button label changes to ``"Hide History"``
        and vice versa.  The clear-history button is shown/hidden in sync with
        the history panel.
        """
        self._history_visible = not self._history_visible
        if self._history_visible:
            self._history_frame.grid()
            self._clear_history_btn.grid()
            self._history_toggle_btn.configure(text="Hide History")
        else:
            self._history_frame.grid_remove()
            self._clear_history_btn.grid_remove()
            self._history_toggle_btn.configure(text="Show History")

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

        Base arithmetic operations (defined in :data:`_ARITHMETIC_OPS`) are
        always pinned to the top of the grid; all other operations follow in
        the order returned by the adapter.
        """
        for widget in self._ops_frame.winfo_children():
            widget.destroy()

        all_operations: list[str] = self._adapter.get_operations()
        base_ops: list[str] = [op for op in _ARITHMETIC_OPS if op in all_operations]
        other_ops: list[str] = [op for op in all_operations if op not in set(_ARITHMETIC_OPS)]
        operations: list[str] = base_ops + other_ops

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
