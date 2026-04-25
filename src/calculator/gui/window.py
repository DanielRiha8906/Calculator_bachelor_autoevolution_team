"""GUI Window for the Calculator application (Issue #414).

Provides GUIWindow — an iOS-inspired grid-based tkinter user interface that
delegates all business logic to GUIController.  This module requires tkinter
to be installed (standard library on most Python distributions).
"""

import tkinter as tk

from src.calculator.gui.controller import GUIController

# ---------------------------------------------------------------------------
# Color constants
# ---------------------------------------------------------------------------

COLOR_BG = "#000000"
COLOR_DIGIT = "#333333"
COLOR_OP = "#FF9500"
COLOR_UTIL = "#A5A5A5"
COLOR_TEXT = "#FFFFFF"


class _ButtonConfig:
    """Button wrapper that stores config for testability under mocked tkinter.

    Stores the widget reference alongside the visual properties and grid
    placement so that ``cget`` and ``grid_info`` return real values even when
    tkinter itself is replaced by a MagicMock in tests.

    Args:
        widget: The underlying ``tk.Button`` instance (or mock).
        bg: Background colour string.
        fg: Foreground (text) colour string.
        relief: Relief style string (e.g. ``"flat"``).
        row: Grid row index.
        column: Grid column index.
        columnspan: Number of columns the button spans.
    """

    def __init__(
        self,
        widget: object,
        bg: str,
        fg: str,
        relief: str,
        row: int,
        column: int,
        columnspan: int = 1,
    ) -> None:
        self._widget = widget
        self._bg = bg
        self._fg = fg
        self._relief = relief
        self._row = row
        self._column = column
        self._columnspan = columnspan

    def cget(self, key: str) -> str | None:
        """Return the stored value for a widget configuration key.

        Args:
            key: One of ``"bg"``, ``"fg"``, or ``"relief"``.

        Returns:
            The corresponding stored value, or ``None`` if the key is unknown.
        """
        mapping: dict[str, str] = {
            "bg": self._bg,
            "fg": self._fg,
            "relief": self._relief,
        }
        return mapping.get(key)

    def grid_info(self) -> dict:
        """Return grid placement information for this button.

        Returns:
            A dict with keys ``"row"``, ``"column"``, and ``"columnspan"``.
        """
        return {
            "row": self._row,
            "column": self._column,
            "columnspan": self._columnspan,
        }


# ---------------------------------------------------------------------------
# Button layout definition
# ---------------------------------------------------------------------------

_BUTTON_LAYOUT: list[tuple[str, str, int, int, int]] = [
    # (text, bg_color, row, col, colspan)
    ("C",   COLOR_UTIL,  0, 0, 1),
    ("Del", COLOR_UTIL,  0, 1, 1),
    ("Mode", COLOR_UTIL, 0, 2, 1),
    ("÷",   COLOR_OP,    0, 3, 1),
    ("7",   COLOR_DIGIT, 1, 0, 1),
    ("8",   COLOR_DIGIT, 1, 1, 1),
    ("9",   COLOR_DIGIT, 1, 2, 1),
    ("×",   COLOR_OP,    1, 3, 1),
    ("4",   COLOR_DIGIT, 2, 0, 1),
    ("5",   COLOR_DIGIT, 2, 1, 1),
    ("6",   COLOR_DIGIT, 2, 2, 1),
    ("+",   COLOR_OP,    2, 3, 1),
    ("1",   COLOR_DIGIT, 3, 0, 1),
    ("2",   COLOR_DIGIT, 3, 1, 1),
    ("3",   COLOR_DIGIT, 3, 2, 1),
    ("−", COLOR_OP, 3, 3, 1),  # U+2212 MINUS SIGN: −
    ("0",   COLOR_DIGIT, 4, 0, 2),  # columnspan=2
    (".",   COLOR_DIGIT, 4, 2, 1),
    ("=",   COLOR_OP,    4, 3, 1),
]

