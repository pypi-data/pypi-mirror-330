
from roleplay.util import get_yaml, get_yaml_from_string, SafeEval

from langchain.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr

import os
import weakref
import logging
from typing import Any, Dict, List, Optional, Type

_logger = logging.getLogger(__name__)

class Tool(BaseModel):
    """A tool model representing executable functionality"""

    name: str = Field(description="Unique name identifying the tool")
    parameters: Optional[Type[BaseModel]] = Field(description="Input parameters schema")
    description: str = Field(description="Natural language description of the tool")
    script: str = Field(description="Executable script code for the tool")

    _Tool: Optional[BaseTool] = None
    _evaluator: SafeEval = PrivateAttr(default_factory=SafeEval)

    def __init__(self, **data):
        super().__init__(**data)

        # Define LangChain tool structure
        class _LangChainTool(BaseTool):
            name: str = self.name
            description: str = self.description
            args_schema: Type[BaseModel] = self.parameters

            def _run(self, **kwargs) -> str:
                return self._outer_tool.run(**kwargs)

        # Set weakref to avoid circular references
        self._Tool = _LangChainTool
        self._Tool._outer_tool = weakref.ref(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tool):
            return NotImplemented
        return self.name == other.name and self.script == other.script

    def run(self, **kwargs) -> Any:
        """Execute the tool's script with validated parameters"""
        if not self.script:
            raise RuntimeError("Cannot execute empty script")

        try:
            return self._evaluator.eval(expr=self.script, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Script execution failed: {str(e)}") from e

    def to_ltool(self) -> BaseTool:
        """Export as a LangChain-compatible tool"""
        return self._Tool()

_all_tools: Dict[str, Tool] = {}

def register_tool(name: str, tool: Tool):
    """
    Register a tool with the given name.
    """
    if name in _all_tools:
        _logger.warning(f"Tool {name} already exists.")
    _all_tools[name] = tool
    _logger.debug(f"Registered tool: {name}")

def check_tool(name: str) -> bool:
    """
    Check if a tool with the given name exists.
    """
    return name in _all_tools

def get_tool(name: str) -> Tool:
    """
    Get a tool with the given name.
    """
    return _all_tools[name]


def generate_class(class_name: str,
                   parameters: List[Dict[str, Any]]) -> Type[BaseModel]:
    # Create annotations and default values
    annotations = {}
    defaults = {}

    if parameters is None:
        return None

    # Supported type mapping
    type_mapping = {
        'float': float,
        'int': int,
        'str': str,
        'bool': bool
    }

    # Populate fields with parameter definitions
    for param in parameters:
        param_name = param['name']
        param_type = type_mapping.get(param['type'], str)  # Default to str if type is unknown
        param_description = param.get('description', '')
        annotations[param_name] = param_type
        defaults[param_name] = Field(description=param_description)

    _logger.debug(f"Generated class: {class_name}: {annotations}")

    # Dynamically create the Pydantic model class
    return type(class_name, (BaseModel,), {
        '__annotations__': annotations,
        **defaults
    })

def create_tool(tool_data: dict) -> Tool:
    """
    Create a Tool instance from the given data dictionary.
    """
    tool_name: str = tool_data['name']
    # tool_type: ToolType = ToolType(tool_data['type'])
    # tool_weight: int = tool_data['weight']
    tool_parameters: Type[BaseModel] = generate_class(tool_name, tool_data['parameters'])
    tool_description: str = tool_data['description']
    tool_script: str = tool_data.get('script', '')
    return Tool(name=tool_name, parameters=tool_parameters,
                description=tool_description, script=tool_script)

def load_tool_from_string(tool_string: str) -> Tool:
    """
    Get a tool from the given string and register it.
    """
    tool_data = get_yaml_from_string(tool_string)
    tool = create_tool(tool_data)
    register_tool(tool.name, tool)
    return tool

def load_tool(tool_file_path: str) -> Tool:
    """
    Get a tool from the given file path and register it.
    """
    tool_data = get_yaml(tool_file_path)
    tool = create_tool(tool_data)

    # 获取 tool.script 文件的路径
    script_file_path = os.path.join(os.path.dirname(tool_file_path), tool.script)
    
    # 读取 script 文件的内容
    with open(script_file_path, 'r') as script_file:
        tool.script = script_file.read()

    register_tool(tool.name, tool)
    return tool

def load_tools_from_dir(tool_dir_path: str) -> List[Tool]:
    """
    Get all tools from the given directory and register them.
    Only files with the extension '.tool.yaml' are processed.
    """
    tools = []

    # Iterate over all files in the directory
    for filename in os.listdir(tool_dir_path):
        # Check if the file ends with '.tool.yaml'
        if filename.endswith('.tool.yaml'):
            # Construct the full file path
            tool_file_path = os.path.join(tool_dir_path, filename)
            # Get the tool and add it to the list
            tool = load_tool(tool_file_path)
            tools.append(tool)

    return tools