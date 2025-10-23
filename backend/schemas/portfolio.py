# backend/schemas/portfolio.py
# Pydantic models – validate incoming JSON and shape outgoing responses

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, validator
import uuid


class Asset(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ticker: str = Field(..., min_length=1, max_length=10)
    shares: float = Field(..., gt=0)
    purchase_date: date
    cost_basis: float = Field(..., gt=0)      # price per share at purchase
    currency: str = Field(..., min_length=3, max_length=3)   # e.g. USD, EUR
    fees: Optional[float] = Field(default=0.0, ge=0)

    @validator("ticker")
    def upper_case(cls, v):
        return v.upper()


class Set(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=50)
    assets: List[Asset] = Field(default_factory=list)


class Portfolio(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    sets: List[Set] = Field(default_factory=list)

    # Helper to create a default "All Assets" set
    @classmethod
    def new(cls, name: str) -> "Portfolio":
        default_set = Set(name="All Assets")
        return cls(name=name, sets=[default_set])
    
class SetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class AssetCreate(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10)
    shares: float = Field(..., gt=0)
    purchase_date: date
    cost_basis: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    fees: Optional[float] = Field(default=0.0, ge=0)

    @validator("ticker")
    def upper_case(cls, v):
        return v.upper()    