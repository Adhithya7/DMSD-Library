import traceback as tb
from flask import Blueprint, render_template, request, flash, redirect, url_for
from utils import connection, cursor

reader = Blueprint('reader', __name__, url_prefix='/reader', template_folder='templates')

@reader.route("/test", methods=["GET"])
def test():
    test_response = "all good"
    return render_template("layout.html", rows=test_response)

@reader.route("/search", methods=["GET"])
def search():
    available_query = """ 
                SELECT C.docid, C.copyno, C.bid from copy C
                EXCEPT
                SELECT C.docid, C.copyno, C.bid from copy C
                JOIN borrows B
                on C.docid=B.docid and C.bid= B.bid and C.copyno = B.copyno
    """
    all_docs_query = """ SELECT * from document D 
                JOIN PUBLISHER P 
                ON D.publisherid = P.publisherid
            """
    cursor.execute(f'SELECT sub.docid from ({available_query}) AS sub')
    available_docs = cursor.fetchall()
    available_docs = [row[0] for row in available_docs]
    if request.args.get('docid'):
        all_docs_query += f"and D.docid={request.args.get('docid')}"
    if request.args.get("title"):
        all_docs_query += f" and D.title like %{request.args.get('title')}%"
    if request.args.get("publisher_name"):
        all_docs_query += f" and P.publisher_name like %{request.args.get('publisher_name')}%"
    if request.args.get("available"):
        all_docs_query += f"and D.docid in (SELECT sub.docid from ({available_query}) AS sub)"
    ql = int(request.args.get('limit', 10))
    if ql < 1 or ql > 100:
        all_docs_query += f" LIMIT 10"
    else:
        all_docs_query += f" LIMIT {ql}"
    print(all_docs_query)
    cursor.execute(all_docs_query)
    columns = [desc[0] for desc in cursor.description]
    all_docs = cursor.fetchall()
    all_docs.insert(0, columns)
    rows = []
    for row in all_docs[1:]:
        tmp = list(row)
        tmp.append(str(request.args.get("available") or row[0] in available_docs))
        rows.append(tmp)
    return render_template("index.html", rows=rows)

@reader.route("/document/{id}", methods=["GET", "POST", "PUT"])
def document():
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass
    if request.method == "PUT":
        pass