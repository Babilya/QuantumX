from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.ai import ai_query

router = APIRouter()


class RouteBody(BaseModel):
    prompt: str
    provider: str = 'gemini'  # gemini | grok


@router.post('/route')
async def route(body: RouteBody):
    try:
        data = await ai_query(body.prompt, model=body.provider)
        return { 'data': data }
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

