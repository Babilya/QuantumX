from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.ai import ai_query

router = APIRouter()

class AIQueryRequest(BaseModel):
    prompt: str
    model: str | None = "gemini"

@router.post("/query")
async def query_ai(req: AIQueryRequest):
    try:
        data = await ai_query(prompt=req.prompt, model=req.model or "gemini")
        return {"ok": True, "data": data}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
