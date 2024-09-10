from src.vectorstores import VectorStoreFactory
from src.llms import get_llm_model
from src.prompts import PromptManager, get_qa_prompt
from src.memory import MemoryManager, ConversationBufferMemory
from src.core.observability import logger, trace_and_measure
from src.core.config import settings

class QueryService:
    def __init__(self):
        self.vector_store = VectorStoreFactory.get_vector_store(settings.VECTOR_STORE_TYPE)
        self.llm = get_llm_model(settings.LLM_MODEL_NAME)
        self.prompt_manager = PromptManager()
        self.prompt_manager.add_prompt("qa", get_qa_prompt())
        self.memory_manager = MemoryManager()

    @trace_and_measure("process_query")
    async def process_query(self, query: str, conversation_id: str = None):
        relevant_docs = self.vector_store.similarity_search(query, k=3)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        
        if conversation_id:
            if conversation_id not in self.memory_manager.memories:
                self.memory_manager.add_memory(conversation_id, ConversationBufferMemory())
            memory = self.memory_manager.get_memory(conversation_id)
            memory.add_user_message(query)
        else:
            memory = None

        prompt = self.prompt_manager.format_prompt("qa", question=query, context=context)
        
        if memory:
            prompt += f"\nPrevious conversation:\n{memory.buffer}"

        response = self.llm(prompt)
        
        if memory:
            memory.add_ai_message(response)

        logger.info(f"Processed query: {query[:50]}...")
        return {"query": query, "answer": response, "source_documents": [doc.metadata for doc in relevant_docs]}