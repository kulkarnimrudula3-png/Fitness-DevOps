import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

from ACEest_Fitness import app


def test_home_page_loads():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"ACEest Fitness" in response.data


def test_health_check():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "UP"


def test_get_members():
    client = app.test_client()
    response = client.get("/members")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_add_member_success():
    client = app.test_client()
    response = client.post("/members", json={"name": "Megha", "plan": "Gold", "trainer": "Riya"})
    assert response.status_code == 201
    assert response.get_json()["name"] == "Neha"


def test_add_member_validation_error():
    client = app.test_client()
    response = client.post("/members", json={"name": "Incomplete"})
    assert response.status_code == 400
