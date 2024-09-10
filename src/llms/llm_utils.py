from typing import List
import re

def extract_entities(text: str) -> List[str]:
    """
    A simple function to extract potential named entities from text.
    This is a placeholder and should be replaced with a more robust NER system in production.
    """
    # This regex looks for capitalized words that are not at the start of a sentence
    entities = re.findall(r'(?<!\.|\?|\!)\s([A-Z][a-z]+)', text)
    return list(set(entities))  # Remove duplicates

def summarize_text(text: str, max_length: int = 100) -> str:
    """
    A simple function to summarize text by truncating it.
    This is a placeholder and should be replaced with a more sophisticated summarization method in production.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'