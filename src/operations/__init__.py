"""Operations subsystem — registry and concrete operation definitions."""
from src.operations.base import Operation, OperationRegistry
from src.operations.basic import register_basic_operations
from src.operations.scientific import register_scientific_operations

__all__ = ["Operation", "OperationRegistry", "register_basic_operations", "register_scientific_operations"]
