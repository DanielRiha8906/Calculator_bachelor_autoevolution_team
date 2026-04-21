"""Tkinter-based GUI interface for the Calculator.

Provides a windowed interface with a mode panel, an input/output panel for
operand entry and result display, and a scrollable history panel.  Operation
buttons are generated dynamically from the operation registry and rebuilt
whenever the active mode changes.
"""

import tkinter as tk
from tkinter import scrolledtext
from typing import Optional

from src.context import CalculatorContext
from src.core.operations import Operation, OperationRegistry
from src.support.error_logger import ErrorLogger
from src.support.history import OperationHistory


class GUIInterface(tk.Tk):
    """Tkinter GUI for the calculator application.

    Lays out three vertical panels:

    1. **Mode panel** (top): displays the current mode and a "Switch Mode"
       button that toggles between ``"normal"`` and ``"scientific"``.
    2. **Input/Output panel** (middle): two operand ``Entry`` widgets (the
       second is hidden for unary operations), a grid of operation buttons,
       and a read-only result label.
    3. **History panel** (bottom): a ``ScrolledText`` widget showing all
       completed operations in the current session.

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

        # Keep track of the currently selected operation so that the button
        # grid can highlight the active choice.
        self._active_operation: Optional[str] = None

        self._build_mode_panel()
        self._build_io_panel()
        self._build_history_panel()
        self._build_operation_buttons()
        self._refresh_history_display()

    # ------------------------------------------------------------------
    # Panel builders
    # ------------------------------------------------------------------

    def _build_mode_panel(self) -> None:
        """Create the top-level mode indicator and switch button."""
        self._mode_frame = tk.Frame(self, relief=tk.RIDGE, borderwidth=2, padx=8, pady=4)
        self._mode_frame.pack(fill=tk.X, padx=8, pady=(8, 0))

        self._mode_label = tk.Label(
            self._mode_frame,
            text=self._mode_display_text(),
            font=("TkDefaultFont", 10, "bold"),
        )
        self._mode_label.pack(side=tk.LEFT)

        switch_btn = tk.Button(
            self._mode_frame,
            text="Switch Mode",
            command=self._on_switch_mode,
        )
        switch_btn.pack(side=tk.RIGHT)

    def _build_io_panel(self) -> None:
        """Create the operand entry fields, result label, and button container."""
        io_frame = tk.Frame(self, relief=tk.RIDGE, borderwidth=2, padx=8, pady=8)
        io_frame.pack(fill=tk.X, padx=8, pady=4)

        # Operand 1
        self._op1_row = tk.Frame(io_frame)
        self._op1_row.pack(fill=tk.X, pady=2)
        tk.Label(self._op1_row, text="Operand 1:", width=10, anchor=tk.W).pack(side=tk.LEFT)
        self._operand1_var = tk.StringVar()
        self._operand1_entry = tk.Entry(self._op1_row, textvariable=self._operand1_var, width=20)
        self._operand1_entry.pack(side=tk.LEFT, padx=4)

        # Operand 2 (shown/hidden based on operation arity)
        self._op2_row = tk.Frame(io_frame)
        self._op2_row.pack(fill=tk.X, pady=2)
        tk.Label(self._op2_row, text="Operand 2:", width=10, anchor=tk.W).pack(side=tk.LEFT)
        self._operand2_var = tk.StringVar()
        self._operand2_entry = tk.Entry(self._op2_row, textvariable=self._operand2_var, width=20)
        self._operand2_entry.pack(side=tk.LEFT, padx=4)
        # Hidden by default; revealed when a binary operation is selected.
        self._op2_row.pack_forget()

        # Result display
        result_row = tk.Frame(io_frame)
        result_row.pack(fill=tk.X, pady=(6, 2))
        tk.Label(result_row, text="Result:", width=10, anchor=tk.W).pack(side=tk.LEFT)
        self._result_var = tk.StringVar(value="—")
        tk.Label(
            result_row,
            textvariable=self._result_var,
            anchor=tk.W,
            width=30,
            relief=tk.SUNKEN,
        ).pack(side=tk.LEFT, padx=4)

        # Container for dynamically generated operation buttons
        self._buttons_frame = tk.Frame(io_frame)
        self._buttons_frame.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

    def _build_history_panel(self) -> None:
        """Create the scrollable history text area."""
        hist_frame = tk.Frame(self, relief=tk.RIDGE, borderwidth=2, padx=8, pady=4)
        hist_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        tk.Label(hist_frame, text="History", font=("TkDefaultFont", 9, "bold")).pack(anchor=tk.W)
        self._history_text = scrolledtext.ScrolledText(
            hist_frame,
            height=8,
            state=tk.DISABLED,
            font=("TkFixedFont", 9),
        )
        self._history_text.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------
    # Operation button management
    # ------------------------------------------------------------------

    def _build_operation_buttons(self) -> None:
        """Populate the buttons frame with buttons for the current mode.

        Clears any previously rendered buttons first, then lays out new
        buttons in a grid of up to 3 columns, one button per available
        operation.
        """
        for widget in self._buttons_frame.winfo_children():
            widget.destroy()

        operations: list[Operation] = self._registry.get_operations()
        columns = 3

        for index, op in enumerate(operations):
            row, col = divmod(index, columns)
            btn = tk.Button(
                self._buttons_frame,
                text=op.display_name,
                width=16,
                command=lambda name=op.name, arity=op.arity: self._on_operation(name, arity),
            )
            btn.grid(row=row, column=col, padx=4, pady=3, sticky=tk.EW)

        # Make all columns expand equally so buttons fill the available width.
        for col in range(columns):
            self._buttons_frame.columnconfigure(col, weight=1)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_switch_mode(self) -> None:
        """Toggle between normal and scientific mode.

        Updates both the ``CalculatorContext`` and the ``OperationRegistry``
        so they stay in sync, then rebuilds the operation buttons and clears
        the operand fields.
        """
        current = self._context.get_mode()
        new_mode = "scientific" if current == "normal" else "normal"
        self._context.set_mode(new_mode)
        self._registry.set_mode(new_mode)

        self._mode_label.config(text=self._mode_display_text())
        self._active_operation = None
        self._operand1_var.set("")
        self._operand2_var.set("")
        self._result_var.set("—")
        self._op2_row.pack_forget()
        self._build_operation_buttons()

    def _on_operation(self, operation_name: str, arity: int) -> None:
        """Handle an operation button press.

        Validates the operand fields for the given *arity*, dispatches the
        operation, records the result in history, and updates the result
        display.  Any calculation or validation error is shown in the result
        area and logged via the ``ErrorLogger``.

        Args:
            operation_name: The canonical operation name (e.g. ``"add"``).
            arity: The number of operands required (1 or 2).
        """
        # Show or hide the second operand field based on arity.
        if arity == 2:
            self._op2_row.pack(fill=tk.X, pady=2, after=self._op1_row)
        else:
            self._op2_row.pack_forget()

        self._active_operation = operation_name

        # Validate operand 1
        raw1 = self._operand1_var.get().strip()
        operand1 = self._parse_float(raw1)
        if operand1 is None:
            self._show_error(f"Invalid operand 1: {raw1!r} is not a number.")
            self._error_logger.log_error(
                ErrorLogger.INVALID_INPUT,
                raw1,
                ValueError(f"Cannot parse {raw1!r} as float"),
            )
            return

        operands: list[float] = [operand1]

        if arity == 2:
            raw2 = self._operand2_var.get().strip()
            operand2 = self._parse_float(raw2)
            if operand2 is None:
                self._show_error(f"Invalid operand 2: {raw2!r} is not a number.")
                self._error_logger.log_error(
                    ErrorLogger.INVALID_INPUT,
                    raw2,
                    ValueError(f"Cannot parse {raw2!r} as float"),
                )
                return
            operands.append(operand2)

        # Dispatch and handle calculation errors
        try:
            result: float = self._registry.dispatch(operation_name, operands)
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            self._show_error(str(exc))
            operand_str = ", ".join(str(o) for o in operands)
            self._error_logger.log_error(
                ErrorLogger.CALCULATION_ERROR,
                f"{operation_name}({operand_str})",
                exc,
            )
            return

        # Format and display result
        operand_str = ", ".join(str(o) for o in operands)
        result_text = f"{operation_name}({operand_str}) = {result}"
        self._result_var.set(result_text)

        # Persist to history and refresh the history panel
        self._history.record_operation(result_text)
        self._refresh_history_display()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _mode_display_text(self) -> str:
        """Return a human-readable mode label for display.

        Returns:
            A string such as ``"Mode: normal"`` reflecting the current mode.
        """
        return f"Mode: {self._context.get_mode()}"

    def _parse_float(self, raw: str) -> Optional[float]:
        """Attempt to parse *raw* as a float.

        Args:
            raw: The raw string to parse.

        Returns:
            The parsed ``float`` value, or ``None`` if parsing fails.
        """
        try:
            return float(raw)
        except ValueError:
            return None

    def _show_error(self, message: str) -> None:
        """Display an error message in the result area.

        Args:
            message: The error message to display.
        """
        self._result_var.set(f"Error: {message}")

    def _refresh_history_display(self) -> None:
        """Reload the history file and update the history text widget."""
        entries: list[str] = self._history.display_history()
        self._history_text.config(state=tk.NORMAL)
        self._history_text.delete("1.0", tk.END)
        if entries:
            self._history_text.insert(tk.END, "\n".join(entries))
        self._history_text.config(state=tk.DISABLED)
        # Scroll to the bottom so the latest entry is visible.
        self._history_text.see(tk.END)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the Tkinter event loop.

        Blocks until the window is closed by the user.
        """
        self.mainloop()
