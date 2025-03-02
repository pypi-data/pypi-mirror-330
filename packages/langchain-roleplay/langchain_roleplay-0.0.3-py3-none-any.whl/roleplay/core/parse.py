
from langchain.schema import AgentAction, AgentFinish
from langchain_core.messages import AIMessage, ToolMessage
from pydantic import BaseModel

import logging
from typing import List, Tuple, Union

_logger = logging.getLogger(__name__)

class RoleParser(BaseModel):
    total_tokens: int = 0
    total_hit_tokens: int = 0
    total_miss_tokens: int = 0
    last_total_tokens: int = 0
    intermediate_steps: List[Tuple[AgentAction, AIMessage, ToolMessage]] = []

    def parse(self, message: AIMessage) -> Union[List[Tuple[AgentAction, str]], AgentFinish]:
        # 提取 token 使用情况
        token_usage = message.response_metadata.get("token_usage", {})
        if not token_usage:
            _logger.warning("No token usage found in message.")
            token_usage = {}
        total_tokens = token_usage.get("total_tokens", 0)

        self.total_tokens += total_tokens
        # DeepSeek Server
        self.total_hit_tokens += token_usage.get("prompt_cache_hit_tokens", 0)
        self.total_miss_tokens += token_usage.get("prompt_cache_miss_tokens", 0)
        # 检查是否有 tool_calls
        if hasattr(message, "tool_calls") and message.tool_calls:
            self.last_total_tokens += total_tokens
            actions = []
            for tool_call in message.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_call_id = tool_call["id"]
                actions.append((AgentAction(
                    tool=tool_name,
                    tool_input=tool_args,
                    log=f"{tool_name}({tool_args})"
                ), tool_call_id))
            if len(actions) > 1:
                raise ValueError("Only one tool call is allowed.")
            _logger.debug(f"Tool call found: {tool_name}({tool_args})")
            return actions
        # 如果没有 返回 AgentFinish
        self.last_total_tokens += total_tokens
        _last_total_tokens = self.last_total_tokens
        self.last_total_tokens = 0

        intermediate_steps = self.intermediate_steps.copy()
        self.intermediate_steps = []
        return AgentFinish(
            return_values={"output": message,
                           "intermediate_steps": intermediate_steps,
                           "total_tokens": _last_total_tokens},
            log=f"{message.content}"
        )

    def add_intermediate_step(self, step: AgentAction, message: AIMessage,
                              observation: ToolMessage):
        self.intermediate_steps.append((step, message, observation))