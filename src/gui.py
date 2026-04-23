"""gui.py — Tkinter-based GUI for the Calculator.

Provides :class:`CalculatorGUI`, a ``tk.Tk`` subclass that wraps a
:class:`~src.calculator.Calculator` instance in a graphical window.

The GUI accepts expressions in the same textual format as the REPL and
CLI: ``OPERATION OPERAND1 [OPERAND2]`` (e.g. ``"add 5 3"``, ``"sqrt 16"``).
Button presses build the expression string; the Equals button dispatches it
through :class:`~src.input_handler.ExpressionParser` and
:class:`~src.input_handler.InputValidator` before delegating to the
``Calculator`` instance.

Usage — standalone::

    python -m src.gui

Usage — from ``src.main`` with ``--gui`` flag::

    python -m src.main --gui
"""

from __future__ import annotations

import tkinter as tk
from typing import Union

from .calculator import Calculator
from .input_handler import ExpressionParser, InputValidator, OperationNotAvailableInModeError
from .logger import get_logger

logger = get_logger(__name__)

# Numeric type alias, consistent with other modules.
Numeric = Union[int, float]

# Valid mode names — kept in sync with input_handler._VALID_MODES.
_VALID_MODES: tuple[str, ...] = ("basic", "advanced", "scientific")

# ---------------------------------------------------------------------------
# Button layout per mode
#
# Each entry is the ordered list of button labels that should be *visible* in
# that mode.  Labels that are present in a higher-capability mode but absent
# in a lower one are hidden via grid_remove() rather than destroyed, so they
# can be cheaply re-shown when the user switches back to a richer mode.
#
# "basic" buttons are the plain arithmetic set.
# "advanced" adds square, cube, roots, power, factorial, and log buttons.
# "scientific" further adds trigonometric and hyperbolic function buttons.
# ---------------------------------------------------------------------------

_BASIC_LABELS: list[str] = [
    "C", "←", "=",
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "+",
]

_ADVANCED_LABELS: list[str] = _BASIC_LABELS + [
    "x²", "x³", "√", "∛", "xⁿ", "n!", "ln", "log",
]

_SCIENTIFIC_LABELS: list[str] = _ADVANCED_LABELS + [
    "sin", "cos", "tan", "asin", "acos", "atan",
    "sinh", "cosh", "tanh", "exp", "deg", "rad",
]

_MODE_BUTTON_LAYOUTS: dict[str, list[str]] = {
    "basic": _BASIC_LABELS,
    "advanced": _ADVANCED_LABELS,
    "scientific": _SCIENTIFIC_LABELS,
}

# Mapping from GUI button label to the operation name used by ExpressionParser.
# Only entries that differ from the label itself are listed here.
_LABEL_TO_OPERATION: dict[str, str] = {
    "x²": "square",
    "x³": "cube",
    "√": "square_root",
    "∛": "cube_root",
    "xⁿ": "power",
    "n!": "factorial",
    "ln": "natural_log",
    "log": "log_base_10",
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "asin": "asin",
    "acos": "acos",
    "atan": "atan",
    "sinh": "sinh",
    "cosh": "cosh",
    "tanh": "tanh",
    "exp": "exp",
    "deg": "degrees",
    "rad": "radians",
}


