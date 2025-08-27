from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.security import require_roles
from backend.services.fraud import score_transaction

router = APIRouter()


class TxFeatures(BaseModel):
    amount: float
    country: str = 'UA'


@router.post('/score')
async def score(body: TxFeatures, user=Depends(require_roles('analyst','admin'))):
    return { 'score': score_transaction(body.model_dump()) }
