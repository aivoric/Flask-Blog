"""
Module contains all the view functions which handle different routes.
"""
from werkzeug.urls import url_parse
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Check if the user is already authenticated. If yes: take them to homepage.
    Check if the user submitted a valid login form. If yes: take them to homepage.
    Load the login page form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        queried_user = User.query.filter_by(username=form.username.data).first()
        if queried_user is None or not queried_user.check_password(form.password.data):
            flash(_('Invalid username or password.'))
            return redirect(url_for('auth.login'))
        login_user(queried_user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)        
    return render_template('auth/login.jinja', title=_('Sign In'), form=form)


@bp.route('/logout')
def logout():
    """ Handle the user logout using the flask-login extension. """
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """ Handle the user registration. """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        queried_user = User(username=form.username.data, email=form.email.data)
        queried_user.set_password(form.password.data)
        db.session.add(queried_user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.jinja', title=_('Register'), form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.jinja',
                           title=_('Reset Password'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
