from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_persons():
    pass

@app.get("/{person_id}")
def get_person():
    pass

@app.post("/")
def create_person():
    pass

@app.put("/{person_id}")
def update_person():
    pass

@app.delete("/{person_id}")
def delete_person():
    pass