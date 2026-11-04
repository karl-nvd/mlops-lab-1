from pathlib import Path

from fastapi.testclient import TestClient

from src.food11 import serve


class FakeModel:
    def predict(self, x):
        # The API expects logits and applies softmax to turn them into scores.
        return [[5.0] + [0.0] * 10]


def test_health(monkeypatch):
    monkeypatch.setenv("SKIP_MODEL", "1")
    with TestClient(serve.app) as client:
        assert client.get("/health").status_code == 200


def test_predict_returns_valid_json(monkeypatch):
    monkeypatch.setenv("SKIP_MODEL", "1")
    with TestClient(serve.app) as client:
        monkeypatch.setattr(serve, "model", FakeModel())
        with (Path(__file__).parent / "fixtures" / "bread.jpg").open("rb") as image:
            response = client.post(
                "/predict", files={"file": ("bread.jpg", image, "image/jpeg")}
            )
    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "Bread"
    assert 0.0 <= body["confidence"] <= 1.0


def test_predict_without_model(monkeypatch):
    monkeypatch.setenv("SKIP_MODEL", "1")
    with TestClient(serve.app) as client:
        response = client.post(
            "/predict", files={"file": ("bread.jpg", b"unused", "image/jpeg")}
        )
    assert response.status_code == 503
