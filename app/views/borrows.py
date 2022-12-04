from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_borrowss():
    pass

@app.get("/{borrows_id}")
def get_borrows():
    pass

@app.post("/")
def create_borrows():
    pass

@app.put("/{borrows_id}")
def update_borrows():
    pass

@app.delete("/{borrows_id}")
def delete_borrows():
    pass