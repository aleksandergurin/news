
from flask import Blueprint, render_template, redirect, flash, request
from flask.ext.login import login_user, logout_user, login_required, current_user
from .forms import Signup, Login, Profile, DeleteAccount, ChangePassword
from ..models import User
from ..extensions import db


account = Blueprint("account", __name__, template_folder="../templates")


@account.route("/signup", methods=["GET", "POST"])
def signup():
    form = Signup()
    if request.method == "POST" and form.validate_on_submit():
        user = User()
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        return redirect("/")
    return render_template("account/signup.html", form=form, sel="signup")


@account.route("/login", methods=["GET", "POST"])
def login():
    form = Login(next_page=(request.args.get("next") or "/"))
    if request.method == "POST":
        if form.validate_on_submit():
            username_or_email = form.username_or_email.data
            password = form.password.data
            user = User.query.filter(
                db.or_(
                    User.username == username_or_email,
                    User.email == username_or_email
                )
            ).first()

            if user and user.verify_password(password):
                login_user(user)
                return redirect(form.next_page.data)
        else:
            flash("Incorrect username or password.")
    return render_template("account/login.html", form=form, sel="login")


@account.route("/logout")
@login_required
def session_logout():
    logout_user()
    return redirect("/")


@account.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = Profile()
    form.about.data = current_user.about
    if request.method == "POST" and form.validate_on_submit():
        current_user.email = form.email.data
        current_user.about = form.about.data
        db.session.commit()
        flash("Your account has been successfully updated.")
        return redirect("/profile")
    return render_template("account/profile.html", form=form, sel="profile")


# @account.route("/delete_account", methods=["GET", "POST"])
# @login_required
# def delete_account():
#     form = DeleteAccount()
#     if request.method == "POST" and form.validate_on_submit():
#         user_id = current_user.id
#         logout_user()
#
#         user = User.query.filter_by(id=user_id).first()
#         if user:
#             db.session.delete(user)
#             db.session.commit()
#             return redirect("/")
#     return render_template("account/delete.html", form=form)


@account.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePassword()
    if request.method == "POST" and form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.commit()
            flash("Your password has been successfully changed.")
            return redirect("/profile")
        else:
            flash("Incorrect old password.")
    return render_template("account/change_password.html", form=form)
