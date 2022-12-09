from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_transactions():
    pass

@app.get("/{transaction_id}")
def get_transaction():
    pass

@app.post("/")
def create_transaction():
    pass

@app.put("/{transaction_id}")
def update_transaction():
    pass

@app.delete("/{transaction_id}")
def delete_transaction():
    pass