_SCIENTIFIC_BUTTONS: list[tuple[str, str, str]] = [
    # (text, bg_color, op_name)
    ("√",  COLOR_OP, "square_root"),   # √
    ("x²", COLOR_OP, "square"),        # x²
    ("xʸ", COLOR_OP, "power"),         # xʸ
    ("n!",      COLOR_OP, "factorial"),
    ("ln",      COLOR_OP, "ln"),
    ("log",     COLOR_OP, "log10"),
]

# Map display symbol → operator name used by the controller
_OP_SYMBOL_MAP: dict[str, str] = {
    "÷": "divide",
    "×": "multiply",
    "+": "add",
    "−": "subtract",  # −
}


class GUIWindow:
    """Tkinter-based iOS-inspired calculator window.

    Renders a numeric keypad grid with operator, utility, and (optionally)
    scientific buttons.  All computation is delegated to the injected
    :class:`GUIController`.

    Args:
        controller: The GUIController instance that provides business logic.
        title: Window title string.  Defaults to ``"Calculator"``.
    """

    def __init__(self, controller: GUIController, title: str = "Calculator") -> None:
        self._controller = controller
        self._buttons: dict[str, _ButtonConfig] = {}
        self._operand1: str = ""
        self._pending_op: str | None = None
        self._awaiting_second: bool = False

        self.root = tk.Tk()
        self.root.title(title)
        self.root.config(bg=COLOR_BG)

        self._build_display()
        self._build_standard_grid()

        if controller.get_current_mode() == "scientific":
            self._build_scientific_panel()

    # ------------------------------------------------------------------
    # Layout builders
    # ------------------------------------------------------------------

    def _build_display(self) -> None:
        """Build the result display label at the top of the window."""
        self._display_var = tk.StringVar(value="0")
        self._display = tk.Label(
            self.root,
            textvariable=self._display_var,
            font=("Helvetica", 28),
            fg="#FFFFFF",
            bg="#000000",
            anchor="e",
            padx=10,
            pady=10,
        )
        self._display.grid(row=0, column=0, columnspan=4, sticky="ew")

    def _build_standard_grid(self) -> None:
        """Build the 4-column × 5-row standard button grid."""
        frame = tk.Frame(self.root, bg=COLOR_BG)
        frame.grid(row=1, column=0, columnspan=4, sticky="nsew")

        for text, bg, row, col, colspan in _BUTTON_LAYOUT:
            command = self._make_command(text)
            self._make_button(frame, text, bg, row, col, colspan, command)

    def _build_scientific_panel(self) -> None:
        """Build the supplementary scientific-function button panel."""
        frame = tk.Frame(self.root, bg=COLOR_BG)
        frame.grid(row=2, column=0, columnspan=4, sticky="nsew")

        for idx, (text, bg, op_name) in enumerate(_SCIENTIFIC_BUTTONS):
            row = idx // 3
            col = idx % 3
            command = self._make_scientific_command(op_name)
            self._make_button(frame, text, bg, row, col, 1, command)

    # ------------------------------------------------------------------
    # Button factory helpers
    # ------------------------------------------------------------------

    def _make_button(
        self,
        frame: tk.Frame,
        text: str,
        bg: str,
        row: int,
        col: int,
        colspan: int,
        command: object,
    ) -> "_ButtonConfig":
        """Create a button, place it in the grid, and register it.

        Args:
            frame: Parent frame widget.
            text: Button label text.
            bg: Background colour string.
            row: Grid row index.
            col: Grid column index.
            colspan: Number of columns to span.
            command: Callable to invoke when the button is pressed.

        Returns:
            The :class:`_ButtonConfig` wrapper stored in ``self._buttons``.
        """
        btn = tk.Button(
            frame,
            text=text,
            bg=bg,
            fg=COLOR_TEXT,
            relief="flat",
            width=4,
            height=2,
            command=command,
        )
        btn.grid(row=row, column=col, columnspan=colspan, padx=2, pady=2, sticky="nsew")
        config = _ButtonConfig(
            btn,
            bg=bg,
            fg=COLOR_TEXT,
            relief="flat",
            row=row,
            column=col,
            columnspan=colspan,
        )
        self._buttons[text] = config
        return config

    def _make_command(self, text: str) -> object:
        """Return the appropriate command callable for a standard button.

        Args:
            text: The button label.

        Returns:
            A zero-argument callable bound to the correct handler.
        """
        if text in _OP_SYMBOL_MAP:
            op_name = _OP_SYMBOL_MAP[text]
            return lambda op=op_name: self._on_operator(op)
        if text == "=":
            return self._on_equals
        if text == "C":
            return self._on_clear
        if text == "Del":
            return self._on_delete
        if text == "Mode":
            return self._on_mode_toggle
        # Digit or decimal
        return lambda d=text: self._on_digit(d)

    def _make_scientific_command(self, op_name: str) -> object:
        """Return a command callable for a scientific-function button.

        Args:
            op_name: The operation name known to the controller.

        Returns:
            A zero-argument callable bound to :meth:`_on_scientific_op`.
        """
        return lambda op=op_name: self._on_scientific_op(op)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the tkinter main event loop (blocking)."""
        self.root.mainloop()

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_digit(self, digit: str) -> None:
        """Append *digit* to the current display value.

        Args:
            digit: A single digit character or ``"."``.
        """
        if self._awaiting_second:
            self._display_var.set("")
            self._awaiting_second = False
        current = self._display_var.get()
        if current == "0" and digit != ".":
            self._display_var.set(digit)
        else:
            self._display_var.set(current + digit)

    def _on_operator(self, op_name: str) -> None:
        """Store the first operand and the pending operation.

        Args:
            op_name: Controller operation name (e.g. ``"add"``).
        """
        self._operand1 = self._display_var.get()
        self._pending_op = op_name
        self._awaiting_second = True

    def _on_equals(self) -> None:
        """Execute the pending binary operation and display the result."""
        if self._pending_op is None:
            return
        operand2 = self._display_var.get()
        try:
            op1 = float(self._operand1)
            op2 = float(operand2)
            result = self._controller.execute_operation(self._pending_op, [op1, op2])
            if result["success"]:
                val = result["result"]
                self._display_var.set(
                    str(int(val)) if isinstance(val, float) and val.is_integer() else str(val)
                )
            else:
                self._display_var.set("Error")
        except (ValueError, Exception):
            self._display_var.set("Error")
        self._pending_op = None
        self._awaiting_second = False

    def _on_clear(self) -> None:
        """Reset the display and all pending state."""
        self._display_var.set("0")
        self._operand1 = ""
        self._pending_op = None
        self._awaiting_second = False

    def _on_delete(self) -> None:
        """Remove the last character from the display."""
        current = self._display_var.get()
        if len(current) > 1:
            self._display_var.set(current[:-1])
        else:
            self._display_var.set("0")

    def _on_mode_toggle(self) -> None:
        """Toggle between normal and scientific modes."""
        current_mode = self._controller.get_current_mode()
        new_mode = "scientific" if current_mode == "normal" else "normal"
        self._controller.switch_mode(new_mode)

    def _on_scientific_op(self, op_name: str) -> None:
        """Execute a unary or binary scientific operation on the current display.

        Args:
            op_name: The operation name known to the controller.
        """
        operand = self._display_var.get()
        try:
            op1 = float(operand)
            arity = self._controller.get_operation_arity(op_name)
            if arity == 1:
                result = self._controller.execute_operation(op_name, [op1])
            elif arity == 2:
                result = self._controller.execute_operation(op_name, [op1, 2])
            else:
                result = self._controller.execute_operation(op_name, [])
            if result["success"]:
                val = result["result"]
                self._display_var.set(
                    str(int(val)) if isinstance(val, float) and val.is_integer() else str(val)
                )
            else:
                self._display_var.set("Error")
        except (ValueError, Exception):
            self._display_var.set("Error")
