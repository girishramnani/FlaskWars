__author__ = 'Girish'

from flask.ext.script import Manager

from app import create_app

app = create_app("development")
manager = Manager(app)
from app import db
from app.auth.model import User


@manager.command
def adduser(email, username, admin=True):
    from getpass import getpass

    password = getpass()
    password2 = getpass(prompt="Confirm: ")
    if password != password2:
        import sys

        sys.exit("Error : password do not match")

    db.create_all()
    user = User(email=email, username=username, password=password, is_admin=admin)
    db.session.add(user)
    db.session.commit()
    print("done")


@manager.command
def refresh_db():
    db.create_all()


if __name__ == "__main__":
    manager.run()
