from fastapi import FastAPI, HTTPException
from Awol import (
    authenticate,
    get_leave_status,
    apply_leave,
    get_all_employees,
    get_all_leave_balances,
    reset_leave,
)

app = FastAPI(title="AWOL Leave Management API")

# Authentication/login
@app.post("/login")
def login(employee_id: int, password: str):
    user = authenticate(employee_id, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "employee_id": user[0],
        "name": user[1],
        "total_leave": user[3],
        "leave_taken": user[4],
        "role": user[5],
    }

# Employee menu functions
@app.get("/leave_status/{employee_id}")
def leave_status(employee_id: int):
    status = get_leave_status(employee_id)
    if not status:
        raise HTTPException(status_code=404, detail="Employee not found")
    return status

@app.post("/apply_leave")
def apply_leave_api(employee_id: int, days: int):
    success, msg = apply_leave(employee_id, days)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}

#Manager menu functions
@app.get("/employees")
def employees():
    return get_all_employees()

@app.get("/leave_balances")
def leave_balances():
    return get_all_leave_balances()

@app.post("/reset_leave")
def reset_leave_api(employee_id: int):
    success, msg = reset_leave(employee_id)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}


#open http://127.0.0.1:8000/docs to see the Swagger UI API documentation
#open http://127.0.0.1:8000/redoc to see an alternative API documentation
#run the app with: uvicorn AwolAPI:app --reload


    