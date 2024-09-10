from abc import ABC, abstractmethod

class BaseVectorStore(ABC):
    @abstractmethod
    def add_texts(self, texts, metadatas=None):
        pass

    @abstractmethod
    def add_documents(self, documents):
        pass

    @abstractmethod
    def similarity_search(self, query, k=4):
        pass

    @abstractmethod
    def delete_all(self):
        pass

    @abstractmethod
    def custom_search(self, query, filter=None, k=4):
        pass

    @abstractmethod
    def update_document(self, doc_id, new_text, new_metadata=None):
        pass

    @abstractmethod
    def delete_document(self, doc_id):
        pass