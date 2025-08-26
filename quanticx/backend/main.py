from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.ai import router as ai_router
from backend.routers.payments import router as payments_router
from backend.routers.currency import router as currency_router
from backend.routers.auth import router as auth_router
from backend.routers.economy import router as economy_router
from backend.routers.osint import router as osint_router
from backend.routers.shop import router as shop_router
from backend.routers.casino import router as casino_router
from backend.routers.guarantor import router as guarantor_router
from backend.routers.analytics import router as analytics_router
from backend.routers.chat import router as chat_router
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
app.include_router(economy_router, prefix="/economy", tags=["economy"]) 
app.include_router(osint_router, prefix="/osint", tags=["osint"]) 
app.include_router(shop_router, prefix="/shop", tags=["shop"]) 
app.include_router(casino_router, prefix="/casino", tags=["casino"]) 
app.include_router(guarantor_router, prefix="/guarantor", tags=["guarantor"]) 
app.include_router(analytics_router, prefix="/analytics", tags=["analytics"]) 
app.include_router(chat_router, prefix="", tags=["ws"]) 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
