from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_session
from backend.models.db_models import LeaderboardEntry

router = APIRouter()


@router.get("/{metric}")
async def leaderboard(metric: str, session: AsyncSession = Depends(get_session)):
    q = select(LeaderboardEntry).where(LeaderboardEntry.metric == metric).order_by(desc(LeaderboardEntry.value)).limit(100)
    rows = (await session.execute(q)).scalars().all()
    return [
        {"user_id": r.user_id, "value": r.value}
        for r in rows
    ]

