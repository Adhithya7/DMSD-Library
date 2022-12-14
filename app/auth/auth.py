import traceback as tb
import os

from flask import Blueprint, render_template, flash, redirect, url_for,current_app, session
from auth.forms import LoginForm
from dotenv import load_dotenv
from flask_login import login_user, login_required, logout_user, current_user
from auth.models import User

load_dotenv()

from flask_principal import Identity, AnonymousIdentity, \
     identity_changed

auth = Blueprint('auth', __name__, url_prefix='/',template_folder='../templates')

@auth.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        is_valid = True
        uname = form.username.data
        pwd = form.password.data
        if is_valid:
            try:
                if pwd == os.environ.get('PASSWORD') and uname == os.environ.get('UNAME'):
                    user = User(id = 1, username=uname)
                    success = login_user(user) # login the user via flask_login
                    if success:
                        identity_changed.send(current_app._get_current_object(),
                                identity=Identity(user.id))
                        session["user"] = user.toJson()
                        flash("Log in successful", "success")
                        return redirect(url_for("auth.landing_page"))
                    else:
                        flash("Error logging in", "danger")
                else:
                    flash("Invalid username or password", "warning")
            except Exception as e:
                flash(str(e), "danger")
                print(tb.format_exc())
    return render_template("login.html", form=form)

@auth.route("/logout", methods=["GET"])
def logout():
    logout_user()
     # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    flash("Successfully logged out", "success")
    return redirect(url_for("auth.login"))

@auth.route("/landing-page", methods=["GET","POST"])
@login_required
def landing_page():
    return render_template("adminHome.html")