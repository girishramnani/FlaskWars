import os

from flask.ext.login import current_user, login_required
from flask.globals import request
from flask.helpers import flash, url_for
from flask import redirect
from werkzeug.utils import secure_filename

from app.questions.forms import SubmitForm


__author__ = 'Girish'
from flask import render_template
from app.questions import questions
from app.questions.model import Question, Submission

ALLOWED_EXTENSIONS = set(['c', 'cpp', 'py', 'rb', 'java', 'txt'])


@questions.route("/")
def index():
    if current_user.is_authenticated():
        all_questions = Question.query.all()
        print(all_questions)
        return render_template("index.html", all_quest=all_questions)
    flash("you need to login to see the questions", category="warning")
    return redirect(url_for("auth.login"))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@questions.route("/questions/<int:id>")
@login_required
def getquestion(id):
    submitform = SubmitForm()
    selected_question = Question.query.filter(Question.id == id).first()
    return render_template("question.html", question=selected_question, form=submitform)


@questions.route('/questions/<int:id>/submit', methods=('GET', 'POST'))
@login_required
def submit(id):
    print(current_user.username)
    form = SubmitForm()
    if request.method == 'POST':
        file = request.files['code']
        print(os.path.abspath("static"))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("app\\static\\upload", filename))
            flash("your code has been uploaded")
            return redirect(url_for("questions.getquestion", id=id))
        else:
            flash("that file format is not allowed", category="warning")
            return redirect(url_for("questions.getquestion", id=id))


@questions.route('/status/')
def status():
    all_submissions = Submission.query.all()
    return  render_template("status.html",submissions=all_submissions)