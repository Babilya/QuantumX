from fastapi.testclient import TestClient
from backend.main import app

def test_convert_forbidden():
    client = TestClient(app)
    r = client.post("/currency/convert", json={"from_curr":"shadow_talks","to_curr":"casino_coins","amount":100})
    assert r.status_code == 403
