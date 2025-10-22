# main.py - FastAPI app entry point with basic endpoint and CORS for frontend integration

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Enables CORS to allow frontend requests from different origins

app = FastAPI()  # Initialize the FastAPI application instance

# Add CORS middleware for security and dev convenience (extensible: update origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from Vite dev server
    allow_credentials=True,  # Support cookies if needed later (e.g., sessions)
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (e.g., Authorization for JWT)
)

@app.get("/")  # Define a GET endpoint at the root path
def read_root():
    return {"message": "Hello from backend!"}  # Return a simple JSON response; this will be fetched by frontend