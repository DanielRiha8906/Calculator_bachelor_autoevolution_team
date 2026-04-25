"""GUI Controller for the Calculator application (Issue #414).

Provides GUIController — a pure Python business-logic layer that mediates
between the GUI window and the underlying operation registry.  The controller
has no dependency on any UI toolkit (no tkinter imports here).
"""

from src.calculator.main import _build_registry, MODE_NORMAL, MODE_SCIENTIFIC, VALID_MODES
from src.calculator.operations import OperationRegistry

# The 12 scientific-only operations that are absent from the normal-mode registry.
# Checked in execute_operation BEFORE the registry lookup so that the error
# message "not available in normal mode" fires instead of "unknown operation".
_SCIENTIFIC_ONLY: frozenset[str] = frozenset({
    "sin",
    "cos",
    "tan",
    "asin",
    "acos",
    "atan",
    "sinh",
    "cosh",
    "tanh",
    "exp",
    "pi",
    "e",
})


class GUIController:
    """Business-logic controller for the GUI calculator.

    Manages the active mode, the operation registry, and a session history
    of successfully executed operations.  All methods return plain Python
    objects so that any UI layer (tkinter, PyQt, web, …) can consume them
    without coupling to a specific toolkit.

    Args:
        mode: Initial operating mode; one of ``"normal"`` or
            ``"scientific"``.  Defaults to ``"scientific"``.
    """

    def __init__(self, mode: str = "scientific") -> None:
        self._current_mode: str = mode
        self._active_registry: OperationRegistry = _build_registry(mode)
        # Each entry is a dict with keys: operation, operands, result.
        self._session_history: list[dict] = []

    # ------------------------------------------------------------------
    # Mode queries and switching
    # ------------------------------------------------------------------

    def get_current_mode(self) -> str:
        """Return the currently active mode string.

        Returns:
            ``"normal"`` or ``"scientific"``.
        """
        return self._current_mode

    def switch_mode(self, mode: str) -> None:
        """Switch to a different operating mode and rebuild the registry.

        The session history is cleared on every mode switch.

        Args:
            mode: Target mode; must be a value in
                :data:`~src.calculator.main.VALID_MODES`.

        Raises:
            ValueError: If *mode* is not a valid mode string.
        """
        if mode not in VALID_MODES:
            raise ValueError(
                f"Invalid mode '{mode}'. Valid modes are: {sorted(VALID_MODES)}"
            )
        self._active_registry = _build_registry(mode)
        self._current_mode = mode
        self._session_history = []

    # ------------------------------------------------------------------
    # Operation queries
    # ------------------------------------------------------------------

    def get_available_operations(self) -> list[str]:
        """Return the list of operation names available in the current mode.

        Returns:
            A list of operation name strings in insertion order.
        """
        return self._active_registry.list_all()

    def get_operation_arity(self, operation_name: str) -> int:
        """Return the number of operands required by *operation_name*.

        Args:
            operation_name: The operation key string.

        Returns:
            Integer arity (0 for constants such as ``pi`` and ``e``).

        Raises:
            KeyError: If *operation_name* is not registered in the current
                mode's registry.
        """
        op = self._active_registry.get(operation_name)  # raises KeyError if absent
        return op.arity

    # ------------------------------------------------------------------
    # Operation execution
    # ------------------------------------------------------------------

    def execute_operation(self, operation_name: str, operands: list) -> dict:
        """Execute *operation_name* with the provided *operands*.

        Returns a result dictionary.  On success the dict contains the keys
        ``success``, ``operation``, ``operands``, and ``result``.  On failure
        it contains ``success`` (``False``) and ``error`` (a human-readable
        message string).

        Args:
            operation_name: The operation key string (e.g. ``"add"``).
            operands: A list of numeric operand values.

        Returns:
            A dict with either ``{"success": True, "operation": ...,
            "operands": ..., "result": ...}`` or
            ``{"success": False, "error": ...}``.
        """
        # Check for scientific-only operations when in normal mode.
        if operation_name in _SCIENTIFIC_ONLY and self._current_mode == MODE_NORMAL:
            return {
                "success": False,
                "error": f"Operation '{operation_name}' not available in normal mode",
            }

        # Check that the operation exists in the active registry.
        if not self._active_registry.has(operation_name):
            return {
                "success": False,
                "error": f"Unknown operation '{operation_name}'",
            }

        op_obj = self._active_registry.get(operation_name)

        # Validate arity.
        if len(operands) != op_obj.arity:
            return {
                "success": False,
                "error": (
                    f"operation '{operation_name}' requires {op_obj.arity} "
                    f"operand(s), got {len(operands)}"
                ),
            }

        # Execute and capture domain errors.
        try:
            result = op_obj.execute(*operands)
        except (ValueError, ZeroDivisionError) as exc:
            return {"success": False, "error": str(exc)}

        # Record successful execution in session history.
        entry: dict = {
            "operation": operation_name,
            "operands": operands,
            "result": result,
        }
        self._session_history.append(entry)

        return {
            "success": True,
            "operation": operation_name,
            "operands": operands,
            "result": result,
        }

    # ------------------------------------------------------------------
    # Session history
    # ------------------------------------------------------------------

    def get_session_history(self) -> list[str]:
        """Return a copy of the session history as a list of formatted strings.

        Each entry is formatted as ``"<op>(<operands>) = <result>"``.

        Returns:
            A list of human-readable history strings, one per successful
            operation, in chronological order.
        """
        formatted: list[str] = []
        for entry in self._session_history:
            op = entry["operation"]
            ops_str = ", ".join(str(o) for o in entry["operands"])
            result = entry["result"]
            formatted.append(f"{op}({ops_str}) = {result}")
        return formatted

    def clear_session_history(self) -> None:
        """Discard all session history entries."""
        self._session_history = []
