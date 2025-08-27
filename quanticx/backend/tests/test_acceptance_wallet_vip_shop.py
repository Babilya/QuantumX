from fastapi.testclient import TestClient
from backend.main import app
from backend.services.auth import create_access_token


def auth_headers(user_id: str = "u1", role: str = "vip"):
    return {"Authorization": f"Bearer {create_access_token(user_id, role)}"}


def test_topup_vip_checkout():
    client = TestClient(app)
    # Topup Shadow Talks
    r = client.post("/wallet/topup?currency=shadow_talks&amount=100", headers=auth_headers())
    assert r.status_code == 200

    # Purchase VIP
    r = client.post("/vip/purchase?months=1", headers=auth_headers())
    assert r.status_code == 200
    assert "expires_at" in r.json()

    # Add to cart and checkout
    r = client.post("/shop/cart", json={"sku": "EMOJI_1", "qty": 2}, headers=auth_headers())
    assert r.status_code == 200
    r = client.post("/shop/checkout", headers=auth_headers())
    assert r.status_code == 200
    assert "total_paid" in r.json()

