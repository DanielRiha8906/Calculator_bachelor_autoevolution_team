"""iOS-style Tkinter window for the Calculator GUI.

:class:`GuiCalculator` is a self-contained :class:`tk.Tk` subclass that
renders an iOS-inspired dark calculator skin.  Appearance is fully driven
by the module-level :data:`_THEME` dictionary; no colour or font literal
appears anywhere else in the file.

Operation discovery is handled through an injected
:class:`~src.gui.session_adapter.GUISessionAdapter`, keeping all
computation and mode state inside the existing session layer.
"""

import tkinter as tk

from ..core.calculator import Calculator
from ..session import CalculatorSession
from .session_adapter import GUISessionAdapter

# ---------------------------------------------------------------------------
# Theme — single source of truth for all visual constants.
# ---------------------------------------------------------------------------

_THEME: dict[str, object] = {
    "bg_window": "#000000",
    "bg_display": "#000000",
    "fg_display": "#FFFFFF",
    "bg_operator": "#FF9500",
    "bg_operator_hover": "#FFB143",
    "fg_operator": "#FFFFFF",
    "bg_utility": "#1C1C1E",
    "bg_utility_hover": "#2C2C2E",
    "fg_utility": "#FFFFFF",
    "bg_normal": "#333333",
    "bg_normal_hover": "#4D4D4D",
    "fg_normal": "#FFFFFF",
    "bg_frame": "#000000",
    "bg_toggle": "#1C1C1E",
    "fg_toggle": "#FFFFFF",
    "font_display": ("Courier New", 32, "bold"),
    "font_button": ("Arial", 14, "bold"),
    "font_toggle": ("Arial", 12, "bold"),
}

# ---------------------------------------------------------------------------
# Symbol map — maps canonical operation names to display symbols.
# ---------------------------------------------------------------------------

_SYMBOL_MAP: dict[str, str] = {
    "add": "+",
    "subtract": "−",       # −
    "multiply": "×",       # ×
    "divide": "÷",         # ÷
    "sqrt": "√",           # √
    "square_root": "√",    # √
    "square": "x²",        # x²
    "cube": "x³",          # x³
    "power": "xʸ",         # xʸ
    "factorial": "n!",
    "logarithm": "log",
    "log": "log",
    "natural_logarithm": "ln",
    "ln": "ln",
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "cot": "cot",
    "asin": "asin",
    "acos": "acos",
    "cube_root": "∛",      # ∛
    "pi": "π",             # π
    "e": "e",
}

# ---------------------------------------------------------------------------
# Operator operations — receive the orange iOS accent colour.
# ---------------------------------------------------------------------------

_OPERATOR_OPS: set[str] = {"add", "subtract", "multiply", "divide"}


# ---------------------------------------------------------------------------
# Main window class
# ---------------------------------------------------------------------------


