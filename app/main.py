from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    work_email: str

class Employee(EmployeeCreate):
    id: int

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

