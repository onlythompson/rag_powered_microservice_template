from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from src.core.config import settings
from .custom_embeddings import CustomHuggingFaceEmbeddings

def get_embedding_model(model_name: str = None):
    model_name = model_name or settings.EMBEDDING_MODEL_NAME

    if model_name == "text-embedding-ada-002":
        return OpenAIEmbeddings(model=model_name)
    elif model_name.startswith("sentence-transformers/"):
        return HuggingFaceEmbeddings(model_name=model_name)
    elif model_name == "custom-huggingface":
        return CustomHuggingFaceEmbeddings(
            model_name=settings.CUSTOM_HUGGINGFACE_MODEL_NAME,
            model_kwargs=settings.CUSTOM_HUGGINGFACE_MODEL_KWARGS
        )
    else:
        raise ValueError(f"Unsupported embedding model: {model_name}")