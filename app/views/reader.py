import traceback as tb
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ..utils.raw_sql.db import make_connection
from flask import Blueprint, render_template, request, flash, redirect, url_for

connection, cursor = make_connection()
reader = Blueprint('reader', __name__, url_prefix='/reader')

@reader.route("/search", methods=["GET"])
def search():
    query = """ SELECT * from document D 
                JOIN PUBLISHER P 
                ON D.publisherid = P.publisherid 
            """
    if request.args.get('docid'):
        query += f"and D.docid={request.args.get('docid')}"
    if request.args.get("title"):
        query += f" and D.title like %{request.args.get('title')}%"
    if request.args.get("publisher_name"):
        query += f" and P.publisher_name like %{request.args.get('publisher_name')}%"
    query += f" LIMIT %s"
    ql = int(request.args.get('limit', 10))
    if ql < 1 or ql > 100:
        query += f" LIMIT 10"
    else:
        query += f" LIMIT {ql}"
    print(query)
    cursor.execute(query)
    rows = cursor.fetchall()
    return render_template("xyz.html", rows=rows)

@reader.route("/return/{id}", methods=["GET", "POST", "DELETE"])
def document():
    query = """
    """