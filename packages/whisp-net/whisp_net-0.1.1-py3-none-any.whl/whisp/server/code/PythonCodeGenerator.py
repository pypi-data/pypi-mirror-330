import dataclasses
from enum import Enum
from pathlib import Path
from typing import List, Type, Any, Dict

from jinja2 import Template, Environment, FileSystemLoader

from whisp.messages.WhispMessage import WhispMessage  # Provides the base fields and functionality
from whisp.server.code import _templates
from whisp.server.code.BaseCodeGenerator import BaseCodeGenerator


class PythonCodeGenerator(BaseCodeGenerator):
    def __init__(self) -> None:
        # Load the Jinja2 template file for Python dataclass generation.
        templates_path = Path(_templates.__file__).parent
        env = Environment(
            loader=FileSystemLoader(str(templates_path))
        )
        # Register filters for converting default values, types, and property names.
        env.filters["to_python_value"] = self.to_python_value
        self.template: Template = env.get_template("python.py.jinja")

    def generate(self, messages: List[Type[WhispMessage]]) -> str:
        """
        Generates a Python file that defines dataclass-based messages.
        Each generated class extends WhispMessage and uses the @whisp_message decorator.
        Only fields that are not defined in WhispMessage are generated.
        """
        # Determine the names of fields defined in WhispMessage (the base class)
        base_field_names = {f.name for f in dataclasses.fields(WhispMessage)}

        py_messages = []
        for message in messages:
            message_fields = []
            for field in dataclasses.fields(message):
                if field.name in base_field_names:
                    continue
                message_fields.append({
                    "name": field.name,
                    "type": self._get_type_hint(field),
                    "default": self._get_py_default_value(field)
                })
            py_messages.append({
                "name": message.__name__,
                # Use the attributes set by the whisp_message decorator.
                "event": message.event,
                "description": message.description,
                "fields": message_fields,
            })

        # Extract enums from the IL document.
        document = self.convert_to_il(messages)
        enums = self._extract_enums(document)

        context: Dict[str, Any] = {"messages": py_messages, "enums": list(enums.values())}
        return self.template.render(context)

    @staticmethod
    def to_python_value(value: Any) -> str:
        """
        Converts a Python value into a C# literal.
        """
        if isinstance(value, Enum):
            return f"{type(value).__name__}.{value.name}"
        return str(value)

    def _get_type_hint(self, field: dataclasses.Field) -> str:
        """
        Returns a string representation of the field's type.
        """
        try:
            return field.type.__name__
        except AttributeError:
            return str(field.type)

    def _get_py_default_value(self, field: dataclasses.Field) -> str:
        """
        Converts a dataclass field default to an appropriate Python literal.
        Returns an empty string if no default is set.
        Special handling for fields (like time_stamp) is assumed to be part of the base class.
        """
        if field.default is not dataclasses.MISSING:
            default = field.default
            if default is None:
                return "None"
            elif isinstance(default, str):
                return f'"{default}"'
            elif isinstance(default, bool):
                return "True" if default else "False"
            elif isinstance(default, (int, float)):
                return str(default)
            elif isinstance(default, Enum):
                return f"{type(default).__name__}.{default.name}"
            else:
                return ""
        elif field.default_factory is not dataclasses.MISSING:
            # We leave fields with a default_factory without a literal default.
            return ""
        else:
            return ""