class CalculatorGUI(tk.Tk):
    """Graphical front-end for the Calculator.

    Inherits from ``tk.Tk`` so the instance is itself the main window.
    All computation is delegated to the injected ``Calculator`` instance
    via the same public API used by the CLI and REPL.

    Args:
        calculator: A :class:`~src.calculator.Calculator` instance to
            delegate all computation to.  Defaults to a new
            ``Calculator()`` with the default mode (``"advanced"``) when
            not provided.

    Example::

        app = CalculatorGUI()
        app.mainloop()
    """

    def __init__(self, calculator: Calculator | None = None) -> None:
        """Initialise the window, widgets, and keybindings.

        Args:
            calculator: Optional injected ``Calculator`` instance.  If
                ``None``, a fresh ``Calculator()`` is created with the
                default mode.
        """
        super().__init__()

        self._calculator: Calculator = calculator if calculator is not None else Calculator()
        self._parser: ExpressionParser = ExpressionParser()
        self._validator: InputValidator = InputValidator()

        # Current expression being built by button presses.
        self._expression: str = ""

        # Stores label → tk.Button widget for all buttons created across all
        # modes.  Populated by _build_button_grid(); used by
        # _rebuild_button_grid_for_mode() to show/hide buttons without
        # destroying and recreating them.
        self._button_widgets: dict[str, tk.Button] = {}

        self.title("Calculator")
        self.resizable(False, False)

        self._build_ui()

        logger.debug("CalculatorGUI initialised.")

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Build and grid all widgets inside the main window."""
        self._build_display()
        self._build_mode_selector()
        self._build_button_grid()

    def _build_display(self) -> None:
        """Create the display Entry widget at the top of the window."""
        self._display_var: tk.StringVar = tk.StringVar(value="")
        display = tk.Entry(
            self,
            textvariable=self._display_var,
            font=("Courier", 18),
            justify="right",
            state="readonly",
            readonlybackground="white",
            relief="sunken",
            bd=4,
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=8, pady=(8, 4))

    def _build_mode_selector(self) -> None:
        """Create the mode selector label and OptionMenu below the display."""
        frame = tk.Frame(self)
        frame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=8, pady=(0, 4))

        tk.Label(frame, text="Mode:").pack(side="left")

        self._mode_var: tk.StringVar = tk.StringVar(value=self._calculator._mode)
        mode_menu = tk.OptionMenu(
            frame,
            self._mode_var,
            self._calculator._mode,
            *[m for m in _VALID_MODES if m != self._calculator._mode],
            command=self._on_mode_change,
        )
        mode_menu.pack(side="left", padx=4)

    def _build_button_grid(self) -> None:
        """Create and grid all buttons for every mode.

        All buttons across *all* modes are created upfront and stored in
        ``self._button_widgets``.  Only the buttons appropriate for the
        current mode are made visible; the rest are hidden via
        ``grid_remove()`` so they can be cheaply re-shown later without
        widget re-creation.

        Button layout definition
        ------------------------
        Each entry is a 4-tuple ``(label, row, col, colspan)``.  The grid
        spans rows 2–9 with 4 columns (indices 0–3).  Rows 2–6 are the
        basic layout; rows 7–8 hold the advanced function buttons; row 9
        holds the scientific function buttons.
        """
        # ------------------------------------------------------------------
        # Full button specification: (label, row, col, colspan)
        # ------------------------------------------------------------------
        all_buttons: list[tuple[str, int, int, int]] = [
            # Row 2: control buttons
            ("C",   2, 0, 1),
            ("←",   2, 1, 1),
            ("",    2, 2, 1),   # placeholder kept for grid alignment
            ("=",   2, 3, 1),
            # Row 3: top digit row
            ("7",   3, 0, 1),
            ("8",   3, 1, 1),
            ("9",   3, 2, 1),
            ("/",   3, 3, 1),
            # Row 4
            ("4",   4, 0, 1),
            ("5",   4, 1, 1),
            ("6",   4, 2, 1),
            ("*",   4, 3, 1),
            # Row 5
            ("1",   5, 0, 1),
            ("2",   5, 1, 1),
            ("3",   5, 2, 1),
            ("-",   5, 3, 1),
            # Row 6
            ("0",   6, 0, 2),
            (".",   6, 2, 1),
            ("+",   6, 3, 1),
            # Row 7: advanced — unary operations
            ("x²",  7, 0, 1),
            ("x³",  7, 1, 1),
            ("√",   7, 2, 1),
            ("∛",   7, 3, 1),
            # Row 8: advanced — binary / log operations
            ("xⁿ",  8, 0, 1),
            ("n!",  8, 1, 1),
            ("ln",  8, 2, 1),
            ("log", 8, 3, 1),
            # Row 9: scientific — trig row 1
            ("sin", 9, 0, 1),
            ("cos", 9, 1, 1),
            ("tan", 9, 2, 1),
            ("asin",9, 3, 1),
            # Row 10: scientific — trig row 2
            ("acos",10, 0, 1),
            ("atan",10, 1, 1),
            ("sinh",10, 2, 1),
            ("cosh",10, 3, 1),
            # Row 11: scientific — misc
            ("tanh",11, 0, 1),
            ("exp", 11, 1, 1),
            ("deg", 11, 2, 1),
            ("rad", 11, 3, 1),
        ]

        # Determine which labels should be visible for the initial mode.
        initial_mode = self._calculator._mode
        visible_labels: set[str] = set(_MODE_BUTTON_LAYOUTS.get(initial_mode, _BASIC_LABELS))

        # Store per-button grid kwargs so _rebuild_button_grid_for_mode can
        # re-grid them at their original position.
        self._button_grid_kwargs: dict[str, dict] = {}

        for label, row, col, colspan in all_buttons:
            if not label:
                # Empty placeholder — skip widget creation.
                continue

            grid_kwargs: dict = {
                "row": row,
                "column": col,
                "columnspan": colspan,
                "sticky": "nsew",
                "padx": 2,
                "pady": 2,
            }
            self._button_grid_kwargs[label] = grid_kwargs

            btn = tk.Button(
                self,
                text=label,
                font=("Helvetica", 14),
                width=4,
                height=2,
                command=lambda lbl=label: self._on_button(lbl),
            )

            self._button_widgets[label] = btn

            if label in visible_labels:
                btn.grid(**grid_kwargs)
            else:
                # Create the widget but keep it out of the grid until the
                # user switches to a mode that requires it.
                btn.grid(**grid_kwargs)
                btn.grid_remove()

        # Configure grid weights so buttons resize predictably.
        for col in range(4):
            self.columnconfigure(col, weight=1)
        for row in range(2, 12):
            self.rowconfigure(row, weight=1)

    # ------------------------------------------------------------------
    # Mode-driven layout update
    # ------------------------------------------------------------------

    def _rebuild_button_grid_for_mode(self, mode: str) -> None:
        """Show or hide buttons according to the given *mode*.

        Buttons that belong to the requested mode are re-gridded at their
        original position; buttons that do not belong are hidden via
        ``grid_remove()``.  Widgets are *never* destroyed — this allows
        switching back to a richer mode without recreating any widget.

        Args:
            mode: One of ``"basic"``, ``"advanced"``, or ``"scientific"``.
                If an unrecognised mode is supplied, the method falls back
                to the ``"basic"`` layout and logs a warning.
        """
        if mode not in _MODE_BUTTON_LAYOUTS:
            logger.warning(
                "_rebuild_button_grid_for_mode: unknown mode %r, falling back to 'basic'.",
                mode,
            )
            mode = "basic"

        visible_labels: set[str] = set(_MODE_BUTTON_LAYOUTS[mode])

        for label, btn in self._button_widgets.items():
            if label in visible_labels:
                grid_kwargs = self._button_grid_kwargs.get(label)
                if grid_kwargs is not None:
                    btn.grid(**grid_kwargs)
            else:
                btn.grid_remove()

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_mode_change(self, selected_mode: str) -> None:
        """Switch the calculator mode when the OptionMenu selection changes.

        Updates both the underlying ``Calculator`` mode and the visible
        button layout to match the selected mode.

        Args:
            selected_mode: The mode name chosen by the user.
        """
        try:
            self._calculator.set_mode(selected_mode)
            logger.debug("Mode switched to '%s'.", selected_mode)
        except ValueError as exc:
            self._show_error(f"Mode error: {exc}")
            return

        self._rebuild_button_grid_for_mode(selected_mode)

    def _on_button(self, label: str) -> None:
        """Handle a button press by label.

        Dispatches to the appropriate action: clear, backspace, evaluate,
        arithmetic operator, function operation, or append the label to
        the current expression string.

        Args:
            label: The text on the pressed button.
        """
        if label == "C":
            self._clear()
        elif label == "←":
            self._backspace()
        elif label == "=":
            self._evaluate()
        elif label in ("+", "-", "*", "/"):
            self._append_operator(label)
        elif label in _LABEL_TO_OPERATION:
            self._append_function(label)
        else:
            self._append(label)

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def _set_display(self, text: str) -> None:
        """Update the display field to *text*.

        Args:
            text: The string to show in the display Entry widget.
        """
        self._display_var.set(text)

    def _show_error(self, message: str) -> None:
        """Show *message* in the display field and log it.

        Args:
            message: A human-readable error description.
        """
        logger.warning("CalculatorGUI error: %s", message)
        self._set_display(message)

    # ------------------------------------------------------------------
    # Expression management
    # ------------------------------------------------------------------

    def _clear(self) -> None:
        """Reset the expression and display to the empty state."""
        self._expression = ""
        self._set_display("")

    def _backspace(self) -> None:
        """Remove the last character from the current expression."""
        self._expression = self._expression[:-1]
        self._set_display(self._expression)

    def _append(self, text: str) -> None:
        """Append *text* to the current expression and update the display.

        Args:
            text: A digit or decimal-point character to append.
        """
        self._expression += text
        self._set_display(self._expression)

    def _append_operator(self, operator: str) -> None:
        """Translate a symbolic operator and append it to the expression.

        Converts the symbolic operator (``+``, ``-``, ``*``, ``/``) into
        the corresponding word-based operation name understood by
        :class:`~src.input_handler.ExpressionParser`, then inserts it at
        the correct position in the expression string.

        The GUI expression is constructed so that the first token is always
        the operation name; operands follow.  Pressing an operator button
        therefore sets the operation prefix when the expression is otherwise
        a bare number, or appends the second operand separator when the
        expression already has an operation.

        Args:
            operator: One of ``"+"``, ``"-"``, ``"*"``, ``"/"``.
        """
        _op_map: dict[str, str] = {
            "+": "add",
            "-": "subtract",
            "*": "multiply",
            "/": "divide",
        }
        operation = _op_map[operator]

        # If the expression already has an operation token and at least one
        # operand, treat pressing an operator as inserting a space (so the
        # user can type the second operand).  Otherwise, prepend the
        # operation to whatever number is currently displayed.
        stripped = self._expression.strip()
        parts = stripped.split()

        if not stripped:
            # Nothing typed yet — set the operation and wait for the operand.
            self._expression = operation + " "
        elif len(parts) == 1:
            # A single token: assume it's the first operand; prepend the op.
            self._expression = f"{operation} {stripped} "
        else:
            # Already have op + at least one operand; append a space to
            # separate the next token.
            self._expression = stripped + " "

        self._set_display(self._expression)

    def _append_function(self, label: str) -> None:
        """Set the expression to invoke the function associated with *label*.

        Function buttons (e.g. ``"x²"``, ``"√"``, ``"sin"``) always set
        the operation prefix in the expression, preserving any number that
        was already typed as the first operand.

        Args:
            label: The GUI button label (e.g. ``"x²"``, ``"sin"``).
        """
        operation = _LABEL_TO_OPERATION[label]
        stripped = self._expression.strip()
        parts = stripped.split()

        if not stripped:
            # Nothing typed yet — set the operation and wait for the operand.
            self._expression = operation + " "
        elif len(parts) == 1:
            # A bare number is already typed; treat it as the operand.
            self._expression = f"{operation} {stripped} "
        else:
            # Expression already has an operation; replace with the new one,
            # keeping the first operand if present.
            self._expression = f"{operation} {parts[1]} " if len(parts) > 1 else operation + " "

        self._set_display(self._expression)

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    def _evaluate(self) -> None:
        """Parse and evaluate the current expression, then show the result.

        The expression string is dispatched through :class:`ExpressionParser`
        and :class:`InputValidator` before the matching ``Calculator`` method
        is called.  All errors are caught and displayed in the display field
        so the application never crashes on bad input.
        """
        raw = self._expression.strip()
        if not raw:
            return

        logger.debug("CalculatorGUI evaluating: %r", raw)

        # --- Parse ---
        try:
            operation, operands = self._parser.parse(raw)
        except ValueError as exc:
            self._show_error(f"Input error: {exc}")
            return

        # --- Validate ---
        try:
            self._validator.validate(operation, operands)
        except ValueError as exc:
            self._show_error(f"Validation error: {exc}")
            return

        # --- Dispatch ---
        try:
            method = getattr(self._calculator, operation)
            result: Numeric = method(*operands)
        except OperationNotAvailableInModeError as exc:
            logger.warning(
                "CalculatorGUI mode error: operation=%r current_mode=%r",
                exc.operation,
                exc.current_mode,
            )
            self._show_error(
                f"'{exc.operation}' not available in {exc.current_mode} mode"
            )
            return
        except ZeroDivisionError:
            self._show_error("Error: division by zero")
            return
        except ValueError as exc:
            self._show_error(f"Error: {exc}")
            return
        except TypeError as exc:
            self._show_error(f"Type error: {exc}")
            return
        except AttributeError:
            self._show_error(f"Unknown operation: {operation}")
            return

        # --- Display result and reset expression ---
        result_str = str(result)
        self._expression = result_str
        self._set_display(result_str)
        logger.debug("CalculatorGUI result: %r -> %r", raw, result_str)


if __name__ == "__main__":
    app = CalculatorGUI()
    app.mainloop()
