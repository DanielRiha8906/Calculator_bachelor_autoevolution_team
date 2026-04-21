"""Tkinter-based graphical user interface for the calculator.

Provides a ``CalculatorGUI`` class that wraps a ``Calculator`` instance and
exposes a window with number and operation buttons, a result display, and
a toggle for scientific mode that shows/hides advanced operation buttons.

Usage::

    import tkinter as tk
    from src.presentation.gui import CalculatorGUI

    root = tk.Tk()
    app = CalculatorGUI(root)
    app.run()
"""

import tkinter as tk
from tkinter import font as tkfont
from typing import Optional

from src.logic import Calculator


class CalculatorGUI:
    """Tkinter GUI window for the calculator.

    Wraps a ``Calculator`` instance and manages the full button layout,
    display, and state machine for a graphical calculator.

    State:
        _display_var: The StringVar driving the result Label.
        _first_operand: The left-hand side value waiting for a second operand.
        _pending_op: The operation symbol currently awaiting a second operand.
        _reset_on_next_digit: Flag indicating that the next digit press should
            start a fresh number rather than appending to the current display.
    """

    # Maps display symbol -> Calculator method name for binary operations.
    _BINARY_OPS: dict[str, str] = {
        "+": "add",
        "-": "subtract",
        "*": "multiply",
        "/": "divide",
        "^": "power",
    }

    # Scientific unary operations: label -> Calculator method name.
    _SCIENTIFIC_OPS: list[tuple[str, str]] = [
        ("sin", "sin"),
        ("cos", "cos"),
        ("tan", "tan"),
        ("sqrt", "sqrt"),
        ("cbrt", "cube_root"),
        ("x!", "factorial"),
        ("log", "log10"),
        ("ln", "natural_log"),
        ("exp", "exp"),
        ("x²", "square"),
        ("x³", "cube"),
        ("√x", "square_root"),
    ]

    def __init__(self, root: tk.Tk) -> None:
        """Initialise the GUI and lay out all widgets.

        Args:
            root: The tkinter root window that this GUI will be drawn inside.
        """
        self._root = root
        self._root.title("Calculator")
        self._root.resizable(False, False)

        self._calc: Calculator = Calculator()

        # --- State ---
        self._display_var: tk.StringVar = tk.StringVar(value="0")
        self._first_operand: Optional[float] = None
        self._pending_op: Optional[str] = None
        self._reset_on_next_digit: bool = False
        self._scientific_visible: bool = False

        self._build_ui()
        self._bind_keyboard()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Create and arrange all widgets in the root window."""
        display_font = tkfont.Font(family="Courier", size=24, weight="bold")
        btn_font = tkfont.Font(family="Helvetica", size=14)
        sci_font = tkfont.Font(family="Helvetica", size=11)

        # Display area
        display_frame = tk.Frame(self._root, bg="#1e1e1e")
        display_frame.pack(fill=tk.X, padx=4, pady=(6, 2))

        self._display_label = tk.Label(
            display_frame,
            textvariable=self._display_var,
            anchor="e",
            bg="#1e1e1e",
            fg="#f0f0f0",
            font=display_font,
            padx=8,
            pady=6,
        )
        self._display_label.pack(fill=tk.X)

        # Scientific toggle button
        toggle_frame = tk.Frame(self._root, bg="#2d2d2d")
        toggle_frame.pack(fill=tk.X, padx=4, pady=(0, 2))
        self._toggle_btn = tk.Button(
            toggle_frame,
            text="Scientific Mode: OFF",
            command=self._toggle_scientific_mode,
            bg="#3a3a3a",
            fg="#cccccc",
            font=sci_font,
            relief=tk.FLAT,
            bd=0,
            padx=6,
            pady=4,
        )
        self._toggle_btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Scientific panel (initially hidden)
        self._sci_frame = tk.Frame(self._root, bg="#2d2d2d")
        self._build_scientific_panel(self._sci_frame, sci_font)
        # Not packed yet — shown only when scientific mode is toggled on.

        # Main button grid
        self._btn_frame = tk.Frame(self._root, bg="#2d2d2d")
        self._btn_frame.pack(padx=4, pady=4)
        self._build_button_grid(self._btn_frame, btn_font)

    def _btn(
        self,
        parent: tk.Frame,
        text: str,
        command,
        bg: str = "#3a3a3a",
        fg: str = "#f0f0f0",
        font: Optional[tkfont.Font] = None,
        width: int = 4,
        height: int = 2,
    ) -> tk.Button:
        """Create and return a styled Button widget.

        Args:
            parent: The parent frame to attach the button to.
            text: Button label text.
            command: Callback invoked on button click.
            bg: Background colour string.
            fg: Foreground (text) colour string.
            font: Font for the button label.
            width: Character width of the button.
            height: Character height of the button.

        Returns:
            The constructed ``tk.Button`` instance.
        """
        b = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            font=font,
            width=width,
            height=height,
            relief=tk.FLAT,
            bd=1,
            activebackground="#505050",
            activeforeground="#ffffff",
        )
        return b

    def _build_button_grid(self, parent: tk.Frame, font: tkfont.Font) -> None:
        """Build the standard calculator button grid inside *parent*.

        Layout (rows x cols):
            Row 0: Clear (C), Backspace (⌫), %, /
            Row 1: 7, 8, 9, *
            Row 2: 4, 5, 6, -
            Row 3: 1, 2, 3, +
            Row 4: +/-, 0, ., =

        Args:
            parent: Frame in which the grid will be placed.
            font: Font applied to all buttons in the grid.
        """
        op_bg = "#e07b39"
        clear_bg = "#a33"
        eq_bg = "#5a9e5a"

        buttons: list[list[tuple]] = [
            [
                ("C",   self._on_clear_click,      clear_bg, "#fff"),
                ("⌫",  self._on_backspace_click,   "#555",   "#fff"),
                ("%",   lambda: self._on_percent_click(), "#555", "#fff"),
                ("/",   lambda: self._on_operation_click("/"),   op_bg, "#fff"),
            ],
            [
                ("7", lambda: self._on_number_click("7"), "#3a3a3a", "#f0f0f0"),
                ("8", lambda: self._on_number_click("8"), "#3a3a3a", "#f0f0f0"),
                ("9", lambda: self._on_number_click("9"), "#3a3a3a", "#f0f0f0"),
                ("*", lambda: self._on_operation_click("*"), op_bg, "#fff"),
            ],
            [
                ("4", lambda: self._on_number_click("4"), "#3a3a3a", "#f0f0f0"),
                ("5", lambda: self._on_number_click("5"), "#3a3a3a", "#f0f0f0"),
                ("6", lambda: self._on_number_click("6"), "#3a3a3a", "#f0f0f0"),
                ("-", lambda: self._on_operation_click("-"), op_bg, "#fff"),
            ],
            [
                ("1", lambda: self._on_number_click("1"), "#3a3a3a", "#f0f0f0"),
                ("2", lambda: self._on_number_click("2"), "#3a3a3a", "#f0f0f0"),
                ("3", lambda: self._on_number_click("3"), "#3a3a3a", "#f0f0f0"),
                ("+", lambda: self._on_operation_click("+"), op_bg, "#fff"),
            ],
            [
                ("+/-", lambda: self._on_negate_click(), "#3a3a3a", "#f0f0f0"),
                ("0",   lambda: self._on_number_click("0"), "#3a3a3a", "#f0f0f0"),
                (".",   lambda: self._on_number_click("."), "#3a3a3a", "#f0f0f0"),
                ("=",   self._on_equals_click,            eq_bg,    "#fff"),
            ],
        ]

        for r, row in enumerate(buttons):
            for c, (label, cmd, bg, fg) in enumerate(row):
                b = self._btn(parent, label, cmd, bg=bg, fg=fg, font=font)
                b.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

    def _build_scientific_panel(self, parent: tk.Frame, font: tkfont.Font) -> None:
        """Build the scientific operation buttons inside *parent*.

        Buttons are arranged in a 4-column grid.  Each button triggers a
        unary scientific operation on the current display value.

        Args:
            parent: Frame that will contain the scientific buttons.
            font: Font applied to all scientific buttons.
        """
        for idx, (label, method_name) in enumerate(self._SCIENTIFIC_OPS):
            row, col = divmod(idx, 4)
            b = self._btn(
                parent,
                label,
                lambda m=method_name: self._on_scientific_click(m),
                bg="#2a4a6a",
                fg="#cce4ff",
                font=font,
                width=5,
                height=1,
            )
            b.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

    # ------------------------------------------------------------------
    # Keyboard bindings
    # ------------------------------------------------------------------

    def _bind_keyboard(self) -> None:
        """Attach keyboard event handlers to the root window."""
        root = self._root
        for digit in "0123456789":
            root.bind(f"<Key-{digit}>", lambda e, d=digit: self._on_number_click(d))
        root.bind("<Key-plus>",     lambda e: self._on_operation_click("+"))
        root.bind("<Key-minus>",    lambda e: self._on_operation_click("-"))
        root.bind("<Key-asterisk>", lambda e: self._on_operation_click("*"))
        root.bind("<Key-slash>",    lambda e: self._on_operation_click("/"))
        root.bind("<Key-Return>",   lambda e: self._on_equals_click())
        root.bind("<Key-equal>",    lambda e: self._on_equals_click())
        root.bind("<BackSpace>",    lambda e: self._on_backspace_click())
        root.bind("<Key-c>",        lambda e: self._on_clear_click())
        root.bind("<Key-C>",        lambda e: self._on_clear_click())
        root.bind("<Key-period>",   lambda e: self._on_number_click("."))

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def _update_display(self, text: str) -> None:
        """Update the result display with *text*.

        Args:
            text: The string to show in the display area.
        """
        self._display_var.set(text)

    def _current_display(self) -> str:
        """Return the current text shown in the display.

        Returns:
            The current display string.
        """
        return self._display_var.get()

    # ------------------------------------------------------------------
    # State helpers
    # ------------------------------------------------------------------

    def _parse_display(self) -> float:
        """Parse the current display string as a float.

        Returns:
            The numeric value of the current display.

        Raises:
            ValueError: If the display cannot be converted to a number.
        """
        return float(self._current_display())

    def _reset_state(self) -> None:
        """Clear pending operation and first operand, ready for a new calculation."""
        self._first_operand = None
        self._pending_op = None
        self._reset_on_next_digit = False

    # ------------------------------------------------------------------
    # Button handlers
    # ------------------------------------------------------------------

    def _on_number_click(self, digit: str) -> None:
        """Handle a digit or decimal-point button press.

        Appends *digit* to the current display.  If ``_reset_on_next_digit``
        is set (e.g. after an equals press), the display is replaced instead
        of appended to.

        Args:
            digit: A single character: one of ``"0"``–``"9"`` or ``"."``.
        """
        current = self._current_display()

        if self._reset_on_next_digit:
            current = "0"
            self._reset_on_next_digit = False

        # Prevent multiple decimal points
        if digit == "." and "." in current:
            return

        if current == "0" and digit != ".":
            new_value = digit
        else:
            new_value = current + digit

        self._update_display(new_value)

    def _on_operation_click(self, op: str) -> None:
        """Handle an arithmetic operation button press (+, -, *, /, ^).

        Saves the current display value as the first operand and records the
        pending operation.  If a pending operation already exists the chain is
        resolved first (left-to-right evaluation).

        Args:
            op: The operation symbol — one of ``"+"``, ``"-"``, ``"*"``,
                ``"/"``, ``"^"``.
        """
        try:
            current_value = self._parse_display()
        except ValueError:
            # Display might contain an error string; treat as reset
            self._on_clear_click()
            return

        if self._pending_op is not None and not self._reset_on_next_digit:
            # Chain: resolve the previous pending op first
            self._execute_operation()
            try:
                current_value = self._parse_display()
            except ValueError:
                return

        self._first_operand = current_value
        self._pending_op = op
        self._reset_on_next_digit = True

    def _on_equals_click(self) -> None:
        """Execute the pending operation and display the result.

        If no pending operation is set, this is a no-op.  On success the
        display is updated with the result and all pending state is cleared.
        """
        if self._pending_op is None:
            return
        self._execute_operation()
        self._pending_op = None
        self._first_operand = None
        self._reset_on_next_digit = True

    def _on_clear_click(self) -> None:
        """Reset the display and all calculator state to the initial condition."""
        self._update_display("0")
        self._reset_state()

    def _on_backspace_click(self) -> None:
        """Remove the last character from the current display.

        If the display becomes empty after removal, it is replaced with ``"0"``.
        If the current display is an error message, the display is cleared to
        ``"0"`` entirely.
        """
        current = self._current_display()
        # If it is an error string, just clear entirely
        if current.startswith("Error"):
            self._update_display("0")
            self._reset_state()
            return
        new_value = current[:-1]
        self._update_display(new_value if new_value and new_value != "-" else "0")

    def _on_negate_click(self) -> None:
        """Toggle the sign of the current display value."""
        current = self._current_display()
        if current.startswith("Error"):
            return
        try:
            value = self._parse_display()
        except ValueError:
            return
        negated = value * -1
        # Format without unnecessary trailing zeros
        if negated == int(negated):
            self._update_display(str(int(negated)))
        else:
            self._update_display(str(negated))

    def _on_percent_click(self) -> None:
        """Divide the current display value by 100."""
        current = self._current_display()
        if current.startswith("Error"):
            return
        try:
            value = self._parse_display()
        except ValueError:
            return
        result = value / 100.0
        self._update_display(self._format_result(result))

    def _on_scientific_click(self, method_name: str) -> None:
        """Apply a unary scientific operation to the current display value.

        Args:
            method_name: The name of the ``Calculator`` method to invoke
                (e.g. ``"sin"``, ``"sqrt"``, ``"factorial"``).
        """
        current = self._current_display()
        if current.startswith("Error"):
            self._on_clear_click()
            return
        try:
            value = self._parse_display()
        except ValueError:
            self._update_display("Error: invalid input")
            self._reset_state()
            return

        method = getattr(self._calc, method_name, None)
        if method is None:
            self._update_display(f"Error: {method_name} not available")
            return

        try:
            result = method(value)
        except ZeroDivisionError:
            self._update_display("Error: Division by zero")
            self._reset_state()
            return
        except ValueError as exc:
            self._update_display(f"Error: {exc}")
            self._reset_state()
            return
        except TypeError as exc:
            self._update_display(f"Error: {exc}")
            self._reset_state()
            return

        self._update_display(self._format_result(result))
        self._reset_on_next_digit = True

    def _toggle_scientific_mode(self) -> None:
        """Show or hide the scientific operations panel.

        Toggling does not affect the ``Calculator`` instance's mode — it only
        controls the visibility of the extra button panel in the GUI.
        """
        if self._scientific_visible:
            self._sci_frame.pack_forget()
            self._scientific_visible = False
            self._toggle_btn.config(text="Scientific Mode: OFF")
        else:
            self._sci_frame.pack(
                before=self._btn_frame,
                padx=4,
                pady=(0, 2),
            )
            self._scientific_visible = True
            self._toggle_btn.config(text="Scientific Mode: ON")

    # ------------------------------------------------------------------
    # Calculation engine
    # ------------------------------------------------------------------

    def _execute_operation(self) -> None:
        """Perform the pending binary operation and update the display.

        Uses ``_first_operand``, ``_pending_op``, and the current display
        value as the second operand.  The result replaces the display.  On any
        arithmetic error the display shows the error message and pending state
        is cleared.
        """
        if self._pending_op is None or self._first_operand is None:
            return

        try:
            second_operand = self._parse_display()
        except ValueError:
            self._update_display("Error: invalid input")
            self._reset_state()
            return

        method_name = self._BINARY_OPS.get(self._pending_op)
        if method_name is None:
            self._update_display(f"Error: unknown op '{self._pending_op}'")
            self._reset_state()
            return

        method = getattr(self._calc, method_name)
        try:
            result = method(self._first_operand, second_operand)
        except ZeroDivisionError:
            self._update_display("Error: Division by zero")
            self._reset_state()
            return
        except ValueError as exc:
            self._update_display(f"Error: {exc}")
            self._reset_state()
            return
        except TypeError as exc:
            self._update_display(f"Error: {exc}")
            self._reset_state()
            return

        self._update_display(self._format_result(result))

    # ------------------------------------------------------------------
    # Formatting
    # ------------------------------------------------------------------

    @staticmethod
    def _format_result(result: int | float) -> str:
        """Format a numeric result for display.

        Integers are shown without a decimal point; floats are shown with up
        to 10 significant decimal digits, stripping trailing zeros.

        Args:
            result: The numeric value to format.

        Returns:
            A clean string representation of *result*.
        """
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        if isinstance(result, float):
            formatted = f"{result:.10g}"
            return formatted
        return str(result)

    # ------------------------------------------------------------------
    # Event loop
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the tkinter main event loop.

        This call blocks until the window is closed.
        """
        self._root.mainloop()
