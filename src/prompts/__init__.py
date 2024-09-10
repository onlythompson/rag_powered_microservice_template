from .custom_prompts import (
    get_qa_prompt,
    get_summarization_prompt,
    get_entity_extraction_prompt,
    get_fact_checking_prompt
)
from .prompt_manager import PromptManager






# Example usage in src/services/query_service.py

from src.prompts import PromptManager, get_qa_prompt

class QueryService:
    def __init__(self):
        self.prompt_manager = PromptManager()
        self.prompt_manager.add_prompt("qa", get_qa_prompt())

    async def process_query(self, query: str, context: str):
        prompt = self.prompt_manager.format_prompt("qa", question=query, context=context)
        # Use the formatted prompt with your LLM here
        # ...

