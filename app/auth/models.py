from flask_login import UserMixin
from auth.utils import JsonSerializable

class User(UserMixin, JsonSerializable):
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.authenticated = False
    def is_active(self):
        return self.is_active()
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return self.authenticated
    def is_active(self):
        return True
    def get_id(self):
        return str(self.id)