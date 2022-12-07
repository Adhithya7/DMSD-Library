from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

app = FastAPI()

@app.get("/")
def list_journel_issues():
    pass

@app.get("/{journel_issue_id}")
def get_journel_issue():
    pass

@app.post("/")
def create_journel_issue():
    pass

@app.put("/{journel_issue_id}")
def update_journel_issue():
    pass

@app.delete("/{journel_issue_id}")
def delete_journel_issue():
    pass