"""Tkinter-based GUI interface for the Calculator application.

Provides a windowed calculator that mirrors the REPL's capabilities:
mode switching, operation selection, operand input, result display,
and session history — all through a point-and-click interface.

The GUI is a pure presentation layer; all calculation logic is
delegated to the existing Calculator, OperationRegistry,
CalculatorContext, OperationHistory, and ErrorLogger components.
"""

import tkinter as tk
from tkinter import messagebox
from typing import Any, Optional

from src.core.operations import Operation, OperationRegistry
from src.context import CalculatorContext
from src.support.error_logger import ErrorLogger

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.support.history import OperationHistory


class GUICalculator(tk.Tk):
    """Tkinter GUI front-end for the Calculator application.

    Builds a window with:
    - A mode selector (normal / scientific radio buttons).
    - Dynamically populated operation buttons filtered for the current mode.
    - Operand Entry widgets whose count reflects the selected operation's arity.
    - A result display label.
    - A scrollable history panel.

    All arithmetic is dispatched through :class:`~src.core.operations.OperationRegistry`.
    Mode state is kept in :class:`~src.context.CalculatorContext`.
    History is recorded and read via the injected
    :class:`~src.support.history.OperationHistory` instance.

    Args:
        calculator: A :class:`~src.calculator.Calculator` instance.
        history: An optional :class:`~src.support.history.OperationHistory`
            instance for recording and displaying session history.
        error_logger: An optional :class:`~src.support.error_logger.ErrorLogger`
            instance for persisting error entries.
        context: An optional :class:`~src.context.CalculatorContext` instance
            for persisting mode state.  A fresh context is created when
            ``None`` is supplied.
    """

    def __init__(
        self,
        calculator: Any,
        history: Optional["OperationHistory"] = None,
        error_logger: Optional[ErrorLogger] = None,
        context: Optional[CalculatorContext] = None,
    ) -> None:
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)

        self.calculator = calculator
        self.history = history
        self.error_logger = error_logger
        self._context: CalculatorContext = context if context is not None else CalculatorContext()
        self._registry = OperationRegistry(calculator)
        self._registry.set_mode(self._context.get_mode())

        # Tracks the currently selected operation name (canonical).
        self._selected_operation: Optional[str] = None

        # StringVar used by the mode radio buttons.
        self._mode_var = tk.StringVar(value=self._context.get_mode())

        # Holds Entry widget(s) for operand input; rebuilt when arity changes.
        self._operand_entries: list[tk.Entry] = []

        # Frames that are populated / cleared dynamically.
        self._operation_buttons_frame: Optional[tk.Frame] = None
        self._operand_frame: Optional[tk.Frame] = None

        # History listbox widget reference for updates.
        self._history_listbox: Optional[tk.Listbox] = None

        # Result StringVar so the label updates reactively.
        self._result_var = tk.StringVar(value="")

        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction helpers
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Assemble all UI sections in top-to-bottom order."""
        self._build_mode_selector()
        self._build_operation_buttons()
        self._build_operand_inputs()
        self._build_result_display()

        # Execute button.
        execute_btn = tk.Button(
            self,
            text="Calculate",
            command=self._execute_calculation,
            width=20,
            bg="#4a7c59",
            fg="white",
            font=("Arial", 11, "bold"),
        )
        execute_btn.pack(pady=(4, 8), padx=12)

        self._build_history_panel()

    def _build_mode_selector(self) -> None:
        """Build the mode-selector radio-button row at the top of the window."""
        frame = tk.LabelFrame(self, text="Mode", padx=8, pady=4)
        frame.pack(fill=tk.X, padx=12, pady=(8, 4))

        for mode in ("normal", "scientific"):
            rb = tk.Radiobutton(
                frame,
                text=mode.capitalize(),
                variable=self._mode_var,
                value=mode,
                command=lambda m=mode: self._handle_mode_change(m),
            )
            rb.pack(side=tk.LEFT, padx=6)

    def _build_operation_buttons(self) -> None:
        """Create (or recreate) operation buttons for the current mode.

        Fetches the mode-filtered operation list from the registry and
        renders one button per operation in a wrapping grid layout.
        Destroys any previously rendered button frame first so the method
        can be called repeatedly on mode change.
        """
        if self._operation_buttons_frame is not None:
            self._operation_buttons_frame.destroy()

        frame = tk.LabelFrame(self, text="Operations", padx=8, pady=4)
        frame.pack(fill=tk.X, padx=12, pady=4)
        self._operation_buttons_frame = frame

        operations: list[Operation] = self._registry.get_operations()

        # Lay buttons out in a grid of up to 4 columns.
        columns = 4
        for index, op in enumerate(operations):
            row, col = divmod(index, columns)
            btn = tk.Button(
                frame,
                text=op.display_name,
                width=14,
                command=lambda name=op.name: self._handle_operation_selected(name),
            )
            btn.grid(row=row, column=col, padx=4, pady=3, sticky="ew")

        # Make all columns expand equally.
        for col in range(columns):
            frame.columnconfigure(col, weight=1)

    def _build_operand_inputs(self) -> None:
        """Create the operand-input section.

        Initially renders a single Entry widget (arity 1).  Replaced
        wholesale by :meth:`_handle_operation_selected` when an operation
        is chosen and its arity is known.
        """
        if self._operand_frame is not None:
            self._operand_frame.destroy()

        frame = tk.LabelFrame(self, text="Operands", padx=8, pady=4)
        frame.pack(fill=tk.X, padx=12, pady=4)
        self._operand_frame = frame

        self._operand_entries = []
        arity = 1
        if self._selected_operation is not None:
            op = self._registry.get_operation(self._selected_operation)
            if op is not None:
                arity = op.arity

        for i in range(arity):
            label_text = "Value:" if arity == 1 else f"Operand {i + 1}:"
            lbl = tk.Label(frame, text=label_text, width=10, anchor="w")
            lbl.grid(row=i, column=0, padx=4, pady=3, sticky="w")
            entry = tk.Entry(frame, width=20)
            entry.grid(row=i, column=1, padx=4, pady=3, sticky="ew")
            self._operand_entries.append(entry)

        frame.columnconfigure(1, weight=1)

    def _build_result_display(self) -> None:
        """Build the result display label beneath the operand inputs."""
        frame = tk.LabelFrame(self, text="Result", padx=8, pady=4)
        frame.pack(fill=tk.X, padx=12, pady=4)

        lbl = tk.Label(
            frame,
            textvariable=self._result_var,
            font=("Courier", 13, "bold"),
            anchor="e",
            width=32,
        )
        lbl.pack(fill=tk.X)

    def _build_history_panel(self) -> None:
        """Build a scrollable listbox that shows the session operation history."""
        frame = tk.LabelFrame(self, text="History", padx=8, pady=4)
        frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(4, 12))

        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        listbox = tk.Listbox(
            frame,
            yscrollcommand=scrollbar.set,
            height=6,
            font=("Courier", 10),
            selectmode=tk.SINGLE,
        )
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._history_listbox = listbox
        self._update_history_display()

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _handle_mode_change(self, mode: str) -> None:
        """React to the user selecting a different mode radio button.

        Updates the context and registry, then rebuilds the operation
        buttons so that only mode-appropriate operations are shown.

        Args:
            mode: The newly selected mode string (``"normal"`` or
                ``"scientific"``).
        """
        try:
            self._context.set_mode(mode)
            self._registry.set_mode(mode)
        except ValueError as exc:
            self._show_error(str(exc))
            return

        # The previously selected operation may not be in the new mode;
        # deselect it to avoid stale state.
        self._selected_operation = None
        self._result_var.set("")

        self._build_operation_buttons()
        self._build_operand_inputs()

    def _handle_operation_selected(self, operation_name: str) -> None:
        """React to the user clicking an operation button.

        Stores the selection and rebuilds the operand input section with
        the correct number of Entry widgets for the operation's arity.

        Args:
            operation_name: The canonical operation name (e.g. ``"add"``).
        """
        self._selected_operation = operation_name
        self._result_var.set("")
        self._build_operand_inputs()

    def _execute_calculation(self) -> None:
        """Validate inputs, dispatch the calculation, and update the display.

        Reads values from the operand Entry widgets, calls
        :meth:`~src.core.operations.OperationRegistry.dispatch`, stores the
        result in the result StringVar, records the operation in history, and
        refreshes the history panel.

        Shows an error message via :meth:`_show_error` on any failure.
        """
        if self._selected_operation is None:
            self._show_error("Please select an operation first.")
            return

        # Parse operands from entry widgets.
        operands: list[float] = []
        for i, entry in enumerate(self._operand_entries):
            raw = entry.get().strip()
            if not raw:
                self._show_error(f"Operand {i + 1} is empty. Please enter a number.")
                return
            try:
                operands.append(float(raw))
            except ValueError:
                self._show_error(f"Invalid number for operand {i + 1}: {raw!r}")
                return

        operation = self._selected_operation
        user_input = f"{operation}({', '.join(str(o) for o in operands)})"

        try:
            result = self._registry.dispatch(operation, operands)
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            error_msg = str(exc)
            if self.error_logger is not None:
                self.error_logger.log_error(
                    ErrorLogger.CALCULATION_ERROR, user_input, exc
                )
            self._show_error(error_msg)
            return

        # Format result — strip unnecessary trailing zeros for integers.
        if isinstance(result, float) and result.is_integer():
            result_str = str(int(result))
        else:
            result_str = str(result)

        self._result_var.set(result_str)

        # Record in history.
        if self.history is not None:
            entry = f"{user_input} = {result_str}"
            self.history.record_operation(entry)
            self._update_history_display()

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def _update_history_display(self) -> None:
        """Reload the history listbox from the OperationHistory store.

        Clears the listbox and repopulates it from
        :meth:`~src.support.history.OperationHistory.display_history`.
        Does nothing when no history object was injected.
        """
        if self._history_listbox is None:
            return
        if self.history is None:
            return

        self._history_listbox.delete(0, tk.END)
        entries = self.history.display_history()
        for entry in entries:
            self._history_listbox.insert(tk.END, entry)

        # Scroll to the most recent entry.
        if entries:
            self._history_listbox.see(tk.END)

    def _show_error(self, error_message: str) -> None:
        """Display an error to the user in a modal messagebox.

        Args:
            error_message: A human-readable description of the error.
        """
        messagebox.showerror("Calculator Error", error_message)
