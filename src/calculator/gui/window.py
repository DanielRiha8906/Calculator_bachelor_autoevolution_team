"""GUI Window for the Calculator application (Issue #414).

Provides GUIWindow — the tkinter-based user interface that delegates all
business logic to GUIController.  This module requires tkinter to be
installed (standard library on most Python distributions).
"""

import tkinter as tk
from tkinter import ttk

from src.calculator.gui.controller import GUIController


class GUIWindow:
    """Tkinter-based calculator window.

    Renders mode selection, operation dropdown, dynamic operand entry fields,
    a result label, and a history listbox.  All computation is delegated to
    the injected :class:`GUIController`.

    Args:
        controller: The GUIController instance that provides business logic.
        title: Window title string.  Defaults to ``"Calculator"``.
    """

    def __init__(self, controller: GUIController, title: str = "Calculator") -> None:
        self._controller = controller

        # Root window
        self.root = tk.Tk()
        self.root.title(title)

        # Shared state variables
        self._mode_var = tk.StringVar(value=controller.get_current_mode())
        self._operand_entries: list[tk.Entry] = []

        # Build all UI sections
        self._build_mode_frame()
        self._build_operation_frame()
        self._build_operand_frame()
        self._build_calculate_button()
        self._build_result_label()
        self._build_history_frame()

        # Initialise dropdown and operand fields
        self._update_operation_dropdown()

    # ------------------------------------------------------------------
    # Layout builders
    # ------------------------------------------------------------------

    def _build_mode_frame(self) -> None:
        """Build the mode selection radio-button row."""
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X, padx=8, pady=4)
        tk.Label(frame, text="Mode:").pack(side=tk.LEFT)
        tk.Radiobutton(
            frame,
            text="Normal",
            variable=self._mode_var,
            value="normal",
            command=self._on_mode_changed,
        ).pack(side=tk.LEFT)
        tk.Radiobutton(
            frame,
            text="Scientific",
            variable=self._mode_var,
            value="scientific",
            command=self._on_mode_changed,
        ).pack(side=tk.LEFT)

    def _build_operation_frame(self) -> None:
        """Build the operation selection row with a combobox."""
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X, padx=8, pady=4)
        tk.Label(frame, text="Operation:").pack(side=tk.LEFT)
        self._operation_dropdown = ttk.Combobox(frame, state="readonly")
        self._operation_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._operation_dropdown.bind("<<ComboboxSelected>>", self._on_operation_selected)

    def _build_operand_frame(self) -> None:
        """Build the container frame for dynamic operand entry widgets."""
        self._operand_frame = tk.Frame(self.root)
        self._operand_frame.pack(fill=tk.X, padx=8, pady=4)

    def _build_calculate_button(self) -> None:
        """Build the Calculate button."""
        tk.Button(
            self.root,
            text="Calculate",
            command=self._on_calculate_clicked,
        ).pack(padx=8, pady=4)

    def _build_result_label(self) -> None:
        """Build the result display label."""
        self._result_label = tk.Label(self.root, text="")
        self._result_label.pack(padx=8, pady=4)

    def _build_history_frame(self) -> None:
        """Build the history section with a listbox and scrollbar."""
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        tk.Label(frame, text="History:").pack(anchor=tk.W)
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        self._history_listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self._history_listbox.yview)
        self._history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the tkinter main event loop (blocking)."""
        self.root.mainloop()

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_mode_changed(self) -> None:
        """Handle a mode radio-button selection change."""
        mode = self._mode_var.get()
        self._controller.switch_mode(mode)
        self._update_operation_dropdown()
        self._update_operand_fields(0)
        self._update_history_display()
        self._result_label.config(text="")

    def _on_operation_selected(self, event: object = None) -> None:
        """Handle a combobox selection event, updating operand fields."""
        op = self._operation_dropdown.get()
        try:
            arity = self._controller.get_operation_arity(op)
        except KeyError:
            arity = 0
        self._update_operand_fields(arity)

    def _on_calculate_clicked(self) -> None:
        """Read operands, call execute_operation, and display the result."""
        op = self._operation_dropdown.get()
        operands: list[float] = []
        for entry in self._operand_entries:
            raw = entry.get()
            try:
                operands.append(float(raw))
            except ValueError:
                self._result_label.config(text=f"Error: Invalid number '{raw}'")
                return
        result = self._controller.execute_operation(op, operands)
        if result["success"]:
            self._result_label.config(text=self._format_result_display(result))
            self._update_history_display()
        else:
            self._result_label.config(text=f"Error: {result['error']}")

    # ------------------------------------------------------------------
    # UI update helpers
    # ------------------------------------------------------------------

    def _update_operation_dropdown(self) -> None:
        """Refresh the combobox values from the controller's available ops."""
        ops = self._controller.get_available_operations()
        self._operation_dropdown["values"] = ops
        if ops:
            self._operation_dropdown.set(ops[0])
            self._on_operation_selected()

    def _update_operand_fields(self, arity: int) -> None:
        """Rebuild the operand entry widgets to match the required *arity*.

        Args:
            arity: Number of operand entry fields to display.
        """
        for widget in self._operand_frame.winfo_children():
            widget.destroy()
        self._operand_entries = []
        for i in range(arity):
            label = tk.Label(self._operand_frame, text=f"Operand {i + 1}:")
            label.grid(row=i, column=0, sticky=tk.W)
            entry = tk.Entry(self._operand_frame)
            entry.grid(row=i, column=1, sticky=tk.EW)
            self._operand_entries.append(entry)

    def _update_history_display(self) -> None:
        """Refresh the history listbox from the controller's session history."""
        self._history_listbox.delete(0, tk.END)
        for entry_str in self._controller.get_session_history():
            self._history_listbox.insert(tk.END, entry_str)

    def _format_result_display(self, result_dict: dict) -> str:
        """Format a successful result dict as a human-readable string.

        Args:
            result_dict: A dict with ``success``, ``operation``, ``operands``,
                and ``result`` keys.

        Returns:
            A string such as ``"add(2, 3) = 5"``.
        """
        if result_dict["success"]:
            op = result_dict["operation"]
            operands = result_dict["operands"]
            result = result_dict["result"]
            return f"{op}({', '.join(str(o) for o in operands)}) = {result}"
        return f"Error: {result_dict['error']}"
