import logging
from fastapi.params import Depends
import uvicorn
import os

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from app.api import api_router
from app.utils.auth import check_basic_auth

app = FastAPI(title="Library", openapi_url=None, docs_url=None, redoc_url=None)

app.include_router(api_router)

@app.get("/docs")
async def get_docs(username: str = Depends(check_basic_auth)):
    return get_swagger_ui_html(openapi_url="http://127.0.0.1:8000/openapi.json", title="docs")

@app.get("/openapi.json")
async def openapi(username: str = Depends(check_basic_auth)):
    return get_openapi(title = "FastAPI", version="0.1.0", routes=app.routes)

@app.get("/ping")
def ping():
    return {"message": "pong"}

if __name__ == "__main__":
    logging.basicConfig(
        format='INFO',
        level='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    uvicorn.run(app, host="0.0.0.0", port=8000)
