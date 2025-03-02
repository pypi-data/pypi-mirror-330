
from langchain_core.messages import HumanMessage, BaseMessage
from pydantic import BaseModel, Field

import logging
from datetime import datetime
from typing import Any, Dict, List

_logger = logging.getLogger(__name__)

class BaseMemory(BaseModel):
    memories: Dict[str, Any] = Field(default={'meta': [], 'history': []})

    def _load(self, _input, history: List) -> Dict[str, Any]:
        return {}
    def _save(self, _input: HumanMessage, outputs: Dict[str, Any]) -> int:
        return 0
    def _clear(self) -> None:
        pass

    def load(self, _input) -> Dict[str, Any]:
        history = []
        for h in self.memories['history']:
            history.append(h['input'])
            for (_, msg, ob) in h['intermediate_steps']:
                history.append(msg)
                history.append(ob)
            history.append(h['output'])

        if isinstance(_input['input'], BaseMessage):
            history.append(_input['input'])
        if isinstance(_input['input'], list):
            for msg in _input['input']:
                if not isinstance(msg, BaseMessage):
                    raise ValueError(f"Got unexpected input type {type(msg)}")
            history.extend(_input['input'])

        return_dict = {'history': history}
        return_dict.update(self._load(_input, history))
        _logger.debug(f"Memory loaded: {return_dict}")
        return return_dict

    def save(self, _input: HumanMessage, outputs: Dict[str, Any]) -> int:
        _logger.debug(f"Memory saved: {outputs}")
        self.memories['meta'].append({'input': _input, 'output': outputs, 'time': datetime.now()})
        self.memories['history'].append({'input': _input,
                                            'output': outputs['output'],
                                            'intermediate_steps': outputs['intermediate_steps']})
        return self._save(_input, outputs)

    def clear(self) -> None:
        self.memories['meta'] = []
        self.memories['history'] = []
        self._clear()
        _logger.debug(f"Memory cleared")