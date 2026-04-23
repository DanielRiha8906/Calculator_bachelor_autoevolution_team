"""Tkinter-based GUI for the calculator application.

This module provides :class:`CalculatorGUI`, a fully self-contained graphical
interface that wires together :class:`~calculator.Calculator`,
:class:`~operations.OperationRegistry`, :class:`~mode_manager.ModeManager`,
:func:`~validation.validate_operand`, and :class:`~session_history.SessionHistory`.

It intentionally avoids importing ``InputHandler``, ``OperationHistory``, or
``CalculatorWorkflow`` — those are CLI/workflow concerns that do not belong in
the GUI layer.
"""

import tkinter as tk
from tkinter import scrolledtext

from .calculator import Calculator
from .mode_manager import ModeManager
from .operations import OperationRegistry
from .session_history import SessionHistory
from .validation import OperandValidationError, validate_operand


class CalculatorGUI:
    """Graphical calculator interface built with tkinter.

    The GUI presents an operation list, operand input fields, an execute
    button, a result display, and a scrollable history pane.  It supports
    Normal and Scientific modes via :class:`~mode_manager.ModeManager`.

    Args:
        root: The top-level :class:`tk.Tk` window.
        history: A :class:`~session_history.SessionHistory` instance used to
            record and display past calculations.

    Example::

        import tkinter as tk
        from src.session_history import SessionHistory
        from src.gui import CalculatorGUI

        root = tk.Tk()
        history = SessionHistory()
        gui = CalculatorGUI(root, history)
        gui.run()
    """

    def __init__(self, root: tk.Tk, history: SessionHistory) -> None:
        """Initialise the GUI, engine components, and build all widgets.

        Args:
            root: The top-level Tk window.
            history: Session history instance for recording operations.
        """
        self.root: tk.Tk = root
        self.root.title("Calculator")

        self._history: SessionHistory = history
        self._calc: Calculator = Calculator()
        self._registry: OperationRegistry = OperationRegistry(self._calc)
        self._mode_manager: ModeManager = ModeManager()

        # Operand entry widgets are created dynamically based on arity.
        self._operand_entries: list[tk.Entry] = []
        self._operand_labels: list[tk.Label] = []

        self._build_widgets()
        self._populate_operations()

    # ------------------------------------------------------------------
    # Widget construction
    # ------------------------------------------------------------------

    def _build_widgets(self) -> None:
        """Create and arrange all widgets in the root window."""
        self.root.columnconfigure(0, weight=1)

        # ---- Header frame ----
        header_frame = tk.Frame(self.root, pady=6)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.columnconfigure(0, weight=1)

        tk.Label(
            header_frame,
            text="Calculator",
            font=("Helvetica", 16, "bold"),
        ).grid(row=0, column=0)

        # ---- Mode row ----
        mode_frame = tk.Frame(self.root, pady=4)
        mode_frame.grid(row=1, column=0, sticky="ew", padx=10)
        mode_frame.columnconfigure(1, weight=1)

        tk.Label(mode_frame, text="Mode:").grid(row=0, column=0, sticky="w")
        self._mode_label = tk.Label(
            mode_frame,
            text=self._mode_manager.get_mode_display_name(),
            width=12,
            anchor="w",
        )
        self._mode_label.grid(row=0, column=1, sticky="w", padx=(4, 0))

        self._mode_button = tk.Button(
            mode_frame,
            text="Switch Mode",
            command=self._on_mode_switch,
        )
        self._mode_button.grid(row=0, column=2, sticky="e")

        # ---- Operation listbox with scrollbar ----
        ops_frame = tk.LabelFrame(self.root, text="Operations", padx=6, pady=6)
        ops_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(4, 0))
        ops_frame.columnconfigure(0, weight=1)

        ops_scrollbar = tk.Scrollbar(ops_frame, orient=tk.VERTICAL)
        self._ops_listbox = tk.Listbox(
            ops_frame,
            height=8,
            yscrollcommand=ops_scrollbar.set,
            exportselection=False,
        )
        ops_scrollbar.config(command=self._ops_listbox.yview)
        self._ops_listbox.grid(row=0, column=0, sticky="ew")
        ops_scrollbar.grid(row=0, column=1, sticky="ns")
        self._ops_listbox.bind("<<ListboxSelect>>", self._on_operation_selected)

        # ---- Operand inputs frame ----
        self._inputs_frame = tk.LabelFrame(
            self.root, text="Inputs", padx=6, pady=6
        )
        self._inputs_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(4, 0))
        self._inputs_frame.columnconfigure(1, weight=1)

        # ---- Execute button ----
        self._execute_button = tk.Button(
            self.root,
            text="Calculate",
            command=self._execute_operation,
        )
        self._execute_button.grid(row=4, column=0, pady=6, padx=10, sticky="ew")

        # ---- Result display ----
        result_frame = tk.LabelFrame(self.root, text="Result", padx=6, pady=6)
        result_frame.grid(row=5, column=0, sticky="ew", padx=10, pady=(0, 4))
        result_frame.columnconfigure(0, weight=1)

        self._result_label = tk.Label(
            result_frame,
            text="",
            font=("Helvetica", 12),
            anchor="w",
        )
        self._result_label.grid(row=0, column=0, sticky="ew")

        # ---- Error message label (hidden until needed) ----
        self._error_label = tk.Label(
            self.root,
            text="",
            fg="red",
            wraplength=380,
            justify="left",
        )
        self._error_label.grid(row=6, column=0, sticky="ew", padx=10)
        self._error_label.grid_remove()

        # ---- History pane ----
        history_frame = tk.LabelFrame(
            self.root, text="History", padx=6, pady=6
        )
        history_frame.grid(row=7, column=0, sticky="ew", padx=10, pady=(0, 4))
        history_frame.columnconfigure(0, weight=1)

        self._history_text = scrolledtext.ScrolledText(
            history_frame,
            height=8,
            state=tk.DISABLED,
            wrap=tk.WORD,
        )
        self._history_text.grid(row=0, column=0, sticky="ew")

        self._clear_history_button = tk.Button(
            history_frame,
            text="Clear History",
            command=self._on_clear_history,
        )
        self._clear_history_button.grid(row=1, column=0, pady=(4, 0))

    # ------------------------------------------------------------------
    # Operations list management
    # ------------------------------------------------------------------

    def _populate_operations(self) -> None:
        """Refresh the operations listbox to reflect the current mode."""
        self._ops_listbox.delete(0, tk.END)
        available = self._registry.get_available_operations(self._mode_manager)
        self._ops_keys: list[str] = []
        for key, description in available.items():
            self._ops_listbox.insert(tk.END, f"{key}  —  {description}")
            self._ops_keys.append(key)

        # Reset operand fields when operations list changes.
        self._rebuild_operand_inputs(arity=0)

    def _on_operation_selected(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        """Handle a listbox selection change; rebuild operand fields for arity.

        Args:
            event: The tkinter virtual event (not used directly).
        """
        selection = self._ops_listbox.curselection()
        if not selection:
            return

        key = self._ops_keys[selection[0]]
        _method, arity, _description = self._registry.get_operation(key)
        self._rebuild_operand_inputs(arity)
        self._clear_error()

    def _rebuild_operand_inputs(self, arity: int) -> None:
        """Recreate operand label/entry pairs to match the required arity.

        Args:
            arity: Number of operand input fields to create (0 clears all).
        """
        # Remove existing widgets.
        for widget in self._inputs_frame.winfo_children():
            widget.destroy()
        self._operand_entries = []
        self._operand_labels = []

        if arity == 0:
            tk.Label(
                self._inputs_frame, text="Select an operation above.", fg="grey"
            ).grid(row=0, column=0, columnspan=2, sticky="w")
            return

        labels = (
            ["Value:"]
            if arity == 1
            else ["First operand:", "Second operand:"]
        )
        for idx, label_text in enumerate(labels[:arity]):
            lbl = tk.Label(self._inputs_frame, text=label_text, anchor="w")
            lbl.grid(row=idx, column=0, sticky="w", pady=2)
            entry = tk.Entry(self._inputs_frame)
            entry.grid(row=idx, column=1, sticky="ew", padx=(4, 0), pady=2)
            self._operand_labels.append(lbl)
            self._operand_entries.append(entry)

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def _execute_operation(self) -> None:
        """Read operands, run the selected operation, and update the display.

        Validates inputs using :func:`~validation.validate_operand`, calls the
        operation method from the registry, and records the result in
        :class:`~session_history.SessionHistory`.  Any error is shown via
        :meth:`_display_error` without interrupting the event loop.
        """
        self._clear_error()
        selection = self._ops_listbox.curselection()
        if not selection:
            self._display_error("Please select an operation.")
            return

        key = self._ops_keys[selection[0]]
        method, arity, description = self._registry.get_operation(key)

        # Validate and parse operands.
        operands: list[float] = []
        for idx, entry in enumerate(self._operand_entries[:arity]):
            raw = entry.get().strip()
            try:
                value: float = validate_operand(raw)
            except OperandValidationError as exc:
                self._display_error(str(exc))
                return

            # Factorial expects an integer operand.
            if key == "factorial":
                if value != int(value):
                    self._display_error(
                        "Factorial requires a non-negative integer."
                    )
                    return
                operands.append(int(value))
            else:
                operands.append(value)

        # Execute.
        try:
            result: float = method(*operands)
        except (ValueError, ZeroDivisionError, ArithmeticError) as exc:
            self._display_error(str(exc))
            return

        self._display_result(description, operands, result)
        self._history.record_operation(key, operands, result)
        self._refresh_history_display()

    # ------------------------------------------------------------------
    # Mode switching
    # ------------------------------------------------------------------

    def _on_mode_switch(self) -> None:
        """Toggle between Normal and Scientific modes and repopulate operations."""
        self._mode_manager.switch_mode()
        self._mode_label.config(text=self._mode_manager.get_mode_display_name())
        self._populate_operations()
        self._result_label.config(text="")
        self._clear_error()

    # ------------------------------------------------------------------
    # History management
    # ------------------------------------------------------------------

    def _on_clear_history(self) -> None:
        """Clear the session history and update the history display."""
        self._history.clear()
        self._refresh_history_display()

    def _refresh_history_display(self) -> None:
        """Sync the read-only history text widget with the current session history."""
        self._history_text.config(state=tk.NORMAL)
        self._history_text.delete("1.0", tk.END)
        self._history_text.insert(tk.END, self._history.display_history())
        self._history_text.config(state=tk.DISABLED)

    # ------------------------------------------------------------------
    # Result / error display helpers
    # ------------------------------------------------------------------

    def _display_result(
        self, operation: str, operands: list, result: float
    ) -> None:
        """Update the result label with the formatted calculation output.

        Args:
            operation: Human-readable operation description.
            operands: Operand values used in the calculation.
            result: The numeric result.
        """
        operands_str = ", ".join(str(o) for o in operands)
        self._result_label.config(
            text=f"{operation}  ({operands_str})  =  {result}"
        )

    def _display_error(self, message: str) -> None:
        """Show an error message below the execute button.

        The error label is hidden again by :meth:`_clear_error` before each
        new calculation attempt.

        Args:
            message: The error text to display.
        """
        self._error_label.config(text=f"Error: {message}")
        self._error_label.grid()

    def _clear_error(self) -> None:
        """Hide the error label and clear its text."""
        self._error_label.config(text="")
        self._error_label.grid_remove()

    # ------------------------------------------------------------------
    # Run
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the tkinter main event loop."""
        self.root.mainloop()
