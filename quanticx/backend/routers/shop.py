from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_session
from backend.models.db_models import Transaction
from backend.security import get_current_user
from backend.services.economy import spend, SHADOW_TALKS

router = APIRouter()


class ShopItem(BaseModel):
    sku: str
    title: str
    price: float
    tags: List[str] = []


CATALOG: list[ShopItem] = (
    [ShopItem(sku=f"EMOJI_{i}", title=f"Emoji Pack {i}", price=1.0 + (i % 5), tags=["emoji", "digital"]) for i in range(1, 251)]
    + [ShopItem(sku=f"SKIN_{i}", title=f"Skin {i}", price=2.0 + (i % 7), tags=["skin", "theme"]) for i in range(1, 150)]
    + [ShopItem(sku=f"REPORT_{i}", title=f"OSINT Report {i}", price=5.0 + (i % 10), tags=["report", "osint"]) for i in range(1, 120)]
)


@router.get("/catalog")
async def catalog() -> list[ShopItem]:
    return CATALOG


class PurchaseBody(BaseModel):
    sku: str


@router.post("/purchase")
async def purchase(
    body: PurchaseBody,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    item = next((x for x in CATALOG if x.sku == body.sku), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await spend(session, user.user_id, SHADOW_TALKS, item.price, "purchase")
    await session.commit()
    return {"ok": True}

