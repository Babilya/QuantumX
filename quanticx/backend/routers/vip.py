from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

from backend.db import get_session
from backend.models.db_models import Subscription
from backend.security import get_current_user

router = APIRouter()


@router.post('/purchase')
async def purchase_vip(months: int = 1, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    result = await session.execute(select(Subscription).where(Subscription.user_id == user.user_id))
    sub = result.scalar_one_or_none()
    expires = datetime.utcnow() + timedelta(days=30 * max(1, months))
    if sub is None:
        sub = Subscription(user_id=user.user_id, tier='vip', expires_at=expires)
        session.add(sub)
    else:
        sub.tier = 'vip'
        sub.expires_at = expires
    await session.commit()
    return { 'ok': True, 'expires_at': sub.expires_at.isoformat() }
