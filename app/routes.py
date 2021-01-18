"""
Module contains all the view functions which handle different routes.
"""
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm

@app.route('/')
@app.route('/index')
@login_required
def index():
    """Homepage."""
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.jinja', title='Home Page', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Check if the user is already authenticated. If yes: take them to homepage.
    Check if the user submitted a valid login form. If yes: take them to homepage.
    Load the login page form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)        
    return render_template('login.jinja', title='Sign In', form=form)

@app.route('/logout')
def logout():
    """ Handle the user logout using the flask-login extension. """
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Handle the user registration. """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.jinja', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    """ User profile page. """
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.jinja', user=user, posts=posts)