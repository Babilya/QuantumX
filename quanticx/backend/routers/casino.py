from __future__ import annotations

import random
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_session
from backend.security import get_current_user, require_roles
from backend.services.economy import spend, win, CASINO_COINS

router = APIRouter()


class SpinBody(BaseModel):
    bet: float


@router.post("/spin")
async def spin(
    body: SpinBody,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_roles("vip_gambler", "admin")),
):
    if body.bet <= 0:
        raise HTTPException(status_code=400, detail="Invalid bet")
    await spend(session, user.user_id, CASINO_COINS, body.bet, "loss")
    # 45% chance to win 2x
    if random.random() < 0.45:
        await win(session, user.user_id, body.bet * 2)
        outcome = "win"
    else:
        outcome = "loss"
    await session.commit()
    return {"outcome": outcome}

