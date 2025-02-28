import dataclasses
import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Type, Dict, Optional, Any, get_origin, get_args, Union

from whisp.messages.WhispMessage import WhispMessage
from whisp.server.code.IntermediateLanguage import ILDocument, ILMessage, ILField, ILType, PrimitiveKind, \
    ILPrimitiveType, ILArrayType, ILEnum, ILEnumType


class BaseCodeGenerator(ABC):

    @abstractmethod
    def generate(self, messages: List[Type[WhispMessage]]) -> str:
        pass

    def convert_to_il(self, messages: List[Type[WhispMessage]]) -> ILDocument:
        """
        Converts a list of message dataclasses into an ILDocument.

        Args:
            messages: A list of dataclass types (e.g., WhispMessage subclasses).

        Returns:
            An ILDocument representing all converted IL types.
        """
        doc = ILDocument()
        processed: Dict[Type, ILMessage] = {}
        for msg_cls in messages:
            il_msg = self._convert_dataclass_to_il_message(msg_cls, processed)
            if il_msg is not None:
                doc.types.append(il_msg)
        return doc

    def _convert_dataclass_to_il_message(
            self, msg_cls: Type, processed: Dict[Type, ILMessage]
    ) -> Optional[ILMessage]:
        """
        Converts a single dataclass into an ILMessage.

        Args:
            msg_cls: The dataclass type to convert.
            processed: A dict caching already processed types to prevent recursion.

        Returns:
            An ILMessage representing the dataclass, or None if conversion failed.
        """
        if msg_cls in processed:
            return processed[msg_cls]

        il_msg = ILMessage(name=msg_cls.__name__)
        processed[msg_cls] = il_msg

        # add class fields
        for field in dataclasses.fields(msg_cls):
            il_type = self._convert_field_type(field.type, processed)
            if il_type is None:
                logging.warning(
                    f"Field '{field.name}' in '{msg_cls.__name__}' has unsupported type '{field.type}'"
                )
                continue

            default_value = field.default if field.default is not dataclasses.MISSING else None
            il_field = ILField(name=field.name, type=il_type, default_value=default_value)
            il_msg.fields.append(il_field)

        # add static fields
        if issubclass(msg_cls, WhispMessage):
            il_event_field = ILField(name="event",
                                     type=ILPrimitiveType(kind=PrimitiveKind.STRING),
                                     default_value=msg_cls.event)
            il_description_field = ILField(name="description",
                                           type=ILPrimitiveType(kind=PrimitiveKind.STRING),
                                           default_value=msg_cls.description)
            il_msg.attributes[il_event_field.name] = il_event_field
            il_msg.attributes[il_description_field.name] = il_description_field

        return il_msg

    def _convert_field_type(
            self, typ: Any, processed: Dict[Type, ILMessage]
    ) -> Optional[ILType]:
        """
        Converts a Python type annotation into an ILType.

        Supports primitive types, Optional (nullable), lists, enums, and dataclass messages.
        Unsupported types are logged as warnings.

        Args:
            typ: The type annotation to convert.
            processed: A dict caching already processed message types.

        Returns:
            An ILType representing the Python type, or None if unsupported.
        """
        # Handle Optional types (i.e., Union with None).
        origin = get_origin(typ)
        if origin is Union:
            args = get_args(typ)
            non_none_args = [arg for arg in args if arg is not type(None)]
            if len(non_none_args) == 1:
                # This is an Optional type.
                return self._convert_field_type(non_none_args[0], processed)
            else:
                logging.warning(f"Unsupported union field type: {typ}")
                return None

        # Handle primitive types.
        if typ in (bool, int, float, str, bytes):
            mapping = {
                bool: PrimitiveKind.BOOL,
                int: PrimitiveKind.INT,
                float: PrimitiveKind.FLOAT,
                str: PrimitiveKind.STRING,
                bytes: PrimitiveKind.BYTES,
            }
            return ILPrimitiveType(kind=mapping[typ])

        # Handle List types.
        if origin in (list, List):
            args = get_args(typ)
            if args and len(args) == 1:
                inner_type = self._convert_field_type(args[0], processed)
                if inner_type is not None:
                    return ILArrayType(element_type=inner_type)
            logging.warning(f"Unsupported list field type: {typ}")
            return None

        # Handle Enum types.
        if isinstance(typ, type) and issubclass(typ, Enum):
            # Extract enum member names.
            values = list(typ.__members__.keys())
            enum_def = ILEnum(name=typ.__name__, values=values)
            return ILEnumType(enum=enum_def)

        # Handle nested dataclass messages.
        if dataclasses.is_dataclass(typ):
            return self._convert_dataclass_to_il_message(typ, processed)

        logging.warning(f"Unsupported field type: {typ}")
        return None

    @staticmethod
    def _extract_enums(document: ILDocument) -> Dict[str, ILEnum]:
        # Extract enums from the IL document.
        enums: Dict[str, ILEnum] = {}
        for il_type in document.types:
            # Check if we have an ILMessage (which contains "fields").
            if isinstance(il_type, ILMessage):
                for field in il_type.fields + il_type.static_fields:
                    if hasattr(field.type, "enum"):
                        enum_def = field.type.enum
                        enums[enum_def.name] = enum_def
        return enums
