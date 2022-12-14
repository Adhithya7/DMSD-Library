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

@admin.route("/most_borrowed", methods=["GET"])
def most_borrowed():
    n_value = request.args.get('n_value')
    print(n_value)
    return render_template('contact.html')