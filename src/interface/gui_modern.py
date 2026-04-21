"""Modern iOS-inspired tkinter GUI for the Calculator.

Provides a flat-design calculator window with a hardcoded button layout
mirroring a standard iOS/mobile calculator.  Supports a standard 4-column
mode and an optional scientific panel that slides in to the left of the
standard grid when the Mode button is pressed.

The standard button layout (4 columns x 5 rows):

    C       Del     Mode    ÷
    7       8       9       ×
    4       5       6       +
    1       2       3       −
    0 (span=2)      .       =

The scientific panel (3 columns x 2 rows, shown to the left):

    √       x²      xʸ
    n!      ln      log
"""

import tkinter as tk
from typing import Optional

from src.calculator import Calculator
from src.context import CalculatorContext
from src.core.operations import OperationRegistry
from src.support.error_logger import ErrorLogger
from src.support.history import OperationHistory

# ---------------------------------------------------------------------------
# Color and font constants
# ---------------------------------------------------------------------------

BG_COLOR: str = "#000000"
NUM_BTN_COLOR: str = "#333333"
OP_BTN_COLOR: str = "#FF9500"
UTIL_BTN_COLOR: str = "#A5A5A5"
TEXT_COLOR: str = "#FFFFFF"
DISPLAY_FONT: tuple[str, int] = ("Arial", 28)
BTN_FONT: tuple[str, int] = ("Arial", 18)

# Operator symbols used on button faces (Unicode characters)
_DIV_SYMBOL = "÷"   # ÷
_MUL_SYMBOL = "×"   # ×
_SUB_SYMBOL = "−"   # −

# Mapping from button label to canonical Calculator operation name
_OPERATOR_MAP: dict[str, str] = {
    "+": "add",
    _SUB_SYMBOL: "subtract",
    _MUL_SYMBOL: "multiply",
    _DIV_SYMBOL: "divide",
}

_SCIENTIFIC_MAP: dict[str, str] = {
    "√": "square_root",   # √
    "x²": "square",       # x²
    "xʸ": "power",        # xʸ  (treated as binary: base=current, exp=next)
    "n!": "factorial",
    "ln": "natural_logarithm",
    "log": "logarithm",
}

# Standard button grid definition: each entry is (label, col, colspan)
# Rows are 0-indexed within the button area (display occupies grid row 0).
_STANDARD_ROWS: list[list[str]] = [
    ["C",    "Del",  "Mode",  _DIV_SYMBOL],   # row 0 of buttons → grid row 1
    ["7",    "8",    "9",     _MUL_SYMBOL],   # row 1 → grid row 2
    ["4",    "5",    "6",     "+"],            # row 2 → grid row 3
    ["1",    "2",    "3",     _SUB_SYMBOL],   # row 3 → grid row 4
    # Row 4: "0" spans 2 columns, then "." and "="
]

_SCIENTIFIC_LABELS: list[list[str]] = [
    ["√", "x²", "xʸ"],  # √  x²  xʸ
    ["n!",     "ln",      "log"],
]


