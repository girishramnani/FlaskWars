from flask.globals import request
from flask.helpers import flash, url_for
from flask import redirect
from app.auth.forms import LoginForm, RegistrationForm
from flask import render_template
from app.auth import auth
from  flask.ext.login import login_user, login_required, logout_user
from app.auth.model import User
from app import db




@auth.route('/login', methods=["GET","POST"])
def login():
    form =LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.verify(form.password.data):
            flash("Invalid email or password")
            return redirect(url_for("auth.login"))
        print("out")
        login_user(user,form.remember_me.data)
        return redirect(url_for("index"))
    return render_template("login.html",forms=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("index"))


@auth.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm(request.form)

    if request.method=="POST":
        if form.validate_on_submit():
            user = User(email=form.data.email,username=form.data.username,password=form.data.password,is_admin=False)
            db.session.add(user)
            db.session.commit()
    return render_template("")

