
from roleplay.util import get_yaml, get_yaml_from_string

from roleplay.core.role import Role, register_role
# from roleplay.core.memory import BaseMemory

# from roleplay.memory import __pair__
from roleplay.memory import RoleWithMemory, create_role_with_memory

from langchain_core.messages import AIMessage, BaseMessage

import os
# import logging
from typing import Iterator, List, Optional, Callable

# _logger = logging.getLogger(__name__)

class RoleStreamWithMemory(RoleWithMemory):
    stream_fn: Optional[Callable] = None

    def set_stream_fn(self, fn: Callable) -> object:
        self.stream_fn = fn
        return self

    def _process_stream(self, stream: Iterator[BaseMessage]) -> BaseMessage:
        if self.stream_fn is None:
            raise ValueError('stream_fn is not set, please call set_stream_fn first')
        full_messages = next(stream)
        last_message = full_messages
        self.stream_fn(full_messages, 'begin')
        for message in stream:
            self.stream_fn(message, 'update')
            full_messages += message
            last_message = message
        self.stream_fn(full_messages, 'end')
        full_messages.usage_metadata = last_message.usage_metadata
        full_messages.response_metadata['token_usage'] = full_messages.usage_metadata
        return full_messages

    def _invoke(self, **kwargs):
        kwargs.update(self.memory.load(kwargs))
        return self._process_stream(self.llm_chain.stream(kwargs))

    def _tool_invoke(self, _input: List[BaseMessage]) -> AIMessage:
        kwargs = {'input': _input}
        kwargs.update(self.memory.load(kwargs))
        return self._process_stream(self.llm_chain.stream(kwargs))


def load_role_from_string(role_string: str) -> Role:
    """
    Get a role from the given string and register it.
    """
    role_data = get_yaml_from_string(role_string)
    role = RoleStreamWithMemory(**create_role_with_memory(role_data))
    register_role(role.name, role)
    return role

def load_role(role_file: str) -> Role:
    """
    Get a role from the given file and register it.
    """
    role_data = get_yaml(role_file)
    role = RoleStreamWithMemory(**create_role_with_memory(role_data))
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