from enum import Enum

class DocumentType(Enum):
    PDF = "pdf"
    TXT = "txt"
    HTML = "html"
    CSV = "csv"

class VectorStoreType(Enum):
    FAISS = "faiss"
    PINECONE = "pinecone"
    MILVUS = "milvus"

class EmbeddingModelType(Enum):
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    CUSTOM = "custom"

MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30  # seconds