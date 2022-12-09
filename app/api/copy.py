from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_copies():
    pass

@app.get("/{copy_id}")
def get_copy():
    pass

@app.post("/")
def create_copy():
    pass

@app.put("/{copy_id}")
def update_copy():
    pass

@app.delete("/{copy_id}")
def delete_copy():
    pass