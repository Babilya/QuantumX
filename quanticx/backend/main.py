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
from backend.routers.groups import router as groups_router
from backend.routers.subscriptions import router as subs_router
from backend.routers.affiliate import router as affiliate_router
from backend.routers.leaderboards import router as leaderboards_router
from backend.routers.polls import router as polls_router
from backend.middleware import setup_rate_limiter
from backend.db import engine
from backend.models.db_models import Base
from backend.observability import setup_logging, setup_sentry, metrics_middleware, metrics_response
from backend.tracing import setup_tracing
from backend.routers.osint_export import router as osint_export_router
from backend.routers.flags import router as flags_router
from backend.routers.fraud import router as fraud_router
from backend.routers.referral import router as referral_router
from backend.routers.wallet import router as wallet_router
from backend.routers.games import router as games_router
from backend.routers.admin_ops import router as admin_ops_router
from backend.routers.ai_router import router as ai_route_router
from backend.routers.vip import router as vip_router
from backend.routers.shop_cart import router as shop_cart_router
from backend.routers.profile import router as profile_router
from backend.routers.escrow import router as escrow_router

setup_logging()
setup_sentry()
app = FastAPI(title="QuanticX API", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_rate_limiter(app)
app.middleware('http')(metrics_middleware)
setup_tracing(app)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get('/metrics')
async def metrics():
    return metrics_response()

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
app.include_router(groups_router, prefix="/groups", tags=["groups"])
app.include_router(subs_router, prefix="/subscriptions", tags=["subscriptions"])
app.include_router(affiliate_router, prefix="/affiliate", tags=["affiliate"])
app.include_router(leaderboards_router, prefix="/leaderboards", tags=["leaderboards"])
app.include_router(polls_router, prefix="/polls", tags=["polls"])
app.include_router(referral_router, prefix="/referral", tags=["referral"])
app.include_router(wallet_router, prefix="/wallet", tags=["wallet"])
app.include_router(games_router, prefix="/games", tags=["games"])
app.include_router(admin_ops_router, prefix="/api/admin", tags=["admin"])
app.include_router(ai_route_router, prefix="/ai", tags=["ai"])
app.include_router(vip_router, prefix="/vip", tags=["vip"])
app.include_router(shop_cart_router, prefix="/shop", tags=["shop"])
app.include_router(profile_router, prefix="/profile", tags=["profile"])
app.include_router(escrow_router, prefix="/escrow", tags=["escrow"])
app.include_router(osint_export_router, prefix="/osint/export", tags=["osint"]) 
app.include_router(flags_router, prefix="/flags", tags=["flags"]) 
app.include_router(fraud_router, prefix="/fraud", tags=["fraud"]) 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
