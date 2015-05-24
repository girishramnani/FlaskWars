import os
import time


from flask.ext.login import current_user, login_required
from flask.globals import request
from flask.helpers import flash, url_for
from flask import redirect
from werkzeug.utils import secure_filename

from app.questions.forms import SubmitForm, TestForm


__author__ = 'Girish'
from flask import render_template
from app.questions import questions
from app.questions.model import Question, Submission
import subprocess

ALLOWED_EXTENSIONS = set(['c', 'cpp', 'py', 'rb', 'java', 'txt'])
UPLOAD_LOCATION = os.path.abspath("app\\static\\upload")
TEST_LOCATION = os.path.abspath("app\\static\\tests")

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
    testform= TestForm()
    selected_question = Question.query.filter(Question.id == id).first()
    return render_template("question.html", question=selected_question, form=submitform,test_form=testform)


@questions.route('/questions/<int:id>/submit', methods=('GET', 'POST'))
@login_required
def submit(id):
    print(current_user.username)
    form = SubmitForm()
    if request.method == 'POST':
        file = request.files['code']
        print(os.path.abspath("static"))
        if file and allowed_file(file.filename):
            filename ="_".join([current_user.username,str(id),str(int(time.time()))])

            file.save(os.path.join(UPLOAD_LOCATION, filename))
            flash("your code has been uploaded")
            return redirect(url_for("questions.getquestion", id=id))
        else:
            flash("that file format is not allowed", category="warning")
            return redirect(url_for("questions.getquestion", id=id))


@questions.route('/status/')
def status():
    all_submissions = Submission.query.all()
    return render_template("status.html",submissions=all_submissions)

@questions.route('/submissions/')
@login_required
def status_individual():
    user_submissions =Submission.query.filter(current_user.id == Submission.question_id)
    return render_template("status.html",submissions =user_submissions,ofuser=True)




@questions.route('/tests/<int:id>',methods=['POST'])
@login_required
def test_check(id):
    if request.method=="POST":
        selected_question = Question.query.filter(Question.id == id).first()
        filename = selected_question.testcases[0].output_tests
        test_file_name = "_".join([current_user.username,str(selected_question.id),str(int(time.time()))])
        test_file_name+=".txt"
        test_file = request.files['test']
        location = os.path.join("app\\static\\tests\\user_tests",test_file_name)
        test_file.save(location)

        return "hehaha"





