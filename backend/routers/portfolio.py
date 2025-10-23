# backend/routers/portfolio.py

from fastapi import APIRouter, HTTPException, status
from typing import List
from services.portfolio import get_all, get_by_id, create, add_set, add_asset_to_set
from schemas.portfolio import Portfolio, SetCreate, AssetCreate

router = APIRouter(prefix="/portfolios", tags=["portfolios"])

@router.get("/", response_model=List[Portfolio])
def list_portfolios():
    """Return every portfolio (just IDs + names for a compact list)."""
    return get_all()


@router.get("/{portfolio_id}", response_model=Portfolio)
def read_portfolio(portfolio_id: str):
    """Full portfolio with all Sets and Assets."""
    portfolio = get_by_id(portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio


@router.post("/", response_model=Portfolio, status_code=201)
def create_portfolio(payload: Portfolio):
    """Create a new portfolio (you can send just the name)."""
    # If client sends full object we keep it, otherwise make a minimal one
    if not payload.name:
        raise HTTPException(status_code=400, detail="Portfolio name required")
    new_port = Portfolio.new(name=payload.name)
    return create(new_port)

@router.post("/{portfolio_id}/sets", response_model=Portfolio, status_code=201)
def create_set(portfolio_id: str, set_data: SetCreate):
    """Create a new Set inside a portfolio"""
    portfolio = get_by_id(portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    add_set(portfolio, set_data)
    return portfolio


@router.post("/{set_id}/assets", response_model=Portfolio, status_code=201)
def create_asset(set_id: str, asset_data: AssetCreate):
    """Add an Asset to a specific Set (find portfolio via Set)"""
    # Find which portfolio contains this set
    for portfolio in get_all():
        target_set = next((s for s in portfolio.sets if s.id == set_id), None)
        if target_set:
            add_asset_to_set(portfolio, set_id, asset_data)
            return portfolio
    raise HTTPException(status_code=404, detail="Set not found")