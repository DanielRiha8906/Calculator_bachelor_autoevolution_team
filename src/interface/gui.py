"""Tkinter-based GUI interface for the Calculator.

Provides a modern iOS-inspired windowed interface with a result display,
a mode toggle panel, and dynamically generated operation buttons.  Operation
buttons are rebuilt whenever the active mode changes.
"""

import tkinter as tk
from tkinter import simpledialog
from typing import Optional

from src.context import CalculatorContext
from src.core.operations import Operation, OperationRegistry
from src.support.error_logger import ErrorLogger
from src.support.history import OperationHistory

# ---------------------------------------------------------------------------
# Symbol and colour mappings
# ---------------------------------------------------------------------------

SYMBOL_MAP: dict[str, str] = {
    "add": "+",
    "subtract": "−",       # U+2212 MINUS SIGN
    "multiply": "×",
    "divide": "÷",
    "square": "x²",
    "cube": "x³",
    "square_root": "√",
    "cube_root": "∛",
    "power": "xʸ",
    "factorial": "n!",
    "natural_logarithm": "ln",
    "logarithm": "log",
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "asin": "asin",
    "acos": "acos",
    "atan": "atan",
}

OPERATOR_COLORS: dict[str, str] = {
    "add": "#FF9500",
    "subtract": "#FF9500",
    "multiply": "#FF9500",
    "divide": "#FF9500",
}

UTILITY_COLOR: str = "#A5A5A5"
DEFAULT_COLOR: str = "#333333"


