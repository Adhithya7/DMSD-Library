import os
import sys
from flask import Flask
from dotenv import load_dotenv

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
print(CURR_DIR)
sys.path.append(CURR_DIR)

load_dotenv()
def create_app(config_filename=''):
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "missing_secret")
    with app.app_context():
        from views.reader import reader
        app.register_blueprint(reader)
        from views.admin import admin
        app.register_blueprint(admin)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
