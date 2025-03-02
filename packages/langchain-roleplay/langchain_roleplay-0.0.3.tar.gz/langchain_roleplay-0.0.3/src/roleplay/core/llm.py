
from roleplay.util import get_yaml, get_yaml_from_string

import openai
from langchain_openai import ChatOpenAI
# from langchain_deepseek import ChatDeepSeek

import os
import logging
from typing import Any, Dict, Iterator, List, Optional, Type, Union

# langchain-openai start
from json import JSONDecodeError
from langchain_core.outputs import ChatResult
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.messages import (
    BaseMessage,
    AIMessageChunk,
)
from langchain_core.outputs import ChatGenerationChunk, ChatResult

class ChatOpenAIReasoning(ChatOpenAI):
    def _create_chat_result(
        self,
        response: Union[dict, openai.BaseModel],
        generation_info: Optional[Dict] = None,
    ) -> ChatResult:
        rtn = super()._create_chat_result(response, generation_info)

        if not isinstance(response, openai.BaseModel):
            return rtn

        if hasattr(response.choices[0].message, "reasoning_content"):  # type: ignore
            rtn.generations[0].message.additional_kwargs["reasoning_content"] = (
                response.choices[0].message.reasoning_content  # type: ignore
            )

        return rtn

    def _convert_chunk_to_generation_chunk(
        self,
        chunk: dict,
        default_chunk_class: Type,
        base_generation_info: Optional[Dict],
    ) -> Optional[ChatGenerationChunk]:
        generation_chunk = super()._convert_chunk_to_generation_chunk(
            chunk,
            default_chunk_class,
            base_generation_info,
        )
        if (choices := chunk.get("choices")) and generation_chunk:
            top = choices[0]
            if reasoning_content := top.get("delta", {}).get("reasoning_content"):
                if isinstance(generation_chunk.message, AIMessageChunk):
                    generation_chunk.message.additional_kwargs["reasoning_content"] = (
                        reasoning_content
                    )
        return generation_chunk

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        try:
            yield from super()._stream(
                messages, stop=stop, run_manager=run_manager, **kwargs
            )
        except JSONDecodeError as e:
            raise JSONDecodeError(
                "API returned an invalid response. "
                "Please check the API status and try again.",
                e.doc,
                e.pos,
            ) from e

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        try:
            return super()._generate(
                messages, stop=stop, run_manager=run_manager, **kwargs
            )
        except JSONDecodeError as e:
            raise JSONDecodeError(
                "API returned an invalid response. "
                "Please check the API status and try again.",
                e.doc,
                e.pos,
            ) from e
# langchain-openai end

# class LLM(ChatOpenAIReasoning):
    # models: List[str]
    # api_keys: List[str]
    # api_keys_index: int = 0
    # def __init__(self, **kwargs):
    #     # self.name = kwargs.pop('name')
    #     self.api_keys = kwargs.pop('api_keys')
    #     self.index = 0
    #     self.models = kwargs.pop('models')
    #     self.kwargs = kwargs

    # def run(self, **kwargs) -> ChatOpenAIReasoning:
    #     _kwargs = self.kwargs.copy()
    #     _kwargs.update(kwargs)
    #     if self.index >= len(self.api_keys):
    #         self.index = 0
    #     if _kwargs.get('model') not in self.models:
    #         logging.warning(f"Model {_kwargs.get('model')} not found in {self.models}")
    #     if _kwargs.get('model') is None:
    #         _kwargs.update({'model': self.models[0]})
    #     _kwargs.update({'api_key': self.api_keys[self.index]})
    #     return ChatOpenAIReasoning(**_kwargs)

_logger = logging.getLogger(__name__)
_all_llms = {}

def register_llm(name: str, llm) -> None:
    if name in _all_llms:
        _logger.warning(f"LLM {name} already registered")
    _all_llms[name] = llm
    _logger.debug(f"LLM {name} registered")

def check_llm(name: str) -> bool:
    return name in _all_llms

def get_llm(name: str, **kwargs) -> ChatOpenAIReasoning:
    _dict = _all_llms[name].copy()
    _dict.update(kwargs)
    _logger.debug(f"LLM {name} created: {_dict}")
    return ChatOpenAIReasoning(**_dict)

def create_llm(llm_data: dict) -> ChatOpenAIReasoning:
    # return ChatOpenAIReasoning(**llm_data)
    return llm_data

def load_llm_from_string(llm_string: str):
    llm_data = get_yaml_from_string(llm_string)
    llm = create_llm(llm_data)
    register_llm(llm['name'], llm)

def load_llm(llm_file_path: str):
    llm_data = get_yaml(llm_file_path)
    llm = create_llm(llm_data)
    register_llm(llm['name'], llm)

def load_llms_from_dir(llm_dir_path: str):
    for file in os.listdir(llm_dir_path):
        if file.endswith('.llm.yaml'):
            load_llm(os.path.join(llm_dir_path, file))