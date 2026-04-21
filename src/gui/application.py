"""Main GUI application for the Calculator.

This module contains :class:`CalculatorGUI`, a tkinter-based calculator
interface that supports both Simple and Scientific modes, maintains a
calculation history panel, and delegates all arithmetic to the
:class:`~src.core.calculator.Calculator` backend.

No arithmetic is performed in this module; the GUI is purely responsible
for input collection, dispatch, display, and history rendering.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import font as tkfont
from typing import Callable

from src.core.calculator import Calculator
from src.support.history import HistoryTracker
from src.gui.modes import CalcMode, SimpleMode, ScientificMode


class CalculatorGUI:
    """Tkinter-based calculator GUI.

    Handles user interaction for a :class:`~src.core.calculator.Calculator`
    backend.  The visible operation buttons are driven entirely by the active
    :class:`~src.gui.modes.CalcMode`, so swapping modes rebuilds the widget
    tree while preserving the shared :class:`~src.support.history.HistoryTracker`.

    Args:
        root: The top-level Tk window.
        calculator: The Calculator instance used for all computation.
        mode: The initial CalcMode (Simple or Scientific).
        history_tracker: The shared HistoryTracker instance.

    Attributes:
        _current_input: The digit/decimal string the user is currently typing.
        _first_operand: The stored first operand for a pending binary operation.
        _pending_op: A ``(callable, arity)`` tuple for the queued operation,
            or ``None`` when no operation is pending.
        _pending_op_name: The name string of the pending operation, used when
            recording history.
    """

    def __init__(
        self,
        root: tk.Tk,
        calculator: Calculator,
        mode: CalcMode,
        history_tracker: HistoryTracker,
    ) -> None:
        self._root = root
        self._calculator = calculator
        self._mode = mode
        self._history_tracker = history_tracker

        # Mutable state
        self._current_input: str = ""
        self._first_operand: float | None = None
        self._pending_op: tuple[Callable, int] | None = None
        self._pending_op_name: str | None = None

        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction helpers
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Build or rebuild the entire widget tree for the current mode.

        Called on initial construction and whenever the mode is switched.
        All previously created widgets are destroyed before rebuilding so
        that a clean layout is produced for the new mode.
        """
        for widget in self._root.winfo_children():
            widget.destroy()

        self._root.configure(bg="#2b2b2b")
        self._root.resizable(True, True)

        # ---- top-level frames ----
        left_frame = tk.Frame(self._root, bg="#2b2b2b")
        left_frame.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

        right_frame = tk.Frame(self._root, bg="#2b2b2b")
        right_frame.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")

        self._root.columnconfigure(0, weight=3)
        self._root.columnconfigure(1, weight=2)
        self._root.rowconfigure(0, weight=1)

        self._build_display(left_frame)
        self._build_mode_buttons(left_frame)
        self._build_number_buttons(left_frame)
        self._build_operation_buttons(left_frame)
        self._build_history_panel(right_frame)

        self._refresh_history()

    def _build_display(self, parent: tk.Frame) -> None:
        """Build the calculator display entry widget.

        Args:
            parent: The parent frame to attach the display to.
        """
        display_font = tkfont.Font(family="Courier", size=20, weight="bold")
        self._display_var = tk.StringVar(value="0")
        self._display = tk.Entry(
            parent,
            textvariable=self._display_var,
            font=display_font,
            bd=0,
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="#ffffff",
            justify="right",
            state="readonly",
            readonlybackground="#1e1e1e",
        )
        self._display.grid(row=0, column=0, columnspan=4, sticky="ew", padx=4, pady=(4, 8))
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        parent.columnconfigure(3, weight=1)

    def _build_mode_buttons(self, parent: tk.Frame) -> None:
        """Build the Simple / Scientific mode-switch buttons.

        Args:
            parent: The parent frame to attach the buttons to.
        """
        btn_font = tkfont.Font(family="Arial", size=10)
        simple_btn = tk.Button(
            parent,
            text="Simple",
            font=btn_font,
            bg="#3c3f41" if self._mode.name == "Scientific" else "#007acc",
            fg="#ffffff",
            relief="flat",
            command=self._switch_to_simple,
        )
        simple_btn.grid(row=1, column=0, columnspan=2, sticky="ew", padx=2, pady=2)

        scientific_btn = tk.Button(
            parent,
            text="Scientific",
            font=btn_font,
            bg="#3c3f41" if self._mode.name == "Simple" else "#007acc",
            fg="#ffffff",
            relief="flat",
            command=self._switch_to_scientific,
        )
        scientific_btn.grid(row=1, column=2, columnspan=2, sticky="ew", padx=2, pady=2)

    def _build_number_buttons(self, parent: tk.Frame) -> None:
        """Build the digit (0-9), decimal, clear, and equals buttons.

        The layout mirrors a standard calculator numpad:
        rows 7-8-9, 4-5-6, 1-2-3, then clear/0/decimal/equals.

        Args:
            parent: The parent frame to attach the buttons to.
        """
        btn_font = tkfont.Font(family="Arial", size=14)

        digit_layout = [
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2),
        ]

        for label, row, col in digit_layout:
            btn = tk.Button(
                parent,
                text=label,
                font=btn_font,
                bg="#3c3f41",
                fg="#ffffff",
                relief="flat",
                width=3,
                command=lambda d=label: self._on_digit(d),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

        # Bottom row: Clear, 0, decimal, equals
        clear_btn = tk.Button(
            parent,
            text="C",
            font=btn_font,
            bg="#cc3333",
            fg="#ffffff",
            relief="flat",
            width=3,
            command=self._on_clear,
        )
        clear_btn.grid(row=5, column=0, sticky="nsew", padx=2, pady=2)

        zero_btn = tk.Button(
            parent,
            text="0",
            font=btn_font,
            bg="#3c3f41",
            fg="#ffffff",
            relief="flat",
            width=3,
            command=lambda: self._on_digit("0"),
        )
        zero_btn.grid(row=5, column=1, sticky="nsew", padx=2, pady=2)

        dot_btn = tk.Button(
            parent,
            text=".",
            font=btn_font,
            bg="#3c3f41",
            fg="#ffffff",
            relief="flat",
            width=3,
            command=self._on_decimal,
        )
        dot_btn.grid(row=5, column=2, sticky="nsew", padx=2, pady=2)

        equals_btn = tk.Button(
            parent,
            text="=",
            font=btn_font,
            bg="#007acc",
            fg="#ffffff",
            relief="flat",
            width=3,
            command=self._on_equals,
        )
        equals_btn.grid(row=5, column=3, sticky="nsew", padx=2, pady=2)

        for r in range(2, 6):
            parent.rowconfigure(r, weight=1)

    def _build_operation_buttons(self, parent: tk.Frame) -> None:
        """Build one button per operation provided by the current mode.

        Binary operations (arity 2) queue themselves as the pending
        operation and await a second operand and = press.
        Unary operations (arity 1) execute immediately on the current input.

        Args:
            parent: The parent frame to attach the buttons to.
        """
        btn_font = tkfont.Font(family="Arial", size=11)
        operations = self._mode.get_operations()

        # Place operation buttons in a sub-frame below the numpad, spanning
        # all 4 columns, flowing left-to-right, 4 per row.
        ops_frame = tk.Frame(parent, bg="#2b2b2b")
        ops_frame.grid(row=6, column=0, columnspan=4, sticky="ew", padx=0, pady=(6, 2))

        for col_idx in range(4):
            ops_frame.columnconfigure(col_idx, weight=1)

        for idx, (op_name, (op_callable, arity)) in enumerate(operations.items()):
            row_idx = idx // 4
            col_idx = idx % 4
            label = op_name.replace("_", " ")
            btn = tk.Button(
                ops_frame,
                text=label,
                font=btn_font,
                bg="#4a4a6a",
                fg="#ffffff",
                relief="flat",
                command=lambda name=op_name, fn=op_callable, ar=arity: self._on_operation(name, fn, ar),
            )
            btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=2, pady=2)
            ops_frame.rowconfigure(row_idx, weight=1)

    def _build_history_panel(self, parent: tk.Frame) -> None:
        """Build the history panel showing past calculations.

        Args:
            parent: The parent frame containing the history widgets.
        """
        label_font = tkfont.Font(family="Arial", size=11, weight="bold")
        history_label = tk.Label(
            parent,
            text="History",
            font=label_font,
            bg="#2b2b2b",
            fg="#aaaaaa",
            anchor="w",
        )
        history_label.pack(fill="x", padx=4, pady=(4, 2))

        list_font = tkfont.Font(family="Courier", size=10)
        self._history_listbox = tk.Listbox(
            parent,
            font=list_font,
            bg="#1e1e1e",
            fg="#cccccc",
            selectbackground="#007acc",
            selectforeground="#ffffff",
            bd=0,
            highlightthickness=0,
            activestyle="none",
        )
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=self._history_listbox.yview)
        self._history_listbox.configure(yscrollcommand=scrollbar.set)

        self._history_listbox.pack(side="left", fill="both", expand=True, padx=(4, 0), pady=4)
        scrollbar.pack(side="right", fill="y", pady=4)

        parent.rowconfigure(0, weight=1)

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def _set_display(self, text: str) -> None:
        """Update the display widget content.

        Args:
            text: The string to show in the display.
        """
        self._display_var.set(text)

    def _get_display(self) -> str:
        """Return the current display content.

        Returns:
            The string currently shown in the display.
        """
        return self._display_var.get()

    # ------------------------------------------------------------------
    # Input event handlers
    # ------------------------------------------------------------------

    def _on_digit(self, digit: str) -> None:
        """Append a digit character to the current input.

        If the display currently shows an error message the input is reset
        before appending the new digit.

        Args:
            digit: A single digit character "0"-"9".
        """
        if self._current_input.startswith("Error"):
            self._current_input = ""
        self._current_input += digit
        self._set_display(self._current_input)

    def _on_decimal(self) -> None:
        """Append a decimal point to the current input, if not already present.

        Prevents multiple decimal points in the same number.  If the
        display shows an error, the input is reset first.
        """
        if self._current_input.startswith("Error"):
            self._current_input = ""
        if "." not in self._current_input:
            self._current_input += "."
            self._set_display(self._current_input if self._current_input != "." else "0.")

    def _on_clear(self) -> None:
        """Reset all transient state: current input, pending operation, operand."""
        self._current_input = ""
        self._first_operand = None
        self._pending_op = None
        self._pending_op_name = None
        self._set_display("0")

    def _on_operation(self, op_name: str, op_callable: Callable, arity: int) -> None:
        """Handle an operation button press.

        For unary operations (arity 1): execute immediately on the current
        input value.

        For binary operations (arity 2): store the current input as the first
        operand and queue the operation, waiting for a second operand and
        ``=`` press.

        Args:
            op_name: The operation identifier string (e.g. ``"add"``).
            op_callable: The bound Calculator method to invoke.
            arity: The number of operands: 1 (unary) or 2 (binary).
        """
        if arity == 1:
            value = self._parse_current_input()
            if value is None:
                self._set_display("Error: invalid input")
                return
            self._execute_unary(op_name, op_callable, value)
        else:
            # Binary: store first operand and queue operation
            value = self._parse_current_input()
            if value is None:
                self._set_display("Error: invalid input")
                return
            self._first_operand = value
            self._pending_op = (op_callable, arity)
            self._pending_op_name = op_name
            self._current_input = ""

    def _on_equals(self) -> None:
        """Execute the pending binary operation with the second operand.

        Does nothing if no binary operation is queued.  On success the
        display is updated with the result and the state is reset.  On
        failure an error message is shown in the display.
        """
        if self._pending_op is None:
            return

        second_value = self._parse_current_input()
        if second_value is None:
            self._set_display("Error: invalid input")
            return

        op_callable, _ = self._pending_op
        op_name = self._pending_op_name

        try:
            result = op_callable(self._first_operand, second_value)
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            self._set_display(f"Error: {exc}")
            self._current_input = f"Error: {exc}"
            self._pending_op = None
            self._pending_op_name = None
            self._first_operand = None
            return

        self._history_tracker.record(op_name, [self._first_operand, second_value], result)
        self._refresh_history()

        result_str = self._format_result(result)
        self._set_display(result_str)
        self._current_input = result_str
        self._first_operand = None
        self._pending_op = None
        self._pending_op_name = None

    # ------------------------------------------------------------------
    # Calculation helpers
    # ------------------------------------------------------------------

    def _execute_unary(self, op_name: str, op_callable: Callable, value: float) -> None:
        """Run a unary operation and update the display with the result.

        Args:
            op_name: The operation identifier string.
            op_callable: The bound Calculator method to invoke.
            value: The single numeric operand.
        """
        # factorial requires an int; convert if the value is a whole number
        if op_name == "factorial":
            if value != int(value):
                self._set_display("Error: factorial requires an integer")
                self._current_input = "Error: factorial requires an integer"
                return
            value = int(value)

        try:
            result = op_callable(value)
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            self._set_display(f"Error: {exc}")
            self._current_input = f"Error: {exc}"
            return

        self._history_tracker.record(op_name, [value], result)
        self._refresh_history()

        result_str = self._format_result(result)
        self._set_display(result_str)
        self._current_input = result_str

    def _parse_current_input(self) -> float | None:
        """Parse the current input string as a float.

        Returns:
            The parsed float value, or ``None`` if the string is empty or
            cannot be converted.
        """
        raw = self._current_input.strip()
        if not raw or raw.startswith("Error"):
            return None
        try:
            return float(raw)
        except ValueError:
            return None

    @staticmethod
    def _format_result(result: object) -> str:
        """Format a calculation result for display.

        Integers and whole-number floats are displayed without a decimal
        point to keep the output clean (e.g. ``"5"`` instead of ``"5.0"``).
        Very long floats are shown to a maximum of 10 significant digits.

        Args:
            result: The raw value returned by a Calculator method.

        Returns:
            A human-readable string representation of the result.
        """
        if isinstance(result, int):
            return str(result)
        if isinstance(result, float):
            if result == int(result) and not (result != result):  # not NaN
                return str(int(result))
            # Use up to 10 significant digits, strip trailing zeros
            formatted = f"{result:.10g}"
            return formatted
        return str(result)

    # ------------------------------------------------------------------
    # History helpers
    # ------------------------------------------------------------------

    def _refresh_history(self) -> None:
        """Repopulate the history listbox from the HistoryTracker.

        Clears the listbox and inserts all current history entries, then
        scrolls to show the most recent entry.
        """
        self._history_listbox.delete(0, tk.END)
        for entry in self._history_tracker.get_history():
            self._history_listbox.insert(tk.END, entry)
        if self._history_tracker.get_history():
            self._history_listbox.see(tk.END)

    # ------------------------------------------------------------------
    # Mode switching
    # ------------------------------------------------------------------

    def _switch_to_simple(self) -> None:
        """Switch the calculator to Simple mode and rebuild the UI.

        No-op if the current mode is already Simple.
        """
        if self._mode.name == "Simple":
            return
        self._mode = SimpleMode(self._calculator)
        self._reset_transient_state()
        self._build_ui()

    def _switch_to_scientific(self) -> None:
        """Switch the calculator to Scientific mode and rebuild the UI.

        No-op if the current mode is already Scientific.
        """
        if self._mode.name == "Scientific":
            return
        self._mode = ScientificMode(self._calculator)
        self._reset_transient_state()
        self._build_ui()

    def _reset_transient_state(self) -> None:
        """Reset all transient calculator state without touching the history."""
        self._current_input = ""
        self._first_operand = None
        self._pending_op = None
        self._pending_op_name = None
