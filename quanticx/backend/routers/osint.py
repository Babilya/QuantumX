from __future__ import annotations

import os
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import aiohttp

from backend.security import require_roles
from backend.redis_client import get_redis
from backend.services.ai import ai_query

router = APIRouter()


class SearchBody(BaseModel):
    query: str


@router.post("/search")
async def osint_search(body: SearchBody, user=Depends(require_roles("analyst", "admin"))):
    google_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CSE_ID")
    if not google_key or not cx:
        raise HTTPException(status_code=500, detail="Google CSE not configured")
    url = f"https://www.googleapis.com/customsearch/v1?q={body.query}&key={google_key}&cx={cx}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
    summary = await ai_query(f"Підсумуй публічні дані: {data}")
    r = get_redis()
    key = f"osint:{body.query}"
    r.hset(key, "results", str(data))
    r.hset(key, "summary", str(summary))
    return {"results": data, "summary": summary, "key": key}

