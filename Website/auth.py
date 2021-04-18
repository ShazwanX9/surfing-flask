from flask import Blueprint, render_template, url_for, redirect, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .dbmodel import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

##############################################################################

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('psw')
        remember  = request.form.get("remember")

        user = User.query.filter_by(username=username).first()
        # print(user, user.password, password)
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=bool(remember))
                return redirect(url_for('view.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')


    return render_template ( 
                        "login.html", 
                        headerBgPath    = "static/BackgroundImages/" + "bg2.jpg", 
                        headerFgColor   = "#66ff33",
                        bgColor         = "#00fce",
                        user            = current_user
                        )

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=["GET", "POST"])
def signUp():
    if request.method == "POST":
        email     = request.form.get("email")
        username  = request.form.get("username")
        password1 = request.form.get("psw")
        password2 = request.form.get("psw-repeat")
        remember  = request.form.get("remember")
        # print(email, username, password1, remember, sep="\n")

        user = User.query.filter_by(username=username).first()
        if user:
            flash("User Already EXIST!", category="error")
        elif '@' not in email:
            flash("Email is NOT Valid!", category="error")
        elif password1 != password2:
            flash("Password didn't Match", category="error")
        elif len(password1) < 3 :
            flash("Password is too short. Password need to be at least 3 character", category="error")
        elif len(username) < 3 :
            flash("Username is too short. Username need to be at least 3 character", category="error")
        else:
            new_user = User(
                            email=email, 
                            username=username, 
                            password=generate_password_hash(
                                        password1, 
                                        method='sha256'
                                     )
                            )
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=bool(remember))
            flash('Account created!', category='success')
            return redirect(url_for("view.home"))

    return render_template ( 
                        "sign-up.html", 
                        headerBgPath    = "static/BackgroundImages/" + "bg3.jpg", 
                        headerFgColor   = "#66ff33",
                        bgColor         = "#00fce",
                        user            = current_user
                        )

@auth.route("/test")
def test():
    return "<p>test</p>"

@auth.route("/<name>")
def user(name):
    # return f"Hello {name}!"
    return redirect(url_for("view.home"))
