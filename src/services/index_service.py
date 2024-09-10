from src.vectorstores import VectorStoreFactory
from src.core.observability import logger, trace_and_measure
from src.core.config import settings

class IndexService:
    def __init__(self):
        self.vector_store = VectorStoreFactory.get_vector_store(settings.VECTOR_STORE_TYPE)

    @trace_and_measure("get_index_stats")
    async def get_index_stats(self):
        stats = self.vector_store.get_stats()
        logger.info(f"Retrieved index stats: {stats}")
        return stats

    @trace_and_measure("clear_index")
    async def clear_index(self):
        self.vector_store.clear()
        logger.info("Cleared vector store index")
        return {"message": "Index cleared successfully"}

    @trace_and_measure("update_document")
    async def update_document(self, doc_id: str, new_text: str, new_metadata: dict = None):
        self.vector_store.update_document(doc_id, new_text, new_metadata)
        logger.info(f"Updated document: {doc_id}")
        return {"message": f"Document {doc_id} updated successfully"}

    @trace_and_measure("delete_document")
    async def delete_document(self, doc_id: str):
        self.vector_store.delete_document(doc_id)
        logger.info(f"Deleted document: {doc_id}")
        return {"message": f"Document {doc_id} deleted successfully"}