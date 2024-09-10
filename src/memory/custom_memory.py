# src/memory/custom_memory.py

from typing import List, Tuple
from langchain.memory import ConversationBufferMemory as LangChainBufferMemory
from langchain.memory import ConversationSummaryMemory as LangChainSummaryMemory
from langchain.memory import ConversationKGMemory as LangChainKGMemory
from langchain.llms import BaseLLM
from src.core.observability import logger, trace_and_measure

class ConversationBufferMemory(LangChainBufferMemory):
    @trace_and_measure("memory_add")
    def add_user_message(self, message: str) -> None:
        super().add_user_message(message)
        logger.info(f"Added user message to buffer memory: {message[:50]}...")

    @trace_and_measure("memory_add")
    def add_ai_message(self, message: str) -> None:
        super().add_ai_message(message)
        logger.info(f"Added AI message to buffer memory: {message[:50]}...")

class ConversationSummaryMemory(LangChainSummaryMemory):
    @trace_and_measure("memory_add")
    def add_message(self, message: str) -> None:
        super().add_message(message)
        logger.info(f"Added message to summary memory: {message[:50]}...")

    @trace_and_measure("memory_summarize")
    def predict_new_summary(
        self, messages: List[str], existing_summary: str
    ) -> str:
        summary = super().predict_new_summary(messages, existing_summary)
        logger.info(f"Generated new summary: {summary[:50]}...")
        return summary

class ConversationKGMemory(LangChainKGMemory):
    @trace_and_measure("memory_add")
    def add_message(self, message: str) -> None:
        super().add_message(message)
        logger.info(f"Added message to KG memory: {message[:50]}...")

    @trace_and_measure("memory_kg_extract")
    def _extract_triplets(self, text: str) -> List[Tuple[str, str, str]]:
        triplets = super()._extract_triplets(text)
        logger.info(f"Extracted {len(triplets)} triplets from text")
        return triplets