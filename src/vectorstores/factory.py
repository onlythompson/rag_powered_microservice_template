# src/vectorstores/factory.py

from src.vectorstores.pinecone_store import PineconeVectorStore
from src.vectorstores.mongodb_store import MongoDBVectorStore

class VectorStoreFactory:
    @staticmethod
    def get_vector_store(store_type: str):
        if store_type.lower() == 'pinecone':
            return PineconeVectorStore()
        elif store_type.lower() == 'mongodb':
            return MongoDBVectorStore()
        else:
            raise ValueError(f"Unsupported vector store type: {store_type}")