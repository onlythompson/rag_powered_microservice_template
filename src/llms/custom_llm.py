from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import requests

class CustomLLM(LLM):
    base_url: str
    api_key: str

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt,
            "stop": stop or []
        }
        response = requests.post(f"{self.base_url}/generate", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["generated_text"]

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"base_url": self.base_url}