from langchain.chains import RetrievalQA
from src.llms import get_llm_model
from src.vectorstores import VectorStoreFactory
from src.prompts import PromptManager, get_qa_prompt
from src.core.config import settings
from src.core.observability import logger, trace_and_measure
from .base_chain import BaseChain

class RAGChain(BaseChain):
    def __init__(self):
        self.llm = get_llm_model(settings.LLM_MODEL_NAME)
        self.vector_store = VectorStoreFactory.get_vector_store(settings.VECTOR_STORE_TYPE)
        self.prompt_manager = PromptManager()
        self.prompt_manager.add_prompt("qa", get_qa_prompt())
        self.retrieval_qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_manager.get_prompt("qa")}
        )

    @trace_and_measure("rag_chain_call")
    async def _acall(self, inputs: dict) -> dict:
        query = inputs["query"]
        logger.info(f"RAG Chain processing query: {query[:50]}...")
        result = await self.retrieval_qa(query)
        return {
            "query": query,
            "result": result["result"],
            "source_documents": [doc.page_content for doc in result["source_documents"]]
        }
