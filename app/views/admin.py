import io
import csv
import traceback
from flask import Blueprint, render_template, request, redirect, flash

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route("/import", methods=["GET","POST"])
def document():
    pass