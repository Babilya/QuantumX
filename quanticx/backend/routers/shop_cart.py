from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.redis_client import get_redis
from backend.security import get_current_user
from backend.routers.shop import CATALOG

router = APIRouter()


def cart_key(user_id: str) -> str:
    return f"cart:{user_id}"


class CartItem(BaseModel):
    sku: str
    qty: int


@router.post('/cart')
async def add_to_cart(item: CartItem, user=Depends(get_current_user)):
    r = get_redis()
    r.lpush(cart_key(user.user_id), f"{item.sku}:{item.qty}")
    return { 'ok': True }


@router.post('/checkout')
async def checkout(user=Depends(get_current_user)):
    r = get_redis()
    items = r.lrange(cart_key(user.user_id), 0, -1)
    total = 0.0
    for s in items:
        sku, qty_s = s.split(':', 1)
        qty = int(qty_s)
        item = next((x for x in CATALOG if x.sku == sku), None)
        if item:
            total += item.price * qty
    # VIP discount 10%
    total = round(total * 0.9, 2)
    r.delete(cart_key(user.user_id))
    return { 'total_paid': total }
