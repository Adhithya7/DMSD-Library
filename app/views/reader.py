import traceback as tb
from flask import Blueprint, render_template, request, flash, redirect, url_for
from utils import connection, cursor

reader = Blueprint('reader', __name__, url_prefix='/reader')

@reader.route("/test", methods=["GET"])
def test():
    test_response = "all good"
    return render_template("layout.html", rows=test_response)

@reader.route("/search", methods=["GET"])
def search():
    all_docs_query = """ SELECT * from document D 
                JOIN PUBLISHER P 
                ON D.publisherid = P.publisherid 
            """
    if request.args.get('docid'):
        all_docs_query += f"and D.docid={request.args.get('docid')}"
    if request.args.get("title"):
        all_docs_query += f" and D.title like %{request.args.get('title')}%"
    if request.args.get("publisher_name"):
        all_docs_query += f" and P.publisher_name like %{request.args.get('publisher_name')}%"
    ql = int(request.args.get('limit', 10))
    if ql < 1 or ql > 100:
        all_docs_query += f" LIMIT 10"
    else:
        all_docs_query += f" LIMIT {ql}"
    print(all_docs_query)
    cursor.execute(all_docs_query)
    all_docs = set(cursor.fetchall())
    doc_ids = [row[0] for row in all_docs]

    print(all_docs)

    return render_template("explore.html", rows=all_docs)

@reader.route("/document/{id}", methods=["GET", "POST", "PUT"])
def document():
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass
    if request.method == "PUT":
        pass