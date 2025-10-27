# backend/routers/portfolio.py
######################################################################################
from fastapi import APIRouter, HTTPException
from typing import List
from schemas.portfolio import Portfolio, PortfolioCreate, SetCreate, AssetCreate
from services.portfolio import get_all, get_by_id, create, add_set, add_asset_to_set

router = APIRouter(prefix="/portfolios", tags=["portfolios"])

@router.get("/", response_model=List[Portfolio])
def list_portfolios():
    return get_all()

@router.get("/{portfolio_id}", response_model=Portfolio)
def read_portfolio(portfolio_id: str):
    portfolio = get_by_id(portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

@router.post("/", response_model=Portfolio, status_code=201)
def create_portfolio(payload: PortfolioCreate):
    new_p = Portfolio.new(name=payload.name)
    return create(new_p)

@router.post("/{portfolio_id}/sets", response_model=Portfolio, status_code=201)
def create_set(portfolio_id: str, set_data: SetCreate):
    portfolio = get_by_id(portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    add_set(portfolio, set_data)
    return portfolio

@router.post("/sets/{set_id}/assets", response_model=Portfolio, status_code=201)
def create_asset(set_id: str, asset_data: AssetCreate):
    for portfolio in get_all():
        target_set = next((s for s in portfolio.sets if s.id == set_id), None)
        if target_set:
            add_asset_to_set(portfolio, set_id, asset_data)
            return portfolio
    raise HTTPException(status_code=404, detail="Set not found")