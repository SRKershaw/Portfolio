from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import date
import uuid

def uuid_factory():
    return str(uuid.uuid4())

class Asset(BaseModel):
    id: str = Field(default_factory=uuid_factory)
    ticker: str
    shares: float
    purchase_date: date
    cost_basis: float
    currency: str
    fees: Optional[float] = 0.0

    @field_validator("ticker")
    def upper(cls, v):
        return v.upper()

class Set(BaseModel):
    id: str = Field(default_factory=uuid_factory)
    name: str
    assets: List[Asset] = Field(default_factory=list)

class Portfolio(BaseModel):
    id: str = Field(default_factory=uuid_factory)
    name: str
    sets: List[Set] = Field(default_factory=list)

    @classmethod
    def new(cls, name: str) -> "Portfolio":
        return cls(name=name, sets=[Set(name="All Assets")])

class PortfolioCreate(BaseModel):
    name: str

class SetCreate(BaseModel):
    name: str

class AssetCreate(BaseModel):
    ticker: str
    shares: float
    purchase_date: date
    cost_basis: float
    currency: str
    fees: Optional[float] = 0.0

    @field_validator("ticker")
    def upper(cls, v):
        return v.upper()