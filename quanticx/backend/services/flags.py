from __future__ import annotations

from typing import Dict
from backend.redis_client import get_redis


def set_flag(name: str, value: str) -> None:
    r = get_redis()
    r.hset('feature_flags', name, value)


def get_flags() -> Dict[str, str]:
    r = get_redis()
    return r.hgetall('feature_flags')
