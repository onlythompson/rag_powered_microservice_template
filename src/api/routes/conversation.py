from fastapi import APIRouter, HTTPException
from src.services import ConversationService
from src.api.schemas.request_schemas import ConversationMessageRequest
from src.api.schemas.response_schemas import ConversationResponse, ConversationSummaryResponse, OperationResponse
from src.core.observability import logger

router = APIRouter()
conversation_service = ConversationService()

@router.post("/conversation/message", response_model=ConversationResponse)
async def process_message(request: ConversationMessageRequest):
    try:
        result = await conversation_service.process_message(request.conversation_id, request.message)
        logger.info(f"Message processed for conversation: {request.conversation_id}")
        return ConversationResponse(
            response=result['response'],
            summary=result['summary']
        )
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversation/{conversation_id}/summary", response_model=ConversationSummaryResponse)
async def get_conversation_summary(conversation_id: str):
    try:
        result = await conversation_service.get_conversation_summary(conversation_id)
        logger.info(f"Summary retrieved for conversation: {conversation_id}")
        return ConversationSummaryResponse(summary=result['summary'])
    except ValueError as e:
        logger.error(f"Conversation not found: {conversation_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving conversation summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/conversation/{conversation_id}/clear", response_model=OperationResponse)
async def clear_conversation(conversation_id: str):
    try:
        result = await conversation_service.clear_conversation(conversation_id)
        logger.info(f"Conversation cleared: {conversation_id}")
        return OperationResponse(message=result['message'])
    except Exception as e:
        logger.error(f"Error clearing conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))