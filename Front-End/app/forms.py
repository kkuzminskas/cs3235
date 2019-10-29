from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField

class LoginForm(Form):
    username = StringField('Username')
    password = StringField('Password')
    submit = SubmitField('Login')