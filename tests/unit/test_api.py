import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import pytest
import asyncio
from fastapi.testclient import TestClient


from api.app import app

client = TestClient(app)


def test_api():
    response = client.post(
        "/process-images/",
        json={
            "images": [
                "https://i.ibb.co/RNKnqMh/algea.jpg",
                "https://i.ibb.co/0cCYDLF/burger.jpg",
            ]
        },
    )
    assert response.status_code == 200
    assert "processing started" in response.json()["status"]