class GuiCalculator(tk.Tk):
    """iOS-style calculator window built with Tkinter.

    Constructs its own :class:`~src.gui.session_adapter.GUISessionAdapter`
    internally so callers only need to instantiate this class and call
    :meth:`mainloop`.

    Layout (top to bottom inside the root window):
    - Row 0: Result display label.
    - Row 1: Mode toggle button.
    - Row 2: Button grid frame.

    Args:
        adapter: An optional pre-configured
            :class:`~src.gui.session_adapter.GUISessionAdapter`.  When
            *None* a fresh adapter wired to a default
            :class:`~src.core.calculator.Calculator` is created
            automatically.
    """

    def __init__(self, adapter: GUISessionAdapter | None = None) -> None:
        tk.Tk.__init__(self)

        if adapter is None:
            calc = Calculator()
            session = CalculatorSession(calc)
            adapter = GUISessionAdapter(session)

        self._adapter: GUISessionAdapter = adapter
        self._mode: str = "normal"
        self._selected_op: str | None = None

        # Initialise the session mode to match the default UI mode.
        self._adapter.set_mode(self._mode)

        self.title("Calculator")
        self.configure(bg=str(_THEME["bg_window"]))
        self.minsize(300, 400)

        self._result_label: tk.Label
        self._toggle_btn: tk.Button
        self._grid_frame: tk.Frame

        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Construct and grid all top-level widgets."""
        self.columnconfigure(0, weight=1)

        # Row 0 — Result display.
        self._result_label = tk.Label(
            self,
            text="0",
            bg=str(_THEME["bg_display"]),
            fg=str(_THEME["fg_display"]),
            font=_THEME["font_display"],
            anchor=tk.E,
            padx=16,
            pady=12,
        )
        self._result_label.grid(row=0, column=0, sticky="ew")

        # Row 1 — Mode toggle button.
        self._toggle_btn = tk.Button(
            self,
            text="scientific",
            bg=str(_THEME["bg_toggle"]),
            fg=str(_THEME["fg_toggle"]),
            activebackground=str(_THEME["bg_utility_hover"]),
            activeforeground=str(_THEME["fg_toggle"]),
            font=_THEME["font_toggle"],
            relief="flat",
            borderwidth=0,
            command=self._on_mode_toggle,
        )
        self._toggle_btn.grid(row=1, column=0, sticky="ew", padx=4, pady=2)
        self._toggle_btn.bind(
            "<Enter>",
            lambda _e: self._toggle_btn.configure(
                bg=str(_THEME["bg_utility_hover"])
            ),
        )
        self._toggle_btn.bind(
            "<Leave>",
            lambda _e: self._toggle_btn.configure(bg=str(_THEME["bg_toggle"])),
        )

        # Row 2 — Button grid frame.
        self._grid_frame = tk.Frame(self, bg=str(_THEME["bg_frame"]))
        self._grid_frame.grid(row=2, column=0, sticky="nsew", padx=4, pady=4)
        self.rowconfigure(2, weight=1)

        self._build_button_grid(self._grid_frame)

    def _build_button_grid(self, frame: tk.Frame) -> None:
        """Populate *frame* with one button per operation in the current mode.

        Buttons are arranged in a 4-column grid.  Each button fills its cell
        equally (``sticky="nsew"``).  Colours are determined by
        :meth:`_get_button_colors`.

        Args:
            frame: The :class:`tk.Frame` that will contain all buttons.
        """
        for col in range(4):
            frame.columnconfigure(col, weight=1)

        operations: list[str] = self._adapter.get_operations()

        for idx, op_name in enumerate(operations):
            row = idx // 4
            col = idx % 4

            symbol = _SYMBOL_MAP.get(op_name, op_name)
            bg, fg, hover_bg = self._get_button_colors(op_name)

            btn = tk.Button(
                frame,
                text=symbol,
                bg=bg,
                fg=fg,
                activebackground=hover_bg,
                activeforeground="#FFFFFF",
                relief="flat",
                borderwidth=0,
                font=_THEME["font_button"],
                command=lambda op=op_name: self._on_operation_click(op),
            )
            frame.rowconfigure(row, weight=1)
            btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

            # Capture bg/hover_bg in default args to avoid late-binding issues.
            btn.bind(
                "<Enter>",
                lambda _e, b=btn, h=hover_bg: b.configure(bg=h),
            )
            btn.bind(
                "<Leave>",
                lambda _e, b=btn, c=bg: b.configure(bg=c),
            )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_button_colors(self, op_name: str) -> tuple[str, str, str]:
        """Return ``(bg, fg, hover_bg)`` for *op_name*.

        Operator keys (``+``, ``−``, ``×``, ``÷``) receive the iOS orange
        accent.  In scientific mode all non-operator buttons receive the
        dark-utility colours.  In normal mode they receive the mid-grey
        normal colours.

        Args:
            op_name: The canonical operation name.

        Returns:
            A 3-tuple of colour strings ``(bg, fg, hover_bg)``.
        """
        if op_name in _OPERATOR_OPS:
            return (
                str(_THEME["bg_operator"]),
                str(_THEME["fg_operator"]),
                str(_THEME["bg_operator_hover"]),
            )
        if self._mode == "scientific":
            return (
                str(_THEME["bg_utility"]),
                str(_THEME["fg_utility"]),
                str(_THEME["bg_utility_hover"]),
            )
        return (
            str(_THEME["bg_normal"]),
            str(_THEME["fg_normal"]),
            str(_THEME["bg_normal_hover"]),
        )

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_mode_toggle(self) -> None:
        """Toggle between normal and scientific mode.

        Updates the toggle button label, switches the adapter mode, and
        rebuilds the button grid.  The result display is reset to ``"0"``.
        """
        if self._mode == "normal":
            self._mode = "scientific"
            self._toggle_btn.configure(text="normal")
        else:
            self._mode = "normal"
            self._toggle_btn.configure(text="scientific")

        self._adapter.set_mode(self._mode)
        self._selected_op = None

        # Rebuild button grid in-place.
        for widget in self._grid_frame.winfo_children():
            widget.destroy()
        self._build_button_grid(self._grid_frame)

        self.update_result("0")

    def _on_operation_click(self, op_name: str) -> None:
        """Handle a button press for *op_name*.

        Stores the selected operation and reflects the corresponding symbol
        in the result display.

        Args:
            op_name: The canonical operation name that was clicked.
        """
        self._selected_op = op_name
        symbol = _SYMBOL_MAP.get(op_name, op_name)
        self.update_result(symbol)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def update_result(self, text: str) -> None:
        """Update the result display label to *text*.

        This method is intentionally public so that external components (e.g.
        an adapter callback) can push display updates without accessing
        private attributes.

        Args:
            text: The string to display.
        """
        self._result_label.configure(text=text)
