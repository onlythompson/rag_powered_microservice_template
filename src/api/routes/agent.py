# src/api/routes/agent.py

from fastapi import APIRouter, HTTPException
from src.agents.rag_agent import RAGAgent
from pydantic import BaseModel

router = APIRouter()
rag_agent = RAGAgent()

class AgentQuery(BaseModel):
    query: str

@router.post("/agent/query")
async def agent_query(query: AgentQuery):
    try:
        result = await rag_agent.run(query.query)
        return {"query": query.query, "response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))