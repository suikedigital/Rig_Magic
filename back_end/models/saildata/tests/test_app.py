import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_saildata():
    response = client.get("/saildata/1")
    assert response.status_code in (200, 404, 422)
