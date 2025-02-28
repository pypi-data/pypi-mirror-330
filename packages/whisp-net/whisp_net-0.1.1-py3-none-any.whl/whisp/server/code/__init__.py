from typing import Dict, Type

from whisp.server.code.BaseCodeGenerator import BaseCodeGenerator
from whisp.server.code.CSharpCodeGenerator import CSharpCodeGenerator
from whisp.server.code.JavaScriptCodeGenerator import JavaScriptCodeGenerator
from whisp.server.code.PythonCodeGenerator import PythonCodeGenerator

CODE_GENERATORS: Dict[str, Type[BaseCodeGenerator]] = {
    "javascript": JavaScriptCodeGenerator,
    "python": PythonCodeGenerator,
    "csharp": CSharpCodeGenerator
}
