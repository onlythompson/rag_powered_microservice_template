# src/vectorstores/mongodb_store.py

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from src.core.config import settings
from src.vectorstores.base_store import BaseVectorStore
import numpy as np

class MongoDBVectorStore(BaseVectorStore):
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_DB_NAME]
        self.collection = self.db[settings.MONGODB_COLLECTION_NAME]
        self.embedding = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL_NAME)
        self._create_index()

    def _create_index(self):
        self.collection.create_index([("vector", "2dsphere")])

    def add_texts(self, texts, metadatas=None):
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        embeddings = self.embedding.embed_documents(texts)
        
        documents = []
        for i, (text, embedding, metadata) in enumerate(zip(texts, embeddings, metadatas)):
            doc = {
                "text": text,
                "vector": embedding,
                "metadata": metadata
            }
            documents.append(doc)
        
        try:
            self.collection.insert_many(documents)
        except DuplicateKeyError:
            print("Some documents already exist. Skipping duplicates.")

    def add_documents(self, documents):
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        self.add_texts(texts, metadatas)

    def similarity_search(self, query, k=4):
        query_embedding = self.embedding.embed_query(query)
        results = self.collection.aggregate([
            {
                "$search": {
                    "knnBeta": {
                        "vector": query_embedding,
                        "path": "vector",
                        "k": k
                    }
                }
            },
            {
                "$project": {
                    "text": 1,
                    "metadata": 1,
                    "score": {"$meta": "searchScore"}
                }
            }
        ])

        documents = []
        for result in results:
            doc = Document(
                page_content=result["text"],
                metadata=result["metadata"]
            )
            documents.append(doc)

        return documents

    def delete_all(self):
        self.collection.delete_many({})

    def custom_search(self, query, filter=None, k=4):
        query_embedding = self.embedding.embed_query(query)
        search_stage = {
            "$search": {
                "knnBeta": {
                    "vector": query_embedding,
                    "path": "vector",
                    "k": k
                }
            }
        }

        if filter:
            search_stage["$search"]["compound"] = {
                "must": [search_stage["$search"]["knnBeta"]],
                "filter": [{"text": filter}]
            }
            del search_stage["$search"]["knnBeta"]

        results = self.collection.aggregate([
            search_stage,
            {
                "$project": {
                    "text": 1,
                    "metadata": 1,
                    "score": {"$meta": "searchScore"}
                }
            }
        ])

        documents = []
        for result in results:
            doc = Document(
                page_content=result["text"],
                metadata=result["metadata"]
            )
            documents.append(doc)

        return documents

    def update_document(self, doc_id, new_text, new_metadata=None):
        new_embedding = self.embedding.embed_query(new_text)
        update_data = {
            "text": new_text,
            "vector": new_embedding
        }
        if new_metadata:
            update_data["metadata"] = new_metadata
        
        self.collection.update_one({"_id": doc_id}, {"$set": update_data})

    def delete_document(self, doc_id):
        self.collection.delete_one({"_id": doc_id})
