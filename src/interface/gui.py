"""Tkinter-based graphical calculator interface.

This module provides GuiCalculator, a tkinter GUI that reuses the existing
Calculator, OperationDispatcher, and History components without duplicating
any core logic.  The GUI coexists with the CLI and interactive REPL modes.

Typical usage::

    from src.core import Calculator
    from src.interface.gui import run_gui

    calc = Calculator()
    run_gui(calc)

Or via the command line::

    python -m src --gui
    CALCULATOR_GUI=1 python -m src
"""

from __future__ import annotations

# tkinter is part of the Python standard library but may be absent in minimal
# installations (e.g. headless CI runners without the python3-tk system package).
# We defer the hard error to instantiation time so that importing this module
# does not break the test suite or the CLI/REPL modes.
try:
    import tkinter as tk
    from tkinter import font as tkfont  # noqa: F401  (reserved for future use)
    _TK_AVAILABLE: bool = True
except ImportError:
    tk = None  # type: ignore[assignment]
    _TK_AVAILABLE = False

from ..core.calculator import Calculator
from ..operations import OPERATIONS
from ..session.history import History
from ..shared.dispatcher import OperationDispatcher
from ..shared.logger import Logger
from .mode import CalculatorMode, ScientificMode, SimpleMode

# Layout constants
_DISPLAY_BG = "#1e1e2e"
_DISPLAY_FG = "#cdd6f4"
_BTN_DIGIT_BG = "#313244"
_BTN_DIGIT_FG = "#cdd6f4"
_BTN_OP_BG = "#45475a"
_BTN_OP_FG = "#cdd6f4"
_BTN_EQUALS_BG = "#89b4fa"
_BTN_EQUALS_FG = "#1e1e2e"
_BTN_CLEAR_BG = "#f38ba8"
_BTN_CLEAR_FG = "#1e1e2e"
_WIN_BG = "#1e1e2e"
_HISTORY_BG = "#181825"
_HISTORY_FG = "#a6adc8"


