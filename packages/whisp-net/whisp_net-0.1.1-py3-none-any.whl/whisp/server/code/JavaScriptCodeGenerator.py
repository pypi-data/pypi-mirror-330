import json
from enum import Enum
from pathlib import Path
from typing import List, Type

from jinja2 import Environment, FileSystemLoader

from whisp.messages.WhispMessage import WhispMessage
from whisp.server.code import _templates
from whisp.server.code.BaseCodeGenerator import BaseCodeGenerator


class JavaScriptCodeGenerator(BaseCodeGenerator):
    def __init__(self) -> None:
        templates_path = Path(_templates.__file__).parent

        env = Environment(loader=FileSystemLoader(str(templates_path)))
        env.filters['tojson_safe'] = self.tojson_safe
        self.template = env.get_template("javascript.js.jinja")

    @staticmethod
    def tojson_safe(value):
        try:
            if isinstance(value, Enum):
                return f"{type(value).__name__}.{value.name}"

            return json.dumps(value)
        except TypeError:
            # Fallback: convert to string if value is not JSON serializable
            return json.dumps(str(value))

    def generate(self, messages: List[Type[WhispMessage]]) -> str:
        # Convert the list of WhispMessage dataclasses into an ILDocument.
        document = self.convert_to_il(messages)

        # Extract enums from the IL document.
        # We look at all fields (and static fields) in each message.
        enums = self._extract_enums(document)

        # Render the javascript module using the provided template.
        return self.template.render(document=document, enums=list(enums.values()))
