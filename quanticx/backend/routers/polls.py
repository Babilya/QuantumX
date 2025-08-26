from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_session
from backend.models.db_models import Poll, PollVote
from backend.security import get_current_user

router = APIRouter()


class CreatePollBody(BaseModel):
    question: str


@router.post("/create")
async def create_poll(body: CreatePollBody, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    p = Poll(question=body.question, created_by=user.user_id)
    session.add(p)
    await session.commit()
    return {"id": p.id}


class VoteBody(BaseModel):
    poll_id: int
    option: str


@router.post("/vote")
async def vote(body: VoteBody, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    v = PollVote(poll_id=body.poll_id, user_id=user.user_id, option=body.option)
    session.add(v)
    await session.commit()
    return {"ok": True}

