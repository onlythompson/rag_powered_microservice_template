from typing import Dict, Any
from langchain.prompts import PromptTemplate
from src.core.observability import logger

class PromptManager:
    def __init__(self):
        self.prompts: Dict[str, PromptTemplate] = {}

    def add_prompt(self, name: str, prompt: PromptTemplate):
        if name in self.prompts:
            logger.warning(f"Overwriting existing prompt: {name}")
        self.prompts[name] = prompt
        logger.info(f"Added prompt: {name}")

    def get_prompt(self, name: str) -> PromptTemplate:
        if name not in self.prompts:
            raise KeyError(f"Prompt not found: {name}")
        return self.prompts[name]

    def remove_prompt(self, name: str):
        if name in self.prompts:
            del self.prompts[name]
            logger.info(f"Removed prompt: {name}")
        else:
            logger.warning(f"Attempt to remove non-existent prompt: {name}")

    def list_prompts(self) -> Dict[str, str]:
        return {name: str(prompt) for name, prompt in self.prompts.items()}

    def format_prompt(self, name: str, **kwargs: Any) -> str:
        prompt = self.get_prompt(name)
        return prompt.format(**kwargs)