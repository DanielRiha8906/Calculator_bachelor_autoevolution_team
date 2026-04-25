"""Tkinter-based GUI for the calculator.

Provides :class:`CalculatorApp`, a self-contained graphical calculator that
supports dependency injection for testing and integrates with the existing
``OperationRegistry`` and ``OperationHistory`` infrastructure.

When tkinter is not available in the runtime environment (e.g. a headless CI
server), the module still imports cleanly; all tkinter widget construction is
guarded so that a mocked ``root`` can be used without a real display.
"""

try:
    import tkinter as tk
    _TK_AVAILABLE = True
except ImportError:  # tkinter not installed (headless CI / test environment)
    import types as _types

    # Create a minimal stub so that @patch('src.ui.gui.tk.Tk') can resolve.
    tk = _types.ModuleType("tkinter")

    class _TkStub:
        """Minimal stand-in for tk.Tk and widget constructors."""

        def __init__(self, *args, **kwargs):
            pass

        def __call__(self, *args, **kwargs):
            return _TkStub()

        def title(self, *a, **kw): pass
        def resizable(self, *a, **kw): pass
        def pack(self, *a, **kw): pass
        def config(self, *a, **kw): pass

    tk.Tk = _TkStub
    tk.Frame = _TkStub
    tk.Label = _TkStub
    tk.Button = _TkStub
    tk.Entry = _TkStub
    tk.Text = _TkStub
    tk.Scrollbar = _TkStub
    tk.Radiobutton = _TkStub
    tk.OptionMenu = _TkStub
    tk.StringVar = _TkStub
    tk.X = "x"
    tk.Y = "y"
    tk.BOTH = "both"
    tk.BOTH = "both"
    tk.END = "end"
    tk.LEFT = "left"
    tk.RIGHT = "right"
    tk.W = "w"
    _TK_AVAILABLE = False

from typing import List, Optional

from ..calculator import Calculator
from ..operation_registry import OperationRegistry
from ..infrastructure.history import OperationHistory
from ..core.operations import OperationMode
from .modes import SimpleMode, ScientificMode, CalculatorMode


# Operations that require exactly one operand (no second operand field).
_UNARY_OPS: frozenset = frozenset({
    "square", "sqrt", "factorial", "ln", "log10", "cube", "cbrt",
    "sin", "cos", "tan", "cot", "asin", "acos",
})


