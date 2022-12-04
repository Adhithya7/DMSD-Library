from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_chairs():
    pass

@app.get("/{chair_id}")
def get_chair():
    pass

@app.post("/")
def create_chair():
    pass

@app.put("/{chair_id}")
def update_chair():
    pass

@app.delete("/{chair_id}")
def delete_chair():
    pass