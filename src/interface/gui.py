"""Tkinter-based GUI for the Calculator application.

This module provides GuiCalculator, a graphical user interface that exposes
the same operation set as the interactive CLI session, with mode switching
(Normal / Scientific) via radio buttons, an operation button grid, a result
display label, and a scrollable history widget.

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


class GuiCalculator:
    """Tkinter-based graphical calculator interface.

    Displays mode radio buttons (Normal / Scientific), an operation button
    grid filtered by the current mode, a result label, and a scrollable
    history widget.  All calculation logic is delegated to the injected
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
        self._calculator = calculator
        self._logger: Logger | None = logger
        self._dispatcher = OperationDispatcher(calculator)
        self._history = History()
        self._mode: Mode = Mode.NORMAL
        self._mode_handler = BaseMode()

        # StringVar used by the mode radio buttons.
        self._mode_var = tk.StringVar(value=Mode.NORMAL.value)

        # Widget references populated by _setup_layout.
        self._result_label: tk.Label | None = None
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
        """Build and grid all top-level frames and widgets.

        Layout (top to bottom):
        1. Mode selector row (Normal / Scientific radio buttons).
        2. Operation button grid (rebuilt on mode change).
        3. Result display label.
        4. History text widget with vertical scrollbar.
        """
        self._root.columnconfigure(0, weight=1)

        # --- Mode selector ---
        mode_frame = tk.Frame(self._root, padx=8, pady=4)
        mode_frame.grid(row=0, column=0, sticky="ew")
        self._setup_mode_selector(mode_frame)

        # --- Operation button grid ---
        self._op_frame = tk.Frame(self._root, padx=8, pady=4)
        self._op_frame.grid(row=1, column=0, sticky="nsew")
        self._root.rowconfigure(1, weight=0)
        self._setup_operation_grid()

        # --- Result label ---
        self._result_label = tk.Label(
            self._root,
            text="Result: —",
            anchor="w",
            font=("TkDefaultFont", 12, "bold"),
            padx=8,
            pady=4,
        )
        self._result_label.grid(row=2, column=0, sticky="ew")

        # --- History text + scrollbar ---
        history_frame = tk.Frame(self._root, padx=8, pady=4)
        history_frame.grid(row=3, column=0, sticky="nsew")
        self._root.rowconfigure(3, weight=1)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)

        self._history_text = tk.Text(
            history_frame,
            state="disabled",
            height=8,
            wrap="word",
        )
        self._history_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self._history_text.yview,
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._history_text.configure(yscrollcommand=scrollbar.set)

    def _setup_mode_selector(self, parent: tk.Frame) -> None:
        """Add Normal/Scientific radio buttons to *parent*.

        Args:
            parent: The frame that will contain the radio buttons.
        """
        tk.Label(parent, text="Mode:").pack(side="left")
        for mode in Mode:
            tk.Radiobutton(
                parent,
                text=mode.value.capitalize(),
                variable=self._mode_var,
                value=mode.value,
                command=lambda m=mode: self._on_mode_change(m),
            ).pack(side="left", padx=4)

    def _setup_operation_grid(self) -> None:
        """Populate the operation button grid for the current mode.

        Clears any previously rendered buttons before rebuilding.  Buttons
        are arranged in rows of four.
        """
        if self._op_frame is None:
            return

        # Clear existing buttons.
        for widget in self._op_frame.winfo_children():
            widget.destroy()

        available = self._get_available_operations_for_mode()
        columns = 4
        for index, (op_key, op_info) in enumerate(available.items()):
            row, col = divmod(index, columns)
            btn = tk.Button(
                self._op_frame,
                text=op_info["label"],
                width=24,
                command=lambda k=op_key: self._on_operation_click(k),
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")

        for col in range(columns):
            self._op_frame.columnconfigure(col, weight=1)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_mode_change(self, new_mode: Mode) -> None:
        """Handle a mode radio-button selection change.

        Updates the internal mode state and rebuilds the operation grid to
        reflect the newly available operations.

        Args:
            new_mode: The Mode value that was selected.
        """
        self._mode = new_mode
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
            self._result_label.configure(text=f"Result: {result}")

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
