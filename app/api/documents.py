from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_documents():
    pass

@app.get("/{document_id}")
def get_document():
    pass

@app.post("/")
def create_document():
    pass

@app.put("/{document_id}")
def update_document():
    pass

@app.delete("/{document_id}")
def delete_document():
    pass