from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from elo_rank.models.users import User

auth = Blueprint("auth", __name__)


@auth.get("/login")
def display_login():
    return render_template("login.html")


@auth.post("/login")
def manage_login():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(
            url_for("auth.display_login")
        )  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for("user.profile"))


@auth.get("/register")
def display_register():
    return render_template("register.html")


@auth.post("/register")
def manage_register():
    from elo_rank import db

    # code to validate and add user to database goes here
    email = request.form.get("email")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    password = request.form.get("password")

    user = User.query.filter_by(
        email=email
    ).first()  # if this returns a user, then the email already exists in database

    if (
        user
    ):  # if a user is found, we want to redirect back to signup page so user can try again
        flash("Email address already exists")
        return redirect(url_for("auth.display_register"))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=generate_password_hash(password, method="scrypt"),
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.display_login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
