from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_gedits():
    pass

@app.get("/{gedit_id}")
def get_gedit():
    pass

@app.post("/")
def create_gedit():
    pass

@app.put("/{gedit_id}")
def update_gedit():
    pass

@app.delete("/{gedit_id}")
def delete_gedit():
    pass