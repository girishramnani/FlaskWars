from flask.ext.login import current_user, login_required
from flask.helpers import flash, url_for
from flask import redirect
from werkzeug.utils import secure_filename
from app.questions.forms import SubmitForm

__author__ = 'Girish'
from flask import render_template
from app.questions import questions
from app.questions.model import Question

ALLOWED_EXTENSIONS = set(['c', 'cpp', 'py', 'rb', 'java'])

@questions.route("/")
def index():
    if current_user.is_authenticated():
        all_questions = Question.query.all()
        print(all_questions)
        return render_template("index.html",all_quest=all_questions)
    flash("you need to login to see the questions")
    return redirect(url_for("auth.login"))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@questions.route("/questions/<int:id>")
@login_required
def getquestion(id):
    submitform =SubmitForm()
    selected_question = Question.query.filter(Question.id ==id).first()
    return render_template("question.html",question=selected_question,form = submitform)


@questions.route('/questions/<int:id>/submit', methods=('GET', 'POST'))
@login_required
def submit(id):
    print(current_user.username)
    form = SubmitForm()
    if form.validate_on_submit():
        print(form.code.data)
        return "hello"