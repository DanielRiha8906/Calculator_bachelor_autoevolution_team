"""GUI layer — iOS-inspired dark calculator interface.

Provides a graphical front-end for the calculator application styled after
the iOS dark calculator.  All arithmetic is delegated to the existing
:class:`~src.calculator.Calculator` engine via
:func:`~src.input_loop.dispatch`.

The module exposes one public symbol:

* :class:`CalculatorGUI` — the main application window.
"""

from __future__ import annotations

import tkinter as tk
from typing import Optional

from .calculator import Calculator
from .input_loop import dispatch

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------

_BG = "#000000"
_BTN_DIGIT = "#333333"
_BTN_OPERATOR = "#FF9500"
_BTN_UTILITY = "#A5A5A5"
_FG = "#FFFFFF"

# ---------------------------------------------------------------------------
# Main application class
# ---------------------------------------------------------------------------


class CalculatorGUI:
    """iOS-inspired dark calculator GUI.

    Integrates with the existing :class:`~src.calculator.Calculator` without
    reimplementing any arithmetic logic.  Operations are executed via
    :func:`~src.input_loop.dispatch`.

    Attributes:
        _calc: The shared :class:`~src.calculator.Calculator` instance.
        _current_display: String currently shown in the display.
        _pending_operator: Operation key awaiting a second operand, or ``None``.
        _pending_operand: First operand captured when an operator was pressed.
        _decimal_entered: Whether the user has already typed a decimal point in
            the current number.
        _is_scientific_mode: When ``True`` the scientific button rows are shown.
        _result_just_shown: When ``True`` the next digit press starts a fresh
            number rather than appending to the current display.
    """

    def __init__(self) -> None:
        """Initialise the root window and all frames and widgets."""
        self._calc: Calculator = Calculator()

        # State machine attributes
        self._current_display: str = "0"
        self._pending_operator: Optional[str] = None
        self._pending_operand: Optional[float] = None
        self._decimal_entered: bool = False
        self._is_scientific_mode: bool = False
        self._result_just_shown: bool = False

        # Build window
        self._root = tk.Tk()
        self._root.title("Calculator")
        self._root.configure(bg=_BG)
        self._root.resizable(False, False)

        # Display label variable
        self._display_var = tk.StringVar(value=self._current_display)

        self._build_display()
        self._build_mode_toggle()
        self._build_button_grid()

    # ------------------------------------------------------------------
    # UI builders
    # ------------------------------------------------------------------

    def _build_display(self) -> None:
        """Create the large right-aligned result display at the top."""
        display_frame = tk.Frame(self._root, bg=_BG)
        display_frame.pack(fill="x", padx=8, pady=(16, 4))

        display_label = tk.Label(
            display_frame,
            textvariable=self._display_var,
            font=("Courier", 48, "bold"),
            bg=_BG,
            fg=_FG,
            anchor="e",
            justify="right",
            width=10,
        )
        display_label.pack(fill="x", padx=8)

    def _build_mode_toggle(self) -> None:
        """Create the Normal / Scientific mode toggle button below the display."""
        toggle_frame = tk.Frame(self._root, bg=_BG)
        toggle_frame.pack(fill="x", padx=8, pady=(0, 4))

        self._mode_btn = tk.Button(
            toggle_frame,
            text="Scientific",
            font=("Helvetica", 13),
            bg=_BTN_UTILITY,
            fg=_FG,
            activebackground=_BTN_UTILITY,
            activeforeground=_FG,
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=8,
            command=self._on_mode_toggle,
        )
        self._mode_btn.pack(side="left", padx=4, pady=2)

    def _build_button_grid(self) -> None:
        """Create the full button grid (normal + scientific rows)."""
        self._btn_frame = tk.Frame(self._root, bg=_BG)
        self._btn_frame.pack(fill="both", padx=8, pady=4)

        # ------------------------------------------------------------------
        # Helper: create a single button
        # ------------------------------------------------------------------
        def make_button(
            parent: tk.Widget,
            text: str,
            color: str,
            row: int,
            col: int,
            colspan: int = 1,
            command: Optional[object] = None,
        ) -> tk.Button:
            btn = tk.Button(
                parent,
                text=text,
                font=("Helvetica", 20, "bold"),
                bg=color,
                fg=_FG,
                activebackground=color,
                activeforeground=_FG,
                relief=tk.FLAT,
                bd=0,
                width=4 * colspan,
                height=2,
                command=command,
            )
            btn.grid(
                row=row,
                column=col,
                columnspan=colspan,
                padx=4,
                pady=4,
                sticky="nsew",
            )
            return btn

        # Row 0 — utility and divide
        make_button(self._btn_frame, "C",  _BTN_UTILITY,  0, 0, command=self._on_clear_pressed)
        make_button(self._btn_frame, "+/-", _BTN_UTILITY, 0, 1, command=self._on_negate_pressed)
        make_button(self._btn_frame, "%",   _BTN_UTILITY, 0, 2, command=self._on_percent_pressed)
        make_button(self._btn_frame, "÷",   _BTN_OPERATOR, 0, 3, command=lambda: self._on_operator_pressed("divide"))

        # Row 1 — 7, 8, 9, ×
        make_button(self._btn_frame, "7", _BTN_DIGIT,    1, 0, command=lambda: self._on_digit_pressed(7))
        make_button(self._btn_frame, "8", _BTN_DIGIT,    1, 1, command=lambda: self._on_digit_pressed(8))
        make_button(self._btn_frame, "9", _BTN_DIGIT,    1, 2, command=lambda: self._on_digit_pressed(9))
        make_button(self._btn_frame, "×", _BTN_OPERATOR, 1, 3, command=lambda: self._on_operator_pressed("multiply"))

        # Row 2 — 4, 5, 6, −
        make_button(self._btn_frame, "4", _BTN_DIGIT,    2, 0, command=lambda: self._on_digit_pressed(4))
        make_button(self._btn_frame, "5", _BTN_DIGIT,    2, 1, command=lambda: self._on_digit_pressed(5))
        make_button(self._btn_frame, "6", _BTN_DIGIT,    2, 2, command=lambda: self._on_digit_pressed(6))
        make_button(self._btn_frame, "−", _BTN_OPERATOR, 2, 3, command=lambda: self._on_operator_pressed("subtract"))

        # Row 3 — 1, 2, 3, +
        make_button(self._btn_frame, "1", _BTN_DIGIT,    3, 0, command=lambda: self._on_digit_pressed(1))
        make_button(self._btn_frame, "2", _BTN_DIGIT,    3, 1, command=lambda: self._on_digit_pressed(2))
        make_button(self._btn_frame, "3", _BTN_DIGIT,    3, 2, command=lambda: self._on_digit_pressed(3))
        make_button(self._btn_frame, "+", _BTN_OPERATOR, 3, 3, command=lambda: self._on_operator_pressed("add"))

        # Row 4 — 0 (colspan 2), ., =
        make_button(self._btn_frame, "0", _BTN_DIGIT,    4, 0, colspan=2, command=lambda: self._on_digit_pressed(0))
        make_button(self._btn_frame, ".", _BTN_DIGIT,    4, 2, command=self._on_decimal_pressed)
        make_button(self._btn_frame, "=", _BTN_OPERATOR, 4, 3, command=self._on_equals_pressed)

        # Configure grid columns to expand equally
        for col_idx in range(4):
            self._btn_frame.columnconfigure(col_idx, weight=1)

        # Scientific button rows (hidden until mode toggled)
        self._sci_frame = tk.Frame(self._root, bg=_BG)
        # Not packed yet — shown on mode toggle
        self._rebuild_scientific_buttons()

    def _rebuild_scientific_buttons(self) -> None:
        """(Re)populate the scientific button rows inside _sci_frame."""
        # Destroy any previously created children
        for widget in self._sci_frame.winfo_children():
            widget.destroy()

        def make_sci(
            text: str,
            row: int,
            col: int,
            key: str,
        ) -> tk.Button:
            btn = tk.Button(
                self._sci_frame,
                text=text,
                font=("Helvetica", 18, "bold"),
                bg=_BTN_DIGIT,
                fg=_FG,
                activebackground=_BTN_DIGIT,
                activeforeground=_FG,
                relief=tk.FLAT,
                bd=0,
                width=4,
                height=2,
                command=lambda k=key: self._on_unary_pressed(k),
            )
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
            return btn

        # Row 5 (relative row 0 inside sci_frame)
        make_sci("√",  0, 0, "square_root")
        make_sci("x²", 0, 1, "square")
        make_sci("x³", 0, 2, "cube")
        make_sci("∛",  0, 3, "cube_root")

        # Row 6 (relative row 1 inside sci_frame)
        make_sci("n!", 1, 0, "factorial")
        make_sci("ln", 1, 1, "ln")
        make_sci("log", 1, 2, "log")

        for col_idx in range(4):
            self._sci_frame.columnconfigure(col_idx, weight=1)

    # ------------------------------------------------------------------
    # Display helper
    # ------------------------------------------------------------------

    def _update_display(self) -> None:
        """Push the current _current_display value to the tk StringVar."""
        self._display_var.set(self._current_display)

    @staticmethod
    def _format_result(value: float) -> str:
        """Return a clean string for *value*, dropping trailing '.0'.

        Args:
            value: The numeric result to format.

        Returns:
            ``"8"`` instead of ``"8.0"``; preserves decimals otherwise.
        """
        text = str(value)
        if text.endswith(".0"):
            return text[:-2]
        return text

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_digit_pressed(self, digit: int) -> None:
        """Handle a digit button (0–9) press.

        Args:
            digit: The integer digit that was pressed.
        """
        if self._result_just_shown or self._current_display == "0":
            self._current_display = str(digit)
            self._decimal_entered = False
        else:
            self._current_display += str(digit)
        self._result_just_shown = False
        self._update_display()

    def _on_decimal_pressed(self) -> None:
        """Handle the decimal point button press."""
        if self._result_just_shown:
            self._current_display = "0."
            self._decimal_entered = True
            self._result_just_shown = False
        elif not self._decimal_entered:
            self._current_display += "."
            self._decimal_entered = True
        self._update_display()

    def _on_operator_pressed(self, operator_key: str) -> None:
        """Handle an arithmetic operator button press.

        Captures the current display as the pending operand and stores the
        operator.  Does not clear the display — the display resets naturally
        when the user starts typing the second number.

        Args:
            operator_key: One of ``"add"``, ``"subtract"``, ``"multiply"``,
                ``"divide"``.
        """
        self._pending_operand = float(self._current_display)
        self._pending_operator = operator_key
        self._result_just_shown = True
        self._decimal_entered = False

    def _on_unary_pressed(self, function_key: str) -> None:
        """Handle a scientific (unary) function button press.

        Applies the function to the current display value immediately.

        Args:
            function_key: A key from :data:`~src.input_loop.OPERATIONS` for a
                unary function (e.g. ``"square_root"``, ``"factorial"``).
        """
        try:
            current_float = float(self._current_display)
            result = dispatch(function_key, [current_float], self._calc)
            self._current_display = self._format_result(result)
            self._decimal_entered = "." in self._current_display
            self._result_just_shown = True
        except (ValueError, KeyError) as exc:
            self._current_display = "Error"
            self._pending_operator = None
            self._pending_operand = None
            self._decimal_entered = False
            self._result_just_shown = False
            _ = exc  # silenced — error shown in display
        self._update_display()

    def _on_equals_pressed(self) -> None:
        """Handle the equals button press.

        Evaluates the pending binary operation using the stored operand and
        the current display value.  Does nothing when no operator is pending.
        """
        if self._pending_operator is None:
            return
        try:
            current_float = float(self._current_display)
            result = dispatch(
                self._pending_operator,
                [self._pending_operand, current_float],  # type: ignore[list-item]
                self._calc,
            )
            self._current_display = self._format_result(result)
            self._pending_operator = None
            self._pending_operand = None
            self._decimal_entered = "." in self._current_display
            self._result_just_shown = True
        except (ValueError, KeyError) as exc:
            self._current_display = "Error"
            self._pending_operator = None
            self._pending_operand = None
            self._decimal_entered = False
            self._result_just_shown = False
            _ = exc  # silenced — error shown in display
        self._update_display()

    def _on_clear_pressed(self) -> None:
        """Handle the C (clear) button press, resetting all state."""
        self._current_display = "0"
        self._pending_operator = None
        self._pending_operand = None
        self._decimal_entered = False
        self._result_just_shown = False
        self._update_display()

    def _on_negate_pressed(self) -> None:
        """Handle the +/- (negate) button press."""
        try:
            current_float = float(self._current_display)
            self._current_display = self._format_result(-current_float)
        except ValueError:
            pass  # display stays as-is (e.g. "Error")
        self._update_display()

    def _on_percent_pressed(self) -> None:
        """Handle the % button press, dividing the current value by 100."""
        try:
            current_float = float(self._current_display)
            self._current_display = self._format_result(current_float / 100.0)
            self._decimal_entered = "." in self._current_display
        except ValueError:
            pass  # display stays as-is
        self._update_display()

    def _on_mode_toggle(self) -> None:
        """Toggle between Normal and Scientific modes.

        Shows or hides the scientific button rows without affecting any
        pending calculation state.
        """
        self._is_scientific_mode = not self._is_scientific_mode
        if self._is_scientific_mode:
            self._sci_frame.pack(fill="both", padx=8, pady=(0, 4))
            self._mode_btn.config(text="Normal")
        else:
            self._sci_frame.pack_forget()
            self._mode_btn.config(text="Scientific")

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the tkinter main event loop.

        Blocks until the user closes the window.
        """
        self._root.mainloop()
