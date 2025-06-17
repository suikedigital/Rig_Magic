import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from src.app import app

client = TestClient(app)


def test_get_hull():
    response = client.get("/hull/1")
    assert response.status_code in (200, 404, 422)
