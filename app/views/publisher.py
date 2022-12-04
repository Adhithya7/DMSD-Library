from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_publishers():
    pass

@app.get("/{publisher_id}")
def get_publisher():
    pass

@app.post("/")
def create_publisher():
    pass

@app.put("/{publisher_id}")
def update_publisher():
    pass

@app.delete("/{publisher_id}")
def delete_publisher():
    pass