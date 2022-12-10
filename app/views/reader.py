import traceback as tb
from flask import Blueprint, render_template, request, flash, redirect, url_for
from utils import connection, cursor

reader = Blueprint('reader', __name__, url_prefix='/reader', template_folder='templates')

available_query = """ 
                SELECT C.docid, C.copyno, C.bid from copy C
                EXCEPT
                SELECT C.docid, C.copyno, C.bid from copy C
                JOIN borrows B
                on C.docid=B.docid and C.bid= B.bid and C.copyno = B.copyno
    """

docs_query = """ SELECT docid, title, pdate, D.publisherid as publisherid, pubname,address from document D 
                JOIN PUBLISHER P 
                ON D.publisherid = P.publisherid
            """

@reader.route("/validate", methods=["GET"])
def validate():
    query = f'SELECT * from READER R where rid={request.args.get("rid")}'
    cursor.execute(query)
    resp = cursor.fetchall()
    if resp:
        return render_template("explore.html")
    return render_template("home.html", valid='false')

@reader.route("/search", methods=["GET"])
def search():
    all_docs_query = docs_query
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
    cursor.execute(all_docs_query)
    columns = [desc[0] for desc in cursor.description]
    all_docs = cursor.fetchall()
    rows = []
    for row in all_docs:
        tmp = list(row)
        tmp.append(str(request.args.get("available") or row[0] in available_docs))
        rows.append(tmp)
    rows.insert(0, columns)
    return render_template("index.html", rows=rows)

@reader.route("/document/<id>", methods=["GET", "POST", "PUT", "DELETE"])
def document(id):
    all_docs_query = docs_query
    if request.method == "GET":
        doc_query = "select {cols} from {type} where docid={id}"

        for type in ['book', 'journal_volume', 'proceedings']:
            cursor.execute(doc_query.format(cols= 'docid',type=type, id=id))
            if cursor.fetchall():
                doc_type = type

        if doc_type == 'book':
            person_query = f"""select doc.docid as docid, pname from ({doc_query.format(cols = 'docid, pid', type='authors', id=id)})
                            as doc join person p on doc.pid = p.pid"""
            spe_query = f"""select p.docid as docid, isbn ,pname from ({person_query}) as p
                            join book b on p.docid = b.docid"""
            final_query = f"""select D.docid as docid, title, pdate, D.publisherid as publisherid,
                            pubname, address, isbn, pname 
                            from ({all_docs_query} and D.docid={id}) as D
                            left join ({spe_query}) as S on D.docid = S.docid"""

        elif doc_type == 'proceedings':
            person_query = f"""select doc.docid as docid, p.pname as pname from ({doc_query.format(cols = 'docid, pid', type='chairs', id=id)})
                            as doc join person p on doc.pid = p.pid"""
            spe_query = f"""select p.docid as docid, cdate, clocation, ceditor, pname from ({person_query}) as p
                            join proceedings pr on p.docid = pr.docid"""
            final_query = f"""select D.docid as docid, title, pdate, D.publisherid as publisherid,
                            pubname, address, cdate, clocation, ceditor, pname
                            from ({all_docs_query} and D.docid={id}) as D
                            left join ({spe_query}) as S on D.docid = S.docid"""
        elif doc_type == 'journal_volume':
            person_query = f"""select doc.docid as docid, issue_no, pname from ({doc_query.format(cols = 'docid, issue_no, pid', type='gedits', id=id)})
                            as doc join person p on doc.pid = p.pid"""
            issue_query = f"""select p.docid as docid, p.issue_no as issue_no, scope, pname from ({person_query}) as p
                            join journal_issue ji on p.docid = ji.docid and p.issue_no = ji.issue_no"""
            editor_query = f"""select doc.docid as docid, volume_no, pname from ({doc_query.format(cols = 'docid, editor, volume_no', type='journal_volume', id=id)})
                            as doc join person p on doc.editor = p.pid"""
            final_query = f"""select D.docid as docid, title, pdate, D.publisherid as publisherid,
                            pubname, address, volume_no, issue_no, scope, S.pname
                            from ({all_docs_query} and D.docid={id}) as D
                            left join ({issue_query}) as S on D.docid = S.docid
                            left join ({editor_query}) as E on D.docid = E.docid"""
        print(final_query)
        cursor.execute(final_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        rows.insert(0, columns)
        print(rows)
        return render_template("index.html", rows=rows)

    elif request.method == "POST":
        rid = request.args.get('rid')
        #select a copy
        copy_query = f"""SELECT docid, copyno, bid from copy
                        WHERE docid in (SELECT sub.docid from ({available_query}) AS sub)"""
        cursor.execute(copy_query)
        copy = cursor.fetchall()
        resv_query = f"""BEGIN;
                        INSERT INTO RESERVES (RID, DOCID, COPYNO, BID) VALUES
                        ({rid}, {copy[0][0]}, {copy[0][1]}, {copy[0][2]});
                        INSERT INTO RESERVATION """
        pass
        
    elif request.method == "PUT":
        pass

    elif request.method == "DELETE":
        pass