from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Length
from wtforms.validators import ValidationError

def is_valid_username(username):
    import re
    r = re.fullmatch("^[a-z0-9_-]{2,30}$", username)
    print("re",r)
    if not r:
        print("validation errr")
        raise ValidationError("Invalid username format")

class AuthForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(2, 30)])
    password = PasswordField("password", validators=[DataRequired(), Length(8)])
    def validate_username(form, field):
        print("checking ", field.data)
        is_valid_username(field.data)

class LoginForm(AuthForm):
    submit = SubmitField("Login")
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__( *args, **kwargs)
        if len(self.password.validators) >= 2:
            self.password.validators.pop(1)