from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_journel_volumes():
    pass

@app.get("/{journel_volume_id}")
def get_journel_volume():
    pass

@app.post("/")
def create_journel_volume():
    pass

@app.put("/{journel_volume_id}")
def update_journel_volume():
    pass

@app.delete("/{journel_volume_id}")
def delete_journel_volume():
    pass