from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.auth import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    user_id: str
    role: str = "user"

@router.post("/login")
async def login(req: LoginRequest):
    if not req.user_id:
        raise HTTPException(status_code=400, detail="user_id required")
    token = create_access_token(subject=req.user_id, role=req.role)
    return {"access_token": token, "token_type": "bearer"}

