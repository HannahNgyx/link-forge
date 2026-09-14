from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    work_email: str

class Employee(EmployeeCreate):
    id: int

class EmployeeWebhook(EmployeeCreate):
    event_id: str

app = FastAPI()
employees: dict[int, Employee] = {}

def generate_id():
    return len(employees) + 1

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/employees", status_code=201)
def create_employee(employee: EmployeeCreate) -> Employee:
    employee_id = generate_id()
    employee = Employee(id=employee_id, **employee.model_dump())
    employees[employee_id] = employee
    return employee

@app.get("/employees")
def get_all_employees() -> list[Employee]:
    return list(employees.values())

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int) -> Employee:
    if employee_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employees[employee_id]

processed_event_ids: set[str] = set()
@app.post("/webhooks/employees", status_code=200)
def receive_employee_webhook(webhook: EmployeeWebhook):
    if webhook.event_id in processed_event_ids:
        return {"status": "ok"}
    employee = Employee(id=generate_id(), **webhook.model_dump(exclude={"event_id"}))
    employees[employee.id] = employee
    processed_event_ids.add(webhook.event_id)
    return {"status": "ok"}
