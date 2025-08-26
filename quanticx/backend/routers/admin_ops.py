from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from backend.security import require_roles

router = APIRouter()


@router.post('/security/lockdown')
async def lockdown(user=Depends(require_roles('admin'))):
    return { 'status': 'lockdown_armed' }


@router.post('/emergency-shutdown')
async def emergency_shutdown(user=Depends(require_roles('admin'))):
    # In real deployment send signal to orchestrator
    return { 'status': 'shutdown_signal_sent' }

