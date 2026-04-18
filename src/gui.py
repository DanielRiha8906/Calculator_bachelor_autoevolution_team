"""GUI layer — tkinter-based calculator interface.

Provides a graphical front-end for the calculator application.  All arithmetic
is delegated to the existing :class:`~src.calculator.Calculator` engine via
:func:`~src.input_loop.dispatch`.  Mode management uses
:func:`~src.mode.get_operations_for_mode` and operation metadata comes from
:data:`~src.input_loop.OPERATIONS`.

The module exposes two public symbols:

* :class:`OperandInputWidget` — a labelled entry field that parses its value
  as a float.
* :class:`CalculatorGUI` — the main application window.
"""

from __future__ import annotations

import tkinter as tk
from typing import Optional

from .calculator import Calculator
from .error_logger import (
    CALCULATION_ERROR,
    INVALID_INPUT,
    ErrorLogger,
)
from .history import OperationHistory
from .input_loop import OPERATIONS, dispatch
from .mode import Mode, get_operations_for_mode


# ---------------------------------------------------------------------------
# Helper widget
# ---------------------------------------------------------------------------


class OperandInputWidget:
    """A labelled entry field for a single numeric operand.

    Wraps a :class:`tk.Label` and a :class:`tk.Entry` into a single logical
    unit.  The widgets are laid out in the parent frame using ``grid``.

    Args:
        parent: The parent tkinter widget.
        label_text: Text to display in the label beside the entry.
        row: Grid row to place both widgets in.
    """

    def __init__(self, parent: tk.Widget, label_text: str, row: int) -> None:
        self._label = tk.Label(parent, text=label_text)
        self._label.grid(row=row, column=0, padx=6, pady=4, sticky="e")

        self._entry = tk.Entry(parent, width=20)
        self._entry.grid(row=row, column=1, padx=6, pady=4, sticky="w")

    def get_value(self) -> float:
        """Parse the entry text as a float.

        Returns:
            The numeric value entered by the user.

        Raises:
            ValueError: If the entry text cannot be converted to a float.
        """
        raw = self._entry.get().strip()
        return float(raw)

    def clear(self) -> None:
        """Clear the entry field."""
        self._entry.delete(0, tk.END)

    def set_visible(self, visible: bool) -> None:
        """Show or hide both the label and the entry widget.

        Args:
            visible: When ``True`` the widgets are shown; when ``False`` they
                are hidden using ``grid_remove``.
        """
        if visible:
            self._label.grid()
            self._entry.grid()
        else:
            self._label.grid_remove()
            self._entry.grid_remove()


# ---------------------------------------------------------------------------
# Main application class
# ---------------------------------------------------------------------------


