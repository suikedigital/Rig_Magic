import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_search_yachts():
    response = client.get("/yachts/search?query=")
    assert response.status_code in (200, 404, 422)
