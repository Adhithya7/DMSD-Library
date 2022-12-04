from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_proceedings():
    pass

@app.get("/{proceeding_id}")
def get_proceeding():
    pass

@app.post("/")
def create_proceeding():
    pass

@app.put("/{proceeding_id}")
def update_proceeding():
    pass

@app.delete("/{proceeding_id}")
def delete_proceeding():
    pass