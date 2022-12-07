from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_books():
    pass

@app.get("/{book_id}")
def get_book():
    pass

@app.post("/")
def create_book():
    pass

@app.put("/{book_id}")
def update_book():
    pass

@app.delete("/{book_id}")
def delete_book():
    pass