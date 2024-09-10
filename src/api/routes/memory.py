from fastapi import APIRouter, HTTPException
from src.memory import MemoryManager, ConversationBufferMemory, ConversationSummaryMemory, ConversationKGMemory
from src.memory.memory_utils import serialize_memory, deserialize_memory
from pydantic import BaseModel

router = APIRouter()
memory_manager = MemoryManager()

class MemoryCreate(BaseModel):
    name: str
    type: str

@router.post("/memories")
async def create_memory(memory: MemoryCreate):
    try:
        if memory.type == "buffer":
            new_memory = ConversationBufferMemory()
        elif memory.type == "summary":
            new_memory = ConversationSummaryMemory()
        elif memory.type == "kg":
            new_memory = ConversationKGMemory()
        else:
            raise ValueError(f"Unsupported memory type: {memory.type}")
        
        memory_manager.add_memory(memory.name, new_memory)
        return {"message": f"Memory '{memory.name}' created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/memories")
async def list_memories():
    return memory_manager.list_memories()

@router.delete("/memories/{name}")
async def delete_memory(name: str):
    try:
        memory_manager.remove_memory(name)
        return {"message": f"Memory '{name}' deleted successfully"}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Memory '{name}' not found")

@router.post("/memories/{name}/clear")
async def clear_memory(name: str):
    try:
        memory = memory_manager.get_memory(name)
        if hasattr(memory, 'clear'):
            memory.clear()
            return {"message": f"Memory '{name}' cleared successfully"}
        else:
            raise HTTPException(status_code=400, detail=f"Memory '{name}' does not support clearing")
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Memory '{name}' not found")

@router.get("/memories/{name}/serialize")
async def serialize_memory_endpoint(name: str):
    try:
        memory = memory_manager.get_memory(name)
        serialized = serialize_memory(memory)
        return {"serialized_memory": serialized}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Memory '{name}' not found")

@router.post("/memories/{name}/deserialize")
async def deserialize_memory_endpoint(name: str, serialized_data: str):
    try:
        memory_type = memory_manager.get_memory(name).__class__.__name__
        deserialized_memory = deserialize_memory(memory_type, serialized_data)
        memory_manager.add_memory(name, deserialized_memory)
        return {"message": f"Memory '{name}' deserialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))