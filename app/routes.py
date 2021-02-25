"""
Module contains all the view functions which handle different routes.
"""
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm, EditProfileForm

@app.before_request
def before_request():
    """Update last_seen every time a user makes a server request."""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

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
        queried_user = User.query.filter_by(username=form.username.data).first()
        if queried_user is None or not queried_user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        login_user(queried_user, remember=form.remember_me.data)
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
        queried_user = User(username=form.username.data, email=form.email.data)
        queried_user.set_password(form.password.data)
        db.session.add(queried_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.jinja', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    """ User profile page. """
    queried_user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': queried_user, 'body': 'Test post #1'},
        {'author': queried_user, 'body': 'Test post #2'}
    ]
    return render_template('user.jinja', user=queried_user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """ Page where user can edit their username and about me. 
    First check if a form was submitted (POST request), and try to handle that. Upon
    success, keep the user on the same page and flash an appropriate message.
    If the request was a GET, then get the user's username and about me, and render
    the form.
    """
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.jinja', title='Edit Profile',
                           form=form)
