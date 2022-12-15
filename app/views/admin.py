import io
import csv
import traceback as tb
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required
from utils import connection, cursor

admin = Blueprint('admin', __name__, url_prefix='/admin',
                   template_folder='templates')

@admin.route("/most_borrowed", methods=["GET"]) # most borrowed books
#@login_required
def most_borrowed():
    limit = request.args.get('n', '10')
    freq_query = f"""SELECT docid, count(*) as doc_count from borrows BS
                GROUP BY docid
                ORDER BY count(*) DESC
                LIMIT {limit}"""
    docs = f"""SELECT D.docid, D.title, doc_count from document D
              JOIN ({freq_query}) as freq
              ON D.docid = freq.docid"""
    try:
        cursor.execute(docs)
    except Exception as e:
        rows=[]
        connection.rollback()
        flash(f"Unexpected error while fetching result: {e}")
        return render_template("adminResults.html", rows=rows)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    rows.insert(0, columns)
    print(rows)
    return render_template('adminResults.html', rows=rows)

@admin.route("/most_popular", methods=["GET"]) # most popular books of a year
#@login_required
def most_popular():
    limit = request.args.get('n', 10)
    year = request.args.get('year')
    selected_txns = f"""SELECT BOR_NO from BORROWING where BDTIME BETWEEN 
                    to_date('{year}-01-01','YYYY-MM-DD') 
                    AND to_date('{year}-12-31','YYYY-MM-DD')"""
    freq_query = f"""SELECT BS.docid, count(*) as doc_count from borrows BS
                    JOIN ({selected_txns}) as sel
                    ON BS.bor_no = sel.bor_no 
                    GROUP BY docid
                    ORDER BY count(*) DESC
                    LIMIT {limit}"""
    docs = f"""SELECT D.docid, D.title, doc_count from document D
              JOIN ({freq_query}) as freq
              ON D.docid = freq.docid"""
    print(docs)
    try:
        cursor.execute(docs)
    except Exception as e:
        rows=[]
        connection.rollback()
        flash(f"Unexpected error while fetching result: {e}")
        return render_template("adminResults.html", rows=rows)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    rows.insert(0, columns)
    print(rows)
    return render_template('adminResults.html', rows=rows)

@admin.route("/avg_fine", methods=["GET"]) # average fine paid by the borrowers by branch in a time period
#@login_required
def avg_fine():
    from_date = request.args.get('from_date', '2022-12-01')
    to_date = request.args.get('to_date', '2022-12-31')
    selected_txns = f"""SELECT BOR_NO, GREATEST(0, (date_part('day', rdtime) - date_part('day', bdtime) - 20))*0.20 as fine 
                    from BORROWING where RDTIME is not NULL and
                    BDTIME BETWEEN to_date('{from_date}','YYYY-MM-DD') 
                    AND to_date('{to_date}','YYYY-MM-DD')"""
    fines_query = f"""SELECT BID, avg(fine) as Average_Fine from BORROWS BR
                    JOIN ({selected_txns}) as sel
                    on BR.bor_no = sel.bor_no
                    GROUP BY BID
                    ORDER BY BID asc"""
    branch_query = f"""SELECT B.bid, b.lname as name, b.location as location, Average_Fine from Branch B
                    JOIN ({fines_query}) as fin
                    on B.bid = fin.bid"""
    try:
        cursor.execute(branch_query)
    except Exception as e:
        rows=[]
        connection.rollback()
        flash(f"Unexpected error while fetching result: {e}")
        return render_template("adminResults.html", rows=rows)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    rows.insert(0, columns)
    print(rows)
    return render_template('adminResults.html', rows=rows)

@admin.route("/fbib", methods=["GET"]) # Get the N most frequent borrowers in branch I.
#@login_required
def most_freq_borrowers_in_branch():
    limit = request.args.get('n', '10')
    id = request.args.get('id')
    freq_query = f"""SELECT rid, count(*) as doc_count from borrows BS
                WHERE bid={id}
                GROUP BY rid
                ORDER BY count(*) DESC
                LIMIT {limit}"""
    docs = f"""SELECT R.rid, R.rname, R.rtype, R.raddress, R.phone_no, doc_count from reader R
              JOIN ({freq_query}) as freq
              ON R.rid = freq.rid"""
    try:
        cursor.execute(docs)
    except Exception as e:
        rows=[]
        connection.rollback()
        flash(f"Unexpected error while fetching result: {e}")
        return render_template("adminResults.html", rows=rows)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    rows.insert(0, columns)
    print(rows)
    return render_template('adminResults.html', rows=rows)

# Get the top N most frequent borrowers in the library and the number of books borrowed.
@admin.route("/freq_borrowers", methods=["GET"])
#@login_required
def freq_borrowers():
    limit = request.args.get('n', '10')
    freq_query = f"""SELECT rid, count(*) as doc_count from borrows BS
                GROUP BY rid
                ORDER BY count(*) DESC
                LIMIT {limit}"""
    docs = f"""SELECT R.rid, R.rname, R.rtype, R.raddress, R.phone_no, doc_count from reader R
              JOIN ({freq_query}) as freq
              ON R.rid = freq.rid"""
    try:
        cursor.execute(docs)
    except Exception as e:
        rows=[]
        connection.rollback()
        flash(f"Unexpected error while fetching result: {e}")
        return render_template("adminResults.html", rows=rows)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    rows.insert(0, columns)
    print(rows)
    return render_template('adminResults.html', rows=rows)

