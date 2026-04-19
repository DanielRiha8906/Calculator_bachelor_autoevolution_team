"""Tkinter-based GUI for the Calculator application.

This module provides GuiCalculator, a graphical iOS-style user interface that
exposes the same operation set as the interactive CLI session, with mode
toggling (Normal / Scientific) via a single toggle button, a display label
that shows the current operand or result, and a button-driven digit and
operation input flow.

Typical usage::

    import tkinter as tk
    from src.core.calculator import Calculator
    from src.interface.gui import GuiCalculator

    root = tk.Tk()
    gui = GuiCalculator(root, Calculator())
    gui.run()
"""

from __future__ import annotations

_THEME = {
    "bg": "#000000",
    "display_bg": "#000000",
    "display_fg": "#FFFFFF",
    "display_font": ("Courier", 32, "bold"),
    "btn_digit_bg": "#333333",
    "btn_digit_fg": "#FFFFFF",
    "btn_op_bg": "#333333",
    "btn_op_fg": "#FFFFFF",
    "btn_binary_bg": "#FF9500",
    "btn_binary_fg": "#FFFFFF",
    "btn_utility_bg": "#A5A5A5",
    "btn_utility_fg": "#FFFFFF",
    "btn_font": ("Helvetica", 18),
    "btn_relief": "flat",
    "btn_borderwidth": 0,
}

try:
    import tkinter as tk
    import tkinter.messagebox as messagebox
except ImportError as _tk_err:  # noqa: F841
    # tkinter is a system-level optional dependency (not available in all
    # environments, e.g. headless CI).  The module can still be imported
    # safely; only GuiCalculator.__init__ / run() will raise at call time
    # if the runtime truly lacks a display.
    tk = None  # type: ignore[assignment]
    messagebox = None  # type: ignore[assignment]

from ..core.calculator import Calculator
from ..shared.dispatcher import OperationDispatcher
from ..shared.logger import Logger
from ..operations import OPERATIONS
from ..session.history import History
from ..session.mode import Mode
from ..session.base_mode import BaseMode

# Keys that are binary operations (store first operand, wait for second).
_BINARY_OP_KEYS: frozenset[str] = frozenset(
    {"add", "subtract", "multiply", "divide", "power"}
)

# Keys that are utility/modifier buttons.
_UTILITY_OP_KEYS: frozenset[str] = frozenset({"clear", "negate", "percent"})


