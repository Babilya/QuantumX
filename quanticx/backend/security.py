from __future__ import annotations

import os
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, Header
import jwt

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

class CurrentUser:
    def __init__(self, user_id: str, role: str):
        self.user_id = user_id
        self.role = role

def get_current_user(authorization: Annotated[Optional[str], Header()] = None) -> CurrentUser:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    return CurrentUser(user_id=str(payload.get("sub")), role=str(payload.get("role", "user")))

def require_roles(*roles: str):
    def checker(user: Annotated[CurrentUser, Depends(get_current_user)]):
        if roles and user.role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker
