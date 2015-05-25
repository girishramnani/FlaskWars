import os
import time
from multiprocessing import Process, Queue

from flask.ext.login import current_user, login_required
from flask.globals import request
from flask.helpers import flash, url_for
from flask import redirect
from sqlalchemy.sql import functions
from app.auth.model import User

from app.questions.forms import SubmitForm, TestForm

from app import db
__author__ = 'Girish'
from flask import render_template
from app.questions import questions
from app.questions.model import Question, Submission

ALLOWED_EXTENSIONS = {'c', 'cpp', 'py', 'rb', 'java', 'txt'}
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
    testform = TestForm()
    selected_question = Question.query.filter(Question.id == id).first()
    return render_template("question.html", question=selected_question, form=submitform, test_form=testform)


def find_score(filename,id,userid):
    """
    the import here is done inside because else a cyclic import situation arrises but as this
    method runs inside another process so the time consumed doesnt matter
    :param filename:
    :param id:
    :return:
    """
    from manage import app
    with app.app_context():
        with open(filename) as file:
            length =len(file.read())
        question = Question.query.filter(Question.id == id).first()
        maxS = question.max_score
        print(length,maxS)
        score = ((maxS-length)/maxS)*100
        if score <1:
            score =1
        submission = Submission(user_id =userid ,question_id=id,\
                                result=True,result_score=score,result_message="Solved")

        db.session.add(submission)
        db.session.commit()
        db.create_all()
        all_submissions = db.session.query(functions.max(Submission.result_score)).group_by(Submission.question_id).all()
        user = User.query.filter(User.id ==userid).first()
        user.total_score=sum((x[0] for x in all_submissions))
        db.session.commit()
        print("done")









@questions.route('/questions/<int:id>/submit', methods=('GET', 'POST'))
@login_required
def submit(id):
    """
    similar to the test submission.
    The code is submitted by this method , it stores the code in the `upload` folder and then finds the score
    :param id:
    :return:
    """
    print(current_user.username)
    form = SubmitForm()
    if request.method == 'POST':
        file = request.files['code']
        print(os.path.abspath("static"))
        if file and allowed_file(file.filename):
            filename = "_".join([current_user.username, str(id), str(int(time.time()))])
            location = os.path.join(UPLOAD_LOCATION, filename)
            file.save(location)
            userid = int(current_user.id)
            code_process= Process(target=find_score,args=(location,id,userid))
            code_process.start()

            flash("your code has been uploaded")
            return redirect(url_for("questions.getquestion", id=id))
        else:
            flash("that file format is not allowed", category="warning")
            return redirect(url_for("questions.getquestion", id=id))


@questions.route('/status/')
def status():
    all_submissions = Submission.query.all()
    all_users = User.query.all()
    all_users_username =[" "]+[user.username for user in all_users ]
    print(all_users_username)

    return render_template("status.html", submissions=all_submissions,allusers = all_users_username)


@questions.route('/submissions/')
@login_required
def status_individual():
    user_submissions = current_user.submissions
    print(user_submissions)
    return render_template("status.html", submissions=user_submissions, ofuser=True)


global_queue = Queue()


def check_similarity(queue, filename1, filename2):
    with open(filename1) as comp_test:
        with open(filename2) as user_test:
            if comp_test.read() == user_test.read():
                queue.put("True")
            else:
                queue.put("False")



@questions.route('/tests/<int:id>', methods=['POST'])
@login_required
def test_check(id):
    '''
    this method takes the test file and saves it to the `tests` folder ,it also spins up a process which stores the
    result in a distributed queue

    TODO - check if multiple requests alienate the queue
    :param id:
    :return:
    '''
    if request.method == "POST":
        selected_question = Question.query.filter(Question.id == id).first()
        filename = selected_question.testcases[0].output_tests
        file_location = os.path.join("app\\static\\tests", filename)

        test_file_name = "_".join([current_user.username, str(selected_question.id), str(int(time.time()))])
        test_file_name += ".txt"
        test_file = request.files['test']
        location = os.path.join("app\\static\\tests\\user_tests", test_file_name)
        test_file.save(location)

        process = Process(target=check_similarity, args=(global_queue, file_location, location))
        process.start()
        data = global_queue.get()
        process.join()
        return data





