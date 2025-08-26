from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_session
from backend.models.db_models import GroupSettings
from backend.security import require_roles

router = APIRouter()


class GroupSettingsBody(BaseModel):
    group_id: str
    welcome_text: str | None = None
    caps_filter: int | None = None
    premium_enabled: int | None = None


@router.post("/set")
async def set_group_settings(
    body: GroupSettingsBody, session: AsyncSession = Depends(get_session), user=Depends(require_roles("moderator", "admin"))
):
    result = await session.execute(select(GroupSettings).where(GroupSettings.group_id == body.group_id))
    gs = result.scalar_one_or_none()
    if gs is None:
        gs = GroupSettings(group_id=body.group_id)
        session.add(gs)
    if body.welcome_text is not None:
        gs.welcome_text = body.welcome_text
    if body.caps_filter is not None:
        gs.caps_filter = body.caps_filter
    if body.premium_enabled is not None:
        gs.premium_enabled = body.premium_enabled
    await session.commit()
    return {"ok": True}


@router.get("/{group_id}")
async def get_group_settings(group_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(GroupSettings).where(GroupSettings.group_id == group_id))
    gs = result.scalar_one_or_none()
    if gs is None:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "group_id": gs.group_id,
        "welcome_text": gs.welcome_text,
        "caps_filter": gs.caps_filter,
        "premium_enabled": gs.premium_enabled,
    }

