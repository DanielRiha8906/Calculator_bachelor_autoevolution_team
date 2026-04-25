"""Tkinter-based graphical calculator GUI.

This module provides a CalculatorGUI class that wraps a Calculator instance
in a simple tkinter window, and a launch_gui() entry-point function.
"""

import tkinter
import tkinter.messagebox

from .calculator_core import Calculator


# Mapping from operation key used in _apply_unary / _calculate to Calculator
# method names.  Binary operations go through _calculate; unary operations go
# through _apply_unary.

_BINARY_OPS: tuple[str, ...] = ("add", "subtract", "multiply", "divide", "power")
_UNARY_OPS: tuple[str, ...] = (
    "square",
    "cube",
    "square_root",
    "cube_root",
    "factorial",
    "log",
    "ln",
)


class CalculatorGUI:
    """A tkinter-based calculator GUI.

    Creates its own root Tk window when instantiated with no arguments, or
    accepts an external root for testing / embedding.

    Attributes:
        root: The tkinter root window (real or mock).
        entry: A tkinter Entry widget used to accept user input.
        display: A tkinter Label widget used to show results.
        current_input: The string currently being typed or shown.
        pending_op: The binary operation key waiting for a second operand,
            or None when no operation is pending.
        first_operand: The first operand captured when an operator was set,
            or None when no operation is pending.
        scientific_mode: Whether scientific mode is currently active.
        scientific_buttons: List of scientific-mode buttons hidden by default.
    """

    def __init__(self, root: object | None = None) -> None:
        """Initialise the calculator GUI.

        Creates a full button layout with digit buttons, operator buttons,
        unary operation buttons, and scientific mode buttons. Scientific
        buttons are hidden by default and shown when the Sci/Norm toggle
        is pressed.

        Args:
            root: Optional tkinter root window.  When None, a new Tk() window
                is created automatically.
        """
        self.calc: Calculator = Calculator()
        self.current_input: str = ""
        self.pending_op: str | None = None
        self.first_operand: float | None = None
        self.scientific_mode: bool = False
        self.scientific_buttons: list = []

        # Create or accept the root window.
        if root is None:
            self.root = tkinter.Tk()
        else:
            self.root = root

        self.root.title("Calculator")
        self.root.config(bg="#000000")
        self.root.geometry("350x450")

        # Configure grid weights for even expansion.
        for i in range(11):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(5):
            self.root.grid_columnconfigure(j, weight=1)

        # Row 0: Display label showing current result.
        self.display = tkinter.Label(
            self.root,
            text="0",
            anchor="e",
            font=("Arial", 30),
            bg="#000000",
            fg="white",
        )
        self.display.grid(row=0, column=0, columnspan=5, sticky="nsew")

        # Row 1: Entry field for typing input.
        self.entry = tkinter.Entry(
            self.root,
            font=("Arial", 14),
            bg="#000000",
            fg="white",
        )
        self.entry.grid(row=1, column=0, columnspan=5, sticky="nsew")

        # ------------------------------------------------------------------
        # Rows 2-7: Standard calculator buttons.
        # Layout:
        #   Row 2: [7][8][9][/][x²]
        #   Row 3: [4][5][6][*][x³]
        #   Row 4: [1][2][3][-][√]
        #   Row 5: [0][.][±][+][∛]
        #   Row 6: [←][C][^][log][ln]
        #   Row 7: [=][!][Sci/Norm]
        # ------------------------------------------------------------------

        # Row 2
        tkinter.Button(
            self.root, text="7",
            command=lambda: self._on_number_click("7"),
            bg="#333333", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=2, column=0, sticky="nsew")
        tkinter.Button(
            self.root, text="8",
            command=lambda: self._on_number_click("8"),
            bg="#333333", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=2, column=1, sticky="nsew")
        tkinter.Button(
            self.root, text="9",
            command=lambda: self._on_number_click("9"),
            bg="#333333", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=2, column=2, sticky="nsew")
        tkinter.Button(
            self.root, text="/",
            command=lambda: self._on_operator_click("divide"),
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=2, column=3, sticky="nsew")
        tkinter.Button(
            self.root, text="x²",
            command=lambda: self._apply_unary("square"),
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=2, column=4, sticky="nsew")

        # Row 3
        tkinter.Button(
            self.root, text="4",
            command=lambda: self._on_number_click("4"),
            bg="#333333", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=3, column=0, sticky="nsew")
        tkinter.Button(
            self.root, text="5",
            command=lambda: self._on_number_click("5"),
            bg="#333333", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=3, column=1, sticky="nsew")
        tkinter.Button(
            self.root, text="6",
            command=lambda: self._on_number_click("6"),
            bg="#333333", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=3, column=2, sticky="nsew")
        tkinter.Button(
            self.root, text="*",
            command=lambda: self._on_operator_click("multiply"),
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=3, column=3, sticky="nsew")
        tkinter.Button(
            self.root, text="x³",
            command=lambda: self._apply_unary("cube"),
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=3, column=4, sticky="nsew")

        # Row 4
        tkinter.Button(
            self.root, text="1",
            command=lambda: self._on_number_click("1"),
            bg="#333333", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=4, column=0, sticky="nsew")
        tkinter.Button(
            self.root, text="2",
            command=lambda: self._on_number_click("2"),
            bg="#333333", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=4, column=1, sticky="nsew")
        tkinter.Button(
            self.root, text="3",
            command=lambda: self._on_number_click("3"),
            bg="#333333", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=4, column=2, sticky="nsew")
        tkinter.Button(
            self.root, text="-",
            command=lambda: self._on_operator_click("subtract"),
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=4, column=3, sticky="nsew")
        tkinter.Button(
            self.root, text="√",
            command=lambda: self._apply_unary("square_root"),
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=4, column=4, sticky="nsew")

        # Row 5
        tkinter.Button(
            self.root, text="0",
            command=lambda: self._on_number_click("0"),
            bg="#333333", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=5, column=0, sticky="nsew")
        tkinter.Button(
            self.root, text=".",
            command=lambda: self._on_number_click("."),
            bg="#333333", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=5, column=1, sticky="nsew")
        tkinter.Button(
            self.root, text="±",
            command=self._on_sign_toggle,
            bg="#333333", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=5, column=2, sticky="nsew")
        tkinter.Button(
            self.root, text="+",
            command=lambda: self._on_operator_click("add"),
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=5, column=3, sticky="nsew")
        tkinter.Button(
            self.root, text="∛",
            command=lambda: self._apply_unary("cube_root"),
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=5, column=4, sticky="nsew")

        # Row 6
        tkinter.Button(
            self.root, text="←",
            command=self._on_backspace,
            bg="#333333", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=6, column=0, sticky="nsew")
        tkinter.Button(
            self.root, text="C",
            command=self._clear,
            bg="#333333", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=6, column=1, sticky="nsew")
        tkinter.Button(
            self.root, text="^",
            command=lambda: self._on_operator_click("power"),
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=6, column=2, sticky="nsew")
        tkinter.Button(
            self.root, text="log",
            command=lambda: self._apply_unary("log"),
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=6, column=3, sticky="nsew")
        tkinter.Button(
            self.root, text="ln",
            command=lambda: self._apply_unary("ln"),
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=6, column=4, sticky="nsew")

        # Row 7: equals, factorial, sci/norm toggle
        tkinter.Button(
            self.root, text="=",
            command=self._calculate,
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=7, column=0, columnspan=2, sticky="nsew")
        tkinter.Button(
            self.root, text="!",
            command=lambda: self._apply_unary("factorial"),
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=7, column=2, sticky="nsew")
        tkinter.Button(
            self.root, text="Sci/Norm",
            command=self._toggle_scientific_mode,
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        ).grid(row=7, column=3, columnspan=2, sticky="nsew")

        # ------------------------------------------------------------------
        # Rows 8+: Scientific mode buttons (hidden by default).
        # ------------------------------------------------------------------
        sci_specs: list[tuple[int, int, str, str]] = [
            # (row, col, label, method_or_constant)
            (8, 0, "sin", "sin"),
            (8, 1, "cos", "cos"),
            (8, 2, "tan", "tan"),
            (8, 3, "asin", "asin"),
            (8, 4, "acos", "acos"),
            (9, 0, "atan", "atan"),
            (9, 1, "sinh", "sinh"),
            (9, 2, "cosh", "cosh"),
            (9, 3, "tanh", "tanh"),
            (9, 4, "exp", "exp"),
        ]
        for row, col, label, method in sci_specs:
            btn = tkinter.Button(
                self.root, text=label,
                command=lambda m=method: self._apply_unary(m),
                bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
            )
            btn.grid(row=row, column=col, sticky="nsew")
            btn.grid_remove()
            self.scientific_buttons.append(btn)

        # Constant buttons for pi and e.
        pi_btn = tkinter.Button(
            self.root, text="π",
            command=lambda: self._on_constant_click("get_pi"),
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        )
        pi_btn.grid(row=10, column=0, sticky="nsew")
        pi_btn.grid_remove()
        self.scientific_buttons.append(pi_btn)

        e_btn = tkinter.Button(
            self.root, text="e",
            command=lambda: self._on_constant_click("get_e"),
            bg="#FF9500", fg="white", relief="flat", padx=3, pady=3,
        )
        e_btn.grid(row=10, column=1, sticky="nsew")
        e_btn.grid_remove()
        self.scientific_buttons.append(e_btn)

    # ------------------------------------------------------------------
    # Number and operator input handlers
    # ------------------------------------------------------------------

    def _on_number_click(self, digit: str) -> None:
        """Append a digit or decimal point to the current input and update entry.

        Args:
            digit: A single character ('0'-'9' or '.') to append.
        """
        self.current_input += digit
        self.entry.delete(0, tkinter.END)
        self.entry.insert(0, self.current_input)

    def _on_operator_click(self, op: str) -> None:
        """Store the first operand and the pending binary operator.

        Reads the current entry as a float. On success, stores it as the
        first operand and records the pending operation. On parse failure
        shows an error dialog.

        Args:
            op: One of 'add', 'subtract', 'multiply', 'divide', 'power'.
        """
        if self.current_input:
            try:
                self.first_operand = float(self.current_input)
                self.pending_op = op
                self.current_input = ""
                self.entry.delete(0, tkinter.END)
            except ValueError as e:
                tkinter.messagebox.showerror("Error", str(e))

    # ------------------------------------------------------------------
    # Operator helpers
    # ------------------------------------------------------------------

    def _set_operator(self, op: str) -> None:
        """Store the first operand and the pending binary operator.

        Args:
            op: One of 'add', 'subtract', 'multiply', 'divide', 'power'.
        """
        self.first_operand = float(self.current_input)
        self.pending_op = op
        self.current_input = ""

    def _apply_unary(self, op: str) -> float | None:
        """Apply a unary operation to the current input.

        Reads current_input as a float, calls the matching Calculator method,
        updates the display, and returns the numeric result.

        Args:
            op: One of 'square', 'cube', 'square_root', 'cube_root',
                'factorial', 'log', 'ln', 'sin', 'cos', 'tan', 'asin',
                'acos', 'atan', 'sinh', 'cosh', 'tanh', 'exp'.

        Returns:
            The computed result as a float, or None if an error occurred.
        """
        if not self.current_input:
            return None
        try:
            val = float(self.current_input)
            method = getattr(self.calc, op)
            result = method(val)
            result_float = float(result)
            self.current_input = str(result_float)
            self.display.config(text=self.current_input)
            self.entry.delete(0, tkinter.END)
            self.entry.insert(0, self.current_input)
            return result_float
        except (ValueError, ZeroDivisionError, AttributeError) as exc:
            tkinter.messagebox.showerror("Error", str(exc))
            return None

    def _calculate(self) -> float | None:
        """Apply the pending binary operation using the current input as the second operand.

        Reads current_input as a float, applies the pending binary operator
        via the Calculator, updates the display, and returns the numeric result.

        Returns:
            The computed result as a float, or None if an error occurred.

        Raises:
            ValueError: If current_input cannot be converted to a float.
            TypeError: If current_input is not a valid numeric string.
        """
        second = float(self.current_input)  # may raise ValueError / TypeError

        if not self.pending_op:
            return None

        try:
            method = getattr(self.calc, self.pending_op)
            result = method(self.first_operand, second)
            result_float = float(result)
            self.display.config(text=str(result_float))
            self.current_input = str(result_float)
            return result_float
        except (ValueError, ZeroDivisionError, AttributeError) as exc:
            tkinter.messagebox.showerror("Error", str(exc))
            return None

    def _clear(self) -> None:
        """Reset the calculator state and update the display."""
        self.current_input = ""
        self.pending_op = None
        self.first_operand = None
        self.display.config(text="0")
        self.entry.delete(0, tkinter.END)

    def _on_backspace(self) -> None:
        """Remove the last character from the current input and update entry."""
        self.current_input = self.current_input[:-1]
        self.entry.delete(0, tkinter.END)
        self.entry.insert(0, self.current_input)

    def _on_sign_toggle(self) -> None:
        """Negate the current input value and update the entry field."""
        if self.current_input and self.current_input != "-":
            try:
                val = float(self.current_input)
                self.current_input = str(-val)
                self.entry.delete(0, tkinter.END)
                self.entry.insert(0, self.current_input)
            except ValueError:
                pass

    def _on_constant_click(self, op: str) -> None:
        """Insert a mathematical constant (pi or e) into the display.

        Calls the zero-arity Calculator method identified by op and displays
        the result.

        Args:
            op: 'get_pi' or 'get_e'.
        """
        try:
            method = getattr(self.calc, op)
            result = method()
            self.current_input = str(float(result))
            self.display.config(text=self.current_input)
            self.entry.delete(0, tkinter.END)
            self.entry.insert(0, self.current_input)
        except (ValueError, ZeroDivisionError) as exc:
            tkinter.messagebox.showerror("Error", str(exc))

    def _toggle_scientific_mode(self) -> None:
        """Toggle visibility of scientific mode buttons."""
        self.scientific_mode = not self.scientific_mode
        if self.scientific_mode:
            for btn in self.scientific_buttons:
                btn.grid()
        else:
            for btn in self.scientific_buttons:
                btn.grid_remove()

    def destroy(self) -> None:
        """Close the root window."""
        self.root.destroy()


def launch_gui() -> None:
    """Create and run the calculator GUI.

    Creates a Tk root window, instantiates CalculatorGUI, and enters the
    tkinter event loop.  This function blocks until the window is closed.
    """
    root = tkinter.Tk()
    app = CalculatorGUI(root)
    root.mainloop()