@admin.route("/mbib", methods=["GET"]) # Get the N most borrowed books in branch I.
#@login_required
def most_borrowed_in_branch():
    limit = request.args.get('n', '10')
    id = request.args.get('id')
    freq_query = f"""SELECT docid, count(*) as doc_count from borrows BS
                WHERE bid={id}
                GROUP BY docid
                ORDER BY count(*) DESC
                LIMIT {limit}"""
    docs = f"""SELECT D.docid, D.title, doc_count from document D
              JOIN ({freq_query}) as freq
              ON D.docid = freq.docid"""
    try:
        cursor.execute(docs)
    except Exception as e:
        rows=[]
        connection.rollback()
        flash(f"Unexpected error while fetching result: {e}")
        return render_template("adminResults.html", rows=rows)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    rows.insert(0, columns)
    print(rows)
    return render_template('adminResults.html', rows=rows)

@admin.route("/branch", methods=["GET"]) # Print branch information (name and location). 
#@login_required
def branch():
    id = request.args.get('id')
    query = f"""Select * from Branch where bid={id};"""
    try:
        cursor.execute(query)
    except Exception as e:
        rows=[]
        connection.rollback()
        flash(f"Unexpected error while fetching result: {e}")
        return render_template("adminResults.html", rows=rows)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    rows.insert(0, columns)
    print(rows)
    return render_template('adminResults.html', rows=rows)

@admin.route("/reader", methods=["POST"]) # Add new reader. 
#@login_required
def reader():
    form_data = {}
    form_data['rtype'] = request.form.get('rtype')
    form_data['rname'] = request.form.get('rname')
    form_data['raddress'] = request.form.get('raddress')
    form_data['phone_no'] = request.form.get('phone_no')
    fields = ["rtype", "rname", "raddress", "phone_no"]
    for field in fields:
        if not request.form.get(field):
            flash(f"{field} is a mandatory field", "danger")
            return render_template('adminHome.html')
        form_data[field] = request.form.get(field)
    print(form_data)
    try:
        query= f"""INSERT INTO READER({','.join(fields)}) VALUES
                        ('{form_data['rtype']}', '{form_data['rname']}', 
                         '{form_data['raddress']}','{form_data['phone_no']}');"""
                         
        print(query)
        cursor.execute(query)
        flash("Added New Reader", "success")
    except Exception as e:
        print(tb.format_exc)
        connection.rollback()
        flash(f"Unexpected error while trying to add reader: {e}", "danger")
    return render_template('adminHome.html')

@admin.route("/search", methods=["GET"]) # Search document copy and check its status.  
#@login_required
def search():
    docid = request.args.get('docid')
    copyno = request.args.get('copynum')
    reserve_query = f"""SELECT docid, copyno, bid, dtime as tx_time, NULL as ret_time, 'RESERVED' as status  from RESERVES R
                        JOIN RESERVATION RI ON R.reservation_no = RI.res_no and R.docid = {docid} and R.copyno = {copyno}"""
    borrow_query = f"""SELECT docid, copyno, bid, bdtime as tx_time, rdtime as ret_time, 'BORROWED' as STATUS from BORROWS B
                      JOIN BORROWING BI ON B.bor_no = BI.bor_no and B.docid = {docid} and B.copyno = {copyno} and BI.rdtime is null"""
    docs = f"""  SELECT sub1.docid as "Doc ID", sub1.copyno as "COPY_NO", title as "Title",
                 location as "BranchLocation", tx_time as "Borrowed On", ret_time as "Returned On",
                 status from 
                (({reserve_query}) UNION ({borrow_query})) as sub1
                JOIN DOCUMENT D on D.docid={docid}
                JOIN BRANCH B ON sub1.bid = B.bid
                """
    try:
        cursor.execute(docs)
        rows = cursor.fetchall()
        if not rows:
            cursor.execute(f"""SELECT title as DOC_TITLE, copyno as COPY_NO, B.lname, NULL as tx_time,
                            NULL as ret_time, 'AVAILABLE' as status from 
                           (SELECT docid, copyno, BR.bid from COPY C
                           JOIN BRANCH BR
                           on BR.bid = C.bid and C.docid = {docid} and C.copyno={copyno}) as sub
                           JOIN BRANCH B ON sub.bid = B.bid
                           JOIN DOCUMENT D on D.docid = {docid}
                           """)
            rows = cursor.fetchall()
    except Exception as e:
        rows=[]
        connection.rollback()
        flash(f"Unexpected error while fetching status: {e}")
        return render_template("adminResults.html", rows=rows)
    columns = [desc[0] for desc in cursor.description]
    rows.insert(0, columns)
    print(rows)
    return render_template('adminResults.html', rows=rows)

@admin.route("/api_1", methods=["POST"]) # Add a document copy.   
#@login_required
def api_1():
    bid_value = request.args.get('bid_value')
    print(bid_value)
    return render_template('adminResults.html')

@admin.route("/api_2", methods=["POST"]) # Add a document copy.   
#@login_required
def api_2():
    bid_value = request.args.get('bid_value')
    print(bid_value)
    return render_template('adminResults.html')