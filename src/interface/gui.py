"""Tkinter-based GUI for the Calculator application.

This module provides GuiCalculator, a graphical user interface that exposes
the same operation set as the interactive CLI session, with mode switching
(Normal / Scientific) via a single toggle button, an iOS-style operation
button grid, a number button grid, and a result display label.

Typical usage::

    import tkinter as tk
    from src.core.calculator import Calculator
    from src.interface.gui import GuiCalculator

    root = tk.Tk()
    gui = GuiCalculator(root, Calculator())
    gui.run()
"""

from __future__ import annotations

try:
    import tkinter as tk
    import tkinter.messagebox as messagebox
    import tkinter.simpledialog as simpledialog
except ImportError as _tk_err:  # noqa: F841
    # tkinter is a system-level optional dependency (not available in all
    # environments, e.g. headless CI).  The module can still be imported
    # safely; only GuiCalculator.__init__ / run() will raise at call time
    # if the runtime truly lacks a display.
    tk = None  # type: ignore[assignment]
    messagebox = None  # type: ignore[assignment]
    simpledialog = None  # type: ignore[assignment]

import math
from typing import Callable

from ..core.calculator import Calculator
from ..shared.dispatcher import OperationDispatcher
from ..shared.logger import Logger
from ..operations import OPERATIONS
from ..session.history import History
from ..session.mode import Mode
from ..session.base_mode import BaseMode


# ---------------------------------------------------------------------------
# Theme — all styling constants in one place
# ---------------------------------------------------------------------------

_THEME: dict = {
    "COLORS": {
        "bg_window": "#000000",
        "bg_display": "#000000",
        "fg_display": "#FFFFFF",
        "bg_operator": "#FF9500",
        "fg_operator": "#FFFFFF",
        "active_operator": "#FFB143",
        "bg_scientific": "#1C1C1E",
        "fg_scientific": "#FFFFFF",
        "active_scientific": "#2C2C2E",
        "bg_standard": "#333333",
        "fg_standard": "#FFFFFF",
        "active_standard": "#4D4D4D",
        "bg_number": "#333333",
        "fg_number": "#FFFFFF",
        "active_number": "#4D4D4D",
    },
    "FONTS": {
        "display": ("Courier", 32, "bold"),
        "button": ("Helvetica", 16),
    },
    "PADDING": {
        "button_padx": 2,
        "button_pady": 2,
    },
}


