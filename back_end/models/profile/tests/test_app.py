import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_list_profiles():
    response = client.get("/profile/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
