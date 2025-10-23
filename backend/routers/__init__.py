# backend/routers/__init__.py
# This makes 'routers' a Python package so imports work

from .portfolio import router as portfolio_router

__all__ = ["portfolio_router"]

