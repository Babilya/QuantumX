from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.redis_client import get_redis
from backend.security import get_current_user

router = APIRouter()


@router.get('/list')
async def list_games():
    return [
        { 'key': 'slots', 'name': 'Slots' },
        { 'key': 'roulette', 'name': 'Roulette' },
        { 'key': 'quiz', 'name': 'Quiz' },
    ]


class PlayBody(BaseModel):
    game: str
    result: str


@router.post('/play')
async def play(body: PlayBody, user=Depends(get_current_user)):
    r = get_redis()
    r.lpush(f"games:{user.user_id}", f"{body.game}:{body.result}")
    return { 'ok': True }


@router.get('/history')
async def history(user=Depends(get_current_user)):
    r = get_redis()
    return { 'entries': r.lrange(f"games:{user.user_id}", 0, -1) }