class GuiCalculator:
    """Tkinter-based iOS-style graphical calculator interface.

    Displays a numeric digit pad and an operation column.  A single toggle
    button switches between Normal and Scientific mode.  Binary operations
    (add, subtract, multiply, divide, power) store the first operand and
    wait for the equals button; unary operations execute immediately on the
    current display value.

    All calculation logic is delegated to the injected Calculator instance
    via OperationDispatcher; no operation logic is duplicated here.

    Args:
        root: The root Tk window to build the UI inside.
        calculator: A Calculator instance used for all computations.
        logger: Optional Logger for error logging.  When None, a Logger is
            created lazily on the first operation execution.
    """

    def __init__(
        self,
        root: object,
        calculator: Calculator,
        logger: Logger | None = None,
    ) -> None:
        if tk is None:
            raise ImportError(
                "tkinter is not available in this environment. "
                "Install the python3-tk system package to use GuiCalculator."
            )
        self._root = root
        self._root.title("Calculator")  # type: ignore[attr-defined]
        self._root.configure(bg=_THEME["bg"])  # type: ignore[attr-defined]
        self._calculator = calculator
        self._logger: Logger | None = logger
        self._dispatcher = OperationDispatcher(calculator)
        self._history = History()
        self._mode: Mode = Mode.NORMAL
        self._mode_handler = BaseMode()

        # Display state
        self._display_value: str = "0"
        self._first_operand: float | None = None
        self._pending_op_key: str | None = None
        self._last_was_operator: bool = False

        # Widget references populated by _setup_layout.
        self._display_label: tk.Label | None = None
        self._mode_toggle_btn: tk.Button | None = None
        self._op_frame: tk.Frame | None = None

        self._setup_layout()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Enter the Tk main-event loop.

        Blocks until the user closes the window.
        """
        self._root.mainloop()

    # ------------------------------------------------------------------
    # Layout setup
    # ------------------------------------------------------------------

    def _setup_layout(self) -> None:
        """Build and grid all top-level frames and widgets.

        Layout (top to bottom):
        1. Display label — full-width, right-anchored, large monospaced font.
        2. Mode toggle button — switches between Normal and Scientific.
        3. Button grid — digit pad (left) and operation buttons (right).
        """
        self._root.columnconfigure(0, weight=1)  # type: ignore[attr-defined]

        # --- Display label ---
        self._display_label = tk.Label(
            self._root,
            text=self._display_value,
            anchor="e",
            font=_THEME["display_font"],
            bg=_THEME["display_bg"],
            fg=_THEME["display_fg"],
            padx=12,
            pady=8,
        )
        self._display_label.grid(row=0, column=0, sticky="ew")

        # --- Mode toggle button ---
        toggle_text = "Scientific" if self._mode == Mode.NORMAL else "Normal"
        self._mode_toggle_btn = tk.Button(
            self._root,
            text=toggle_text,
            bg=_THEME["btn_utility_bg"],
            fg=_THEME["btn_utility_fg"],
            font=_THEME["btn_font"],
            relief=_THEME["btn_relief"],
            borderwidth=_THEME["btn_borderwidth"],
            command=self._on_mode_toggle_click,
        )
        self._mode_toggle_btn.grid(row=1, column=0, sticky="ew", padx=4, pady=2)

        # --- Combined button grid frame ---
        grid_frame = tk.Frame(self._root, bg=_THEME["bg"])
        grid_frame.grid(row=2, column=0, sticky="nsew")
        grid_frame.columnconfigure(0, weight=3)
        grid_frame.columnconfigure(1, weight=2)

        # --- Digit pad (left) ---
        digit_frame = tk.Frame(grid_frame, bg=_THEME["bg"])
        digit_frame.grid(row=0, column=0, sticky="nsew", padx=(4, 2), pady=4)
        self._build_digit_pad(digit_frame)

        # --- Operation buttons (right) ---
        self._op_frame = tk.Frame(grid_frame, bg=_THEME["bg"])
        self._op_frame.grid(row=0, column=1, sticky="nsew", padx=(2, 4), pady=4)
        self._build_operation_buttons()

    def _build_digit_pad(self, parent: tk.Frame) -> None:
        """Build the 3-column x 4-row digit button grid in *parent*.

        Digit layout::

            row 0 : 7  8  9
            row 1 : 4  5  6
            row 2 : 1  2  3
            row 3 : 0  (spans all 3 columns)

        Args:
            parent: Frame that will contain the digit buttons.
        """
        rows = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
        ]
        for r, row_digits in enumerate(rows):
            for c, digit in enumerate(row_digits):
                btn = tk.Button(
                    parent,
                    text=digit,
                    bg=_THEME["btn_digit_bg"],
                    fg=_THEME["btn_digit_fg"],
                    font=_THEME["btn_font"],
                    relief=_THEME["btn_relief"],
                    borderwidth=_THEME["btn_borderwidth"],
                    command=lambda d=digit: self._on_digit_click(d),
                )
                btn.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

        # Row 3: "0" spanning all three columns
        btn_zero = tk.Button(
            parent,
            text="0",
            bg=_THEME["btn_digit_bg"],
            fg=_THEME["btn_digit_fg"],
            font=_THEME["btn_font"],
            relief=_THEME["btn_relief"],
            borderwidth=_THEME["btn_borderwidth"],
            command=lambda: self._on_digit_click("0"),
        )
        btn_zero.grid(row=3, column=0, columnspan=3, padx=2, pady=2, sticky="nsew")

        for c in range(3):
            parent.columnconfigure(c, weight=1)
        for r in range(4):
            parent.rowconfigure(r, weight=1)

    def _build_operation_buttons(self) -> None:
        """Populate the operation button column for the current mode.

        Clears any previously rendered buttons before rebuilding.  Includes
        the equals (=) and clear buttons in addition to the mode operations.
        """
        if self._op_frame is None:
            return

        for widget in self._op_frame.winfo_children():
            widget.destroy()

        available = self._get_available_operations_for_mode()

        row = 0

        # Clear button (utility)
        btn_clear = tk.Button(
            self._op_frame,
            text="C",
            bg=_THEME["btn_utility_bg"],
            fg=_THEME["btn_utility_fg"],
            font=_THEME["btn_font"],
            relief=_THEME["btn_relief"],
            borderwidth=_THEME["btn_borderwidth"],
            command=self._on_clear_click,
        )
        btn_clear.grid(row=row, column=0, padx=2, pady=2, sticky="nsew")
        row += 1

        # Operation buttons from the current mode
        for op_key, op_info in available.items():
            label: str = op_info["label"]
            # Use a short display label for the button
            btn_text = self._short_label(op_key, label)
            bg, fg = self._op_button_colors(op_key)
            if op_key in _BINARY_OP_KEYS:
                cmd = lambda k=op_key: self._on_binary_op_click(k)
            else:
                cmd = lambda k=op_key: self._on_unary_op_click(k)

            btn = tk.Button(
                self._op_frame,
                text=btn_text,
                bg=bg,
                fg=fg,
                font=_THEME["btn_font"],
                relief=_THEME["btn_relief"],
                borderwidth=_THEME["btn_borderwidth"],
                command=cmd,
            )
            btn.grid(row=row, column=0, padx=2, pady=2, sticky="nsew")
            row += 1

        # Equals button (binary)
        btn_eq = tk.Button(
            self._op_frame,
            text="=",
            bg=_THEME["btn_binary_bg"],
            fg=_THEME["btn_binary_fg"],
            font=_THEME["btn_font"],
            relief=_THEME["btn_relief"],
            borderwidth=_THEME["btn_borderwidth"],
            command=self._on_equals_click,
        )
        btn_eq.grid(row=row, column=0, padx=2, pady=2, sticky="nsew")
        row += 1

        self._op_frame.columnconfigure(0, weight=1)
        for r in range(row):
            self._op_frame.rowconfigure(r, weight=1)

    # ------------------------------------------------------------------
    # Button label helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _short_label(op_key: str, label: str) -> str:  # noqa: ARG004
        """Return a concise button label for *op_key*.

        Args:
            op_key: The operation registry key.
            label: The full human-readable label from the registry.

        Returns:
            A short string suitable for display on a small button.
        """
        _SHORT: dict[str, str] = {
            "add": "+",
            "subtract": "−",
            "multiply": "×",
            "divide": "÷",
            "power": "xʸ",
            "factorial": "n!",
            "square": "x²",
            "cube": "x³",
            "square_root": "√",
            "cube_root": "∛",
            "log10": "log",
            "ln": "ln",
            "sin": "sin",
            "cos": "cos",
            "tan": "tan",
            "asin": "asin",
            "acos": "acos",
            "atan": "atan",
            "pi": "π",
            "e": "e",
            "negate": "+/−",
            "percent": "%",
        }
        return _SHORT.get(op_key, op_key)

    @staticmethod
    def _op_button_colors(op_key: str) -> tuple[str, str]:
        """Return (bg, fg) color pair for *op_key* based on its category.

        Args:
            op_key: The operation registry key.

        Returns:
            A (background_color, foreground_color) tuple from ``_THEME``.
        """
        if op_key in _BINARY_OP_KEYS:
            return _THEME["btn_binary_bg"], _THEME["btn_binary_fg"]
        if op_key in _UTILITY_OP_KEYS:
            return _THEME["btn_utility_bg"], _THEME["btn_utility_fg"]
        return _THEME["btn_op_bg"], _THEME["btn_op_fg"]

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_digit_click(self, digit: str) -> None:
        """Handle a digit button press.

        Resets the display when the previous action was an operator or when the
        display currently shows the initial zero.  Otherwise appends *digit* to
        the current display string.

        Args:
            digit: A single character string "0"–"9".
        """
        if self._last_was_operator or self._display_value == "0":
            self._display_value = digit
        else:
            self._display_value += digit
        self._last_was_operator = False
        self._update_display()

    def _on_binary_op_click(self, op_key: str) -> None:
        """Handle a binary operator button press.

        Stores the current display value as the first operand and records
        which operator is pending.  The operation is not executed until the
        equals button is pressed.

        Args:
            op_key: The binary operation key (e.g. "add", "multiply").
        """
        try:
            self._first_operand = float(self._display_value)
        except ValueError:
            self._display_value = "Error"
            self._update_display()
            return
        self._pending_op_key = op_key
        self._last_was_operator = True

    def _on_unary_op_click(self, op_key: str) -> None:
        """Handle a unary operator button press.

        Executes the operation immediately against the current display value
        and updates the display with the result.

        Args:
            op_key: The unary operation key (e.g. "square", "ln").
        """
        op_info = OPERATIONS.get(op_key, {})
        arity: int = op_info.get("arity", 1)

        if arity == 0:
            operands: list = []
        else:
            try:
                operands = [float(self._display_value)]
            except ValueError:
                self._display_value = "Error"
                self._update_display()
                return

        if self._logger is None:
            self._logger = Logger()

        try:
            result = self._dispatcher.dispatch(op_key, operands)
        except (ZeroDivisionError, ValueError, TypeError, ArithmeticError) as exc:
            if self._logger is not None:
                self._logger.log_domain_error(op_key, str(exc))
            self._display_value = "Error"
            self._first_operand = None
            self._pending_op_key = None
            self._last_was_operator = False
            self._update_display()
            return

        self._display_value = self._format_result(result)
        self._last_was_operator = True
        self._update_display()

    def _on_equals_click(self) -> None:
        """Handle the equals button press.

        Executes the pending binary operation using the stored first operand
        and the current display value as the second operand.  Resets the
        pending operation state after execution.
        """
        if self._pending_op_key is None or self._first_operand is None:
            return

        try:
            second_operand = float(self._display_value)
        except ValueError:
            self._display_value = "Error"
            self._update_display()
            return

        if self._logger is None:
            self._logger = Logger()

        try:
            result = self._dispatcher.dispatch(
                self._pending_op_key,
                [self._first_operand, second_operand],
            )
        except (ZeroDivisionError, ValueError, TypeError, ArithmeticError) as exc:
            if self._logger is not None:
                self._logger.log_domain_error(self._pending_op_key, str(exc))
            self._display_value = "Error"
            self._first_operand = None
            self._pending_op_key = None
            self._last_was_operator = False
            self._update_display()
            return

        self._display_value = self._format_result(result)
        self._pending_op_key = None
        self._first_operand = None
        self._last_was_operator = True
        self._update_display()

    def _on_clear_click(self) -> None:
        """Handle the clear (C) button press.

        Resets all display and operation state to initial values.
        """
        self._display_value = "0"
        self._first_operand = None
        self._pending_op_key = None
        self._last_was_operator = False
        self._update_display()

    def _on_mode_toggle_click(self) -> None:
        """Handle the mode toggle button press.

        Switches between Normal and Scientific mode, resets all calculator
        state, rebuilds the operation button panel, and updates the toggle
        button label.
        """
        if self._mode == Mode.NORMAL:
            self._mode = Mode.SCIENTIFIC
            toggle_text = "Normal"
        else:
            self._mode = Mode.NORMAL
            toggle_text = "Scientific"

        self._on_clear_click()
        self._build_operation_buttons()

        if self._mode_toggle_btn is not None:
            self._mode_toggle_btn.configure(text=toggle_text)

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def _update_display(self) -> None:
        """Sync the display label widget to the current ``_display_value``."""
        if self._display_label is not None:
            self._display_label.config(text=self._display_value)

    @staticmethod
    def _format_result(result: float | int) -> str:
        """Format a numeric result for display.

        Integers (e.g. 39.0) are shown without a decimal point ("39").
        Non-integer floats are shown as their default string representation.

        Args:
            result: The numeric value to format.

        Returns:
            A human-readable string representation.
        """
        try:
            if result == int(result):
                return str(int(result))
        except (ValueError, OverflowError):
            pass
        return str(result)

    def _get_available_operations_for_mode(self) -> dict:
        """Return the operation dict filtered for the current mode.

        Delegates to the composed BaseMode instance.

        Returns:
            A dict mapping operation keys to registry entries accessible in
            the current mode.
        """
        return self._mode_handler.get_available_operations(self._mode)