class ModernGUIInterface(tk.Tk):
    """Modern iOS-inspired flat-design calculator GUI.

    Lays out a fixed button grid with a display panel at the top.  An
    optional scientific panel can be toggled via the "Mode" button; it
    appears to the left of the standard grid.

    Args:
        calculator: A :class:`~src.calculator.Calculator` instance.
        operation_registry: An :class:`~src.core.operations.OperationRegistry`
            instance used to dispatch operations.
        context: A :class:`~src.context.CalculatorContext` instance tracking
            the current mode.
        history: An :class:`~src.support.history.OperationHistory` instance.
        error_logger: An :class:`~src.support.error_logger.ErrorLogger`
            instance for logging calculation errors.
    """

    def __init__(
        self,
        calculator: Calculator,
        operation_registry: OperationRegistry,
        context: CalculatorContext,
        history: OperationHistory,
        error_logger: ErrorLogger,
    ) -> None:
        super().__init__()

        self._calculator = calculator
        self._registry = operation_registry
        self._context = context
        self._history = history
        self._error_logger = error_logger

        self.title("Calculator")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        # ------------------------------------------------------------------
        # Display state
        # ------------------------------------------------------------------
        self.display_var: tk.StringVar = tk.StringVar(value="0")
        self.current_input: str = ""
        self.operation: Optional[str] = None
        self.first_operand: Optional[str] = None
        self.result_shown: bool = False

        # Scientific mode visibility flag
        self.scientific_mode: bool = False

        # ------------------------------------------------------------------
        # Layout: scientific panel lives in column 0, standard grid in col 1
        # The scientific frame is placed via grid; standard buttons start at
        # an offset column within a shared master frame.
        # ------------------------------------------------------------------
        self._build_display_panel()
        self._build_standard_buttons()
        self._build_scientific_buttons()

        # Configure outer window column weights so both panels size correctly
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

    # ------------------------------------------------------------------
    # Panel builders
    # ------------------------------------------------------------------

    def _build_display_panel(self) -> None:
        """Create and place the top display label spanning all 4 standard columns.

        The label is placed in grid row 0 of the main window, spanning
        4 columns (columns 1–4 when the scientific panel is factored in, but
        since the scientific frame occupies column 0 as a whole unit, the
        display is spanned across the 4 standard button columns starting at
        column 1).
        """
        self._display_label = tk.Label(
            self,
            textvariable=self.display_var,
            anchor="e",
            justify="right",
            font=DISPLAY_FONT,
            fg=TEXT_COLOR,
            bg=BG_COLOR,
            padx=10,
            pady=10,
        )
        # columnspan=4 covers the four standard button columns (1-based col 1..4)
        self._display_label.grid(
            row=0,
            column=1,
            columnspan=4,
            sticky="nsew",
        )

    def _build_standard_buttons(self) -> None:
        """Create and place all standard-mode buttons in a 4-column x 5-row grid.

        Button grid rows are placed starting at grid row 1 (row 0 is the
        display).  The "0" button in the last row spans 2 columns.
        Color assignment:

        - ``UTIL_BTN_COLOR``: C, Del, Mode
        - ``OP_BTN_COLOR``: ÷, ×, +, −, =
        - ``NUM_BTN_COLOR``: 0–9, .
        """
        util_labels = {"C", "Del", "Mode"}
        op_labels = {_DIV_SYMBOL, _MUL_SYMBOL, "+", _SUB_SYMBOL, "="}

        # Rows 0–3: four buttons per row
        for row_idx, row_labels in enumerate(_STANDARD_ROWS):
            for col_idx, label in enumerate(row_labels):
                btn_color = self._button_color(label, util_labels, op_labels)
                btn = tk.Button(
                    self,
                    text=label,
                    font=BTN_FONT,
                    fg=TEXT_COLOR,
                    bg=btn_color,
                    activebackground=btn_color,
                    activeforeground=TEXT_COLOR,
                    relief="flat",
                    borderwidth=0,
                    command=lambda lbl=label: self._on_button_press(lbl),
                )
                btn.grid(
                    row=row_idx + 1,   # +1 because row 0 is the display
                    column=col_idx + 1,  # +1 because column 0 is scientific panel
                    padx=2,
                    pady=2,
                    sticky="nsew",
                )

        # Row 4 (grid row 5): "0" spanning 2 cols, then ".", "="
        last_row_grid = len(_STANDARD_ROWS) + 1  # = 5

        zero_btn = tk.Button(
            self,
            text="0",
            font=BTN_FONT,
            fg=TEXT_COLOR,
            bg=NUM_BTN_COLOR,
            activebackground=NUM_BTN_COLOR,
            activeforeground=TEXT_COLOR,
            relief="flat",
            borderwidth=0,
            command=lambda: self._on_button_press("0"),
        )
        zero_btn.grid(
            row=last_row_grid,
            column=1,
            columnspan=2,
            padx=2,
            pady=2,
            sticky="nsew",
        )

        for col_offset, label in enumerate([".", "="], start=3):
            btn_color = self._button_color(label, util_labels, op_labels)
            btn = tk.Button(
                self,
                text=label,
                font=BTN_FONT,
                fg=TEXT_COLOR,
                bg=btn_color,
                activebackground=btn_color,
                activeforeground=TEXT_COLOR,
                relief="flat",
                borderwidth=0,
                command=lambda lbl=label: self._on_button_press(lbl),
            )
            btn.grid(
                row=last_row_grid,
                column=col_offset,
                padx=2,
                pady=2,
                sticky="nsew",
            )

        # Configure standard button columns (1–4) and rows (1–5)
        for col in range(1, 5):
            self.columnconfigure(col, weight=1)
        for row in range(1, 6):
            self.rowconfigure(row, weight=1)

    def _build_scientific_buttons(self) -> None:
        """Create the scientific panel frame and place it in column 0.

        The frame contains a 3-column x 2-row grid of scientific function
        buttons.  It is hidden immediately after creation via
        ``grid_remove()`` and shown/hidden by :meth:`_on_mode_toggle`.
        """
        self.sci_frame = tk.Frame(self, bg=BG_COLOR)
        self.sci_frame.grid(
            row=1,
            column=0,
            rowspan=5,
            padx=2,
            pady=2,
            sticky="nsew",
        )

        for row_idx, row_labels in enumerate(_SCIENTIFIC_LABELS):
            for col_idx, label in enumerate(row_labels):
                btn = tk.Button(
                    self.sci_frame,
                    text=label,
                    font=BTN_FONT,
                    fg=TEXT_COLOR,
                    bg=NUM_BTN_COLOR,
                    activebackground=NUM_BTN_COLOR,
                    activeforeground=TEXT_COLOR,
                    relief="flat",
                    borderwidth=0,
                    command=lambda lbl=label: self._on_button_press(lbl),
                )
                btn.grid(
                    row=row_idx,
                    column=col_idx,
                    padx=2,
                    pady=2,
                    sticky="nsew",
                )

        for col in range(3):
            self.sci_frame.columnconfigure(col, weight=1)
        for row in range(2):
            self.sci_frame.rowconfigure(row, weight=1)

        # Hide the scientific panel until the user toggles it on
        self.sci_frame.grid_remove()

    # ------------------------------------------------------------------
    # Event routing
    # ------------------------------------------------------------------

    def _on_button_press(self, label: str) -> None:
        """Route a button press to the appropriate handler.

        Args:
            label: The text label of the button that was pressed.
        """
        if label == "C":
            self._on_clear()
        elif label == "Del":
            self._on_delete()
        elif label == "Mode":
            self._on_mode_toggle()
        elif label == "=":
            self._on_equals()
        elif label in _OPERATOR_MAP:
            self._on_operator(label)
        elif label in _SCIENTIFIC_MAP:
            self._on_scientific(label)
        else:
            self._on_digit(label)

    # ------------------------------------------------------------------
    # Input handlers
    # ------------------------------------------------------------------

    def _on_digit(self, label: str) -> None:
        """Append a digit or decimal point to the current input.

        Clears the current input first if a result was just shown.

        Args:
            label: The digit or ``"."`` character to append.
        """
        if self.result_shown:
            self.current_input = ""
            self.result_shown = False
        # Prevent multiple decimal points
        if label == "." and "." in self.current_input:
            return
        self.current_input += label
        self._update_display()

    def _on_operator(self, label: str) -> None:
        """Store the first operand and selected operator, then clear input.

        Maps the button symbol to the canonical operation name (e.g. ``"+"``
        becomes ``"add"``), stores the current display value as the first
        operand, and resets the current input for the second operand.

        Args:
            label: The operator symbol pressed (``+``, ``−``, ``×``, ``÷``).
        """
        if self.current_input or self.first_operand:
            if self.current_input:
                self.first_operand = self.current_input
            # If current_input is empty but first_operand already set, allow
            # changing the operator without losing the stored operand.
        self.operation = _OPERATOR_MAP[label]
        self.current_input = ""
        self.result_shown = False
        self._update_display(label)

    def _on_equals(self) -> None:
        """Evaluate the pending operation and display the result.

        Dispatches ``self.operation`` with the stored first operand and the
        current input via the :class:`~src.core.operations.OperationRegistry`.
        On success the result is displayed and recorded in history.  On error
        the error message is displayed and logged.
        """
        if self.operation is None or self.first_operand is None:
            return
        if not self.current_input:
            return

        first = self._parse_float(self.first_operand)
        second = self._parse_float(self.current_input)

        if first is None:
            self._display_error(f"Invalid first operand: {self.first_operand!r}")
            return
        if second is None:
            self._display_error(f"Invalid second operand: {self.current_input!r}")
            return

        try:
            result: float = self._registry.dispatch(self.operation, [first, second])
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            self._display_error(str(exc))
            self._error_logger.log_error(
                ErrorLogger.CALCULATION_ERROR,
                f"{self.operation}({first}, {second})",
                exc,
            )
            return

        result_str = self._format_result(result)
        self._history.record_operation(
            f"{self.operation}({first}, {second}) = {result_str}"
        )
        self.current_input = result_str
        self.first_operand = None
        self.operation = None
        self.result_shown = True
        self._update_display()

    def _on_clear(self) -> None:
        """Reset all display state to the initial cleared condition."""
        self.current_input = ""
        self.operation = None
        self.first_operand = None
        self.result_shown = False
        self._update_display("0")

    def _on_delete(self) -> None:
        """Remove the last character from the current input."""
        if self.result_shown:
            self._on_clear()
            return
        self.current_input = self.current_input[:-1]
        self._update_display()

    def _on_mode_toggle(self) -> None:
        """Toggle the scientific panel visibility and update calculator context.

        Shows the scientific button panel when switching to scientific mode,
        hides it when switching back to standard mode.  All display state is
        preserved across the toggle.
        """
        self.scientific_mode = not self.scientific_mode
        if self.scientific_mode:
            self.sci_frame.grid()
            self._context.set_mode("scientific")
            self._registry.set_mode("scientific")
        else:
            self.sci_frame.grid_remove()
            self._context.set_mode("normal")
            self._registry.set_mode("normal")

    def _on_scientific(self, label: str) -> None:
        """Evaluate a scientific (unary or binary) operation.

        Single-operand operations (``√``, ``x²``, ``n!``, ``ln``, ``log``)
        consume :attr:`current_input` directly.  The ``xʸ`` (power) operator
        is treated as a binary operation: it stores the current input as the
        base and waits for the exponent to be entered before pressing ``=``.

        Args:
            label: The scientific button label pressed.
        """
        operation_name = _SCIENTIFIC_MAP[label]

        # xʸ is a binary operation — store first operand and wait for =
        if operation_name == "power":
            if self.current_input:
                self.first_operand = self.current_input
            self.operation = "power"
            self.current_input = ""
            self.result_shown = False
            self._update_display("xʸ")
            return

        # All other scientific operations are unary — nothing to compute without input
        if not self.current_input:
            return

        operand = self._parse_float(self.current_input)
        if operand is None:
            self._display_error(f"Invalid input: {self.current_input!r}")
            return

        try:
            # The registry dispatches 'logarithm' as a two-argument log(x, base).
            # The "log" scientific button performs base-10 log (one operand), so
            # call the Calculator method directly to bypass the registry's
            # two-argument special case.
            if operation_name == "logarithm":
                result: float = self._calculator.logarithm(operand)
            else:
                result = self._registry.dispatch(operation_name, [operand])
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            self._display_error(str(exc))
            self._error_logger.log_error(
                ErrorLogger.CALCULATION_ERROR,
                f"{operation_name}({operand})",
                exc,
            )
            return

        result_str = self._format_result(result)
        self._history.record_operation(f"{operation_name}({operand}) = {result_str}")
        self.current_input = result_str
        self.result_shown = True
        self._update_display()

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def _update_display(self, text: Optional[str] = None) -> None:
        """Set the display label to *text* or derive content from state.

        Args:
            text: An explicit string to show.  When ``None`` the display
                shows :attr:`current_input` if non-empty, otherwise ``"0"``.
        """
        if text is not None:
            self.display_var.set(text)
        else:
            self.display_var.set(self.current_input if self.current_input else "0")

    def _display_error(self, message: str) -> None:
        """Show an error message in the display area.

        Args:
            message: The error description to display.
        """
        self.display_var.set(f"Error: {message}")
        self.current_input = ""
        self.result_shown = False

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _button_color(
        label: str,
        util_labels: set[str],
        op_labels: set[str],
    ) -> str:
        """Return the appropriate background color for a button label.

        Args:
            label: The button's text label.
            util_labels: Set of utility button labels (C, Del, Mode).
            op_labels: Set of operator button labels (+, −, ×, ÷, =).

        Returns:
            A hex color string from the module-level color constants.
        """
        if label in util_labels:
            return UTIL_BTN_COLOR
        if label in op_labels:
            return OP_BTN_COLOR
        return NUM_BTN_COLOR

    @staticmethod
    def _parse_float(raw: str) -> Optional[float]:
        """Attempt to parse *raw* as a float.

        Args:
            raw: The string to parse.

        Returns:
            The parsed ``float`` value, or ``None`` if parsing fails.
        """
        try:
            return float(raw)
        except ValueError:
            return None

    @staticmethod
    def _format_result(result: float) -> str:
        """Format a numeric result for display.

        Returns an integer representation when the value is a whole number
        (e.g. ``2.0`` → ``"2"``), otherwise a float string.

        Args:
            result: The numeric result to format.

        Returns:
            A clean string representation of *result*.
        """
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the Tkinter event loop.

        Blocks until the window is closed by the user.
        """
        self.mainloop()
