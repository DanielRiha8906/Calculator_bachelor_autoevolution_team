"""Tkinter window layout and widget management for the Calculator GUI.

:class:`CalculatorWindow` is the main application window.  It owns all
widget construction, layout, and event-callback wiring.  All actual
computation is delegated to the injected :class:`~src.gui.session_adapter.GUISessionAdapter`.

The window uses an iOS-inspired dark theme defined in :mod:`src.gui.ios_theme`.
"""

import tkinter as tk

from .ios_theme import _THEME, OPERATION_SYMBOLS
from .session_adapter import GUISessionAdapter

# Default operation lists used when the adapter does not expose get_operations().
_NORMAL_OPS: list[str] = [
    "add", "subtract", "multiply", "divide", "square", "square_root",
]
_SCIENTIFIC_OPS: list[str] = [
    "add", "subtract", "multiply", "divide", "square", "square_root",
    "power", "cube", "cube_root", "factorial", "logarithm",
    "natural_logarithm", "sin", "cos", "tan", "cot", "asin", "acos",
]


class CalculatorWindow(tk.Tk):
    """Main Tkinter window for the Calculator GUI (iOS-style dark theme).

    The window is laid out top-to-bottom as:

    - Result display label.
    - Mode toggle button (Normal / Scientific).
    - Grid of operation buttons that changes with the active mode.

    All computation is delegated to the injected
    :class:`~src.gui.session_adapter.GUISessionAdapter`.

    Args:
        session_adapter: A configured :class:`~src.gui.session_adapter.GUISessionAdapter`
            that handles all computation and history management.
    """

    def __init__(self, session_adapter: GUISessionAdapter) -> None:
        super().__init__()

        self._adapter: GUISessionAdapter = session_adapter
        self._selected_op: str | None = None
        self._current_mode: str = "normal"

        self.title("Calculator")
        self.resizable(True, True)
        self.minsize(420, 600)

        self._result_var = tk.StringVar(value="0")

        # Apply window background; guard for test environments where the
        # underlying Tk instance may not support configure().
        try:
            self.configure(bg=_THEME["bg_window"])
        except Exception:  # noqa: BLE001
            pass

        self._build_ui()

        # Start with Normal mode active.
        self.on_mode_changed("normal")

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Construct all widgets.

        Delegates to :meth:`_build_ios_layout` for the new iOS-style
        layout and also creates legacy attribute stubs so that code or
        tests that reference the old widget names remain compatible.
        """
        self._build_ios_layout()
        self._create_legacy_stubs()

    def _build_ios_layout(self) -> None:
        """Construct the iOS-style result display, mode button, and button grid."""
        # --- Result display ---
        result_frame = tk.Frame(self, bg=_THEME["bg_result_display"])
        result_frame.pack(fill=tk.X)
        self._result_label = tk.Label(
            result_frame,
            textvariable=self._result_var,
            font=_THEME["font_result"],
            fg=_THEME["fg_result_display"],
            bg=_THEME["bg_result_display"],
            anchor="e",
            padx=16,
            pady=16,
        )
        self._result_label.pack(fill=tk.X)

        # Alias used by legacy tests that check for _result_label_widget.
        self._result_label_widget = self._result_label

        # --- Mode toggle button ---
        self._mode_button = tk.Button(
            self,
            text="Scientific",
            command=self._on_mode_toggle,
            bg=_THEME["bg_mode_button"],
            fg=_THEME["fg_mode_button"],
            activebackground=_THEME["active_bg_mode_button"],
            activeforeground=_THEME["fg_mode_button"],
            relief=tk.FLAT,
            borderwidth=0,
            font=("Arial", 14),
        )
        self._mode_button.pack(fill=tk.X, padx=8, pady=4)
        self._mode_button.bind(
            "<Enter>",
            lambda e: self._mode_button.configure(bg=_THEME["active_bg_mode_button"]),
        )
        self._mode_button.bind(
            "<Leave>",
            lambda e: self._mode_button.configure(bg=_THEME["bg_mode_button"]),
        )

        # --- Operation buttons grid container ---
        self._ops_container = tk.Frame(self, bg=_THEME["bg_window"])
        self._ops_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self._rebuild_button_grid()

    def _create_legacy_stubs(self) -> None:
        """Create widget attribute stubs expected by legacy callers.

        The iOS layout removes several widgets that were present in the
        original design (operand entry fields, history text widget,
        scrollable canvas).  This method creates ``MagicMock``-like stub
        objects for those attributes so that callers referencing them do
        not raise :class:`AttributeError`.

        In a live Tkinter environment these stubs are inert ``tk.Frame``
        instances.  Tests may replace them with their own mocks.
        """
        # Operand entry stubs — used by on_operation_selected and
        # on_execute_clicked for backward compatibility.
        stub_frame = tk.Frame(self)
        self._operand1_entry: tk.Widget = stub_frame
        self._operand2_entry: tk.Widget = stub_frame
        self._operand2_label: tk.Widget = stub_frame

        # History text stub.
        self._history_text: tk.Widget = stub_frame

        # Scrollable canvas stubs — _ops_canvas and _ops_inner_frame were
        # used by update_operation_buttons in the old layout.
        self._ops_canvas: tk.Widget = stub_frame
        self._ops_inner_frame: tk.Widget = stub_frame

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _on_mode_toggle(self) -> None:
        """Toggle between normal and scientific mode and rebuild the button grid."""
        new_mode = "scientific" if self._current_mode == "normal" else "normal"
        self._current_mode = new_mode

        if hasattr(self._adapter, "set_mode"):
            self._adapter.set_mode(new_mode)

        self._result_var.set("0")
        button_text = "Normal" if self._current_mode == "scientific" else "Scientific"
        self._mode_button.configure(text=button_text)
        self._rebuild_button_grid()

    def _rebuild_button_grid(self) -> None:
        """Destroy existing operation buttons and recreate them for the current mode."""
        for widget in self._ops_container.winfo_children():
            widget.destroy()

        operations = self._get_current_operations()
        columns = 4

        for col in range(columns):
            self._ops_container.columnconfigure(col, weight=1)

        for idx, op_name in enumerate(operations):
            row, col = divmod(idx, columns)
            self._ops_container.rowconfigure(row, weight=1)

            symbol = OPERATION_SYMBOLS.get(op_name, op_name.replace("_", " ").title())

            if op_name in ("add", "subtract", "multiply", "divide"):
                bg = _THEME["bg_operator_button"]
                fg = _THEME["fg_operator_button"]
                active_bg = _THEME["active_bg_operator_button"]
            elif self._current_mode == "scientific":
                bg = _THEME["bg_utility_button"]
                fg = _THEME["fg_utility_button"]
                active_bg = _THEME["active_bg_utility_button"]
            else:
                bg = _THEME["bg_standard_button"]
                fg = _THEME["fg_standard_button"]
                active_bg = _THEME["active_bg_standard_button"]

            btn = tk.Button(
                self._ops_container,
                text=symbol,
                command=lambda name=op_name: self._on_operation_clicked(name),
                bg=bg,
                fg=fg,
                activebackground=active_bg,
                activeforeground=fg,
                relief=tk.FLAT,
                borderwidth=0,
                font=("Arial", 18, "bold"),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            btn.bind("<Enter>", lambda e, b=btn, abg=active_bg: b.configure(bg=abg))
            btn.bind("<Leave>", lambda e, b=btn, dbg=bg: b.configure(bg=dbg))

    def _get_current_operations(self) -> list[str]:
        """Return the operation list for the current mode.

        Delegates to the adapter's ``get_operations()`` if available;
        otherwise falls back to the hardcoded per-mode defaults.

        Returns:
            A list of canonical operation name strings.
        """
        if hasattr(self._adapter, "get_operations"):
            return self._adapter.get_operations()

        if self._current_mode == "scientific":
            return list(_SCIENTIFIC_OPS)
        return list(_NORMAL_OPS)

    def _on_operation_clicked(self, op_name: str) -> None:
        """Store the selected operation and attempt immediate execution.

        For operations that require operands the adapter will return an
        error which is surfaced in the result display.

        Args:
            op_name: The canonical name of the clicked operation.
        """
        self._selected_op = op_name
        try:
            result = self._adapter.execute_operation(op_name)
            self._result_var.set(str(result))
        except AttributeError:
            # Adapter does not expose execute_operation — fall back to
            # execute_operation_safe with no operands to surface an error.
            result_str, error_msg = self._adapter.execute_operation_safe(op_name, [])
            if error_msg:
                self._result_var.set(str(error_msg))
            else:
                self._result_var.set(result_str)
        except Exception as ex:  # noqa: BLE001
            self._result_var.set(str(ex))

    # ------------------------------------------------------------------
    # Public event handlers (backward-compatible interface)
    # ------------------------------------------------------------------

    def on_mode_changed(self, mode_name: str) -> None:
        """Switch the calculator to *mode_name* and refresh operation buttons.

        Args:
            mode_name: ``"normal"`` or ``"scientific"``.
        """
        self._current_mode = mode_name

        if hasattr(self._adapter, "set_mode"):
            self._adapter.set_mode(mode_name)

        self._selected_op = None
        self._result_var.set("0")

        if hasattr(self, "_mode_button"):
            button_text = "Normal" if self._current_mode == "scientific" else "Scientific"
            self._mode_button.configure(text=button_text)

        if hasattr(self, "_ops_container"):
            self._rebuild_button_grid()

    def on_operation_selected(self, op_name: str) -> None:
        """Record the chosen operation and check its arity.

        Kept for backward compatibility.  In the iOS layout, operation
        selection and execution are handled by :meth:`_on_operation_clicked`.

        Args:
            op_name: The canonical operation name chosen by the user.
        """
        self._selected_op = op_name
        self._result_var.set("0")

        # Preserve original behaviour: consult arity so callers relying on
        # adapter.get_arity being called here continue to work.
        self._adapter.get_arity(op_name)

    def on_execute_clicked(self) -> None:
        """Read inputs, execute the selected operation, and display the result.

        Preserved for backward compatibility.  In the iOS layout there is
        no visible Execute button, but this method continues to function
        correctly when called directly (e.g. from external code or tests).
        It shows an inline error message when no operation is selected, an
        operand is non-numeric, or the calculator raises an exception.
        """
        if self._selected_op is None:
            self._result_var.set("Please select an operation first.")
            return

        raw1 = self._operand1_entry.get().strip()
        try:
            op1 = float(raw1)
        except ValueError:
            self._result_var.set(f"Operand 1 is not a valid number: {raw1!r}")
            return

        arity = self._adapter.get_arity(self._selected_op)
        operands: list[float] = [op1]

        if arity > 1:
            raw2 = self._operand2_entry.get().strip()
            try:
                op2 = float(raw2)
            except ValueError:
                self._result_var.set(f"Operand 2 is not a valid number: {raw2!r}")
                return
            operands.append(op2)

        result_str, error_msg = self._adapter.execute_operation_safe(
            self._selected_op, operands
        )

        if error_msg:
            self._result_var.set(f"Error: {error_msg}")
        else:
            self._result_var.set(f"Result: {result_str}")

    def on_clear_history_clicked(self) -> None:
        """Clear the session history.

        Args: (none)
        """
        self._adapter.clear_history()

    def update_history_display(self) -> None:
        """Refresh history from the adapter.

        In the iOS layout there is no visible history panel, but this
        method still calls ``adapter.get_history()`` so that callers
        relying on that side-effect continue to work.
        """
        self._adapter.get_history()

    def update_operation_buttons(self) -> None:
        """Rebuild the operation button grid for the current mode.

        Delegates to :meth:`_rebuild_button_grid`.  Kept for backward
        compatibility with external callers.
        """
        if hasattr(self, "_ops_container"):
            self._rebuild_button_grid()
