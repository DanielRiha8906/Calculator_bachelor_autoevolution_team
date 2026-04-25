# Patterns and Anti-Patterns

Discovered across evolution cycles. Update when a new pattern is confirmed or an anti-pattern is observed more than once.

## Patterns

<!-- Example:
### Pattern: <name>
- **Context:** when does this apply
- **Solution:** what to do
- **First seen:** cycle / issue
-->

## Anti-Patterns

<!-- Example:
### Anti-Pattern: <name>
- **Context:** when this tends to happen
- **Problem:** what goes wrong
- **First seen:** cycle / issue
-->

### Anti-Pattern: sys.modules mutation without restore
- **Context:** Tests that clear sys.modules to check import isolation
- **Problem:** Deleting all src.* entries from sys.modules without restoring them pollutes subsequent tests in the same session; modules re-imported in later tests get fresh instances, breaking registry singleton state
- **First seen:** Issue #415 — test_core_separation.py::test_circular_imports
- **Fix:** Save original modules dict, use try/finally to restore after test
