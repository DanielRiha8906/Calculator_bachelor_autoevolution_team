"""Tkinter window layout and widget management for the Calculator GUI.

:class:`CalculatorWindow` is the main application window.  It owns all
widget construction, layout, and event-callback wiring.  All actual
computation is delegated to the injected :class:`~src.gui.session_adapter.GUISessionAdapter`.
"""

import tkinter as tk
from tkinter import ttk

from .session_adapter import GUISessionAdapter


class CalculatorWindow(tk.Tk):
    """Main Tkinter window for the Calculator GUI.

    Layout (top to bottom):
    - Mode selector frame: ``Normal`` / ``Scientific`` buttons.
    - Operation buttons in a scrollable canvas frame.
    - Input section: two ``Entry`` widgets labeled "Operand 1" / "Operand 2".
    - Execute button.
    - Result label (also used to display errors).
    - History section: scrollable read-only ``Text`` widget.
    - Clear History button.

    Args:
        session_adapter: A configured :class:`~src.gui.session_adapter.GUISessionAdapter`
            that handles all computation and history management.
    """

    def __init__(self, session_adapter: GUISessionAdapter) -> None:
        super().__init__()
        self._adapter: GUISessionAdapter = session_adapter
        self._selected_op: str | None = None

        self.title("Calculator")
        self.resizable(True, True)
        self.minsize(420, 600)

        self._build_ui()

        # Start with Normal mode pre-selected.
        self.on_mode_changed("normal")

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Construct and grid all widgets."""
        self.columnconfigure(0, weight=1)

        # --- Mode selector ---
        mode_frame = ttk.LabelFrame(self, text="Mode", padding=6)
        mode_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))
        mode_frame.columnconfigure(0, weight=1)
        mode_frame.columnconfigure(1, weight=1)

        ttk.Button(
            mode_frame,
            text="Normal",
            command=lambda: self.on_mode_changed("normal"),
        ).grid(row=0, column=0, sticky="ew", padx=4)

        ttk.Button(
            mode_frame,
            text="Scientific",
            command=lambda: self.on_mode_changed("scientific"),
        ).grid(row=0, column=1, sticky="ew", padx=4)

        # --- Operation buttons (scrollable) ---
        ops_outer = ttk.LabelFrame(self, text="Operations", padding=6)
        ops_outer.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)
        ops_outer.columnconfigure(0, weight=1)
        ops_outer.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._ops_canvas = tk.Canvas(ops_outer, height=180, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            ops_outer, orient="vertical", command=self._ops_canvas.yview
        )
        self._ops_canvas.configure(yscrollcommand=scrollbar.set)
        self._ops_canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self._ops_inner_frame = ttk.Frame(self._ops_canvas)
        self._ops_canvas_window = self._ops_canvas.create_window(
            (0, 0), window=self._ops_inner_frame, anchor="nw"
        )

        self._ops_inner_frame.bind("<Configure>", self._on_ops_frame_resize)
        self._ops_canvas.bind("<Configure>", self._on_canvas_resize)

        # --- Input section ---
        input_frame = ttk.LabelFrame(self, text="Inputs", padding=6)
        input_frame.grid(row=2, column=0, sticky="ew", padx=8, pady=4)
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Operand 1:").grid(
            row=0, column=0, sticky="w", padx=4, pady=2
        )
        self._operand1_entry = ttk.Entry(input_frame)
        self._operand1_entry.grid(row=0, column=1, sticky="ew", padx=4, pady=2)

        self._operand2_label = ttk.Label(input_frame, text="Operand 2:")
        self._operand2_label.grid(row=1, column=0, sticky="w", padx=4, pady=2)
        self._operand2_entry = ttk.Entry(input_frame)
        self._operand2_entry.grid(row=1, column=1, sticky="ew", padx=4, pady=2)

        # --- Execute button ---
        ttk.Button(self, text="Execute", command=self.on_execute_clicked).grid(
            row=3, column=0, sticky="ew", padx=8, pady=4
        )

        # --- Result / error label ---
        self._result_var = tk.StringVar(value="")
        result_label = ttk.Label(
            self,
            textvariable=self._result_var,
            wraplength=380,
            anchor="center",
            foreground="black",
        )
        result_label.grid(row=4, column=0, sticky="ew", padx=8, pady=2)
        self._result_label_widget = result_label

        # --- History section ---
        history_outer = ttk.LabelFrame(self, text="History", padding=6)
        history_outer.grid(row=5, column=0, sticky="nsew", padx=8, pady=4)
        history_outer.columnconfigure(0, weight=1)
        history_outer.rowconfigure(0, weight=1)
        self.rowconfigure(5, weight=2)

        self._history_text = tk.Text(
            history_outer, height=8, state="disabled", wrap="word"
        )
        hist_scrollbar = ttk.Scrollbar(
            history_outer, orient="vertical", command=self._history_text.yview
        )
        self._history_text.configure(yscrollcommand=hist_scrollbar.set)
        self._history_text.grid(row=0, column=0, sticky="nsew")
        hist_scrollbar.grid(row=0, column=1, sticky="ns")

        # --- Clear History button ---
        ttk.Button(
            self, text="Clear History", command=self.on_clear_history_clicked
        ).grid(row=6, column=0, sticky="ew", padx=8, pady=(0, 8))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _on_ops_frame_resize(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        """Update the scrollable region when the inner frame changes size."""
        self._ops_canvas.configure(
            scrollregion=self._ops_canvas.bbox("all")
        )

    def _on_canvas_resize(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        """Keep the inner frame width in sync with the canvas width."""
        self._ops_canvas.itemconfigure(
            self._ops_canvas_window, width=event.width
        )

    def _set_result(self, text: str, is_error: bool = False) -> None:
        """Display *text* in the result label, coloured red if *is_error*."""
        self._result_var.set(text)
        colour = "red" if is_error else "dark green"
        self._result_label_widget.configure(foreground=colour)

    # ------------------------------------------------------------------
    # Public event handlers
    # ------------------------------------------------------------------

    def on_mode_changed(self, mode_name: str) -> None:
        """Switch the calculator to *mode_name* and refresh operation buttons.

        Args:
            mode_name: ``"normal"`` or ``"scientific"``.
        """
        self._adapter.set_mode(mode_name)
        self._selected_op = None
        self._set_result("")
        self.update_operation_buttons()

    def on_operation_selected(self, op_name: str) -> None:
        """Record the chosen operation and update the Operand 2 field state.

        Operand 2 is disabled for unary operations and re-enabled for binary
        ones.

        Args:
            op_name: The canonical operation name chosen by the user.
        """
        self._selected_op = op_name
        self._set_result("")

        arity = self._adapter.get_arity(op_name)
        if arity == 1:
            self._operand2_entry.delete(0, tk.END)
            self._operand2_entry.configure(state="disabled")
            self._operand2_label.configure(foreground="grey")
        else:
            self._operand2_entry.configure(state="normal")
            self._operand2_label.configure(foreground="black")

    def on_execute_clicked(self) -> None:
        """Read inputs, execute the selected operation, and display the result.

        Shows an inline error message (without a popup dialog) when:
        - No operation has been selected.
        - An operand field contains a non-numeric value.
        - The calculator raises an exception (e.g. division by zero).
        """
        if self._selected_op is None:
            self._set_result("Please select an operation first.", is_error=True)
            return

        raw1 = self._operand1_entry.get().strip()
        try:
            op1 = float(raw1)
        except ValueError:
            self._set_result(
                f"Operand 1 is not a valid number: {raw1!r}", is_error=True
            )
            return

        arity = self._adapter.get_arity(self._selected_op)
        operands: list[float] = [op1]

        if arity > 1:
            raw2 = self._operand2_entry.get().strip()
            try:
                op2 = float(raw2)
            except ValueError:
                self._set_result(
                    f"Operand 2 is not a valid number: {raw2!r}", is_error=True
                )
                return
            operands.append(op2)

        result_str, error_msg = self._adapter.execute_operation_safe(
            self._selected_op, operands
        )

        if error_msg:
            self._set_result(f"Error: {error_msg}", is_error=True)
        else:
            self._set_result(f"Result: {result_str}")
            self.update_history_display()

    def on_clear_history_clicked(self) -> None:
        """Clear the session history and refresh the history display."""
        self._adapter.clear_history()
        self.update_history_display()

    def update_history_display(self) -> None:
        """Reload all history entries into the read-only history Text widget."""
        self._history_text.configure(state="normal")
        self._history_text.delete("1.0", tk.END)
        entries = self._adapter.get_history()
        for entry in entries:
            self._history_text.insert(tk.END, entry + "\n")
        self._history_text.configure(state="disabled")
        self._history_text.see(tk.END)

    def update_operation_buttons(self) -> None:
        """Rebuild the operation button grid for the current mode.

        Destroys all existing buttons in the scrollable inner frame and
        creates one button per operation returned by the adapter.
        """
        for widget in self._ops_inner_frame.winfo_children():
            widget.destroy()

        operations = self._adapter.get_operations()
        columns = 3

        for idx, op_name in enumerate(operations):
            row, col = divmod(idx, columns)
            btn = ttk.Button(
                self._ops_inner_frame,
                text=op_name,
                command=lambda name=op_name: self.on_operation_selected(name),
            )
            btn.grid(row=row, column=col, sticky="ew", padx=3, pady=2)

        for col in range(columns):
            self._ops_inner_frame.columnconfigure(col, weight=1)

        # Force the scrollregion to update immediately.
        self._ops_inner_frame.update_idletasks()
        self._ops_canvas.configure(
            scrollregion=self._ops_canvas.bbox("all")
        )
