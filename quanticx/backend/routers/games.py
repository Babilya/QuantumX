from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get('/list')
async def list_games():
    return [
        { 'key': 'slots', 'name': 'Slots' },
        { 'key': 'roulette', 'name': 'Roulette' },
        { 'key': 'quiz', 'name': 'Quiz' },
    ]

