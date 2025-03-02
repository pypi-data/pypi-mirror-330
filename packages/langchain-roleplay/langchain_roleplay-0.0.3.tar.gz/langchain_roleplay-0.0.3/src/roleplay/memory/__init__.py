
# Block
# from .block import BlockMemory
# Limit
from .limit import LimitMemory
# Long
# from long import LongMemory
# Block with Long
# from .block_long import BlockMemoryWithLong

__pair__ = {
    # 'block': BlockMemory,
    'limit': LimitMemory,
    # 'long': LongMemory,
    # 'block_long': BlockMemoryWithLong,
}

from roleplay.core.memory import BaseMemory
def register_memory(name: str, memory: BaseMemory) -> None:
    """
    Register a memory to the pair.
    """
    if not isinstance(memory, BaseMemory):
        raise ValueError(f'Memory {name} must be a subclass of BaseMemory.')
    __pair__[name] = memory

# Role with Memory
from .role import RoleWithMemory
from .role import RoleWithMemory as Role
# load functions
from .role import create_role_with_memory
from .role import create_role_with_memory as create_role
from .role import load_role_from_string, load_role, load_roles_from_dir