from langchain.chains import LLMChain
from src.llms import get_llm_model
from src.prompts import PromptManager, get_summarization_prompt
from src.core.config import settings
from src.core.observability import logger, trace_and_measure
from .base_chain import BaseChain

class SummarizationChain(BaseChain):
    def __init__(self):
        self.llm = get_llm_model(settings.LLM_MODEL_NAME)
        self.prompt_manager = PromptManager()
        self.prompt_manager.add_prompt("summarize", get_summarization_prompt())
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_manager.get_prompt("summarize"))

    @trace_and_measure("summarization_chain_call")
    async def _acall(self, inputs: dict) -> dict:
        text = inputs["text"]
        logger.info(f"Summarization Chain processing text: {text[:50]}...")
        summary = await self.chain.arun(text=text)
        return {"summary": summary}