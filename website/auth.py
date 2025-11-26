from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('No account found with that email.', category='error')
        elif not check_password_hash(user.password, password):
            flash('Incorrect password. Please try again.', category='error')
        else:
            remember = bool(request.form.get('remember'))
            login_user(user, remember=remember)
            # flash('Logged in successfully.', category='success')
            return redirect(url_for('aibot.home'))

    # DO NOT FLASH ANYTHING HERE
    return render_template('login.html', user=current_user)



@auth.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You've been logged out. Come back anytime 🤍", category='info')
    return redirect(url_for('auth.login'))



@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        first_name = request.form.get('firstName', '').strip()
        password1 = request.form.get('password1', '')
        password2 = request.form.get('password2', '')

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('An account with that email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be at least 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be at least 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 6:
            flash('Password must be at least 6 characters.', category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1)
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully. You can now log in.', category='success')
            # This is the only place that message is flashed.
            return redirect(url_for('auth.login'))

    return render_template('sign_up.html', user=current_user)
