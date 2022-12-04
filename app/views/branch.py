from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_branchs():
    pass

@app.get("/{branch_id}")
def get_branch():
    pass

@app.post("/")
def create_branch():
    pass

@app.put("/{branch_id}")
def update_branch():
    pass

@app.delete("/{branch_id}")
def delete_branch():
    pass