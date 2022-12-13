import traceback as tb
from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from utils import connection, cursor

reader = Blueprint('reader', __name__, url_prefix='/reader',
                   template_folder='templates')

available_query = """
                SELECT C.docid, C.copyno, C.bid from copy C
                EXCEPT
                ((SELECT C.docid, C.copyno, C.bid from copy C
                JOIN reserves R
                on C.docid=R.docid and C.bid= R.bid and C.copyno = R.copyno)
                UNION
                (SELECT C.docid, C.copyno, C.bid from copy C
                JOIN (SELECT * from BORROWS BR
                JOIN BORROWING BS on BR.rid = {rid} and BR.bor_no = BS.bor_no
                and BS.rdtime is null) as B
                on C.docid = B.docid)
                UNION
                (SELECT C.docid, C.copyno, C.bid from copy C
                JOIN (SELECT * from BORROWS BR
                JOIN BORROWING BS on BR.bor_no = BS.bor_no
                and BS.rdtime is null) as B
                on C.docid = B.docid)
                UNION
                (SELECT C.docid, C.copyno, C.bid from copy C
                JOIN (SELECT * from RESERVES where rid = {rid}) as B
                on C.docid = B.docid))
    """

docs_query = """ SELECT docid, title, pdate, D.publisherid as publisherid, pubname,address from document D
                JOIN PUBLISHER P
                ON D.publisherid = P.publisherid
            """


@reader.route("/", methods=["GET"])
def base():
    return render_template("home.html")


@reader.route("/validate", methods=["GET"])
def validate():
    rid = request.args.get('rid')
    query = f'SELECT * from READER R where rid={request.args.get("rid")}'
    cursor.execute(query)
    resp = cursor.fetchall()
    if resp:
        return render_template("index.html")
    flash("Please register with the library first.", "danger")
    return render_template("home.html", rid=rid)


@reader.route("/search", methods=["GET"])
def search():
    rid = request.args.get('rid')
    all_docs_query = docs_query
    cursor.execute(
        f'SELECT sub.docid from ({available_query.format(rid=rid)}) AS sub')
    available_docs = cursor.fetchall()
    available_docs = set([row[0] for row in available_docs])
    # print(available_docs)
    if request.args.get('docid'):
        all_docs_query += f"and D.docid={request.args.get('docid')}"
    if request.args.get("title"):
        all_docs_query += f" and D.title ilike '%{request.args.get('title')}%'"
    if request.args.get("publisher_name"):
        all_docs_query += f" and P.pubname ilike '%{request.args.get('publisher_name')}%'"
    if request.args.get("available"):
        all_docs_query += f"and D.docid in (SELECT sub.docid from ({available_query.format(rid=rid)}) AS sub)"
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
        tmp.append(str(request.args.get("available")
                   or row[0] in available_docs))
        rows.append(tmp)
    rows.insert(0, columns)
    # print(rows)
    return render_template("explore.html", rows=rows, rid=rid)


