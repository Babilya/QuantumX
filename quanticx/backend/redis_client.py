from __future__ import annotations

import os
from typing import Any, Dict, List

try:
    import redis  # type: ignore
except Exception:  # pragma: no cover
    redis = None  # type: ignore


class _Memory:
    def __init__(self) -> None:
        self._kv: Dict[str, Any] = {}
        self._hash: Dict[str, Dict[str, str]] = {}
        self._lists: Dict[str, List[str]] = {}

    def set(self, key: str, value: Any) -> None:
        self._kv[key] = value

    def get(self, key: str) -> Any:
        return self._kv.get(key)

    def hset(self, name: str, key: str, value: str) -> None:
        self._hash.setdefault(name, {})[key] = value

    def hgetall(self, name: str) -> Dict[str, str]:
        return dict(self._hash.get(name, {}))

    def delete(self, key: str) -> None:
        self._kv.pop(key, None)
        self._hash.pop(key, None)
        self._lists.pop(key, None)

    def lpush(self, key: str, value: str) -> None:
        self._lists.setdefault(key, []).insert(0, value)

    def lrange(self, key: str, start: int, end: int) -> List[str]:
        lst = self._lists.get(key, [])
        if end == -1:
            end = len(lst)
        return lst[start:end]


_mem = _Memory()


def get_redis():
    url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    if redis is None:
        return _mem
    try:
        r = redis.Redis.from_url(url, decode_responses=True)
        r.ping()
        return r
    except Exception:
        return _mem

