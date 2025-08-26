from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_session
from backend.security import require_roles
from backend.models.db_models import Transaction

router = APIRouter()


@router.get("/kpis")
async def kpis(session: AsyncSession = Depends(get_session), user=Depends(require_roles("analyst", "admin"))):
    total_revenue_q = select(func.coalesce(func.sum(Transaction.amount), 0.0)).where(Transaction.type.in_(["deposit", "purchase"]))
    total_revenue = (await session.execute(total_revenue_q)).scalar_one()
    deposits_q = select(func.count()).where(Transaction.type == "deposit")
    deposits = (await session.execute(deposits_q)).scalar_one()
    return {"total_revenue": float(total_revenue), "deposits": int(deposits)}

