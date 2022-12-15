import io
import csv
import traceback
from flask import Blueprint, render_template, request, redirect, flash

admin = Blueprint('admin', __name__, url_prefix='/admin',
                   template_folder='templates')

# @admin.route("/import", methods=["GET","POST"])
# def document():
#     pass

@admin.route("/home_page", methods=["GET"])
def home_page():
    return render_template('adminHome.html')

@admin.route("/most_borrowed", methods=["GET"]) # most borrowed books
def most_borrowed():
    n_value = request.args.get('n_value')
    print(n_value)
    return render_template('adminResults.html')

@admin.route("/most_popular", methods=["GET"]) # most popular books of a year
def most_popular():
    year_value = request.args.get('year_value')
    print(year_value)
    return render_template('adminResults.html')

@admin.route("/avg_fine", methods=["GET"]) # average fine paid by the borrowers by branch in a time period
def avg_fine():
    st_value = request.args.get('st_value')
    print(st_value)
    end_value = request.args.get('end_value')
    print(end_value)
    return render_template('adminResults.html')

@admin.route("/most_borrowed_in_branch", methods=["GET"]) # Get the N most borrowed books in branch I.
def most_borrowed_in_branch():
    n_value = request.args.get('n_value')
    print(n_value)
    i_value = request.args.get('i_value')
    print(i_value)
    return render_template('adminResults.html')

# Get the top N most frequent borrowers in the library and the number of books borrowed.
@admin.route("/freq_borrowers", methods=["GET"])
def freq_borrowers():
    n_value = request.args.get('n_value')
    print(n_value)
    return render_template('adminResults.html')

@admin.route("/api_5", methods=["GET"]) # Get the N most borrowed books in branch I.
def api_5():
    n_value = request.args.get('n_value')
    print(n_value)
    i_value = request.args.get('i_value')
    print(i_value)
    return render_template('adminResults.html')

@admin.route("/api_4", methods=["GET"]) # Print branch information (name and location). 
def api_4():
    bid_value = request.args.get('bid_value')
    print(bid_value)
    return render_template('adminResults.html')

@admin.route("/api_3", methods=["POST"]) # Add new reader. 
def api_3():
    bid_value = request.args.get('bid_value')
    print(bid_value)
    return render_template('adminResults.html')

@admin.route("/api_2", methods=["POST"]) # Search document copy and check its status.  
def api_2():
    bid_value = request.args.get('bid_value')
    print(bid_value)
    return render_template('adminResults.html')

@admin.route("/api_1", methods=["GET"]) # Add a document copy.   
def api_1():
    bid_value = request.args.get('bid_value')
    print(bid_value)
    return render_template('adminResults.html')