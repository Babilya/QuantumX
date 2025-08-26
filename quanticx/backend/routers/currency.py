from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.currency import currency_manager

router = APIRouter()

class ConvertRequest(BaseModel):
    from_curr: str
    to_curr: str
    amount: float

@router.post("/convert")
async def convert(req: ConvertRequest):
    try:
        currency_manager.convert(req.from_curr, req.to_curr, req.amount)
        return {"ok": True}
    except HTTPException as e:
        raise e
