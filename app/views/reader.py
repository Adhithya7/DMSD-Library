import traceback as tb
from flask import Blueprint, render_template, request, flash, redirect, url_for
from utils import connection, cursor

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
    ql = int(request.args.get('limit', 10))
    if ql < 1 or ql > 100:
        query += f" LIMIT 10"
    else:
        query += f" LIMIT {ql}"
    print(query)
    cursor.execute(query)
    rows = cursor.fetchall()
    return render_template("index.html", rows=rows)

@reader.route("/document/{id}", methods=["GET", "POST", "PUT"])
def document():
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass
    if request.method == "PUT":
        pass