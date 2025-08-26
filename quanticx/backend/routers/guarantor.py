from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.db import get_session
from backend.security import require_roles
from backend.services.economy import spend, SHADOW_TALKS

router = APIRouter()


class ContractBody(BaseModel):
    counterparty: str
    amount: float
    terms: str


@router.post("/create")
async def create_contract(
    body: ContractBody,
    session: AsyncSession = Depends(get_session),
    user=Depends(require_roles("user", "vip", "admin")),
):
    if body.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")
    await spend(session, user.user_id, SHADOW_TALKS, 1.0, "escrow_fee")
    await session.commit()
    return {"status": "created"}

