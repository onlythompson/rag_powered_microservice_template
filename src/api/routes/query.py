from fastapi import APIRouter, HTTPException
from src.services import QueryService
from src.api.schemas.request_schemas import QueryRequest
from src.api.schemas.response_schemas import QueryResponse
from src.chains.advanced_rag_chain import AdvancedRAGChain
from src.core.observability import logger
from pydantic import BaseModel

router = APIRouter()
query_service = QueryService()
advanced_rag_chain = AdvancedRAGChain()

class Query(BaseModel):
    query: str

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        result = await query_service.process_query(request.query, request.conversation_id)
        logger.info(f"Query processed: {request.query[:50]}...")
        return QueryResponse(
            query=request.query,
            answer=result['answer'],
            source_documents=result['source_documents']
        )
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query_extended", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        result = await query_service.process_query(request.query)
        return QueryResponse(
            query=request.query,
            answer=result['answer'],
            source_documents=result['source_documents']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query/advanced")
async def advanced_query(query: Query):
    try:
        result = await advanced_rag_chain.run(query.query)
        return {"query": query.query, "response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
