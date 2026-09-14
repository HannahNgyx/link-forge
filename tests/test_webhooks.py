from fastapi.testclient import TestClient
from app.main import app, employees

client = TestClient(app)

def test_first_delivery():
    before_count = len(employees)
    response = client.post("/webhooks/employees", json={"event_id": "123", "first_name": "John", "last_name": "Doe", "work_email": "john.doe@example.com"})
    assert response.status_code == 200
    assert len(employees) == before_count + 1

def test_duplicate_delivery():
    before_count = len(employees)
    response = client.post("/webhooks/employees", json={"event_id": "234", "first_name": "Ana", "last_name": "Taylor", "work_email": "ana.taylor@example.com"})
    response = client.post("/webhooks/employees", json={"event_id": "234", "first_name": "Ana", "last_name": "Taylor", "work_email": "ana.taylor@example.com"})
    assert response.status_code == 200
    assert len(employees) == before_count + 1

def test_missing_event_id():
    response = client.post("/webhooks/employees", json={"first_name": "John", "last_name": "Doe", "work_email": "john.doe@example.com"})
    assert response.status_code == 422
