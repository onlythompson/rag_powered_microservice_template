from pydantic import BaseModel
from typing import List, Dict

class IngestionResponse(BaseModel):
    message: str
    document_count: int

class QueryResponse(BaseModel):
    query: str
    answer: str
    source_documents: List[Dict[str, str]]

class IndexStatsResponse(BaseModel):
    document_count: int
    index_size: str

class OperationResponse(BaseModel):
    message: str

class ConversationResponse(BaseModel):
    response: str
    summary: str

class ConversationSummaryResponse(BaseModel):
    summary: str