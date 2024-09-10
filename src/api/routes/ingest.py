
from fastapi import APIRouter, HTTPException, UploadFile, File
from src.services import IngestionService
from src.api.schemas.request_schemas import TextIngestionRequest
from src.api.schemas.response_schemas import IngestionResponse
from src.core.observability import logger

router = APIRouter()
ingestion_service = IngestionService()

@router.post("/ingest/file", response_model=IngestionResponse)
async def ingest_file(file: UploadFile = File(...)):
    try:
        file_type = file.filename.split('.')[-1].lower()
        if file_type not in ['pdf', 'csv']:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        result = await ingestion_service.ingest_file(file.file, file_type)
        logger.info(f"File ingested: {file.filename}")
        return IngestionResponse(message=f"Ingested file: {file.filename}", document_count=result['document_count'])
    except Exception as e:
        logger.error(f"Error ingesting file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest/text", response_model=IngestionResponse)
async def ingest_text(request: TextIngestionRequest):
    try:
        result = await ingestion_service.ingest_text(request.text, request.metadata)
        logger.info("Text ingested successfully")
        return IngestionResponse(message="Ingested text successfully", document_count=result['document_count'])
    except Exception as e:
        logger.error(f"Error ingesting text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest/directory")
async def ingest_directory(directory: str):
    try:
        result = await ingestion_service.ingest_documents(directory)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
