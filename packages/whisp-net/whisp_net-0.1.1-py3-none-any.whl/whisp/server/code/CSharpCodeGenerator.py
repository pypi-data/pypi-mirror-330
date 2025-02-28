import json
from enum import Enum
from pathlib import Path
from typing import List, Type, Any

from jinja2 import Environment, FileSystemLoader

from whisp.messages.WhispMessage import WhispMessage
from whisp.server.code import _templates
from whisp.server.code.BaseCodeGenerator import BaseCodeGenerator
from whisp.server.code.IntermediateLanguage import ILType, ILPrimitiveType, PrimitiveKind, ILArrayType, ILEnumType, \
    ILMessage


class CSharpCodeGenerator(BaseCodeGenerator):
    def __init__(self) -> None:
        templates_path = Path(_templates.__file__).parent
        env = Environment(
            loader=FileSystemLoader(str(templates_path)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        # Register filters for converting default values, types, and property names.
        env.filters['to_csharp_value'] = self.to_csharp_value
        env.filters['csharp_type'] = self.csharp_type
        env.filters['csharp_property'] = self.csharp_property
        self.template = env.get_template("csharp.cs.jinja")

        self.filtered_fields = {"sender", "time_stamp"}

    @staticmethod
    def to_csharp_value(value: Any) -> str:
        """
        Converts a Python value into a C# literal.
        """
        if value is None:
            return "default"
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            # Escape inner double quotes.
            escaped = value.replace('"', '\\"')
            return f"\"{escaped}\""
        if isinstance(value, Enum):
            return f"{type(value).__name__}.{value.name}"
        # Fallback for non-serializable values.
        try:
            return json.dumps(value)
        except Exception:
            return str(value)

    @staticmethod
    def csharp_type(il_type: ILType) -> str:
        """
        Maps an ILType into its corresponding C# type name.
        """
        # Handle primitive types.
        if isinstance(il_type, ILPrimitiveType):
            mapping = {
                PrimitiveKind.BOOL: "bool",
                PrimitiveKind.INT: "long",  # use long for integer numbers
                PrimitiveKind.FLOAT: "double",  # using double for floating point numbers
                PrimitiveKind.STRING: "string",
                PrimitiveKind.BYTES: "byte[]",
            }
            return mapping.get(il_type.kind, "object")
        # Handle array types by mapping to a List<T>.
        if isinstance(il_type, ILArrayType):
            elem_type = CSharpCodeGenerator.csharp_type(il_type.element_type)
            return f"List<{elem_type}>"
        # Handle enum types.
        if isinstance(il_type, ILEnumType):
            return il_type.enum.name
        # Handle nested messages.
        if hasattr(il_type, "name"):
            return il_type.name
        return "object"

    @staticmethod
    def csharp_property(field_name: str) -> str:
        """
        Converts a snake_case field name to PascalCase as used in C# properties.
        """
        return ''.join(word.capitalize() for word in field_name.split('_'))

    def generate(self, messages: List[Type[WhispMessage]]) -> str:
        # Convert the list of WhispMessage dataclasses into an ILDocument.
        document = self.convert_to_il(messages)

        for message in document.types:
            if isinstance(message, ILMessage):
                message.fields = [f for f in message.fields if f.name not in self.filtered_fields]

        # Extract enums from the IL document.
        enums = self._extract_enums(document)

        # Render the C# code using the provided template.
        return self.template.render(document=document, enums=list(enums.values()))
