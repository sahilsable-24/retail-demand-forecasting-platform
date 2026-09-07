from fastapi.testclient import TestClient
from api.app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_invalid_store():
    response = client.post("/predict", json={
        "store_id": 99999,
        "start_date": "2015-07-01",
        "horizon_days": 3,
        "promo_schedule": [0, 0, 0]
    })
    assert response.status_code == 404

def test_predict_valid():
    response = client.post("/predict", json={
        "store_id": 1,
        "start_date": "2015-07-01",
        "horizon_days": 3,
        "promo_schedule": [1, 0, 0]
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["predictions"]) == 3