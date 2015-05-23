from flask.ext.login import current_user
from flask.helpers import flash, url_for
from flask import redirect
__author__ = 'Girish'
from flask import render_template
from app.questions import questions
from app.questions.model import Question

@questions.route("/")
def index():
    if current_user.is_authenticated():
        all_questions = Question.query.all()
        return render_template("index.html",all_quest=all_questions)
    flash("you need to login to see the questions")
    return redirect(url_for("auth.login"))

@questions.route("/questions/<int:id>")
def getquestion(id):
    selected_question = Question.query.filter(Question.id ==id).first()
    return render_template("question.html",question=selected_question)


