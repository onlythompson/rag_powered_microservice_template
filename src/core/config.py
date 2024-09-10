# src/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RAG Powered Microservice"
    VERSION: str = "1.0.0"
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    PINECONE_INDEX_NAME: str
    MODEL_NAME: str = "gpt-3.5-turbo"
    EMBEDDING_MODEL_NAME: str = "text-embedding-ada-002"
    VECTOR_STORE_TYPE: str = "pinecone"
    MONGODB_VECTOR_STORE_TYPE: str = "mongodb"
    MONGODB_URI: str
    MONGODB_DB_NAME: str
    MONGODB_COLLECTION_NAME: str
    EMBEDDING_MODEL_NAME: str = "text-embedding-ada-002"
    CUSTOM_HUGGINGFACE_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    CUSTOM_HUGGINGFACE_MODEL_KWARGS: dict = {"device": "cpu"}
    LLM_MODEL_NAME: str = "gpt-3.5-turbo"
    LLM_TEMPERATURE: float = 0.7
    CUSTOM_LLM_BASE_URL: str = "http://custom-llm-api.example.com"
    CUSTOM_LLM_API_KEY: str = "your-custom-llm-api-key"


    class Config:
        env_file = ".env"

settings = Settings()