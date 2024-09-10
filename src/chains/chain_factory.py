from src.core.observability import logger
from .rag_chain import RAGChain
from .summarization_chain import SummarizationChain
from .question_answering_chain import QuestionAnsweringChain

class ChainFactory:
    @staticmethod
    def get_chain(chain_type: str):
        logger.info(f"Creating chain of type: {chain_type}")
        if chain_type == "rag":
            return RAGChain()
        elif chain_type == "summarization":
            return SummarizationChain()
        elif chain_type == "qa":
            return QuestionAnsweringChain()
        else:
            raise ValueError(f"Unsupported chain type: {chain_type}")