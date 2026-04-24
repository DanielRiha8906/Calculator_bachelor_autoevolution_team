"""Operation type definitions and metadata for the calculator."""
from enum import Enum
from dataclasses import dataclass


class OperationType(Enum):
    UNARY = "unary"
    BINARY = "binary"


@dataclass
class OperationMetadata:
    name: str
    arity: int
    op_type: OperationType
    description: str
