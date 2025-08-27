from fastapi.testclient import TestClient
from backend.main import app
from backend.services.auth import create_access_token

def auth_admin():
    return { 'Authorization': f'Bearer {create_access_token("admin_user","admin")}' }

def auth_user():
    return { 'Authorization': f'Bearer {create_access_token("buyer","user")}' }

def test_escrow_flow():
    client = TestClient(app)
    r = client.post('/escrow/create', json={'seller_id':'seller','amount':50}, headers=auth_user())
    assert r.status_code == 200
    escrow_id = r.json()['id']
    r = client.post('/escrow/dispute', json={'id':escrow_id}, headers=auth_user())
    assert r.status_code == 200
    r = client.post('/escrow/release', json={'id':escrow_id}, headers=auth_admin())
    assert r.status_code == 200
