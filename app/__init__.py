__author__ = 'Girish'
from flask import Flask

from config import config
from flask.ext.bootstrap import Bootstrap
bootstrap = Bootstrap()
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app=Flask(__name__)
    bootstrap.init_app(app)
    db.init_app(app)
    app.config.from_object(config[config_name])
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    from app.questions import questions as questions_blueprint
    app.register_blueprint(questions_blueprint,url_prefix="")
    login_manager.init_app(app)
    print(app.url_map)
    return app


