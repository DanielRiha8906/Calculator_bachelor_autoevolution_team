"""Tkinter-based GUI for the calculator application.

This module provides :class:`CalculatorGUI`, a fully self-contained graphical
interface styled after an iOS calculator.  It wires together
:class:`~calculator.Calculator`, :class:`~operations.OperationRegistry`,
:class:`~mode_manager.ModeManager`, and :class:`~session_history.SessionHistory`.

It intentionally avoids importing ``InputHandler``, ``OperationHistory``, or
``CalculatorWorkflow`` — those are CLI/workflow concerns that do not belong in
the GUI layer.
"""

import tkinter as tk

from .calculator import Calculator
from .mode_manager import ModeManager
from .operations import OperationRegistry
from .session_history import SessionHistory

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
_BG = "#000000"
_BTN_DIGIT = "#333333"
_BTN_OPERATOR = "#FF9500"
_BTN_UTILITY = "#A5A5A5"
_FG = "#FFFFFF"

# Button dimensions (pixels)
_BTN_WIDTH = 72
_BTN_HEIGHT = 72
_BTN_PAD = 4

# Display font
_DISPLAY_FONT = ("Helvetica", 28)

# Map from display symbol to OperationRegistry key
_SYMBOL_TO_KEY: dict[str, str] = {
    "+": "add",
    "−": "subtract",
    "×": "multiply",
    "÷": "divide",
    "√": "square_root",
    "x²": "square",
    "xʸ": "power",
    "n!": "factorial",
    "ln": "ln",
    "log": "log",
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
}

# Set of binary operator symbols (require two operands)
_BINARY_OPERATORS: frozenset[str] = frozenset({"+", "−", "×", "÷", "xʸ"})

# Set of unary operator symbols (require one operand)
_UNARY_OPERATORS: frozenset[str] = frozenset({"√", "x²", "n!", "ln", "log", "sin", "cos", "tan"})


