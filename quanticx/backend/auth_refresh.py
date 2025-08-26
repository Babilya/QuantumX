from __future__ import annotations

import os
import time
import uuid
import jwt
import redis

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def mint_tokens(user_id: str, role: str = "user") -> dict:
    now = int(time.time())
    access = jwt.encode({"sub": user_id, "role": role, "iat": now, "exp": now + 3600}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    refresh_id = str(uuid.uuid4())
    r.setex(f"refresh:{refresh_id}", 60 * 60 * 24 * 30, user_id)  # 30 days
    return {"access": access, "refresh": refresh_id}


def rotate_refresh(refresh_id: str) -> dict:
    user_id = r.get(f"refresh:{refresh_id}")
    if not user_id:
        raise ValueError("invalid refresh")
    r.delete(f"refresh:{refresh_id}")
    return mint_tokens(user_id)

