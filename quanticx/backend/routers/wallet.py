from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_session
from backend.models.db_models import Wallet
from backend.security import get_current_user
from backend.services.economy import apply_deposit, apply_withdraw

router = APIRouter()


@router.get('')
async def get_wallets(session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    rows = (await session.execute(select(Wallet).where(Wallet.user_id == user.user_id))).scalars().all()
    return [ { 'currency': r.currency, 'balance': r.balance } for r in rows ]


@router.post('/topup')
async def topup(currency: str, amount: float, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    await apply_deposit(session, user.user_id, currency, amount)
    await session.commit()
    return { 'ok': True }


@router.post('/withdraw')
async def withdraw(currency: str, amount: float, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    await apply_withdraw(session, user.user_id, currency, amount)
    await session.commit()
    return { 'ok': True }

