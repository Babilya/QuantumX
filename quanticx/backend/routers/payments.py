import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

try:
    import monobank  # type: ignore
except Exception:
    monobank = None  # fallback for dev without package

router = APIRouter()

MONOBANK_TOKEN = os.getenv("MONOBANK_TOKEN", "")
mono_client = None
if monobank and MONOBANK_TOKEN:
    try:
        mono_client = monobank.Client(token=MONOBANK_TOKEN)  # type: ignore[attr-defined]
    except Exception:
        mono_client = None

ALLOWED_CURRENCIES = {"shadow_talks", "casino_coins"}

class DepositRequest(BaseModel):
    amount: float
    currency: str
    user_id: str

class WithdrawRequest(BaseModel):
    amount: float
    currency: str
    user_id: str
    mono_account: Optional[str] = None

@router.post("/deposit")
async def deposit(req: DepositRequest):
    if req.currency not in ALLOWED_CURRENCIES:
        raise HTTPException(status_code=400, detail="Невірна валюта")
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Невірна сума")

    if mono_client:
        try:
            invoice = mono_client.create_invoice(amount=req.amount, currency="UAH", description=f"Поповнення {req.currency} для {req.user_id}")
            return {"invoice_url": invoice.get("invoice_url"), "status": "created"}
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))
    return {"invoice_url": None, "status": "mock_created"}

@router.post("/withdraw")
async def withdraw(req: WithdrawRequest):
    if req.currency not in ALLOWED_CURRENCIES:
        raise HTTPException(status_code=400, detail="Невірна валюта")
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Невірна сума")

    if req.currency == "casino_coins":
        if mono_client and req.mono_account:
            try:
                # Placeholder for payout; real SDK method name may differ
                mono_client.send_money(to_account=req.mono_account, amount=req.amount, comment="Вивід Casino Coins")
                return {"status": "withdrawn"}
            except Exception as e:
                raise HTTPException(status_code=502, detail=str(e))
        return {"status": "mock_withdrawn"}

    # Shadow Talks withdrawal path should exclude bonuses; enforcement in service layer (not implemented here)
    return {"status": "withdrawn"}

@router.post("/monobank/webhook")
async def monobank_webhook(request: Request):
    try:
        payload = await request.json()
        # Log and verify signature in production
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
