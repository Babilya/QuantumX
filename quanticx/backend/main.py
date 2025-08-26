from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.ai import router as ai_router
from backend.routers.payments import router as payments_router
from backend.routers.currency import router as currency_router
from backend.routers.auth import router as auth_router

app = FastAPI(title="QuanticX API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
