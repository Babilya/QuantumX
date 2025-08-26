from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from backend.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from backend.security import get_current_user
from backend.services.economy import apply_deposit, apply_withdraw, EconomyError


router = APIRouter()


class DepositBody(BaseModel):
    currency: str
    amount: float


class WithdrawBody(BaseModel):
    currency: str
    amount: float


@router.post("/deposit")
async def deposit(
    body: DepositBody,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    try:
        await apply_deposit(session, user.user_id, body.currency, body.amount)
        await session.commit()
        return {"ok": True}
    except EconomyError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/withdraw")
async def withdraw(
    body: WithdrawBody,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    try:
        await apply_withdraw(session, user.user_id, body.currency, body.amount)
        await session.commit()
        return {"ok": True}
    except EconomyError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

