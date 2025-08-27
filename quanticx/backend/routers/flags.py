from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.security import require_roles
from backend.services.flags import set_flag, get_flags

router = APIRouter()


class FlagBody(BaseModel):
    name: str
    value: str


@router.post('')
async def set_feature_flag(body: FlagBody, user=Depends(require_roles('admin'))):
    set_flag(body.name, body.value)
    return { 'ok': True }


@router.get('')
async def list_flags(user=Depends(require_roles('admin'))):
    return get_flags()
