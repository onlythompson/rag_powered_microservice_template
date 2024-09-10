from src.memory import MemoryManager, ConversationSummaryMemory
from src.llms import get_llm_model
from src.prompts import PromptManager, get_summarization_prompt
from src.core.observability import logger, trace_and_measure
from src.core.config import settings

class ConversationService:
    def __init__(self):
        self.memory_manager = MemoryManager()
        self.llm = get_llm_model(settings.LLM_MODEL_NAME)
        self.prompt_manager = PromptManager()
        self.prompt_manager.add_prompt("summarize", get_summarization_prompt())

    @trace_and_measure("process_message")
    async def process_message(self, conversation_id: str, message: str):
        if conversation_id not in self.memory_manager.memories:
            self.memory_manager.add_memory(conversation_id, ConversationSummaryMemory(llm=self.llm))
        
        memory = self.memory_manager.get_memory(conversation_id)
        memory.add_message(message)

        summary = memory.predict_new_summary(
            messages=[message],
            existing_summary=memory.buffer
        )

        prompt = self.prompt_manager.format_prompt("summarize", text=summary)
        response = self.llm(prompt)

        logger.info(f"Processed message for conversation: {conversation_id}")
        return {"response": response, "summary": summary}

    @trace_and_measure("get_conversation_summary")
    async def get_conversation_summary(self, conversation_id: str):
        if conversation_id not in self.memory_manager.memories:
            raise ValueError(f"No conversation found for id: {conversation_id}")
        
        memory = self.memory_manager.get_memory(conversation_id)
        return {"summary": memory.buffer}

    @trace_and_measure("clear_conversation")
    async def clear_conversation(self, conversation_id: str):
        if conversation_id in self.memory_manager.memories:
            self.memory_manager.remove_memory(conversation_id)
            logger.info(f"Cleared conversation: {conversation_id}")
            return {"message": f"Conversation {conversation_id} cleared successfully"}
        else:
            logger.warning(f"Attempt to clear non-existent conversation: {conversation_id}")
            return {"message": f"No conversation found for id: {conversation_id}"}