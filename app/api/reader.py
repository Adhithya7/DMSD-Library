from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_readers():
    pass

@app.get("/{reader_id}")
def get_reader():
    pass

@app.post("/")
def create_reader():
    pass

@app.put("/{reader_id}")
def update_reader():
    pass

@app.delete("/{reader_id}")
def delete_reader():
    pass