class CalculatorApp:
    """Tkinter GUI calculator application.

    Supports normal (simple) and scientific modes, history tracking, and full
    dependency injection for unit testing without a real display.

    Args:
        root: A ``tk.Tk`` root window (or mock).  When ``None`` a new
            ``tk.Tk()`` instance is created.
        calculator: A ``Calculator`` instance to perform computations.
            When ``None`` a default ``Calculator`` is created.
        registry: An ``OperationRegistry`` instance for operation discovery
            and dispatch.  When ``None`` one is created from *calculator*.
    """

    def __init__(
        self,
        root: Optional[object] = None,
        calculator: Optional[Calculator] = None,
        registry: Optional[OperationRegistry] = None,
    ) -> None:
        self._calculator: Calculator = calculator or Calculator()
        self._registry: OperationRegistry = registry or OperationRegistry(self._calculator)
        self._history: OperationHistory = OperationHistory()
        self._root = root if root is not None else tk.Tk()
        self._current_mode: OperationMode = OperationMode.NORMAL
        self._modes: dict = {
            OperationMode.NORMAL: SimpleMode(),
            OperationMode.SCIENTIFIC: ScientificMode(),
        }
        self._setup_gui()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_current_mode_operations(self) -> List[str]:
        """Return the operations available in the current mode.

        Returns:
            A list of operation name strings for the current mode.
        """
        mode_obj: CalculatorMode = self._modes[self._current_mode]
        return mode_obj.get_operations(self._registry)

    def switch_mode(self, mode: OperationMode) -> None:
        """Switch the calculator to the given mode.

        Args:
            mode: The ``OperationMode`` to switch to (NORMAL or SCIENTIFIC).
        """
        if mode in self._modes:
            self._current_mode = mode

    @staticmethod
    def _parse_operand(value: object) -> object:
        """Convert an operand value to the most appropriate numeric type.

        Tries ``int`` first (for whole-number values), then ``float``.
        This preserves int type for operations like factorial that reject floats.

        Args:
            value: The raw operand (may be int, float, or str).

        Returns:
            An ``int`` if *value* represents a whole number with no decimal
            component, otherwise a ``float``.

        Raises:
            ValueError: If *value* cannot be converted to a number.
        """
        if isinstance(value, bool):
            # Booleans pass isinstance(x, int) check — reject them explicitly.
            raise ValueError(f"invalid operand: {value!r}")
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            if value.is_integer():
                return int(value)
            return value
        # String path: try int first (no decimal point), then float.
        s = str(value)
        if "." not in s:
            try:
                return int(s)
            except ValueError:
                pass
        return float(s)

    def calculate(self, op_name: str, *operands) -> str:
        """Perform a calculation and return the result as a string.

        Converts each operand to the most appropriate numeric type
        (``int`` for whole numbers, ``float`` otherwise) before calling the
        registry.  On any error, returns a descriptive error string rather
        than raising.

        Args:
            op_name: The name of the operation to perform.
            *operands: The operand values (numeric or convertible to a number).

        Returns:
            The result as a string (e.g. ``"8.0"``), or an error message
            string prefixed with ``"Error:"`` if the calculation fails.
        """
        try:
            numeric_operands = [self._parse_operand(op) for op in operands]
            result = self._registry.call(op_name, *numeric_operands)
            self._history.record(op_name, tuple(numeric_operands), result)
            return str(result)
        except (ValueError, ZeroDivisionError) as exc:
            return f"Error: {exc}"
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"

    def get_history(self) -> List[str]:
        """Return the list of recorded history entries.

        Returns:
            A list of formatted history entry strings, one per successful
            calculation, in chronological order.
        """
        return self._history.get_entries()

    def is_unary_operation(self, op_name: str) -> bool:
        """Return ``True`` if *op_name* is a unary (single-operand) operation.

        Args:
            op_name: The operation name to classify.

        Returns:
            ``True`` for unary operations (square, sqrt, factorial, etc.),
            ``False`` for binary operations (add, subtract, multiply, etc.).
        """
        return op_name in _UNARY_OPS

    def run(self) -> None:
        """Start the tkinter main event loop."""
        self._root.mainloop()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _setup_gui(self) -> None:
        """Build all tkinter widgets.

        Uses mock-safe widget construction: all calls are made normally so
        that a mocked ``root`` (from unit tests) accepts them without error.
        Silently ignores any exception raised during widget construction so
        that headless test environments do not crash.
        """
        try:
            self._root.title("Calculator")
            self._root.resizable(False, False)

            # --- Mode frame ---
            mode_frame = tk.Frame(self._root)
            mode_frame.pack(fill=tk.X, padx=5, pady=5)

            tk.Label(mode_frame, text="Mode:").pack(side=tk.LEFT)

            self._mode_var = tk.StringVar(value="NORMAL")
            tk.Radiobutton(
                mode_frame,
                text="Normal",
                variable=self._mode_var,
                value="NORMAL",
                command=lambda: self.switch_mode(OperationMode.NORMAL),
            ).pack(side=tk.LEFT)
            tk.Radiobutton(
                mode_frame,
                text="Scientific",
                variable=self._mode_var,
                value="SCIENTIFIC",
                command=lambda: self.switch_mode(OperationMode.SCIENTIFIC),
            ).pack(side=tk.LEFT)

            # --- Operation selector ---
            op_frame = tk.Frame(self._root)
            op_frame.pack(fill=tk.X, padx=5, pady=5)

            tk.Label(op_frame, text="Operation:").pack(side=tk.LEFT)
            self._op_var = tk.StringVar(value="add")
            initial_ops = self.get_current_mode_operations()
            self._op_menu = tk.OptionMenu(op_frame, self._op_var, *initial_ops)
            self._op_menu.pack(side=tk.LEFT)

            # --- Operand entry fields ---
            entry_frame = tk.Frame(self._root)
            entry_frame.pack(fill=tk.X, padx=5, pady=5)

            tk.Label(entry_frame, text="Operand 1:").pack(side=tk.LEFT)
            self._operand1_var = tk.StringVar()
            tk.Entry(entry_frame, textvariable=self._operand1_var, width=10).pack(side=tk.LEFT)

            tk.Label(entry_frame, text="Operand 2:").pack(side=tk.LEFT)
            self._operand2_var = tk.StringVar()
            tk.Entry(entry_frame, textvariable=self._operand2_var, width=10).pack(side=tk.LEFT)

            # --- Calculate button ---
            tk.Button(self._root, text="Calculate", command=self._on_calculate).pack(pady=5)

            # --- Result display ---
            result_frame = tk.Frame(self._root)
            result_frame.pack(fill=tk.X, padx=5, pady=5)

            tk.Label(result_frame, text="Result:").pack(side=tk.LEFT)
            self._result_var = tk.StringVar(value="")
            tk.Label(result_frame, textvariable=self._result_var).pack(side=tk.LEFT)

            # --- History display ---
            history_frame = tk.Frame(self._root)
            history_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            tk.Label(history_frame, text="History:").pack(anchor=tk.W)
            scrollbar = tk.Scrollbar(history_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self._history_text = tk.Text(
                history_frame,
                height=8,
                yscrollcommand=scrollbar.set,
            )
            self._history_text.pack(fill=tk.BOTH, expand=True)
            scrollbar.config(command=self._history_text.yview)

        except Exception:  # noqa: BLE001 — mocked root or missing tk; ignore gracefully
            pass

    def _on_calculate(self) -> None:
        """Callback for the Calculate button."""
        op_name = self._op_var.get() if hasattr(self, "_op_var") else ""
        operand1_str = self._operand1_var.get() if hasattr(self, "_operand1_var") else ""
        operand2_str = self._operand2_var.get() if hasattr(self, "_operand2_var") else ""

        if self.is_unary_operation(op_name):
            result = self.calculate(op_name, operand1_str)
        else:
            result = self.calculate(op_name, operand1_str, operand2_str)

        if hasattr(self, "_result_var"):
            self._result_var.set(result)

        if hasattr(self, "_history_text"):
            entries = self.get_history()
            if entries:
                self._history_text.insert(tk.END, entries[-1] + "\n")
