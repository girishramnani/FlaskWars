from flask.ext.wtf.file import FileField
from flask.ext.wtf.form import Form
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

__author__ = 'Girish'


class SubmitForm(Form):
    code = FileField("Your code", validators=[DataRequired()])
    submit = SubmitField("Upload Code")


class TestForm(Form):
    test = FileField("Your Test output:", validators=[DataRequired()])
    test_submit = SubmitField("Upload Test")


