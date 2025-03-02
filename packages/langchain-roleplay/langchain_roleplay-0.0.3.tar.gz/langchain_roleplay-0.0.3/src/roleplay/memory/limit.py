
from roleplay.core.memory import BaseMemory

from pydantic import Field
from typing import Any, Dict, Optional, List

class LimitMemory(BaseMemory):
    limit: int = Field(default=100, description="The maximum number of memories to keep.")
    keep_first: bool = Field(default=False, description="Whether to keep the first or last memories.")

    def _load(self, _input, history: List) -> Dict[str, Any]:
        if self.keep_first:
            first_item = history[0] if history else None
            recent_history = history[-self.limit + 1:] if len(history) > 1 else []
            return {'history': [first_item] + recent_history}
        return {'history': history[-self.limit:]}