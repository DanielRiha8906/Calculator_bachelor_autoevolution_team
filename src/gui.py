"""Tkinter-based graphical calculator GUI.

This module provides a CalculatorGUI class that wraps a Calculator instance
in a simple tkinter window, and a launch_gui() entry-point function.
"""

import tkinter

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
    """

    def __init__(self, root: object | None = None) -> None:
        """Initialise the calculator GUI.

        Args:
            root: Optional tkinter root window.  When None, a new Tk() window
                is created automatically.
        """
        self.calc: Calculator = Calculator()
        self.current_input: str = ""
        self.pending_op: str | None = None
        self.first_operand: float | None = None

        # Create or accept the root window.
        if root is None:
            self.root = tkinter.Tk()
        else:
            self.root = root

        self.root.title("Calculator")

        # Build widgets.  When tkinter is mocked the constructors return
        # MagicMock objects, which is fine — we just need the attributes to
        # exist and be non-None.
        self.entry = tkinter.Entry(self.root)
        self.display = tkinter.Label(self.root)

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
                'factorial', 'log', 'ln'.

        Returns:
            The computed result as a float, or None if an error occurred.
        """
        try:
            x = float(self.current_input)
            method = getattr(self.calc, op)
            result = method(x)
            result_float = float(result)
            self.display.config(text=str(result_float))
            self.current_input = str(result_float)
            return result_float
        except (ValueError, ZeroDivisionError) as exc:
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

        try:
            method = getattr(self.calc, self.pending_op)
            result = method(self.first_operand, second)
            result_float = float(result)
            self.display.config(text=str(result_float))
            self.current_input = str(result_float)
            return result_float
        except (ValueError, ZeroDivisionError) as exc:
            tkinter.messagebox.showerror("Error", str(exc))
            return None

    def _clear(self) -> None:
        """Reset the calculator state and update the display."""
        self.current_input = ""
        self.pending_op = None
        self.first_operand = None
        self.display.config(text="0")

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
