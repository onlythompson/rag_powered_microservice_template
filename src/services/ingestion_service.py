from src.data import CustomPDFLoader, CustomCSVLoader
from src.vectorstores import VectorStoreFactory
from src.embeddings import get_embedding_model
from src.core.observability import logger, trace_and_measure
from src.core.config import settings

class IngestionService:
    def __init__(self):
        self.vector_store = VectorStoreFactory.get_vector_store(settings.VECTOR_STORE_TYPE)
        self.embedding_model = get_embedding_model(settings.EMBEDDING_MODEL_NAME)

    @trace_and_measure("ingest_file")
    async def ingest_file(self, file_path: str, file_type: str):
        if file_type == 'pdf':
            loader = CustomPDFLoader(file_path)
        elif file_type == 'csv':
            loader = CustomCSVLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        documents = loader.load()
        logger.info(f"Loaded {len(documents)} documents from {file_path}")

        embeddings = self.embedding_model.embed_documents([doc.page_content for doc in documents])
        self.vector_store.add_embeddings(embeddings, documents)
        logger.info(f"Ingested {len(documents)} documents into vector store")

        return {"message": f"Successfully ingested {len(documents)} documents", "document_count": len(documents)}

    @trace_and_measure("ingest_text")
    async def ingest_text(self, text: str, metadata: dict = None):
        embedding = self.embedding_model.embed_query(text)
        self.vector_store.add_embeddings([embedding], [{"page_content": text, "metadata": metadata or {}}])
        logger.info("Ingested text into vector store")

        return {"message": "Successfully ingested text", "document_count": 1}