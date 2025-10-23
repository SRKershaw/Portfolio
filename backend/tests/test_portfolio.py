# backend/tests/test_portfolio.py
from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_list_portfolios():
    resp = client.get("/portfolios")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

def test_read_portfolio():
    portfolio_id = client.get("/portfolios").json()[0]["id"]
    resp = client.get(f"/portfolios/{portfolio_id}")
    assert resp.status_code == 200
    assert "sets" in resp.json()

def test_create_portfolio():
    resp = client.post("/portfolios", json={"name": "Test"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Test"
    assert len(data["sets"]) == 1
    assert data["sets"][0]["name"] == "All Assets"

def test_create_set():
    portfolio_id = client.get("/portfolios").json()[0]["id"]
    resp = client.post(f"/portfolios/{portfolio_id}/sets", json={"name": "New Set"})
    assert resp.status_code == 201
    assert any(s["name"] == "New Set" for s in resp.json()["sets"])

def test_create_asset():
    portfolios = client.get("/portfolios").json()
    set_id = None
    for p in portfolios:
        for s in p["sets"]:
            if s["name"] == "Tech Leaders":
                set_id = s["id"]
                break
        if set_id:
            break
    if not set_id:
        raise ValueError("Tech Leaders not found in any portfolio")
    payload = {
        "ticker": "GOOGL",
        "shares": 3,
        "purchase_date": "2025-04-01",
        "cost_basis": 2800.0,
        "currency": "USD",
        "fees": 2.0
    }
    resp = client.post(f"/sets/{set_id}/assets", json=payload)
    assert resp.status_code == 201
    updated = resp.json()
    assets = next(s["assets"] for s in updated["sets"] if s["id"] == set_id)
    assert any(a["ticker"] == "GOOGL" for a in assets)