class GuiCalculator:
    """Tkinter-based graphical calculator.

    Composes the existing Calculator, OperationDispatcher, and History objects
    rather than reimplementing any core logic.  The GUI supports two modes
    (SimpleMode and ScientificMode) and renders operation buttons dynamically
    based on the active mode.

    Args:
        calculator: A Calculator instance used for all arithmetic.
        logger: Optional Logger instance.  When None a Logger is created
            lazily when the first error is logged.
    """

    def __init__(self, calculator: Calculator, logger: Logger | None = None) -> None:
        if not _TK_AVAILABLE:
            raise ImportError(
                "tkinter is not available in this Python installation. "
                "Install the python3-tk package (e.g. 'sudo apt install python3-tk') "
                "and retry."
            )

        self._calculator: Calculator = calculator
        self._dispatcher: OperationDispatcher = OperationDispatcher(calculator)
        self._history: History = History()
        self._logger: Logger | None = logger

        # Mode — start in SimpleMode
        self._current_mode: CalculatorMode = SimpleMode()

        # Internal state
        self._pending_operation: str | None = None
        self._first_operand: float | None = None
        self._waiting_for_second: bool = False

        # Tkinter state — populated in _build_window
        self._root: tk.Tk = tk.Tk()
        self._display_var: tk.StringVar = tk.StringVar(value="0")
        self._operation_buttons: dict[str, tk.Button] = {}
        self._history_text: tk.Text | None = None

        self._build_window()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the tkinter main event loop.

        Blocks until the window is closed by the user.
        """
        self._root.mainloop()

    def switch_mode(self, mode: CalculatorMode) -> None:
        """Change the current calculator mode and rebuild the operation buttons.

        Args:
            mode: The new CalculatorMode instance to activate.
        """
        self._current_mode = mode
        self._build_operation_buttons()

    # ------------------------------------------------------------------
    # Window construction
    # ------------------------------------------------------------------

    def _build_window(self) -> None:
        """Create the complete tkinter widget tree.

        Layout (top to bottom):
        - Title bar
        - Display label
        - Mode selector (Simple / Scientific radio buttons)
        - Digit buttons (0-9 and decimal point) in a grid
        - Operation buttons (dynamic, based on current mode)
        - Equals and Clear buttons
        - History panel (scrollable Text widget)
        """
        self._root.title("Calculator")
        self._root.configure(bg=_WIN_BG)
        self._root.resizable(False, False)

        # --- Display ---
        display_frame = tk.Frame(self._root, bg=_WIN_BG)
        display_frame.pack(fill=tk.X, padx=8, pady=(8, 4))

        display_label = tk.Label(
            display_frame,
            textvariable=self._display_var,
            anchor="e",
            bg=_DISPLAY_BG,
            fg=_DISPLAY_FG,
            font=("Monospace", 22, "bold"),
            width=24,
            relief=tk.FLAT,
            padx=8,
            pady=6,
        )
        display_label.pack(fill=tk.X)

        # --- Mode selector ---
        mode_frame = tk.Frame(self._root, bg=_WIN_BG)
        mode_frame.pack(fill=tk.X, padx=8, pady=(0, 4))

        self._mode_var: tk.StringVar = tk.StringVar(value="simple")

        for label, value in (("Simple", "simple"), ("Scientific", "scientific")):
            rb = tk.Radiobutton(
                mode_frame,
                text=label,
                variable=self._mode_var,
                value=value,
                command=self._on_mode_change,
                bg=_WIN_BG,
                fg=_DISPLAY_FG,
                selectcolor=_WIN_BG,
                activebackground=_WIN_BG,
                activeforeground=_DISPLAY_FG,
            )
            rb.pack(side=tk.LEFT, padx=4)

        # --- Digit buttons ---
        digit_frame = tk.Frame(self._root, bg=_WIN_BG)
        digit_frame.pack(padx=8, pady=4)

        digits = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2),
            ("0", 3, 0), (".", 3, 1),
        ]
        for (text, row, col) in digits:
            btn = tk.Button(
                digit_frame,
                text=text,
                width=5,
                height=2,
                bg=_BTN_DIGIT_BG,
                fg=_BTN_DIGIT_FG,
                activebackground=_BTN_OP_BG,
                activeforeground=_BTN_DIGIT_FG,
                relief=tk.FLAT,
                command=lambda v=text: self._on_digit(v),
            )
            btn.grid(row=row, column=col, padx=2, pady=2)

        # Clear button (placed in digit area, row 3 col 2)
        clear_btn = tk.Button(
            digit_frame,
            text="C",
            width=5,
            height=2,
            bg=_BTN_CLEAR_BG,
            fg=_BTN_CLEAR_FG,
            activebackground="#f38ba8",
            activeforeground=_BTN_CLEAR_FG,
            relief=tk.FLAT,
            command=self._on_clear,
        )
        clear_btn.grid(row=3, column=2, padx=2, pady=2)

        # Equals button (below digit grid)
        equals_btn = tk.Button(
            digit_frame,
            text="=",
            width=17,
            height=2,
            bg=_BTN_EQUALS_BG,
            fg=_BTN_EQUALS_FG,
            activebackground="#89dceb",
            activeforeground=_BTN_EQUALS_FG,
            relief=tk.FLAT,
            command=self._on_equals,
        )
        equals_btn.grid(row=4, column=0, columnspan=3, padx=2, pady=4, sticky="ew")

        # --- Operation buttons (dynamic) ---
        self._op_frame = tk.Frame(self._root, bg=_WIN_BG)
        self._op_frame.pack(padx=8, pady=4, fill=tk.X)

        self._build_operation_buttons()

        # --- History panel ---
        history_label = tk.Label(
            self._root,
            text="History",
            bg=_WIN_BG,
            fg=_DISPLAY_FG,
            font=("Monospace", 10, "bold"),
        )
        history_label.pack(anchor="w", padx=8)

        history_frame = tk.Frame(self._root, bg=_WIN_BG)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._history_text = tk.Text(
            history_frame,
            height=6,
            bg=_HISTORY_BG,
            fg=_HISTORY_FG,
            font=("Monospace", 9),
            state=tk.DISABLED,
            relief=tk.FLAT,
            yscrollcommand=scrollbar.set,
        )
        self._history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self._history_text.yview)

    def _build_operation_buttons(self) -> None:
        """Generate and place operation buttons for the current mode.

        Clears all existing widgets in _op_frame, then creates one button per
        operation returned by the active mode's available_operations().  Binary
        operations and unary operations are both handled by _on_operation_select.
        The mapping from button to op_key is tracked in _operation_buttons.
        """
        # Clear previous buttons
        for widget in self._op_frame.winfo_children():
            widget.destroy()
        self._operation_buttons.clear()

        ops = self._current_mode.available_operations()
        col = 0
        row = 0
        max_cols = 4

        for op_key, op_info in ops.items():
            label = op_info.get("label", op_key)
            # Truncate long labels to keep buttons uniform
            short_label = op_key.replace("_", " ")
            btn = tk.Button(
                self._op_frame,
                text=short_label,
                width=10,
                height=1,
                bg=_BTN_OP_BG,
                fg=_BTN_OP_FG,
                activebackground=_BTN_DIGIT_BG,
                activeforeground=_BTN_OP_FG,
                relief=tk.FLAT,
                command=lambda key=op_key: self._on_operation_select(key),
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
            self._operation_buttons[op_key] = btn
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_mode_change(self) -> None:
        """Handle mode radio button selection.

        Reads the current _mode_var value and calls switch_mode with the
        appropriate CalculatorMode subclass instance.
        """
        value = self._mode_var.get()
        if value == "simple":
            self.switch_mode(SimpleMode())
        else:
            self.switch_mode(ScientificMode())

    def _on_digit(self, value: str) -> None:
        """Append a digit or decimal point to the display.

        If the current display reads "0" or starts with "Error", replace it
        entirely with *value*.  Otherwise append *value* to the existing text.
        Prevents multiple decimal points in a single number.

        Args:
            value: The digit character ("0"–"9") or "." to append.
        """
        current = self._display_var.get()

        if value == "." and "." in current and not current.startswith("Error"):
            # Ignore additional decimal points
            return

        if current == "0" or current.startswith("Error"):
            self._display_var.set(value)
        else:
            self._display_var.set(current + value)

    def _on_clear(self) -> None:
        """Reset the calculator to its initial state.

        Clears the display to "0" and resets all transient operation state
        (_pending_operation, _first_operand, _waiting_for_second).
        """
        self._display_var.set("0")
        self._pending_operation = None
        self._first_operand = None
        self._waiting_for_second = False

    def _on_operation_select(self, op_key: str) -> None:
        """Handle an operation button press.

        For unary operations (arity == 1): parse the current display value,
        execute the operation immediately, update the display, and record
        the result in history.

        For binary operations (arity == 2): store the current display value
        as the first operand and the operation key, then clear the display so
        the user can enter the second operand.

        Args:
            op_key: Key of the selected operation in the OPERATIONS registry.
        """
        ops = self._current_mode.available_operations()
        if op_key not in ops:
            return

        op_info = ops[op_key]
        arity: int = op_info["arity"]
        coerce = op_info.get("coerce", float)

        current = self._display_var.get()

        try:
            value = coerce(current)
        except (ValueError, TypeError) as exc:
            self._handle_error(str(exc))
            return

        if arity == 1:
            try:
                result = self._dispatch(op_key, [value])
            except (ValueError, ZeroDivisionError, TypeError) as exc:
                self._log_error(op_key, exc)
                self._handle_error(str(exc))
                return
            self._display_var.set(self._format_result(result))
            self._history.add_operation(op_key, [value], result)
            self._update_history_display()
        else:
            # Binary: store first operand, wait for second
            self._first_operand = float(value)
            self._pending_operation = op_key
            self._waiting_for_second = True
            self._display_var.set("0")

    def _on_equals(self) -> None:
        """Execute the pending binary operation using the current display value.

        If no binary operation is pending (_waiting_for_second is False),
        this is a no-op.  On success, updates the display and history widget.
        On any arithmetic error, delegates to _handle_error.
        """
        if not self._waiting_for_second:
            return

        ops = self._current_mode.available_operations()
        op_key = self._pending_operation
        if op_key is None or op_key not in ops:
            return

        op_info = ops[op_key]
        coerce = op_info.get("coerce", float)
        current = self._display_var.get()

        try:
            second = coerce(current)
        except (ValueError, TypeError) as exc:
            self._handle_error(str(exc))
            return

        operands = [self._first_operand, float(second)]

        try:
            result = self._dispatch(op_key, operands)
        except ZeroDivisionError:
            if self._logger is None:
                self._logger = Logger()
            self._logger.log_division_by_zero(operands)
            self._handle_error("Division by zero is not allowed.")
            self._reset_binary_state()
            return
        except (ValueError, TypeError) as exc:
            self._log_error(op_key, exc)
            self._handle_error(str(exc))
            self._reset_binary_state()
            return

        self._display_var.set(self._format_result(result))
        self._history.add_operation(op_key, operands, result)
        self._update_history_display()
        self._reset_binary_state()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _dispatch(self, op_key: str, operands: list) -> float | int:
        """Delegate operation execution to OperationDispatcher.

        Args:
            op_key: A key present in the OPERATIONS registry.
            operands: A list of already-coerced operand values.

        Returns:
            The numeric result of the operation.

        Raises:
            ValueError: Propagated from the Calculator method.
            ZeroDivisionError: Propagated from the Calculator method.
            TypeError: Propagated from the Calculator method.
        """
        return self._dispatcher.dispatch(op_key, operands)

    def _update_history_display(self) -> None:
        """Refresh the history Text widget from the History instance.

        Fetches all entries via History.get_all() and rewrites the widget
        content.  The widget is briefly set to NORMAL state to allow writes,
        then restored to DISABLED to prevent user editing.
        """
        if self._history_text is None:
            return
        entries = self._history.get_all()
        self._history_text.config(state=tk.NORMAL)
        self._history_text.delete("1.0", tk.END)
        self._history_text.insert(tk.END, "\n".join(entries))
        self._history_text.config(state=tk.DISABLED)
        # Scroll to the latest entry
        self._history_text.see(tk.END)

    def _handle_error(self, message: str) -> None:
        """Display an error message in the calculator display.

        Args:
            message: The human-readable error description shown to the user.
        """
        self._display_var.set(f"Error: {message}")

    def _log_error(self, op_key: str, exc: Exception) -> None:
        """Log a domain or type error via the Logger instance.

        Creates a Logger lazily if none was provided at construction time.

        Args:
            op_key: The operation that caused the error.
            exc: The caught exception.
        """
        if self._logger is None:
            self._logger = Logger()
        self._logger.log_domain_error(op_key, str(exc))

    def _reset_binary_state(self) -> None:
        """Reset transient binary-operation state after = is pressed."""
        self._pending_operation = None
        self._first_operand = None
        self._waiting_for_second = False

    @staticmethod
    def _format_result(result: float | int) -> str:
        """Format a numeric result for display.

        Displays integers without a decimal point and floats as-is,
        removing unnecessary trailing zeros.

        Args:
            result: The numeric result to format.

        Returns:
            A human-readable string representation.
        """
        if isinstance(result, int):
            return str(result)
        # Remove redundant trailing zeros (e.g. "3.0" -> "3", "3.50" -> "3.5")
        formatted = f"{result:g}"
        return formatted


def run_gui(calculator: Calculator, logger: Logger | None = None) -> None:
    """Create a GuiCalculator and start the tkinter event loop.

    This is the canonical entry point for GUI mode, called from __main__.py.

    Args:
        calculator: The Calculator instance to use for all operations.
        logger: Optional Logger instance passed through to GuiCalculator.
    """
    gui = GuiCalculator(calculator, logger)
    gui.run()
