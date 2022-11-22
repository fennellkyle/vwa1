from flask import request, redirect, url_for, flash, session
from flask import render_template
from flask_login import login_user, logout_user

from forms import RegistrationForm, LoginForm
from main import app, db
from models import User


@app.route("/register", methods=["GET", "POST"])
def register():
	form = RegistrationForm(request.form)
	lform = LoginForm(request.form)
	if request.method == "POST" and form.validate():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		login_user(user)
		session["username"] = form.username.data
		flash("Thanks for registering")
		return redirect(url_for("index"))
	return render_template("register.html", form=form, lform=lform)


@app.route("/login", methods=["POST"])
def login():
	lform=LoginForm(request.form)
	if lform.validate():
		user = element = db.session.execute(db.select(User).filter_by(username=lform.username.data)).scalar()
		if user and user.check_password(password=lform.password.data):
			login_user(user)
			session["username"] = lform.username.data
			flash("Success!")
			return redirect(url_for("index"))
	return redirect(url_for("register"))


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("index"))