class GuiCalculator:
    """Tkinter-based graphical calculator interface.

    Displays a single mode toggle button (Normal / Scientific), an iOS-style
    operation button grid filtered by the current mode (rebuilt on toggle),
    a fixed 4x3 number button grid, and a result display label.  All
    calculation logic is delegated to the injected Calculator instance via
    OperationDispatcher; no operation logic is duplicated here.

    Visual layout (top to bottom):
        Row 0: Result display (right-aligned, Courier 32 bold, black bg).
        Row 1: Mode toggle button.
        Row 2: Operation button grid (dynamic, rebuilt on mode switch).
        Row 3: Number button grid (fixed 4x3, digits 0-9).

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
        self._root.configure(bg=_THEME["COLORS"]["bg_window"])  # type: ignore[attr-defined]
        self._calculator = calculator
        self._logger: Logger | None = logger
        self._dispatcher = OperationDispatcher(calculator)
        self._history = History()
        self._mode: Mode = Mode.NORMAL
        self._mode_handler = BaseMode()

        # StringVar kept for internal tracking (no longer bound to radio buttons).
        self._mode_var = tk.StringVar(value=Mode.NORMAL.value)

        # Widget references populated by _setup_layout.
        self._result_label: tk.Label | None = None
        self._history_text: tk.Text | None = None
        self._op_frame: tk.Frame | None = None
        self._mode_toggle_btn: tk.Button | None = None

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
            Row 0: Result display label (full-width, right-aligned).
            Row 1: Mode toggle button.
            Row 2: Operation button grid (rebuilt on mode change).
            Row 3: Number button grid (fixed 4x3).
        """
        colors = _THEME["COLORS"]
        self._root.columnconfigure(0, weight=1)

        # --- Row 0: Result display ---
        self._result_label = tk.Label(
            self._root,
            text="0",
            anchor="e",
            font=_THEME["FONTS"]["display"],
            bg=colors["bg_display"],
            fg=colors["fg_display"],
            padx=12,
            pady=8,
        )
        self._result_label.grid(row=0, column=0, sticky="ew")

        # --- Row 1: Mode toggle button ---
        mode_frame = tk.Frame(
            self._root,
            bg=colors["bg_window"],
            padx=8,
            pady=4,
        )
        mode_frame.grid(row=1, column=0, sticky="ew")
        mode_frame.columnconfigure(0, weight=1)

        toggle_label = self._mode_toggle_label()
        self._mode_toggle_btn = tk.Button(
            mode_frame,
            text=toggle_label,
            font=_THEME["FONTS"]["button"],
            bg=colors["bg_scientific"],
            fg=colors["fg_scientific"],
            activebackground=colors["active_scientific"],
            activeforeground=colors["fg_scientific"],
            bd=0,
            relief="flat",
            padx=_THEME["PADDING"]["button_padx"],
            pady=_THEME["PADDING"]["button_pady"],
            command=self._on_mode_toggle,
        )
        self._mode_toggle_btn.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        self._bind_hover(
            self._mode_toggle_btn,
            colors["bg_scientific"],
            colors["active_scientific"],
        )

        # --- Row 2: Operation button grid ---
        self._op_frame = tk.Frame(
            self._root,
            bg=colors["bg_window"],
            padx=8,
            pady=4,
        )
        self._op_frame.grid(row=2, column=0, sticky="nsew")
        self._root.rowconfigure(2, weight=0)
        self._setup_operation_grid()

        # --- Row 3: Number button grid ---
        num_frame = tk.Frame(
            self._root,
            bg=colors["bg_window"],
            padx=8,
            pady=4,
        )
        num_frame.grid(row=3, column=0, sticky="nsew")
        self._root.rowconfigure(3, weight=0)
        self._setup_number_grid(num_frame)

    def _setup_operation_grid(self) -> None:
        """Populate the operation button grid for the current mode.

        Clears any previously rendered buttons before rebuilding.  Buttons
        are arranged in rows of four.  Color is determined by operation type
        via _get_operation_color_group().  Button label is the symbolic
        representation via _get_operation_symbol().
        """
        if self._op_frame is None:
            return

        colors = _THEME["COLORS"]
        padding = _THEME["PADDING"]

        # Clear existing buttons.
        for widget in self._op_frame.winfo_children():
            widget.destroy()

        available = self._get_available_operations_for_mode()
        columns = 4
        num_ops = len(available)
        rows = math.ceil(num_ops / columns) if num_ops > 0 else 0

        for index, op_key in enumerate(available.keys()):
            row, col = divmod(index, columns)
            color_group = self._get_operation_color_group(op_key)

            bg_key = f"bg_{color_group}"
            fg_key = f"fg_{color_group}"
            active_key = f"active_{color_group}"

            bg_color = colors[bg_key]
            fg_color = colors[fg_key]
            active_color = colors[active_key]

            symbol = self._get_operation_symbol(op_key)

            btn = tk.Button(
                self._op_frame,
                text=symbol,
                font=_THEME["FONTS"]["button"],
                bg=bg_color,
                fg=fg_color,
                activebackground=active_color,
                activeforeground=fg_color,
                bd=0,
                relief="flat",
                padx=padding["button_padx"],
                pady=padding["button_pady"],
                command=lambda k=op_key: self._on_operation_click(k),
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self._bind_hover(btn, bg_color, active_color)

        for col in range(columns):
            self._op_frame.columnconfigure(col, weight=1)
        for r in range(rows):
            self._op_frame.rowconfigure(r, weight=1)

    def _setup_number_grid(self, parent: tk.Frame) -> None:
        """Build the fixed 4x3 number button grid inside *parent*.

        Layout (row, col):
            Row 0: 1, 2, 3
            Row 1: 4, 5, 6
            Row 2: 7, 8, 9
            Row 3: 0, (empty), (empty)

        Number buttons share the same bg/fg as standard buttons.  Clicking
        a digit appends it to the current display value (future wiring point).

        Args:
            parent: The frame that will contain the number buttons.
        """
        colors = _THEME["COLORS"]
        padding = _THEME["PADDING"]

        layout = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
            ["0", None, None],
        ]

        for row_idx, row_digits in enumerate(layout):
            for col_idx, digit in enumerate(row_digits):
                if digit is None:
                    # Empty placeholder — spacer frame to preserve grid shape.
                    spacer = tk.Frame(
                        parent,
                        bg=colors["bg_window"],
                    )
                    spacer.grid(
                        row=row_idx,
                        column=col_idx,
                        padx=padding["button_padx"],
                        pady=padding["button_pady"],
                        sticky="nsew",
                    )
                else:
                    btn = tk.Button(
                        parent,
                        text=digit,
                        font=_THEME["FONTS"]["button"],
                        bg=colors["bg_number"],
                        fg=colors["fg_number"],
                        activebackground=colors["active_number"],
                        activeforeground=colors["fg_number"],
                        bd=0,
                        relief="flat",
                        padx=padding["button_padx"],
                        pady=padding["button_pady"],
                    )
                    btn.grid(
                        row=row_idx,
                        column=col_idx,
                        padx=2,
                        pady=2,
                        sticky="nsew",
                    )
                    self._bind_hover(btn, colors["bg_number"], colors["active_number"])

            parent.columnconfigure(col_idx, weight=1)

        for r in range(len(layout)):
            parent.rowconfigure(r, weight=1)

    # ------------------------------------------------------------------
    # Theme helpers
    # ------------------------------------------------------------------

    def _get_operation_symbol(self, op_key: str) -> str:
        """Return the display symbol for the given operation key.

        Args:
            op_key: An operation key present in the OPERATIONS registry.

        Returns:
            A Unicode symbol string for the operation, or the operation key
            itself if no symbol mapping is defined.
        """
        _SYMBOLS: dict[str, str] = {
            "add": "+",
            "subtract": "\u2212",
            "multiply": "\u00d7",
            "divide": "\u00f7",
            "sqrt": "\u221a",
            "square": "x\u00b2",
            "cube": "x\u00b3",
            "power": "x\u02b8",
            "factorial": "n!",
            "log": "log",
            "ln": "ln",
            "sin": "sin",
            "cos": "cos",
            "tan": "tan",
            "pi": "\u03c0",
            "e": "e",
        }
        return _SYMBOLS.get(op_key, op_key)

    def _get_operation_color_group(self, op_key: str) -> str:
        """Return the color-group name for the given operation.

        Args:
            op_key: An operation key present in the OPERATIONS registry.

        Returns:
            "operator" for basic arithmetic operations (add, subtract,
            multiply, divide), "scientific" for all other operations when
            in scientific mode, or "standard" for other operations in
            normal mode.
        """
        _OPERATORS = {"add", "subtract", "multiply", "divide"}
        if op_key in _OPERATORS:
            return "operator"
        if self._mode == Mode.SCIENTIFIC:
            return "scientific"
        return "standard"

    def _bind_hover(
        self,
        button: tk.Button,
        default_bg: str,
        hover_bg: str,
    ) -> None:
        """Bind hover color effects to *button*.

        On <Enter> the button background switches to *hover_bg*; on <Leave>
        it is restored to *default_bg*.

        Args:
            button: The tkinter Button widget to bind.
            default_bg: The background color when the cursor is not over the button.
            hover_bg: The background color when the cursor hovers over the button.
        """
        button.bind("<Enter>", lambda _event, b=button, c=hover_bg: b.configure(bg=c))
        button.bind("<Leave>", lambda _event, b=button, c=default_bg: b.configure(bg=c))

    # ------------------------------------------------------------------
    # Mode toggle
    # ------------------------------------------------------------------

    def _mode_toggle_label(self) -> str:
        """Return the label for the mode toggle button given the current mode.

        Returns:
            "scientific" when the current mode is NORMAL (clicking will switch
            to scientific), or "normal" when the current mode is SCIENTIFIC.
        """
        if self._mode == Mode.NORMAL:
            return "scientific"
        return "normal"

    def _on_mode_toggle(self) -> None:
        """Handle a click on the mode toggle button.

        Flips the mode between NORMAL and SCIENTIFIC, updates the toggle
        button label, and rebuilds the operation grid.
        """
        new_mode = Mode.SCIENTIFIC if self._mode == Mode.NORMAL else Mode.NORMAL
        self._on_mode_change(new_mode)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_mode_change(self, new_mode: Mode) -> None:
        """Handle a mode change request.

        Updates the internal mode state, updates the toggle button label,
        and rebuilds the operation grid to reflect the newly available
        operations.

        Args:
            new_mode: The Mode value to switch to.
        """
        self._mode = new_mode
        self._mode_var.set(new_mode.value)
        if self._mode_toggle_btn is not None:
            self._mode_toggle_btn.configure(text=self._mode_toggle_label())
        self._setup_operation_grid()

    def _on_operation_click(self, op_key: str) -> None:
        """Handle an operation button click.

        Looks up the operation in the registry, prompts for operands via
        simple dialog boxes, executes the operation, and updates the result
        label.

        Args:
            op_key: The operation key identifying the button that was clicked.
        """
        op_info = OPERATIONS[op_key]
        arity: int = op_info["arity"]
        coerce: Callable = op_info.get("coerce", float)  # type: ignore[assignment]

        operands = self._prompt_operands_dialog(op_key, arity, coerce)
        if operands is None:
            # User cancelled one of the dialogs.
            return

        self._execute_operation(op_key, operands)

    def _prompt_operands_dialog(
        self,
        op_key: str,
        arity: int,
        coerce: Callable,
    ) -> list | None:
        """Show dialog boxes to collect operands for the operation.

        One dialog is shown per required operand.  If the user cancels any
        dialog, or if the value cannot be coerced to the required type, the
        method returns None (no silent failure — an error dialog is shown
        for invalid input, but cancel is treated as an abort).

        Args:
            op_key: The operation key, used in the dialog title.
            arity: Number of operands to collect (0, 1, or 2).
            coerce: Callable used to convert the raw string (e.g. float or int).

        Returns:
            A list of coerced operand values, or None if collection was
            cancelled or a coercion error occurred.
        """
        operands: list = []
        labels = ["first", "second"] if arity == 2 else [""]
        for label in labels[:arity]:
            prompt_text = f"Enter {label + ' ' if label else ''}operand for '{op_key}':"
            raw = simpledialog.askstring(
                title=op_key,
                prompt=prompt_text,
                parent=self._root,
            )
            if raw is None:
                # User pressed Cancel.
                return None
            raw = raw.strip()
            try:
                coerced = self._dispatcher.coerce_operands([raw], coerce)
                operands.extend(coerced)
            except ValueError as exc:
                if self._logger is not None:
                    self._logger.log_invalid_operand(raw, "<numeric>")
                self._show_error_dialog("Invalid Operand", str(exc))
                return None
        return operands

    def _execute_operation(self, op_key: str, operands: list) -> None:
        """Execute *op_key* with *operands* and update the display.

        Delegates the actual calculation to OperationDispatcher.dispatch().
        Catches domain errors and zero-division and shows them in an error
        dialog rather than crashing.

        Args:
            op_key: A key present in the OPERATIONS registry.
            operands: A list of already-coerced operand values.
        """
        if self._logger is None:
            self._logger = Logger()

        try:
            result = self._dispatcher.dispatch(op_key, operands)
        except ZeroDivisionError:
            self._logger.log_division_by_zero(operands)
            self._show_error_dialog(
                "Division by Zero",
                "Division by zero is not allowed.",
            )
            return
        except ValueError as exc:
            self._logger.log_domain_error(op_key, str(exc))
            self._show_error_dialog("Domain Error", str(exc))
            return
        except TypeError as exc:
            self._logger.log_domain_error(op_key, str(exc))
            self._show_error_dialog("Type Error", str(exc))
            return

        self._history.add_operation(op_key, operands, result)
        self._update_result_display(result)
        self._update_history_display()

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def _update_result_display(self, result: float | int) -> None:
        """Update the result label with the latest computation result.

        Args:
            result: The numeric result to display.
        """
        if self._result_label is not None:
            self._result_label.configure(text=str(result))

    def _update_history_display(self) -> None:
        """Refresh the history text widget from the current History entries."""
        if self._history_text is None:
            return
        entries = self._history.get_all()
        self._history_text.configure(state="normal")
        self._history_text.delete("1.0", "end")
        self._history_text.insert("end", "\n".join(entries))
        self._history_text.configure(state="disabled")
        self._history_text.see("end")

    def _get_available_operations_for_mode(self) -> dict:
        """Return the operation dict filtered for the current mode.

        Delegates to the composed BaseMode instance.

        Returns:
            A dict mapping operation keys to registry entries accessible in
            the current mode.
        """
        return self._mode_handler.get_available_operations(self._mode)

    def _show_error_dialog(self, title: str, message: str) -> None:
        """Display a modal error dialog.

        Args:
            title: The dialog window title.
            message: The error message body.
        """
        messagebox.showerror(title=title, message=message, parent=self._root)
