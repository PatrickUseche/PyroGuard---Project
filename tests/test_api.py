from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def normal_payload():
    return {
        "node_id": "TEST-001",
        "temperature": 22.0,
        "humidity": 70.0,
        "smoke": 12.0,
        "gas": 5.0,
        "flame": False,
        "timestamp": "2026-10-13T12:00:00-05:00",
    }


def test_health_has_model_loaded():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["model_loaded"] is True
    assert body["status"] == "ok"


def test_prediction_contract_and_probabilities():
    response = client.post("/predict", json=normal_payload())
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "ok"
    assert body["node_id"] == "TEST-001"
    assert body["risk_level"] in {"NORMAL", "WARNING", "FIRE"}
    assert 0 <= body["risk_probability"] <= 1
    assert set(body["probabilities"]) == {"NORMAL", "WARNING", "FIRE"}
    assert body["model_version"]


def test_gas_is_optional():
    payload = normal_payload()
    payload.pop("gas")
    response = client.post("/predict", json=payload)
    assert response.status_code == 200, response.text


def test_rejects_out_of_range_humidity():
    payload = normal_payload()
    payload["humidity"] = 150
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
