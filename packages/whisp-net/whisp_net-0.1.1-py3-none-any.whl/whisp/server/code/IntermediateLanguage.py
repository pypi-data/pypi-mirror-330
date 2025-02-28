from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Any, Dict


# Enum for supported primitive types.
class PrimitiveKind(Enum):
    BOOL = "bool"
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    BYTES = "bytes"


# Base type for all IL types.
class ILType(ABC):
    pass


# Primitive type now uses the PrimitiveKind enum.
@dataclass
class ILPrimitiveType(ILType):
    kind: PrimitiveKind


# Definition of an enumeration.
@dataclass
class ILEnum:
    name: str
    values: List[str]


# Enum type that refers to an ILEnum definition.
@dataclass
class ILEnumType(ILType):
    enum: ILEnum


# Message type is now a subclass of ILType.
@dataclass
class ILMessage(ILType):
    name: str
    fields: List[ILField] = field(default_factory=list)
    static_fields: List[ILField] = field(default_factory=list)
    attributes: Dict[str, ILField] = field(default_factory=dict)

    @property
    def event(self) -> ILField:
        return self.attributes["event"]

    @property
    def description(self) -> ILField:
        return self.attributes["description"]


# Array type that can wrap any ILType (allowing nested arrays or arrays of messages/enums).
@dataclass
class ILArrayType(ILType):
    element_type: ILType


# Field now uses an ILType instance.
@dataclass
class ILField:
    name: str
    type: ILType
    default_value: Optional[Any] = None


# Top-level document that holds all types.
@dataclass
class ILDocument:
    types: List[ILType] = field(default_factory=list)
