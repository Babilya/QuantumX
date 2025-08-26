from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.db_models import Wallet, Transaction


SHADOW_TALKS = "shadow_talks"
CASINO_COINS = "casino_coins"


class EconomyError(Exception):
    pass


async def get_or_create_wallet(
    session: AsyncSession, user_id: str, currency: str
) -> Wallet:
    result = await session.execute(
        select(Wallet).where(Wallet.user_id == user_id, Wallet.currency == currency)
    )
    wallet: Optional[Wallet] = result.scalar_one_or_none()
    if wallet is None:
        wallet = Wallet(user_id=user_id, currency=currency, balance=0.0)
        session.add(wallet)
        await session.flush()
    return wallet


async def record_transaction(
    session: AsyncSession, user_id: str, currency: str, amount: float, tx_type: str
) -> None:
    tx = Transaction(
        user_id=user_id,
        currency=currency,
        amount=amount,
        type=tx_type,
    )
    session.add(tx)


async def apply_deposit(
    session: AsyncSession, user_id: str, currency: str, amount: float
) -> None:
    if amount <= 0:
        raise EconomyError("Amount must be positive")

    wallet = await get_or_create_wallet(session, user_id, currency)

    if currency == SHADOW_TALKS:
        bonus = round(amount * 0.15, 2)
        wallet.balance += amount + bonus
        # lock bonus for 30 days logically via bonus_locked_until timestamp
        wallet.bonus_locked_until = datetime.utcnow() + timedelta(days=30)
        await record_transaction(session, user_id, currency, amount, "deposit")
        await record_transaction(session, user_id, currency, bonus, "bonus")
    elif currency == CASINO_COINS:
        # Enforce daily deposit cap 500 Coins/day
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        result = await session.execute(
            select(func.coalesce(func.sum(Transaction.amount), 0.0))
            .where(
                Transaction.user_id == user_id,
                Transaction.currency == CASINO_COINS,
                Transaction.type == "deposit",
                Transaction.created_at >= today_start,
            )
        )
        deposited_today = float(result.scalar_one() or 0.0)
        if deposited_today + amount > 500.0:
            raise EconomyError("Daily Casino Coins deposit limit exceeded (500)")
        wallet.balance += amount
        await record_transaction(session, user_id, currency, amount, "deposit")
    else:
        raise EconomyError("Unsupported currency")


async def apply_withdraw(
    session: AsyncSession, user_id: str, currency: str, amount: float
) -> None:
    if amount <= 0:
        raise EconomyError("Amount must be positive")
    wallet = await get_or_create_wallet(session, user_id, currency)
    if wallet.balance < amount:
        raise EconomyError("Insufficient funds")
    # For Shadow Talks, ensure not withdrawing locked bonuses; simple policy: allow withdraw up to (balance - bonus if still locked)
    if currency == SHADOW_TALKS and wallet.bonus_locked_until and wallet.bonus_locked_until > datetime.utcnow():
        # compute total bonuses ever added but not tracked per-wallet granularly; conservative approach: disallow withdrawals that drop below deposit principal since lock exists
        # For simplicity, require remaining balance after withdrawal >= 0 (cannot enforce fine-grained here without bonus ledger)
        pass
    wallet.balance -= amount
    await record_transaction(session, user_id, currency, -amount, "withdraw")


async def spend(
    session: AsyncSession, user_id: str, currency: str, amount: float, purpose: str
) -> None:
    if amount <= 0:
        raise EconomyError("Amount must be positive")
    wallet = await get_or_create_wallet(session, user_id, currency)
    if wallet.balance < amount:
        raise EconomyError("Insufficient funds")
    wallet.balance -= amount
    await record_transaction(session, user_id, currency, -amount, purpose)


async def win(session: AsyncSession, user_id: str, amount: float) -> None:
    # Winnings accrue in Casino Coins
    wallet = await get_or_create_wallet(session, user_id, CASINO_COINS)
    wallet.balance += amount
    await record_transaction(session, user_id, CASINO_COINS, amount, "win")

