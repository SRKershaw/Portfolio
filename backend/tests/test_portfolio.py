# backend/tests/test_portfolio.py
from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_list_portfolios():
    resp = client.get("/portfolios")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_read_portfolio():
    ids = [p["id"] for p in client.get("/portfolios").json()]
    resp = client.get(f"/portfolios/{ids[0]}")
    assert resp.status_code == 200
    assert "sets" in resp.json()

def test_create_portfolio():
    payload = {"name": "My New Portfolio"}
    resp = client.post("/portfolios", json=payload)
    assert resp.status_code == 201
    new = resp.json()
    assert new["name"] == payload["name"]
    assert len(new["sets"]) == 1
    assert new["sets"][0]["name"] == "All Assets"

def test_create_set():
    portfolio_id = client.get("/portfolios").json()[0]["id"]
    resp = client.post(f"/portfolios/{portfolio_id}/sets", json={"name": "Test Set"})
    assert resp.status_code == 201
    data = resp.json()
    assert any(s["name"] == "Test Set" for s in data["sets"])

def test_create_asset():
    portfolio = client.get("/portfolios").json()[0]
    set_id = next((s["id"] for s in portfolio["sets"] if s["name"] == "Tech Leaders"), None)
    if not set_id:
        raise ValueError("Tech Leaders not found")
    payload = {
        "ticker": "GOOGL",
        "shares": 3,
        "purchase_date": "2025-04-01",
        "cost_basis": 2800.0,
        "currency": "USD",
        "fees": 2.0
    }
    resp = client.post(f"/portfolios/sets/{set_id}/assets", json=payload)
    assert resp.status_code == 201
    updated = resp.json()
    assets = next(s["assets"] for s in updated["sets"] if s["id"] == set_id)
    assert any(a["ticker"] == "GOOGL" for a in assets)