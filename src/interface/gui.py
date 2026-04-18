"""Tkinter-based GUI for the Calculator application.

This module provides GuiCalculator, a graphical user interface that exposes
the same operation set as the interactive CLI session, with mode switching
(Normal / Scientific) via a toggle button, an operation button grid, and a
result display label.

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

from typing import Callable

from ..core.calculator import Calculator
from ..shared.dispatcher import OperationDispatcher
from ..shared.logger import Logger
from ..operations import OPERATIONS
from ..session.history import History
from ..session.mode import Mode
from ..session.base_mode import BaseMode


# ---------------------------------------------------------------------------
# Module-level theme and symbol constants
# ---------------------------------------------------------------------------

_THEME: dict[str, object] = {
    "window_bg": "#000000",
    "display_bg": "#000000",
    "display_fg": "#FFFFFF",
    "display_font": ("Courier", 32, "bold"),
    "btn_operator_bg": "#FF9500",
    "btn_operator_fg": "#FFFFFF",
    "btn_operator_active": "#FFB143",
    "btn_scientific_bg": "#1C1C1E",
    "btn_scientific_fg": "#FFFFFF",
    "btn_scientific_active": "#2C2C2E",
    "btn_normal_bg": "#333333",
    "btn_normal_fg": "#FFFFFF",
    "btn_normal_active": "#4D4D4D",
    "mode_toggle_bg": "#1C1C1E",
    "mode_toggle_fg": "#FFFFFF",
    "mode_toggle_active": "#2C2C2E",
}

_SYMBOL_MAP: dict[str, str] = {
    "add": "+",
    "subtract": "−",
    "multiply": "×",
    "divide": "÷",
    "sqrt": "√",
    "square": "x²",
    "cube": "x³",
    "power": "xʸ",
    "factorial": "n!",
    "log": "log",
    "ln": "ln",
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "pi": "π",
    "e": "e",
}


class GuiCalculator:
    """Tkinter-based graphical calculator interface.

    Displays an iOS-style dark-themed layout with a mode toggle button
    (Normal / Scientific), an operation button grid filtered by the current
    mode, and a result label.  All calculation logic is delegated to the
    injected Calculator instance via OperationDispatcher; no operation logic
    is duplicated here.

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
        self._calculator = calculator
        self._logger: Logger | None = logger
        self._dispatcher = OperationDispatcher(calculator)
        self._history = History()
        self._mode: Mode = Mode.NORMAL
        self._mode_handler = BaseMode()

        # Widget references populated by _setup_layout.
        self._result_label: tk.Label | None = None
        self._mode_toggle_btn: tk.Button | None = None
        self._btn_frame: tk.Frame | None = None
        # Legacy attribute stubs retained for API compatibility.
        self._history_text: tk.Text | None = None
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
        """Build all top-level frames and widgets using the iOS-style theme.

        Layout (top to bottom):
        1. Result display label (right-aligned, large font).
        2. Mode toggle button (switches between Normal and Scientific).
        3. Operation button grid (rebuilt on mode change).
        """
        self._root.configure(bg=_THEME["window_bg"])  # type: ignore[attr-defined]

        # --- Display area ---
        display_frame = tk.Frame(self._root, bg=_THEME["display_bg"])
        display_frame.pack(fill="x")

        self._result_label = tk.Label(
            display_frame,
            anchor="e",
            bg=_THEME["display_bg"],
            fg=_THEME["display_fg"],
            font=_THEME["display_font"],
            text="0",
            padx=10,
            pady=10,
        )
        self._result_label.pack(fill="x")

        # --- Mode toggle button ---
        toggle_frame = tk.Frame(self._root, bg=_THEME["window_bg"])
        toggle_frame.pack(fill="x")

        self._mode_toggle_btn = tk.Button(
            toggle_frame,
            text="scientific",
            bg=_THEME["mode_toggle_bg"],
            fg=_THEME["mode_toggle_fg"],
            activebackground=_THEME["mode_toggle_active"],
            relief="flat",
            borderwidth=0,
            command=self._on_mode_toggle,
        )
        self._mode_toggle_btn.pack(fill="x")

        # Hover bindings for mode toggle button.
        self._mode_toggle_btn.bind(
            "<Enter>",
            lambda e: self._mode_toggle_btn.config(bg=_THEME["mode_toggle_active"]),  # type: ignore[union-attr]
        )
        self._mode_toggle_btn.bind(
            "<Leave>",
            lambda e: self._mode_toggle_btn.config(bg=_THEME["mode_toggle_bg"]),  # type: ignore[union-attr]
        )

        # --- Button grid ---
        self._btn_frame = tk.Frame(self._root, bg=_THEME["window_bg"])
        self._btn_frame.pack(fill="both", expand=True)

        self._build_button_grid()

    # ------------------------------------------------------------------
    # Button grid construction
    # ------------------------------------------------------------------

    def _build_button_grid(self) -> None:
        """Build the 4-column button grid for the current mode."""
        if self._btn_frame is None:
            return

        available = self._get_available_operations_for_mode()
        num_cols = 4

        for i in range(num_cols):
            self._btn_frame.columnconfigure(i, weight=1)

        for idx, (op_key, _op_meta) in enumerate(available.items()):
            row = idx // num_cols
            col = idx % num_cols
            label = _SYMBOL_MAP.get(op_key, op_key)
            bg, fg, active_bg = self._get_button_colors(op_key)

            btn = tk.Button(
                self._btn_frame,
                text=label,
                bg=bg,
                fg=fg,
                activebackground=active_bg,
                activeforeground=fg,
                relief="flat",
                borderwidth=0,
                command=lambda k=op_key: self._on_operation_click(k),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
            self._btn_frame.rowconfigure(row, weight=1)

            # Hover bindings.
            btn.bind("<Enter>", lambda e, b=btn, c=active_bg: b.config(bg=c))
            btn.bind("<Leave>", lambda e, b=btn, c=bg: b.config(bg=c))

    def _rebuild_button_grid(self) -> None:
        """Destroy existing buttons and rebuild the grid for the current mode."""
        if self._btn_frame is None:
            return
        for widget in self._btn_frame.winfo_children():
            widget.destroy()
        self._build_button_grid()

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------

    def _get_button_colors(self, op_key: str) -> tuple[str, str, str]:
        """Return (bg, fg, activebackground) for the given operation key.

        Operator buttons (add, subtract, multiply, divide) receive the orange
        operator accent colour.  In scientific mode all other buttons use the
        dark scientific style; in normal mode they use the slightly lighter
        normal style.

        Args:
            op_key: The operation key from the OPERATIONS registry.

        Returns:
            A 3-tuple of (background, foreground, active-background) colour
            strings.
        """
        operators = {"add", "subtract", "multiply", "divide"}
        if op_key in operators:
            return (
                str(_THEME["btn_operator_bg"]),
                str(_THEME["btn_operator_fg"]),
                str(_THEME["btn_operator_active"]),
            )
        if self._mode == Mode.SCIENTIFIC:
            return (
                str(_THEME["btn_scientific_bg"]),
                str(_THEME["btn_scientific_fg"]),
                str(_THEME["btn_scientific_active"]),
            )
        return (
            str(_THEME["btn_normal_bg"]),
            str(_THEME["btn_normal_fg"]),
            str(_THEME["btn_normal_active"]),
        )

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_mode_toggle(self) -> None:
        """Handle the mode toggle button click.

        Switches between NORMAL and SCIENTIFIC mode and rebuilds the button
        grid to reflect the newly available operations.
        """
        if self._mode == Mode.NORMAL:
            self._mode = Mode.SCIENTIFIC
            self._mode_toggle_btn.config(text="normal")  # type: ignore[union-attr]
        else:
            self._mode = Mode.NORMAL
            self._mode_toggle_btn.config(text="scientific")  # type: ignore[union-attr]
        self._rebuild_button_grid()

    def _on_mode_change(self, new_mode: Mode) -> None:
        """Handle a mode change (legacy compatibility entry point).

        Updates the internal mode state and rebuilds the operation grid to
        reflect the newly available operations.  This method mirrors the
        radio-button driven approach from the previous design and is retained
        so that existing callers (tests and any programmatic users) continue
        to work without modification.

        Args:
            new_mode: The Mode value to switch to.
        """
        self._mode = new_mode
        self._rebuild_button_grid()

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
        """Refresh the history text widget from the current History entries.

        This method is a no-op when the ``_history_text`` widget is None (i.e.
        when the iOS-style layout is active and no text widget exists).  It
        remains part of the public API so that test code that injects a mock
        ``_history_text`` can still exercise history formatting logic.
        """
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
