# backend/main.py
######################################################################################

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import portfolio_router as portfolio

app = FastAPI(
    title="Portfolio API",
    version="0.1.0"
)

# CORS – keep allowing the Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(portfolio)

# (Optional) root just for health check
@app.get("/")
def root():
    return {"message": "Portfolio API is alive"}