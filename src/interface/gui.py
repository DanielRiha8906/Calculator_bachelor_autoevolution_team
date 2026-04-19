"""Tkinter-based GUI for the Calculator application.

This module provides GuiCalculator, a graphical user interface styled after
a modern iOS calculator layout.  The interface exposes the same operation set
as the interactive CLI session, with mode switching (Normal / Scientific) via
a single toggle button, an iOS-style operation button grid, a numeric keypad,
a result display label, and a scrollable history widget.

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
# iOS-style theme constants
# ---------------------------------------------------------------------------

_THEME: dict[str, object] = {
    "bg": "#000000",                        # window / frame background
    "fg": "#FFFFFF",                        # default text colour
    "display_font": ("Courier", 32, "bold"),  # result display font
    "button_font": ("Helvetica", 18, "bold"),  # button label font
    "op_bg": "#FF9500",                     # arithmetic operator background
    "op_active": "#FFB143",                 # arithmetic operator hover
    "sci_bg": "#1C1C1E",                    # scientific button background
    "sci_active": "#2C2C2E",                # scientific button hover
    "std_bg": "#333333",                    # standard (non-op) background
    "std_active": "#4D4D4D",                # standard button hover
    "num_bg": "#505050",                    # digit button background
    "num_active": "#707070",                # digit button hover
    "toggle_bg": "#1C1C1E",                 # mode-toggle button background
    "toggle_active": "#2C2C2E",             # mode-toggle button hover
}

# Mapping of operation registry keys to their display symbols / labels.
_OP_SYMBOLS: dict[str, str] = {
    "add": "+",
    "subtract": "\u2212",   # −
    "multiply": "\u00d7",   # ×
    "divide": "\u00f7",     # ÷
    "sqrt": "\u221a",       # √
    "square": "x\u00b2",   # x²
    "cube": "x\u00b3",     # x³
    "power": "x\u02b8",    # xʸ
    "factorial": "n!",
    "log": "log",
    "ln": "ln",
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "pi": "\u03c0",         # π
    "e": "e",
}

# Arithmetic-operator keys that receive the orange iOS highlight.
_ARITHMETIC_OPS: frozenset[str] = frozenset({"add", "subtract", "multiply", "divide"})


class GuiCalculator:
    """Tkinter-based graphical calculator interface styled after iOS.

    Displays a result label (right-anchored), a mode toggle button
    (Normal / Scientific), an operation button grid (4 columns), and a
    3x4 numeric keypad.  A scrollable history widget below shows past
    calculations.  All calculation logic is delegated to the injected
    Calculator instance via OperationDispatcher; no operation logic is
    duplicated here.

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

        # Widget references populated by _setup_layout.
        self._result_label: tk.Label | None = None
        self._history_text: tk.Text | None = None
        self._op_frame: tk.Frame | None = None
        self._toggle_btn: tk.Button | None = None
        self._num_frame: tk.Frame | None = None

        self._setup_layout()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Enter the Tk main-event loop.

        Blocks until the user closes the window.
        """
        self._root.mainloop()  # type: ignore[attr-defined]

    # ------------------------------------------------------------------
    # Layout setup
    # ------------------------------------------------------------------

    def _setup_layout(self) -> None:
        """Build and grid all top-level frames and widgets.

        Layout (top to bottom):
        1. Result display label (right-anchored, black background).
        2. Mode toggle button (Single button: "Scientific" / "Normal").
        3. Operation button grid (4-column, rebuilt on mode change).
        4. Number grid (3 wide x 4 rows with digits 0-9).
        5. History text widget with vertical scrollbar.
        """
        self._root.columnconfigure(0, weight=1)  # type: ignore[attr-defined]

        # --- Result display ---
        display_frame = tk.Frame(self._root, bg=_THEME["bg"], padx=8, pady=8)
        display_frame.grid(row=0, column=0, sticky="ew")
        display_frame.columnconfigure(0, weight=1)

        self._result_label = tk.Label(
            display_frame,
            text="0",
            anchor="e",
            font=_THEME["display_font"],
            bg=_THEME["bg"],
            fg=_THEME["fg"],
            padx=8,
            pady=4,
        )
        self._result_label.grid(row=0, column=0, sticky="ew")

        # --- Mode toggle button ---
        toggle_frame = tk.Frame(self._root, bg=_THEME["bg"], padx=8, pady=4)
        toggle_frame.grid(row=1, column=0, sticky="ew")
        toggle_frame.columnconfigure(0, weight=1)

        self._toggle_btn = tk.Button(
            toggle_frame,
            text="Scientific",
            font=_THEME["button_font"],
            bg=_THEME["toggle_bg"],
            fg=_THEME["fg"],
            activebackground=_THEME["toggle_active"],
            activeforeground=_THEME["fg"],
            relief=tk.FLAT,
            bd=0,
            command=self._on_toggle_mode,
        )
        self._toggle_btn.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        self._toggle_btn.bind(
            "<Enter>",
            lambda e, b=self._toggle_btn: b.config(bg=_THEME["toggle_active"]),
        )
        self._toggle_btn.bind(
            "<Leave>",
            lambda e, b=self._toggle_btn: b.config(bg=_THEME["toggle_bg"]),
        )

        # --- Operation button grid ---
        self._op_frame = tk.Frame(self._root, bg=_THEME["bg"], padx=8, pady=4)
        self._op_frame.grid(row=2, column=0, sticky="nsew")
        self._root.rowconfigure(2, weight=0)  # type: ignore[attr-defined]
        self._setup_operation_grid()

        # --- Number grid ---
        self._num_frame = tk.Frame(self._root, bg=_THEME["bg"], padx=8, pady=4)
        self._num_frame.grid(row=3, column=0, sticky="nsew")
        self._root.rowconfigure(3, weight=0)  # type: ignore[attr-defined]
        self._setup_number_grid()

        # --- History text + scrollbar ---
        history_frame = tk.Frame(self._root, bg=_THEME["bg"], padx=8, pady=4)
        history_frame.grid(row=4, column=0, sticky="nsew")
        self._root.rowconfigure(4, weight=1)  # type: ignore[attr-defined]
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)

        self._history_text = tk.Text(
            history_frame,
            state="disabled",
            height=6,
            wrap="word",
            bg=_THEME["bg"],
            fg=_THEME["fg"],
            font=("Helvetica", 12),
            relief=tk.FLAT,
            bd=0,
        )
        self._history_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self._history_text.yview,
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._history_text.configure(yscrollcommand=scrollbar.set)

    def _setup_operation_grid(self) -> None:
        """Populate the operation button grid for the current mode.

        Clears any previously rendered buttons before rebuilding.  Buttons
        are arranged in rows of four with equal weighting so they fill the
        available width.  Symbol overrides from ``_OP_SYMBOLS`` are applied
        where available; otherwise the registry label is used verbatim.

        Color rules:
        - Arithmetic ops (add/subtract/multiply/divide): orange theme.
        - All other scientific-mode ops: dark (#1C1C1E) theme.
        - All other normal-mode ops: medium-dark (#333333) theme.
        """
        if self._op_frame is None:
            return

        # Clear existing buttons.
        for widget in self._op_frame.winfo_children():
            widget.destroy()

        available = self._get_available_operations_for_mode()
        columns = 4
        num_ops = len(available)
        num_rows = math.ceil(num_ops / columns) if num_ops else 0

        for index, (op_key, op_info) in enumerate(available.items()):
            row, col = divmod(index, columns)

            label_text = _OP_SYMBOLS.get(op_key, op_info.get("label", op_key))

            if op_key in _ARITHMETIC_OPS:
                default_bg = _THEME["op_bg"]
                hover_bg = _THEME["op_active"]
            elif self._mode is Mode.SCIENTIFIC:
                default_bg = _THEME["sci_bg"]
                hover_bg = _THEME["sci_active"]
            else:
                default_bg = _THEME["std_bg"]
                hover_bg = _THEME["std_active"]

            btn = tk.Button(
                self._op_frame,
                text=label_text,
                font=_THEME["button_font"],
                bg=default_bg,
                fg=_THEME["fg"],
                activebackground=hover_bg,
                activeforeground=_THEME["fg"],
                relief=tk.FLAT,
                bd=0,
                command=lambda k=op_key: self._on_operation_click(k),
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            btn.bind(
                "<Enter>",
                lambda e, b=btn, c=hover_bg: b.config(bg=c),
            )
            btn.bind(
                "<Leave>",
                lambda e, b=btn, c=default_bg: b.config(bg=c),
            )

        for col in range(columns):
            self._op_frame.columnconfigure(col, weight=1)
        for row in range(num_rows):
            self._op_frame.rowconfigure(row, weight=1)

    def _setup_number_grid(self) -> None:
        """Build the fixed 3x4 digit button grid.

        Grid layout::

            Row 0 | 7 | 8 | 9 |
            Row 1 | 4 | 5 | 6 |
            Row 2 | 1 | 2 | 3 |
            Row 3 |   | 0 |   |

        All three columns and all four rows have weight=1.  Each button uses
        sticky="nsew" to fill its cell.  Column 0 and column 2 of row 3 are
        intentionally empty (no widget placed).  Digit buttons do not
        currently dispatch any calculation — they are visual placeholders for
        the iOS-style layout.  Hover effects are applied.
        """
        if self._num_frame is None:
            return

        digit_layout: list[tuple[int, int, str]] = [
            (0, 0, "7"), (0, 1, "8"), (0, 2, "9"),
            (1, 0, "4"), (1, 1, "5"), (1, 2, "6"),
            (2, 0, "1"), (2, 1, "2"), (2, 2, "3"),
            (3, 1, "0"),
        ]

        for grid_row, grid_col, digit in digit_layout:
            btn = tk.Button(
                self._num_frame,
                text=digit,
                font=_THEME["button_font"],
                bg=_THEME["num_bg"],
                fg=_THEME["fg"],
                activebackground=_THEME["num_active"],
                activeforeground=_THEME["fg"],
                relief=tk.FLAT,
                bd=0,
            )
            btn.grid(
                row=grid_row,
                column=grid_col,
                padx=2,
                pady=2,
                sticky="nsew",
            )
            btn.bind(
                "<Enter>",
                lambda e, b=btn: b.config(bg=_THEME["num_active"]),
            )
            btn.bind(
                "<Leave>",
                lambda e, b=btn: b.config(bg=_THEME["num_bg"]),
            )

        for col in range(3):
            self._num_frame.columnconfigure(col, weight=1)
        for row in range(4):
            self._num_frame.rowconfigure(row, weight=1)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_toggle_mode(self) -> None:
        """Handle the mode toggle button click.

        Switches between NORMAL and SCIENTIFIC mode.  Updates the toggle
        button label first, then rebuilds the operation grid.  Calculation
        state (history, result) is not affected.
        """
        if self._mode is Mode.NORMAL:
            new_mode = Mode.SCIENTIFIC
        else:
            new_mode = Mode.NORMAL
        self._on_mode_change(new_mode)

    def _on_mode_change(self, new_mode: Mode) -> None:
        """Handle a mode change request.

        Updates the internal mode state, refreshes the toggle button text to
        reflect the *next* toggle target, and rebuilds the operation grid.

        Args:
            new_mode: The Mode value to activate.
        """
        self._mode = new_mode

        # Update toggle button label: show the mode we would switch *to*.
        if self._toggle_btn is not None:
            if self._mode is Mode.NORMAL:
                self._toggle_btn.configure(text="Scientific")
            else:
                self._toggle_btn.configure(text="Normal")

        self._setup_operation_grid()

    def _on_operation_click(self, op_key: str) -> None:
        """Handle an operation button click.

        Looks up the operation in the registry, prompts for operands via
        simple dialog boxes, executes the operation, and updates both the
        result label and the history widget.

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
