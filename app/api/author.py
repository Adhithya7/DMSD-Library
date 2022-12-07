from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_authors():
    pass

@app.get("/{author_id}")
def get_author():
    pass

@app.post("/")
def create_author():
    pass

@app.put("/{author_id}")
def update_author():
    pass

@app.delete("/{author_id}")
def delete_author():
    pass
