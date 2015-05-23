from flask.ext.login import current_user
from flask.helpers import flash, url_for
from flask import redirect
__author__ = 'Girish'
from flask import render_template
from app.questions import questions


@questions.route("/")
def index():
    if current_user.is_authenticated():
        return render_template("index.html")
    flash("you need to login to see the questions")
    return redirect(url_for("auth.login"))

@questions.route("/questions/<int:id>")
def getquestion(id):
    return "hello"


