from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_borrowings():
    pass

@app.get("/{borrowing_id}")
def get_borrowing():
    pass

@app.post("/")
def create_borrowing():
    pass

@app.put("/{borrowing_id}")
def update_borrowing():
    pass

@app.delete("/{borrowing_id}")
def delete_borrowing():
    pass