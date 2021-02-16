from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user

from grocery_app.models import User
from grocery_app.auth.forms import SignUpForm, LoginForm

from grocery_app import bcrypt
from grocery_app import db

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash("New account sucessfully created.")
        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)

            return redirect(request.args.get('next') or url_for('main.homepage'))

    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))
