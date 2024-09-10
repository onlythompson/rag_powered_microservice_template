from langchain.chains import LLMChain
from src.llms import get_llm_model
from src.prompts import PromptManager, get_qa_prompt
from src.core.config import settings
from src.core.observability import logger, trace_and_measure
from .base_chain import BaseChain

class QuestionAnsweringChain(BaseChain):
    def __init__(self):
        self.llm = get_llm_model(settings.LLM_MODEL_NAME)
        self.prompt_manager = PromptManager()
        self.prompt_manager.add_prompt("qa", get_qa_prompt())
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_manager.get_prompt("qa"))

    @trace_and_measure("qa_chain_call")
    async def _acall(self, inputs: dict) -> dict:
        question = inputs["question"]
        context = inputs["context"]
        logger.info(f"QA Chain processing question: {question[:50]}...")
        answer = await self.chain.arun(question=question, context=context)
        return {"question": question, "answer": answer}