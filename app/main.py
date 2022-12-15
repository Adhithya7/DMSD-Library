import os
import sys
from flask import Flask
from dotenv import load_dotenv
from flask import Flask, session, render_template
import flask_login
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, Principal

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
print(CURR_DIR)
sys.path.append(CURR_DIR)

load_dotenv()

login_manager = flask_login.LoginManager()
def create_app(config_filename=''):
    app = Flask(__name__,
                template_folder='templates')
    app.secret_key = os.environ.get("SECRET_KEY", "missing_secret")
    login_manager.init_app(app)
    with app.app_context():
        from views.reader import reader
        app.register_blueprint(reader)
        from views.admin import admin
        app.register_blueprint(admin)
        from auth.auth import auth
        app.register_blueprint(auth)

        # load the extension
        principals = Principal(app) # must be defined/initialized for identity to work (flask_principal)
        @login_manager.user_loader
        def load_user(user_id):
            if user_id is None:
                return None
            print("login_manager loading user") # happens each request
            from auth.models import User
            if session["_user_id"] == user_id and "user" in session.keys():
                print("loading user from session")
                # load user from session (convert json to User)
                # see User object for convering json of roles to [Roles]
                import jsons
                return jsons.loads(session["user"], User)

        @identity_loaded.connect_via(app)
        def on_identity_loaded(sender, identity):
            # Set the identity user object
            identity.user = current_user
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
