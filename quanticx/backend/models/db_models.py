from __future__ import annotations

from datetime import datetime
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, default="user")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    wallets: Mapped[list["Wallet"]] = relationship(back_populates="user")

class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    currency: Mapped[str] = mapped_column(String)  # shadow_talks | casino_coins
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    bonus_locked_until: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship(back_populates="wallets")

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String)
    currency: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    type: Mapped[str] = mapped_column(String)  # deposit | withdraw | bonus | purchase | win | loss
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Escrow(Base):
    __tablename__ = 'escrow'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    buyer_id: Mapped[str] = mapped_column(String)
    seller_id: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String, default='created')  # created | released | disputed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class GroupSettings(Base):
    __tablename__ = "group_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_id: Mapped[str] = mapped_column(String, unique=True)
    welcome_text: Mapped[str] = mapped_column(String, default="Вітаємо!")
    caps_filter: Mapped[int] = mapped_column(Integer, default=1)  # 1 enabled, 0 disabled
    premium_enabled: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Affiliate(Base):
    __tablename__ = "affiliates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String)
    code: Mapped[str] = mapped_column(String, unique=True)
    percent: Mapped[float] = mapped_column(Float, default=0.30)
    referred_count: Mapped[int] = mapped_column(Integer, default=0)
    revenue: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String)
    tier: Mapped[str] = mapped_column(String)  # basic | pro | vip
    expires_at: Mapped[datetime] = mapped_column(DateTime)


class LeaderboardEntry(Base):
    __tablename__ = "leaderboard"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    metric: Mapped[str] = mapped_column(String)  # games_played, wins, points
    user_id: Mapped[str] = mapped_column(String)
    value: Mapped[float] = mapped_column(Float, default=0.0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Poll(Base):
    __tablename__ = "polls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(String)
    created_by: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PollVote(Base):
    __tablename__ = "poll_votes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    poll_id: Mapped[int] = mapped_column(Integer, ForeignKey("polls.id"))
    user_id: Mapped[str] = mapped_column(String)
    option: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
