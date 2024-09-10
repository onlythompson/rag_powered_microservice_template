from langchain.embeddings import HuggingFaceEmbeddings
from typing import List

class CustomHuggingFaceEmbeddings(HuggingFaceEmbeddings):
    def __init__(self, model_name: str, model_kwargs: dict = None, **kwargs):
        super().__init__(model_name=model_name, model_kwargs=model_kwargs, **kwargs)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # Add any custom preprocessing here
        embeddings = super().embed_documents(texts)
        # Add any custom postprocessing here
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        # Add any custom preprocessing here
        embedding = super().embed_query(text)
        # Add any custom postprocessing here
        return embedding
