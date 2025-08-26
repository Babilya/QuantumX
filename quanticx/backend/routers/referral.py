from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_session
from backend.models.db_models import Affiliate
from backend.security import get_current_user

router = APIRouter()


@router.get('/link')
async def link(session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    row = (await session.execute(select(Affiliate).where(Affiliate.user_id == user.user_id))).scalar_one_or_none()
    code = row.code if row else 'AFFXXXXXX'
    return { 'link': f'https://t.me/your_bot?start={code}' }


@router.get('/stats')
async def stats(session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    row = (await session.execute(select(Affiliate).where(Affiliate.user_id == user.user_id))).scalar_one_or_none()
    if not row:
        return { 'referred': 0, 'revenue': 0.0 }
    return { 'referred': row.referred_count, 'revenue': row.revenue }

