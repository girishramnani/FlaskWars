__author__ = 'Girish'
from flask import render_template

from app.questions import questions


@questions.route("/")
def register():
    return render_template()

@questions.route("/questions/<int:id>")
def getquestion(id):
    question


