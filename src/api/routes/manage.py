from fastapi import APIRouter, HTTPException
from src.services.index_service import IndexService
from src.api.schemas.request_schemas import UpdateDocumentRequest
from src.api.schemas.response_schemas import IndexStatsResponse, OperationResponse

router = APIRouter()
index_service = IndexService()

@router.get("/index/stats", response_model=IndexStatsResponse)
async def get_index_stats():
    try:
        stats = await index_service.get_index_stats()
        return IndexStatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/index/clear", response_model=OperationResponse)
async def clear_index():
    try:
        result = await index_service.clear_index()
        return OperationResponse(message=result['message'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/index/document", response_model=OperationResponse)
async def update_document(request: UpdateDocumentRequest):
    try:
        result = await index_service.update_document(request.doc_id, request.new_text, request.new_metadata)
        return OperationResponse(message=result['message'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/index/document/{doc_id}", response_model=OperationResponse)
async def delete_document(doc_id: str):
    try:
        result = await index_service.delete_document(doc_id)
        return OperationResponse(message=result['message'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))