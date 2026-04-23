"""Tkinter-based iOS-inspired GUI for the calculator application.

This module provides :class:`CalculatorGUI`, a fully self-contained graphical
interface styled after iOS calculator aesthetics. It wires together
:class:`~calculator.Calculator` and :class:`~session_history.SessionHistory`
for arithmetic execution and history recording.

It intentionally avoids importing ``InputHandler``, ``OperationHistory``, or
``CalculatorWorkflow`` — those are CLI/workflow concerns that do not belong in
the GUI layer.
"""

import tkinter as tk

from .calculator import Calculator
from .session_history import SessionHistory


# ---------------------------------------------------------------------------
# Color constants
# ---------------------------------------------------------------------------

BG_COLOR = "#000000"
BTN_STANDARD = "#333333"   # numeric (0-9), Del, C
BTN_OPERATOR = "#FF9500"   # +, −, ×, ÷
BTN_UTILITY = "#A5A5A5"    # Mode, =
DISPLAY_FG = "#FFFFFF"


class CalculatorGUI:
    """iOS-inspired graphical calculator interface built with tkinter.

    The GUI presents a display and a standard button grid laid out in the
    style of iOS Calculator.  A scientific panel can be shown or hidden via
    the Mode button.  Arithmetic is delegated to :class:`~calculator.Calculator`
    and results are recorded in :class:`~session_history.SessionHistory`.

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
        """Initialise the GUI, engine components, and build all widgets.

        Args:
            root: The top-level Tk window.
            history: Session history instance for recording operations.
        """
        self.root: tk.Tk = root
        self.root.title("Calculator")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self._history: SessionHistory = history
        self._calc: Calculator = Calculator()

        # ---- Internal state ----
        self._display_var: tk.StringVar = tk.StringVar(value="0")
        self._first_operand: float | None = None
        self._pending_op: str | None = None
        self._reset_display: bool = False
        self._scientific_visible: bool = False

        self._build_widgets()

    # ------------------------------------------------------------------
    # Widget construction
    # ------------------------------------------------------------------

    def _build_widgets(self) -> None:
        """Build display, standard grid, and scientific panel."""
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # ---- Display frame (spans full width) ----
        display_frame = tk.Frame(main_frame, bg=BG_COLOR)
        display_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=4, pady=(8, 4))
        display_frame.columnconfigure(0, weight=1)

        self._display_label = tk.Label(
            display_frame,
            textvariable=self._display_var,
            font=("Helvetica", 28),
            fg=DISPLAY_FG,
            bg=BG_COLOR,
            anchor="e",
            padx=8,
            pady=4,
        )
        self._display_label.grid(row=0, column=0, sticky="ew")

        # ---- Buttons frame: scientific panel (left) + standard grid (right) ----
        buttons_frame = tk.Frame(main_frame, bg=BG_COLOR)
        buttons_frame.grid(row=1, column=0, sticky="nsew", padx=4, pady=(0, 4))

        # Scientific panel (initially hidden)
        self._sci_frame = tk.Frame(buttons_frame, bg=BG_COLOR)
        self._sci_frame.grid(row=0, column=0, sticky="ns", padx=(0, 4))
        self._sci_frame.grid_remove()

        # Standard grid frame
        self._std_frame = tk.Frame(buttons_frame, bg=BG_COLOR)
        self._std_frame.grid(row=0, column=1, sticky="nsew")

        self._build_scientific_panel(self._sci_frame)
        self._build_standard_grid(self._std_frame)

    def _make_button(
        self,
        parent: tk.Frame,
        text: str,
        bg: str,
        command,
        columnspan: int = 1,
    ) -> tk.Button:
        """Create and return a styled calculator button.

        Args:
            parent: The parent frame to place the button in.
            text: The label displayed on the button.
            bg: The background color hex string.
            command: The callback to invoke on click.
            columnspan: How many columns the button should span (default 1).

        Returns:
            The configured :class:`tk.Button` widget.
        """
        return tk.Button(
            parent,
            text=text,
            bg=bg,
            fg=DISPLAY_FG,
            font=("Helvetica", 18, "bold"),
            relief="flat",
            borderwidth=0,
            width=4,
            height=2,
            activebackground=bg,
            activeforeground=DISPLAY_FG,
            command=command,
        )

    def _build_standard_grid(self, parent: tk.Frame) -> None:
        """Build the 4-column × 5-row standard button grid.

        Layout::

            Row 0: C        Del     Mode    ÷
            Row 1: 7        8       9       ×
            Row 2: 4        5       6       +
            Row 3: 1        2       3       −
            Row 4: 0 (span=2)       .       =

        Args:
            parent: The frame that contains the standard button grid.
        """
        # Row 0: C, Del, Mode, ÷
        btns_row0 = [
            ("C",    BTN_STANDARD, lambda: self._on_clear()),
            ("Del",  BTN_STANDARD, lambda: self._on_delete()),
            ("Mode", BTN_UTILITY,  lambda: self._on_mode_toggle()),
            ("÷",    BTN_OPERATOR, lambda: self._on_operator("÷")),
        ]
        for col, (text, color, cmd) in enumerate(btns_row0):
            btn = self._make_button(parent, text, color, cmd)
            btn.grid(row=0, column=col, padx=1, pady=1)

        # Row 1: 7, 8, 9, ×
        btns_row1 = [
            ("7", BTN_STANDARD, lambda: self._on_digit("7")),
            ("8", BTN_STANDARD, lambda: self._on_digit("8")),
            ("9", BTN_STANDARD, lambda: self._on_digit("9")),
            ("×", BTN_OPERATOR, lambda: self._on_operator("×")),
        ]
        for col, (text, color, cmd) in enumerate(btns_row1):
            btn = self._make_button(parent, text, color, cmd)
            btn.grid(row=1, column=col, padx=1, pady=1)

        # Row 2: 4, 5, 6, +
        btns_row2 = [
            ("4", BTN_STANDARD, lambda: self._on_digit("4")),
            ("5", BTN_STANDARD, lambda: self._on_digit("5")),
            ("6", BTN_STANDARD, lambda: self._on_digit("6")),
            ("+", BTN_OPERATOR, lambda: self._on_operator("+")),
        ]
        for col, (text, color, cmd) in enumerate(btns_row2):
            btn = self._make_button(parent, text, color, cmd)
            btn.grid(row=2, column=col, padx=1, pady=1)

        # Row 3: 1, 2, 3, −
        btns_row3 = [
            ("1", BTN_STANDARD, lambda: self._on_digit("1")),
            ("2", BTN_STANDARD, lambda: self._on_digit("2")),
            ("3", BTN_STANDARD, lambda: self._on_digit("3")),
            ("−", BTN_OPERATOR, lambda: self._on_operator("−")),
        ]
        for col, (text, color, cmd) in enumerate(btns_row3):
            btn = self._make_button(parent, text, color, cmd)
            btn.grid(row=3, column=col, padx=1, pady=1)

        # Row 4: 0 (colspan=2), ., =
        btn_zero = self._make_button(parent, "0", BTN_STANDARD, lambda: self._on_digit("0"))
        btn_zero.configure(width=9)
        btn_zero.grid(row=4, column=0, columnspan=2, padx=1, pady=1, sticky="ew")

        btn_dot = self._make_button(parent, ".", BTN_STANDARD, lambda: self._on_decimal())
        btn_dot.grid(row=4, column=2, padx=1, pady=1)

        btn_eq = self._make_button(parent, "=", BTN_UTILITY, lambda: self._on_equals())
        btn_eq.grid(row=4, column=3, padx=1, pady=1)

    def _build_scientific_panel(self, parent: tk.Frame) -> None:
        """Build the 2-column × 3-row scientific function panel.

        Functions laid out as::

            Row 0: √    x²
            Row 1: xʸ   n!
            Row 2: ln   log

        Args:
            parent: The frame that hosts the scientific panel buttons.
        """
        sci_buttons = [
            ("√",   lambda: self._on_scientific("√")),
            ("x²",  lambda: self._on_scientific("x²")),
            ("xʸ",  lambda: self._on_scientific("xʸ")),
            ("n!",  lambda: self._on_scientific("n!")),
            ("ln",  lambda: self._on_scientific("ln")),
            ("log", lambda: self._on_scientific("log")),
        ]
        for index, (text, cmd) in enumerate(sci_buttons):
            row = index // 2
            col = index % 2
            btn = self._make_button(parent, text, BTN_STANDARD, cmd)
            btn.grid(row=row, column=col, padx=1, pady=1)

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def _set_display(self, value: str) -> None:
        """Set the display to an arbitrary string value.

        Args:
            value: The string to show on the display.
        """
        self._display_var.set(value)

    def _get_display(self) -> str:
        """Return the current display string.

        Returns:
            The text currently shown on the display.
        """
        return self._display_var.get()

    def _format_result(self, value: float) -> str:
        """Format a float result for display, removing unnecessary trailing zeros.

        Args:
            value: The numeric result to format.

        Returns:
            A string representation, using integer notation when the value is
            whole (e.g. ``3.0`` becomes ``"3"``).
        """
        if value == int(value) and not ("e" in str(value).lower()):
            return str(int(value))
        return str(value)

    # ------------------------------------------------------------------
    # Button handlers
    # ------------------------------------------------------------------

    def _on_digit(self, digit: str) -> None:
        """Append a digit to the display, respecting the reset-display flag.

        When ``_reset_display`` is ``True`` (set after an operator is pressed),
        the display is cleared before the new digit is appended, so the user
        starts entering the second operand fresh.

        Args:
            digit: A single character string ``"0"``–``"9"``.
        """
        current = self._get_display()
        if self._reset_display:
            self._set_display(digit)
            self._reset_display = False
            return

        if current == "0":
            self._set_display(digit)
        else:
            self._set_display(current + digit)

    def _on_decimal(self) -> None:
        """Append a decimal point if one is not already present.

        If ``_reset_display`` is active, starts a fresh ``"0."`` entry.
        """
        if self._reset_display:
            self._set_display("0.")
            self._reset_display = False
            return

        current = self._get_display()
        if "." not in current:
            self._set_display(current + ".")

    def _on_operator(self, op: str) -> None:
        """Store the current display as the first operand and record the operator.

        If a previous operator is pending, it is evaluated first so that
        chained operations (e.g. ``3 + 4 × …``) resolve left-to-right.

        Args:
            op: One of ``"+"``, ``"−"``, ``"×"``, ``"÷"``.
        """
        if self._pending_op is not None and not self._reset_display:
            # Evaluate the chain before storing the new operator.
            self._evaluate()

        try:
            self._first_operand = float(self._get_display())
        except ValueError:
            self._set_display("Error")
            return

        self._pending_op = op
        self._reset_display = True

    def _on_equals(self) -> None:
        """Evaluate the pending operation and show the result.

        Delegates to :meth:`_evaluate` and then resets pending state so
        subsequent digit presses start a new number.
        """
        self._evaluate()
        # After equals, the next digit should start fresh.
        self._first_operand = None
        self._pending_op = None

    def _on_clear(self) -> None:
        """Reset the display to ``"0"`` and clear all pending state."""
        self._set_display("0")
        self._first_operand = None
        self._pending_op = None
        self._reset_display = False

    def _on_delete(self) -> None:
        """Remove the last character from the display.

        If only one character remains (or the display shows an error/zero),
        the display is reset to ``"0"``.
        """
        current = self._get_display()
        if current in ("Error", "0") or len(current) <= 1:
            self._set_display("0")
        else:
            self._set_display(current[:-1])

    def _on_mode_toggle(self) -> None:
        """Show or hide the scientific panel on the left side of the calculator."""
        self._scientific_visible = not self._scientific_visible
        if self._scientific_visible:
            self._sci_frame.grid()
        else:
            self._sci_frame.grid_remove()

    def _on_scientific(self, func: str) -> None:
        """Apply a scientific function to the current display value.

        For unary functions (``√``, ``x²``, ``n!``, ``ln``, ``log``), the
        current display value is used directly as the operand.  For ``xʸ``
        (power), the current display value is stored as the base and the
        operator state is set so the user can enter the exponent next.

        Args:
            func: One of ``"√"``, ``"x²"``, ``"xʸ"``, ``"n!"``, ``"ln"``,
                ``"log"``.
        """
        try:
            x = float(self._get_display())
        except ValueError:
            self._set_display("Error")
            return

        if func == "xʸ":
            # Binary: treat like an operator — store base, wait for exponent.
            self._first_operand = x
            self._pending_op = "xʸ"
            self._reset_display = True
            return

        try:
            if func == "√":
                result = self._calc.square_root(x)
                self._history.record_operation("square_root", [x], result)
            elif func == "x²":
                result = self._calc.square(x)
                self._history.record_operation("square", [x], result)
            elif func == "n!":
                if x != int(x) or x < 0:
                    self._set_display("Error")
                    return
                result = float(self._calc.factorial(int(x)))
                self._history.record_operation("factorial", [int(x)], result)
            elif func == "ln":
                result = self._calc.ln(x)
                self._history.record_operation("ln", [x], result)
            elif func == "log":
                result = self._calc.log(x)
                self._history.record_operation("log", [x], result)
            else:
                self._set_display("Error")
                return
        except (ValueError, ZeroDivisionError, ArithmeticError, OverflowError) as exc:  # noqa: F841
            self._set_display("Error")
            return

        self._set_display(self._format_result(result))
        self._reset_display = True

    # ------------------------------------------------------------------
    # Core evaluation
    # ------------------------------------------------------------------

    def _evaluate(self) -> None:
        """Evaluate the pending binary operation and update the display.

        Uses ``_first_operand`` as the left operand and the current display
        value as the right operand.  Results are recorded in
        :class:`~session_history.SessionHistory`.  Any arithmetic or value
        error is caught and ``"Error"`` is shown on the display.
        """
        if self._pending_op is None or self._first_operand is None:
            return

        try:
            second_operand = float(self._get_display())
        except ValueError:
            self._set_display("Error")
            self._reset_display = True
            return

        a = self._first_operand
        b = second_operand
        op = self._pending_op

        try:
            if op == "+":
                result = self._calc.add(a, b)
                self._history.record_operation("add", [a, b], result)
            elif op == "−":
                result = self._calc.subtract(a, b)
                self._history.record_operation("subtract", [a, b], result)
            elif op == "×":
                result = self._calc.multiply(a, b)
                self._history.record_operation("multiply", [a, b], result)
            elif op == "÷":
                result = self._calc.divide(a, b)
                self._history.record_operation("divide", [a, b], result)
            elif op == "xʸ":
                result = self._calc.power(a, b)
                self._history.record_operation("power", [a, b], result)
            else:
                self._set_display("Error")
                self._reset_display = True
                return
        except (ValueError, ZeroDivisionError, ArithmeticError, OverflowError):
            self._set_display("Error")
            self._reset_display = True
            return

        self._set_display(self._format_result(result))
        self._reset_display = True
        self._first_operand = float(self._format_result(result))

    # ------------------------------------------------------------------
    # Run
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the tkinter main event loop."""
        self.root.mainloop()
