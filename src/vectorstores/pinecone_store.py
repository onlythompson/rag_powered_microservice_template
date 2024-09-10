
from pinecone import Pinecone, ServerlessSpec
from langchain.vectorstores import Pinecone as LangchainPinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from src.core.config import settings
from src.vectorstores.base_store import BaseVectorStore

class PineconeVectorStore(BaseVectorStore):
    def __init__(self):
        self.index_name = settings.PINECONE_INDEX_NAME
        self.embedding = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL_NAME)
        self._init_pinecone()

    def _init_pinecone(self):
        Pinecone.init(
            api_key=settings.PINECONE_API_KEY,
            environment=settings.PINECONE_ENVIRONMENT
        )
        if self.index_name not in Pinecone.list_indexes():
            Pinecone.create_index(
                name=self.index_name,
                metric='cosine',
                dimension=1536  # OpenAI embedding dimension
            )
        self.index = pinecone.Index(self.index_name)

    def add_texts(self, texts, metadatas=None):
        return LangchainPinecone.from_texts(
            texts=texts,
            embedding=self.embedding,
            index_name=self.index_name,
            metadatas=metadatas
        )

    def add_documents(self, documents):
        return LangchainPinecone.from_documents(
            documents=documents,
            embedding=self.embedding,
            index_name=self.index_name
        )

    def similarity_search(self, query, k=4):
        vectorstore = LangchainPinecone.from_existing_index(
            index_name=self.index_name,
            embedding=self.embedding
        )
        return vectorstore.similarity_search(query, k=k)

    def delete_all(self):
        self.index.delete(delete_all=True)

    def custom_search(self, query, filter=None, k=4):
        vectorstore = LangchainPinecone.from_existing_index(
            index_name=self.index_name,
            embedding=self.embedding
        )
        return vectorstore.similarity_search(
            query,
            filter=filter,
            k=k
        )

    def update_document(self, doc_id, new_text, new_metadata=None):
        embedded_query = self.embedding.embed_query(new_text)
        self.index.upsert(
            vectors=[(doc_id, embedded_query, new_metadata)]
        )

    def delete_document(self, doc_id):
        self.index.delete(ids=[doc_id])

