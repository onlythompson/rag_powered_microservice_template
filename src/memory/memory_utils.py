from typing import Any, List, Dict
import json

from memory.custom_memory import ConversationBufferMemory, ConversationKGMemory, ConversationSummaryMemory

def serialize_memory(memory: Any) -> str:
    """Serialize memory object to JSON string."""
    if hasattr(memory, 'to_json'):
        return memory.to_json()
    elif hasattr(memory, '__dict__'):
        return json.dumps(memory.__dict__)
    else:
        raise ValueError(f"Unable to serialize memory of type: {type(memory)}")

def deserialize_memory(memory_type: str, serialized_memory: str) -> Any:
    """Deserialize JSON string to memory object."""
    data = json.loads(serialized_memory)
    if memory_type == "ConversationBufferMemory":
        return ConversationBufferMemory(**data)
    elif memory_type == "ConversationSummaryMemory":
        return ConversationSummaryMemory(**data)
    elif memory_type == "ConversationKGMemory":
        return ConversationKGMemory(**data)
    else:
        raise ValueError(f"Unsupported memory type: {memory_type}")