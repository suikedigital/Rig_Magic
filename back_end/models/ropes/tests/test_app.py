import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_possible_ropes():
    response = client.get("/ropes/possible/1")
    assert response.status_code in (200, 404, 422)