class CalculatorGUI:
    """iOS-inspired graphical calculator interface built with tkinter.

    The GUI renders a numeric keypad with an optional scientific panel that
    slides in when Mode is toggled.  All computation is delegated to the
    :class:`~calculator.Calculator` instance via :class:`~operations.OperationRegistry`.

    Args:
        root: The top-level :class:`tk.Tk` window.
        history: A :class:`~session_history.SessionHistory` instance used to
            record past calculations.

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
        """Initialise the GUI, engine components, internal state, and build widgets.

        Args:
            root: The top-level Tk window.
            history: Session history instance for recording operations.
        """
        self.root: tk.Tk = root
        self.root.title("Calculator")
        self.root.configure(bg=_BG)
        self.root.resizable(False, False)

        self._history: SessionHistory = history
        self._calc: Calculator = Calculator()
        self._registry: OperationRegistry = OperationRegistry(self._calc)
        self._mode_manager: ModeManager = ModeManager()

        # --- Internal calculator state ---
        self._display_value: str = "0"
        self._accumulated_value: float | None = None
        self._pending_operator: str | None = None
        self._is_new_number: bool = True

        self._build_widgets()

    # ------------------------------------------------------------------
    # Widget construction
    # ------------------------------------------------------------------

    def _build_widgets(self) -> None:
        """Create the display label and button frames and pack them into root."""
        # Top-level container — fills the window
        self._main_frame = tk.Frame(self.root, bg=_BG)
        self._main_frame.pack(fill=tk.BOTH, expand=True)

        # Display area
        self._display_label = tk.Label(
            self._main_frame,
            text=self._display_value,
            font=_DISPLAY_FONT,
            bg=_BG,
            fg=_FG,
            anchor="e",
            padx=12,
            pady=8,
        )
        self._display_label.pack(fill=tk.X)

        # Separator line between display and buttons
        tk.Frame(self._main_frame, bg="#222222", height=1).pack(fill=tk.X)

        # Button area — horizontal layout: [optional scientific] [standard]
        self._buttons_frame = tk.Frame(self._main_frame, bg=_BG)
        self._buttons_frame.pack()

        # Scientific panel (hidden by default)
        self._scientific_frame = tk.Frame(self._buttons_frame, bg=_BG)
        self._build_scientific_grid(self._scientific_frame)
        # Do NOT pack _scientific_frame yet — it is shown on mode switch.

        # Standard grid is always visible
        self._standard_frame = tk.Frame(self._buttons_frame, bg=_BG)
        self._standard_frame.pack(side=tk.LEFT)
        self._build_standard_grid(self._standard_frame)

    def _make_button(
        self,
        parent: tk.Frame,
        text: str,
        bg: str,
        command,
        column_span: int = 1,
    ) -> tk.Button:
        """Create and return a styled calculator button (without placing it).

        Args:
            parent: The parent frame to attach the button to.
            text: The label shown on the button face.
            bg: Background colour hex string.
            command: Callable invoked on button press.
            column_span: How many grid columns the button spans (for the
                wide zero button).

        Returns:
            The configured but unplaced :class:`tk.Button` instance.
        """
        width_px = _BTN_WIDTH * column_span + _BTN_PAD * (column_span - 1)
        btn = tk.Button(
            parent,
            text=text,
            font=("Helvetica", 16, "bold"),
            bg=bg,
            fg=_FG,
            activebackground=bg,
            activeforeground=_FG,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            width=1,
            height=1,
            command=command,
        )
        # Override the size in pixels via the image trick — simpler: just use
        # padx/pady to achieve uniform button faces without importing PIL.
        btn.configure(padx=0, pady=0)
        btn.config(width=width_px // 10, height=2)
        return btn

    def _build_standard_grid(self, parent: tk.Frame) -> None:
        """Create the 4-column by 5-row standard button grid.

        Layout::

            Row 0: [C]      [Del]   [Mode]  [÷]
            Row 1: [7]      [8]     [9]     [×]
            Row 2: [4]      [5]     [6]     [ ]   <- empty cell (−)
            Row 3: [1]      [2]     [3]     [−]
            Row 4: [0 ×2]          [.]     [=]

        The minus key sits on the right of row 3 and the empty cell in row 2
        keeps the grid symmetrical with the iOS layout (the − button is taller
        on a real iOS calc; here we place it in row 3 right).

        Args:
            parent: The frame in which to build the grid.
        """
        pad = _BTN_PAD

        # Row 0 — utility row
        row0: list[tuple[str, str, object, int]] = [
            ("C",    _BTN_UTILITY,  self._on_clear,            1),
            ("Del",  _BTN_UTILITY,  self._on_delete,           1),
            ("Mode", _BTN_UTILITY,  self._on_mode_switch,      1),
            ("÷",    _BTN_OPERATOR, lambda: self._on_operator("÷"), 1),
        ]
        # Row 1 — digits 7-9 + multiply
        row1: list[tuple[str, str, object, int]] = [
            ("7", _BTN_DIGIT, lambda: self._on_digit("7"), 1),
            ("8", _BTN_DIGIT, lambda: self._on_digit("8"), 1),
            ("9", _BTN_DIGIT, lambda: self._on_digit("9"), 1),
            ("×", _BTN_OPERATOR, lambda: self._on_operator("×"), 1),
        ]
        # Row 2 — digits 4-6 + empty slot
        row2: list[tuple[str, str, object, int]] = [
            ("4", _BTN_DIGIT, lambda: self._on_digit("4"), 1),
            ("5", _BTN_DIGIT, lambda: self._on_digit("5"), 1),
            ("6", _BTN_DIGIT, lambda: self._on_digit("6"), 1),
            ("",  _BG,        lambda: None,                  1),  # empty cell
        ]
        # Row 3 — digits 1-3 + subtract
        row3: list[tuple[str, str, object, int]] = [
            ("1", _BTN_DIGIT, lambda: self._on_digit("1"), 1),
            ("2", _BTN_DIGIT, lambda: self._on_digit("2"), 1),
            ("3", _BTN_DIGIT, lambda: self._on_digit("3"), 1),
            ("−", _BTN_OPERATOR, lambda: self._on_operator("−"), 1),
        ]
        # Row 4 — zero (wide) + decimal + equals
        row4: list[tuple[str, str, object, int]] = [
            ("0", _BTN_DIGIT,    lambda: self._on_digit("0"), 2),
            (".", _BTN_DIGIT,    self._on_decimal,            1),
            ("=", _BTN_UTILITY,  self._on_equals,             1),
        ]

        rows = [row0, row1, row2, row3, row4]
        for row_idx, row_def in enumerate(rows):
            col_idx = 0
            for text, bg, cmd, span in row_def:
                btn = self._make_button(parent, text, bg, cmd, column_span=span)
                btn.grid(
                    row=row_idx,
                    column=col_idx,
                    columnspan=span,
                    padx=pad,
                    pady=pad,
                    sticky="nsew",
                )
                col_idx += span

    def _build_scientific_grid(self, parent: tk.Frame) -> None:
        """Create the scientific functions button grid (shown in scientific mode).

        Functions arranged in a 2-column grid to the left of the standard pad::

            Row 0: [√]   [x²]
            Row 1: [xʸ]  [n!]
            Row 2: [ln]  [log]
            Row 3: [sin] [cos]
            Row 4: [tan] [ ]

        Args:
            parent: The frame in which to build the scientific grid.
        """
        pad = _BTN_PAD
        sci_buttons: list[tuple[str, object]] = [
            ("√",   lambda: self._on_operator("√")),
            ("x²",  lambda: self._on_operator("x²")),
            ("xʸ",  lambda: self._on_operator("xʸ")),
            ("n!",  lambda: self._on_operator("n!")),
            ("ln",  lambda: self._on_operator("ln")),
            ("log", lambda: self._on_operator("log")),
            ("sin", lambda: self._on_operator("sin")),
            ("cos", lambda: self._on_operator("cos")),
            ("tan", lambda: self._on_operator("tan")),
        ]
        for idx, (text, cmd) in enumerate(sci_buttons):
            row_idx = idx // 2
            col_idx = idx % 2
            btn = self._make_button(parent, text, _BTN_OPERATOR, cmd)
            btn.grid(
                row=row_idx,
                column=col_idx,
                padx=pad,
                pady=pad,
                sticky="nsew",
            )

    # ------------------------------------------------------------------
    # Display update
    # ------------------------------------------------------------------

    def _update_display(self) -> None:
        """Refresh the display label to show the current ``_display_value``."""
        self._display_label.config(text=self._display_value)

    # ------------------------------------------------------------------
    # Button handlers — digits and decimal
    # ------------------------------------------------------------------

    def _on_digit(self, digit: str) -> None:
        """Append a digit character to the current display value.

        If ``_is_new_number`` is True the digit replaces the display entirely
        (starting fresh), otherwise it is appended.

        Args:
            digit: Single-character digit string ("0"–"9").
        """
        if self._is_new_number:
            self._display_value = digit
            self._is_new_number = False
        else:
            # Prevent multiple leading zeros (e.g. "007")
            if self._display_value == "0":
                self._display_value = digit
            else:
                self._display_value += digit
        self._update_display()

    def _on_decimal(self) -> None:
        """Add a decimal point to the current number if one is not already present."""
        if self._is_new_number:
            self._display_value = "0."
            self._is_new_number = False
        elif "." not in self._display_value:
            self._display_value += "."
        self._update_display()

    # ------------------------------------------------------------------
    # Button handlers — operators and equals
    # ------------------------------------------------------------------

    def _on_operator(self, op_symbol: str) -> None:
        """Handle an operator button press.

        For binary operators (+, −, ×, ÷, xʸ):
          - If there is already a pending binary operator and a first operand,
            execute the pending operation first (chaining).
          - Store the current display value as the first operand.
          - Store the operator symbol and set ``_is_new_number = True`` so the
            next digit starts a new number.

        For unary operators (√, x², n!, ln, log, sin, cos, tan):
          - Execute immediately on the current display value.
          - Record in history.
          - Show the result.

        Args:
            op_symbol: The operator symbol string from the button label.
        """
        if op_symbol in _UNARY_OPERATORS:
            self._execute_unary(op_symbol)
            return

        # Binary operator path
        current = self._display_value
        try:
            current_float = float(current)
        except ValueError:
            self._display_value = "Error"
            self._update_display()
            self._is_new_number = True
            return

        if self._pending_operator is not None and not self._is_new_number:
            # Chain: execute the pending binary operation first
            self._execute_pending()
        else:
            self._accumulated_value = current_float

        self._pending_operator = op_symbol
        self._is_new_number = True

    def _on_equals(self) -> None:
        """Execute the pending binary operation and display the result.

        If no pending operator is set, the display is left unchanged.
        The result is recorded in session history.
        """
        if self._pending_operator is None:
            return

        self._execute_pending()
        self._pending_operator = None

    def _execute_pending(self) -> None:
        """Execute the currently pending binary operation and update internal state.

        Reads ``_accumulated_value`` as the first operand and the current
        ``_display_value`` as the second operand.  Calls the appropriate
        :class:`~operations.OperationRegistry` method and stores the result
        back into ``_accumulated_value`` and ``_display_value``.

        If any arithmetic or validation error occurs the display shows "Error"
        and state is reset.
        """
        if self._pending_operator is None or self._accumulated_value is None:
            return

        try:
            second = float(self._display_value)
        except ValueError:
            self._display_value = "Error"
            self._update_display()
            self._is_new_number = True
            self._pending_operator = None
            self._accumulated_value = None
            return

        op_key = self._symbol_to_operation(self._pending_operator)
        try:
            method, _arity, _desc = self._registry.get_operation(op_key)
        except KeyError:
            self._display_value = "Error"
            self._update_display()
            self._is_new_number = True
            self._pending_operator = None
            self._accumulated_value = None
            return

        operands: list[float | int]
        if op_key == "factorial":
            first_int = int(self._accumulated_value)
            operands = [first_int]
        else:
            operands = [self._accumulated_value, second]

        try:
            result: float = method(*operands)
        except (ValueError, ZeroDivisionError, ArithmeticError, TypeError) as exc:
            self._display_value = str(exc)
            self._update_display()
            self._is_new_number = True
            self._pending_operator = None
            self._accumulated_value = None
            return

        self._history.record_operation(op_key, operands, result)

        # Format result: remove trailing ".0" for whole-number results
        result_str = self._format_result(result)
        self._display_value = result_str
        self._accumulated_value = result
        self._is_new_number = True
        self._update_display()

    def _execute_unary(self, op_symbol: str) -> None:
        """Execute a unary operation on the current display value immediately.

        Args:
            op_symbol: Symbol string corresponding to a unary operator.
        """
        try:
            value = float(self._display_value)
        except ValueError:
            self._display_value = "Error"
            self._update_display()
            self._is_new_number = True
            return

        op_key = self._symbol_to_operation(op_symbol)

        try:
            method, _arity, _desc = self._registry.get_operation(op_key)
        except KeyError:
            self._display_value = "Error"
            self._update_display()
            self._is_new_number = True
            return

        operand: int | float
        if op_key == "factorial":
            operand = int(value)
        else:
            operand = value

        try:
            result: float = method(operand)
        except (ValueError, ZeroDivisionError, ArithmeticError, TypeError) as exc:
            self._display_value = str(exc)
            self._update_display()
            self._is_new_number = True
            return

        self._history.record_operation(op_key, [operand], result)
        self._display_value = self._format_result(result)
        self._accumulated_value = result
        self._is_new_number = True
        self._update_display()

    # ------------------------------------------------------------------
    # Button handlers — clear, delete, mode
    # ------------------------------------------------------------------

    def _on_clear(self) -> None:
        """Reset the display and all internal calculator state to initial values."""
        self._display_value = "0"
        self._accumulated_value = None
        self._pending_operator = None
        self._is_new_number = True
        self._update_display()

    def _on_delete(self) -> None:
        """Remove the last character from the current display value.

        If only one character remains (or the display shows a result / error),
        the display is reset to "0".
        """
        if self._is_new_number:
            # After an operator press or completed computation, Del clears to 0
            self._display_value = "0"
            self._is_new_number = False
            self._update_display()
            return

        if len(self._display_value) <= 1:
            self._display_value = "0"
        else:
            self._display_value = self._display_value[:-1]
        self._update_display()

    def _on_mode_switch(self) -> None:
        """Toggle between Normal and Scientific modes.

        Shows or hides the scientific panel frame and updates the ModeManager.
        """
        self._mode_manager.switch_mode()
        from .mode_manager import CalculatorMode
        if self._mode_manager.get_current_mode() is CalculatorMode.SCIENTIFIC:
            self._scientific_frame.pack(side=tk.LEFT, before=self._standard_frame)
        else:
            self._scientific_frame.pack_forget()

    # ------------------------------------------------------------------
    # Helper utilities
    # ------------------------------------------------------------------

    @staticmethod
    def _symbol_to_operation(symbol: str) -> str:
        """Map a button symbol string to the operation key used by OperationRegistry.

        Args:
            symbol: Display symbol such as "÷", "×", "√", etc.

        Returns:
            The string key understood by :class:`~operations.OperationRegistry`
            (e.g. ``"divide"``, ``"multiply"``, ``"square_root"``).

        Raises:
            KeyError: If the symbol has no mapping (should not happen in normal
                operation as the button set is fixed).
        """
        return _SYMBOL_TO_KEY[symbol]

    @staticmethod
    def _format_result(value: float) -> str:
        """Format a numeric result for display, stripping unnecessary decimals.

        Args:
            value: The numeric result to format.

        Returns:
            A string representation: integer form if the value is a whole
            number, otherwise the default float representation.
        """
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)

    # ------------------------------------------------------------------
    # Run
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the tkinter main event loop."""
        self.root.mainloop()
