from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.db import get_session
from backend.models.db_models import Subscription
from backend.security import get_current_user

router = APIRouter()


@router.get('')
async def profile(session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    sub = (await session.execute(select(Subscription).where(Subscription.user_id == user.user_id))).scalar_one_or_none()
    return { 'user_id': user.user_id, 'role': user.role, 'vip_expires_at': (sub.expires_at.isoformat() if sub else None) }
