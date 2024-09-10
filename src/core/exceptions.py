class RAGException(Exception):
    """Base exception for RAG microservice"""

class DocumentProcessingError(RAGException):
    """Raised when there's an error processing a document"""

class EmbeddingError(RAGException):
    """Raised when there's an error generating embeddings"""

class VectorStoreError(RAGException):
    """Raised when there's an error with the vector store operations"""

class LLMError(RAGException):
    """Raised when there's an error with the language model"""