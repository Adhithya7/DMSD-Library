from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_reserves():
    pass

@app.get("/{reserve_id}")
def get_reserve():
    pass

@app.post("/")
def create_reserve():
    pass

@app.put("/{reserve_id}")
def update_reserve():
    pass

@app.delete("/{reserve_id}")
def delete_reserve():
    pass