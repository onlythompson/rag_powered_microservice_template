from pydantic import BaseModel
from typing import Optional, Dict

class TextIngestionRequest(BaseModel):
    text: str
    metadata: Optional[Dict[str, str]] = None

class QueryRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None

class UpdateDocumentRequest(BaseModel):
    doc_id: str
    new_text: str
    new_metadata: Optional[Dict[str, str]] = None

class ConversationMessageRequest(BaseModel):
    conversation_id: str
    message: str