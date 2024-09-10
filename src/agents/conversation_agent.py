from chains.chain_factory import ChainFactory
from src.services import ConversationService
from src.core.observability import logger, trace_and_measure
from .base_agent import BaseAgent

class ConversationAgent(BaseAgent):
    def __init__(self):
        self.conversation_service = ConversationService()
        self.qa_chain = ChainFactory.get_chain("qa")


    @trace_and_measure("run")
    async def run(self, conversation_id: str, message: str) -> dict:
        logger.info(f"Running Conversation Agent for conversation: {conversation_id}")
        
        # First, get the conversation summary
        summary = await self.get_summary(conversation_id)
        
        # Then, use the QA chain to generate a response
        response = await self.qa_chain.acall({"question": message, "context": summary})
        
        # Update the summary with the new message and response
        new_summary = await self.summarization_chain.acall({"text": f"{summary}\nHuman: {message}\nAI: {response['answer']}"})
        
        return {
            "response": response['answer'],
            "summary": new_summary['summary']
        }

    # @trace_and_measure("run")
    # async def run(self, conversation_id: str, message: str) -> dict:
    #     logger.info(f"Running Conversation Agent for conversation: {conversation_id}")
    #     result = await self.conversation_service.process_message(conversation_id, message)
    #     return {
    #         "response": result['response'],
    #         "summary": result['summary']
    #     }

    @trace_and_measure("get_summary")
    async def get_summary(self, conversation_id: str) -> str:
        logger.info(f"Retrieving summary for conversation: {conversation_id}")
        result = await self.conversation_service.get_conversation_summary(conversation_id)
        return result['summary']

    @trace_and_measure("clear_conversation")
    async def clear_conversation(self, conversation_id: str) -> dict:
        logger.info(f"Clearing conversation: {conversation_id}")
        result = await self.conversation_service.clear_conversation(conversation_id)
        return {"message": result['message']}