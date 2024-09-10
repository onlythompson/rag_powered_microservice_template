from typing import Dict, Any
from src.core.observability import logger

class MemoryManager:
    def __init__(self):
        self.memories: Dict[str, Any] = {}

    def add_memory(self, name: str, memory: Any):
        if name in self.memories:
            logger.warning(f"Overwriting existing memory: {name}")
        self.memories[name] = memory
        logger.info(f"Added memory: {name}")

    def get_memory(self, name: str) -> Any:
        if name not in self.memories:
            raise KeyError(f"Memory not found: {name}")
        return self.memories[name]

    def remove_memory(self, name: str):
        if name in self.memories:
            del self.memories[name]
            logger.info(f"Removed memory: {name}")
        else:
            logger.warning(f"Attempt to remove non-existent memory: {name}")

    def list_memories(self) -> Dict[str, str]:
        return {name: str(memory) for name, memory in self.memories.items()}

    def clear_all_memories(self):
        for memory in self.memories.values():
            if hasattr(memory, 'clear'):
                memory.clear()
        logger.info("Cleared all memories")