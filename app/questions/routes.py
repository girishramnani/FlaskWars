__author__ = 'Girish'
from flask import render_template
from app.questions import model
from app.questions import questions


@questions.route("/")
def index():
    return render_template("index.html")

@questions.route("/questions/<int:id>")
def getquestion(id):
    return "hello"


