from flask.ext.wtf.file import FileField
from flask.ext.wtf.form import Form
__author__ = 'Girish'



class SubmitForm(Form):
    code = FileField("Your code")


