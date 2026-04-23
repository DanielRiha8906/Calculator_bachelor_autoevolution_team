"""Tkinter window layout and widget management for the Calculator GUI.

:class:`CalculatorWindow` is the main application window.  It owns all
widget construction, layout, and event-callback wiring.  All actual
computation is delegated to the injected :class:`~src.gui.session_adapter.GUISessionAdapter`.

The UI follows an iOS-style dark calculator layout:
- Full-width result display (right-aligned, monospace)
- Single mode toggle button
- 3-column number grid (with "0" spanning full width)
- 4-column operations grid (dynamic rows based on available operations)
"""

import tkinter as tk

from .session_adapter import GUISessionAdapter


# ---------------------------------------------------------------------------
# Theme constants
# ---------------------------------------------------------------------------

_THEME: dict = {
    "window_bg": "#000000",
    "result": {
        "bg": "#000000",
        "fg": "#FFFFFF",
        "font": ("Courier New", 32, "bold"),
        "pad_x": 16,
        "pad_y": 12,
    },
    "colors": {
        "operator": {
            "bg": "#FF9500",
            "fg": "#FFFFFF",
            "activebackground": "#FFB143",
        },
        "scientific": {
            "bg": "#1C1C1E",
            "fg": "#FFFFFF",
            "activebackground": "#2C2C2E",
        },
        "number": {
            "bg": "#333333",
            "fg": "#FFFFFF",
            "activebackground": "#4D4D4D",
        },
        "mode_toggle": {
            "bg": "#FF9500",
            "fg": "#FFFFFF",
            "activebackground": "#FFB143",
        },
        "standard_op": {
            "bg": "#333333",
            "fg": "#FFFFFF",
            "activebackground": "#4D4D4D",
        },
    },
    "button_font": ("Helvetica", 20, "bold"),
    "mode_button_font": ("Helvetica", 14, "bold"),
    "frame_bg": "#000000",
}

# ---------------------------------------------------------------------------
# Operation symbol mapping
# ---------------------------------------------------------------------------

