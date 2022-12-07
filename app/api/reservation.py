from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_reservations():
    pass

@app.get("/{reservation_id}")
def get_reservation():
    pass

@app.post("/")
def create_reservation():
    pass

@app.put("/{reservation_id}")
def update_reservation():
    pass

@app.delete("/{reservation_id}")
def delete_reservation():
    pass