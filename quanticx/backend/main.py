from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.ai import router as ai_router
from backend.routers.payments import router as payments_router
from backend.routers.currency import router as currency_router
from backend.routers.auth import router as auth_router
from backend.middleware import setup_rate_limiter
from backend.db import engine
from backend.models.db_models import Base

app = FastAPI(title="QuanticX API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_rate_limiter(app)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(ai_router, prefix="/ai", tags=["ai"]) 
app.include_router(payments_router, prefix="/payments", tags=["payments"]) 
app.include_router(currency_router, prefix="/currency", tags=["currency"]) 
app.include_router(auth_router, prefix="/auth", tags=["auth"]) 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
