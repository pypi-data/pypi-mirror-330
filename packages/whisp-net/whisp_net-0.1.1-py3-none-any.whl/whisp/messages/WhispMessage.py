import dataclasses
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable, TypeVar, Type, Dict, List, Optional, Union

T = TypeVar("T")


@runtime_checkable
class WhispMessageProtocol(Protocol):
    event: str
    description: str
    system_message: bool


class JsonSerializable(ABC):
    @abstractmethod
    def to_dict(self: T):
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        pass


@dataclass(kw_only=True)
class WhispDataclass(JsonSerializable):
    sender: Optional[str] = None
    time_stamp: Optional[int] = None

    def __post_init__(self):
        if self.time_stamp is None:
            self.time_stamp = round(time.monotonic() * 1000)

    def to_dict(self: T):
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        field_types = {f.name: f.type for f in dataclasses.fields(cls)}
        parsed_data = {}

        for key, value in data.items():
            if key in field_types:
                expected_type = field_types[key]
                if expected_type is float:
                    parsed_data[key] = float(value)
                elif expected_type is int:
                    parsed_data[key] = int(value)
                else:
                    parsed_data[key] = value

        return cls(**parsed_data)


@dataclass(slots=True)
class WhispMessage(WhispMessageProtocol, WhispDataclass, ABC):
    pass


WHISP_MESSAGE_REGISTRY: List[Type[Union[WhispDataclass, WhispMessage]]] = []


def whisp_message(cls: Any = None, /, *, event: str, description: str, system_message: bool = False):
    def decorator(inner_cls):
        if issubclass(inner_cls, WhispDataclass):
            WHISP_MESSAGE_REGISTRY.append(inner_cls)

        inner_cls.event = event
        inner_cls.description = description
        inner_cls.system_message = system_message
        return inner_cls

    if cls is None:
        return decorator
    return decorator(cls)
