from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.db import get_session
from backend.models.db_models import Escrow
from backend.security import get_current_user, require_roles

router = APIRouter()


class EscrowCreate(BaseModel):
    seller_id: str
    amount: float


@router.post('/create')
async def create(body: EscrowCreate, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    if body.amount <= 0:
        raise HTTPException(status_code=400, detail='invalid amount')
    e = Escrow(buyer_id=user.user_id, seller_id=body.seller_id, amount=body.amount)
    session.add(e)
    await session.commit()
    return { 'id': e.id, 'status': e.status }


class EscrowAction(BaseModel):
    id: int


@router.post('/release')
async def release(body: EscrowAction, session: AsyncSession = Depends(get_session), user=Depends(require_roles('support','admin'))):
    e = (await session.execute(select(Escrow).where(Escrow.id == body.id))).scalar_one_or_none()
    if not e:
        raise HTTPException(status_code=404, detail='not found')
    e.status = 'released'
    await session.commit()
    return { 'status': e.status }


@router.post('/dispute')
async def dispute(body: EscrowAction, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    e = (await session.execute(select(Escrow).where(Escrow.id == body.id))).scalar_one_or_none()
    if not e:
        raise HTTPException(status_code=404, detail='not found')
    e.status = 'disputed'
    await session.commit()
    return { 'status': e.status }
