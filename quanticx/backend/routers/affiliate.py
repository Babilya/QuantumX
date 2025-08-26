from __future__ import annotations

import random
import string
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_session
from backend.models.db_models import Affiliate
from backend.security import get_current_user

router = APIRouter()


def _gen_code() -> str:
    return "AFF" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


@router.post("/create")
async def create_affiliate(session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    result = await session.execute(select(Affiliate).where(Affiliate.user_id == user.user_id))
    aff = result.scalar_one_or_none()
    if aff is None:
        aff = Affiliate(user_id=user.user_id, code=_gen_code())
        session.add(aff)
        await session.commit()
    return {"code": aff.code, "percent": aff.percent}