class GUIInterface(tk.Tk):
    """Tkinter GUI for the calculator application.

    Lays out three vertical sections:

    1. **Result display** (top): a large right-aligned label on a black
       background showing the current result or ``"0"``.
    2. **Mode toggle** (middle): two flat buttons to switch between
       ``"normal"`` and ``"scientific"`` mode.
    3. **Button grid** (bottom): dynamically generated operation buttons
       coloured according to ``OPERATOR_COLORS`` / ``DEFAULT_COLOR``.

    Operand values are collected via modal dialogs when an operation is
    invoked, so no persistent Entry widgets are required.

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
        self.configure(bg="#000000")

        # Keep track of the currently selected operation.
        self._active_operation: Optional[str] = None

        self._build_result_display()
        self._build_mode_toggle()
        self._build_operation_buttons()

    # ------------------------------------------------------------------
    # Panel builders
    # ------------------------------------------------------------------

    def _build_result_display(self) -> None:
        """Create the large result label at the top of the window."""
        result_frame = tk.Frame(self, bg="#000000")
        result_frame.pack(fill=tk.X, padx=8, pady=(16, 8))

        self._result_var = tk.StringVar(value="0")
        self._result_label = tk.Label(
            result_frame,
            textvariable=self._result_var,
            bg="#000000",
            fg="#FFFFFF",
            font=("TkDefaultFont", 28, "bold"),
            anchor=tk.E,
            justify=tk.RIGHT,
        )
        self._result_label.pack(fill=tk.X, padx=8, pady=(8, 8))

    def _build_mode_toggle(self) -> None:
        """Create the flat mode-toggle buttons above the operation grid."""
        self._mode_frame = tk.Frame(self, bg="#000000")
        self._mode_frame.pack(fill=tk.X, padx=8, pady=(0, 4))

        self._normal_btn = tk.Button(
            self._mode_frame,
            text="Normal",
            relief=tk.FLAT,
            borderwidth=0,
            bg="#333333",
            fg="#FFFFFF",
            activebackground="#FF9500",
            activeforeground="#FFFFFF",
            font=("TkDefaultFont", 12),
            padx=12,
            pady=6,
            command=lambda: self._on_select_mode("normal"),
        )
        self._normal_btn.pack(side=tk.LEFT, padx=(0, 4))

        self._scientific_btn = tk.Button(
            self._mode_frame,
            text="Scientific",
            relief=tk.FLAT,
            borderwidth=0,
            bg="#333333",
            fg="#FFFFFF",
            activebackground="#FF9500",
            activeforeground="#FFFFFF",
            font=("TkDefaultFont", 12),
            padx=12,
            pady=6,
            command=lambda: self._on_select_mode("scientific"),
        )
        self._scientific_btn.pack(side=tk.LEFT)

        # Highlight the button that matches the current mode.
        self._update_mode_button_highlights()

    def _update_mode_button_highlights(self) -> None:
        """Update toggle button backgrounds to reflect the active mode."""
        current = self._context.get_mode()
        self._normal_btn.config(
            bg="#FF9500" if current == "normal" else "#333333"
        )
        self._scientific_btn.config(
            bg="#FF9500" if current == "scientific" else "#333333"
        )

    def _build_operation_buttons(self) -> None:
        """Populate the buttons frame with buttons for the current mode.

        Clears any previously rendered buttons first, then lays out new
        buttons in a grid of up to 4 columns, one button per available
        operation.  Button colours are determined by ``OPERATOR_COLORS`` and
        ``DEFAULT_COLOR``.
        """
        # Create the frame on first call; clear children on subsequent calls.
        if not hasattr(self, "_buttons_frame"):
            self._buttons_frame = tk.Frame(self, bg="#000000")
            self._buttons_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(4, 8))
        else:
            for widget in self._buttons_frame.winfo_children():
                widget.destroy()

        operations: list[Operation] = self._registry.get_operations()
        columns = 4

        for index, op in enumerate(operations):
            row, col = divmod(index, columns)
            label = SYMBOL_MAP.get(op.name, op.display_name)
            bg_color = OPERATOR_COLORS.get(op.name, DEFAULT_COLOR)
            btn = tk.Button(
                self._buttons_frame,
                text=label,
                relief=tk.FLAT,
                borderwidth=0,
                bg=bg_color,
                fg="#FFFFFF",
                activebackground="#FFFFFF",
                activeforeground="#000000",
                font=("TkDefaultFont", 14),
                padx=8,
                pady=8,
                width=6,
                command=lambda name=op.name, arity=op.arity: self._on_operation(name, arity),
            )
            btn.grid(row=row, column=col, padx=3, pady=3, sticky=tk.EW)

        # Make all columns expand equally so buttons fill the available width.
        for col in range(columns):
            self._buttons_frame.columnconfigure(col, weight=1)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_select_mode(self, mode: str) -> None:
        """Switch to the given *mode* and refresh the UI.

        Args:
            mode: Either ``"normal"`` or ``"scientific"``.
        """
        self._context.set_mode(mode)
        self._registry.set_mode(mode)

        self._active_operation = None
        self._result_var.set("0")
        self._update_mode_button_highlights()
        self._build_operation_buttons()

    def _on_switch_mode(self) -> None:
        """Toggle between normal and scientific mode.

        Updates both the ``CalculatorContext`` and the ``OperationRegistry``
        so they stay in sync, then rebuilds the operation buttons and resets
        the result display.
        """
        current = self._context.get_mode()
        new_mode = "scientific" if current == "normal" else "normal"
        self._on_select_mode(new_mode)

    def _on_operation(self, operation_name: str, arity: int) -> None:
        """Handle an operation button press.

        Prompts the user for operand values via modal dialogs, dispatches the
        operation, records the result in history, and updates the result
        display.  Any calculation error is shown in the result label and
        logged via the ``ErrorLogger``.

        Args:
            operation_name: The canonical operation name (e.g. ``"add"``).
            arity: The number of operands required (1 or 2).
        """
        self._active_operation = operation_name

        operand1 = simpledialog.askfloat(
            "Operand",
            "Enter operand 1:",
            parent=self,
        )
        if operand1 is None:
            # User cancelled the dialog.
            return

        operands: list[float] = [operand1]

        if arity == 2:
            operand2 = simpledialog.askfloat(
                "Operand",
                "Enter operand 2:",
                parent=self,
            )
            if operand2 is None:
                # User cancelled the dialog.
                return
            operands.append(operand2)

        # Dispatch and handle calculation errors.
        try:
            result: float = self._registry.dispatch(operation_name, operands)
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            self._result_var.set(f"Error: {exc}")
            operand_str = ", ".join(str(o) for o in operands)
            self._error_logger.log_error(
                ErrorLogger.CALCULATION_ERROR,
                f"{operation_name}({operand_str})",
                exc,
            )
            return

        # Format and display result.
        operand_str = ", ".join(str(o) for o in operands)
        result_text = f"{operation_name}({operand_str}) = {result}"
        self._result_var.set(str(result))

        # Persist to history.
        self._history.record_operation(result_text)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _mode_display_text(self) -> str:
        """Return a human-readable mode label for display.

        Returns:
            A string such as ``"Mode: normal"`` reflecting the current mode.
        """
        return f"Mode: {self._context.get_mode()}"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the Tkinter event loop.

        Blocks until the window is closed by the user.
        """
        self.mainloop()
