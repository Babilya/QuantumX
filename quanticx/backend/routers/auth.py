from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.auth import create_access_token
from backend.auth_refresh import mint_tokens, rotate_refresh

router = APIRouter()

class LoginRequest(BaseModel):
    user_id: str
    role: str = "user"

@router.post("/login")
async def login(req: LoginRequest):
    if not req.user_id:
        raise HTTPException(status_code=400, detail="user_id required")
    tokens = mint_tokens(user_id=req.user_id, role=req.role)
    return {"access_token": tokens["access"], "refresh_token": tokens["refresh"], "token_type": "bearer"}


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh")
async def refresh(req: RefreshRequest):
    try:
        tokens = rotate_refresh(req.refresh_token)
        return {"access_token": tokens["access"], "refresh_token": tokens["refresh"], "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