class CalculatorGUI:
    """Tkinter-based graphical calculator application.

    Integrates with the existing :class:`~src.calculator.Calculator` and
    :class:`~src.history.OperationHistory` without reimplementing any
    arithmetic logic.  Operations are executed via
    :func:`~src.input_loop.dispatch`.

    Attributes:
        _calc: The shared :class:`~src.calculator.Calculator` instance.
        _history: Session history recorder.
        _error_logger: Error event recorder.
        _current_mode: The currently active :class:`~src.mode.Mode`.
        _selected_operation: The key of the currently selected operation, or
            ``None`` when no operation has been chosen yet.
        _root: The root :class:`tk.Tk` window.
    """

    def __init__(self) -> None:
        """Initialise the root window and all frames and widgets."""
        self._calc: Calculator = Calculator()
        self._history: OperationHistory = OperationHistory()
        self._error_logger: ErrorLogger = ErrorLogger()
        self._current_mode: Mode = Mode.NORMAL
        self._selected_operation: Optional[str] = None

        self._root = tk.Tk()
        self._root.title("Calculator")
        self._root.resizable(False, False)

        # Operation buttons are stored so they can be rebuilt on mode change.
        self._operation_buttons: list[tk.Button] = []

        # OperandInputWidget instances (up to two).
        self._operand_widgets: list[OperandInputWidget] = []

        # Result and error label variable.
        self._result_var = tk.StringVar(value="")
        self._error_var = tk.StringVar(value="")

        # Build UI sections top to bottom.
        self._create_mode_selector_frame()
        self._create_operation_selector_frame()
        self._create_input_frame()
        self._create_result_frame()
        self._create_history_frame()

        # Populate operation buttons for the initial mode.
        self._update_operation_buttons()

    # ------------------------------------------------------------------
    # Frame builders
    # ------------------------------------------------------------------

    def _create_mode_selector_frame(self) -> None:
        """Create the Normal / Scientific mode toggle buttons."""
        frame = tk.LabelFrame(self._root, text="Mode", padx=8, pady=6)
        frame.pack(fill="x", padx=10, pady=(10, 4))

        self._mode_var = tk.StringVar(value=self._current_mode.value)

        for mode in Mode:
            btn = tk.Radiobutton(
                frame,
                text=mode.value.capitalize(),
                variable=self._mode_var,
                value=mode.value,
                command=self._on_mode_changed_from_radio,
            )
            btn.pack(side="left", padx=8)

    def _create_operation_selector_frame(self) -> None:
        """Create the scrollable frame that holds operation buttons."""
        self._ops_outer_frame = tk.LabelFrame(
            self._root, text="Operation", padx=8, pady=6
        )
        self._ops_outer_frame.pack(fill="x", padx=10, pady=4)

        # Inner frame whose children are the actual buttons.
        self._ops_inner_frame = tk.Frame(self._ops_outer_frame)
        self._ops_inner_frame.pack()

    def _create_input_frame(self) -> None:
        """Create the operand entry fields (up to two)."""
        frame = tk.LabelFrame(self._root, text="Operands", padx=8, pady=6)
        frame.pack(fill="x", padx=10, pady=4)

        # Pre-create two operand widgets; visibility is toggled by
        # _on_operation_selected based on the selected operation's arity.
        labels = ["Operand 1:", "Operand 2:"]
        for i, label in enumerate(labels):
            widget = OperandInputWidget(frame, label, row=i)
            widget.set_visible(False)
            self._operand_widgets.append(widget)

        # Calculate button lives in the input frame.
        self._calc_button = tk.Button(
            frame,
            text="Calculate",
            command=self._perform_calculation,
            state="disabled",
            width=14,
        )
        self._calc_button.grid(
            row=len(labels), column=0, columnspan=2, pady=(8, 2)
        )

    def _create_result_frame(self) -> None:
        """Create the result display label."""
        frame = tk.LabelFrame(self._root, text="Result", padx=8, pady=6)
        frame.pack(fill="x", padx=10, pady=4)

        result_label = tk.Label(
            frame,
            textvariable=self._result_var,
            font=("TkFixedFont", 13, "bold"),
            anchor="center",
            width=35,
        )
        result_label.pack()

        error_label = tk.Label(
            frame,
            textvariable=self._error_var,
            fg="red",
            anchor="center",
            width=35,
            wraplength=300,
        )
        error_label.pack()

    def _create_history_frame(self) -> None:
        """Create the scrollable history listbox."""
        frame = tk.LabelFrame(self._root, text="History", padx=8, pady=6)
        frame.pack(fill="both", expand=True, padx=10, pady=(4, 10))

        scrollbar = tk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self._history_listbox = tk.Listbox(
            frame,
            height=8,
            width=50,
            yscrollcommand=scrollbar.set,
            selectmode="browse",
        )
        self._history_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self._history_listbox.yview)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_mode_changed_from_radio(self) -> None:
        """Read the radio-button variable and delegate to _on_mode_changed."""
        mode_value = self._mode_var.get()
        new_mode = Mode(mode_value)
        self._on_mode_changed(new_mode)

    def _on_mode_changed(self, new_mode: Mode) -> None:
        """Switch to *new_mode* and rebuild the operation buttons.

        Args:
            new_mode: The :class:`~src.mode.Mode` to switch to.
        """
        self._current_mode = new_mode
        self._selected_operation = None
        self._clear_operand_inputs()
        self._result_var.set("")
        self._error_var.set("")
        self._calc_button.config(state="disabled")
        # Hide all operand widgets until a new operation is selected.
        for widget in self._operand_widgets:
            widget.set_visible(False)
        self._update_operation_buttons()

    def _on_operation_selected(self, operation: str) -> None:
        """Update UI when the user selects an operation.

        Shows the correct number of input fields (1 for unary, 2 for binary)
        and enables the Calculate button.

        Args:
            operation: A key from :data:`~src.input_loop.OPERATIONS`.
        """
        self._selected_operation = operation
        self._clear_operand_inputs()
        self._result_var.set("")
        self._error_var.set("")

        _, operand_count = OPERATIONS[operation]

        # Show the appropriate number of operand input fields.
        if operand_count >= 1:
            self._operand_widgets[0].set_visible(True)
        else:
            self._operand_widgets[0].set_visible(False)

        if operand_count >= 2:
            self._operand_widgets[1].set_visible(True)
        else:
            self._operand_widgets[1].set_visible(False)

        self._calc_button.config(state="normal")

    # ------------------------------------------------------------------
    # Calculation logic
    # ------------------------------------------------------------------

    def _perform_calculation(self) -> None:
        """Validate inputs, call dispatch(), display result, record history.

        Reads operand values from the visible entry widgets.  Shows an error
        message in the GUI (and logs it) on invalid input or a calculation
        error.  On success the result is displayed and appended to the
        session history.
        """
        if self._selected_operation is None:
            self._show_error("No operation selected.")
            return

        operation = self._selected_operation
        _, operand_count = OPERATIONS[operation]

        # Collect operands from the visible widgets.
        operands: list[float] = []
        for i in range(operand_count):
            try:
                value = self._operand_widgets[i].get_value()
                operands.append(value)
            except ValueError:
                label = f"Operand {i + 1}" if operand_count > 1 else "Operand"
                error_msg = f"Invalid input: {label} must be a number."
                self._error_logger.log_error(
                    INVALID_INPUT,
                    error_msg,
                    {"operation": operation, "operand_index": i},
                )
                self._show_error(error_msg)
                return

        # Dispatch to the Calculator engine.
        try:
            result = dispatch(operation, operands, self._calc)
        except ValueError as exc:
            error_msg = str(exc)
            self._error_logger.log_error(
                CALCULATION_ERROR,
                error_msg,
                {"operation": operation, "operands": operands, "error": error_msg},
            )
            self._show_error(f"Error: {error_msg}")
            return

        # Success — display result and record history.
        self._result_var.set(str(result))
        self._error_var.set("")
        self._history.record_operation(operation, operands, result)
        self._refresh_history_display()

    # ------------------------------------------------------------------
    # UI update helpers
    # ------------------------------------------------------------------

    def _update_operation_buttons(self) -> None:
        """Rebuild the operation button grid for the current mode.

        Destroys all existing buttons and creates new ones for the
        operations permitted by :attr:`_current_mode`.
        """
        # Destroy existing buttons.
        for btn in self._operation_buttons:
            btn.destroy()
        self._operation_buttons.clear()

        allowed_keys = get_operations_for_mode(self._current_mode)

        # Preserve OPERATIONS order, filter to allowed keys, skip meta-commands.
        ordered_ops = [
            key for key in OPERATIONS
            if key in allowed_keys and OPERATIONS[key][1] > 0
        ]

        # Lay out buttons in a grid with up to 3 columns.
        columns = 3
        for idx, op_key in enumerate(ordered_ops):
            label_text, _ = OPERATIONS[op_key]
            row, col = divmod(idx, columns)
            btn = tk.Button(
                self._ops_inner_frame,
                text=label_text,
                width=22,
                command=lambda k=op_key: self._on_operation_selected(k),
            )
            btn.grid(row=row, column=col, padx=4, pady=3, sticky="ew")
            self._operation_buttons.append(btn)

    def _refresh_history_display(self) -> None:
        """Repopulate the history listbox from the current session history."""
        self._history_listbox.delete(0, tk.END)
        for entry in self._history.get_history():
            self._history_listbox.insert(tk.END, entry)
        # Auto-scroll to the latest entry.
        if self._history_listbox.size() > 0:
            self._history_listbox.see(tk.END)

    def _clear_operand_inputs(self) -> None:
        """Reset all operand entry fields to empty."""
        for widget in self._operand_widgets:
            widget.clear()

    def _show_error(self, message: str) -> None:
        """Display *message* in the error label and clear the result label.

        Args:
            message: Human-readable error description to display in the GUI.
        """
        self._result_var.set("")
        self._error_var.set(message)

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the tkinter main event loop.

        Blocks until the user closes the window.
        """
        self._root.mainloop()
