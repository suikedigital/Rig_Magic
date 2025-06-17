import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_search_yachts():
    response = client.get("/yachts/search?query=")
    assert response.status_code in (200, 404, 422)
