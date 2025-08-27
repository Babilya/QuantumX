from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.db import get_session
from backend.models.db_models import Transaction
from backend.security import require_roles

router = APIRouter()


@router.post('/security/lockdown')
async def lockdown(user=Depends(require_roles('admin'))):
    return { 'status': 'lockdown_armed' }


@router.post('/emergency-shutdown')
async def emergency_shutdown(user=Depends(require_roles('admin'))):
    # In real deployment send signal to orchestrator
    return { 'status': 'shutdown_signal_sent' }


@router.get('/stats')
async def stats(session: AsyncSession = Depends(get_session), user=Depends(require_roles('analyst','admin'))):
    total_rev = (await session.execute(select(func.coalesce(func.sum(Transaction.amount), 0.0)))).scalar_one()
    tx_count = (await session.execute(select(func.count(Transaction.id)))).scalar_one()
    return { 'total_revenue': float(total_rev), 'transactions': int(tx_count) }

