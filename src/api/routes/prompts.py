from fastapi import APIRouter, HTTPException
from src.prompts import PromptManager
from pydantic import BaseModel

router = APIRouter()
prompt_manager = PromptManager()

class PromptCreate(BaseModel):
    name: str
    template: str

@router.post("/prompts")
async def create_prompt(prompt: PromptCreate):
    try:
        new_prompt = PromptTemplate(template=prompt.template, input_variables=extract_variables(prompt.template))
        prompt_manager.add_prompt(prompt.name, new_prompt)
        return {"message": f"Prompt '{prompt.name}' created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/prompts")
async def list_prompts():
    return prompt_manager.list_prompts()

@router.delete("/prompts/{name}")
async def delete_prompt(name: str):
    try:
        prompt_manager.remove_prompt(name)
        return {"message": f"Prompt '{name}' deleted successfully"}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Prompt '{name}' not found")