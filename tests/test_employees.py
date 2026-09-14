from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_employee():
    response = client.post("/employees", json={"first_name": "John", "last_name": "Doe", "work_email": "john.doe@example.com"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "first_name": "John", "last_name": "Doe", "work_email": "john.doe@example.com"}

def test_missing_fields():
    response = client.post("/employees", json={"first_name": "John", "last_name": "Doe"})
    assert response.status_code == 422

def test_missing_id():
    response = client.get("/employees/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}