_OP_SYMBOLS: dict[str, str] = {
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

# Operations that belong to the orange "operator" colour group
_OPERATOR_OPS: frozenset[str] = frozenset({"add", "subtract", "multiply", "divide"})


class CalculatorWindow(tk.Tk):
    """Main Tkinter window for the Calculator GUI.

    Layout (top to bottom):
    - Result display: full-width label, right-aligned, black background, white text.
    - Mode toggle button: single button whose label reflects the *opposite* mode.
    - Numbers grid: 3 columns x 4 rows; the ``0`` key spans the full width.
    - Operations grid: 4 columns, dynamic rows based on available operations.

    Args:
        session_adapter: A configured :class:`~src.gui.session_adapter.GUISessionAdapter`
            that handles all computation and history management.
    """

    # Number pad layout (row-major, left-to-right, top-to-bottom).
    # Each entry is either a string digit label or ``None`` for an empty cell.
    _NUMBER_LAYOUT: list[list[str | None]] = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        ["0", None, None],  # "0" will be made to span all 3 columns
    ]

    def __init__(self, session_adapter: GUISessionAdapter) -> None:
        super().__init__()
        self._adapter: GUISessionAdapter = session_adapter
        self._selected_op: str | None = None
        self._current_mode: str = "normal"

        # Operand accumulator: collects digit characters typed via number pad.
        self._operand_buffer: str = ""

        self.title("Calculator")
        self.resizable(True, True)
        self.minsize(340, 560)
        self.configure(bg=_THEME["window_bg"])

        self._build_ui()

        # Start with Normal mode pre-selected.
        self.on_mode_changed("normal")

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Construct and grid all top-level sections."""
        self.columnconfigure(0, weight=1)
        # Result display gets no extra vertical weight; it's fixed height.
        self.rowconfigure(0, weight=0)
        # Mode toggle takes no extra space.
        self.rowconfigure(1, weight=0)
        # Numbers grid grows proportionally.
        self.rowconfigure(2, weight=3)
        # Operations grid grows proportionally.
        self.rowconfigure(3, weight=2)

        self._build_result_display()
        self._build_mode_toggle()
        self._build_numbers_grid()
        self._build_operations_grid()

    def _build_result_display(self) -> None:
        """Create the result display label at the top of the window."""
        theme = _THEME["result"]
        self._result_var = tk.StringVar(value="0")
        self._result_label = tk.Label(
            self,
            textvariable=self._result_var,
            bg=theme["bg"],
            fg=theme["fg"],
            font=theme["font"],
            anchor="e",
            padx=theme["pad_x"],
            pady=theme["pad_y"],
        )
        self._result_label.grid(row=0, column=0, sticky="ew")

    def _build_mode_toggle(self) -> None:
        """Create the single mode toggle button."""
        theme = _THEME["colors"]["mode_toggle"]
        self._mode_toggle_btn = tk.Button(
            self,
            text="Scientific",  # Will be updated by on_mode_changed
            bg=theme["bg"],
            fg=theme["fg"],
            activebackground=theme["activebackground"],
            activeforeground=theme["fg"],
            font=_THEME["mode_button_font"],
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self._on_mode_toggle_clicked,
        )
        self._mode_toggle_btn.grid(row=1, column=0, sticky="ew", padx=2, pady=2)
        self._bind_hover(
            self._mode_toggle_btn,
            theme["bg"],
            theme["activebackground"],
        )

    def _build_numbers_grid(self) -> None:
        """Create the 3-column number pad frame and populate it."""
        self._numbers_frame = tk.Frame(self, bg=_THEME["frame_bg"])
        self._numbers_frame.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)

        for col in range(3):
            self._numbers_frame.columnconfigure(col, weight=1)
        for row in range(len(self._NUMBER_LAYOUT)):
            self._numbers_frame.rowconfigure(row, weight=1)

        for row_idx, row_digits in enumerate(self._NUMBER_LAYOUT):
            for col_idx, digit in enumerate(row_digits):
                if digit is None:
                    # Empty placeholder — skip, the "0" span covers this space.
                    continue
                col_span = 3 if digit == "0" else 1
                self._make_number_button(
                    parent=self._numbers_frame,
                    label=digit,
                    row=row_idx,
                    col=col_idx,
                    col_span=col_span,
                )

    def _build_operations_grid(self) -> None:
        """Create the 4-column operations frame (populated on mode change)."""
        self._ops_frame = tk.Frame(self, bg=_THEME["frame_bg"])
        self._ops_frame.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)
        for col in range(4):
            self._ops_frame.columnconfigure(col, weight=1)

    # ------------------------------------------------------------------
    # Button factory helpers
    # ------------------------------------------------------------------

    def _make_number_button(
        self,
        parent: tk.Frame,
        label: str,
        row: int,
        col: int,
        col_span: int = 1,
    ) -> tk.Button:
        """Create and grid a single number pad button.

        Args:
            parent: The parent frame to place the button in.
            label: The digit string to display on the button.
            row: Grid row index.
            col: Grid column index.
            col_span: Number of columns the button should span (default 1).

        Returns:
            The created :class:`tk.Button` instance.
        """
        theme = _THEME["colors"]["number"]
        btn = tk.Button(
            parent,
            text=label,
            bg=theme["bg"],
            fg=theme["fg"],
            activebackground=theme["activebackground"],
            activeforeground=theme["fg"],
            font=_THEME["button_font"],
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda d=label: self._on_digit_pressed(d),
        )
        btn.grid(
            row=row,
            column=col,
            columnspan=col_span,
            sticky="nsew",
            padx=1,
            pady=1,
        )
        self._bind_hover(btn, theme["bg"], theme["activebackground"])
        return btn

    def _make_op_button(
        self,
        parent: tk.Frame,
        op_name: str,
        row: int,
        col: int,
        is_scientific: bool,
    ) -> tk.Button:
        """Create and grid a single operation button.

        The button colour is determined by whether the operation is a core
        arithmetic operator or a scientific/utility function.

        Args:
            parent: The parent frame to place the button in.
            op_name: The canonical operation name (e.g. ``"add"``).
            row: Grid row index.
            col: Grid column index.
            is_scientific: ``True`` when the calculator is in scientific mode.

        Returns:
            The created :class:`tk.Button` instance.
        """
        label = _OP_SYMBOLS.get(op_name, op_name)

        if op_name in _OPERATOR_OPS:
            color_key = "operator"
        elif is_scientific:
            color_key = "scientific"
        else:
            color_key = "standard_op"

        theme = _THEME["colors"][color_key]
        btn = tk.Button(
            parent,
            text=label,
            bg=theme["bg"],
            fg=theme["fg"],
            activebackground=theme["activebackground"],
            activeforeground=theme["fg"],
            font=_THEME["button_font"],
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda name=op_name: self.on_operation_selected(name),
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
        self._bind_hover(btn, theme["bg"], theme["activebackground"])
        return btn

    # ------------------------------------------------------------------
    # Hover effect
    # ------------------------------------------------------------------

    @staticmethod
    def _bind_hover(
        btn: tk.Button,
        normal_color: str,
        hover_color: str,
    ) -> None:
        """Attach ``<Enter>``/``<Leave>`` hover colour-swap events to *btn*.

        Args:
            btn: The button widget to bind events on.
            normal_color: Background colour when the pointer is not over the button.
            hover_color: Background colour when the pointer is over the button.
        """
        btn.bind(
            "<Enter>",
            lambda _event, b=btn, c=hover_color: b.configure(bg=c),
        )
        btn.bind(
            "<Leave>",
            lambda _event, b=btn, c=normal_color: b.configure(bg=c),
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _on_digit_pressed(self, digit: str) -> None:
        """Append *digit* to the operand buffer and update the display.

        Args:
            digit: A single decimal digit character (``"0"``–``"9"``).
        """
        self._operand_buffer += digit
        self._result_var.set(self._operand_buffer)

    def _on_mode_toggle_clicked(self) -> None:
        """Toggle between ``"normal"`` and ``"scientific"`` modes."""
        next_mode = "scientific" if self._current_mode == "normal" else "normal"
        self.on_mode_changed(next_mode)

    def _set_result(self, text: str) -> None:
        """Set the result display text.

        Args:
            text: The string to show in the result area.
        """
        self._result_var.set(text)

    def _execute_current_operation(self) -> None:
        """Execute the currently selected operation using the buffered operand.

        Reads the operand buffer, parses it as a float, and delegates to
        the adapter.  On success the result is shown; on error an inline
        error message is displayed.  Binary operations that need a second
        operand are currently not supported by the number-pad flow and will
        show an informative message.
        """
        if self._selected_op is None:
            self._set_result("Select an operation")
            return

        raw = self._operand_buffer.strip()
        if not raw:
            self._set_result("Enter a number")
            return

        try:
            op1 = float(raw)
        except ValueError:
            self._set_result(f"Invalid: {raw!r}")
            return

        arity = self._adapter.get_arity(self._selected_op)
        operands: list[float] = [op1]

        if arity > 1:
            # Binary operations via number-pad flow are not yet supported;
            # provide a clear user message rather than silently failing.
            self._set_result("Use operand entry for binary ops")
            return

        result_str, error_msg = self._adapter.execute_operation_safe(
            self._selected_op, operands
        )

        if error_msg:
            self._set_result(f"Error: {error_msg}")
        else:
            self._operand_buffer = result_str
            self._set_result(result_str)

    # ------------------------------------------------------------------
    # Public event handlers
    # ------------------------------------------------------------------

    def on_mode_changed(self, mode_name: str) -> None:
        """Switch the calculator to *mode_name* and refresh operation buttons.

        Updates the mode toggle button label to show the *opposite* mode
        (so the user knows what they will switch to on next click).

        Args:
            mode_name: ``"normal"`` or ``"scientific"``.
        """
        self._current_mode = mode_name
        self._adapter.set_mode(mode_name)
        self._selected_op = None
        self._set_result("0")
        self._operand_buffer = ""

        # Toggle button shows the *other* mode name
        opposite = "Scientific" if mode_name == "normal" else "Normal"
        self._mode_toggle_btn.configure(text=opposite)

        self.update_operation_buttons()

    def on_operation_selected(self, op_name: str) -> None:
        """Record the chosen operation and auto-execute for unary operations.

        For unary operations, immediately executes against the current
        buffer when a number is already present.  For binary operations,
        simply records the selection for a subsequent execution.

        Args:
            op_name: The canonical operation name chosen by the user.
        """
        self._selected_op = op_name
        arity = self._adapter.get_arity(op_name)
        if arity == 1 and self._operand_buffer:
            self._execute_current_operation()
        else:
            symbol = _OP_SYMBOLS.get(op_name, op_name)
            self._set_result(f"{symbol} ...")

    def update_operation_buttons(self) -> None:
        """Rebuild the operation button grid for the current mode.

        Destroys all existing buttons in the operations frame and creates
        one button per operation returned by the adapter.  Buttons are laid
        out in a 4-column grid; rows are added dynamically.
        """
        for widget in self._ops_frame.winfo_children():
            widget.destroy()

        operations = self._adapter.get_operations()
        columns = 4
        is_scientific = self._current_mode == "scientific"

        for row_idx in range((len(operations) + columns - 1) // columns):
            self._ops_frame.rowconfigure(row_idx, weight=1)

        for idx, op_name in enumerate(operations):
            row, col = divmod(idx, columns)
            self._make_op_button(
                parent=self._ops_frame,
                op_name=op_name,
                row=row,
                col=col,
                is_scientific=is_scientific,
            )
