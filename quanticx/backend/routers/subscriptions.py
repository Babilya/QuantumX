from __future__ import annotations

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_session
from backend.models.db_models import Subscription
from backend.security import get_current_user

router = APIRouter()


class SubscribeBody(BaseModel):
    tier: str  # basic | pro | vip
    months: int = 1


@router.post("/subscribe")
async def subscribe(body: SubscribeBody, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    if body.tier not in {"basic", "pro", "vip"}:
        raise HTTPException(status_code=400, detail="Invalid tier")
    result = await session.execute(select(Subscription).where(Subscription.user_id == user.user_id))
    sub = result.scalar_one_or_none()
    now = datetime.utcnow()
    expires = now + timedelta(days=30 * max(1, body.months))
    if sub is None:
        sub = Subscription(user_id=user.user_id, tier=body.tier, expires_at=expires)
        session.add(sub)
    else:
        sub.tier = body.tier
        sub.expires_at = expires
    await session.commit()
    return {"ok": True, "expires_at": sub.expires_at.isoformat()}

