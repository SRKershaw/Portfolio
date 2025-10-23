# tests/test_main.py - Pytest for API endpoints; extensible for more tests (e.g., auth, data validation)

import pytest
from fastapi.testclient import TestClient  # Simulates HTTP requests without running server
from backend.main import app  # Import the FastAPI app instance

client = TestClient(app)  # Create a test client for in-memory requests

def test_read_root():
    response = client.get("/")  # Send a simulated GET request to root endpoint
    assert response.status_code == 200  # Assert HTTP status is success
    assert response.json() == {"message": "Hello from backend!"}  # Assert response matches expected JSON