@reader.route("/document/<id>", methods=["GET", "POST", "PUT", "DELETE"])
def document(id):
    all_docs_query = docs_query
    if request.method == "GET":  # View document
        available = request.args.get('available')
        doc_query = "select {cols} from {type} where docid={id}"

        for type in ['book', 'journal_volume', 'proceedings']:
            cursor.execute(doc_query.format(cols='docid', type=type, id=id))
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
                            pubname, address, volume_no, issue_no, scope, S.pname as issue_editor, E.pname as chief_editor
                            from ({all_docs_query} and D.docid={id}) as D
                            left join ({issue_query}) as S on D.docid = S.docid
                            left join ({editor_query}) as E on D.docid = E.docid"""
        # print(final_query)
        cursor.execute(final_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        rows.insert(0, columns)
        print(rows)
        return render_template("resource.html", rows=rows, doc_type=doc_type, available=available)

    elif request.method == "POST":  # RESERVE DOC
        rid = request.args.get('rid')
        available = request.args.get('available')
        # select a copy
        copy_query = f"""SELECT D.copyno, D.bid from ({available_query.format(rid=rid)}) AS D
                        WHERE docid={id} limit 1;"""
        cursor.execute(copy_query)
        copy = cursor.fetchall()
        if not copy:
            flash(
                "User has already reserved/borrowed a different copy of the book", "danger")
            print("User has already reserved/borrowed a different copy of the book")
            return ()
        resv_query = f"""INSERT INTO RESERVES (RID, DOCID, COPYNO, BID) VALUES
                        ({rid}, {id}, {copy[0][0]}, {copy[0][1]});"""
        try:
            cursor.execute(resv_query)
            connection.commit()
            flash("Reserved Book", "success")
        except Exception as e:
            print(tb.format_exc())
            flash(f"Unexpected error while reserving book: {e}")
        return redirect(request.url)

    elif request.method == "PUT":  # BORROW DOC
        rid = request.args.get('rid')
        copy_query = f"""SELECT copyno, bid from reserves
                        WHERE docid = {id} and rid = {rid};"""
        cursor.execute(copy_query)
        copy = cursor.fetchall()
        borrow_query = f"""INSERT INTO BORROWS (RID, DOCID, COPYNO, BID) VALUES
                        ({rid}, {id}, {copy[0][0]}, {copy[0][1]});"""
        try:
            cursor.execute(borrow_query)
            connection.commit()
            flash("Borrowed Book", "success")
        except Exception as e:
            print(tb.format_exc())
            flash(f"Unexpected error while Borrowing book: {e}")
        return redirect(request.url)


@reader.route("/return_document/<id>", methods=["GET"])
def return_document(id):
    rid = request.args.get('rid')
    borrow_query = f"""SELECT BOR_NO from BORROWS
                        WHERE docid = {id} and rid = {rid}"""
    return_query = f"""UPDATE BORROWING
                            SET RDTIME = now()
                            WHERE BOR_NO in ({borrow_query}) and RDTIME is NULL;"""
    try:
        cursor.execute(return_query)
        connection.commit()
        # flash("Returned Book", "success")
    except Exception as e:
        print(tb.format_exc())
        flash(f"Unexpected error while Returning book: {e}")
        
    #Loading my transactions page again
    reserve_query = f"""SELECT docid, bid, dtime as tx_time, NULL as ret_time, 'RESERVED' as status  from RESERVES R
                        JOIN RESERVATION RI ON R.reservation_no = RI.res_no and R.rid = {rid}"""
    borrow_query = f"""SELECT docid, bid, bdtime as tx_time, rdtime as ret_time, 'RETURNED' as STATUS from BORROWS B
                      JOIN BORROWING BI ON B.bor_no = BI.bor_no and B.rid = {rid} and BI.rdtime is not null"""
    return_query = f"""SELECT docid, bid, bdtime as tx_time, NULL as ret_time, 'BORROWED' as STATUS from BORROWS B
                       JOIN BORROWING BI ON B.bor_no = BI.bor_no and B.rid = {rid} and BI.rdtime is null"""
    docs = f"""  SELECT sub1.docid as "Doc ID", title as "Title", location as "BranchLocation", tx_time as "Borrowed On", ret_time as "Returned On", status as "Status" from 
                (({reserve_query}) UNION ({borrow_query}) UNION ({return_query})) as sub1
                JOIN DOCUMENT D on sub1.docid = D.docid
                JOIN BRANCH B ON sub1.bid = B.bid
                """

    cursor.execute(docs)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    rows.insert(0, columns)
    print(rows)
    return render_template("my_transactions.html", rows=rows, rid=rid)


@reader.route("/document", methods=["GET"])
def list_documents():
    rid = request.args.get('rid')
    reserve_query = f"""SELECT docid, bid, dtime as tx_time, NULL as ret_time, 'RESERVED' as status  from RESERVES R
                        JOIN RESERVATION RI ON R.reservation_no = RI.res_no and R.rid = {rid}"""
    borrow_query = f"""SELECT docid, bid, bdtime as tx_time, rdtime as ret_time, 'RETURNED' as STATUS from BORROWS B
                      JOIN BORROWING BI ON B.bor_no = BI.bor_no and B.rid = {rid} and BI.rdtime is not null"""
    return_query = f"""SELECT docid, bid, bdtime as tx_time, NULL as ret_time, 'BORROWED' as STATUS from BORROWS B
                       JOIN BORROWING BI ON B.bor_no = BI.bor_no and B.rid = {rid} and BI.rdtime is null"""
    docs = f"""  SELECT sub1.docid as "Doc ID", title as "Title", location as "BranchLocation", tx_time as "Borrowed On", ret_time as "Returned On", status as "Status" from 
                (({reserve_query}) UNION ({borrow_query}) UNION ({return_query})) as sub1
                JOIN DOCUMENT D on sub1.docid = D.docid
                JOIN BRANCH B ON sub1.bid = B.bid
                """

    cursor.execute(docs)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    rows.insert(0, columns)
    print(rows)
    return render_template("my_transactions.html", rows=rows, rid=rid)


@reader.route("/fines/<rid>", methods=["GET"])
def fine(rid):
    docid = request.args.get('docid')
    all_docs_query = docs_query
    reader_docs_query = f"""SELECT docid from """
