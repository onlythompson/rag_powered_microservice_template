from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from src.core.config import settings
from .custom_llm import CustomLLM

def get_llm_model(model_name: str = None):
    model_name = model_name or settings.LLM_MODEL_NAME

    if model_name.startswith("gpt-3.5") or model_name.startswith("gpt-4"):
        return ChatOpenAI(model_name=model_name, temperature=settings.LLM_TEMPERATURE)
    elif model_name.startswith("text-"):
        return OpenAI(model_name=model_name, temperature=settings.LLM_TEMPERATURE)
    elif model_name == "custom":
        return CustomLLM(base_url=settings.CUSTOM_LLM_BASE_URL, api_key=settings.CUSTOM_LLM_API_KEY)
    else:
        raise ValueError(f"Unsupported LLM model: {model_name}")