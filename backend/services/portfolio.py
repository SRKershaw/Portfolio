# backend/services/portfolio.py
######################################################################################

from typing import List, Optional
from schemas.portfolio import Portfolio, Set, Asset, SetCreate, AssetCreate
from fastapi import HTTPException
from datetime import date
import uuid

_portfolios: List[Portfolio] = []

def get_all() -> List[Portfolio]:
    if not _portfolios:
        seed_demo()
    return _portfolios

def get_by_id(portfolio_id: str) -> Optional[Portfolio]:
    return next((p for p in get_all() if p.id == portfolio_id), None)

def create(portfolio: Portfolio) -> Portfolio:
    _portfolios.append(portfolio)
    return portfolio

def add_set(portfolio: Portfolio, set_data: SetCreate) -> Set:
    new_set = Set(name=set_data.name)
    portfolio.sets.append(new_set)
    return new_set

def add_asset_to_set(portfolio: Portfolio, set_id: str, asset_data: AssetCreate) -> Asset:
    target_set = next((p for p in portfolio.sets if p.id == set_id), None)
    if not target_set:
        raise HTTPException(status_code=404, detail="Set not found")
    new_asset = Asset(
        ticker=asset_data.ticker.upper(),
        shares=asset_data.shares,
        purchase_date=asset_data.purchase_date,
        cost_basis=asset_data.cost_basis,
        currency=asset_data.currency,
        fees=asset_data.fees or 0.0
    )
    target_set.assets.append(new_asset)
    return new_asset

def seed_demo():
    if any(p.name == "Demo Growth Portfolio" for p in _portfolios):
        return
    demo = Portfolio.new(name="Demo Growth Portfolio")
    tech_set = Set(name="Tech Leaders")
    tech_set.assets.extend([
        Asset(ticker="AAPL", shares=10, purchase_date=date(2025,1,15), cost_basis=150.0, currency="USD", fees=5.0),
        Asset(ticker="MSFT", shares=5, purchase_date=date(2025,2,1), cost_basis=300.0, currency="USD")
    ])
    demo.sets.append(tech_set)
    create(demo)