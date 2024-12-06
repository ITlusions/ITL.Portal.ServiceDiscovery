# test_main.py
from fastapi.testclient import TestClient
from src.main import (  
    app,
)  

client = TestClient(app, base_url="http://localhost:8000")

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()
