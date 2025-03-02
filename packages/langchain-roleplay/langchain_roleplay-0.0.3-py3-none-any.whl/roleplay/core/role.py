
from roleplay.util import get_yaml, get_yaml_from_string

from .llm import check_llm, get_llm
from .tool import Tool, get_tool, check_tool, create_tool
from .parse import RoleParser

from pydantic import BaseModel, Field
from langchain.schema import AgentAction, AgentFinish
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from langchain_core.runnables import RunnableSerializable

import os
import weakref
import logging
from typing import Any, Dict, List, Optional, Union

_logger = logging.getLogger(__name__)

class Role(BaseModel):
    name: str = Field(description='The name of the role')
    llm: str = Field(description='The name of the LLM to use')
    config: Dict[str, Any] = Field(description='The configuration for the role')
    prompt: ChatPromptTemplate = Field(description='The prompt to use for the role')
    tools: List[str] = Field(description='The tools to use for the role')
    parser: RoleParser = Field(default_factory=RoleParser)
    as_tool: Optional[Tool] = None
    llm_chain: Optional[RunnableSerializable[dict, BaseMessage]] = None

    def __init__(self, **data):
        super().__init__(**data)
        self._as_tool_init()
        self._set_llm()

    def _as_tool_init(self):
        if not self.as_tool:
            return
        self.as_tool._Tool._outer_tool = weakref.ref(self)

    def _get_tools(self):
        for tool_name in self.tools:
            if not check_tool(tool_name):
                raise ValueError(f"Tool {tool_name} not found.")
        return [get_tool(tool_name).to_ltool() for tool_name in self.tools]

    def _set_llm(self):
        if not check_llm(self.llm):
            raise ValueError(f"LLM {self.llm} not found.")
        if self.llm_chain is not None:
            return
        self.config['stream_usage'] = True
        llm = get_llm(self.llm, **self.config)
        if len(tools := self._get_tools()) > 0:
            llm = llm.bind_tools(tools)
        self.llm_chain = self.prompt | llm
    
    def set_llm(self, llm: str, **kwargs):
        self.llm = llm
        self.config = kwargs
        self._set_llm()

    def _invoke(self, **kwargs) -> AIMessage:
        return self.llm_chain.invoke(kwargs)

    def _tool_invoke(self, _input: List[BaseMessage]) -> AIMessage:
        input = {'input': _input}
        return self.llm_chain.invoke(input)

    def _post_invoke(self, _input: HumanMessage, outputs: Dict[str, Any]) -> int:
        return 0

    def _tool_loop(self, ai_msg: AIMessage, call: AgentAction, call_id: str,
                    tool_history: List[Union[BaseMessage]]) -> AgentFinish:
        while True:
            back = get_tool(call.tool).run(**call.tool_input)
            if not isinstance(back, str):
                raise ValueError("Bot tool back must return a string.")
            _logger.debug(f'Tool Back: {back}')
            tool_msg = ToolMessage(content=back, tool_call_id=call_id)
            self.parser.add_intermediate_step(call, ai_msg, tool_msg)

            ai_msg1 = self._tool_invoke(tool_history + [ai_msg, tool_msg])
            mp = self.parser.parse(ai_msg1)
            if isinstance(mp, AgentFinish):
                return mp

            if len(mp) > 0:
                action, _call_id = mp[0]
                call = action
                call_id = _call_id
                tool_history = tool_history + [ai_msg, tool_msg]
                ai_msg = ai_msg1
            else:
                raise ValueError("No action found in the parsed message.")

    def run(self, **kwargs) -> Dict[str, Any]:
        kwargs.update({'input': HumanMessage(content=kwargs.get('input') or '')})
        ai_msg = self._invoke(**kwargs)
        mp = self.parser.parse(ai_msg)
        if not isinstance(mp, AgentFinish):
            action, _call_id = mp[0]
            mp = self._tool_loop(ai_msg, action, _call_id, [kwargs['input']])
        if not isinstance(mp, AgentFinish):
            raise ValueError("Tool loop error.")
        self.parser.total_tokens += self._post_invoke(
            kwargs['input'],
            mp.return_values
        )
        return mp.return_values

_all_roles = {}

def register_role(name: str, role: Role):
    """
    Register a role with the given name.
    """
    if name in _all_roles:
        _logger.warning(f"Role {name} already exists.")
    _all_roles[name] = role
    _logger.debug(f"Registered role: {name}")

def check_role(name: str) -> bool:
    """
    Check if a role with the given name exists.
    """
    return name in _all_roles

def get_role(name: str) -> Role:
    """
    Get a role with the given name.
    """
    return _all_roles[name]

def create_role(role_data: dict) -> dict:
    role_name: str = role_data['name']
    role_llm: str = role_data['llm']
    role_prompt = []
    role_config: dict = role_data.get('config', {})
    as_tool: Tool = None
    role_tools_name: List[str] = role_data.get('tools', [])

    if role_data.get('as_tool', None):
        as_tool = create_tool(role_data['as_tool'])

    for p in role_data['prompt']:
        role: str = p['role']
        content: str = p['content']
        role_prompt.append((role, content))

    # return Role(role_name=role_name, role_llm=role_llm,
    #             role_prompt=ChatPromptTemplate.from_messages(role_prompt),
    #             role_config=role_config, role_tools_name=role_tools_name,
    #             as_tool=as_tool)
    return {'name': role_name, 'llm': role_llm,
            'prompt': ChatPromptTemplate.from_messages(role_prompt),
            'config': role_config, 'tools': role_tools_name,
            'as_tool': as_tool}

def load_role_from_string(role_string: str) -> Role:
    """
    Get a role from the given string and register it.
    """
    role_data = get_yaml_from_string(role_string)
    role = Role(**create_role(role_data))
    register_role(role.name, role)
    return role

def load_role(role_file: str) -> Role:
    """
    Get a role from the given file and register it.
    """
    role_data = get_yaml(role_file)
    role = Role(**create_role(role_data))
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
