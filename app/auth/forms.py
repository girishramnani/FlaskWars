from flask.ext.wtf.recaptcha.fields import RecaptchaField
from wtforms.fields.core import StringField, BooleanField
from wtforms.fields.simple import PasswordField, SubmitField, TextField
from wtforms.validators import Required, DataRequired, Length, Email, EqualTo

__author__ = 'Girish'

from flask.ext.wtf import Form

class LoginForm(Form):
    email = StringField("Email",validators=[DataRequired("Cannot be empty"),Length(1,64),Email()])
    password= PasswordField("Password",validators=[DataRequired("Cannot be empty")])
    remember_me =BooleanField("Keep me logged in")
    submit = SubmitField("log In")


class RegistrationForm(Form):
    username = StringField('Username', validators=[Length(min=4, max=25)])
    email = StringField('Email Address', validators = [Length(min=6, max=35)])
    password = PasswordField('New Password', validators= [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept that the code submitted can be used for any external purposes', [DataRequired()])
    submit = SubmitField("Register")