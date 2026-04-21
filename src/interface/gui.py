"""Tkinter-based GUI interface for the Calculator.

Provides an iOS-inspired dark-theme windowed interface with a compact button
grid.  Operation buttons are generated dynamically from the operation registry
and rebuilt whenever the active mode changes.  Business logic (calculation
dispatch, mode switching) is delegated to the existing Calculator and
OperationRegistry infrastructure.
"""

import tkinter as tk
from typing import Optional

from src.context import CalculatorContext
from src.core.operations import Operation, OperationRegistry
from src.support.error_logger import ErrorLogger
from src.support.history import OperationHistory

# ---------------------------------------------------------------------------
# Color palette — iOS-inspired dark theme
# ---------------------------------------------------------------------------

COLOR_BACKGROUND = "#000000"
COLOR_BUTTON_STANDARD = "#333333"
COLOR_BUTTON_OPERATOR = "#FF9500"
COLOR_BUTTON_UTILITY = "#A5A5A5"
COLOR_TEXT_RESULT = "#FFFFFF"
COLOR_TEXT_BUTTON = "#FFFFFF"


class GUIInterface(tk.Tk):
    """Tkinter GUI for the calculator application.

    Renders an iOS-inspired dark calculator layout with three sections:

    1. **Result panel** (top): a right-aligned display label showing the
       current input or computed result.
    2. **Mode toggle** (middle): two buttons to switch between
       ``"normal"`` and ``"scientific"`` modes.
    3. **Button grid** (bottom): a grid of calculator buttons whose layout
       and content depend on the active mode.

    Args:
        calculator: A ``Calculator`` instance whose methods will be called.
        operation_registry: An ``OperationRegistry`` instance used to retrieve
            available operations and dispatch them.
        context: A ``CalculatorContext`` instance tracking the current mode.
        history: An ``OperationHistory`` instance used to persist results.
        error_logger: An ``ErrorLogger`` instance used to log errors.
    """

    def __init__(
        self,
        calculator,
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
        self.resizable(False, False)
        self.configure(bg=COLOR_BACKGROUND)
        self.geometry("320x560")

        # ------------------------------------------------------------------
        # Internal state machine
        # ------------------------------------------------------------------
        self._current_input: str = "0"
        self._pending_operand_1: Optional[float] = None
        self._pending_operation: Optional[str] = None
        self._result_shown: bool = False

        # ------------------------------------------------------------------
        # Build UI
        # ------------------------------------------------------------------
        self._build_result_panel()
        self._build_mode_toggle()
        self._build_calculator_grid()

    # ------------------------------------------------------------------
    # Panel builders
    # ------------------------------------------------------------------

    def _build_result_panel(self) -> None:
        """Create the top result/input display panel.

        Stores the display label as ``self._display_label`` with initial
        text ``"0"``.
        """
        result_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
        result_frame.pack(fill=tk.X, padx=8, pady=(16, 4))

        self._display_label = tk.Label(
            result_frame,
            text="0",
            font=("TkDefaultFont", 28, "bold"),
            fg=COLOR_TEXT_RESULT,
            bg=COLOR_BACKGROUND,
            anchor=tk.E,
            justify=tk.RIGHT,
        )
        self._display_label.pack(fill=tk.X, padx=8)

    def _build_mode_toggle(self) -> None:
        """Create the mode toggle buttons above the calculator grid.

        Two flat buttons — ``"Normal"`` and ``"Scientific"`` — switch the
        active mode and rebuild the button grid.
        """
        toggle_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
        toggle_frame.pack(fill=tk.X, padx=8, pady=(0, 4))

        normal_btn = tk.Button(
            toggle_frame,
            text="Normal",
            bg=COLOR_BUTTON_UTILITY,
            fg="#000000",
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=4,
            command=lambda: self._on_switch_mode("normal"),
        )
        normal_btn.pack(side=tk.LEFT, padx=2)

        scientific_btn = tk.Button(
            toggle_frame,
            text="Scientific",
            bg=COLOR_BUTTON_UTILITY,
            fg="#000000",
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=4,
            command=lambda: self._on_switch_mode("scientific"),
        )
        scientific_btn.pack(side=tk.LEFT, padx=2)

    def _build_calculator_grid(self) -> None:
        """Build (or rebuild) the calculator button grid for the current mode.

        Removes any previously rendered button grid, then creates a new one
        according to the active mode.  The button frame is stored as
        ``self._buttons_frame``.

        Normal mode layout (rows top to bottom):
            Row 0: C, DEL, (empty), ÷
            Row 1: 7, 8, 9, ×
            Row 2: 4, 5, 6, −
            Row 3: 1, 2, 3, +
            Row 4: 0 (colspan 2), ., =

        Scientific mode adds an extra row above the normal grid for
        scientific operations drawn from the registry.
        """
        # Destroy any existing grid
        if hasattr(self, "_buttons_frame") and self._buttons_frame is not None:
            self._buttons_frame.destroy()

        self._buttons_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
        self._buttons_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Determine whether we are in scientific mode
        is_scientific = self._context.get_mode() == "scientific"

        # Collect scientific-only operations from the registry when needed
        scientific_ops: list[Operation] = []
        if is_scientific:
            all_ops = self._registry.get_operations()
            scientific_ops = [
                op for op in all_ops
                if op.mode == "scientific"
            ]

        row_offset = 0

        # ------------------------------------------------------------------
        # Scientific extra rows (shown only in scientific mode)
        # ------------------------------------------------------------------
        if is_scientific and scientific_ops:
            sci_cols = 3
            for idx, op in enumerate(scientific_ops):
                r, c = divmod(idx, sci_cols)
                symbol = self._map_operation_to_symbol(op.name)
                btn = tk.Button(
                    self._buttons_frame,
                    text=symbol,
                    bg=COLOR_BUTTON_STANDARD,
                    fg=COLOR_TEXT_BUTTON,
                    relief=tk.FLAT,
                    bd=0,
                    width=6,
                    height=2,
                    command=lambda name=op.name: self._press_unary_op(name),
                )
                btn.grid(row=r, column=c, padx=1, pady=1, sticky=tk.NSEW)

            sci_rows = -(-len(scientific_ops) // sci_cols)  # ceiling division
            row_offset = sci_rows

            # Configure scientific columns
            for c in range(sci_cols):
                self._buttons_frame.columnconfigure(c, weight=1)

        # ------------------------------------------------------------------
        # Standard 4-column grid
        # ------------------------------------------------------------------
        # Row 0: C, DEL, (empty), ÷
        self._make_button("C",    row_offset + 0, 0, COLOR_BUTTON_UTILITY, self._press_clear)
        self._make_button("DEL",  row_offset + 0, 1, COLOR_BUTTON_UTILITY, self._press_backspace)
        # Empty placeholder
        tk.Label(
            self._buttons_frame, bg=COLOR_BACKGROUND
        ).grid(row=row_offset + 0, column=2, padx=1, pady=1, sticky=tk.NSEW)
        self._make_button("÷", row_offset + 0, 3, COLOR_BUTTON_OPERATOR,
                          lambda: self._press_operator("divide"))

        # Row 1: 7, 8, 9, ×
        self._make_button("7", row_offset + 1, 0, COLOR_BUTTON_STANDARD,
                          lambda: self._append_digit("7"))
        self._make_button("8", row_offset + 1, 1, COLOR_BUTTON_STANDARD,
                          lambda: self._append_digit("8"))
        self._make_button("9", row_offset + 1, 2, COLOR_BUTTON_STANDARD,
                          lambda: self._append_digit("9"))
        self._make_button("×", row_offset + 1, 3, COLOR_BUTTON_OPERATOR,
                          lambda: self._press_operator("multiply"))

        # Row 2: 4, 5, 6, −
        self._make_button("4", row_offset + 2, 0, COLOR_BUTTON_STANDARD,
                          lambda: self._append_digit("4"))
        self._make_button("5", row_offset + 2, 1, COLOR_BUTTON_STANDARD,
                          lambda: self._append_digit("5"))
        self._make_button("6", row_offset + 2, 2, COLOR_BUTTON_STANDARD,
                          lambda: self._append_digit("6"))
        self._make_button("−", row_offset + 2, 3, COLOR_BUTTON_OPERATOR,
                          lambda: self._press_operator("subtract"))

        # Row 3: 1, 2, 3, +
        self._make_button("1", row_offset + 3, 0, COLOR_BUTTON_STANDARD,
                          lambda: self._append_digit("1"))
        self._make_button("2", row_offset + 3, 1, COLOR_BUTTON_STANDARD,
                          lambda: self._append_digit("2"))
        self._make_button("3", row_offset + 3, 2, COLOR_BUTTON_STANDARD,
                          lambda: self._append_digit("3"))
        self._make_button("+", row_offset + 3, 3, COLOR_BUTTON_OPERATOR,
                          lambda: self._press_operator("add"))

        # Row 4: 0 (span 2 cols), ., =
        zero_btn = tk.Button(
            self._buttons_frame,
            text="0",
            bg=COLOR_BUTTON_STANDARD,
            fg=COLOR_TEXT_BUTTON,
            relief=tk.FLAT,
            bd=0,
            height=2,
            command=lambda: self._append_digit("0"),
        )
        zero_btn.grid(
            row=row_offset + 4, column=0, columnspan=2,
            padx=1, pady=1, sticky=tk.NSEW
        )
        self._make_button(".", row_offset + 4, 2, COLOR_BUTTON_UTILITY,
                          lambda: self._append_digit("."))
        self._make_button("=", row_offset + 4, 3, COLOR_BUTTON_UTILITY,
                          self._press_equals)

        # Configure the 4 standard columns to expand equally
        for c in range(4):
            self._buttons_frame.columnconfigure(c, weight=1)

        # Configure all rows to expand equally
        total_rows = row_offset + 5
        for r in range(total_rows):
            self._buttons_frame.rowconfigure(r, weight=1)

    # ------------------------------------------------------------------
    # Button factory helper
    # ------------------------------------------------------------------

    def _make_button(
        self,
        text: str,
        row: int,
        col: int,
        color: str,
        command,
    ) -> tk.Button:
        """Create and grid a single calculator button.

        Args:
            text: The label displayed on the button.
            row: The grid row index.
            col: The grid column index.
            color: The background color for the button.
            command: The callable invoked when the button is pressed.

        Returns:
            The created ``tk.Button`` instance.
        """
        btn = tk.Button(
            self._buttons_frame,
            text=text,
            bg=color,
            fg=COLOR_TEXT_BUTTON,
            relief=tk.FLAT,
            bd=0,
            width=6,
            height=2,
            command=command,
        )
        btn.grid(row=row, column=col, padx=1, pady=1, sticky=tk.NSEW)
        return btn

    # ------------------------------------------------------------------
    # Symbol mapping
    # ------------------------------------------------------------------

    @staticmethod
    def _map_operation_to_symbol(operation_name: str) -> str:
        """Map a canonical operation name to its display symbol.

        Args:
            operation_name: The canonical operation name (e.g. ``"add"``).

        Returns:
            A UTF-8 symbol string suitable for a button label.  Returns
            *operation_name* unchanged when no mapping exists.
        """
        _SYMBOL_MAP: dict[str, str] = {
            "add":               "+",
            "subtract":          "−",  # −
            "multiply":          "×",  # ×
            "divide":            "÷",  # ÷
            "square":            "x²",  # x²
            "cube":              "x³",  # x³
            "power":             "xʸ",  # xʸ
            "factorial":         "n!",
            "square_root":       "√",   # √
            "natural_logarithm": "ln",
            "logarithm":         "log",
            "sin":               "sin",
            "cos":               "cos",
            "tan":               "tan",
        }
        return _SYMBOL_MAP.get(operation_name, operation_name)

    # ------------------------------------------------------------------
    # Event handlers — input state machine
    # ------------------------------------------------------------------

    def _append_digit(self, digit: str) -> None:
        """Append a digit or decimal point to the current input.

        Replaces the display when a result has just been shown.  Prevents
        duplicate decimal points from being entered.

        Args:
            digit: A single character — ``"0"``–``"9"`` or ``"."``.
        """
        if self._result_shown:
            # Start fresh after a completed calculation
            self._current_input = "0"
            self._result_shown = False

        if digit == ".":
            if "." in self._current_input:
                return  # only one decimal point allowed
            self._current_input += digit
        elif self._current_input == "0":
            self._current_input = digit
        else:
            self._current_input += digit

        self._update_display(self._current_input)

    def _press_operator(self, op_name: str) -> None:
        """Store the current input and operator for a pending binary operation.

        If a previous binary operation is already pending and a second number
        has been entered, evaluates the pending operation first (chained input)
        before storing the new operator.

        Args:
            op_name: The canonical operation name for a binary operator
                (e.g. ``"add"``, ``"subtract"``).
        """
        try:
            current_value = float(self._current_input)
        except ValueError:
            self._update_display("Error")
            return

        # Chain: if a binary op is already pending and the user enters another
        # operator, evaluate the pending op first.
        if self._pending_operation is not None and not self._result_shown:
            try:
                result = self._registry.dispatch(
                    self._pending_operation,
                    [self._pending_operand_1, current_value],
                )
                current_value = result
                self._update_display(self._format_number(result))
            except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
                self._update_display(f"Error: {exc}")
                self._error_logger.log_error(
                    ErrorLogger.CALCULATION_ERROR,
                    f"{self._pending_operation}({self._pending_operand_1}, {current_value})",
                    exc,
                )
                self._pending_operation = None
                self._pending_operand_1 = None
                return

        self._pending_operand_1 = current_value
        self._pending_operation = op_name
        self._result_shown = True  # next digit press starts fresh

    def _press_equals(self) -> None:
        """Execute the pending binary operation and display the result.

        Does nothing when no operation is pending.  Records the result in
        history and logs errors via the ``ErrorLogger``.
        """
        if self._pending_operation is None or self._pending_operand_1 is None:
            return

        try:
            operand2 = float(self._current_input)
        except ValueError:
            self._update_display("Error")
            return

        try:
            result = self._registry.dispatch(
                self._pending_operation,
                [self._pending_operand_1, operand2],
            )
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            self._update_display(f"Error: {exc}")
            operand_str = f"{self._pending_operand_1}, {operand2}"
            self._error_logger.log_error(
                ErrorLogger.CALCULATION_ERROR,
                f"{self._pending_operation}({operand_str})",
                exc,
            )
            self._pending_operation = None
            self._pending_operand_1 = None
            return

        result_text = (
            f"{self._pending_operation}"
            f"({self._pending_operand_1}, {operand2}) = {result}"
        )
        self._history.record_operation(result_text)

        formatted = self._format_number(result)
        self._current_input = formatted
        self._update_display(formatted)
        self._result_shown = True
        self._pending_operation = None
        self._pending_operand_1 = None

    def _press_clear(self) -> None:
        """Reset all input state and show ``"0"`` on the display."""
        self._current_input = "0"
        self._pending_operand_1 = None
        self._pending_operation = None
        self._result_shown = False
        self._update_display("0")

    def _press_backspace(self) -> None:
        """Remove the last character from the current input.

        If the result is being displayed after an ``=`` press, clears to
        ``"0"`` instead of removing a character from the result.  Ensures
        the display never becomes empty by falling back to ``"0"``.
        """
        if self._result_shown:
            self._press_clear()
            return

        if len(self._current_input) <= 1:
            self._current_input = "0"
        else:
            self._current_input = self._current_input[:-1]

        self._update_display(self._current_input)

    def _press_unary_op(self, op_name: str) -> None:
        """Apply a unary operation to the current display value.

        Dispatches the operation through the registry, shows the result, and
        records it in history.

        Args:
            op_name: The canonical name of the unary operation
                (e.g. ``"square_root"``, ``"factorial"``).
        """
        try:
            operand = float(self._current_input)
        except ValueError:
            self._update_display("Error")
            return

        try:
            result = self._registry.dispatch(op_name, [operand])
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            self._update_display(f"Error: {exc}")
            self._error_logger.log_error(
                ErrorLogger.CALCULATION_ERROR,
                f"{op_name}({operand})",
                exc,
            )
            return

        result_text = f"{op_name}({operand}) = {result}"
        self._history.record_operation(result_text)

        formatted = self._format_number(result)
        self._current_input = formatted
        self._update_display(formatted)
        self._result_shown = True

    def _update_display(self, text: str) -> None:
        """Update the result display label.

        Args:
            text: The string to show on the display.
        """
        self._display_label.config(text=text)

    # ------------------------------------------------------------------
    # Mode switching
    # ------------------------------------------------------------------

    def _on_switch_mode(self, new_mode: str) -> None:
        """Switch to *new_mode* and rebuild the calculator grid.

        Keeps ``CalculatorContext`` and ``OperationRegistry`` in sync.

        Args:
            new_mode: The target mode — either ``"normal"`` or
                ``"scientific"``.
        """
        if new_mode == self._context.get_mode():
            return  # already in the requested mode

        self._context.set_mode(new_mode)
        self._registry.set_mode(new_mode)
        self._build_calculator_grid()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _format_number(value: float) -> str:
        """Format a float for display, omitting the ``.0`` suffix for integers.

        Args:
            value: The numeric value to format.

        Returns:
            A compact string representation of *value*.
        """
        if value == int(value) and not (value != value):  # not NaN
            return str(int(value))
        return str(value)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the Tkinter event loop.

        Blocks until the window is closed by the user.
        """
        self.mainloop()
