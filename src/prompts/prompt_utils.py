from typing import List
import re

def extract_variables(template: str) -> List[str]:
    """Extract variables from a prompt template."""
    return re.findall(r'\{(\w+)\}', template)

def validate_prompt(template: str, variables: List[str]) -> bool:
    """Validate that a prompt template contains all required variables."""
    extracted_vars = extract_variables(template)
    return all(var in extracted_vars for var in variables)