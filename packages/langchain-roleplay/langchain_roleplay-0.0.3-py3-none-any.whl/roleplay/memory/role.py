from roleplay.util import get_yaml, get_yaml_from_string

from roleplay.core.role import Role, create_role, register_role
from roleplay.core.memory import BaseMemory

from roleplay.memory import __pair__

from pydantic import Field
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage

import os
import logging
from typing import Any, Dict, List, Optional

_logger = logging.getLogger(__name__)

class RoleWithMemory(Role):
    memory: BaseMemory = Field(default_factory=BaseMemory,
                               description='The memory to use for the role')
    # def __init__(self, memory: Optional[BaseMemory]=None, **kwargs):
    #     super().__init__(**kwargs)
    #     self.memory = memory or BaseMemory()
    #     if not isinstance(self.memory, BaseMemory):
    #         raise TypeError("memory must be an instance of BaseMemory")

    def _invoke(self, **kwargs):
        kwargs.update(self.memory.load(kwargs))
        return self.llm_chain.invoke(kwargs)

    def _tool_invoke(self, _input: List[BaseMessage]) -> AIMessage:
        input = {'input': _input}
        input.update(self.memory.load(input))
        return self.llm_chain.invoke(input)

    def _post_invoke(self, _input: HumanMessage, outputs: Dict[str, Any]) -> int:
        return self.memory.save(_input, outputs)

    def mem_clear(self) -> None:
        self.memory.clear()

def create_role_with_memory(role_data: dict) -> dict:
    """Create a role with memory from a dictionary."""
    role_memory = role_data.get('memory', None)
    if role_memory is None:
        # raise ValueError("memory must be specified")
        _logger.warning("memory not specified, using base memory")
        role_memory = {'type': 'base'}
    role_memory_type = role_memory.get('type', 'base')
    type_dict = { 'base': BaseMemory }
    type_dict.update(__pair__)
    role_kwargs = create_role(role_data)
    role_kwargs['memory'] = type_dict[role_memory_type](**role_memory)
    return role_kwargs

def load_role_from_string(role_string: str) -> Role:
    """
    Get a role from the given string and register it.
    """
    role_data = get_yaml_from_string(role_string)
    role = RoleWithMemory(**create_role_with_memory(role_data))
    register_role(role.name, role)
    return role

def load_role(role_file: str) -> Role:
    """
    Get a role from the given file and register it.
    """
    role_data = get_yaml(role_file)
    role = RoleWithMemory(**create_role_with_memory(role_data))
    register_role(role.name, role)
    return role

def load_roles_from_dir(role_dir: str) -> List[Role]:
    """
    Get all roles from the given directory and register them.
    Only files with the extension '.role.yaml' are processed.
    """
    roles = []
    for filename in os.listdir(role_dir):
        if filename.endswith('.role.yaml'):
            role_file = os.path.join(role_dir, filename)
            role = load_role(role_file)
            roles.append(role)
    return roles