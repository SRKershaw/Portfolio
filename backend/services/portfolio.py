# backend/services/portfolio.py
# In-memory storage – replace with SQLAlchemy later (same interface)

from schemas.portfolio import Portfolio, Set, Asset, SetCreate, AssetCreate
from typing import List, Optional

# Global list – will hold all user portfolios
_portfolios: List[Portfolio] = []


def get_all() -> List[Portfolio]:
    return _portfolios


def get_by_id(portfolio_id: str) -> Optional[Portfolio]:
    return next((p for p in _portfolios if p.id == portfolio_id), None)


def create(portfolio: Portfolio) -> Portfolio:
    _portfolios.append(portfolio)
    return portfolio

def add_set(portfolio: Portfolio, set_data: SetCreate) -> Set:
    """Create a new Set and append to portfolio.sets"""
    new_set = Set(name=set_data.name)
    portfolio.sets.append(new_set)
    return new_set

def add_asset_to_set(portfolio: Portfolio, set_id: str, asset_data: AssetCreate) -> Asset:
    """Find Set by ID and add Asset"""
    target_set = next((s for s in portfolio.sets if s.id == set_id), None)
    if not target_set:
        raise HTTPException(status_code=404, detail="Set not found")

    new_asset = Asset(
        ticker=asset_data.ticker,
        shares=asset_data.shares,
        purchase_date=asset_data.purchase_date,
        cost_basis=asset_data.cost_basis,
        currency=asset_data.currency,
        fees=asset_data.fees
    )
    target_set.assets.append(new_asset)
    return new_asset


# Helper to seed a demo portfolio (optional, for quick testing)
def seed_demo():
    from schemas.portfolio import Portfolio, Set, Asset
    from datetime import date

    demo = Portfolio.new(name="Demo Growth Portfolio")
    tech_set = Set(name="Tech Leaders")
    tech_set.assets.extend([
        Asset(ticker="AAPL", shares=10, purchase_date=date(2025,1,15),
              cost_basis=150.0, currency="USD", fees=5.0),
        Asset(ticker="MSFT", shares=5, purchase_date=date(2025,2,1),
              cost_basis=300.0, currency="USD")
    ])
    demo.sets.append(tech_set)
    create(demo)

# Run once on import (remove in production)
seed_demo()