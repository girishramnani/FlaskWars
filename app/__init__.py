from flask.ext.admin.base import Admin
from flask.ext.admin.contrib.sqla.view import ModelView
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

from config import config




# from app.questions.model import Question,TestCase

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
from app.auth.model import User
from app.questions.model import Question, TestCase, Submission
from app.model.modelViewSecure import SecureView

def create_app(config_name):
    app = Flask(__name__)

    bootstrap.init_app(app)
    db.init_app(app)
    admin = Admin(app)
    admin.add_view(SecureView(User, db.session))
    admin.add_view(SecureView(Question, db.session))
    admin.add_view(SecureView(TestCase, db.session))
    admin.add_view(SecureView(Submission, db.session))
    app.config.from_object(config[config_name])
    from app.auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from app.questions import questions as questions_blueprint

    app.register_blueprint(questions_blueprint, url_prefix="")
    login_manager.init_app(app)
    return app
