"""Abstract base class for calculator operation modules.

Provides the interface contract that all concrete operation modules
must satisfy, ensuring structural consistency and future extensibility
within the modular calculator architecture.
"""

from abc import ABC


class OperationModule(ABC):
    """Abstract base class for all calculator operation modules.

    Concrete subclasses group related mathematical operations and are
    composed into the Calculator facade.  No abstract methods are
    mandated here — the contract is structural: every module must be
    an OperationModule, making isinstance checks and type annotations
    unambiguous.
    """
