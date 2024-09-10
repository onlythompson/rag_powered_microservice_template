from src.core.observability import logger
from .rag_agent import RAGAgent
from .conversation_agent import ConversationAgent
from .multi_tool_agent import MultiToolAgent

class AgentFactory:
    @staticmethod
    def get_agent(agent_type: str):
        logger.info(f"Creating agent of type: {agent_type}")
        if agent_type == "rag":
            return RAGAgent()
        elif agent_type == "conversation":
            return ConversationAgent()
        elif agent_type == "multi_tool":
            return MultiToolAgent()
        else:
            raise ValueError(f"Unsupported agent type: {agent_type}")