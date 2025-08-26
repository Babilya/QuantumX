from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

RoleName = Literal[
    "user","vip","moderator","support","analyst","admin","affiliate","enterprise","tester","vip_gambler","crypto_user"
]

class User(BaseModel):
    id: str
    username: Optional[str] = None
    role: RoleName = "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Transaction(BaseModel):
    id: str
    user_id: str
    currency: Literal["shadow_talks","casino_coins"]
    amount: float
    type: Literal["deposit","withdraw","bonus","purchase","win","loss"]
    created_at: datetime = Field(default_factory=datetime.utcnow)

